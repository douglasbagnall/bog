import json
import os

def read_info_json(d):
    """An example:

     [ {"language": "en",
        "genre": "articles",
        "folder": "problem001"},
       ...
     ]

    return list of (dir, lang, genre) tuples.
    """
    f = open(os.path.join(d, "info.json"))
    raw_info = json.load(f)
    f.close()
    info = []
    for x in raw_info:
        info.append((x['folder'], x['language'], x['genre']))
    return info


def read_lang_info(d, lang):
    dirs = []
    for subdir, d_lang, genre in read_info_json(d):
        if lang == d_lang:
            dirs.append(subdir)
    return dirs


def makepath(fragments):
    fn = os.path.join(*fragments)
    d = os.path.dirname(fn)
    try:
        os.makedirs(d)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise
    return fn


def write_clusters_json(clusters, *dirpath):
    json_clusters = []
    for cluster in clusters:
        json_clusters.append([{'document': x} for x in cluster])

    fn = makepath(dirpath + ("clustering.json",))
    f = open(fn, 'w')
    json.dump(f, json_clusters, indent=4)
    f.close()


def write_attractions_json(attractions, *dirpath):
    json_pairs = []
    for a, b, p in attractions:
        json_pairs.append({'document1': a,
                           'document2': b,
                           'score': p})
    fn = makepath(dirpath + ("ranking.json",))
    f = open(fn, 'w')
    json.dump(f, json_pairs, indent=4)
    f.close()


def write_results(d, lang, title, affinities, clusters):
    write_clusters_json(clusters, d, title, lang)
    write_attractions_json(affinities, d, title, lang)
