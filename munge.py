#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import numpy as np
from itertools import combinations
from meta import makepath
import math
import os

def write_normalised_png(a, fn, verbose=False):
    from PIL import Image
    hi = np.amax(a)
    lo = np.amin(a)
    scale = 255.9 / (hi - lo)
    b = (a - lo) * scale
    c = np.array(b, dtype='uint8')
    if verbose:
        print fn
        print "low %f high %f scale %f" % (lo, hi, scale)
        print "b min %f b max %f" % (np.amin(b), np.amax(b))
        print "c min %d b max %d" % (np.amin(c), np.amax(c))
    im = Image.fromarray(c)
    makepath(fn)
    im.save(fn)


def clip_range(x, extreme):
    x = np.maximum(x, -extreme)
    x = np.minimum(x, extreme)
    return x


def clipped_neg_exp(raw_affinities):
    x = clip_range(raw_affinities, 40)
    return np.exp(-x)


def clipped_logistic(raw_affinities):
    x = clip_range(raw_affinities, 40)
    return 1.0 / (1.0 + np.exp(x * -3.0))


def links_to_clusters(links):
    n = links.shape[0]
    clusters = [set([x]) for x in range(n)]

    for a, b in zip(*np.where(links)):
        if clusters[a] is not clusters[b]:
            c1, c2 = clusters[a], clusters[b]
            c1.update(c2)
            for x in c2:
                clusters[x] = c1

    return set(frozenset(x) for x in clusters)


def data_to_clusters(data, threshold, names=None):
    links = data > threshold
    clusters = links_to_clusters(links)
    if names is None:
        return clusters

    clusters_d = {}
    for c in clusters:
        k = min(c)
        if names:
            clusters_d[k] = frozenset(names[x] for x in c)
        else:
            clusters_d[k] = c
    return clusters_d


def p_to_affinities(input, samples=1000):
    """Treat the input array as a (somehow) scaled probability that two
    nodes are linked. The probability that they're in the same cluster
    has a transitive element.
    """
    totals = np.zeros_like(input)
    scale = 0.1
    min_scale = 1e-20
    max_scale = 1.0 / (1e-3 + np.min(input))
    runs = samples
    while runs > 0:
        scale = random.uniform(min_scale, max_scale)

        r = np.random.random(input.shape)
        p = input * scale
        links = r < p
        clusters = links_to_clusters(links)

        if len(clusters) == 1:
            # everything is connected, so the scale is too high
            # make sure we don't go higher.
            max_scale = (scale + max_scale) * 0.5
            continue

        if len(clusters) == input.shape[0]:
            # nothing is connected
            min_scale = (scale + 3 * min_scale) * 0.25
            continue

        for c in clusters:
            z = np.zeros(totals.shape[0])
            c = np.array(sorted(c), dtype=int)
            z[c] = 1
            for y in c:
                totals[y] += z

        runs -= 1
    totals *= 1.0 / (np.amax(totals) + 1e-10)
    return totals


def shuffle_array(a):
    # np.random.shuffle does only one dimension.
    shape = a.shape
    a = a.flatten()
    np.random.shuffle(a)
    return a.reshape(shape)


def array_to_link_pairs(a, names, include_self=False):
    """make a sorted list of links from the top triangle of an array."""
    links = []
    no_self = int(not include_self)
    n = a.shape[0]
    for i in range(n):
        for j in range(i + no_self, n):
            links.append((a[i, j], (names[i], names[j])))
    return links


# Connecting

def cluster_aware_scoring(links, names, depth=3):
    doc_indices = {d: i for i, d in enumerate(names)}
    pairs = sorted(links, reverse=True)
    affinities = {x: {} for x in names}
    scores = {p:s for s, p in pairs}
    multiples = [pairs]
    for i in range(depth - 2):
        print "looking at (3+%d)-uples" % i
        prevuple = multiples[-1]
        newuple = []
        multiples.append(newuple)
        for s, p in prevuple:
            j = doc_indices[p[-1]] + 1
            for new_d in names[j:]:
                new_s = s
                for d in p:
                    new_s += scores[(d, new_d)]
                newuple.append((new_s, p + (new_d,)))

    for i, uple in enumerate(multiples):
        uple.sort(reverse=True)
        # n! / r! / (n-r)!
        scale = 2.0 / ((i + 2) * (i + 1))
        uple = [(s * scale, p) for s, p in uple]
        s, p = uple[0]
        print "%d: %d, best %s %.3f" % (len(p), len(uple), p, s)

    alluple = []
    for x in multiples:
        alluple.extend(x)
    alluple.sort(reverse=True)
    used_links = set()
    out = []
    for s, uple in alluple:
        for p in combinations(uple, 2):
            if p in used_links:
                continue
            used_links.add(p)
            out.append((s, p))
    return out


def links_to_matrix(links, names):
    """make a symmetric array from a set of links."""
    n = len(names)
    doc_indices = {d: i for i, d in enumerate(names)}

    a = np.zeros((n, n))
    for s, p in links:
        d1, d2 = p
        x = doc_indices[d1]
        y = doc_indices[d2]
        a[x, y] = s
        a[y, x] = s
    return a


def cluster_aware_matrix(data, names):
    links = array_to_link_pairs(data, names)
    links = cluster_aware_scoring(links, names)
    return links_to_matrix(links, names)


def text_length_penalty(data, names, dirname):
    """reduce the score of short texts and their models (towards zero),
    because they can't be certain about anything.
    """
    files = os.listdir(dirname)
    if sorted(files) != sorted(names):
        print set(files) - set(names)
        print set(names) - set(files)
        raise ValueError("the files don't match")
    penalty = []
    for fn in names:
        s = os.stat('%s/%s' % (dirname, fn)).st_size
        penalty.append(1.0 - 2.0 / math.log(s))

    p = np.array(penalty)
    p2 = p.reshape(p.shape + (1,))

    data *= p
    data *= p2

    return data
