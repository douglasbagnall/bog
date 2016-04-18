#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import time
import os
import sys
HERE = os.path.dirname(__file__)
sys.path.append(HERE)
import argparse
import charmodel
import random
import json
import numpy as np
import errno

import language

from meta import write_results, makepath, save_opinions, load_opinions


def write_normalised_png(a, fn):
    #print a
    print fn
    from PIL import Image
    hi = np.amax(a)
    lo = np.amin(a)
    scale = 255.9 / (hi - lo)
    b = (a - lo) * scale
    c = np.array(b, dtype='uint8')
    print "low %f high %f scale %f" % (lo, hi,  scale)
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


def best_connections(rel_entropies):
    entropies = np.copy(rel_entropies)
    n = rel_entropies.shape[0]
    print entropies.shape
    for text in range(n):
        for model in range(n):
            row = rel_entropies[text]
            direct = row[model]
            best = direct
            for m2 in range(n):
                if (row[m2] < best and
                    row[m2] + rel_entropies[m2, model] < best):
                    best = row[m2] + rel_entropies[m2, model]
                    print ("%2d->%-2d direct %.5f; via %2d %.5f, rev %.5f" %
                           (text, model, direct, m2, best,
                            rel_entropies[model, text]))
                    entropies[text, model] = best
    return entropies


def links_to_clusters(links):
    symlinks = links | links.T
    n = links.shape[0]
    clusters = [set([x]) for x in range(n)]

    for a, b in zip(*np.where(links)):
        if clusters[a] != clusters[b]:
            clusters[a].update(clusters[b])
            clusters[b] = clusters[a]

    return set(frozenset(x) for x in clusters)


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
        #print p
        links = r < p
        clusters = links_to_clusters(links)

        #print "found %2d clusters at %g" % (len(clusters), scale)

        if len(clusters) == 1:
            # everything is connected, so the scale is too high
            # make sure we don't go higher.
            max_scale = (scale + max_scale) * 0.5
            print "adjusting max to %.3g after %.3g" %  (max_scale, scale)
            continue

        if len(clusters) == input.shape[0]:
            #nothing is connected
            min_scale = (scale + 3 * min_scale) * 0.25
            print "adjusting MIN to %.3g after %.3g" %  (min_scale, scale)
            continue

        for c in clusters:
            c = np.array(sorted(c), dtype=int)
            for y in c:
                totals[y, c] += 1

        runs -= 1
    totals *= 1.0 / (np.amax(totals) + 1e-10)
    return totals
