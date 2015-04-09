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


def write_results(d, lang, results):
    pass
