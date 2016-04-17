
C_NORMAL    = "\033[00m"
DARK_RED    = "\033[00;31m"
RED         = "\033[01;31m"
DARK_GREEN  = "\033[00;32m"
GREEN       = "\033[01;32m"
YELLOW      = "\033[01;33m"
DARK_YELLOW = "\033[00;33m"
DARK_BLUE   = "\033[00;34m"
BLUE        = "\033[01;34m"
PURPLE      = "\033[00;35m"
MAGENTA     = "\033[01;35m"
DARK_CYAN   = "\033[00;36m"
CYAN        = "\033[01;36m"
GREY        = "\033[00;37m"
WHITE       = "\033[01;37m"

REV_RED     = "\033[01;41m"

foreground = "\033[38;5;%sm".__mod__
background = "\033[48;5;%sm".__mod__

def _gen_print_functions():
    for c in (
            'DARK_RED',
            'RED',
            'DARK_GREEN',
            'GREEN',
            'YELLOW',
            'DARK_YELLOW',
            'DARK_BLUE',
            'BLUE',
            'PURPLE',
            'MAGENTA',
            'DARK_CYAN',
            'CYAN',
            'GREY',
            'WHITE',):
        def f(s, colour=globals()[c]):
            print "%s%s%s" % (colour, s, C_NORMAL)

        globals()['print_' + c] = f

_gen_print_functions()
