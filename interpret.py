from operator import neg
import numpy as np
import sys
import os

from meta import load_opinions
from munge import data_to_clusters
from munge import p_to_affinities
from munge import clipped_neg_exp, clipped_logistic, shuffle_array
from munge import find_text_lengths, text_length_penalty
from munge import cluster_aware_matrix
from colour import C_NORMAL, GREY


def find_n_clusters(data, thresholds=None):
    if thresholds is None:
        thresholds = np.unique(data)
    n_clusters = []
    for t in thresholds:
        clusters = data_to_clusters(data, t)
        n_clusters.append(len(clusters))
    return n_clusters


def find_n_links(data, thresholds=None):
    if thresholds is None:
        thresholds = np.unique(data)
    n_links = []
    w = data.shape[0]
    scale = 1.0 / (w * w)
    for t in thresholds:
        links = np.sum(data > t)
        n_links.append(links * scale)

    return n_links


def find_cluster_cliff(data):
    thresholds = np.unique(data)
    n_clusters = find_n_clusters(data)
    for n, cliff in zip(n_clusters, thresholds):
        if n > 1:
            return cliff


def find_clusteriness_anchors(data):
    diagonal = np.diagonal(data)
    d_median = np.median(diagonal)
    cliff = find_cluster_cliff(data)
    return cliff, d_median


def threshold_to_clusteriness(data, threshold):
    cliff, d_median = find_clusteriness_anchors(data)
    if cliff == d_median:
        print "undefined clusteriness!"
        return 0
    return (d_median - threshold) / (d_median - cliff)


def clusteriness_to_threshold(data, clusteriness):
    cliff, d_median = find_clusteriness_anchors(data)
    return d_median - clusteriness * (d_median - cliff)


def load_all_opinions(filenames):
    opinions = load_opinions(filenames[0])
    affinities = opinions['affinities']
    names = opinions['names']
    control_texts = opinions['control_texts']
    control_models = opinions['control_models']

    text_lengths = opinions.get('text_lengths')

    if len(filenames) > 1:
        for fn in filenames[1:]:
            opinions = load_opinions(fn)
            names2 = opinions['names']
            control_texts2 = opinions['control_texts']
            control_models2 = opinions['control_models']
            if (names2 != names):
                raise ValueError("Multiple input files are not compatible")

            # only one needs to have text lengths
            if text_lengths is None:
                text_lengths = opinions.get('text_lengths')

            affinities2 = opinions['affinities']
            for k in affinities:
                affinities[k] += affinities2[k]
                control_texts[k] += control_texts2[k]
                control_models[k] += control_models2[k]

        for k in affinities:
            scale = 1.0 / len(filenames)
            affinities[k] *= scale
            control_texts[k] *= scale
            control_models[k] *= scale

    return affinities, names, control_texts, control_models, text_lengths


def _norm_mean(x, *etc):
    x -= np.mean(x, axis=1)
    return x


def _norm_mean_scale_l1(x, control_texts, control_models):
    x -= np.mean(x, axis=1)
    y = np.abs(x)
    s = y.sum(0)
    s = np.maximum(s, 1e-8)
    return x / s


def _norm_diagonal(x, *etc):
    d = np.diagonal(x)
    d = d.reshape(d.shape + (1,))
    return x - d


def _norm_texts(x, control_texts, control_models):
    return x - control_texts


def _norm_models(x, control_texts, control_models):
    return x - control_models


def _norm_text_zero_mean(x, control_texts, control_models):
    x -= control_texts
    s = x.sum(0)
    s /= len(s)
    return x - s


def _norm_both(x, control_texts, control_models):
    return 2 * x - control_texts - control_models


def _norm_none(x, control_texts, control_models):
    return x


def _norm_scale_l1(x, control_texts, control_models):
    x -= control_texts
    y = np.abs(x)
    s = y.sum(0)
    s = np.maximum(s, 1e-8)
    return x / s


def _norm_scale_l2(x, control_texts, control_models):
    x -= control_texts
    y = x * x
    s = y.sum(0)
    s = np.maximum(s, 1e-8)
    return x / s


def _norm_scale_diagonal_l1(x, control_texts, control_models):
    x = _norm_diagonal(x, control_texts, control_models)
    y = np.abs(x)
    s = y.sum(0)
    s = np.maximum(s, 1e-8)
    return x / s


def _norm_scale_diagonal_l2(x, control_texts, control_models):
    x = _norm_diagonal(x, control_texts, control_models)
    y = x * x
    s = y.sum(0)
    s = np.maximum(s, 1e-8)
    return x / s


def _norm_scale_half_l1(x, control_texts, control_models):
    x -= control_texts
    y = np.abs(x)
    s = y.sum(0)
    s = np.maximum(s, 1e-8)
    s += np.mean(s) * 0.5
    x /= s
    return x


def _norm_scale_half_l2(x, control_texts, control_models):
    x -= control_texts
    y = x * x
    s = y.sum(0)
    s += np.mean(s) * 0.5
    x /= s
    return x

NORMALISERS = {k[6:]: v for k, v in globals().items() if k[:6] == '_norm_'}


def symmetricise(x):
    return (x + x.T) * 0.5


def rmul(n):
    def mul(x):
        return x * n
    mul.__name__ = 'mul_%d' % n
    return mul


STRATEGIES = {
    'asymmetric': (neg,),
    'simple': (neg, symmetricise),
    'transpose': (np.transpose, neg),
    'montecarlo': (rmul(100.0), symmetricise, clipped_neg_exp,
                   p_to_affinities),
    'montecarlo-10': (rmul(10.0), symmetricise, clipped_neg_exp,
                      p_to_affinities),
    'montecarlo-asymmetric': (rmul(10.0), clipped_neg_exp, p_to_affinities),
    'montecarlo-sigmoid': (neg, rmul(10.0), symmetricise, clipped_logistic,
                           p_to_affinities),
    'montecarlo-sigmoid-asymmetric': (neg, rmul(10.0), clipped_logistic,
                                      p_to_affinities),
    'sigmoid': (neg, symmetricise, clipped_logistic,),
    'exp': (symmetricise, clipped_neg_exp),
    'transpose-sigmoid': (np.transpose, neg, clipped_logistic,),
    'sigmoid-asymmetric': (neg, clipped_logistic,),
}


def add_core_interpret_options(parser, corpus_dir=True):
    parser.add_argument('-n', '--normalise', default='texts',
                        choices=NORMALISERS.keys(),
                        help='normalise in this dimension')

    parser.add_argument('--strategy', default='simple',
                        choices=STRATEGIES.keys(),
                        help='how to process the affinities')

    parser.add_argument('--cluster-aware', type=float, default=0,
                        help="use cluster aware scoring (using this L-norm)")

    parser.add_argument('--text-length-penalty', const=corpus_dir, nargs='?',
                        help=("penalise short texts "
                              "(optional: dir to read from)"))
    return parser


def add_interpret_options(parser, corpus_dir=True):
    parser.add_argument('-i', '--input', action='append',
                        help='input filename[s] (pickle)')

    parser.add_argument('--list-strategies', action='store_true',
                        help='print valid strategies and exit')

    parser.add_argument('--shuffle', action='store_true',
                        help="randomly shuffle results (for baseline)")

    add_core_interpret_options(parser, corpus_dir)
    return parser


def apply_interpret_options(args):
    if args.list_strategies:
        for k, v in STRATEGIES.items():
            print "%-30s %s%s%s" % (k, GREY, ' . '.join(x.__name__ for x in v),
                                    C_NORMAL)
        sys.exit()

    opinions = load_all_opinions(args.input)
    raw, names, control_texts, control_models, text_lengths = opinions
    affinities = {}
    for pid, data in raw.items():
        c_texts = control_texts[pid]
        c_models = control_models[pid]

        if args.shuffle:
            data = shuffle_array(data)

        norm = NORMALISERS[args.normalise]
        data = norm(data, c_texts, c_models)

        functions = STRATEGIES[args.strategy]
        for func in functions:
            data = func(data)

        if args.cluster_aware:
            data = cluster_aware_matrix(data, names[pid],
                                        power=args.cluster_aware)

        if args.text_length_penalty:
            if text_lengths is None:
                print "guessing text_lengths"
                if args.text_length_penalty is True:
                    # try to read the lengths from the pickle
                    print "%s doesn't have text lengths saved." % args.input,
                    print "please provide a directory name"
                    print "e.g --text-length-penalty=corpus/pan16/"
                    sys.exit()
                else:
                    d = os.path.join(args.text_length_penalty, pid)
                    lengths = find_text_lengths(names[pid], d)
            else:
                lengths = text_lengths[pid]
            data = text_length_penalty(data, lengths)

        affinities[pid] = data

    return affinities, names
