import language
import os
import subprocess
import time


def add_rnn_args(add_arg):
    import charmodel
    add_arg('-H', '--hidden-size', type=int, default=199,
            metavar='<nodes>', help="number of hidden nodes")

    add_arg('-e', '--epochs', type=int,
            help="how many cycles through the texts to do")
    add_arg('-V', '--stop-on-validation-reverse', type=int, default=0,
            help="stop after this many worsening validation results")

    add_arg('--presynaptic-noise', type=float, default=0.1,
            metavar='<float>', help="Add this much presynaptic noise")

    add_arg('-l', '--learn-rate', type=float, default=1e-1,
            help=charmodel.Net.learn_rate.__doc__)

    add_arg('-L', '--leakage', type=float, default=-2.0,
            help=("how much training leaks into other classes "
                  "[0-1] or negative"))

    add_arg('--leakage-decay', type=float, default=0.9,
            help="change in leakage per epoch")

    add_arg('--learn-rate-decay', type=float, default=1,
            help="change in learn-rate per epoch")

    add_arg('--log-file', help="log to this file")

    add_arg('--enable-fp-exceptions', action='store_true',
            help="crash on bad floating point errors")

    add_arg('--batch-size', type=int, default=20, metavar='<int>',
            help="mini-batch size")

    add_arg('--temporal-pgm-dump', action='store_true',
            help=("save images showing changing state "
                  "of input/error vectors"))

    add_arg('--periodic-pgm-dump', metavar='"({ih,ho,bi}{w,m,d,t})*"',
            help=("Periodically dump images of weights;"
                  "string determines which"))

    add_arg('--periodic-pgm-period', type=int, default=10000,
            help=("periodicity of periodic-pgm-dump"))

    add_arg('--learning-method', type=int, default=4,
            help=("0: weighted, 2: simplified N., "
                  "3: classical, 4: adagrad"))

    add_arg('--activation', type=int, default=2,
            help=("1: ReLU, 2: ReSQRT, 5: clipped ReLU"))

    add_arg('-d', '--bptt-depth', type=int, default=50,
            help="how far to backpropagate through time")

    add_arg('--ignore-start', type=int, default=0,
            help="don't train on this many characters at start")

    add_arg('-f', '--filename', help="save net here")

    add_arg('--init-method', type=int,
            default=charmodel.INIT_FLAT,
            help="0: zeros, 1: flat, 2: fan-in, 3: runs")

    add_arg('-c', '--control-corpus',
            default=language.CONTROL_CORPUS,
            help="use this alternative control corpus")

    add_arg('--validation-corpus',
            default=language.VALIDATION_CORPUS,
            help="use this text for validation")

    add_arg('-C', '--control-n', default=40, type=int,
            help="how many controls to add")

    add_arg('--reverse', action='store_true',
            help="process all texts in reverse")

    add_arg('--save', help='save raw opinions here')

    add_arg('--opinion-every', type=int,
            help="write an opinion at this interval of epochs")


def add_common_args(add_arg, input_dir=True):
    add_arg('lang', help="the language to look at")
    if input_dir:
        add_arg('-i', '--input-dir', default=language.TRAINING_CORPUS,
                help='find problems here')

    add_arg('-o', '--output-dir', help='write results here')

    add_arg('-n', '--basename', default='pan',
            help="base filenames upon this")

    add_arg('-v', '--verbose', action='store_true',
            help="print more to stderr")

    add_arg('-r', '--rng-seed', type=int, default=-1,
            help="rng seed (-1 for auto)")


def make_directory_name(basename, lang, reloading=False):
    # make up a good name
    here = os.path.dirname(__file__)
    git_hash = subprocess.check_output(['git', '-C', here,
                                        'rev-parse',
                                        '--short', 'HEAD']).strip()
    now = time.strftime('%Y-%m-%d+%H-%M-%S')
    mod = '-'
    if subprocess.call(['git', 'diff-files', '--quiet']):
        mod = '+'
    if reloading:
        basename = 'reload-' + basename
    return 'results/%s-%s-%s%s-%s' % (basename, lang, git_hash, mod, now)
