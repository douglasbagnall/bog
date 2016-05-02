import json
import os
from colour import print_GREEN, print_YELLOW, print_CYAN, RED


def load_clustering_json(fn):
    f = open(fn)
    raw_clusters = json.load(f)
    f.close()
    documents = set()
    clusters = []
    for cluster in raw_clusters:
        cluster = frozenset(x['document'] for x in cluster)
        clusters.append(cluster)
        documents.update(cluster)

    return documents, clusters


def load_ranking_json(fn):
    f = open(fn)
    raw_pairs = json.load(f)
    f.close()
    links = []
    for pair in raw_pairs:
        d1 = pair['document1']
        d2 = pair['document2']
        score = pair['score']
        if d1 > d2:
            d2, d1 = d1, d2
        links.append((score, (d1, d2)))

    links.sort(reverse=True)
    return links


def load_ground_truths(srcdir):
    truths = {}
    for d, dirnames, filenames in os.walk(srcdir):
        pid = os.path.basename(d)
        pid_truths = truths.setdefault(pid, {})
        for fn in filenames:
            ffn = os.path.join(d, fn)
            if fn == 'ranking.json':
                pid_truths['ranking'] = load_ranking_json(ffn)

            elif fn == 'clustering.json':
                docs, clustering = load_clustering_json(ffn)
                pid_truths['clustering'] = clustering
                pid_truths['documents'] = docs

    return truths


def avg_precision(d, pairs, truth):
    precision = 0.0
    count = 0.0
    correct = 0.0
    truth = set(x for x in truth if d in x)
    for pair in pairs:
        if d not in pair:
            continue
        count += 1.0
        if pair in truth:
            correct += 1.0
            precision += correct / count
            if correct == len(truth):
                break

    return precision / correct


def calc_map_individual(links, truth, documents):
    true_links = set(p for s, p in truth)
    true_docs = set()
    for d1, d2 in true_links:
        true_docs.add(d1)
        true_docs.add(d2)

    pairs = {}
    for s, p in sorted(links, reverse=True):
        p1, p2 = p
        if p1 in true_docs:
            pairs.setdefault(p1, []).append(p)
        if p2 in true_docs:
            pairs.setdefault(p2, []).append(p)

    score = 0.0
    for d in true_docs:
        score += avg_precision(d, pairs[d], true_links)

    return score / len(documents)


def calc_map(links, truth):
    if not truth or not links:
        return 0.0
    true_links = set(p for s, p in truth)
    count = 0.0
    correct = 0.0
    score = 0.0
    for s, p in sorted(links, reverse=True):
        count += 1.0
        if p in true_links:
            correct += 1.0
            score += correct / count
            if correct == len(true_links):
                break

    return score / len(true_links)


def print_links(links, truth, documents):
    links = sorted(links, reverse=True)
    true_links = set(x[1] for x in truth)
    self_links = [(x, x) for x in documents]
    n = 0
    i = 0
    bad_run = []
    for score, pair in links:
        i += 1
        spair = '--'.join(str(x)[-8:-4] for x in pair)
        if pair in self_links or pair in true_links:
            if bad_run:
                print("...skipped %d false links %.3f-%.3f" % (len(bad_run),
                                                               bad_run[0],
                                                               bad_run[-1]))
                bad_run = []
            if pair in true_links:
                print_GREEN("%.3f %s TRUE link" % (score, spair))
                n += 1
                if n == len(true_links):
                    print_CYAN("all true links found after %d of %d" %
                               (i, len(links)))
                    print("...skipping %d false links" % (len(links) - i))
                    break
            else:
                print_YELLOW("%.3f %s SELF link" % (score, spair))
        else:
            bad_run.append(score)
