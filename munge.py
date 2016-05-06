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

    named_clusters = set()
    for c in clusters:
        named_clusters.add(frozenset(names[x] for x in c))
    return named_clusters


def p_to_affinities(input, samples=3000):
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


def add_to_cluster(p, linkmap, p2, scores):
    #print "adding %s to %s" % (p, c)
    c = linkmap[p2]
    s, x = c
    if p not in x:
        for y in x:
            s += scores[(p, y)]
        x.add(p)
        c[0] = s
    linkmap[p] = c
    n = len(x)
    scale = 2.0 / ((n + 2) * (n + 1))
    return s * scale


def array_to_link_pairs_cluster_aware(a, names, power=1.0):
    """make a sorted list of links from the top triangle of an array."""
    links = array_to_link_pairs(a, names, True)
    pairs = [(s ** power, p) for s, p in links if p[0] != p[1]]
    pairs.sort(reverse=True)
    scores = {}
    for s, p in pairs:
        scores[p] = s
        scores[(p[1], p[0])] = s

    links_out = [(s, p) for s, p in links if p[0] == p[1]]

    linkmap = {}
    inv_power = 1.0 / power
    # how many candidates to consider
    max_n = len(names) * len(names)

    for i, pair in enumerate(pairs[:max_n]):
        score, link = pair
        p1, p2 = link
        if p1 in linkmap and p2 in linkmap:
            c1 = linkmap[p1]
            c2 = linkmap[p2]
            if c1 is not c2:
                # [score, set]
                s1, x1 = c1
                s2, x2 = c2
                for x in x2:
                    linkmap[x] = c1
                    for y in x1:
                        s1 += scores[(x, y)]

                x1.update(x2)
                c1[0] = s1 + s2

            n = len(c1[1])
            #    scale == 1 / (n! / (r! * (n-r)!)
            #          == r! * (n-r)! / n!, and here r == 2
            #          ==  2 / (n * (n-1))
            scale = 2.0 / ((n + 2) * (n + 1))
            s = (c1[0] * scale) ** inv_power
            links_out.append((s, link))

        elif p1 in linkmap:
            s = add_to_cluster(p2, linkmap, p1, scores)
            links_out.append((s ** inv_power, link))


        elif p2 in linkmap:
            s = add_to_cluster(p1, linkmap, p2, scores)
            links_out.append((s ** inv_power, link))

        else :
            c = [score, set(link)]
            linkmap[p1] = c
            linkmap[p2] = c
            links_out.append((score ** inv_power, link))
    links_out.sort(reverse=True)
    return links_out


def scale_array01(x):
    hi = np.amax(x)
    lo = np.amin(x)
    if lo == hi:
        return np.zeros_like(x)
    return (x - lo) / (hi - lo)


def cluster_aware_matrix(data, names, power, mix=1.0):
    links = array_to_link_pairs_cluster_aware(data, names, power)
    cdata = links_to_matrix(links, names)
    if mix == 1.0:
        return cdata
    cdata = scale_array01(cdata)
    data = scale_array01(data)
    return cdata * mix + data * (1.0 - mix)


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


def find_text_lengths(names, dirname):
    """For when the text length hasn't been saved"""
    files = os.listdir(dirname)
    if sorted(files) != sorted(names):
        print set(files) - set(names)
        print set(names) - set(files)
        raise ValueError("the files don't match")
    lengths = []
    for fn in names:
        s = os.stat('%s/%s' % (dirname, fn)).st_size
        lengths.append(s)
    return lengths


def text_length_penalty(data, lengths):
    """reduce the score of short texts and their models (towards zero),
    because they can't be certain about anything.
    """
    penalty = [1.0 - 2.0 / math.log(s) for s in lengths]

    p = np.array(penalty)
    p2 = p.reshape(p.shape + (1,))

    data *= p
    data *= p2

    return data
