# -*- coding: utf-8 -*-
# OPTIONS: threshold 2e-05, dotellipses collapse_brackets text collapse_dashes collapse_digits threshold decompose_caps decompose
charmap = {
    u' ': u' ',                 # kept Zs (145729)
    u'e': u'e',
    u'n': u'n',
    u'a': u'a',
    u'i': u'i',
    u't': u't',
    u'r': u'r',
    u'o': u'o',
    u'd': u'd',
    u's': u's',
    u'l': u'l',
    u'g': u'g',
    u'h': u'h',
    u'k': u'k',
    u'v': u'v',
    u'm': u'm',
    u'u': u'u',
    u'j': u'j',
    u'p': u'p',
    u'c': u'c',
    u'w': u'w',
    u'b': u'b',
    u'z': u'z',
    u'.': u'.',                 # kept Po (8162)
    u',': u',',                 # kept Po (6263)
    u'f': u'f',
    u'D': u'\xb9d',             # decomposed caps
    u'\n': u'\n',               # kept Cc (1924)
    u"'": "'",                  # single quote
    u'M': u'\xb9m',             # decomposed caps
    u'B': u'\xb9b',             # decomposed caps
    u'H': u'\xb9h',             # decomposed caps
    u'-': u'-',                 # kept Pd (1201)
    u'E': u'\xb9e',             # decomposed caps
    u'V': u'\xb9v',             # decomposed caps
    u'I': u'\xb9i',             # decomposed caps
    u'A': u'\xb9a',             # decomposed caps
    u'0': '7',                  # digit
    u'S': u'\xb9s',             # decomposed caps
    u'y': u'y',
    u'1': '7',                  # digit
    u'C': u'\xb9c',             # decomposed caps
    u'W': u'\xb9w',             # decomposed caps
    u'P': u'\xb9p',             # decomposed caps
    u'\u0308': u'\u0308',       # "̈" -> "̈"  kept Mn (671)  COMBINING DIAERESIS
    u'O': u'\xb9o',             # decomposed caps
    u'Z': u'\xb9z',             # decomposed caps
    u'N': u'\xb9n',             # decomposed caps
    u'T': u'\xb9t',             # decomposed caps
    u'G': u'\xb9g',             # decomposed caps
    u':': u':',                 # kept Po (545)
    u'L': u'\xb9l',             # decomposed caps
    u'2': '7',                  # digit
    u'\u0301': u'\u0301',       # "́" -> "́"  kept Mn (470)  COMBINING ACUTE ACCENT
    u'K': u'\xb9k',             # decomposed caps
    u'F': u'\xb9f',             # decomposed caps
    u'R': u'\xb9r',             # decomposed caps
    u'9': '7',                  # digit
    u'(': u'(',                 # kept Ps (371)
    u')': u')',                 # kept Pe (371)
    u'x': u'x',
    u'J': u'\xb9j',             # decomposed caps
    u'?': u'?',                 # kept Po (346)
    u'5': '7',                  # digit
    u'\u2019': "'",             # "’" -> "'"  single quote RIGHT SINGLE QUOTATION MARK
    u'4': '7',                  # digit
    u'6': '7',                  # digit
    u'3': '7',                  # digit
    u'8': '7',                  # digit
    u'7': '7',                  # digit
    u'U': u'\xb9u',             # decomposed caps
    u'\u2018': "'",             # "‘" -> "'"  single quote LEFT SINGLE QUOTATION MARK
    u'\u0300': u'\u0300',       # "̀" -> "̀"  kept Mn (94)  COMBINING GRAVE ACCENT
    u'!': u'!',                 # kept Po (87)
    u'q': u'q',
    u'"': '"',                  # double quote
    u'\t': '  ',                # tab
    u';': u';',                 # kept Po (40)
    u'Y': u'\xb9y',             # decomposed caps
    u'_': '',                   # dispensible
    u'*': u'*',                 # kept Po (28)
    u'\u2013': u'\u2014',       # "–" -> "—"  unified dash EN DASH
    u'X': u'\xb9x',             # decomposed caps
    u'/': u'/',                 # kept Po (26)
    u'Q': u'\xb9q',             # decomposed caps
    u'\u0327': u'\u0327',       # "̧" -> "̧"  kept Mn (22)  COMBINING CEDILLA
    u'\u201d': '"',             # "”" -> """  double quote RIGHT DOUBLE QUOTATION MARK
    u'\u201c': '"',             # "“" -> """  double quote LEFT DOUBLE QUOTATION MARK
    u'&': '',                   # removed Po, 15 < 18
    u'\u0302': '',              # "̂" -> ""   removed Mn, 7 < 18  COMBINING CIRCUMFLEX ACCENT
    u'\xad': '',                # "­" -> ""   dispensible SOFT HYPHEN
    u'[': u'(',                 # brackets
    u'\x96': '',                # "" -> ""   removed Cc, 5 < 18  <unknown>
    u']': u')',                 # brackets
    u'%': '',                   # removed Po, 3 < 18
    u'@': '',                   # removed Po, 1 < 18
    u'+': '',                   # removed Sm, 0 < 18 (includes discount to 0.25)
    u'\u20ac': '',              # "€" -> ""  removed Sc, 1 < 18  EURO SIGN
    u'\xb0': '',                # "°" -> ""   removed So, 1 < 18  DEGREE SIGN
    u'\u201e': '"',             # "„" -> """  double quote DOUBLE LOW-9 QUOTATION MARK
    u'\u0303': '',              # "̃" -> ""   removed Mn, 1 < 18  COMBINING TILDE
}
# mapping 101 characters to 48, (decomposed)
