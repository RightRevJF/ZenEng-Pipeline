#!/usr/bin/env python3
"""ABC melody parser for the TheSession.org tunes.csv dump.

Usage:
    python3 -I abcparse.py test                 # run unit tests
    python3 -I abcparse.py run TUNES.csv OUT.jsonl.gz REPORT.md

Only tunes.csv is read.  Time unit everywhere is the quarter note.
"""
import collections
import csv
import gzip
import json
import math
import re
import sys
import time
from functools import lru_cache

EPS = 1e-6

# ---------------------------------------------------------------- keys
NOTE_BASE = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
SHARP_ORDER = 'FCGDAEB'
FLAT_ORDER = 'BEADGCF'
TONIC_FIFTHS = {'C': 0, 'G': 1, 'D': 2, 'A': 3, 'E': 4, 'B': 5, 'F': -1}
MODE_OFFSET = {'major': 0, 'lydian': 1, 'mixolydian': -1, 'dorian': -2,
               'minor': -3, 'phrygian': -4, 'locrian': -5}
MODE_ALIASES = {'': 'major', 'maj': 'major', 'ion': 'major', 'm': 'minor',
                'min': 'minor', 'aeo': 'minor', 'dor': 'dorian',
                'mix': 'mixolydian', 'lyd': 'lydian', 'phr': 'phrygian',
                'loc': 'locrian'}
ACC_VAL = {'^': 1, '^^': 2, '_': -1, '__': -2, '=': 0}
TONIC_ACC = {'': 0, '#': 1, '♯': 1, 'b': -1, '♭': -1}


def key_signature(letter, acc, mode):
    """Return {letter: semitone alteration} for a diatonic key."""
    fifths = TONIC_FIFTHS[letter] + 7 * acc + MODE_OFFSET[mode]
    sig = dict.fromkeys('ABCDEFG', 0)
    if fifths > 0:
        for i in range(fifths):
            sig[SHARP_ORDER[i % 7]] += 1
    elif fifths < 0:
        for i in range(-fifths):
            sig[FLAT_ORDER[i % 7]] -= 1
    return sig


KEY_RE = re.compile(r'\s*([A-Ga-g])\s*([#b♯♭]?)\s*([A-Za-z]*)')
KEY_EXTRA_ACC = re.compile(r'(\^\^|\^|__|_|=)([A-Ga-g])')


def parse_key(s):
    """Parse a K: field value -> (sig, tonic_pc, mode) or None if unparseable."""
    s = s.split('%')[0].strip()
    if not s:
        return None
    low = s.lower()
    if low.startswith('none'):
        return dict.fromkeys('ABCDEFG', 0), None, None
    if s.startswith('HP'):
        return dict.fromkeys('ABCDEFG', 0), 9, 'mixolydian'
    if s.startswith('Hp'):
        sig = dict.fromkeys('ABCDEFG', 0)
        sig['F'] = sig['C'] = 1
        return sig, 9, 'mixolydian'
    m = KEY_RE.match(s)
    if not m:
        return None
    letter = m.group(1).upper()
    acc = TONIC_ACC[m.group(2)]
    word = m.group(3).lower()
    mode = MODE_ALIASES.get(word if word == 'm' else word[:3], 'major')
    sig = key_signature(letter, acc, mode)
    for a, l in KEY_EXTRA_ACC.findall(s[m.end():]):
        sig[l.upper()] = ACC_VAL[a]
    return sig, (NOTE_BASE[letter] + acc) % 12, mode


MODE_COL_RE = re.compile(r'([A-G])([#b]?)\s*([a-z]+)')


def parse_mode_column(s):
    m = MODE_COL_RE.fullmatch(s.strip())
    if not m:
        return None
    letter, acc, word = m.group(1), TONIC_ACC[m.group(2)], m.group(3)
    mode = {'ionian': 'major', 'aeolian': 'minor'}.get(word, word)
    if mode not in MODE_OFFSET:
        return None
    return key_signature(letter, acc, mode), (NOTE_BASE[letter] + acc) % 12, mode


# ---------------------------------------------------------------- meter
def parse_meter(s):
    """-> (bar_len_quarters, beat_len_quarters) or None (free / unparseable)."""
    s = s.split('%')[0].strip().replace(' ', '')
    if s == 'C':
        num, den = 4, 4
    elif s == 'C|':
        num, den = 2, 2
    else:
        m = re.fullmatch(r'\(?([\d+]+)\)?/(\d+)', s)
        if not m:
            return None
        num = sum(int(x) for x in m.group(1).split('+') if x)
        den = int(m.group(2))
        if num <= 0 or den <= 0:
            return None
    bar = 4.0 * num / den
    if num % 3 == 0 and num > 3 and den >= 4:
        beat = 12.0 / den          # compound: dotted beat
    else:
        beat = 4.0 / den
    return bar, beat


def is_compound(beat):
    """Compound meters have a dotted beat (not a power of two quarters)."""
    return beat > 0 and abs(math.log2(beat) - round(math.log2(beat))) > 1e-9


# ---------------------------------------------------------------- lengths
LEN_RE = re.compile(r'(\d*)((?:/\d*)*)')
SLASH_RE = re.compile(r'/(\d*)')


@lru_cache(maxsize=None)
def parse_len(s):
    if not s:
        return 1.0
    m = LEN_RE.fullmatch(s)
    if not m:
        return None
    v = float(int(m.group(1))) if m.group(1) else 1.0
    for part in SLASH_RE.findall(m.group(2)):
        d = int(part) if part else 2
        if d == 0:
            return None
        v /= d
    return v


def parse_unit(s):
    m = re.fullmatch(r'\s*(\d+)\s*/\s*(\d+)\s*', s.split('%')[0])
    if not m or int(m.group(1)) == 0 or int(m.group(2)) == 0:
        return None
    return 4.0 * int(m.group(1)) / int(m.group(2))


# ---------------------------------------------------------------- preprocessing
FIELD_LINE = re.compile(r'\s*([A-Za-z]):(.*)$')
TEXT_STRIP = re.compile(r'"[^"\n]*"?|![^!\n]*!|\+[^+\n]*\+|\{[^}\n]*\}?|\[[A-Za-z]:[^\]]*\]|%.*')
WORD_RE = re.compile(r'[A-Za-z]{3,}')
TEXTY = set('hijklmnopqrstw')


def looks_like_text(line):
    s = TEXT_STRIP.sub(' ', line)
    for w in WORD_RE.findall(s):
        if sum(ch in TEXTY for ch in w) >= 2:
            return True
    return False


MIDLINE_FIELD = re.compile(r'(?<=\|)\s*([KLM]):([^|\[\]"]*)$')


def preprocess(abc, info):
    """Turn K:/M:/L:/V: lines into inline fields, drop other header lines,
    lyrics, comments and plain-text lines."""
    out = []
    for line in abc.replace('\r', '\n').split('\n'):
        s = line.strip()
        if not s or s.startswith('%'):
            continue
        m = FIELD_LINE.match(s)
        if m:
            f = m.group(1)
            if not (f in 'abcdefg' or (f in 'ABCDEFG' and '|' in s)):
                val = m.group(2).split('%')[0].replace(']', '').strip()
                if f in 'KMLV':
                    out.append('[%s:%s]' % (f, val))
                elif f in 'wW':
                    info['lyrics'] += 1
                else:
                    info['header_dropped'] += 1
                continue
        if looks_like_text(s):
            info['text_lines'] += 1
            continue
        # a K:/L:/M: field written at the end of a music line after a bar line
        mf = MIDLINE_FIELD.search(line)
        if mf:
            line = line[:mf.start()] + '[%s:%s]' % (mf.group(1), mf.group(2).strip())
            info['midline_fields'] += 1
        out.append(line)
    return '\n'.join(out)


# ---------------------------------------------------------------- tokenizer
MASTER = re.compile(r'''
 (?P<ws>[\s\xa0`\\$y\u200e\u2028\x14]+)
|(?P<comment>%[^\n]*)
|(?P<field>\[[A-Za-z]:[^\]]*\])
|(?P<bar>:*\.?(?:\[\||\|)[|\]]*:*|::+)(?:[ ]*\[?(?P<barend>\d+(?:[,\-]\d+)*))?
|(?P<ending>\[(?P<endnum>\d+(?:[,\-]\d+)*))
|(?P<endtext>\["[^"\n]*"?)
|(?P<quote>"[^"\n]*"?)
|(?P<deco>![A-Za-z0-9.<>()^_\-+/]{1,25}!|\+[A-Za-z0-9.<>()^_\-/]{1,25}\+)
|(?P<grace>\{[^}\n]*\}?)
|(?P<tuplet>\((?P<tp>\d+)(?::(?P<tq>\d*))?(?::(?P<tr>\d*))?)
|(?P<chord>\[(?P<cin>[^\]\[|"\n]*(?:"[^"\n]*"[^\]\[|"\n]*)*)\](?P<clen>[0-9/]*)(?P<ctie>-?))
|(?P<note>(?P<acc>\^\^|\^|__|_|=)?(?P<let>[A-Ga-g])(?P<oct>[,']*)(?P<len>[0-9/]*)(?P<tie>-?))
|(?P<rest>[zx](?P<rlen>[0-9/]*))
|(?P<mrest>[ZX](?P<mlen>\d*))
|(?P<broken>[<>]+)
|(?P<tiechar>-)
|(?P<overlay>&)
|(?P<deco1>[.~HLMOPSTuvJR〜])
|(?P<stray>[IKNQUVWhijklmnopqrstw])
|(?P<ign>[()!+\]:])
''', re.X)
CHORD_NOTE = re.compile(r"(\^\^|\^|__|_|=)?([A-Ga-g])([,']*)([0-9/]*)(-?)")

REP_END, REP_START, SECTION, START, END, IMPL_END, MIDBAR = 1, 2, 4, 8, 16, 32, 64
BOUNDARY = REP_END | REP_START | SECTION | START | END


def bar_flags(s):
    lead = len(s) - len(s.lstrip(':'))
    trail = len(s) - len(s.rstrip(':'))
    core = s.strip(':').lstrip('.')
    if not core:  # '::'
        return REP_END | REP_START
    f = 0
    if lead:
        f |= REP_END
    if trail:
        f |= REP_START
    if len(core) >= 2 or ']' in core or '[' in core:
        f |= SECTION
    return f


def parse_endnums(s):
    nums = set()
    for part in s.split(','):
        if '-' in part:
            a, _, b = part.partition('-')
            if a.isdigit() and b.isdigit() and int(b) >= int(a) and int(b) - int(a) < 10:
                nums.update(range(int(a), int(b) + 1))
            elif a.isdigit():
                nums.add(int(a))
        elif part.isdigit():
            nums.add(int(part))
    return frozenset(nums) if nums else None


def tuplet_params(p, q, r, compound):
    if not q:
        q = {2: 3, 3: 2, 4: 3, 6: 2, 8: 3}.get(p, 3 if compound else 2)
    if not r:
        r = p
    return q / p, r


class ParseError(Exception):
    pass


def tokenize(body, meter, sig, flags, cnt):
    """Walk the ABC body; return events and bars.

    events: kind (0 note / 1 rest), pitch, dur (quarters), tie flag
    bars: [ev_start, ev_end, left_flags, right_flags, ending, bar_len, beat_len]
    """
    kind, pitch, dur, tie, epos = [], [], [], [], []
    here = [0]                                 # text offset of the current token
    bars = []
    unit = 0.5                                 # L:1/8 in quarters
    bar_len, beat_len = meter if meter else (None, 1.0)
    compound = is_compound(beat_len)
    bar_acc = {}
    st = {'bar_start': 0, 'left': START, 'ending': None, 'meter': None}
    last_ne = -1
    next_mult = 1.0
    tup_left, tup_fac = 0, 1.0
    tie_carry = None          # (natural, pitch) of last tied note
    keep_voice = '__unset__'
    voice = ''
    overlay_skip = False

    def close_bar(fl, ending):
        if len(kind) > st['bar_start']:
            m = st['meter'] or (bar_len, beat_len)
            bars.append([st['bar_start'], len(kind), st['left'], fl, st['ending'], m[0], m[1]])
            st['bar_start'] = len(kind)
            st['left'] = fl
            st['ending'] = ending
            st['meter'] = None
        else:
            st['left'] |= fl
            if bars:
                bars[-1][3] |= fl
            if ending:
                st['ending'] = ending if not st['ending'] else (st['ending'] | ending)

    def add(k, p, d, t):
        nonlocal last_ne, next_mult, tup_left
        if tup_left > 0:
            d *= tup_fac
            tup_left -= 1
        if next_mult != 1.0:
            d *= next_mult
            next_mult = 1.0
        if len(kind) == st['bar_start']:
            st['meter'] = (bar_len, beat_len)
        kind.append(k)
        pitch.append(p)
        dur.append(d)
        tie.append(t)
        epos.append(here[0])
        last_ne = len(kind) - 1

    def note_pitch(acc, let, octs):
        nonlocal tie_carry
        up = let.upper()
        nat = NOTE_BASE[up] + (60 if let.isupper() else 72) + 12 * (octs.count("'") - octs.count(','))
        if acc:
            a = ACC_VAL[acc]
            bar_acc[nat] = a
            cnt['accidentals'] += 1
        elif nat in bar_acc:
            a = bar_acc[nat]
        elif tie_carry is not None and tie_carry[0] == nat:
            return tie_carry[1], nat          # tied across a bar line keeps its accidental
        else:
            a = sig[up]
        return nat + a, nat

    pos, n = 0, len(body)
    match = MASTER.match
    while pos < n:
        m = match(body, pos)
        if m is None:
            cnt['unknown_chars'] += 1
            pos += 1
            continue
        here[0] = pos
        pos = m.end()
        g = m.lastgroup
        if g == 'barend':
            g = 'bar'
        if g == 'ws' or g == 'comment':
            continue
        if g == 'field':
            txt = m.group(0)
            f, val = txt[1], txt[3:-1].replace('\n', '').strip()
            if f == 'V':
                voice = val.split()[0] if val.split() else ''
                cnt['voice_fields'] += 1
                continue
            if keep_voice != '__unset__' and voice != keep_voice:
                continue
            if f == 'K':
                r = parse_key(val)
                if r is None:
                    if val.strip():
                        flags.add('bad_key_field')
                    continue
                if r[0] != sig:
                    cnt['key_changes'] += 1
                sig = r[0]
                bar_acc.clear()
            elif f == 'M':
                r = parse_meter(val)
                if r is None:
                    if val.lower().startswith('none'):
                        bar_len, beat_len = None, 1.0
                        flags.add('free_meter')
                    else:
                        flags.add('bad_meter_field')
                    continue
                if (bar_len, beat_len) != r:
                    cnt['meter_changes'] += 1
                bar_len, beat_len = r
                compound = is_compound(beat_len)
                if len(kind) == st['bar_start']:
                    st['meter'] = None
            elif f == 'L':
                u = parse_unit(val)
                if u is None:
                    flags.add('bad_unit_field')
                    continue
                if u != unit:
                    cnt['unit_changes'] += 1
                unit = u
            continue
        # voice filtering: keep only the first voice that carries music
        if keep_voice == '__unset__':
            if g in ('note', 'chord', 'rest', 'mrest'):
                keep_voice = voice
        elif voice != keep_voice:
            continue
        if overlay_skip and g != 'bar':
            continue
        if g == 'note':
            p, nat = note_pitch(m.group('acc'), m.group('let'), m.group('oct'))
            L = parse_len(m.group('len'))
            if L is None or L <= 0:
                cnt['bad_lengths'] += 1
                L = 1.0
            t = bool(m.group('tie'))
            add(0, p, L * unit, t)
            tie_carry = (nat, p) if t else None
        elif g == 'chord':
            inner = m.group('cin')
            notes = CHORD_NOTE.findall(re.sub(r'"[^"]*"|![^!]*!|\+[^+]*\+', '', inner))
            if not notes:
                cnt['empty_chords'] += 1
                continue
            best, first_len, best_tie = None, None, False
            for acc, let, octs, ln, tt in notes:
                p, nat = note_pitch(acc, let, octs)
                L = parse_len(ln)
                if L is None or L <= 0:
                    L = 1.0
                if first_len is None:
                    first_len = L
                if best is None or p > best[0]:
                    best = (p, nat)
                    best_tie = bool(tt)
            mult = parse_len(m.group('clen'))
            if mult is None or mult <= 0:
                mult = 1.0
            t = best_tie or bool(m.group('ctie'))
            if len(notes) > 1:
                cnt['chords'] += 1
            add(0, best[0], first_len * mult * unit, t)
            tie_carry = best if t else None
        elif g == 'rest':
            L = parse_len(m.group('rlen'))
            if L is None or L <= 0:
                L = 1.0
            add(1, -1, L * unit, False)
            cnt['rests'] += 1
            tie_carry = None
        elif g == 'mrest':
            nb = int(m.group('mlen')) if m.group('mlen') else 1
            add(1, -1, nb * (bar_len or 4.0), False)
            cnt['rests'] += 1
            cnt['multibar_rests'] += 1
        elif g == 'bar':
            overlay_skip = False
            bar_acc.clear()
            fl = bar_flags(m.group('bar'))
            en = parse_endnums(m.group('barend')) if m.group('barend') else None
            close_bar(fl, en)
            if tup_left:
                tup_left = 0
        elif g == 'ending':
            en = parse_endnums(m.group('endnum'))
            if len(kind) > st['bar_start']:
                bar_acc.clear()
                if bar_len is not None and sum(dur[st['bar_start']:]) >= bar_len - EPS:
                    flags.add('ending_missing_barline')
                    close_bar(0, en)      # bar already complete: treat as a bar line
                else:
                    flags.add('ending_mid_bar')
                    close_bar(MIDBAR, en)     # bar continues: the ending bar is a continuation
            else:
                close_bar(0, en)
        elif g == 'endtext':
            cnt['text_endings'] += 1
        elif g == 'quote':
            q = m.group(0)[1:2]
            if q and q in 'ABCDEFG':
                cnt['chord_symbols'] += 1
            else:
                cnt['annotations'] += 1
        elif g == 'tuplet':
            p = int(m.group('tp'))
            if p < 2:
                cnt['bad_tuplets'] += 1
                continue
            q = int(m.group('tq')) if m.group('tq') else None
            r = int(m.group('tr')) if m.group('tr') else None
            tup_fac, tup_left = tuplet_params(p, q, r, compound)
            cnt['tuplets'] += 1
        elif g == 'broken':
            s = m.group(0)
            k = len(s)
            if last_ne < 0 or len(set(s)) > 1:
                cnt['bad_broken'] += 1
                continue
            short = 0.5 ** k
            longf = 2.0 - short
            if s[0] == '>':
                dur[last_ne] *= longf
                next_mult = short
            else:
                dur[last_ne] *= short
                next_mult = longf
            cnt['broken'] += 1
        elif g == 'tiechar':
            if last_ne >= 0 and kind[last_ne] == 0:
                tie[last_ne] = True
        elif g == 'grace':
            cnt['grace'] += 1
        elif g == 'deco' or g == 'deco1':
            cnt['decorations'] += 1
        elif g == 'stray':
            cnt['stray_letters'] += 1
        elif g == 'overlay':
            overlay_skip = True
            flags.add('overlay_dropped')
        # 'ign': slurs, stray ']' ':' '!' '+'
    close_bar(END | SECTION, None)
    if keep_voice not in ('__unset__',) and cnt['voice_fields'] > 1:
        flags.add('multivoice_first_kept')
    return kind, pitch, dur, tie, bars, epos


# ---------------------------------------------------------------- bar analysis
def analyse_bars(bars, dur, flags, cnt):
    """Per bar: duration, alignment shift (pickups right-aligned), irregular flag."""
    nb = len(bars)
    bdur = [sum(dur[b[0]:b[1]]) for b in bars]
    metered = [b[5] is not None for b in bars]
    ref = [b[5] for b in bars]
    meters = {(b[5], b[6]) for b in bars}
    if len(meters) == 1 and nb >= 4 and bars[0][5] is not None:
        inner = [round(bdur[k], 4) for k in range(1, nb - 1)
                 if not (bars[k][2] & MIDBAR) and not (bars[k + 1][2] & MIDBAR)]
        mode_val, mode_n = collections.Counter(inner).most_common(1)[0] if inner else (0, 0)
        if inner and abs(mode_val - bars[0][5]) > EPS and mode_n >= 0.5 * len(inner):
            flags.add('meter_mismatch')
            ref = [mode_val] * nb
    shift = [0.0] * nb
    irregular = 0
    mid_shift = None              # shift of a first ending that began mid-bar
    for k, b in enumerate(bars):
        if not metered[k]:
            continue
        r = ref[k]
        d = bdur[k]
        short = d < r - EPS
        long_ = d > r + EPS
        if b[4] is not None and not (b[2] & MIDBAR):
            if mid_shift is not None and 1 not in b[4]:
                shift[k] = mid_shift            # later ending of a mid-bar ending group
                if mid_shift + d > r + EPS:
                    irregular += 1
                continue
            mid_shift = None
        elif b[4] is None and (b[2] & (SECTION | REP_START)):
            mid_shift = None
        left_b = k == 0 or (b[2] & BOUNDARY) or b[4] is not None
        right_b = k == nb - 1 or (b[3] & BOUNDARY) or (k + 1 < nb and bars[k + 1][4] is not None)
        if (b[2] & MIDBAR) and k > 0:
            shift[k] = shift[k - 1] + bdur[k - 1]   # ending started mid-bar
            mid_shift = shift[k]
            if shift[k] + d > r + EPS:
                irregular += 1
            continue
        if k == 0 and short and nb > 1:
            shift[0] = r - d
            flags.add('anacrusis')
        elif short and (b[2] & BOUNDARY) and b[4] is None and not right_b \
                and k + 1 < nb and abs(bdur[k + 1] - ref[k + 1]) < EPS:
            shift[k] = r - d
            cnt['internal_pickups'] += 1
        elif (k + 1 < nb and bars[k + 1][2] & MIDBAR):
            pass                                      # checked with its continuation
        elif long_ or (short and not (left_b or right_b)):
            irregular += 1
    return bdur, shift, irregular


# ---------------------------------------------------------------- repeat expansion
def expand(bars, flags):
    """Return list of bar indices in playing order (or None on failure)."""
    nb = len(bars)
    ending = [b[4] for b in bars]
    right = [b[3] for b in bars]
    left = [b[2] for b in bars]
    starts = [k for k in range(nb) if ending[k] is not None]
    if not starts and not any(f & REP_END for f in right):
        return list(range(nb))
    span = {}
    for k in starts:
        j = k
        while not (right[j] & BOUNDARY) and j + 1 < nb and ending[j + 1] is None:
            j += 1
        span[k] = j
    groups = []
    for k in starts:
        if groups and k == span[groups[-1][-1]] + 1 and \
                not any(ending[k] & ending[j] for j in groups[-1]):
            groups[-1].append(k)
        else:
            groups.append([k])
    group_of, last_end, ignore_rep = {}, set(), set()
    allowed = {}
    for gi, g in enumerate(groups):
        maxnum = max(max(ending[k]) for k in g)
        if len(g) == 1:
            flags.add('exp_single_ending')
        for k in g[:-1] if len(g) > 1 else g:
            e = span[k]
            if not (right[e] & REP_END):
                right[e] |= IMPL_END
                flags.add('exp_implicit_repeat')
            allowed[e] = max(1, maxnum - 1)
        if len(g) > 1:
            k = g[-1]
            e = span[k]
            first_len = span[g[0]] - g[0] + 1
            if not (right[e] & BOUNDARY) and e - k + 1 > first_len:
                # last ending runs on into a later ending group: assume same length as first
                e = k + first_len - 1
                span[k] = e
                flags.add('exp_ending_extent_guessed')
            elif right[e] & REP_END:
                if e - k + 1 > first_len:
                    e = k + first_len - 1
                    span[k] = e
                    flags.add('exp_ending_extent_guessed')
                else:
                    ignore_rep.add(e)
                    flags.add('exp_repeat_in_last_ending')
            last_end.add(e)
        for k in g:
            group_of[k] = gi
    order = []
    i, rep_start, cur_pass = 0, 0, 1
    jumps = {}
    guard = 8 * nb + 20
    while i < nb:
        if len(order) > guard:
            flags.add('expansion_guard')
            return None
        if (left[i] & REP_START) and rep_start != i:
            rep_start, cur_pass = i, 1
        if ending[i] is not None:
            g = groups[group_of[i]]
            if cur_pass not in ending[i]:
                later = [k for k in g if k > i and cur_pass in ending[k]]
                if later:
                    i = later[0]
                    continue
                if cur_pass == 1 and not any(1 in ending[k] for k in g):
                    flags.add('exp_ending_numbers_odd')     # e.g. a lone [2: play it
                else:
                    nxt = span[g[-1]] + 1
                    if len(g) > 1 and cur_pass > max(max(ending[k]) for k in g):
                        flags.add('exp_pass_beyond_endings')
                    i, rep_start, cur_pass = nxt, nxt, 1
                    continue
        order.append(i)
        if i in last_end:
            rep_start, cur_pass = i + 1, 1
            i += 1
            continue
        if (right[i] & (REP_END | IMPL_END)) and i not in ignore_rep:
            t = jumps.get(i, 0)
            if t < allowed.get(i, 1):
                jumps[i] = t + 1
                cur_pass += 1
                i = rep_start
                continue
            rep_start, cur_pass = i + 1, 1
        elif right[i] & (SECTION | END):
            rep_start, cur_pass = i + 1, 1
        i += 1
    return order


# ---------------------------------------------------------------- sequences
def r6(x):
    v = round(x, 6)
    iv = int(v)
    return iv if v == iv else v


def build_sequence(order, bars, kind, pitch, dur, tie, shift):
    P, D, O, B, BP = [], [], [], [], []
    t = 0.0
    prev_tied = False
    for bi, k in enumerate(order):
        s, e, _, _, _, _, beat = bars[k]
        off = shift[k]
        for j in range(s, e):
            d = dur[j]
            if kind[j] == 0:
                if prev_tied and P and P[-1] == pitch[j] and abs(O[-1] + D[-1] - t) < EPS:
                    D[-1] += d
                else:
                    P.append(pitch[j])
                    D.append(d)
                    O.append(t)
                    B.append(bi)
                    BP.append(off / beat)
                prev_tied = tie[j]
            else:
                prev_tied = False
            t += d
            off += d
    return {'pitch': P, 'dur': [r6(x) for x in D], 'onset': [r6(x) for x in O],
            'bar': B, 'beatpos': [r6(x) for x in BP]}


# ---------------------------------------------------------------- main entry
def parse_setting(abc, meter_str, mode_str, debug=False):
    flags = set()
    cnt = collections.Counter()
    info = collections.Counter()
    mk = parse_mode_column(mode_str or '')
    if mk is None:
        flags.add('bad_mode_column')
        sig, tonic_pc, mode_name = dict.fromkeys('ABCDEFG', 0), None, None
    else:
        sig, tonic_pc, mode_name = mk
    meter = parse_meter(meter_str or '')
    if meter is None:
        flags.add('bad_meter_column')
    body = preprocess(abc or '', info)
    if info['text_lines']:
        flags.add('text_line_dropped')
    kind, pitch, dur, tie, bars, epos = tokenize(body, meter, sig, flags, cnt)
    rec = {'tonic_pc': tonic_pc, 'mode_name': mode_name}
    n_raw = kind.count(0)
    if n_raw == 0 or not bars:
        flags.add('no_notes')
        empty = {'pitch': [], 'dur': [], 'onset': [], 'bar': [], 'beatpos': []}
        rec.update(n_notes=0, ok=False, flags=sorted(flags), written=empty,
                   expanded=empty, n_bars=0, n_bars_expanded=0, irregular_bars=0,
                   n_chords=0, n_chord_symbols=cnt['chord_symbols'])
        return rec
    bdur, shift, irregular = analyse_bars(bars, dur, flags, cnt)
    written = build_sequence(range(len(bars)), bars, kind, pitch, dur, tie, shift)
    try:
        order = expand(bars, flags)
    except Exception:
        order = None
        flags.add('expansion_error')
    if order is None:
        flags.add('expansion_fallback')
        expanded = written
        order = list(range(len(bars)))
    else:
        expanded = build_sequence(order, bars, kind, pitch, dur, tie, shift)
    # informational flags
    for k, fl in (('chords', 'chords'), ('tuplets', 'tuplets'), ('broken', 'broken_rhythm'),
                  ('key_changes', 'key_change'), ('meter_changes', 'meter_change'),
                  ('unit_changes', 'unit_change'), ('grace', 'grace_notes'),
                  ('internal_pickups', 'internal_pickup'), ('multibar_rests', 'multibar_rest'),
                  ('text_endings', 'text_ending_ignored')):
        if cnt[k]:
            flags.add(fl)
    if cnt['unknown_chars'] > 3:
        flags.add('unknown_chars')
    if cnt['stray_letters'] > 3:
        flags.add('stray_letters')
    if cnt['bad_lengths'] or cnt['bad_broken'] or cnt['bad_tuplets']:
        flags.add('bad_tokens')
    nb = len(bars)
    n_notes = len(written['pitch'])
    bad = False
    if n_notes < 8:
        flags.add('too_few_notes')
        bad = True
    if nb >= 2 and irregular > max(1, 0.2 * nb):
        flags.add('irregular_bars')
        bad = True
    if (cnt['unknown_chars'] + cnt['stray_letters'] + cnt['bad_lengths']) > 0.1 * n_raw:
        flags.add('much_junk')
        bad = True
    if 'bad_mode_column' in flags or 'bad_meter_column' in flags:
        bad = True
    rec.update(n_notes=n_notes, ok=not bad, flags=sorted(flags),
               written=written, expanded=expanded,
               n_bars=nb, n_bars_expanded=len(order), irregular_bars=irregular,
               n_chords=cnt['chords'], n_chord_symbols=cnt['chord_symbols'])
    if debug:
        rec['_debug'] = {'body': body, 'bars': bars, 'epos': epos, 'order': order,
                         'kind': kind, 'shift': shift, 'bdur': bdur}
    return rec


def parse_row(row):
    try:
        rec = parse_setting(row['abc'], row['meter'], row['mode'])
    except Exception as e:  # never let one setting kill the run
        empty = {'pitch': [], 'dur': [], 'onset': [], 'bar': [], 'beatpos': []}
        rec = {'tonic_pc': None, 'mode_name': None, 'n_notes': 0, 'ok': False,
               'flags': ['parse_exception:%s' % type(e).__name__],
               'written': empty, 'expanded': empty}
    out = {'tune_id': int(row['tune_id']), 'setting_id': int(row['setting_id']),
           'name': row['name'], 'type': row['type'], 'meter': row['meter'], 'mode': row['mode']}
    out.update(rec)
    return out


# ================================================================= unit tests
NAMES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B']


def pname(p):
    return '%s%d' % (NAMES[p % 12], p // 12 - 1)


def run_tests():
    def P(abc, meter='4/4', mode='Dmajor'):
        return parse_setting(abc, meter, mode)

    # pitches, octaves, key signature
    r = P('CDEF GABc|defg abc\'d\'|C,D,E,F, G,A,B,C|', mode='Cmajor')
    assert r['written']['pitch'][:8] == [60, 62, 64, 65, 67, 69, 71, 72], r['written']['pitch']
    assert r['written']['pitch'][8:16] == [74, 76, 77, 79, 81, 83, 84, 86]
    assert r['written']['pitch'][16:24] == [48, 50, 52, 53, 55, 57, 59, 60]
    r = P('FcGd ABcd|', mode='Dmajor')
    assert r['written']['pitch'][:3] == [66, 73, 67], r['written']['pitch']
    r = P('Bbea BEAD|', mode='Fmajor')  # F major: Bb only
    assert r['written']['pitch'][:2] == [70, 82]
    assert parse_key('Bb')[0]['E'] == -1 and parse_key('Bb')[0]['B'] == -1
    assert parse_key('Edor')[0] == key_signature('E', 0, 'dorian')
    assert parse_key('Edor')[0]['F'] == 1 and parse_key('Edor')[0]['C'] == 1 and parse_key('Edor')[0]['G'] == 0
    assert parse_key('Amix')[0]['G'] == 0 and parse_key('Amix')[0]['C'] == 1 and parse_key('Amix')[0]['F'] == 1
    assert parse_key('Bm')[2] == 'minor' and parse_key('Bm')[0]['C'] == 1
    assert parse_key('F#m')[1] == 6
    assert parse_key('Dlyd')[0]['G'] == 1
    assert sum(parse_key('Ephr')[0].values()) == 0
    assert sum(parse_key('Bloc')[0].values()) == 0
    assert parse_key('D exp ^f')[0]['F'] == 1
    assert parse_mode_column('Ephrygian')[0] == dict.fromkeys('ABCDEFG', 0)
    assert parse_mode_column('Alocrian')[0]['B'] == -1
    # accidentals carry to end of bar, same octave only, reset at bar line
    r = P('^G G g =G|G2 _B B|B4|', mode='Cmajor')
    assert r['written']['pitch'] == [68, 68, 79, 67, 67, 70, 70, 71], r['written']['pitch']
    r = P('^^C __D =F C|', mode='Dmajor')
    assert r['written']['pitch'] == [62, 60, 65, 62], r['written']['pitch']
    # durations
    r = P('A2 A/2 A/ A3/2 A// A|', mode='Cmajor')
    assert r['written']['dur'] == [1, 0.25, 0.25, 0.75, 0.125, 0.5], r['written']['dur']
    assert r['written']['onset'] == [0, 1, 1.25, 1.5, 2.25, 2.375]
    # broken rhythm
    r = P('A>B A<B A>>B A2|', mode='Cmajor')
    assert r['written']['dur'] == [0.75, 0.25, 0.25, 0.75, 0.875, 0.125, 1], r['written']['dur']
    # triplets and general tuplets
    r = P('(3ABc d2 (3:2:3ABc|', mode='Cmajor')
    d = r['written']['dur']
    assert all(abs(x - 1 / 3) < 1e-5 for x in d[:3]) and d[3] == 1, d
    r = P('(5ABcde (3:2:2A2B ', '4/4', 'Cmajor')
    assert abs(r['written']['dur'][0] - 0.2) < 1e-5 and abs(r['written']['dur'][5] - 2 / 3) < 1e-5
    r = P('(5ABcde f3 |', '6/8', 'Cmajor')   # compound: q=3
    assert abs(r['written']['dur'][0] - 0.3) < 1e-5
    # ties
    r = P('A2-A2 B2-B2-|B4 c-d|', mode='Cmajor')
    assert r['written']['pitch'] == [69, 71, 72, 74] and r['written']['dur'][:2] == [2, 4], r['written']
    r = P('^F4-|F4 F4|', mode='Cmajor')     # tied accidental carries over bar line
    assert r['written']['pitch'] == [66, 65] and r['written']['dur'] == [4, 2], r['written']
    # rests keep time gaps
    r = P('A2 z2 B z/2 c3/2|', mode='Cmajor')
    assert r['written']['pitch'] == [69, 71, 72] and r['written']['onset'] == [0, 2, 2.75]
    # chords: highest note, chord duration = first note length * multiplier
    r = P('[CEG]2 [G,2D2]B "Am"[ceg]/ c|', mode='Cmajor')
    assert r['written']['pitch'][:3] == [67, 62, 71] and r['written']['dur'][:2] == [1, 1], r['written']
    assert r['n_chords'] == 3 and r['n_chord_symbols'] == 1 and 'chords' in r['flags']
    # grace notes, decorations, chord symbols, slurs, annotations dropped
    r = P('{gf}~A2 .B !trill!c +fermata+d "^hi"(ef) TuvG HA|', mode='Cmajor')
    assert r['written']['pitch'] == [69, 71, 72, 74, 76, 77, 67, 69], r['written']['pitch']
    # inline fields
    r = P('ABcd [K:Bb] B2 E2|[M:3/4] A2 B2 c2|[L:1/4] AB|', mode='Gmajor')
    w = r['written']
    assert w['pitch'][4:6] == [70, 63], w['pitch']
    assert w['dur'][-2:] == [1, 1]
    assert 'key_change' in r['flags'] and 'meter_change' in r['flags']
    r = P('ABcd|\nK:G\nfefe|', mode='Dmajor')
    assert r['written']['pitch'][-4:] == [78, 76, 78, 76]
    r = P('ABcd|\nK:C\nfefe|\nT:Title\nw: la la\nfg|', mode='Dmajor')
    assert r['written']['pitch'][4:8] == [77, 76, 77, 76] and r['written']['pitch'][-2:] == [77, 79]
    # repeats
    r = P('|:AB:|cd|', '2/4', 'Cmajor')
    assert r['expanded']['pitch'] == [69, 71, 69, 71, 72, 74], r['expanded']
    assert r['expanded']['bar'] == [0, 0, 1, 1, 2, 2]
    r = P('AB:|cd:|', '2/4', 'Cmajor')     # unclosed repeat from start; second from after first
    assert r['expanded']['pitch'] == [69, 71, 69, 71, 72, 74, 72, 74], r['expanded']
    r = P('AB||cd:|', '2/4', 'Cmajor')
    assert r['expanded']['pitch'] == [69, 71, 72, 74, 72, 74]
    r = P('|:AB|1cd:|2ef||', '2/4', 'Cmajor')
    assert r['expanded']['pitch'] == [69, 71, 72, 74, 69, 71, 76, 77], r['expanded']
    r = P('|:AB|[1cd:|[2ef|]|:ga|1 bc\':|2 c\'2|]', '2/4', 'Cmajor')
    assert r['expanded']['pitch'] == [69, 71, 72, 74, 69, 71, 76, 77, 79, 81, 83, 84, 79, 81, 84], r['expanded']
    r = P('|:AB|1cd|ef:|2gg|aa||', '2/4', 'Cmajor')   # two-bar first ending
    assert r['expanded']['pitch'] == [69, 71, 72, 74, 76, 77, 69, 71, 79, 79, 81, 81], r['expanded']
    r = P('|:AB::cd:|', '2/4', 'Cmajor')
    assert r['expanded']['pitch'] == [69, 71, 69, 71, 72, 74, 72, 74]
    r = P('|:AB|1cd|2ef|3ga:|', '2/4', 'Cmajor')      # no colon before |2 -> implicit
    assert r['expanded']['pitch'][:8] == [69, 71, 72, 74, 69, 71, 76, 77], r['expanded']
    r = P('|:AB|1,3cd:|2ef:|4ga|]', '2/4', 'Cmajor')
    assert r['expanded']['pitch'] == [69, 71, 72, 74, 69, 71, 76, 77, 69, 71, 72, 74, 69, 71, 79, 81], r['expanded']
    r = P("|:AB|1cd:|2ef|ga|1 bc':|2 c'2||", '2/4', 'Cmajor')   # B part without |:
    assert r['expanded']['pitch'] == [69, 71, 72, 74, 69, 71, 76, 77, 79, 81, 83, 84, 79, 81, 84], r['expanded']
    r = P("|:ABcd|ef [1ga:|2bc'||", '2/4', 'Cmajor')     # ending starts mid-bar
    assert r['expanded']['pitch'] == [69, 71, 72, 74, 76, 77, 79, 81, 69, 71, 72, 74, 76, 77, 83, 84], r['expanded']
    assert r['written']['beatpos'] == [0, 0.5, 1, 1.5, 0, 0.5, 1, 1.5, 1, 1.5] and r['irregular_bars'] == 0, r
    assert r['expanded']['beatpos'][-2:] == [1, 1.5]
    # anacrusis: pickup bar right-aligned
    r = P('D|:G2 AB c2 d2|e8:|', '4/4', 'Gmajor')
    assert 'anacrusis' in r['flags'] and r['written']['beatpos'][0] == 3.5, r['written']
    assert r['written']['beatpos'][1:4] == [0, 1, 1.5]
    r = P('ef|:g3 f3|e6:|', '6/8', 'Gmajor')
    assert r['written']['beatpos'][:3] == [r6(4 / 3), r6(5 / 3), 0], r['written']['beatpos']
    # multivoice: keep first voice
    r = P('V:1\nABcd|\nV:2\nCDEF|\nV:1\nefga|', '4/4', 'Cmajor')
    assert r['written']['pitch'] == [69, 71, 72, 74, 76, 77, 79, 81] and 'multivoice_first_kept' in r['flags']
    # backslash continuation, y spacer, $ and ! line breaks
    r = P('AB y cd|\\\nef $ ga|!\nbc\'d\'e\'|', '4/4', 'Cmajor')
    assert len(r['written']['pitch']) == 12
    r = P('ABcd|efga|M:3/4\nABcdef|', '2/4', 'Cmajor')   # field at end of a music line
    assert 'meter_change' in r['flags'] and r['irregular_bars'] == 0
    r = P('|:ABcd|efga[1 gfed:|2 cdef||', '2/4', 'Cmajor')   # [1 with missing bar line
    assert r['irregular_bars'] == 0 and 'ending_missing_barline' in r['flags'], r
    # text line dropped
    r = P('ABcd|\nThe second time through play this\ndefg|', '4/4', 'Cmajor')
    assert len(r['written']['pitch']) == 8 and 'text_line_dropped' in r['flags']
    # beat positions in 6/8 are in dotted-quarter beats
    r = P('ABc dBG|', '6/8', 'Gmajor')
    assert r['written']['beatpos'] == [0, round(1 / 3, 6), round(2 / 3, 6), 1, round(4 / 3, 6), round(5 / 3, 6)], r['written']['beatpos']
    print('all unit tests passed')


# ================================================================= driver
FLAG_DOC = {
    'anacrusis': 'first bar shorter than the meter; treated as a pickup (beatpos right-aligned)',
    'internal_pickup': 'short bar right after a section/repeat boundary, followed by a full bar; right-aligned as a pickup',
    'tuplets': 'contains (p:q:r tuplets',
    'broken_rhythm': 'contains > or < broken rhythm',
    'grace_notes': 'grace notes {...} present (dropped)',
    'chords': 'note chords [..] present (highest note kept)',
    'key_change': 'K: field inside the body changed the key signature',
    'meter_change': 'M: field inside the body changed the meter',
    'unit_change': 'L: field changed the unit note length',
    'meter_mismatch': 'most bars have a length different from the declared meter (e.g. 2/4 bars under 4/4); that length is used as reference',
    'irregular_bars': 'FAIL: >20% of bars (and >1) have a wrong length that a pickup/section boundary cannot explain',
    'much_junk': 'FAIL: unknown characters / stray letters / bad lengths exceed 10% of the notes',
    'no_notes': 'FAIL: no notes found',
    'too_few_notes': 'FAIL: fewer than 8 notes',
    'multivoice_first_kept': 'several V: voices; only the first voice carrying music was kept',
    'overlay_dropped': 'voice overlay (&) material dropped up to the next bar line',
    'text_line_dropped': 'a line of plain prose inside the body was dropped',
    'stray_letters': 'more than 3 letters that are neither notes nor standard decorations (dropped)',
    'unknown_chars': 'more than 3 characters that could not be tokenised (skipped)',
    'bad_tokens': 'zero/invalid lengths, dangling broken rhythm or (1 tuplet ignored',
    'bad_meter_field': 'an inline M: field could not be parsed (ignored)',
    'bad_key_field': 'an inline K: field could not be parsed (ignored)',
    'bad_unit_field': 'an inline L: field could not be parsed (ignored)',
    'free_meter': 'M:none somewhere: no bar-length checks for those bars',
    'multibar_rest': 'Z/X multi-bar rests',
    'text_ending_ignored': 'an ending written with a text label ["..." was ignored',
    'ending_mid_bar': '[1/[2 started in the middle of a bar; the ending continues the bar (beatpos continues)',
    'ending_missing_barline': '[1/[2 written right after a complete bar without a bar line; treated as a bar line',
    'exp_implicit_repeat': 'expansion: a first ending had no :| ; a repeat was assumed at its end',
    'exp_single_ending': 'expansion: a [1 ending with no [2; skipped on the repeat',
    'exp_repeat_in_last_ending': 'expansion: :| at the end of the last ending ignored (would loop forever / means da capo)',
    'exp_ending_extent_guessed': 'expansion: length of the last ending guessed = length of the first ending',
    'exp_ending_numbers_odd': 'expansion: ending numbers did not match the pass (e.g. a lone [2); played as written',
    'exp_pass_beyond_endings': 'expansion: pass number exceeded the ending numbers',
    'expansion_guard': 'expansion produced an implausibly long sequence',
    'expansion_error': 'expansion raised an error',
    'expansion_fallback': 'expanded = written because expansion failed',
}


def _worker(row):
    return parse_row(row)


def run(csv_path, out_path):
    import multiprocessing as mp
    csv.field_size_limit(10 ** 9)
    with open(csv_path, encoding='utf-8', newline='') as fh:
        rows = list(csv.DictReader(fh))
    t0 = time.time()
    summ = []
    with mp.Pool(2) as pool, gzip.open(out_path, 'wt', encoding='utf-8', compresslevel=6) as out:
        for rec in pool.imap(_worker, rows, chunksize=100):
            out.write(json.dumps(rec, ensure_ascii=False, separators=(',', ':')))
            out.write('\n')
            summ.append((rec['type'], rec['ok'], rec['n_notes'], len(rec['expanded']['pitch']),
                         tuple(rec['flags']), rec.get('n_bars', 0), rec.get('n_bars_expanded', 0)))
    return rows, summ, time.time() - t0


def quantiles(xs, qs=(0, 0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99, 1)):
    xs = sorted(xs)
    return [xs[min(len(xs) - 1, int(round(q * (len(xs) - 1))))] for q in qs]


def fmt_seq(rec, bars_sel, which='written'):
    seq = rec[which]
    lines = ['| # | note | midi | dur (q) | onset (q) | bar | beatpos |', '|---|---|---|---|---|---|---|']
    for i, b in enumerate(seq['bar']):
        if b in bars_sel:
            p = seq['pitch'][i]
            lines.append('| %d | %s | %d | %s | %s | %d | %s |' % (i, pname(p), p, seq['dur'][i], seq['onset'][i], b, seq['beatpos'][i]))
    return '\n'.join(lines)


def fragment(dbg, k0, k1):
    """ABC text of bars k0..k1, from the bar line before k0 to the bar line after k1."""
    body, bars, epos = dbg['body'], dbg['bars'], dbg['epos']
    if k0 == 0:
        a = 0
    else:
        p = epos[bars[k0 - 1][1] - 1]
        q = [x for x in (body.find('|', p), body.find('[', p + 1)) if 0 <= x < epos[bars[k0][0]]]
        a = min(q) if q else epos[bars[k0][0]]
    b = epos[bars[k1 + 1][0]] if k1 + 1 < len(bars) else len(body)
    cut = body.rfind('|', epos[bars[k1][1] - 1], b)
    if cut >= 0:
        b = cut + 1
        while b < len(body) and body[b] in ':]':
            b += 1
    return body[a:b].strip()


def bar_of_pos(dbg, pos):
    bars, epos = dbg['bars'], dbg['epos']
    for k, b in enumerate(bars):
        if epos[b[1] - 1] >= pos:
            return k
    return len(bars) - 1


def pick_spot_checks(rows):
    """Deterministically pick illustrative ok settings for each feature."""
    import random
    rnd = random.Random(7)
    idx = list(range(len(rows)))
    rnd.shuffle(idx)
    checks = []
    wanted = ['key_change', 'triplet', 'broken', 'endings', 'accidental_carry',
              'chord', 'anacrusis', 'tie', 'meter_change', 'rest_grace_symbols']
    found = {}
    acc_re = re.compile(r"([\^_=])([A-Ga-g])([,']*)[^|\n]*?(?<![\^_=])\2\3(?![,'])")
    for i in idx:
        if len(found) == len(wanted):
            break
        r = rows[i]
        abc = r['abc']
        if len(abc) > 900:
            continue
        for w in wanted:
            if w in found:
                continue
            rec = None
            if w == 'key_change' and re.search(r'\[K:|\nK:', abc):
                rec = parse_setting(abc, r['meter'], r['mode'], debug=True)
                if rec['ok'] and 'key_change' in rec['flags']:
                    d = rec['_debug']
                    mk = re.search(r'\[K:([^\]]*)\]', d['body'][5:])
                    if not mk:
                        continue
                    p = mk.start() + 5
                    new = parse_key(mk.group(1))
                    old = parse_mode_column(r['mode'])
                    if not new or not old:
                        continue
                    changed = [l for l in 'ABCDEFG' if new[0][l] != old[0][l]]
                    k = bar_of_pos(d, p)
                    if k > 0 and changed and k + 1 < len(d['bars']):
                        fr = fragment(d, k, k + 1)
                        if any(re.search(r'(?<![\^_=])[%s%s]' % (l, l.lower()), fr) for l in changed):
                            found[w] = (i, rec, k - 1, k + 1, 'written')
            elif w == 'triplet' and '(3' in abc and '"' not in abc:
                rec = parse_setting(abc, r['meter'], r['mode'], debug=True)
                if rec['ok']:
                    d = rec['_debug']
                    k = bar_of_pos(d, d['body'].find('(3', 10))
                    b = d['bars'][k]
                    if k > 0 and d['shift'][k] == 0 and abs(d['bdur'][k] - b[5]) < EPS:
                        found[w] = (i, rec, k, k, 'written')
            elif w == 'broken' and '>' in abc and '(' not in abc and '{' not in abc:
                rec = parse_setting(abc, r['meter'], r['mode'], debug=True)
                if rec['ok']:
                    d = rec['_debug']
                    k = bar_of_pos(d, d['body'].find('>'))
                    found[w] = (i, rec, k, k, 'written')
            elif w == 'endings' and '|1' in abc and ':|2' in abc and len(abc) < 450 and '"' not in abc:
                rec = parse_setting(abc, r['meter'], r['mode'], debug=True)
                if rec['ok'] and not any(f.startswith('exp_') for f in rec['flags']) and rec['n_bars'] <= 20:
                    found[w] = (i, rec, None, None, 'expanded')
            elif w == 'accidental_carry' and acc_re.search(abc):
                rec = parse_setting(abc, r['meter'], r['mode'], debug=True)
                if rec['ok']:
                    d = rec['_debug']
                    m = acc_re.search(d['body'])
                    if m:
                        k = bar_of_pos(d, m.start())
                        found[w] = (i, rec, k, k, 'written')
            elif w == 'chord' and re.search(r'\[[A-Ga-g][^\]:]*[A-Ga-g]', abc):
                rec = parse_setting(abc, r['meter'], r['mode'], debug=True)
                if rec['ok'] and rec['n_chords']:
                    d = rec['_debug']
                    k = bar_of_pos(d, re.search(r'\[[A-Ga-g][^\]:]*[A-Ga-g]', d['body']).start())
                    found[w] = (i, rec, k, k, 'written')
            elif w == 'anacrusis' and r['type'] == 'jig':
                rec = parse_setting(abc, r['meter'], r['mode'], debug=True)
                if rec['ok'] and 'anacrusis' in rec['flags'] and rec['written']['beatpos'][0] != 0:
                    found[w] = (i, rec, 0, 1, 'written')
            elif w == 'tie' and re.search(r"[A-Ga-g][,']*\d*-\s*\|?\s*[A-Ga-g]", abc):
                rec = parse_setting(abc, r['meter'], r['mode'], debug=True)
                if rec['ok']:
                    d = rec['_debug']
                    m = re.search(r"([A-Ga-g][,']*)\d*-\s*\|?\s*\1", d['body'])
                    if m:
                        k = bar_of_pos(d, m.start())
                        found[w] = (i, rec, k, min(k + 1, len(d['bars']) - 1), 'written')
            elif w == 'meter_change' and '[M:' in abc:
                rec = parse_setting(abc, r['meter'], r['mode'], debug=True)
                if rec['ok'] and 'meter_change' in rec['flags']:
                    d = rec['_debug']
                    p = d['body'].find('[M:', 3)
                    if p > 0:
                        k = bar_of_pos(d, p)
                        found[w] = (i, rec, max(k - 1, 0), k, 'written')
            elif w == 'rest_grace_symbols' and 'z' in abc and '{' in abc and '"' in abc:
                rec = parse_setting(abc, r['meter'], r['mode'], debug=True)
                if rec['ok']:
                    d = rec['_debug']
                    for k, b in enumerate(d['bars']):
                        fr = fragment(d, k, k)
                        if 'z' in fr and '{' in fr and '"' in fr and '-' not in fragment(d, max(k - 1, 0), k):
                            found[w] = (i, rec, k, k, 'written')
                            break
    return [(w, rows[found[w][0]]) + found[w][1:] for w in wanted if w in found]


SPOT_TITLES = {
    'key_change': 'Key change inside the body',
    'triplet': 'Triplet (3',
    'broken': 'Broken rhythm > / <',
    'endings': 'First and second endings (repeat expansion)',
    'accidental_carry': 'Accidental carried to the end of the bar',
    'chord': 'Chord [..] -> highest note',
    'anacrusis': 'Anacrusis (pickup) -> right-aligned beat positions',
    'tie': 'Tie merged into one note',
    'meter_change': 'Inline meter change',
    'rest_grace_symbols': 'Rest, grace notes and chord symbols',
}


def write_report(rows, summ, elapsed, path, out_path):
    n = len(summ)
    n_ok = sum(1 for s in summ if s[1])
    L = []
    L.append('# TheSession ABC melody parse report\n')
    L.append('Source: `tunes.csv` only (%d settings, %d tunes). Output: `%s`. '
             'Parse time %.0f s on 2 cores.\n' % (n, len({r['tune_id'] for r in rows}), out_path, elapsed))
    L.append('**ok: %d / %d = %.2f%%**; failed or broken-looking: %d (%.2f%%).\n' % (n_ok, n, 100.0 * n_ok / n, n - n_ok, 100.0 * (n - n_ok) / n))
    L.append('## Conventions\n')
    L.append('- Time unit: quarter note. Default L:1/8 (an eighth = 0.5); inline/line `L:` changes it.\n'
             '- Pitch: MIDI, C (octave 4) = 60, c = 72; `,` -12, `\'` +12. Key signature from the `mode` column '
             '(tonic + diatonic mode), then any body `K:`. Accidentals hold for that letter+octave to the bar line; '
             'a note tied across a bar line keeps its accidental.\n'
             '- Chords: highest note, duration of the first note in the chord x the chord multiplier. Grace notes, decorations, '
             'slurs, chord symbols/annotations dropped. Rests are not in the note lists but their time is kept in onsets.\n'
             '- Ties: consecutive notes of the same pitch joined by `-` merge into one note (onset of the first).\n'
             '- Multi-voice tunes: the first voice that carries music is kept.\n'
             '- `bar`: bar index (written order for `written`, playing order for `expanded`); bar 0 is the pickup if there is an anacrusis.\n'
             '- `beatpos`: position in the bar in beats of the meter (quarter for x/4, half for x/2, dotted quarter for 6/8, 9/8, 12/8). '
             'Pickup bars (first bar, or a short bar right after a section boundary) are right-aligned, so a one-eighth pickup in 4/4 has beatpos 3.5.\n'
             '- Expansion: `|: :|` played twice; `:|` without `|:` repeats from the last `|:`, `||`, `|]`, previous repeat end, or the start; '
             '`[1`/`|1` played on pass 1, `[2` on pass 2 (lists and ranges like `[1,3` supported). Flags starting with `exp_` mark heuristic decisions; '
             '`expansion_fallback` means expanded = written.\n'
             '- `ok` = no failure flag (irregular_bars, much_junk, no_notes, too_few_notes, parse exception).\n')
    # by type
    L.append('## ok / failed by type\n')
    L.append('| type | settings | ok | failed | ok % |')
    L.append('|---|---|---|---|---|')
    bt = collections.defaultdict(lambda: [0, 0])
    for s in summ:
        bt[s[0]][0 if s[1] else 1] += 1
    for t, (a, b) in sorted(bt.items(), key=lambda x: -sum(x[1])):
        L.append('| %s | %d | %d | %d | %.2f |' % (t, a + b, a, b, 100.0 * a / (a + b)))
    L.append('| **all** | %d | %d | %d | %.2f |\n' % (n, n_ok, n - n_ok, 100.0 * n_ok / n))
    # failure kinds
    L.append('## Failure kinds (failed settings; a setting can have several)\n')
    fail_flags = collections.Counter()
    for s in summ:
        if not s[1]:
            for f in s[4]:
                if f in ('irregular_bars', 'much_junk', 'no_notes', 'too_few_notes') or f.startswith('parse_exception'):
                    fail_flags[f] += 1
    L.append('| failure | settings | meaning |')
    L.append('|---|---|---|')
    for f, c in fail_flags.most_common():
        L.append('| %s | %d | %s |' % (f, c, FLAG_DOC.get(f, '')))
    L.append('')
    # note counts
    L.append('## Note counts (ok settings)\n')
    qs = (0, 0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99, 1)
    wn = [s[2] for s in summ if s[1]]
    en = [s[3] for s in summ if s[1]]
    nbw = [s[5] for s in summ if s[1]]
    nbe = [s[6] for s in summ if s[1]]
    L.append('| quantity | ' + ' | '.join('q%g' % (100 * q) for q in qs) + ' | mean |')
    L.append('|---|' + '---|' * (len(qs) + 1))
    for lab, xs in (('written notes', wn), ('expanded notes', en), ('written bars', nbw), ('expanded bars', nbe)):
        L.append('| %s | %s | %.1f |' % (lab, ' | '.join(str(v) for v in quantiles(xs, qs)), sum(xs) / len(xs)))
    L.append('')
    edges = [0, 8, 50, 100, 150, 200, 300, 400, 600, 1000, 10 ** 9]
    L.append('| written notes | settings |')
    L.append('|---|---|')
    for a, b in zip(edges[:-1], edges[1:]):
        c = sum(1 for s in summ if a <= s[2] < b)
        L.append('| %s | %d |' % ('%d-%d' % (a, b - 1) if b < 10 ** 9 else '>=%d' % a, c))
    L.append('')
    # flags
    L.append('## Flags\n')
    fc = collections.Counter(f for s in summ for f in s[4])
    fb = collections.Counter(f for s in summ if not s[1] for f in s[4])
    L.append('| flag | settings | of which failed | meaning |')
    L.append('|---|---|---|---|')
    for f, c in fc.most_common():
        L.append('| %s | %d | %d | %s |' % (f, c, fb[f], FLAG_DOC.get(f, '')))
    L.append('')
    # spot checks
    L.append('## Spot checks\n')
    L.append('Ten settings picked deterministically (seeded shuffle) among ok settings. '
             'Fragment = the ABC text of the shown bars (after header lines were turned into inline fields).\n')
    for j, (w, row, rec, k0, k1, which) in enumerate(pick_spot_checks(rows), 1):
        d = rec['_debug']
        L.append('### %d. %s\n' % (j, SPOT_TITLES[w]))
        L.append('setting %s (tune %s) "%s", %s, %s, %s\n' % (row['setting_id'], row['tune_id'], row['name'], row['type'], row['meter'], row['mode']))
        if which == 'expanded':
            L.append('```\n%s\n```\n' % row['abc'].strip())
            L.append('Written bars: %d; playing order of written bars: `%s`\n' % (len(d['bars']), ' '.join(str(x) for x in d['order'])))
            lens = [round(x, 3) for x in d['bdur']]
            L.append('Bar durations (quarters): `%s`\n' % ' '.join(str(x) for x in lens))
            e = rec['expanded']
            # show where the first ending is replaced by the second
            ends = [k for k, b in enumerate(d['bars']) if b[4] is not None]
            for k in ends[:2]:
                pos = [i for i, x in enumerate(d['order']) if x == k]
                L.append('- written bar %d (ending %s, text `%s`) is played at expanded bar(s) %s' % (
                    k, ','.join(str(x) for x in sorted(d['bars'][k][4])), fragment(d, k, k), pos))
            L.append('')
            # print expanded notes around the first ending's two passes
            if ends:
                pos = [i for i, x in enumerate(d['order']) if x == ends[0]]
                pos2 = [i for i, x in enumerate(d['order']) if len(ends) > 1 and x == ends[1]]
                sel = set()
                for p_ in pos + pos2:
                    sel.update({p_ - 1, p_})
                L.append(fmt_seq(rec, sel, 'expanded') + '\n')
        else:
            L.append('```\n%s\n```\n' % fragment(d, k0, k1))
            L.append(fmt_seq(rec, set(range(k0, k1 + 1)), 'written') + '\n')
    L.append('## Record format (`parsed.jsonl.gz`, one JSON object per line, file order of tunes.csv)\n')
    L.append('```\n'
             '{"tune_id": int, "setting_id": int, "name": str, "type": str, "meter": str, "mode": str,\n'
             ' "tonic_pc": 0-11 (from mode column), "mode_name": "major|minor|dorian|mixolydian|lydian|phrygian|locrian",\n'
             ' "n_notes": int (written, after tie merging), "ok": bool, "flags": [str],\n'
             ' "written":  {"pitch": [midi], "dur": [quarters], "onset": [quarters from start], "bar": [int], "beatpos": [beats]},\n'
             ' "expanded": {same fields, in playing order with repeats/endings expanded},\n'
             ' "n_bars": int, "n_bars_expanded": int, "irregular_bars": int, "n_chords": int, "n_chord_symbols": int}\n'
             '```\n')
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(L))


if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == 'test':
        run_tests()
    elif len(sys.argv) >= 5 and sys.argv[1] == 'run':
        run_tests()
        rows, summ, elapsed = run(sys.argv[2], sys.argv[3])
        write_report(rows, summ, elapsed, sys.argv[4], sys.argv[3])
        n_ok = sum(1 for s in summ if s[1])
        print('done: %d settings, %d ok (%.2f%%), %.0f s' % (len(summ), n_ok, 100.0 * n_ok / len(summ), elapsed))
    else:
        print(__doc__)
