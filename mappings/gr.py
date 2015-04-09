# -*- coding: utf-8 -*-
# OPTIONS: threshold 2e-05, dotellipses collapse_brackets text collapse_dashes collapse_latin collapse_digits threshold decompose_caps decompose
charmap = {
    u'\n': u'\n',               # kept Cc (3701)
    u'\r': '',                  # dispensible
    u' ': u' ',                 # kept Zs (126977)
    u'!': u'!',                 # kept Po (471)
    u'"': '"',                  # double quote
    u'$': '',                   # removed Sc, 2 < 17
    u'%': u'%',                 # kept Po (146)
    u'&': u'&',                 # kept Po (83)
    u"'": "'",                  # single quote
    u'(': u'(',                 # kept Ps (997)
    u')': u')',                 # kept Pe (1009)
    u'*': u'*',                 # kept Po (18)
    u'+': '',                   # removed Sm, 4 < 17 (includes discount to 0.25)
    u',': u',',                 # kept Po (7897)
    u'-': u'-',                 # kept Pd (1015)
    u'.': u'.',                 # kept Po (7476)
    u'/': u'/',                 # kept Po (136)
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
    u':': u':',                 # kept Po (480)
    u';': u';',                 # kept Po (507)
    u'=': '',                   # removed Sm, 7 < 17 (includes discount to 0.25)
    u'>': '',                   # removed Sm, 5 < 17 (includes discount to 0.25)
    u'?': u'?',                 # kept Po (34)
    u'A': u'\xb9s',             # decomposed caps latin
    u'B': u'\xb9s',             # decomposed caps latin
    u'C': u'\xb9s',             # decomposed caps latin
    u'D': u'\xb9s',             # decomposed caps latin
    u'E': u'\xb9s',             # decomposed caps latin
    u'F': u'\xb9s',             # decomposed caps latin
    u'G': u'\xb9s',             # decomposed caps latin
    u'H': u'\xb9s',             # decomposed caps latin
    u'I': u'\xb9s',             # decomposed caps latin
    u'J': u'\xb9s',             # decomposed caps kept letter under threshold 8 < 17
    u'K': u'\xb9s',             # decomposed caps latin
    u'L': u'\xb9s',             # decomposed caps latin
    u'M': u'\xb9s',             # decomposed caps latin
    u'N': u'\xb9s',             # decomposed caps latin
    u'O': u'\xb9s',             # decomposed caps latin
    u'P': u'\xb9s',             # decomposed caps latin
    u'Q': u'\xb9s',             # decomposed caps kept letter under threshold 5 < 17
    u'R': u'\xb9s',             # decomposed caps latin
    u'S': u'\xb9s',             # decomposed caps latin
    u'T': u'\xb9s',             # decomposed caps latin
    u'U': u'\xb9s',             # decomposed caps kept letter under threshold 12 < 17
    u'V': u'\xb9s',             # decomposed caps latin
    u'W': u'\xb9s',             # decomposed caps kept letter under threshold 16 < 17
    u'X': u'\xb9s',             # decomposed caps kept letter under threshold 4 < 17
    u'Y': u'\xb9s',             # decomposed caps kept letter under threshold 6 < 17
    u'[': u'(',                 # brackets
    u']': u')',                 # brackets
    u'`': u'`',                 # kept Sk (141)
    u'a': 's',                  # latin
    u'b': 's',                  # latin
    u'c': 's',                  # latin
    u'd': 's',                  # latin
    u'e': 's',                  # latin
    u'f': 's',                  # latin
    u'g': 's',                  # latin
    u'h': 's',                  # latin
    u'i': 's',                  # latin
    u'j': 's',                  # kept letter under threshold 12 < 17
    u'k': 's',                  # latin
    u'l': 's',                  # latin
    u'm': 's',                  # latin
    u'n': 's',                  # latin
    u'o': 's',                  # latin
    u'p': 's',                  # latin
    u'q': 's',                  # latin
    u'r': 's',                  # latin
    u's': 's',                  # latin
    u't': 's',                  # latin
    u'u': 's',                  # latin
    u'v': 's',                  # latin
    u'w': 's',                  # latin
    u'x': 's',                  # latin
    u'y': 's',                  # latin
    u'z': 's',                  # latin
    u'{': u'(',                 # brackets
    u'|': '',                   # removed Sm, 0 < 17 (includes discount to 0.25)
    u'\x85': '',                # "" -> ""   dispensible <unknown>
    u'\xab': u'\xab',           # "«" -> "«"  kept Pi (656)  LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    u'\xbb': u'\xbb',           # "»" -> "»"  kept Pf (650)  RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    u'\u0301': u'\u0301',       # "́" -> "́"  kept Mn (72085)  COMBINING ACUTE ACCENT
    u'\u0303': '',              # "̃" -> ""   removed Mn, 1 < 17  COMBINING TILDE
    u'\u0308': u'\u0308',       # "̈" -> "̈"  kept Mn (307)  COMBINING DIAERESIS
    u'\u0313': '',              # "̓" -> ""   removed Mn, 1 < 17  COMBINING COMMA ABOVE
    u'\u0391': u'\xb9\u03b1',   # "Α" -> "¹α"  decomposed caps  GREEK CAPITAL LETTER ALPHA
    u'\u0392': u'\xb9\u03b2',   # "Β" -> "¹β"  decomposed caps  GREEK CAPITAL LETTER BETA
    u'\u0393': u'\xb9\u03b3',   # "Γ" -> "¹γ"  decomposed caps  GREEK CAPITAL LETTER GAMMA
    u'\u0394': u'\xb9\u03b4',   # "Δ" -> "¹δ"  decomposed caps  GREEK CAPITAL LETTER DELTA
    u'\u0395': u'\xb9\u03b5',   # "Ε" -> "¹ε"  decomposed caps  GREEK CAPITAL LETTER EPSILON
    u'\u0396': u'\xb9\u03b6',   # "Ζ" -> "¹ζ"  decomposed caps  GREEK CAPITAL LETTER ZETA
    u'\u0397': u'\xb9\u03b7',   # "Η" -> "¹η"  decomposed caps  GREEK CAPITAL LETTER ETA
    u'\u0398': u'\xb9\u03b8',   # "Θ" -> "¹θ"  decomposed caps  GREEK CAPITAL LETTER THETA
    u'\u0399': u'\xb9\u03b9',   # "Ι" -> "¹ι"  decomposed caps  GREEK CAPITAL LETTER IOTA
    u'\u039a': u'\xb9\u03ba',   # "Κ" -> "¹κ"  decomposed caps  GREEK CAPITAL LETTER KAPPA
    u'\u039b': u'\xb9\u03bb',   # "Λ" -> "¹λ"  decomposed caps  GREEK CAPITAL LETTER LAMDA
    u'\u039c': u'\xb9\u03bc',   # "Μ" -> "¹μ"  decomposed caps  GREEK CAPITAL LETTER MU
    u'\u039d': u'\xb9\u03bd',   # "Ν" -> "¹ν"  decomposed caps  GREEK CAPITAL LETTER NU
    u'\u039e': u'\xb9\u03be',   # "Ξ" -> "¹ξ"  decomposed caps  GREEK CAPITAL LETTER XI
    u'\u039f': u'\xb9\u03bf',   # "Ο" -> "¹ο"  decomposed caps  GREEK CAPITAL LETTER OMICRON
    u'\u03a0': u'\xb9\u03c0',   # "Π" -> "¹π"  decomposed caps  GREEK CAPITAL LETTER PI
    u'\u03a1': u'\xb9\u03c1',   # "Ρ" -> "¹ρ"  decomposed caps  GREEK CAPITAL LETTER RHO
    u'\u03a3': u'\xb9\u03c3',   # "Σ" -> "¹σ"  decomposed caps  GREEK CAPITAL LETTER SIGMA
    u'\u03a4': u'\xb9\u03c4',   # "Τ" -> "¹τ"  decomposed caps  GREEK CAPITAL LETTER TAU
    u'\u03a5': u'\xb9\u03c5',   # "Υ" -> "¹υ"  decomposed caps  GREEK CAPITAL LETTER UPSILON
    u'\u03a6': u'\xb9\u03c6',   # "Φ" -> "¹φ"  decomposed caps  GREEK CAPITAL LETTER PHI
    u'\u03a7': u'\xb9\u03c7',   # "Χ" -> "¹χ"  decomposed caps  GREEK CAPITAL LETTER CHI
    u'\u03a8': u'\xb9\u03c8',   # "Ψ" -> "¹ψ"  decomposed caps kept letter under threshold 16 < 17 GREEK CAPITAL LETTER PSI
    u'\u03a9': u'\xb9\u03c9',   # "Ω" -> "¹ω"  decomposed caps  GREEK CAPITAL LETTER OMEGA
    u'\u03b1': u'\u03b1',       # "α" -> "α"   GREEK SMALL LETTER ALPHA
    u'\u03b2': u'\u03b2',       # "β" -> "β"   GREEK SMALL LETTER BETA
    u'\u03b3': u'\u03b3',       # "γ" -> "γ"   GREEK SMALL LETTER GAMMA
    u'\u03b4': u'\u03b4',       # "δ" -> "δ"   GREEK SMALL LETTER DELTA
    u'\u03b5': u'\u03b5',       # "ε" -> "ε"   GREEK SMALL LETTER EPSILON
    u'\u03b6': u'\u03b6',       # "ζ" -> "ζ"   GREEK SMALL LETTER ZETA
    u'\u03b7': u'\u03b7',       # "η" -> "η"   GREEK SMALL LETTER ETA
    u'\u03b8': u'\u03b8',       # "θ" -> "θ"   GREEK SMALL LETTER THETA
    u'\u03b9': u'\u03b9',       # "ι" -> "ι"   GREEK SMALL LETTER IOTA
    u'\u03ba': u'\u03ba',       # "κ" -> "κ"   GREEK SMALL LETTER KAPPA
    u'\u03bb': u'\u03bb',       # "λ" -> "λ"   GREEK SMALL LETTER LAMDA
    u'\u03bc': u'\u03bc',       # "μ" -> "μ"   GREEK SMALL LETTER MU
    u'\u03bd': u'\u03bd',       # "ν" -> "ν"   GREEK SMALL LETTER NU
    u'\u03be': u'\u03be',       # "ξ" -> "ξ"   GREEK SMALL LETTER XI
    u'\u03bf': u'\u03bf',       # "ο" -> "ο"   GREEK SMALL LETTER OMICRON
    u'\u03c0': u'\u03c0',       # "π" -> "π"   GREEK SMALL LETTER PI
    u'\u03c1': u'\u03c1',       # "ρ" -> "ρ"   GREEK SMALL LETTER RHO
    u'\u03c2': u'\u03c2',       # "ς" -> "ς"   GREEK SMALL LETTER FINAL SIGMA
    u'\u03c3': u'\u03c3',       # "σ" -> "σ"   GREEK SMALL LETTER SIGMA
    u'\u03c4': u'\u03c4',       # "τ" -> "τ"   GREEK SMALL LETTER TAU
    u'\u03c5': u'\u03c5',       # "υ" -> "υ"   GREEK SMALL LETTER UPSILON
    u'\u03c6': u'\u03c6',       # "φ" -> "φ"   GREEK SMALL LETTER PHI
    u'\u03c7': u'\u03c7',       # "χ" -> "χ"   GREEK SMALL LETTER CHI
    u'\u03c8': u'\u03c8',       # "ψ" -> "ψ"   GREEK SMALL LETTER PSI
    u'\u03c9': u'\u03c9',       # "ω" -> "ω"   GREEK SMALL LETTER OMEGA
    u'\u2012': u'\u2014',       # "‒" -> "—"  unified dash FIGURE DASH
    u'\u2013': u'\u2014',       # "–" -> "—"  unified dash EN DASH
    u'\u2018': "'",             # "‘" -> "'"  single quote LEFT SINGLE QUOTATION MARK
    u'\u2019': "'",             # "’" -> "'"  single quote RIGHT SINGLE QUOTATION MARK
    u'\u201c': '"',             # "“" -> """  double quote LEFT DOUBLE QUOTATION MARK
    u'\u201d': '"',             # "”" -> """  double quote RIGHT DOUBLE QUOTATION MARK
    u'\u20ac': u'\u20ac',       # "€" -> "€"  kept Sc (77)  EURO SIGN
    u'\ufeff': '',              # "﻿" -> ""  dispensible ZERO WIDTH NO-BREAK SPACE
    u'\U0001f600': '',          # "😀" -> ""  removed Cn, 1 < 17  <unknown>
}
# mapping 153 characters to 52, (decomposed)
