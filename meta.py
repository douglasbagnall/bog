import json
import os
import errno
import numpy as np
import pickle


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


def makepath(*fragments):
    fn = os.path.join(*fragments)
    d = os.path.dirname(fn)
    try:
        os.makedirs(d)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise
    return fn


def write_clusters_json(clusters, docnames, output_dir, problem,
                        tag=None):
    json_clusters = []
    for cluster in clusters:
        json_clusters.append([{'document': docnames[x]} for x in cluster])

    fn = "clustering.json"
    if tag:
        fn = '%s-%s' % (tag, fn)
    ffn = makepath(output_dir, problem, fn)
    f = open(ffn, 'w')
    json.dump(json_clusters, f, indent=4)
    f.close()


def write_attractions_json(attractions, docnames, output_dir, problem,
                           tag=None):
    low = np.amin(attractions)
    high = np.amax(attractions)
    scale = 0.999999 / (high - low)
    scores = (attractions - low) * scale
    json_pairs = []

    for x in range(attractions.shape[0]):
        for y in range(x + 1, scores.shape[0]):
            json_pairs.append({'document1': docnames[x],
                               'document2': docnames[y],
                               'score': scores[x, y]})
    fn = "ranking.json"
    if tag:
        fn = '%s-%s' % (tag, fn)
    ffn = makepath(output_dir, problem, fn)
    f = open(ffn, 'w')
    json.dump(json_pairs, f, indent=4)
    f.close()


def write_results(docnames, problem, affinities,
                  clusters, d, tag=None):
    print len(clusters), clusters
    write_clusters_json(clusters, docnames, d, problem, tag=tag)
    write_attractions_json(affinities, docnames, d, problem, tag=tag)

# opinions should be like this:
# problems, affinities, names, control_texts, control_models
# problems:      dict (string => lists of lists)
# affinities     dict (string => numpy array)
# names          dict (string => list of string)
# control_texts  dict (string => nx1 numpy array)
# control_models dict (string => 1xn numpy array)
#
# All dicts should be the same size

def save_opinions(dest, *opinions):
    makepath(dest)
    f = open(dest, 'w')
    pickle.dump(opinions, f)
    f.close()


def load_opinions(src):
    makepath(src)
    f = open(src)
    opinions = pickle.load(f)
    f.close()
    return opinions
