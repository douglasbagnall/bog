# -*- coding: utf-8 -*-
# OPTIONS: threshold 2e-05, dotellipses collapse_brackets text collapse_dashes collapse_digits threshold decompose_caps decompose
charmap = {
    u'\n': u'\n',               # kept Cc (2305)
    u' ': u' ',                 # kept Zs (189928)
    u'!': u'!',                 # kept Po (99)
    u'"': '"',                  # double quote
    u'$': '',                   # removed Sc, 7 < 22
    u'%': u'%',                 # kept Po (41)
    u'&': u'&',                 # kept Po (86)
    u"'": "'",                  # single quote
    u'(': u'(',                 # kept Ps (513)
    u')': u')',                 # kept Pe (525)
    u'+': '',                   # removed Sm, 0 < 22 (includes discount to 0.25)
    u',': u',',                 # kept Po (11378)
    u'-': u'-',                 # kept Pd (1857)
    u'.': u'.',                 # kept Po (8334)
    u'/': u'/',                 # kept Po (219)
    u'0': '7',                  # digit
    u'1': '7',                  # digit
    u'2': '7',                  # digit
    u'3': '7',                  # digit
    u'4': '7',                  # digit
    u'5': '7',                  # digit
    u'6': '7',                  # digit
    u'7': '7',                  # digit
    u'8': '7',                  # digit
    u'9': '7',                  # digit
    u':': u':',                 # kept Po (809)
    u';': u';',                 # kept Po (475)
    u'<': '',                   # removed Sm, 1 < 22 (includes discount to 0.25)
    u'>': '',                   # removed Sm, 1 < 22 (includes discount to 0.25)
    u'?': u'?',                 # kept Po (434)
    u'A': u'\xb9a',             # decomposed caps
    u'B': u'\xb9b',             # decomposed caps
    u'C': u'\xb9c',             # decomposed caps
    u'D': u'\xb9d',             # decomposed caps
    u'E': u'\xb9e',             # decomposed caps
    u'F': u'\xb9f',             # decomposed caps
    u'G': u'\xb9g',             # decomposed caps
    u'H': u'\xb9h',             # decomposed caps
    u'I': u'\xb9i',             # decomposed caps
    u'J': u'\xb9j',             # decomposed caps
    u'K': u'\xb9k',             # decomposed caps
    u'L': u'\xb9l',             # decomposed caps
    u'M': u'\xb9m',             # decomposed caps
    u'N': u'\xb9n',             # decomposed caps
    u'O': u'\xb9o',             # decomposed caps
    u'P': u'\xb9p',             # decomposed caps
    u'Q': u'\xb9q',             # decomposed caps
    u'R': u'\xb9r',             # decomposed caps
    u'S': u'\xb9s',             # decomposed caps
    u'T': u'\xb9t',             # decomposed caps
    u'U': u'\xb9u',             # decomposed caps
    u'V': u'\xb9v',             # decomposed caps
    u'W': u'\xb9w',             # decomposed caps
    u'X': u'\xb9x',             # decomposed caps kept letter under threshold 11 < 22
    u'Y': u'\xb9y',             # decomposed caps
    u'Z': u'\xb9z',             # decomposed caps
    u'[': u'(',                 # brackets
    u']': u')',                 # brackets
    u'a': u'a',
    u'b': u'b',
    u'c': u'c',
    u'd': u'd',
    u'e': u'e',
    u'f': u'f',
    u'g': u'g',
    u'h': u'h',
    u'i': u'i',
    u'j': u'j',
    u'k': u'k',
    u'l': u'l',
    u'm': u'm',
    u'n': u'n',
    u'o': u'o',
    u'p': u'p',
    u'q': u'q',
    u'r': u'r',
    u's': u's',
    u't': u't',
    u'u': u'u',
    u'v': u'v',
    u'w': u'w',
    u'x': u'x',
    u'y': u'y',
    u'z': u'z',
    u'|': '',                   # removed Sm, 0 < 22 (includes discount to 0.25)
    u'~': '',                   # removed Sm, 9 < 22
    u'\xa3': u'\xa3',           # "£" -> "£"  kept Sc (65)  POUND SIGN
    u'\u0301': '',              # "́" -> ""   removed Mn, 12 < 22  COMBINING ACUTE ACCENT
    u'\u0304': '',              # "̄" -> ""   removed Mn, 2 < 22  COMBINING MACRON
    u'\u030c': '',              # "̌" -> ""   removed Mn, 5 < 22  COMBINING CARON
    u'\u2010': u'\u2014',       # "‐" -> "—"  unified dash HYPHEN
    u'\u2013': u'\u2014',       # "–" -> "—"  unified dash EN DASH
    u'\u2014': u'\u2014',       # "—" -> "—"  unified dash EM DASH
    u'\u2018': "'",             # "‘" -> "'"  single quote LEFT SINGLE QUOTATION MARK
    u'\u2019': "'",             # "’" -> "'"  single quote RIGHT SINGLE QUOTATION MARK
    u'\u201c': '"',             # "“" -> """  double quote LEFT DOUBLE QUOTATION MARK
    u'\u201d': '"',             # "”" -> """  double quote RIGHT DOUBLE QUOTATION MARK
    u'\u20ac': '',              # "€" -> ""  removed Sc, 2 < 22  EURO SIGN
    u'\ufeff': '',              # "﻿" -> ""  dispensible ZERO WIDTH NO-BREAK SPACE
}
# mapping 99 characters to 46, (decomposed)
