import json
import os


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


def avg_precision(d, n, links, truth):
    precision = 0.0
    count = 0.0
    correct = 0.0
    for score, pair in links:
        if d not in pair:
            continue
        count += 1.0
        if pair in truth:
            correct += 1.0
        precision += correct / count
        if correct == len(truth):
            break

    return precision / count


def calc_map(links, truth, documents):
    true_links = set(x[1] for x in truth)
    score = 0.0
    for d in documents:
        score += avg_precision(d, len(documents), links, true_links)

    return score / len(documents)


def calc_map2(links, truth, documents):
    true_links = set(x[1] for x in truth)

    records = {}
    for d in documents:
        records[d] = [0.0, 0.0, 0.0, 0.0]
        links = set(x for x in true_links if d in x)
        records[d].append(links)
        records[d].append(len(links))

    for _, pair in links:
        for d in pair:
            record = records[d]
            precision, count, correct, links, n_links = record
            if correct == n_links:
                continue
            count += 1.0
            if pair in links:
                correct += 1.0
            precision += correct / count
            records[d] = [precision, count, correct, links, n_links]

    for d in documents:
        score += records[d][0]

    return score / len(documents)
