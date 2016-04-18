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


def entropy_to_p(raw_affinities):
    print raw_affinities
    x = np.maximum(raw_affinities, -40.0)
    x = np.minimum(x, 40.0)
    x *= 10
    sigmoid_affinities = 1.0 / (1.0 + np.exp(x))
    open_affinities = np.exp(-x)
    return sigmoid_affinities, open_affinities


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


def p_to_affinities(input, samples=100000):
    """Treat the input array as a (somehow) scaled probability that two
    nodes are linked. The probability that they're in the same cluster
    has a transitive element.
    """
    totals = np.zeros_like(input)
    scale = 0.1
    min_scale = 1e-20
    max_scale = 1.0 / (1e-3 + np.min(input))
    runs = 100
    while runs > 0:
        scale = random.uniform(min_scale, max_scale)

        r = np.random.random(input.shape)
        p = input * scale

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
            min_scale = (scale + min_scale) * 0.5
            print "adjusting MIN to %.3g after %.3g" %  (min_scale, scale)
            continue

        for v in clusters.values():
            #print v
            for x in v:
                for y in v:
                    totals[x, y] += 1.0

        runs -= 1
    totals *= 1.0 / (np.amax(totals) + 1e-10)
    return totals
