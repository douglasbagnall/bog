# Copyright 2016 Douglas Bagnall <douglas@halo.gen.nz>
# -*- coding: utf-8 -*-
import os
import unicodedata
import re
from collections import Counter
from hashlib import sha1

import mappings
import meta

HERE = os.path.dirname(__file__)
TRAINING_CORPUS = os.path.join(HERE,
        'corpus/pan16-author-clustering-training-dataset-2016-02-17/')
CONTROL_CORPUS = os.path.join(HERE,
                              'corpus/control/')

VALIDATION_CORPUS = os.path.join(HERE,
                                 'corpus/validation/')


def always(x):
    return True


def read_file(fn):
    f = open(fn)
    text = f.read()
    f.close()
    return text


def get_text_and_id(fn, lang, raw=False):
    text = read_file(fn)
    if not raw:
        remap = mappings.get_charmap(lang)
        text = remap(text)
    tid = sha1(text).hexdigest()
    return text, tid


def load_control_texts(srcdir, lang, ext='.txt'):
    """load the texts, deduplicating along the way."""
    texts = {}
    records = []
    srcdir = os.path.join(srcdir, lang)
    for d, dirnames, filenames in os.walk(srcdir, followlinks=True):
        for fn in filenames:
            if fn.endswith(ext):
                ffn = os.path.join(d, fn)
                text, tid = get_text_and_id(ffn, lang)
                texts[tid] = text
                records.append((fn, ffn, tid))

    return texts, records


def load_problem_texts(srcdir, lang, raw=False, ext='.txt'):
    """load the texts, remapping and deduplicating along the way."""
    texts = {}
    records = []
    for fn in sorted(os.listdir(srcdir)):
        if fn.endswith(ext):
            ffn = os.path.join(srcdir, fn)
            text, tid = get_text_and_id(ffn, lang, raw)
            texts[tid] = text
            records.append((fn, ffn, tid))

    return texts, records


def load_corpus(srcdir, lang, raw=False):
    dirs = meta.read_lang_info(srcdir, lang)
    texts = {}
    problems = {}
    for d in dirs:
        fulldir = os.path.join(srcdir, d)
        d_texts, records = load_problem_texts(fulldir, lang, raw)
        problems[d] = records
        texts.update(d_texts)

    return texts, problems


def concat_corpus(srcdir, lang, raw=False):
    texts, problems = load_corpus(srcdir, lang, raw)
    return '\n'.join(texts.values())


def count_chars(text, decompose=False):
    text = text.decode('utf-8')
    if decompose:
        text = unicodedata.normalize('NFKD', text)
    else:
        text = unicodedata.normalize('NFKC', text)
    c = Counter(text)
    return c.most_common()


# Charmaps always discard these
dispensible_chars = set('\x0b\x0c\r'.decode('utf8') + u'\ufeff\xad\x85' +
                        u'\u2028\\_')

# Charmaps discard these unless really common.
discountable_chars = {k: 0.25 for k in '+=<>|%'}

single_quotes = set("'‘’‘‘".decode('utf8') + u'\u2018')

double_quotes = set('‟"„“”'.decode('utf8'))


def unify_case(text):
    # trickier than .lower() because of the decomposed case marker
    text = text.lower()
    return text.replace("¹".decode('utf8'), "")


def split_words(text, ignore_case=False):
    if not isinstance(text, unicode):
        text = text.decode('utf8')
    if ignore_case:
        text = unify_case(text)
    text = re.sub(r"(?<=\w)'(?=\w)", r"³".decode('utf8'),
                  text, flags=re.U)
    words = re.split(r"[^\w³-]+".decode('utf8'), text, flags=re.U)
    words = sum((w.split('--') for w in words), [])
    words = [x.strip('-_') for x in words]
    return [x for x in words if x]


def decode_split_word(w):
    return w.replace('³'.decode('utf8'), "'")


def print_word_counts(c):
    prev_n = None
    for w, n in c.most_common():
        if n != prev_n:
            print "\n------------- %s --------------" % n
            prev_n = n
        w = decode_split_word(w)
        print w,
    print
    print len(c)
