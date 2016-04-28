from operator import neg
import cPickle
import numpy as np
import sys
import os

from meta import load_opinions
from munge import p_to_affinities, data_to_clusters, array_to_link_pairs
from munge import clipped_neg_exp, clipped_logistic, shuffle_array
from munge import find_text_lengths, text_length_penalty
from munge import write_normalised_png, cluster_aware_matrix


def load_all_opinions(filenames):
    opinions = load_opinions(filenames[0])
    affinities = opinions['affinities']
    names = opinions['names']
    control_texts = opinions['control_texts']
    control_models = opinions['control_models']

    if len(filenames) > 1:
        for fn in filenames:
            opinions = load_opinions(fn)
            names2 = opinions['names']
            control_texts2 = opinions['control_texts']
            control_models2 = opinions['control_models']
            if (names2 != names):
                raise ValueError("Multiple input files are not compatible")

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

    return affinities, names, control_texts, control_models


def _norm_diagonal(x, *etc):
    d = np.diagonal(x)
    d = d.reshape(d.shape + (1,))
    return x - d


def _norm_texts(x, control_texts, control_models):
    return x - control_texts


def _norm_models(x, control_texts, control_models):
    return x - control_models


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
    'montecarlo': (rmul(100.0), symmetricise, clipped_neg_exp, p_to_affinities),
    'montecarlo-10': (rmul(10.0), symmetricise, clipped_neg_exp,
                      p_to_affinities),
    'montecarlo-asymmetric': (rmul(10.0), clipped_neg_exp, p_to_affinities),
    'montecarlo-sigmoid': (neg, rmul(10.0), symmetricise, clipped_logistic,
                           p_to_affinities),
    'montecarlo-sigmoid-asymmetric': (neg, rmul(10.0), clipped_logistic,
                           p_to_affinities),
    'sigmoid': (neg, symmetricise, clipped_logistic,),
    'transpose-sigmoid': (np.transpose, neg, clipped_logistic,),
    'sigmoid-asymmetric': (neg, clipped_logistic,),
}



def add_interpret_options(parser):
    parser.add_argument('-i', '--input', action='append',
                        help='input filename[s] (pickle)')

    parser.add_argument('-n', '--normalise', default='texts',
                        choices=NORMALISERS.keys(),
                        help='normalise in this dimension')

    parser.add_argument('--strategy', default='simple',
                        choices=STRATEGIES.keys(),
                        help='how to process the affinities')

    parser.add_argument('--list-strategies', action='store_true',
                        help='print valid strategies and exit')

    parser.add_argument('--shuffle', action='store_true',
                        help="randomly shuffle results (for baseline)")

    parser.add_argument('--cluster-aware', action='store_true',
                        help="use cluster aware scoring")

    parser.add_argument('--text-length-penalty', const=True, nargs='?',
                        help=("penalise short texts "
                              "(optional: dir to read from)"))

    return parser


def apply_interpret_options(args):
    if args.list_strategies:
        for k, v in STRATEGIES.items():
            print "%-30s %s%s%s" % (k, GREY, ' . '.join(x.__name__ for x in v),
                                    C_NORMAL)
        sys.exit()

    opinions = load_all_opinions(args.input)
    raw, names, control_texts, control_models = opinions[:4]
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
            data = cluster_aware_matrix(data, names[pid])

        if args.text_length_penalty:
            if args.text_length_penalty is True:
                # try to read the lengths from the pickle
                try:
                    lengths = opinions[5]
                except IndexError:
                    print "%s doesn't have text lengths saved." % args.input,
                    print "please provide a directory name"
                    print "e.g --text-length-penalty=corpus/pan16/"
                    sys.exit()
            else:
                d = os.path.join(args.text_length_penalty, pid)
                lengths = find_text_lengths(names[pid], d)
                                            

            data = text_length_penalty(data, lengths)

        affinities[pid] = data

    return affinities, names
