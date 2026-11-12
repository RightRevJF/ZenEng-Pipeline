"""ZenEng v116 -- song 45, Before It's Done, on the v116 port (fixes 355-363 in force; findings from 375). A fingerpicked ballad, q = 72,
4/4 (Q4 B); searched in G major, the last chorus and the tag lifted a whole step to A in the record (Q6 A); a man's middle voice (the search
row B2-D4, so the lifted chorus tops at E4; Q5 A); 56 bars (Q7 A).
Designs in force, named (Q14 A, Q15 A):
  the chorus over the verse: the verse low and narrow, the chorus to the song's top (constructive registers, as song 44).
  'Hold that thought': 'thought' held two and a half beats, on G or D (the guitar's sus resolves under it).
  'before it's done' steps down D4 C4 B3 A3 in choruses 1-2 (ends on the 2nd, over D); C4 B3 A3 G3 in the last chorus (home).
  the tag's last note on A3, the 2nd (B after the lift), left open.
  A design gate (317), its pass rate printed.
Usage: PYTHONHASHSEED=0 python3 melody_p45.py N main|ctl [tag]
The v116 port it is built on:
ZenEng v116 PORT (fixes 355-364; Window 136, 27.60) on the v115 port. Songs 40, 42 and 43 run again on it, and song 43 twice more
with fix 348 off and with fix 354 off (356's diagnostic runs, ZE_OFF=348 / ZE_OFF=354).
  355 sixteenths: runs at the kept rate. A sixteenth-position onset followed by a sixteenth (a run) is weighted by a knob set on unaimed
      builds toward the kept 31% in runs; onsets on a sixteenth position weighted by a second knob toward the kept 9.4%.
  356 the rhythm band's bits and the distinct note lengths are read on each calibration round; the four 354 knobs stop when either
      leaves the kept middle half (distinct lengths: the kept windows' quartiles; the rhythm band: the middle half of a normal band
      fitted to 286's soft limits as the kept 5th and 95th, 1.98-2.53, since the tables give no quartiles).
  357 the calibration runs while a knob still moves at full step, up to six rounds, the rounds printed; s16 does not rise while the
      onsets on a sixteenth read over the kept 9.4%.
  358 a note outside the scale that moves by step (one or two semitones) to both its neighbours, on a weak eighth or a sixteenth, is
      allowed whatever the chord; fix 200's rule stays for notes on the beat.
  359 not ported (Q1 A, v116): the kept-window table carries no key, so the 70 minor windows cannot be read apart; costs are read
      against all 314 and the report says so.
  360 a bar that fails 303's check is fitted again (the copy's onsets required in that bar) before it is left out.
  361 unit returns drawn on the section's two-bar units whatever the line lengths: a fresh line covering a returning unit takes the
      earlier unit's onsets bar by bar and its pitches as the contour; sections of two-bar lines keep 350's line plans.
  362 the pick: the judge's first among the survivors that break no soft limit; if none, the judge's first, and the run says so.
  363 and 364 are the report's.
Usage: PYTHONHASHSEED=0 python3 melody_v116_p40.py N main|ctl [tag]
The v115 port it is built on:
ZenEng v115 PORT (fixes 348-354; Window 135, 27.59) on the v114 port. Songs 40, 42 and 43 run again on it before any new song.
  348 a sixteenth only as a push in a drawn line: an onset on a sixteenth position is followed by an eighth or more (a run is not
      drawn); a returning line's words are fitted by splitting on the eighth grid unless there is no room. The writer's reading (Q1 A):
      "unless there is no room" holds for drawn lines too: a line with more syllables than eighth-grid places in its slot may run.
  349 the share outside the scale placed: the build's drawn share is met by moving notes a semitone to the song's sung extra pitch
      class where fix 200 allows it (no chord tone a semitone away, no tritone from the root; no tritone or leap past a sixth made with
      a neighbour; never a line's last note); the walk no longer offers them by weight. A minor song's share is drawn at the kept minor rate (4.5%).
  350 four-line plans keep their returns: unit 3 returns unit 1 at the kept 31.5%, units 2 and 4 as 346.
  351 a bar that fails the one-onset check drops out of the copy; the rest of the line keeps its copied bars; the rate read after.
  352 the pick of record is the judge's first; the composite's first (255's pick) and each one's rank on the other printed.
  353 a minor song's window measures read on its own tonic with the natural minor scale (MTON, MAJ set by the song).
  354 the gaps between onsets (a sixteenth, an eighth, a quarter, longer) aimed together at the kept means for the song's notes a
      bar (Table DU), by four knobs set on unaimed builds.
Usage: PYTHONHASHSEED=0 python3 melody_v115_p40.py N main|ctl [tag]
From the v114 port:
ZenEng v114 PORT (fixes 340-347; Window 134) on the v113 base, for the new song.
  341 sixteenths are pushes: gaps of a sixteenth (and a dotted eighth) weighted by a knob set on unaimed builds toward the kept 11% of
      gaps; a sixteenth-position onset followed by a sixteenth (a run) weighted down, followed by an eighth or more (a push) weighted up.
  343 four note lengths: each section kind's palette drawn per build, three to five lengths (four at the median) from 288's eight,
      the eighth always among them; a line's gaps and line-end holds drawn from it (dropped, and counted, when no rhythm fits).
  344 notes outside the scale: a build's share drawn from the kept windows (none in half; else a kept nonzero share), placed by the
      walk among the song's sung extra pitch classes, a knob set toward the kept mean of 7.1%.
  345 long notes (a beat or longer) on chord tones: a knob on chord tones for long notes, set toward the kept 72%.
  346 the off-beat eighth (kept 0.37) and distinct pitches in a section (kept 6.4 in eight bars) aimed by knobs; in sections of
      two-bar lines, a line returns the line before it at the kept 17% (unit 2) and line 4 returns line 2 at the kept 19%.
  340/347 the report's (a judge fitted on the kept windows against the run's builds; no measure over half a point); 342 intake's.
Every knob above is set in the calibration on builds drawn as the run draws them (338).
Usage: PYTHONHASHSEED=0 python3 melody_v114_p40.py N main|ctl [tag]
From the v113 port:
ZenEng v113 PORT (fixes 337-339): the base for the new song.
  338 verse 2's rate (293, 331) is set on unaimed builds: each calibration round draws its own builds as the main run draws them
      (targets drawn, not set at the pools' medians) and reads verse 2's share there; copies given up printed.
  337 a count read with its spread (the report's); 339 the debugging closed.
Usage: PYTHONHASHSEED=0 python3 melody_v113_p40.py N main|ctl [tag]
From the v112 port:
ZenEng v112 PORT (fixes 330-336) on song 40: Nothing Else on Earth once more, same lyric, intake and seed (Window 132, 27.56).
  330 a partner whose bar copy fails the one-onset check keeps its partner's stressed onsets (322) and is not given up.
  331 293's per-bar copy rate set in the calibration so that verse 2's median share of verse 1's bar rhythms (within one onset)
      is the kept 50%.
  332 a knob that takes its largest step two rounds running is frozen and reported; the other knobs finish their rounds.
  333 the song's range drawn no wider than the row less two semitones.
  334-336 the report's: every tempo band's quartiles; each test read against its kept figure or marked a reading; the floor's
      share a reading.
Usage: PYTHONHASHSEED=0 python3 melody_v112_p40.py N main|ctl [tag]
From the v111 port:
ZenEng v111 PORT (fixes 322-329) on song 40: Nothing Else on Earth again, same lyric, intake and seed (Window 131, 27.55).
  322 a partner of another length (more than one syllable apart) keeps its partner's stressed onsets, the rest drawn freely, with no
      one-onset check; partners within one syllable copy every bar as under 310.
  323 a source bar one onset over the line's cap is copied without its weakest onset (lowest metric weight; the later on a tie);
      bars more than one over are still left out.
  324 a tonic ending takes the tonic nearest the centre of its section's drawn register (the register's drawn median), and the
      test is read there.
  325 every condition a design places on a note is checked against the drawn registers, which are redrawn until it can be met
      (none on this path).
  327 a unit's last line ends by beat 3, or the copy after it enters after the downbeat: where a line cannot end with a breath
      before the copy that follows, the copy is fitted again to enter after its downbeat, then the join is read again.
  328 the sixteenth share printed beside the tempo band's kept figures (the report).
  329 the song's lowest and highest drawn notes are each sung, the lowest in a verse or the bridge and the highest in a chorus or
      the bridge (one fresh line each, chosen per build); no section's floor and cap narrower than the kept window range's 75th
      percentile (13 semitones) where the song's range allows.
Usage: PYTHONHASHSEED=0 python3 melody_v111_p40.py N main|ctl [tag]
From the v110 port:
ZenEng v110 PORT (fixes 310-321) on song 40, the test of the port before song 42: Nothing Else on Earth on the default path again.
  310 a paired line (the same slot in parallel four-bar units) takes its partner's bar rhythm as laid under 308; a line ending a four-bar
      unit ends by beat 3 of the unit's last bar; no judge refitted.  311 the register drawn for an ending section holds its ending
      degree, redrawn until it does (counted).  312/315 the contour amplitude capped at 7; the arch aimed at the kept middle half (0.0-0.55),
      raised only while leaps past a fifth stay at or under 3.6% of moves at the median; the calibration stops, and says so, when a knob
      takes its largest step two rounds running.  313 copied bars chosen among those the line's cap allows.  314 the song's range drawn
      first (kept 17 semitones, 14.5-22), cut to the row and centred in it; the verse's median drawn at the kept share of that range
      (50%, 40-57%); a tonic ending takes the tonic nearest its section's median.  316 a long line's entry and landing drawn only from
      those that admit 308's cap.  317 a design gate stands outside 275, its pass rate printed (none on this path).  318-321 printed.
Usage: PYTHONHASHSEED=0 python3 melody_v110_p40.py N main|ctl [tag]
From the v109 port:
ZenEng v109 PORT (fixes 298-309) on song 40, the test of the port before song 41: Nothing Else on Earth on the default path again.
  300 realness is a printed reading, out of 277's count; 301 the six of 286 read jointly (94.2% of the pairs: no refit; limits_v109.json);
  302 an ending line's last note is drawn first and the walk runs back to it; 303 a copied bar may add or drop one onset;
  304 turns per move not aimed in the chorus; 305 the arch read over the line's span, aimed at the kept 0.23, no cap on the amplitude;
  306 a line's last note drawn from the kept ratio to its mean note; 308 a line of nine syllables or more has at most 57% of them in
  one bar; 298/307 printed in the report; 309 every file a run reads in the repo.
Usage: PYTHONHASHSEED=0 python3 melody_v109_p40.py N main|ctl [tag]
From song 40 under v108:
Riff-led rock, 4/4 at q = 116, D major, a warm mezzo (A3-D5); no era, no character, no designed summit, no bridge register, no chorus
lift, no countermelody (the default path); the drums' half-time verse is an arrangement design and touches no melody gate.
Everything in song 38's rerun Run B (melody_v2_p38.py; 257-285 with the session's readings, now 297's), and:
  286  the five Table B readings, the rhythm band and the sequence legs are soft limits counted in 277's three, hard at the 1st/99th
       (the spectral reading on the kept chart limits of zeneng_v108_spectral_and_registers.json; the other six on the POP909
       calibration pairs: limits286.json).
  287  a return built by 239 is left alone: only its late-changed (and added) notes are re-drawn by the leap repair; no join repair.
  288  up to eight note lengths, the line-end holds weighted by the class's kept rates; section registers drawn from the kept
       distribution of chorus over verse (median, top, lowest drawn together) and bridge over verse.
  289  the landing shares of Window 124's line ends; 290 beat 3 not aimed, turns aimed; 291 the refitted judges and floor;
  293  verse 2's bar rhythms drawn from verse 1's bars at 40%, then the syllables fitted (no axis chosen: its first half does not
       apply); 295 endings drawn, not moved; 296 the composite's fit term without the lift mark.
  230  a line's slot from its syllables (1-3 bars); the writer's form and lyric are the design where a 9-11 syllable line takes two
       bars (Q21: A). 232: the title's last stress ('earth') lands on beat 1 or 3 and is held.
Every build is kept on file, dead or alive.
Usage: PYTHONHASHSEED=0 python3 melody_p40.py N main|ctl [tag]     ctl: 243 off (every build aimed at its pool's medians)."""
import sys, os, json, math, random, pickle, hashlib, collections, platform, inspect
import numpy as np
from scipy.stats import norm
_MODE = sys.argv[2] if len(sys.argv) > 2 else "main"; _N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000; _TAG = sys.argv[3] if len(sys.argv) > 3 else ""
sys.argv = [sys.argv[0], "1", "main"]
sys.path[:0] = ["/home/claude/p49", "/home/claude/p40", "/home/claude/p36", "/home/claude/carol", "/home/claude/pop"]
import melody_p36 as M
import lyric_p45 as L
import judges as J
from measures import beta_pitch, s_spectral, cmp_score, m_horizon, PPM, ic_profile, feature_vec
MODE = _MODE; HERE = "/home/claude/p40"; H109 = "/home/claude/p41"; H110 = "/home/claude/p42"; H111 = "/home/claude/p43"; H112 = "/home/claude/p44"; H113 = "/home/claude/p45"; H114 = "/home/claude/p45"; H115 = "/home/claude/p46"; H116 = "/home/claude/p47"; VAR = MODE; NEW = True
F = dict(f243=MODE == "main")
KW = json.load(open(f"{HERE}/tables/zeneng_v105_kept_windows.json"))
LIT = json.load(open(f"{HERE}/tables/zeneng_v104_line_in_time.json"))
GL = json.load(open(f"{HERE}/tables/zeneng_v106_gate_limits.json"))
SR = json.load(open(f"{HERE}/tables/zeneng_v108_spectral_and_registers.json"))
L286 = json.load(open(f"{HERE}/limits286.json"))["limits"]
L109 = json.load(open(f"{H109}/limits_v109.json"))
C110 = json.load(open(f"{HERE}/tables/zeneng_v110_song41_checks.json"))["kept"]                  # 310, 312, 314: the kept counts of Window 130
K314 = C110["314 the song's range and the verse in it"]                                     # 301: the six's joint pass on the pairs (no refit at 94.2%)
assert L109["chosen"]["hard_percentile"] == 1
DT = json.load(open(f"{HERE}/tables/zeneng_v96_discriminator_tables.json")); DM = DT["measures"]
AX = json.load(open(f"{HERE}/tables/zeneng_v97_axes_of_character.json"))
TR = json.load(open(f"{HERE}/tables/zeneng_v103_selector.json"))["judges, ready to use"]["training rows"]
ERA = None                                                                            # Q8: no era

# ---- the key, the chords, the form ----
BAR, BEAT = 48, 12
M.TONIC = 7; M.SCALE = {7, 9, 11, 0, 2, 4, 6}; M.SUNGPC = M.SCALE | {8}                 # G major; G-sharp sung over the bridge's E (V of A)
OUT_PCS = (8,)
M.CH = {"G": (7, {7, 11, 2}), "D": (2, {2, 6, 9}), "Em": (4, {4, 7, 11}), "C": (0, {0, 4, 7}), "Am": (9, {9, 0, 4}), "E": (4, {4, 8, 11})}
M.ROMAN = {"G": "I", "D": "V", "Em": "vi", "C": "IV", "Am": "ii", "E": "VI"}
M.QBPM = 72; M.SEC_PER_TW = 60 / M.QBPM / BEAT; M.LO = 47; TOP = 62; M.SUMMIT = TOP      # the search row B2-D4; the lifted last chorus tops at E4 (Q5 A)
M.DEG = sorted(p for p in range(36, 90) if p % 12 in M.SCALE)
FEEL = "a fingerpicked acoustic ballad, q = 72, 4/4; a cello from verse 2 (Q4 B)"
LIFT = 2                                                                               # the last chorus and the tag, a whole step up in the record (Q6 A)
PLAN = {"Intro": ["Em", "C", "G", "D"], "Verse": ["Em", "C", "G", "D", "Em", "C", "Am", "D"], "Chorus": ["G", "D", "Em", "C", "G", "D", "C", "D"],
        "LastChorus": ["G", "D", "Em", "C", "G", "D", "C", "G"], "Bridge": ["Am", "Em", "C", "G", "Am", "Em", "C", "E"], "Tag": ["Em", "C", "G", "C"]}
FORM = [("Intro", "Intro", 4), ("Verse 1", "Verse", 8), ("Chorus 1", "Chorus", 8), ("Verse 2", "Verse", 8), ("Chorus 2", "Chorus", 8),
        ("Bridge", "Bridge", 8), ("Last Chorus", "Chorus", 8), ("Tag", "Tag", 4)]
BAR0, CHORD = {}, []
b = 0
for nm, kind, nb in FORM: BAR0[nm] = b; CHORD += PLAN["LastChorus" if nm == "Last Chorus" else kind]; b += nb
NBARS = b; assert NBARS == 56 and len(CHORD) == NBARS
STOP_BARS = set()
KIND = {nm: kind for nm, kind, _ in FORM}; SECLEN = {nm: nb for nm, _, nb in FORM}
SUNG = ["Verse 1", "Chorus 1", "Verse 2", "Chorus 2", "Bridge", "Last Chorus", "Tag"]
M.FORM, M.PLAN, M.BAR0, M.CHORD, M.NBARS, M.KIND, M.SUNG = FORM, PLAN, BAR0, CHORD, NBARS, KIND, SUNG
M.SPANS8 = [(s, 0) for s in SUNG if SECLEN[s] >= 8] + [(s, 8) for s in SUNG if SECLEN[s] >= 16]; M.SPANS16 = [s for s in SUNG if SECLEN[s] >= 16]
SECS = 60 / M.QBPM * 4 * NBARS

# ---- the stress reading (194, 223; the writer's chant) ----
_W1 = {}
def _mono(w):
    if w not in _W1: _W1[w] = len(M.E.syllables(w)) == 1
    return _W1[w]
UNSTRESS_FIRST = set()
def syl(text):
    out = M.syl(text); words = []
    for i, (w, s) in enumerate(out):
        if words and words[-1][0] == w and words[-1][2] == i - 1: words[-1][1].append(i); words[-1][2] = i
        else: words.append([w, [i], i])
    for wi, (w, idx, _) in enumerate(words):
        core = w.strip(",.;:—'\"").lower()
        if core in UNSTRESS_FIRST and len(idx) == 2: out[idx[0]][1] = False; out[idx[1]][1] = True; continue
        if len(idx) == 2 and out[idx[0]][1] and out[idx[1]][1] and wi != len(words) - 1:
            if any(_mono(core[:k]) and _mono(core[k:]) for k in range(2, len(core) - 1)): out[idx[1]][1] = False
    return out
M.WORDS_OF = dict(L.SECTIONS)
LINES = {s: [syl(t.replace('"', "")) for _, t in M.WORDS_OF[s]] for s in SUNG}
M.LINES = LINES
# ---- 230: a line's slot from its syllables; the writer's form is the design where a 9-11 syllable line takes two bars (Q21) ----
SLOTS = {"Verse": [2] * 4, "Chorus": [2] * 4, "Bridge": [2] * 4, "Last Chorus": [2] * 4, "Tag": [2] * 2}      # every line two bars
def slots_of(sec): return SLOTS["Last Chorus"] if sec == "Last Chorus" else SLOTS[KIND[sec]]
for _s in SUNG: assert sum(slots_of(_s)) == SECLEN[_s] and len(slots_of(_s)) == len(LINES[_s]), _s
def slot_len(sec, i): return slots_of(sec)[i]
def line_start(sec, i): return (BAR0[sec] + sum(slots_of(sec)[:i])) * BAR
def unit_end(sec, i): return sum(slots_of(sec)[:i + 1]) % 4 == 0                    # 310: the line ends a four-bar unit of its section
def slot_end(sec, i):
    n = slot_len(sec, i)
    if unit_end(sec, i): return (n - 1) * BAR + 24                                       # 310: a unit's last line ends by beat 3 of the unit's last bar
    return 36 if n == 1 else n * BAR - 24
def ordinary_end(sec, i):
    n = slot_len(sec, i); return 36 if n == 1 else n * BAR - 24                         # 327: the end without 310's unit rule
def units_of(sec):
    """310: the section cut into four-bar units at its slot boundaries; None where a boundary falls inside a line."""
    sl = slots_of(sec); out, cur, acc = [], [], 0
    for i, n in enumerate(sl):
        cur.append(i); acc += n
        if acc % 4 == 0: out.append(cur); cur = []
    return out if not cur else None
def pair_of(sec, i):
    """310: the partner of a line in the second of two parallel units (units 2m and 2m+1 with the same slots): the first's line in the same place."""
    us = units_of(sec)
    if not us: return None
    for k, u in enumerate(us):
        if i in u and k % 2 == 1:
            v = us[k - 1]
            if [slot_len(sec, j) for j in u] == [slot_len(sec, j) for j in v]: return v[u.index(i)]
    return None
ROLE = {s: [r for r, _ in M.WORDS_OF[s]] for s in SUNG}
def is_title(sec, i): return ROLE[sec][i] in ("hook", "tag")
DESIGNED_TWO_BAR = [(s, i, len(LINES[s][i])) for s in SUNG for i in range(len(LINES[s])) if len(LINES[s][i]) >= 9 and slot_len(s, i) == 2]

# ---- 225/226/243: targets are one whole kept window ----
KR = [dict(zip(TR["measures"], r)) for r in TR["kept_real"]]
KRW = [dict(zip(KW["measures"], [np.nan if x is None else x for x in r])) for r in KW["rows"]]   # 266: all 56 + 4 measures, same order
YEAR = KW["year"]
def axes_of(f):
    z = []
    for m in AX["measures"]:
        v = f.get(m, np.nan) if f else np.nan; q = AX["percentiles"][m]
        if v is None or not np.isfinite(v): z.append(0.0); continue
        z.append(norm.ppf(np.clip(np.interp(v, q, AX["percentile_grid"]), 1, 99) / 100))
    return (np.array(z) @ np.array(AX["projection"]) / np.array(AX["axis_sd"])).round(3).tolist()
AXN = [a["name"] for a in AX["axes"]]
KAX = [axes_of(r) for r in KR]
POOL = {"V": [i for i, sct in enumerate(KW["section"]) if sct == "verse"],                 # 243 with no era and no character: a kept window
        "C": [i for i, sct in enumerate(KW["section"]) if sct == "chorus"]}              # of the section's own kind (verse 169, chorus 145)
KR = KRW
AIMED = ["repeat", "step", "third", "fourth_fifth", "past_fifth", "chord_tones_on_beat", "chord_tones_off_beat", "gap_eighth", "gap_quarter", "gap_sixteenth",
         "longest_over_median_note", "notes_per_bar", "on_tonic", "on_third", "on_fifth", "on_beat3", "on_beats_2_4", "turns_per_move"]
MED = {p: {k: (float(np.nanmedian([KR[i][k] for i in POOL[p]])) if k in KR[0] else float(DM[k]["chart"][2])) for k in AIMED} for p in POOL}
NOT_IN_ROWS = [k for k in AIMED if k not in KW["measures"]]                            # read from the chart median (the rows lack them)
def draw_targets(rng, p):
    if F["f243"]:
        i = rng.choice(POOL[p]); t = {k: KR[i].get(k, np.nan) for k in AIMED}
        for k in AIMED:
            if not np.isfinite(t[k]): t[k] = MED[p][k]
        return i, t
    return None, dict(MED[p])

# ---- 249: knobs, calibrated on this song ----
KNOB0 = {k: 1.0 for k in ("repeat", "step", "third", "fourth_fifth", "larger", "ct_on", "ct_off", "on_tonic", "on_third", "on_fifth", "turn",
                          "beat3", "beats24", "gap8", "gap4", "gap16")}
KNOBS = {"V": dict(KNOB0), "C": dict(KNOB0)}
GAMMA = 1.5
def rel(t, p, k): return max(0.05, t[k]) / max(0.05, MED[p][k])
class Aim:
    def __init__(self, t, p):
        self.t, self.p = t, p; K = KNOBS[p]; r = lambda k: rel(t, p, k) ** GAMMA
        self.cat = dict(repeat=K["repeat"] * r("repeat"), step=K["step"] * r("step"), third=K["third"] * r("third"),
                        fourth_fifth=K["fourth_fifth"] * r("fourth_fifth"), larger=K["larger"] * r("past_fifth"))
        self.cw = (K["ct_on"] * r("chord_tones_on_beat"), 1.0, K["ct_off"] * r("chord_tones_off_beat"), 1.0)
        self.deg = {0: K["on_tonic"] * r("on_tonic"), 3: K["on_third"] * r("on_third"), 4: K["on_third"] * r("on_third"), 7: K["on_fifth"] * r("on_fifth")}
        self.turn = K["turn"] * r("turns_per_move") if p == "V" else 1.0               # 304: turns per move not aimed in the chorus
        self.b3, self.b24 = K["beat3"] * r("on_beat3"), K["beats24"] * r("on_beats_2_4")
        self.b3land, self.b3 = 1.0, 1.0                                                 # 290: onsets on beat 3 are no longer aimed
        g16 = K["gap16"] * r("gap_sixteenth")                                          # 288: the sixteenth (and dotted eighth) offered, aimed from the window
        self.tilt = {3: g16, 6: K["gap8"] * r("gap_eighth"), 9: g16, 12: K["gap4"] * r("gap_quarter"), 18: 1.6, 24: 1.6}
        H = min(36, max(12, 6 * t["longest_over_median_note"]))
        self.holds = {L_: math.exp(-(L_ - H) ** 2 / (2 * 9.0 ** 2)) for L_ in (12, 18, 24, 36)}
        x = max(0.0, t["notes_per_bar"] / 3.9 - 1.0)
        self.mel_inner, self.mel_final = min(0.40, 0.04 + 1.2 * x), min(0.5, 0.08 + 1.5 * x)
AIMS = {}; AIM = None
LK = dict(amp=5.0, widen=1.0, fresh=2.0, leap=1.0, s16=1.0, ctl=1.0, offb=1.0, dpk=1.0, k44=1.0, g8=1.0, g4=1.0, glong=1.0, run=0.01, on16=1.0)   # 355: run, on16 (the run knob starts low: a run is taken wherever it is allowed)
DU = [(0, 3.5, (0.04, 0.40, 0.24, 0.29)), (3.5, 4.5, (0.11, 0.50, 0.17, 0.18)), (4.5, 5.5, (0.14, 0.55, 0.16, 0.11)), (5.5, 99, (0.28, 0.49, 0.08, 0.09))]   # 354: Table DU
GAPS = ("gap_sixteenth", "gap_eighth", "gap_quarter", "gap_longer")
def du_target(npb): return next(t for lo, hi, t in DU if lo <= npb < hi)         # 341-346 knobs (338: set on unaimed builds)
RUNW, PUSHW = 0.25, 1.5                                                               # 341: a sixteenth-position onset continued by a sixteenth / held an eighth or more
KEPT355 = dict(in_runs=0.31, on_sixteenth=0.094)                                          # 355
_dd = sorted(r_["distinct_durations"] for r_ in KRW if np.isfinite(r_.get("distinct_durations", np.nan)))
MID356 = dict(distinct_durations=(float(np.percentile(_dd, 25)), float(np.percentile(_dd, 75))),
              rhythm_bits=(2.2541 - 0.6732 * 0.674 / 1.645, 2.2541 + 0.6732 * 0.674 / 1.645))     # 356: the rhythm band's middle half, from 286's soft limits
STOP356 = []
def s16_shape(notes):
    """355: of onsets on a sixteenth position in the verse and chorus windows: how many, how many in runs, how many pushed."""
    n6 = r6 = p6 = 0
    for s_ in ("Verse 1", "Chorus 1"):
        ons = sorted({n_["on"] for n_ in notes if BAR0[s_] * BAR <= n_["on"] < (BAR0[s_] + 8) * BAR}); S_ = set(ons)
        for t_ in ons:
            if t_ % 6 == 3: n6 += 1; r6 += (t_ - 3) in S_ and (t_ + 3) in S_; p6 += (t_ + 3) not in S_
    return n6, r6, p6
KEPT114 = dict(gap_sixteenth=0.107, chord_tones_on_long_notes=0.716, on_offbeat_eighth=0.371, distinct_pitches=6.38, outside_scale=0.071)
PAL_K = ([3, 4, 5], [0.25, 0.5, 0.25])                                                 # 343: the kept count of note lengths in eight bars (three to five, four at the median)
RATE343 = {3: 0.147, 9: 0.055, 12: 0.204, 18: 0.050, 24: 0.040, 36: 0.031, 48: 0.031}   # 288's class rates for the lengths other than the eighth
PALS = {}; OS_T = [0.0]; SEC_USED = set()
OS_SCALE = 1.0                                                                        # 349: 4.5 / 7.1 for a minor song (set by the song)
MTON = None                                                                           # 353: a minor song's tonic for the window measures (set by the song)
def mton(): return M.TONIC if MTON is None else MTON
def place_outside(rng, ns, notes_on, meta):
    """349: the build's drawn share outside the scale, met by moving notes as fix 200 chooses them."""
    extra = sorted(M.SUNGPC - M.SCALE)
    if not extra or len(ns) < 3: return
    want = OS_T[0] * len(ns) + meta.get("os_carry", 0.0); k = int(want)
    on_ = set(notes_on) | {x["on"] for x in ns}; cand = []
    for j in range(0, len(ns) - 1):                                                       # not a line's last note (its ending)
        n = ns[j]; ch = M.chord_for(n, on_)
        if n.get("pin"): continue                                                          # a designed note stays (Q15 A)
        for q in (n["p"] - 1, n["p"] + 1):
            if j > 0 and n["on"] % BEAT and q % 12 in (M.SUNGPC - M.SCALE) and "358" not in OFF \
               and 1 <= abs(q - ns[j - 1]["p"]) <= 2 and 1 <= abs(ns[j + 1]["p"] - q) <= 2:    # 358: a chromatic passing or neighbour note, off the beat, any chord
                cand.append((j, q, True)); STATS["358: chromatic passing places"] += 1; break
            if q % 12 not in extra or M.clash(q, ch) or tri(q, ch): continue                   # fix 200: no chord tone a semitone away; no tritone from the root
            if j > 0 and (abs(q - ns[j - 1]["p"]) in (6,) or abs(q - ns[j - 1]["p"]) > 9): continue
            if abs(ns[j + 1]["p"] - q) in (6,) or abs(ns[j + 1]["p"] - q) > 9: continue
            cand.append((j, q, False)); break
    rng.shuffle(cand); used = set(); placed = 0
    for j, q, pas in cand:
        if placed >= k: break
        if j in used or j - 1 in used or j + 1 in used: continue
        ns[j]["p"] = q; ns[j]["outside"] = True; used.add(j); placed += 1
        if pas: ns[j]["pass358"] = True; STATS["358: chromatic passing notes placed"] += 1
    STATS["349: notes placed outside the scale"] += placed
    if placed < k: STATS["349: places wanting"] += k - placed
    meta["os_carry"] = want - placed
OS_KEPT = [r_["outside_scale"] for r_ in KRW if np.isfinite(r_.get("outside_scale", np.nan)) and r_["outside_scale"] > 0]   # 344                                              # 257/258/259 strengths, set by 249's pass (B, C)
PRIOR_W = None                                                                        # 293: verse 2's bars are copied at 40%, not tilted (268's 8 retired)
def pool_of(sec): return "V" if KIND[sec] in ("Verse", "Pre") else "C"

# ---- 231/289: where a line lands (relative to its slot's first downbeat), Window 124's line ends; 232 for the title ----
LAND_SH = dict(b1=0.26, b3=0.10, b24=0.16, off=0.49)
def land_draw(rng, sec, n_syl, i=None, allowed=None):
    nb = slot_len(sec, i); lo_ = 0 if nb == 1 else (nb - 1) * BAR - 24; hi_ = slot_end(sec, i)
    cls = lambda t: "b1" if t % BAR == 0 else "b3" if t % BAR == 24 else "b24" if t % BEAT == 0 else "off"
    opts = [t for t in range(lo_, hi_ + 1, 6)]
    if allowed is not None: opts = [t for t in opts if t in allowed] or sorted(allowed)                   # 316
    sh = dict(LAND_SH)
    if is_title(sec, i): sh = dict(b1=0.26, b3=0.10)                                    # 232: the title's stress on beat 1 or 3
    k = rng.choices(list(sh), list(sh.values()))[0]; o = [t for t in opts if cls(t) == k]
    return rng.choice(o) if o else rng.choice(opts)

# ---- the rhythm of a line ----
GRID = list(range(-12, 3 * BAR, 6))
ENTRY = dict(on=0.179, after=0.525, pickup=0.143)                                  # 260: kept song medians (normalised when drawn)
ENTRY_T = dict(on=lambda t: t == 0, after=lambda t: 6 <= t <= 30, pickup=lambda t: -12 <= t <= -6)
def entry_kind(t): return "pickup" if t < 0 else "on" if t == 0 else "after" if t <= 30 else "late"
FITS = {}
def line_rhythm(sy, rng, tmin, sec, last_max=None, fix=None, entry=None, prior=None, i=None, copybars=None, pair=False, stressbars=None, fallback=None, allbars=False):
    se = slot_end(sec, i); end = se if last_max is None else min(se, last_max)
    step = 3                                                                            # 288: the sixteenth grid, at the class table's rates and the window's aim
    n = len(sy); st = [x[1] for x in sy]
    mono_weak = [not sy[k][1] and (k == 0 or sy[k - 1][0] != sy[k][0]) and (k == n - 1 or sy[k + 1][0] != sy[k][0]) for k in range(n)]
    def H(k, d): return 1.0 if not mono_weak[k] else (0.1 if d >= 18 else 0.3 if d >= 12 else 1.0)
    Ls = max([k for k in range(n) if st[k]] or [n - 1]); post = n - 1 - Ls
    def A(k, t):
        m = M.mw(t); w = {1.0: 1.0, 0.8: 0.8, 0.55: 0.5, 0.35: 0.3, 0.08: 0.05}[m] if st[k] else {1.0: 0.06, 0.8: 0.15, 0.55: 0.5, 0.35: 1.0, 0.08: 0.8}[m]
        tm = t % BAR
        return (w * (AIM.b3 if tm == 24 else AIM.b24 if tm in (12, 36) else 1.0) * (LK["offb"] if t % 12 == 6 else 1.0)   # 346: the off-beat eighth
                * (LK["on16"] if t % 6 == 3 and "348" not in OFF else 1.0))                       # 355: onsets on a sixteenth aimed at the kept 9.4%
    tilt = AIM.tilt; fix = fix or {}
    cap = int(LONG_SHARE * n) if n >= 9 else n                                           # 308: no bar holds more than 57% of a long line
    if copybars:                                                                         # 313: only bars the cap allows can be copied
        allowed = {}
        for bb, ts in copybars.items():
            if len(ts) <= cap: allowed[bb] = ts
            elif len(ts) == cap + 1:                                                       # 323: one over: copied without its weakest onset
                wk = min(ts, key=lambda t: (M.mw(t), -t)); allowed[bb] = [t for t in ts if t != wk]
                STATS["323: bar one onset over the cap, weakest onset dropped"] += 1
            else: STATS["313: copied bars the cap does not allow, left out"] += 1
        copybars = allowed
    G = [t for t in range(-12, end + 1, step) if tmin <= t <= end]
    runs_ok = len([t for t in G if t % 6 == 0 and (t >= 0 or not st[0])]) < n               # 348 (Q1 A): no room on the eighth grid: runs allowed
    if runs_ok: STATS["348: a drawn line with no room on the eighth grid (runs allowed)"] += 1
    def tw(tp, k, d):
        w = M.RT[tp % BAR][d] * H(k - 1, d) * tilt.get(d, 1.0)
        if "354" not in OFF: w *= LK["s16"] if d in (3, 9) else LK["g8"] if d == 6 else LK["g4"] if d == 12 else LK["glong"] if d > 12 else 1.0   # 354: the gaps together
        if tp % 6 == 3 and d < 6 and not runs_ok and "348" not in OFF: w *= LK["run"]        # 355 (amends 348): a run at the kept rate, the rest pushes
        return w
    pal = PALS.get(KIND[sec])
    def dp(kind_, tgt, cb, sb=None, strict=()):
        def cbw(t, k=0):
            w = 1.0 if not cb or (t // BAR) not in cb or t in cb[t // BAR] else (0.0 if (t // BAR) in strict else 0.04)   # 360: a bar fitted again
            if sb and st[k] and (t // BAR) in sb and t not in sb[t // BAR]: w *= 0.04           # 322: a stressed syllable on the partner's stresses
            return w
        alpha = [dict() for _ in range(n)]
        for t in G:
            if t > tgt: break
            if Ls == 0 and t != tgt: continue
            if 0 in fix and t != fix[0]: continue
            if st[0] and t < 0: continue
            if kind_ is not None:
                if not ENTRY_T[kind_](t): continue
                alpha[0][(t, 1)] = A(0, t) * cbw(t, 0); continue
            alpha[0][(t, 1)] = (1.0 if t < 0 else (0.35 if t == 0 else 0.5)) * A(0, t) * cbw(t, 0)
        for k in range(1, n):
            for t in G:
                if k == Ls and t != tgt: continue
                if k < Ls and t >= tgt: continue
                if k in fix and t != fix[k]: continue
                if st[k] and t < 0: continue
                acc = collections.defaultdict(float)
                for (tp, cp), a_ in alpha[k - 1].items():
                    d = t - tp
                    if step <= d <= 24 and (pal is None or d in pal):                      # 343: the section's palette
                        c = cp + 1 if t // BAR == tp // BAR else 1
                        if c <= cap: acc[c] += a_ * tw(tp, k, d)
                w_ = A(k, t) * cbw(t, k)
                for c, v in acc.items():
                    if v > 0: alpha[k][(t, c)] = v * w_
        return alpha, cbw
    fits = None
    if n >= 9 and not fix:                                                               # 316: the entry and landing drawn only from those that admit the cap
        nb = slot_len(sec, i); lo_ = 0 if nb == 1 else (nb - 1) * BAR - 24
        lands = [t for t in range(lo_, min(slot_end(sec, i), end) + 1, 6) if tmin + step * Ls <= t and t + step * post <= end]
        key = (sec, i, tmin, end, tuple(lands), tuple(sorted(pal)) if pal else None)
        if key not in FITS: FITS[key] = {(k_, t) for k_ in ENTRY for t in lands if dp(k_, t, {})[0][n - 1]}   # cached: what fits depends on the slot alone
        fits = FITS[key]
        STATS["316: long lines"] += 1
        if not fits: STATS["316: long line with no entry and landing that fit"] += 1
    NT = 20 if copybars else 14
    if n >= 9: NT = 60
    for _try in range(NT + 10):
        free = _try >= NT or (fits is not None and not fits)
        if free and _try == NT: STATS["rhythm: placed with a free entry and landing"] += 1
        if free and pal is not None: pal = None; STATS["343: palette dropped for a line"] += 1
        kind_ = None
        if NEW and not fix and not free:
            ek = list(ENTRY) if fits is None else [k_ for k_ in ENTRY if any(f[0] == k_ for f in fits)]
            if entry in ENTRY_T and (fits is None or entry in ek): kind_ = entry
            else: kind_ = rng.choices(ek, [ENTRY[k_] for k_ in ek])[0]
            if kind_ == "pickup" and st[0] and fits is None: kind_ = rng.choices(["on", "after"], [ENTRY["on"], ENTRY["after"]])[0]
        if Ls in fix: tgt = fix[Ls]
        elif free: tgt = rng.choice(list(range(max(0, tmin + step * Ls), end - step * post + 1, step)) or [end])
        elif fits is not None: tgt = land_draw(rng, sec, n, i, allowed={t for k_, t in fits if k_ == kind_})
        else: tgt = land_draw(rng, sec, n, i)
        cb = {}; sb = {}
        if copybars and _try < 14 and not free: cb = {bb: ts for bb, ts in copybars.items() if pair or allbars or rng.random() < RATE293[0]}   # 293 at 331's rate; 310 and 361: every bar
        elif copybars and _try == 14 and not (pair and fallback): STATS["361: unit return given up for a line" if allbars else "293: copy given up for a line" if not pair else "310: partner's rhythm given up for a line"] += 1
        if pair and fallback and 14 <= _try < NT and not free: sb = fallback                  # 330: the copy failed: the partner's stresses
        elif pair and fallback and _try == NT: STATS["330: partner given up after its stresses"] += 1
        if stressbars and _try < 14 and not free: sb = stressbars                         # 322
        elif stressbars and _try == 14: STATS["322: partner's stresses given up for a line"] += 1
        if tgt + step * post > end or tgt - step * Ls < tmin: continue
        alpha, cbw = dp(kind_, tgt, cb, sb)
        if not alpha[n - 1]:
            if n >= 9: STATS["308: long line redrawn"] += 1
            continue
        def sample(alpha):
            ks = list(alpha[n - 1]); ws = [alpha[n - 1][x] * (1.0 + (end - x[0]) / 40) for x in ks]
            if not ks or sum(ws) <= 0: return None
            cur = rng.choices(ks, ws)[0]; ons = [cur[0]]
            for k in range(n - 1, 0, -1):
                t, c = cur
                ks = [(tp, cp) for (tp, cp) in alpha[k - 1] if step <= t - tp <= 24 and (cp + 1 if t // BAR == tp // BAR else 1) == c]
                ws = [alpha[k - 1][x] * tw(x[0], k, t - x[0]) for x in ks]
                if not ks or sum(ws) <= 0: return None
                cur = rng.choices(ks, ws)[0]; ons.append(cur[0])
            ons.reverse(); return ons
        ons = sample(alpha)
        if ons is None: continue
        if cb:                                                                             # 303 with 351: a bar off by more than one onset leaves the copy
            badf = lambda o_: [bb for bb, ts in cb.items() if len(set(ts) ^ {t for t in o_ if t // BAR == bb}) > 1]
            bad = badf(ons)
            if bad and "360" not in OFF:                                                   # 360: the failed bars fitted again, the copy's onsets required there
                a2, _ = dp(kind_, tgt, cb, sb, strict=set(bad))
                o2 = sample(a2) if a2[n - 1] else None
                if o2 is not None and len(badf(o2)) < len(bad):
                    STATS["360: bars fitted again and kept"] += len(bad) - len(badf(o2)); ons = o2; bad = badf(o2)
                else: STATS["360: bars fitted again without success"] += len(bad)
            if bad: STATS["351: bars left out of a copy"] += len(bad); cb = {bb: ts for bb, ts in cb.items() if bb not in bad}
        STATS["361: unit bars copied" if allbars else "293: bars copied" if not pair else "310: partner bars copied"] += len(cb)
        if sb and not pair: STATS["322: partner's stresses kept"] += 1
        if sb and pair: STATS["330: copy failed, partner's stresses kept"] += 1
        return ons
    return None
RATE293 = [0.40]                                                                     # 331: set in the calibration (kept verse 2 share 50%)
V2_KEPT = 0.50
def v2_share(notes):
    """331 (and 313's reading): verse 2's bars whose onsets are within one of verse 1's same bar."""
    def bars(s):
        out = collections.defaultdict(set)
        for n in notes:
            if n["sec"] == s: out[n["on"] // BAR - BAR0[s]].add(n["on"] % BAR)
        return out
    a, c = bars("Verse 2"), bars("Verse 1"); return sum(1 for k, x in a.items() if k in c and len(x ^ c[k]) <= 1) / max(1, len(a))
LONG_SHARE = 0.57                                                                    # 308: the kept 75th percentile of the fullest bar's share
SIXTEENTH = 0.147                                                                     # 288: the class's kept share of sixteenth gaps (v88, pop, mean)
def melismas(ons, rng, end, pal=None):
    rows = []
    ok = lambda *g: pal is None or all(x in pal for x in g)                                # 343: a split's lengths in the palette
    for k, t in enumerate(ons):
        rows.append([t, k, False]); nxt = ons[k + 1] if k + 1 < len(ons) else None
        sx = rng.random() < SIXTEENTH / 0.431 * LK["s16"]                                  # a sixteenth split (a push: held to the next onset), 341's knob
        if nxt is None:
            if t + 6 <= end and rng.random() < AIM.mel_final:
                g = 3 if sx else 6
                if ok(g): rows.append([t + g, k, True])
        elif nxt - t >= 12 and rng.random() < AIM.mel_inner:
            g = 3 if sx else (nxt - t) // 2 // 6 * 6
            if ok(g, nxt - t - g): rows.append([t + g, k, True])
    return rows

# ---- the walk: 182 with 197, 214's one draw, 215, 251's tilts ----
def chord_w(p, n, ch):
    tones = M.CH[ch][1]; on_beat = n["on"] % BEAT == 0; cw = AIM.cw
    w = (cw[0] if p % 12 in tones else cw[1]) if on_beat else (cw[2] if p % 12 in tones else cw[3])
    if n.get("dur", 0) >= 12 and p % 12 in tones: w *= LK["ctl"]                           # 345: a long note on a chord tone
    return w
def extra_w(p):
    """344: a pitch class outside the scale at the build's drawn share; 346: a pitch already sung in the section."""
    w = 1.0
    if p % 12 not in M.SCALE: w = 0.0                                                    # 349: placed, not offered
    if p in SEC_USED: w *= LK["dpk"]
    return w
def deg_w(p): return AIM.deg.get((p - mton()) % 12, 1.0)                                # 353: the degrees aimed where they are read
def tri(p, ch): return (p - M.CH[ch][0]) % 12 == 6
def next_pitch(rng, prev, run, n, ch, mu, lo, hi, last_iv=None, toward=None):
    if prev is None:
        cands = [p for p in range(lo, hi + 1) if p % 12 in M.SCALE and not tri(p, ch)]
        return rng.choices(cands, [math.exp(-(p - mu) ** 2 / (2 * M.RSD ** 2)) * M.kp(p) * chord_w(p, n, ch) * deg_w(p) for p in cands])[0]
    cats = [(c, AIM.cat[c], sz) for c, _, sz in M.CATS]
    if last_iv is not None and abs(last_iv) > 7: cats = [x for x in cats if x[0] in ("step", "third")]
    allc, allw = [], []
    for c in cats:
        cands, ws, base = [], [], 0.0
        for sz in c[2]:
            for sg in ((0,) if sz == 0 else (-1, 1)):
                p = prev + sg * sz
                if not (lo <= p <= hi) or p % 12 not in M.SUNGPC or M.clash(p, ch): continue
                if tri(p, ch): continue                                                    # 215
                if last_iv is not None and abs(last_iv) > 7 and (sg > 0) == (last_iv > 0): continue
                if toward is not None and (abs(toward - p) > 7 or abs(toward - p) == 6): continue
                w0 = math.exp(-(p - mu) ** 2 / (2 * M.RSD ** 2)) * M.kp(p) * M.SIZE_W.get(sz, 1.0)
                w0 *= 1.0 if sz == 0 else (M.DESC if sg < 0 else 1 - M.DESC)
                if sz and last_iv: w0 *= AIM.turn if (sg > 0) != (last_iv > 0) else 1.0
                sf = math.exp(-(p - SHAPE[0]) ** 2 / (2 * 2.5 ** 2)) if SHAPE is not None else 1.0   # 257: toward the line's contour, across move kinds
                cands.append(p); ws.append(w0 * chord_w(p, n, ch) * deg_w(p) * sf * extra_w(p)); base += w0
        if c[0] == "larger": c = (c[0], c[1] * LK["leap"], c[2])                            # 312: leaps past a fifth held to the kept 75th percentile
        if cands and base > 0 and c[1] > 0:
            wd = math.exp(LK["widen"] * (SHAPE[1] - 0.5) * (-1 if c[0] in ("repeat", "step") else 1)) if SHAPE is not None else 1.0   # 258: on the category
            for p, w in zip(cands, ws): allc.append(p); allw.append(c[1] * wd * w / base)
    if allc and sum(allw) > 0: return rng.choices(allc, allw)[0]
    return None
SHAPE = None
CONTOURS = {"arch": [(0, 0), (0.3, 1), (1, -0.2)], "falling": [(0, 0), (1, -1)], "valley": [(0, 0), (0.5, -1), (1, 0)], "rising": [(0, 0), (1, 1)],
            "level then falling": [(0, 0), (0.4, 0), (1, -1)], "falling then level": [(0, 0), (0.6, -1), (1, -1)], "rising then level": [(0, 0), (0.6, 1), (1, 1)],
            "level then rising": [(0, 0), (0.4, 0), (1, 1)], "level": [(0, 0), (1, 0)]}
KEPT_KINDS = LIT["findings"]["kept"]["contour kinds"]
def draw_shape(rng, ns, mu, lo, hi):
    """257: a contour chosen before the notes; 259: the line's first pitch from the contour's start in the section's register."""
    kind = rng.choices(list(KEPT_KINDS), list(KEPT_KINDS.values()))[0]; pts = CONTOURS[kind]; D = LK["amp"] * rng.uniform(0.7, 1.3)
    t0, t1 = ns[0]["on"], ns[-1]["on"]; xs = [(n["on"] - t0) / max(1, t1 - t0) for n in ns]
    f = [D * float(np.interp(x, [a for a, _ in pts], [b for _, b in pts])) for x in xs]
    h0 = mu + rng.gauss(0, LK["fresh"]) - float(np.mean(f))
    h0 = min(hi - max(f) - 0.5, max(lo - min(f) + 0.5, h0)) if max(f) - min(f) < hi - lo - 1 else (lo + hi) / 2 - float(np.mean(f))
    return kind, [(h0 + y, x) for y, x in zip(f, xs)]
def first_note(rng, n, ch, h0, lo, hi):
    cands = [p for p in range(lo, hi + 1) if p % 12 in M.SCALE and not tri(p, ch)]
    return rng.choices(cands, [math.exp(-(p - h0) ** 2 / (2 * 1.5 ** 2)) * M.kp(p) * chord_w(p, n, ch) * deg_w(p) + 1e-12 for p in cands])[0]
def walk_notes(rng, notes, prev, run, mu, lo, hi, notes_on, fixed=None, shape=None):
    global SHAPE
    out = []; notes_on = set(notes_on) | {n["on"] for n in notes}; last_iv = None
    for i, n in enumerate(notes): n["dur"] = notes[i + 1]["on"] - n["on"] if i + 1 < len(notes) else 24
    for i, n in enumerate(notes):
        if fixed and i in fixed: p = fixed[i]
        elif n["slur"] and out:
            q_ = out[-1]; ch_ = M.chord_for(n, notes_on)
            opts = [x for x in (q_ - 2, q_ - 1, q_ + 1, q_ + 2) if lo <= x <= hi and x % 12 in M.SCALE and not tri(x, ch_)]
            p = rng.choices(opts, [(3 if x < q_ else 1) * chord_w(x, n, ch_) for x in opts])[0] if opts else q_
        elif shape is not None and i == 0:
            p = first_note(rng, n, M.chord_for(n, notes_on), shape[0][0], lo, hi)       # 259: not the next step from the line before
        else:
            tw = fixed.get(i + 1) if fixed else None
            SHAPE = shape[i] if shape is not None else None
            p = next_pitch(rng, prev, run, n, M.chord_for(n, notes_on), mu, lo, hi, last_iv, toward=tw); SHAPE = None
            if p is None: return None
        run = run + 1 if p == prev else 1
        last_iv = (p - prev) if prev is not None else last_iv
        prev = p; out.append(p)
    return out
def fresh_line(sy, rng, U, tmin, sec, last_max=None, fix=None, entry=None, i=None, partner=None, unitbars=None):
    if fix and len(fix) == len(sy):                                                   # a designed rhythm
        if fix[0] < tmin: return None
        return [dict(on=U + fix[k], p=None, syl=k, slur=False, stress=sy[k][1]) for k in range(len(sy))]
    kw = {}
    if partner is not None:
        if abs(partner[2] - len(sy)) > 1 and "322" not in OFF:                             # 322: another length: the partner's stressed onsets
            kw = dict(stressbars=stress_bars(partner[0], partner[1])); STATS["322: paired lines of another length"] += 1
        else: kw = dict(copybars=again_kw(partner[0], partner[1])["copybars"], pair=True, fallback=stress_bars(partner[0], partner[1]))  # 310; 330
    if not kw and unitbars: kw = dict(copybars=unitbars, allbars=True)                    # 361: the returning unit's onsets, bar by bar
    ons = line_rhythm(sy, rng, tmin, sec, last_max, fix, entry=entry, i=i, **kw)
    if ons is None: return None
    se = slot_end(sec, i); rows = melismas(ons, rng, se if last_max is None else min(se, last_max), PALS.get(KIND[sec])) if not fix or len(fix) < len(sy) else [[t, k, False] for k, t in enumerate(ons)]
    return [dict(on=U + t, p=None, syl=k, slur=s, stress=(sy[k][1] and not s)) for t, k, s in rows]

# 181's mapping, splits on the eighth grid
_src = inspect.getsource(M.align) + inspect.getsource(M._align)
_src = (_src.replace("def align(", "def align3(").replace("def _align(", "def _align3(").replace("r = _align(", "r = _align3(")
        .replace('min(12, 72 - ev[k]["t"])', 'min(12, END_T - ev[k]["t"])').replace("if d < 6: return None", "if d < MINSPLIT: return None")
        .replace("d // 2 // 3 * 3", "d // 2 // STEP * STEP").replace("gap = 6 if t0 - 6 * npk >= max(tmin, -12) else 3", "gap = 6 if t0 - 6 * npk >= max(tmin, -12) else STEP"))
exec(_src, M.__dict__)
ALIGN_END = [72]
def align(src, src_sy, sy, U0, U, tmin):
    M.END_T = ALIGN_END[0]; M.MINSPLIT = 12; M.STEP = 3 if "348" in OFF else 6            # 348: split on the eighth grid first (diagnostic: off)
    ns = M.align3(src, src_sy, sy, U0, U, tmin)
    if ns is None:
        M.STEP = 3; ns = M.align3(src, src_sy, sy, U0, U, tmin)                            # unless there is no room
        if ns is not None: STATS["348: a returning line split on the sixteenth grid (no room)"] += 1
    if ns is None or any((n["on"] - U) % 3 for n in ns): return None
    return ns

# ---- 239/246: the varied return ----
STATS = collections.Counter()
def _durs(ns):
    for j, n in enumerate(ns): n["dur"] = ns[j + 1]["on"] - n["on"] if j + 1 < len(ns) else 24
    return ns
def redraw_added(rng, ns, src_rel, U, lo, hi, notes_on):
    """246: an added note (an onset the source lacks) is drawn: repeat .28, step .48, leap .24 from the note before it."""
    on_all = set(notes_on) | {n["on"] for n in ns}
    for j, n in enumerate(ns):
        if n["on"] - U in src_rel or j == 0: continue
        prev = ns[j - 1]["p"]; ch = M.chord_for(n, on_all); kind = rng.choices(["repeat", "step", "leap"], [0.28, 0.48, 0.24])[0]
        sizes = {"repeat": [0], "step": [1, 2], "leap": [3, 4, 5]}[kind]
        opts = [prev + s * sz for sz in sizes for s in ((0,) if sz == 0 else (-1, 1))]
        nxt = ns[j + 1]["p"] if j + 1 < len(ns) else None
        opts = [p for p in opts if lo <= p <= hi and p % 12 in M.SUNGPC and not M.clash(p, ch) and not tri(p, ch) and (nxt is None or abs(nxt - p) <= 7)]
        if opts: n["p"] = rng.choice(opts); STATS["added_" + ("repeat" if n["p"] == prev else "step" if abs(n["p"] - prev) <= 2 else "leap")] += 1
        n["added"] = True
    return ns
def vary_return(rng, S, Ssy, sy, SU, U, tmin, lo, hi, notes_on, late=0.5, endok=None):
    last = None
    for _ in range(6):
        ns, kd = _vary_return(rng, S, Ssy, sy, SU, U, tmin, lo, hi, notes_on, late, endok)
        if ns is not None: return ns, kd
        if kd == "align": break
        last = LAST_TRY
    if last is not None:                                                               # 278: steered six times, then kept
        STATS["return: first or top note not kept (aim)"] += 1; return last
    return None, kd
LAST_TRY = None
def _vary_return(rng, S, Ssy, sy, SU, U, tmin, lo, hi, notes_on, late=0.5, endok=None):
    hi = max(hi, max(n["p"] for n in S)); lo = min(lo, min(n["p"] for n in S))
    ns = [dict(n) for n in S] if [x[0] for x in Ssy] == [x[0] for x in sy] else align(S, Ssy, sy, SU, U, tmin)
    if ns is None: return None, "align"
    if [x[0] for x in Ssy] == [x[0] for x in sy]:
        ns = [dict(n, on=n["on"] - SU + U) for n in S]
        if rng.random() >= late and (endok is None or endok(ns[-1]["p"])): return ns, "exact"
    src_rel = {n["on"] - SU for n in S}; src_p = {n["on"] - SU: n["p"] for n in S}
    ns = _durs([dict(n) for n in ns]); [n.pop("hold", None) for n in ns]
    ns = redraw_added(rng, ns, src_rel, U, lo, hi, notes_on)
    span = max(n["on"] - U for n in ns); q4 = 0.75 * span                                 # 239(c): the change in the last quarter
    idx = []
    if rng.random() < late or (endok is not None and not endok(ns[-1]["p"])):
        idx = [j for j, n in enumerate(ns) if n["on"] - U >= q4 and j > 0 and not (n["on"] % BEAT == 0 and (n["on"] - U) in src_rel)]
        if endok is not None and not endok(ns[-1]["p"]) and len(ns) - 1 not in idx: idx.append(len(ns) - 1)
        for j in idx:
            prev = ns[j - 1]["p"]; ch = M.chord_for(ns[j], notes_on)
            opts = [prev + d for d in (-2, -1, 0, 1, 2, -3, 3, -4, 4) if lo <= prev + d <= hi and (prev + d) % 12 in M.SCALE and not tri(prev + d, ch)]
            if j == len(ns) - 1 and endok is not None: opts = [q for q in opts if endok(q)] or opts      # 295: drawn among the permitted degrees
            if opts: ns[j]["p"] = rng.choice(opts)
    late_set = set(idx) | {j for j, n in enumerate(ns) if n.get("added")}
    ns = repair(rng, _durs(ns), None, lo, max(hi, max(n["p"] for n in S)), notes_on, keep={j for j in range(len(ns)) if j not in late_set})   # 287
    if endok is not None and not endok(ns[-1]["p"]): STATS["295: returning last line still off its ending"] += 1
    global LAST_TRY
    rch = len({n["on"] - U for n in ns} ^ src_rel) > 0
    pch = any(src_p[n["on"] - U] != n["p"] for n in ns if n["on"] - U in src_rel) or any(n.get("added") for n in ns)
    kd_ = {(False, False): "exact", (True, False): "rhythm", (False, True): "pitch", (True, True): "both"}[(rch, pch)]
    sh = [j for j, n in enumerate(ns) if n["on"] - U in src_rel]
    LAST_TRY = (ns, kd_)
    if max(n["p"] for n in ns) < max(n["p"] for n in S): return None, "kept"                 # 239(f): the top note kept or higher
    if not sh or ns[sh[0]]["p"] != S[0]["p"]: return None, "kept"                          # 239(b): the first note kept
    return ns, kd_

# ---- 228: sung again ----
def sing_again(rng, S, Ssy, sy, SU, U, tmin, sec, lo, hi, notes_on, last_max=None, ons=None):
    """verse 1's line as contour and cadence; the rhythm fitted again to the new words; a stressed note on a beat moves a step to a
    chord tone where it lands on none."""
    i_ = int(S[0]["line"].split(":")[1]) if "line" in S[0] else None
    if ons is None:
        ons = line_rhythm(sy, rng, tmin, sec, last_max, i=i_, **again_kw(S, SU))
        if ons is None: return None
    se = slot_end(sec, i_); rows = melismas(ons, rng, se if last_max is None else min(se, last_max))
    ns = _durs([dict(on=U + t, p=None, syl=k, slur=s, stress=(sy[k][1] and not s)) for t, k, s in rows])
    srel = [(n["on"] - SU, n["p"]) for n in S]; s0, s1 = srel[0][0], srel[-1][0]; n0, n1 = ns[0]["on"] - U, ns[-1]["on"] - U
    on_all = set(notes_on) | {n["on"] for n in ns}
    for j, n in enumerate(ns):
        x = (n["on"] - U - n0) / max(1, n1 - n0) * (s1 - s0) + s0
        n["p"] = min(srel, key=lambda e: abs(e[0] - x))[1]
    ns[-1]["p"] = S[-1]["p"]; ns[0]["p"] = S[0]["p"]
    for n in ns:
        ch = M.chord_for(n, on_all); tones = M.CH[ch][1]
        if (n["stress"] and n["on"] % BEAT == 0 and n["p"] % 12 not in tones) or tri(n["p"], ch):
            opts = [n["p"] + d for d in (-1, 1, -2, 2) if (n["p"] + d) % 12 in tones and lo <= n["p"] + d <= hi]
            if opts: n["p"] = opts[0]
    return repair(rng, ns, None, lo, hi, on_all, keep={0, len(ns) - 1})
def stress_bars(S, SU):
    """322: the partner's stressed onsets, bar by bar (relative to its line's start)."""
    sb = collections.defaultdict(set)
    for n in S:
        t = n["on"] - SU
        if t >= 0 and n.get("stress"): sb[t // BAR].add(t)
    return dict(sb)
def again_kw(S, SU):
    """297: a verse-2 line takes its source's entry; 293: its bar rhythms are drawn from the source's bars at 40% (line_rhythm)."""
    cb = collections.defaultdict(list)
    for n in S:
        t = n["on"] - SU
        if t >= 0: cb[t // BAR].append(t)
    return dict(entry=entry_kind(S[0]["on"] - SU), copybars=dict(cb))
def repair(rng, ns, prev, lo, hi, notes_on, keep=()):
    """a mapped line's leaps past a sixth, tritones and runs of four are re-walked, the other notes held."""
    for _pass in range(5):
        bad = set(); run = 1
        for j in range(1, len(ns)):
            iv = abs(ns[j]["p"] - ns[j - 1]["p"]); run = run + 1 if iv == 0 else 1
            if iv > 9 or iv == 6: bad.add(j if j not in keep else j - 1)
        bad -= set(keep)
        if not bad: return ns
        mu = float(np.median([n["p"] for n in ns]))
        ps = walk_notes(rng, ns, prev if 0 in bad else None, 1, mu, lo, hi, notes_on, fixed={j: ns[j]["p"] for j in range(len(ns)) if j not in bad})
        if ps:
            for n, p in zip(ns, ps): n["p"] = p if p % 12 in M.SCALE or not M.clash(p, M.chord_for(n, notes_on)) else n["p"]
    return ns

# ---- 218/288: holds, up to eight note lengths at the class's kept rates ----
GAP_MIN = 18
PALETTE = (3, 6, 9, 12, 18, 24, 36, 48)                                               # 288: sixteenth to whole bar (eight)
KEPT_RATE = {6: 0.431, 9: 0.055, 12: 0.204, 18: 0.050, 24: 0.040, 36: 0.031, 48: 0.031}  # v88 rhythm_by_class pop (mean), 'longer' split 36/48
END_LENS = (48, 36, 24, 18, 12, 9, 6)
def finish(notes, rng):
    for i, n in enumerate(notes):
        nx = notes[i + 1]["on"] if i + 1 < len(notes) else None
        if "fixdur" in n: n["dur"] = n["fixdur"]; continue
        if nx is None: n["dur"] = 48 if n.get("title") else 24
        elif notes[i + 1]["line"] != n["line"]:
            room = nx - n["on"] - 6
            if "hold" not in n:                                                               # 306: the last note from the kept ratio to the line's mean note
                ln = [m for m in notes if m["line"] == n["line"] and m is not n]
                S = sum(m.get("dur", 12) for m in ln); k_ = len(ln) + 1
                r_ = float(np.interp(rng.random(), [0, .05, .25, .5, .75, .95, 1], [0.867, 0.867, 1.182, 1.478, 1.714, 2.298, 2.298]))
                want = r_ * S / max(0.5, k_ - r_)
                if n.get("title"): want = max(want, 24)                                        # 232 over 306: the title's stress held two beats or more
                pl = PALS.get(KIND.get(n.get("sec"), ""), PALETTE)                                 # 343: the line-end hold from the section's palette
                opts = [L_ for L_ in pl if L_ <= max(3, room)] or [L_ for L_ in PALETTE if L_ <= max(3, room)] or [3]
                n["hold"] = min(opts, key=lambda L_: abs(L_ - want))
            n["dur"] = max([L_ for L_ in PALETTE if L_ <= max(3, room) and L_ <= n["hold"]] or [3])
        else: n["dur"] = nx - n["on"]
    return notes

# ---- 181/219/248: the return gate on lines, on shared events ----
def unit_lines(notes, a, b2, U, keep=None):
    ns = [n for n in notes if a <= n["on"] < b2 and (keep is None or n["on"] - U in keep)]
    if len(ns) < 2: return set(), [], ns
    ons = {n["on"] - U for n in ns}; body = ns[:-1]; ser = []; k = 0; cur = body[0]["p"]
    for t in range(U, body[-1]["on"] + 3, 3):
        while k < len(body) and body[k]["on"] <= t: cur = body[k]["p"]; k += 1
        ser.append(cur)
    return ons, ser, ns
def related_lines(u1, u2):
    o1, s1, _ = u1; o2, s2, _ = u2
    if not o1 or not o2: return False, 0.0, 0.0
    jac = len(o1 & o2) / len(o1 | o2); n = min(len(s1), len(s2))
    a, b2 = np.array(s1[:n], float), np.array(s2[:n], float)
    if n < 2 or (a.std() == 0 and b2.std() == 0): r = 1.0 if n >= 2 else 0.0
    elif a.std() == 0 or b2.std() == 0: r = 0.0
    else: r = float(np.corrcoef(a, b2)[0, 1])
    return (jac >= 0.6 and r >= 0.6), jac, r
def line_span(notes, sec, i):
    ln = [n for n in notes if n["line"] == f"{sec}:{i}"]
    nxt = [n for n in notes if n["line"] == f"{sec}:{i + 1}"]
    a = ln[0]["on"]; b2 = nxt[0]["on"] if nxt else max(n["on"] for n in ln) + 1
    return a, b2, line_start(sec, i)
def returns_related(c):
    out = []
    for sec, i, s0, i0, kind in c["meta"]["returns"]:
        if kind == "sung again": continue
        a, b2, U = line_span(c["notes"], sec, i); a0, b0, U0 = line_span(c["notes"], s0, i0)
        shared = {n["on"] - U for n in c["notes"] if a <= n["on"] < b2} & {n["on"] - U0 for n in c["notes"] if a0 <= n["on"] < b0}
        out.append(((sec, i, s0, i0, kind),) + related_lines(unit_lines(c["notes"], a, b2, U, shared), unit_lines(c["notes"], a0, b0, U0, shared)))
    return out
def opening_rel(notes, s1, s2):
    return related_lines(unit_lines(notes, *line_span(notes, s1, 0)), unit_lines(notes, *line_span(notes, s2, 0)))

# ---- plans (181, 205, 213): a return only between lines of the same slot ----
VERSE_PLANS = [("ABCDAB", 0.25), ("ABCDAE", 0.25), ("ABCCAB", 0.15), ("ABCCDE", 0.15), ("ABCDEF", 0.20)]
BRIDGE_PLANS = [("ABCABC", 0.25), ("ABCADE", 0.25), ("ABCDBE", 0.15), ("ABCDEF", 0.35)]
PRE_PLANS = [("AB", 0.75), ("AA", 0.25)]
PAIRS = {"Verse": ["Verse 1", "Verse 2"], "Pre": ["Pre 1", "Pre 2"], "Bridge": ["Bridge"]}
def admissible(sec, plan):
    for i, x in enumerate(plan):
        j = plan.index(x)
        if j != i and (slot_len(sec, i) != slot_len(sec, j) or any(abs(len(LINES[s][i]) - len(LINES[s][j])) > 3 for s in PAIRS[KIND[sec]])): return False
    return True
def draw_plan(rng, sec, plans):
    plans = [(p[:len(LINES[sec])], w) for p, w in plans]                                  # four-line sections: each plan cut to its first lines
    ok = [(p, w) for p, w in plans if admissible(sec, p)] or [("ABCDEF"[:len(LINES[sec])], 1.0)]
    pl = list(rng.choices([p for p, _ in ok], [w for _, w in ok])[0])
    if len(pl) >= 4 and all(x == 2 for x in slots_of(sec)):                                # 346: a later unit returns an earlier one at the kept rates
        for j, src, rate in ((1, 0, 0.172), (2, 0, 0.315), (3, 1, 0.188)):                     # 346; 350: unit 3 returns unit 1
            if pl.index(pl[j]) == j and rng.random() < rate:
                tr = pl[:j] + [pl[src]] + pl[j + 1:]
                if admissible(sec, "".join(tr)): pl = tr; STATS[f"346: line {j + 1} returns line {src + 1}"] += 1
    return pl
SRC = {"Verse 2": "Verse 1", "Chorus 2": "Chorus 1", "Last Chorus": "Chorus 1"}

# ---- 288: section registers drawn from the kept distribution (chorus and bridge against the verse) ----
QS = [1, 5, 25, 50, 75, 95, 99]
REG = SR["section registers, kept percentiles (1, 5, 25, 50, 75, 95, 99)"]
def kept_draw(key, u): return float(np.interp(100 * u, QS, REG[key]))
V_MU, V_CAP, V_FLOOR = 64, 69, 57                                                     # replaced per build by 314's draw (below)
ROW_LO, ROW_HI = M.LO, TOP; PLACE = "high"                                             # Q14 A: the song placed high in the row, so the chorus opens to its top                                           # 314: the row, and the writer's placement (centre unless chosen)
Q5 = [5, 25, 50, 75, 95]
def kq(vals, u): return float(np.interp(100 * u, [0] + Q5 + [100], [vals[0] - (vals[1] - vals[0])] + list(vals) + [vals[-1] + (vals[-1] - vals[-2])]))
def draw_song_range(rng):
    """314: the song's range drawn at the kept shares, cut to the row, centred (unused semitones split, the odd one above)."""
    row = ROW_HI - ROW_LO; r = int(round(min(row - 2, max(5, kq(K314["the song's sung range, semitones (5, 25, 50, 75, 95)"], rng.random())))))   # 333
    spare = row - r
    lo = ROW_LO + (spare // 2 if PLACE == "centre" else 0 if PLACE == "low" else spare); return lo, lo + r
ENDING_NEEDS = {}                                                                     # 311: kind -> the degrees an ending section must find in its register
DESIGN_REG = []                                                                       # 325: (name, test on the drawn registers); none on the default path
def draw_registers(rng):
    global V_MU, V_CAP, V_FLOOR
    for tries in range(50):
        R_, info = _draw_registers(rng)
        ok = all(any(p % 12 in need for p in range(int(R_[k][2]), int(R_[k][1]) + 1)) for k, need in ENDING_NEEDS.items())
        dz = [nm for nm, t in DESIGN_REG if not t(R_, info)]
        if ok and not dz: break
        if not ok: STATS["311: register redrawn for its ending"] += 1
        for nm in dz: STATS["325: register redrawn for a design: " + nm] += 1
    else: STATS["311/325: ending or design missing after 50 draws"] += 1
    info["redraws"] = tries; return R_, info
def _draw_registers(rng):
    global V_MU, V_CAP, V_FLOOR
    lo, hi = draw_song_range(rng); r = hi - lo; us = rng.random()
    V_MU = lo + kq(K314["verse median"], us) * r; V_FLOOR = max(lo, int(round(V_MU - 7))); V_CAP = min(hi, int(round(V_MU + 5)))
    R_, info = draw_registers_288(rng, lo, hi)
    info.update(song_lo=lo, song_hi=hi, song_range=r, verse_share=round((V_MU - lo) / max(1, r), 3), v_mu=V_MU, v_cap=R_["Verse"][1], v_floor=R_["Verse"][2],
                sections={k: tuple(round(x, 2) for x in v) for k, v in R_.items()})
    return R_, info
def draw_registers_288(rng, lo, hi):
    u = rng.random(); ub = rng.random()                                               # chorus median, top and lowest drawn together; the bridge apart
    lm, lt, lf, lb = kept_draw("chorus_median_minus_verse", u), kept_draw("chorus_top_minus_verse", u), kept_draw("chorus_floor_minus_verse", u), kept_draw("bridge_median_minus_verse", ub)
    c_mu = min(hi - 2, max(lo + 2, V_MU + lm)); c_cap = int(round(min(hi, max(c_mu + 3, V_CAP + lt)))); c_floor = int(round(max(lo, min(c_mu - 3, V_FLOOR + lf))))
    b_mu = min(hi - 2, max(lo + 2, V_MU + lb))
    R = {"Verse": (V_MU, V_CAP, V_FLOOR), "Chorus": (c_mu, c_cap, c_floor), "Pre": ((V_MU + c_mu) / 2, max(V_CAP, c_cap), V_FLOOR),
         "Bridge": (b_mu, int(round(min(hi, b_mu + 6))), int(round(max(lo, b_mu - 7))))}
    R["Tag"] = R["Chorus"]                                                             # the tag sings in the chorus's register
    R = {k: widen_329(v, lo, hi) for k, v in R.items()}
    vf_ = lo + (1 if rng.random() < 0.5 else 0); vc_ = min(hi - 3, vf_ + 8); vm_ = (vf_ + vc_) / 2           # Q14 A: the verse low and narrow (eight semitones)
    ch_ = hi; cl_ = max(lo, min(vc_ - 2, ch_ - 10)); cm_ = (cl_ + ch_) / 2                                     # the chorus over it, to the song's top
    R["Verse"] = (vm_, vc_, vf_); R["Chorus"] = (cm_, ch_, cl_); R["Tag"] = R["Chorus"]
    globals().update(V_MU=vm_, V_CAP=vc_, V_FLOOR=vf_)
    return R, dict(u=u, ub=ub, chorus_median=lm, chorus_top=lt, chorus_floor=lf, bridge_median=lb)
WIN_MIN = 13                                                                          # 329: the kept eight-bar range's 75th percentile (8 to 13)
def widen_329(reg, lo, hi):
    """329: a section's floor and cap no narrower than the kept window range allows, inside the song's range; the cap first."""
    mu, cap, fl = reg; need = WIN_MIN - (cap - fl)
    if need > 0:
        up = min(hi - cap, (need + 1) // 2); cap += up; need -= up
        dn = min(fl - lo, need); fl -= dn; need -= dn
        cap += min(hi - cap, max(0, need))
        STATS["329: a section's register widened"] += 1
    return (mu, cap, fl)

# ---- 262/295: how a section ends; endings drawn, not moved ----
TRIAD = {7, 11, 2}
ENDING_NEEDS.update(Verse={2, 9})                                                     # 311: the verse closes on D or A, over its D (the half cadence)
def end_ok(sec, i, p):
    if i != len(LINES[sec]) - 1: return True
    if sec == "Verse 1": return p % 12 in (2, 9)
    return True                                                                         # the choruses and the tag end on designed notes (Q15 A)
def end_target(sec, i, h_end, lo, hi, mu=None):
    """295: the contour of an ending line is drawn toward the nearest permitted ending; 314: a tonic ending toward the tonic nearest the
    section's median."""
    c = [p for p in range(lo, hi + 1) if p % 12 in M.SCALE and end_ok(sec, i, p)]
    if mu is not None and c and all((p - M.TONIC) % 12 == 0 for p in c): return min(c, key=lambda p: (abs(p - mu), p))
    return min(c, key=lambda p: abs(p - h_end)) if c else h_end
def end_rule(sec, i, ns, notes_on, lo, hi):
    if end_ok(sec, i, ns[-1]["p"]): return
    n = ns[-1]; ch = M.chord_for(n, set(notes_on) | {x["on"] for x in ns}); q0 = n["p"]
    opts = [q0 + d for d in (-1, 1, -2, 2, -3, 3) if lo <= q0 + d <= max(hi, q0) and (q0 + d) % 12 in M.SCALE and not tri(q0 + d, ch) and end_ok(sec, i, q0 + d)]
    if opts: n["p"] = opts[0]; STATS["262: last note moved"] += 1

def generate(rng, cal=None):
    """one build. cal: a calibration build (targets at the pools' medians)."""
    global AIM
    meta = dict(returns=[], kinds={}, win={}, targets={})
    for p in ("V", "C"):
        i, t = (None, dict(MED[p])) if cal else draw_targets(rng, p)
        meta["win"][p] = i; meta["targets"][p] = t; AIMS[p] = Aim(t, p)
    REGS, meta["registers"] = draw_registers(rng)
    PALS.clear()
    for k_ in sorted({KIND[s_] for s_ in SUNG}):                                           # 343
        K_ = rng.choices(*PAL_K)[0]; pool = [L_ for L_ in RATE343]; pal = {6}
        while len(pal) < K_ and pool:
            L_ = rng.choices(pool, [RATE343[x] for x in pool])[0]; pal.add(L_); pool.remove(L_)
        PALS[k_] = pal
    OS_T[0] = 0.0 if rng.random() < 0.5 else rng.choice(OS_KEPT) * OS_SCALE                    # 344; 349: a minor song at the kept minor rate
    meta["os_carry"] = 0.0
    meta["palettes"] = {k_: sorted(v) for k_, v in PALS.items()}; meta["outside_target"] = OS_T[0]
    plans = dict(Verse=draw_plan(rng, "Verse 1", VERSE_PLANS), Bridge=draw_plan(rng, "Bridge", BRIDGE_PLANS),
                 tail=rng.choice(["return", "fresh"]), line5=rng.choice(["return", "fresh"]))
    meta["plans"] = plans
    UR = {}                                                                              # 361: unit returns on the bar grid, for sections not all of two-bar lines
    for k_ in sorted({KIND[s_] for s_ in SUNG}):
        s1_ = next(s_ for s_ in SUNG if KIND[s_] == k_)
        if all(x == 2 for x in slots_of(s1_)) or SECLEN[s1_] < 8 or "361" in OFF: continue
        UR[k_] = {}
        for j, src, rate in ((1, 0, 0.172), (2, 0, 0.315), (3, 1, 0.188)):
            if rng.random() < rate: UR[k_][j] = src; STATS[f"361: unit {j + 1} returns unit {src + 1} (bar grid), drawn"] += 1
    meta["unit_returns"] = {k_: dict(v) for k_, v in UR.items()}
    meta["tonic_endings"] = []
    built, lines = {}, []; prev, run, last_on = None, 0, -10 ** 6; notes_on_all = set(); pending = {}
    meta["contour"] = {}; meta["free"] = collections.Counter(); meta["moved"] = 0
    def _fail(err): return dict(notes=sorted([dict(n) for l in lines for n in l], key=lambda n: n["on"]), meta=meta, partial=True), err
    def place(sec, i, ns):
        nonlocal prev, run, last_on
        for n in ns:
            n["sec"] = sec; n["line"] = f"{sec}:{i}"
            if is_title(sec, i) and n is ns[-1]: n["title"] = True
        built[(sec, i)] = ns; lines.append(ns)
        prev = ns[-1]["p"]; last_on = ns[-1]["on"]; rr = 1
        for a, b2 in zip(ns[::-1], ns[-2::-1]):
            if a["p"] == b2["p"]: rr += 1
            else: break
        run = rr
    def how(sec, i):
        """('copy'|'return'|'again'|'plan'|'fresh'|'tail', source section, source line)."""
        kind = KIND[sec]
        if sec == "Chorus 2": return ("copy", "Chorus 1", i)
        if sec == "Last Chorus": return ("return", "Chorus 1", i) if i in (1, 2) else ("fresh", None, None)   # the morning's words on the chorus's tune (line 0 designed on it); its last line new
        if sec == "Verse 2": return ("again", "Verse 1", i)
        if kind in ("Chorus", "Tag"): return ("fresh", None, None)
        plan = plans[kind]; first = plan.index(plan[i])
        return ("plan", sec, first) if first < i else ("fresh", None, None)
    # 329: one fresh line carries the song's lowest drawn note (a verse or the bridge), one its highest (a chorus or the bridge)
    xlo = min(p for p in range(meta["registers"]["song_lo"], meta["registers"]["song_hi"] + 1) if p % 12 in M.SCALE)
    xhi = max(p for p in range(meta["registers"]["song_lo"], meta["registers"]["song_hi"] + 1) if p % 12 in M.SCALE)
    lowc = [(s_, j) for s_ in SUNG if s_ in CARRY_LOW for j in range(len(LINES[s_])) if how(s_, j)[0] == "fresh"]
    highc = [(s_, j) for s_ in SUNG if s_ in CARRY_HIGH for j in range(len(LINES[s_])) if how(s_, j)[0] == "fresh"]
    car_lo = rng.choice(lowc) if lowc else None
    highc = [x for x in highc if x != car_lo] or highc
    car_hi = rng.choice(highc) if highc else None
    CARRY = {}
    if "329" in OFF: car_lo = car_hi = None                                                 # diagnostics only
    if car_lo: CARRY[car_lo] = xlo
    if car_hi: CARRY[car_hi] = xhi
    meta["carriers"] = dict(low=(car_lo, xlo), high=(car_hi, xhi))
    for (s_, j), x in CARRY.items():                                                       # the carrying section's register reaches it
        k_ = KIND[s_]; mu_, cap_, fl_ = REGS[k_]; REGS[k_] = (mu_, max(cap_, x), min(fl_, x))
    def endok_of(sec, i):
        rule = sec == "Verse 1" and i == len(LINES[sec]) - 1
        return (lambda p: end_ok(sec, i, p)) if rule else None
    def prefit(sec, i):
        """247: a copy, return or re-sung line is fitted to its words before the line ahead of it is drawn."""
        if (sec, i) in pending: return pending[(sec, i)]
        h, s0, i0 = how(sec, i); U = line_start(sec, i); r = None
        if (sec, i) in FIXR: r = ("ons", [FIXR[(sec, i)][k] for k in sorted(FIXR[(sec, i)])], None)   # Q15 A: the designed rhythm, known ahead
        if h in ("copy", "return", "plan", "tail") and (s0, i0) in built:
            S = built[(s0, i0)]; SU = line_start(s0, i0); lo_, hi_ = REGS[KIND[sec]][2], REGS[KIND[sec]][1]
            if h == "copy": r = ("ns", [dict(n, on=n["on"] - SU + U) for n in S], "exact")
            elif h == "tail":
                k0 = len(LINES[s0][i0]) - len(LINES[sec][i])
                r = ("ns", [dict(n, on=n["on"] - SU + U, syl=n["syl"] - k0) for n in S if n["syl"] >= k0], "exact")
            else:
                ALIGN_END[0] = slot_end(sec, i)
                ns, kd = vary_return(rng, S, LINES[s0][i0], LINES[sec][i], SU, U, -12, lo_, hi_, notes_on_all, endok=endok_of(sec, i))
                r = ("ns", ns, kd) if ns else ("fail", kd, None)
        elif h == "again" and (s0, i0) in built:
            AIMP = AIM; globals()["AIM"] = AIMS[pool_of(sec)]
            ons = line_rhythm(LINES[sec][i], rng, -12, sec, i=i, **again_kw(built[(s0, i0)], line_start(s0, i0))); globals()["AIM"] = AIMP
            r = ("ons", ons, None) if ons else ("fail", None, None)
        if r is not None: pending[(sec, i)] = r
        return r
    def refit_327(sec2, i2):
        """327: the copy after a line that cannot breathe, fitted again with no pickup added before its source's entry; a unit's last
        line so fitted keeps the ordinary end (beat 4 of a one-bar line) instead of 310's beat 3. An exact copy cannot move."""
        pf = pending.get((sec2, i2))
        if not pf or pf[0] == "fail": return False
        U2 = line_start(sec2, i2); f0 = (pf[1][0]["on"] - U2) if pf[0] == "ns" else pf[1][0]
        if f0 > 0: return False
        h2, s2, j2 = how(sec2, i2)
        if h2 in ("return", "plan") and (s2, j2) in built:
            S = built[(s2, j2)]; SU = line_start(s2, j2); lo_, hi_ = REGS[KIND[sec2]][2], REGS[KIND[sec2]][1]
            ALIGN_END[0] = ordinary_end(sec2, i2)
            ns2, kd = vary_return(rng, S, LINES[s2][j2], LINES[sec2][i2], SU, U2, 6, lo_, hi_, notes_on_all, endok=endok_of(sec2, i2))
            if ns2 and ns2[0]["on"] - U2 > f0:
                pending[(sec2, i2)] = ("ns", ns2, kd); STATS[f"327: {h2} fitted again without a pickup" + (", ordinary end" if unit_end(sec2, i2) else "")] += 1; return True
        elif h2 == "again" and (s2, j2) in built:
            AIMP = globals()["AIM"]; globals()["AIM"] = AIMS[pool_of(sec2)]
            ons = line_rhythm(LINES[sec2][i2], rng, 6, sec2, i=i2, **again_kw(built[(s2, j2)], line_start(s2, j2))); globals()["AIM"] = AIMP
            if ons and ons[0] > f0: pending[(sec2, i2)] = ("ons", ons, None); STATS["327: sung-again line fitted after its downbeat"] += 1; return True
        STATS[f"327: copy could not enter later ({h2}, entry {'pickup' if f0 < 0 else 'on'})"] += 1
        return False
    for sec in SUNG:
        kind = KIND[sec]; mu, hi, lo = REGS[kind]; sys_ = LINES[sec]; AIM = AIMS[pool_of(sec)]; SEC_USED.clear()
        for i, sy in enumerate(sys_):
            U = line_start(sec, i); tmin = max(-12, last_on + GAP_MIN - U)
            nxt = (sec, i + 1) if i + 1 < len(sys_) else ((SUNG[SUNG.index(sec) + 1], 0) if SUNG.index(sec) + 1 < len(SUNG) else None)
            last_max = None
            if nxt:
                pf = prefit(*nxt)
                if pf and pf[0] == "fail": globals().__setitem__("WHERE", ("prefit",) + tuple(nxt) + (how(*nxt)[0],)); return _fail(("align: the words do not fit the returning tune" if pf[1] == "align" else "rhythm: no placement"))
                f0 = None
                if pf and pf[1]: f0 = (pf[1][0]["on"] - line_start(*nxt)) if pf[0] == "ns" else pf[1][0]
                if f0 is not None: last_max = (line_start(*nxt) + f0 - U) - GAP_MIN
            h, s0, i0 = how(sec, i)
            if h in ("copy", "return", "plan", "tail") and (prefit(sec, i) or ("",))[0] == "ns":
                _, ns, kd = pending[(sec, i)]; ns = [dict(n) for n in ns]
                for n in ns: n.pop("hold", None); n.pop("title", None)
                meta["kinds"][(sec, i)] = kd if h != "tail" else "tail"
                if h in ("return", "plan"): meta["returns"].append((sec, i, s0, i0, kd))
            elif h == "again":
                pf = pending.get((sec, i)); S = built[(s0, i0)]
                if pf and pf[1] and ((last_max is not None and pf[1][-1] > last_max) or pf[1][0] < tmin): pf = None   # redrawn against the line ahead (247)
                ns = sing_again(rng, S, LINES[s0][i0], sy, line_start(s0, i0), U, tmin, sec, lo, hi, notes_on_all, last_max, ons=pf[1] if pf else None)
                if ns is None: globals().__setitem__("WHERE", (sec, i)); return _fail("rhythm: no placement")
                meta["returns"].append((sec, i, s0, i0, "sung again")); meta["kinds"][(sec, i)] = "sung again"
            elif h in ("copy", "return", "plan", "tail"):
                globals().__setitem__("WHERE", (sec, i)); return _fail("align: the words do not fit the returning tune")
            else:
                pj = pair_of(sec, i); partner = (built[(sec, pj)], line_start(sec, pj), len(LINES[sec][pj])) if pj is not None and (sec, pj) in built else None
                if partner is not None: STATS["310: paired lines"] += 1
                ub, upit = {}, {}                                                          # 361: the bars of a returning unit this line covers
                for bl in range(slot_len(sec, i)):
                    ba = U // BAR + bl; rel = ba - BAR0[sec]; j = rel // 2
                    src = UR.get(kind, {}).get(j) if rel < 8 else None
                    if src is None: continue
                    sba = BAR0[sec] + 2 * src + rel % 2
                    if (BAR0[sec] + 2 * src + 2) * BAR > U: STATS["361: unit return inside one line, not drawn"] += 1; continue
                    sn = [n_ for l_ in lines for n_ in l_ if n_["sec"] == sec and sba * BAR <= n_["on"] < (sba + 1) * BAR]
                    if not sn: continue
                    ub[bl] = [bl * BAR + n_["on"] % BAR for n_ in sn]
                    for n_ in sn: upit[U + bl * BAR + n_["on"] % BAR] = n_["p"]
                if ub and partner is not None: STATS["361: unit return under a paired line (310 kept)"] += 1; ub, upit = {}, {}
                ns = fresh_line(sy, rng, U, tmin, sec, last_max, FIXR.get((sec, i)), i=i, partner=partner, unitbars=ub or None)
                if ns is None: globals().__setitem__("WHERE", (sec, i)); return _fail("rhythm: no placement")
                if (sec, i) in PIN: ns = [n_ for n_ in ns if not n_["slur"]]                   # Q15 A: one note a syllable where the notes are designed
                meta["free"][sec] += len(ns)
                ps = None; need_end = endok_of(sec, i) is not None
                for _try in range(8):
                    _durs(ns); ck, shape = draw_shape(rng, ns, mu, lo, hi); meta["contour"][(sec, i)] = ck
                    if upit:                                                              # 361: the earlier unit's pitches as the contour
                        shape = [((upit[n_["on"]] if n_["on"] in upit else h_), x_) for n_, (h_, x_) in zip(ns, shape)]
                    fx = None
                    if need_end:                                                          # 302: the last note drawn first, the walk runs back to it
                        if upit and ns[-1]["on"] in upit: shape[-1] = (end_target(sec, i, shape[-1][0], lo, hi, mu), shape[-1][1])
                        tgt = end_target(sec, i, shape[-1][0], lo, hi, mu); d = tgt - shape[-1][0]
                        shape = [(h_ + d * x, x) for h_, x in shape]
                        cands = [p for p in range(lo, hi + 1) if p % 12 in M.SCALE and end_ok(sec, i, p) and not tri(p, M.chord_for(ns[-1], notes_on_all | {x_["on"] for x_ in ns}))]
                        if cands:
                            last_p = tgt if tgt in cands and all((p - M.TONIC) % 12 == 0 for p in cands) else rng.choices(cands, [math.exp(-(p - tgt) ** 2 / 4.5) for p in cands])[0]   # 314
                            if ns[-1]["slur"] and len(ns) > 1: fx = {len(ns) - 1: last_p}
                            else: fx = {len(ns) - 1: last_p}
                    if (sec, i) in PIN or (sec, i) in HOLDP or (sec, i) in COPYON:         # Q15 A: the designed notes
                        fx = dict(fx or {})
                        if (sec, i) in COPYON:
                            S_ = built[COPYON[(sec, i)]]; SU_ = line_start(*COPYON[(sec, i)]); sp_ = {n_["on"] - SU_: n_["p"] for n_ in S_ if not n_["slur"]}
                            for j, n_ in enumerate(ns):
                                if n_["on"] - U in sp_ and lo <= sp_[n_["on"] - U] <= hi: fx[j] = sp_[n_["on"] - U]
                            for j in range(1, len(ns) - 1):                                    # a syllable between two of them: a step between, not a leap
                                if j not in fx and j - 1 in fx and j + 1 in fx:
                                    a_, b_ = fx[j - 1], fx[j + 1]; ch_ = M.chord_for(ns[j], notes_on_all | {x_["on"] for x_ in ns})
                                    cq = [p for p in range(min(a_, b_) - 1, max(a_, b_) + 2) if p % 12 in M.SCALE and lo <= p <= hi and not tri(p, ch_)]
                                    if cq: fx[j] = min(cq, key=lambda p: (abs(p - (a_ + b_) / 2), p == a_, p))
                        for k_, q_ in PIN.get((sec, i), {}).items(): fx[next(j for j, n_ in enumerate(ns) if n_["syl"] == len(sy) + k_)] = q_
                        if (sec, i) in HOLDP:                                                  # 'thought': G or D in the register, near the contour
                            j_ = next(j for j, n_ in enumerate(ns) if n_["syl"] == HOLDP[(sec, i)])
                            cq = [p for p in range(lo, hi + 1) if p % 12 in (7, 2)]
                            fx[j_] = rng.choices(cq, [math.exp(-(p - shape[j_][0]) ** 2 / 8) + 1e-9 for p in cq])[0]
                    if (sec, i) in CARRY and _try < 6:                                    # 329: the drawn extreme on this line
                        x = CARRY[(sec, i)]; hiq = x >= mu; on_ = notes_on_all | {x_["on"] for x_ in ns}
                        order_ = sorted(range(len(ns)), key=lambda j: -shape[j][0] if hiq else shape[j][0])
                        jx = next((j for j in order_ if not ns[j]["slur"] and not (fx and j in fx) and not tri(x, M.chord_for(ns[j], on_))
                                   and not M.clash(x, M.chord_for(ns[j], on_))), None)
                        if jx is not None:
                            d0 = x - shape[jx][0]; xj = shape[jx][1]
                            shape = [(h_ + d0 * math.exp(-((x_ - xj) / 0.25) ** 2), x_) for h_, x_ in shape]
                            fx = dict(fx or {}); fx[jx] = x
                        else: STATS["329: no note on the carrying line can take the extreme"] += 1
                    elif (sec, i) in CARRY and _try == 6: STATS["329: extreme dropped after six tries"] += 1
                    if upit:                                                              # 361: the earlier unit's pitches kept where the chord allows
                        on_ = notes_on_all | {x_["on"] for x_ in ns}; fx = dict(fx or {})
                        for j_, n_ in enumerate(ns[:-1]):
                            q_ = upit.get(n_["on"])
                            if q_ is not None and j_ not in fx and lo <= q_ <= hi and not n_["slur"] and not tri(q_, M.chord_for(n_, on_)) and not M.clash(q_, M.chord_for(n_, on_)): fx[j_] = q_
                    ps = walk_notes(rng, ns, prev, run, mu, lo, hi, notes_on_all, fixed=fx, shape=shape)
                    if ps is None: continue
                    if need_end and not end_ok(sec, i, ps[-1]) and _try < 7: ps = None; continue
                    break
                if ps is None: globals().__setitem__("WHERE", (sec, i)); return _fail("walk: no note")
                for n, p in zip(ns, ps): n["p"] = p
                for n_ in ns:
                    if n_["syl"] - len(sy) in PIN.get((sec, i), {}) or n_["syl"] == HOLDP.get((sec, i)) or (sec, i) in COPYON: n_["pin"] = True
                if need_end and not end_ok(sec, i, ns[-1]["p"]): end_rule(sec, i, ns, notes_on_all, lo, hi); meta["moved"] += 1
                place_outside(rng, ns, notes_on_all, meta)                                       # 349
                if need_end:                                                                   # 324: a tonic ending, against its register's centre
                    tc = [p for p in range(lo, hi + 1) if p % 12 in M.SCALE and end_ok(sec, i, p)]
                    if tc and all((p - M.TONIC) % 12 == 0 for p in tc):
                        meta["tonic_endings"].append(dict(line=f"{sec}:{i}", centre=mu, nearest=min(tc, key=lambda p: (abs(p - mu), p)), drawn=ns[-1]["p"]))
                meta["kinds"][(sec, i)] = "fresh" if not upit else "fresh (361 unit return)"
                if upit: STATS["361: lines drawn on a returning unit"] += 1
            if ns[0]["on"] - last_on < GAP_MIN: globals().__setitem__("WHERE", (sec, i)); return _fail("join: no held end and breath before the line (212)")
            if last_max is not None and ns[-1]["on"] - U > last_max and nxt is not None:      # 327: the copy fitted again to enter after its downbeat
                if refit_327(*nxt):
                    pf = pending[nxt]; f0 = (pf[1][0]["on"] - line_start(*nxt)) if pf[0] == "ns" else pf[1][0]
                    last_max = (line_start(*nxt) + f0 - U) - GAP_MIN
                    STATS["327: copy fitted again after its downbeat" + ("" if ns[-1]["on"] - U <= last_max else ", join still short")] += 1
            if last_max is not None and ns[-1]["on"] - U > last_max: globals().__setitem__("WHERE", (sec, i, h)); return _fail("join: no held end and breath before the copy (212)")
            for n in ns: notes_on_all.add(n["on"]); SEC_USED.add(n["p"])
            place(sec, i, ns)
    notes = sorted([n for l in lines for n in l], key=lambda n: n["on"])
    on = {n["on"] for n in notes}
    built_ret = {f"{sec}:{i}" for sec, i, s0, i0, kd in meta["returns"] if kd != "sung again"}
    for n in notes:
        n.setdefault("dur", 12)
        if M.chord_for(n, on) == "E" and n["p"] % 12 == 7: n["p"] += 1; STATS["the bridge's E: a sung G raised to G-sharp"] += 1   # finding 375
        if n["line"] in built_ret or n.get("pass358") or n.get("pin"): continue                            # 287: a built return is left alone (the limits read it); 358: a passing note stays
        ch_ = M.chord_for(n, on)
        if n["p"] % 12 in OUT_PCS and M.clash(n["p"], ch_):
            tones = M.CH[ch_][1]; n["p"] = min((n["p"] - 1, n["p"] + 1), key=lambda q_: (q_ % 12 not in tones, q_ % 12 not in M.SCALE))
        if tri(n["p"], ch_):                                                                # 215: a copied note moves a step to a chord tone
            tones = M.CH[ch_][1]; n["p"] = min((n["p"] + 1, n["p"] - 1, n["p"] + 2, n["p"] - 2), key=lambda q_: (q_ % 12 not in tones, abs(q_ - n["p"])))
    finish(notes, rng)
    return dict(notes=notes, meta=meta), None

# ---- the discriminator (v96 feats on 8-bar windows) ----
MAJ = {0, 2, 4, 5, 7, 9, 11}
_P37 = open("/home/claude/p37/melody_p37.py").read()
exec(_P37[_P37.index("def feats(N, ton):"):_P37.index("def windows(notes, which=None):")], globals())
def windows(notes, which=None):
    out = []
    for s in SUNG:
        if KIND[s] not in ("Verse", "Chorus") or (which and s not in which): continue
        for k in range(0, SECLEN[s] - 7, 8): out.append((s, BAR0[s] + k))
    return out
def win_N(notes, b0):
    return [((n["on"] - b0 * BAR) / BEAT, n["dur"] / BEAT, n["p"], M.CH[M.chord_at(n["on"])][1]) for n in notes if b0 * BAR <= n["on"] < (b0 + 8) * BAR]
def win_feats(notes, b0): return feats(win_N(notes, b0), mton())                       # 353: a minor song on its own tonic
def win_distance(f):
    ds = []
    for k, v in DM.items():
        if not v["agree"] or f is None or k not in f or not np.isfinite(f[k]): continue
        c = v["centre_reference"]; ds.append(min(3.0, max(0.0, c["q25"] - f[k], f[k] - c["q75"]) / c["width"]))
    return float(np.mean(ds)) if ds else float("nan")
def outside_both(f):
    out = []
    for k, v in DM.items():
        x = f.get(k, np.nan) if f else np.nan
        if not np.isfinite(x): continue
        c, g = v["chart"], v["grid"]
        if (x < c[1] or x > c[3]) and (x < g[1] or x > g[3]): out.append((k, round(x, 3), "low" if x < c[1] else "high"))
    return out
def judge(notes):
    """252-254: the mean over Verse 1's and Chorus 1's windows (8 bars from the section's first bar)."""
    rows = {}
    for s in ("Verse 1", "Chorus 1"):
        N = win_N(notes, BAR0[s]); f = feats(N, mton()); rows[s] = dict(J.score_window(f, N), feats=f)
    return dict(combined=float(np.mean([r["combined"] for r in rows.values()])), content=float(np.mean([r["content"] for r in rows.values()])),
                order=float(np.mean([r["order"] for r in rows.values()])), rows=rows)
ERA_K = ["notes_per_bar", "range", "repeat", "distinct_durations", "pitch_bits"]
def era_read(notes):
    W = [win_feats(notes, BAR0[s]) for s in ("Verse 1", "Chorus 1", "Bridge")]
    return {k: float(np.median([w[k] for w in W if w])) for k in ERA_K}, W

# ---- gates (v107) ----
def top(notes, s): return max(n["p"] for n in notes if n["sec"] == s)
def low(notes, s): return min(n["p"] for n in notes if n["sec"] == s)
def med(notes, s): return float(np.median([n["p"] for n in notes if n["sec"] == s]))
SOFT, HARD, DIRN = GL["soft limits (kept 5th or 95th percentile)"], GL["hard limits (kept 1st or 99th percentile)"], GL["direction"]
LIMITS = list(SOFT)
def limit_readings(notes):
    """276: the eight readings on the whole song's sung notes (Table DL)."""
    on = {n["on"] for n in notes}; iv = [b2["p"] - a2["p"] for a2, b2 in zip(notes, notes[1:])]
    r = dict(tritone_leap_share=sum(abs(x) == 6 for x in iv) / max(1, len(iv)), past_octave_share=sum(abs(x) > 12 for x in iv) / max(1, len(iv)))
    run = 1; worst = 1
    for a2, b2 in zip(notes, notes[1:]):
        run = run + 1 if a2["p"] == b2["p"] and a2["line"] == b2["line"] else 1; worst = max(worst, run)
    r["run_max"] = worst
    bh = [n for n in notes if n["on"] % BEAT == 0 or n["dur"] >= 12]
    r["tritone_from_root_share"] = sum(tri(n["p"], M.chord_for(n, on)) for n in bh) / max(1, len(bh))
    r["max_lengths_8_bars"] = max(len({n["dur"] for n in notes if b0 * BAR <= n["on"] < (b0 + 8) * BAR}) for b0 in range(NBARS - 7))
    r["chorus_top_minus_verse"] = top(notes, "Chorus 1") - top(notes, "Verse 1")
    r["chorus_median_minus_verse"] = med(notes, "Chorus 1") - med(notes, "Verse 1")
    r["chorus_floor_minus_verse"] = low(notes, "Chorus 1") - low(notes, "Verse 1")
    return r
def limit_breaks(r):
    soft, hard = [], []
    for k in LIMITS:
        v = r[k]
        if k == "run_max": s_, h_ = v >= 10, v >= 15                                       # the writer's reading of 270 under 276: soft at 10, hard at 15
        elif DIRN[k] == "at most": s_, h_ = v > SOFT[k] + 1e-9, v > HARD[k] + 1e-9
        else: s_, h_ = v < SOFT[k] - 1e-9, v < HARD[k] - 1e-9
        if h_: hard.append(k)
        elif s_: soft.append(k)
    return soft, hard
NEAR_LEVEL = 2                                                                         # 267: the session's number, uncounted
def return_267(c):
    """267: a return built by 239 is related when the first three-quarters of its shared events keep their pitches, or both near-level."""
    out = []; notes = c["notes"]
    for sec, i, s0, i0, kind in c["meta"]["returns"]:
        if kind == "sung again": continue
        a2, b2, U = line_span(notes, sec, i); a0, b0, U0 = line_span(notes, s0, i0)
        R = {n["on"] - U: n["p"] for n in notes if a2 <= n["on"] < b2}; S_ = {n["on"] - U0: n["p"] for n in notes if a0 <= n["on"] < b0}
        sh = sorted(set(R) & set(S_))
        if not sh: out.append(((sec, i, s0, i0, kind), False, "no shared events")); continue
        q4 = 0.75 * max(R)                                                             # read on the quarter 239 builds: the last quarter of the line's span
        keep = all(R[t] == S_[t] for t in sh if t < q4)
        lvl = (max(R[t] for t in sh) - min(R[t] for t in sh) <= NEAR_LEVEL) and (max(S_[t] for t in sh) - min(S_[t] for t in sh) <= NEAR_LEVEL)
        out.append(((sec, i, s0, i0, kind), keep or lvl, "kept" if keep else "near-level" if lvl else "changed early"))
    return out
# ---- 286: the seven unaudited gates join 277's count as soft limits, hard at the 1st or 99th ----
SPEC = SR["spectral reading (the engine's beta_pitch on Verse 1 then the first 8 bars of Chorus 1)"]
LIM7 = {"spectral": ("between", SPEC["soft limits (kept 5th, 95th)"], SPEC["hard limits (kept 1st, 99th)"]),
        "cmp": ("at least", L286["cmp"]["soft"], L286["cmp"]["hard"]), "memory": ("at least", L286["memory"]["soft"], L286["memory"]["hard"]),
        "surprisal": ("at least", L286["surprisal"]["soft"], L286["surprisal"]["hard"]),
        "rhythm band": ("between", L286["rhythm band"]["soft"], L286["rhythm band"]["hard"]), "sequence legs": ("at most", L286["sequence legs"]["soft"], L286["sequence legs"]["hard"])}
def table_b(notes):
    """the five Table B readings, as v1 reads them (Verse 1 then the first 8 bars of Chorus 1); all always read (286)."""
    V = M.sec_notes(notes, "Verse 1"); H = [n for n in M.sec_notes(notes, "Chorus 1") if n["on"] < (BAR0["Chorus 1"] + 8) * BAR]
    off = V[0]["on"]; tune = M.quarters(V, off) + M.quarters(H, off)
    beta = beta_pitch(tune); cmp_, _ = cmp_score(tune, 4, M.TONIC)
    hq = M.quarters(H, H[0]["on"]); vq = M.quarters(V, V[0]["on"]); mh, _, _ = m_horizon(hq, vq)
    bits = M.PPMM.bits(PPM.symbols(tune, M.TONIC))[len(V):]; hp = [n["p"] for n in H]
    ic, _ = ic_profile(bits, hp.index(max(hp)))
    fv = (feature_vec(hq, M.TONIC, 4) - M.MU) / M.SD
    dist = np.sort(np.sqrt(((M.ZREF - fv) ** 2).sum(1)))[:10].mean(); real = sum(1 for x in M.REAL_KNN if x >= dist) / len(M.REAL_KNN)
    return dict(spectral=beta, cmp=cmp_, memory=mh, surprisal=ic, realness=real, H=H, V=V)
def limit7_readings(notes):
    tb = table_b(notes); r = {k: tb[k] for k in ("spectral", "cmp", "memory", "surprisal", "realness")}
    r["rhythm band"] = M.rhythm_bits(notes); r["sequence legs"] = max(M.sequences(notes) or [1])
    return r, tb
def limit7_breaks(r):
    soft, hard = [], []
    for k, (d, sl, hl) in LIM7.items():                                                # 300: realness is read and printed, not counted
        v = r[k]
        if v is None: hard.append(k); continue
        if d == "between": s_, h_ = not (sl[0] <= v <= sl[1]), not (hl[0] <= v <= hl[1])
        elif d == "at least": s_, h_ = v < sl - 1e-9, v < hl - 1e-9
        else: s_, h_ = v > sl + 1e-9, v > hl + 1e-9
        if h_: hard.append(k)
        elif s_: soft.append(k)
    return soft, hard
GATES = ["limits: a hard limit or three soft breaks (276/277, with 286's seven)", "returns related (267)", "chorus opening another tune (227; 279)",
         "bridge opening unrelated (208; 279)", "pushed notes (159; 279)", "density (159; 279)", "key word on a chord tone (134; 279)", "the judge's floor (254; 279)"]
DESIGN_GATES = ["design: 'thought' held on G or D, 'morning' held on it in the last chorus; 'before it's done' D C B A (choruses), C B A G (last chorus); the tag on A; the chorus over the verse (Q14 A, Q15 A)"]
FIXR = {("Chorus 1", 0): {0: 0, 1: 12, 2: 24, 3: 54, 4: 60, 5: 72, 6: 84},             # 'HOLD that THOUGHT (held), I'm STILL COM-ing'
        ("Last Chorus", 0): {0: 12, 1: 24, 2: 54, 3: 60, 4: 66, 5: 72, 6: 78, 7: 84}}   # 'It's MOR (held) -ning, and I HELD the THOUGHT': the held note where 'thought' was
assert len(LINES["Last Chorus"][0]) == 8, LINES["Last Chorus"][0]
COPYON = {("Last Chorus", 0): ("Chorus 1", 0)}                                        # its notes on the chorus's onsets take the chorus's pitches
assert len(LINES["Chorus 1"][0]) == 7, LINES["Chorus 1"][0]
HOLDP = {("Chorus 1", 0): 2}                                                         # 'thought' on G or D
PIN = {("Chorus 1", 3): {-4: 62, -3: 60, -2: 59, -1: 57}, ("Last Chorus", 3): {-4: 60, -3: 59, -2: 57, -1: 55}, ("Tag", 1): {-1: 57}}
DCOUNT = collections.Counter()
def design_fails(c):
    """317: the writer's design, read on what is sung; outside 275, its pass rate printed."""
    notes = c["notes"]; f = {}; g = DESIGN_GATES[0]
    by = collections.defaultdict(list)
    for n in notes:
        if not n.get("slur"): by[n["line"]].append(n)
    c0, c3, l0, l3, t1 = (by.get(k, []) for k in ("Chorus 1:0", "Chorus 1:3", "Last Chorus:0", "Last Chorus:3", "Tag:1"))
    if not (len(c0) == 7 and len(c3) >= 4 and len(l0) == 8 and len(l3) >= 4 and t1): f[g] = "missing"; return f
    hold = c0[2]["p"] % 12 in (7, 2) and c0[3]["on"] - c0[2]["on"] >= 30 and l0[1]["p"] == c0[2]["p"] and l0[2]["on"] - l0[1]["on"] >= 30
    done = [n["p"] for n in c3[-4:]] == [62, 60, 59, 57] and [n["p"] for n in l3[-4:]] == [60, 59, 57, 55] and t1[-1]["p"] == 57
    vp = [n["p"] for n in notes if n["sec"] == "Verse 1"]; cp = [n["p"] for n in notes if n["sec"] == "Chorus 1"]
    lift = float(np.median(cp)) - float(np.median(vp)) >= 3 and max(cp) > max(vp)
    if not (hold and done and lift): f[g] = dict(hold=hold, done=done, lift=lift)
    DCOUNT["read"] += 1
    for k_, v_ in dict(hold=hold, done=done, lift=lift).items():
        if not v_: DCOUNT[k_] += 1
    if not (hold and done and lift): DCOUNT["any"] += 1
    return f
def design_reg(R_, info):
    """325: the designed notes (G3-D4) inside the chorus's drawn register; the chorus over the verse."""
    vm, vh, vl = R_["Verse"]; cm, ch, cl = R_["Chorus"]
    return cl <= 55 and ch >= 62 and cm - vm >= 3 and ch - vh >= 3
DESIGN_REG.append(("the designed notes inside the chorus register; the chorus over the verse (Q14 A, Q15 A)", design_reg))
CARRY_LOW = [s_ for s_ in SUNG if KIND[s_] in ("Verse", "Bridge") and s_ in ("Verse 1", "Bridge")]     # 329: the first verse or the bridge
CARRY_HIGH = [s_ for s_ in SUNG if s_ in ("Chorus 1", "Bridge")]                                  # 329: the first chorus or the bridge
# 278 (with 288): the aims carry the kept bands
KB = {k: (REG[k][2], REG[k][4]) for k in REG}
AIMS_278 = ["chorus median over the verse's inside the kept middle half (0 to 3)", "chorus top over the verse's inside the kept middle half (-1 to 3)",
            "chorus lowest over the verse's inside the kept middle half (0 to 4)", "bridge median over the verse's inside the kept middle half (0 to 5)",
            "chorus top at or above the verse's", "chorus median not below", "chorus lowest note above", "bridge median above the verse's",
            "bridge top under the song's", "returns keep their first note", "returns keep their top note or higher", "no tritone leap", "no note a tritone from the root"]
def aims_278(c):
    notes = c["notes"]; on = {n["on"] for n in notes}; ret = []
    for sec, i, s0, i0, kind in c["meta"]["returns"]:
        if kind == "sung again": continue
        R = [n for n in notes if n["line"] == f"{sec}:{i}"]; S_ = [n for n in notes if n["line"] == f"{s0}:{i0}"]
        ret.append((R[0]["p"] == S_[0]["p"], max(n["p"] for n in R) >= max(n["p"] for n in S_)))
    iv = [b2["p"] - a2["p"] for a2, b2 in zip(notes, notes[1:])]
    cm, ct, cf, bm = med(notes, "Chorus 1") - med(notes, "Verse 1"), top(notes, "Chorus 1") - top(notes, "Verse 1"), low(notes, "Chorus 1") - low(notes, "Verse 1"), med(notes, "Bridge") - med(notes, "Verse 1")
    return {AIMS_278[0]: KB["chorus_median_minus_verse"][0] <= cm <= KB["chorus_median_minus_verse"][1], AIMS_278[1]: KB["chorus_top_minus_verse"][0] <= ct <= KB["chorus_top_minus_verse"][1],
            AIMS_278[2]: KB["chorus_floor_minus_verse"][0] <= cf <= KB["chorus_floor_minus_verse"][1], AIMS_278[3]: KB["bridge_median_minus_verse"][0] <= bm <= KB["bridge_median_minus_verse"][1],
            AIMS_278[4]: ct >= 0, AIMS_278[5]: cm >= 0, AIMS_278[6]: cf > 0, AIMS_278[7]: bm > 0,
            AIMS_278[8]: top(notes, "Bridge") < max(n["p"] for n in notes), AIMS_278[9]: float(np.mean([x[0] for x in ret])) if ret else None,
            AIMS_278[10]: float(np.mean([x[1] for x in ret])) if ret else None, AIMS_278[11]: not any(abs(x) == 6 for x in iv),
            AIMS_278[12]: not any(tri(n["p"], M.chord_for(n, on)) and (n["on"] % BEAT == 0 or n["dur"] >= 12) for n in notes)}
def gate_fails(c, jd=None):
    notes = c["notes"]; f = {}; info = {}
    if M.pushed_share(notes) > 0.42: f["pushed notes (159; 279)"] = 1
    de = len(notes) / sum(SECLEN[s] * 4 * 60 / M.QBPM for s in SUNG)
    if not (1.1 <= de <= 4.9): f["density (159; 279)"] = de
    if M.keyword_chord(notes)[0] < 0.40: f["key word on a chord tone (134; 279)"] = 1
    lr = limit_readings(notes); soft, hard = limit_breaks(lr)
    l7, tb = limit7_readings(notes); s7, h7 = limit7_breaks(l7)
    info["limits"] = lr; info["limits7"] = l7; info["soft"] = soft + s7; info["hard"] = hard + h7; info["tb"] = {k: tb[k] for k in ("spectral", "cmp", "memory", "surprisal", "realness")}
    if info["hard"] or len(info["soft"]) >= 3: f["limits: a hard limit or three soft breaks (276/277, with 286's seven)"] = (info["hard"], info["soft"])
    rr = return_267(c); info["returns"] = rr
    if any(not x[1] for x in rr): f["returns related (267)"] = next(x for x in rr if not x[1])[0]
    if opening_rel(notes, "Chorus 1", "Verse 1")[0]: f["chorus opening another tune (227; 279)"] = 1
    if opening_rel(notes, "Bridge", "Verse 1")[0] or opening_rel(notes, "Bridge", "Chorus 1")[0]: f["bridge opening unrelated (208; 279)"] = 1
    jd = jd or judge(notes)
    if jd["combined"] < J.FLOOR: f["the judge's floor (254; 279)"] = round(jd["combined"], 3)
    info["lift"] = dict(median=med(notes, "Chorus 1") - med(notes, "Verse 1"), top=top(notes, "Chorus 1") - top(notes, "Verse 1"), lowest=low(notes, "Chorus 1") - low(notes, "Verse 1"),
                        bridge=med(notes, "Bridge") - med(notes, "Verse 1"))
    c["info"] = info
    return f
def composite(c, old_fit=False):
    """the composite, with 296's fit term (no mark for the lift); old_fit=True gives the term as it was, for the report."""
    tb = c["info"]["tb"]; C = M.C; notes = c["notes"]
    V = M.sec_notes(notes, "Verse 1"); H = [n for n in M.sec_notes(notes, "Chorus 1") if n["on"] < (BAR0["Chorus 1"] + 8) * BAR]; hp = [n["p"] for n in H]
    beta, cmp_, mh, ic, real = (tb[k] for k in ("spectral", "cmp", "memory", "surprisal", "realness"))
    S_sp = s_spectral(beta, C["beta"]["p25"], C["beta"]["p75"]) if beta is not None else 0.0; vps = [n["p"] for n in V]; lift = float(np.median(hp) - np.median(vps))
    terms = [M.contour(hp) in ("arch", "ascending", "wave", "descending"), M.contour(vps) in ("flat", "wave"), max(vps) <= c["meta"]["registers"].get("v_cap", V_CAP)]
    if old_fit: terms.insert(1, 1.0 if lift >= 4 else (0.5 if lift >= 2 else 0.0))
    fit = float(np.mean(terms))
    comp = 0.15 * S_sp + 0.15 * min(1.0, cmp_ / C["cmp"]["p75"]) + 0.10 * min(1, mh) + 0.15 * fit + 0.15 * ic + 0.25 * min(1.0, real / C["realness"]["p50"]) + 0.05 * 0.5
    return round(comp, 4), fit, lift
def evaluate(c):
    notes = c["notes"]; ps = [n["p"] for n in notes]
    if min(ps) < M.LO or max(ps) > TOP: return ("range (the voice row)", (min(ps), max(ps))), None
    f = gate_fails(c, c.get("judge")); f.update(design_fails(c))
    for g in DESIGN_GATES + GATES:
        if g in f: return (g, f[g]), None
    comp, fit, lift = composite(c); comp_old, fit_old, _ = composite(c, old_fit=True); tb = c["info"]["tb"]
    return None, dict(composite=comp, composite_old_fit=comp_old, pitch_bits=round(M.pitch_bits(ps), 3), rhythm_bits=round(M.rhythm_bits(notes), 3), IC=tb["surprisal"],
                      CMP=tb["cmp"], M_horizon=tb["memory"], realness=tb["realness"], fit=fit, fit_old=fit_old, lift=lift)

# ---- the line readings of Table DJ (27.48), with the v104 file's own contour code ----
from scipy.fft import dct
PM_ = np.array(LIT["pitch model: rows are the scale degree left (0-11 above the tonic), columns the interval -24..+24, probabilities"])
def _contour(ps, ds):
    e = np.cumsum(ds); x = np.linspace(0, e[-1], 31)[:-1] + e[-1] / 60; y = np.array([ps[min(np.searchsorted(e, v, side="right"), len(ps) - 1)] for v in x], float)
    th = [y[:10].mean(), y[10:20].mean(), y[20:].mean()]; cc = dct(y, type=2, norm="ortho")
    s1 = np.sign(round(th[1] - th[0], 6)) if abs(th[1] - th[0]) > 0.5 else 0; s2 = np.sign(round(th[2] - th[1], 6)) if abs(th[2] - th[1]) > 0.5 else 0
    kind = {(1, -1): "arch", (-1, 1): "valley", (1, 1): "rising", (-1, -1): "falling", (0, 0): "level", (1, 0): "rising then level", (0, 1): "level then rising", (-1, 0): "falling then level", (0, -1): "level then falling"}[(s1, s2)]
    return kind, float(cc[1]), float(-cc[2])
def _ic(p, prev):
    if prev is None: return np.nan
    iv = int(np.clip(p - prev, -24, 24)); return float(-np.log2(max(1e-6, PM_[(prev - M.TONIC) % 12][iv + 24])))
AF = ("arch", "falling", "falling then level", "level then falling")
def line_readings(notes):
    """Table DJ on a build: one line per lyric line (the engine's own lines, not found by rule); shares and medians across its lines."""
    by = collections.OrderedDict()
    for n in notes: by.setdefault(n["line"], []).append(n)
    Ls = [l for l in by.values() if len(l) >= 3]; rows = []; prev_last = None; first_ic, other_ic, joins = [], [], []
    for L_ in Ls:
        ps = [n["p"] for n in L_]; ds = [n["dur"] / BEAT for n in L_]; t0 = L_[0]["on"] / BEAT; tl = L_[-1]["on"] / BEAT
        kind, fall, arch = _contour(ps, ds); iv = np.abs(np.diff(ps)); q = max(1, len(iv) // 5)
        ic = [_ic(L_[0]["p"], prev_last)] + [_ic(ps[k], ps[k - 1]) for k in range(1, len(ps))]
        if prev_last is not None: first_ic.append(ic[0]); joins.append(abs(ps[0] - prev_last))
        other_ic += ic[1:]
        span = max(ps) - min(ps)
        rows.append(dict(kind=kind, arch=arch, arch_span=(arch / span if span > 0 else 0.0), fall=fall, widen=float(iv[-q:].mean() - iv[:q].mean()), peak_first_third=float(np.argmax(ps) / (len(ps) - 1) < 1 / 3),
                         end_minus_mean=float(ps[-1] - np.mean(ps)), last_over_mean=float(ds[-1] / np.mean(ds)), last_longest=float(ds[-1] >= max(ds)),
                         on=float(t0 % 4 < 0.5), after=float(0.5 <= t0 % 4 < 3.0), pickup=float(t0 % 4 >= 3.0), end_down=float(tl % 4 < 0.26 or tl % 4 >= 3.74),
                         sec=L_[0]["sec"], line=L_[0]["line"]))
        prev_last = ps[-1]
    m = lambda k: float(np.mean([r[k] for r in rows])); md = lambda k: float(np.median([r[k] for r in rows]))
    kinds = collections.Counter(r["kind"] for r in rows)
    return dict(lines=len(rows), arch_or_falling=float(np.mean([r["kind"] in AF for r in rows])), valley=float(np.mean([r["kind"] == "valley" for r in rows])),
                arch_positive=float(np.mean([r["arch"] > 0 for r in rows])), arch_term=md("arch"), arch_span=md("arch_span"), falling_term=md("fall"), peak_first_third=m("peak_first_third"),
                end_minus_mean=md("end_minus_mean"), last_over_mean=md("last_over_mean"), last_longest=m("last_longest"), widening=m("widen"),
                first_note_extra_bits=float(np.nanmean(first_ic) - np.nanmean(other_ic)) if first_ic else float("nan"),
                join_fourth=float(np.mean([j >= 5 for j in joins])) if joins else float("nan"), join_mean=float(np.mean(joins)) if joins else float("nan"),
                starts_on_downbeat=m("on"), starts_after_downbeat=m("after"), starts_as_pickup=m("pickup"), ends_on_downbeat=m("end_down"),
                kinds={k: round(v / len(rows), 3) for k, v in kinds.items()}, rows=rows)

# ---- readings for each build ----
def reading(c):
    notes = c["notes"]; Wv = win_feats(notes, BAR0["Verse 1"]); Wc = win_feats(notes, BAR0["Chorus 1"])
    er, _ = era_read(notes); r = dict(v=Wv, c=Wc, era=er, ax_v=axes_of(Wv), ax_c=axes_of(Wc), ax_b=axes_of(win_feats(notes, BAR0["Bridge"])),
                                      dist=float(np.mean([win_distance(Wv), win_distance(Wc)])), outside=len(outside_both(Wv)) / 2 + len(outside_both(Wc)) / 2)
    return r

ARCH_SPAN = 0.23                                                                       # 305: kept median of the arch term over the line's span
ARCH_BAND = (0.0, 0.55); AMP_CAP = 7.0; LEAP_75 = 0.036                                # 312/315: the kept middle half; the cap; the kept 75th percentile
CAL_STOP = []; FROZEN = set(); CAL_ROUNDS = [0]
OFF = set(filter(None, os.environ.get("ZE_OFF", "").split(",")))                       # diagnostics only: a fix switched off for a side run (never in a run of record)
def calibrate(rng, n=30, rounds=6):                                                    # 357: up to six rounds
    """249: the knobs are set on this song so that a build aimed at its pool's medians reads near them."""
    log = []; lines_acc = []; big_prev = set(); pf_acc = []; v2_acc = []
    pairs = {"repeat": "repeat", "step": "step", "third": "third", "fourth_fifth": "fourth_fifth", "larger": "past_fifth", "ct_on": "chord_tones_on_beat",
             "ct_off": "chord_tones_off_beat", "on_tonic": "on_tonic", "on_third": "on_third", "on_fifth": "on_fifth", "turn": "turns_per_move",
             "beat3": "on_beat3", "beats24": "on_beats_2_4", "gap8": "gap_eighth", "gap4": "gap_quarter", "gap16": "gap_sixteenth"}
    full_prev = {"s16", "g8", "g4", "glong", "run", "on16"}
    for rd in range(rounds):
        if rd >= 3 and not full_prev:                                                     # 357: past three rounds only while a knob still moves at full step
            CAL_ROUNDS[0] = rd; break
        CAL_ROUNDS[0] = rd + 1; full_now = set()
        acc = {"V": collections.defaultdict(list), "C": collections.defaultdict(list)}; k = 0; tries = 0
        while k < n and tries < 40 * n:
            tries += 1; c, err = generate(rng, cal=True)
            if err: continue
            k += 1
            if NEW: lines_acc.append(line_readings(c["notes"]))
            for s_ in ("Verse 1", "Chorus 1"):
                f_ = win_feats(c["notes"], BAR0[s_])
                if f_ and np.isfinite(f_.get("past_fifth", np.nan)): pf_acc.append(f_["past_fifth"])
            for p, s in (("V", "Verse 1"), ("C", "Chorus 1")):                                 # no designed notes in the chorus: its own window
                f = win_feats(c["notes"], BAR0[s])
                for kn, m in pairs.items():
                    if f and np.isfinite(f.get(m, np.nan)): acc[p][kn].append(f[m])
        row = {}
        k2 = 0; t2 = 0; ua = collections.defaultdict(list)                                  # 338: builds drawn as the run draws them
        while k2 < n and t2 < 40 * n:
            t2 += 1; c2, e2 = generate(rng)
            if e2: continue
            k2 += 1
            if "Verse 2" in SUNG: v2_acc.append(v2_share(c2["notes"]))
            n6, r6, p6 = s16_shape(c2["notes"]); ua["_n6"].append(n6); ua["_r6"].append(r6)            # 355
            ua["_bits"].append(M.rhythm_bits(c2["notes"]))                                                 # 356
            for s_ in ("Verse 1", "Chorus 1"):
                f_ = win_feats(c2["notes"], BAR0[s_])
                for m_ in list(KEPT114) + list(GAPS) + ["notes_per_bar", "on_sixteenth", "distinct_durations"]:
                    if f_ and np.isfinite(f_.get(m_, np.nan)): ua[m_].append(f_[m_])
        row["338: unaimed builds read"] = k2
        if ua:                                                                              # 341, 344-346: each knob toward its kept figure
            rd = {m_: (float(np.mean(ua[m_])) if ua.get(m_) else KEPT114[m_]) for m_ in KEPT114}
            tg = du_target(float(np.mean(ua["notes_per_bar"])))                              # 354: the four gaps toward the kept means for the density
            on16 = float(np.mean(ua["on_sixteenth"])) if ua.get("on_sixteenth") else KEPT355["on_sixteenth"]
            dd = float(np.median(ua["distinct_durations"])) if ua.get("distinct_durations") else 4.0; bits = float(np.median(ua["_bits"]))
            out356 = [m_ for m_, v_ in (("distinct_durations", dd), ("rhythm_bits", bits)) if not (MID356[m_][0] <= v_ <= MID356[m_][1])]
            if out356 and not STOP356 and "354" not in OFF:                                    # 356: the 354 knobs stop when either reading leaves the kept middle half
                STOP356.append(f"round {CAL_ROUNDS[0]}: {out356} outside the kept middle half (distinct lengths {dd}, rhythm bits {round(bits, 3)}); the 354 knobs stop at "
                               f"{[round(LK[k_], 3) for k_ in ('s16', 'g8', 'g4', 'glong')]}"); print(STOP356[-1])
            for kn_, m_, t_ in zip(("s16", "g8", "g4", "glong"), GAPS, tg):
                if STOP356 or "354" in OFF: break
                r_ = float(np.mean(ua[m_])) if ua.get(m_) else t_
                f_ = float(np.clip(max(0.01, t_) / max(0.01, r_), 0.6, 1.6))
                if kn_ == "s16" and f_ > 1.0 and on16 > KEPT355["on_sixteenth"]: f_ = 1.0         # 357: s16 aimed with the onsets on a sixteenth
                if f_ in (0.6, 1.6): full_now.add(kn_)
                LK[kn_] = float(np.clip(LK[kn_] * f_, 0.05, 5.0))
            if "348" not in OFF:                                                             # 355: the run knob and the sixteenth-onset knob
                ir = sum(ua["_r6"]) / max(1, sum(ua["_n6"]))
                f_ = float(np.clip((KEPT355["in_runs"] / max(0.02, ir)) ** 4, 0.1, 10.0)); LK["run"] = float(np.clip(LK["run"] * f_, 1e-7, 5.0))   # on a log scale: the run weight acts across a line's many paths
                if f_ in (0.1, 10.0): full_now.add("run")
                f_ = float(np.clip(KEPT355["on_sixteenth"] / max(0.01, on16), 0.6, 1.6)); LK["on16"] = float(np.clip(LK["on16"] * f_, 0.05, 5.0))
                if f_ in (0.6, 1.6): full_now.add("on16")
                row["355 (kept, unaimed reading, knob)"] = dict(in_runs=(0.31, round(ir, 3), round(LK["run"], 3)), on_sixteenth=(0.094, round(on16, 3), round(LK["on16"], 3)))
            row["356 (middle half, unaimed reading)"] = dict(distinct_durations=(MID356["distinct_durations"], dd), rhythm_bits=(tuple(round(x, 3) for x in MID356["rhythm_bits"]), round(bits, 3)))
            row["354 (band target, unaimed reading, knob)"] = {m_: (t_, round(float(np.mean(ua[m_])), 3) if ua.get(m_) else None, round(LK[k_], 3)) for k_, m_, t_ in zip(("s16", "g8", "g4", "glong"), GAPS, tg)}
            LK["ctl"] = float(np.clip(LK["ctl"] * np.clip((KEPT114["chord_tones_on_long_notes"] / max(0.05, rd["chord_tones_on_long_notes"])) ** 2, 0.6, 2.0), 0.5, 8.0))
            LK["offb"] = float(np.clip(LK["offb"] * np.clip(KEPT114["on_offbeat_eighth"] / max(0.05, rd["on_offbeat_eighth"]), 0.6, 1.6), 0.3, 3.0))
            LK["dpk"] = float(np.clip(LK["dpk"] * np.clip((rd["distinct_pitches"] / KEPT114["distinct_pitches"]) ** 2, 0.6, 2.0), 0.5, 8.0))
            LK["k44"] = float(np.clip(LK["k44"] * np.clip(KEPT114["outside_scale"] / max(0.005, rd["outside_scale"]), 0.5, 2.0), 0.01, 30.0))
            row["341-346 (kept, unaimed reading, knob)"] = {m_: (KEPT114[m_], round(rd[m_], 3)) for m_ in KEPT114} | {"knobs": {k_: round(LK[k_], 3) for k_ in ("s16", "ctl", "offb", "dpk", "k44")}}
        if v2_acc:                                                                          # 331: the rate moved toward the kept median share
            sh = float(np.median(v2_acc)); RATE293[0] = float(np.clip(RATE293[0] + (V2_KEPT - sh), 0.05, 1.0))
            row["293 rate"] = (V2_KEPT, round(sh, 3), round(RATE293[0], 3)); v2_acc.clear()
        if NEW and lines_acc:
            keep = {k_: LK[k_] for k_ in FROZEN}
            arch = float(np.mean([x["arch_span" if "305" not in OFF else "arch_term"] for x in lines_acc])); wid = float(np.mean([x["widening"] for x in lines_acc])); fr = float(np.nanmean([x["first_note_extra_bits"] for x in lines_acc]))
            big = set(); pf = float(np.median(pf_acc)) if pf_acc else 0.0
            if arch < ARCH_BAND[0] and pf <= LEAP_75: m_ = float(np.clip(ARCH_SPAN / max(0.02, arch) if arch > 0 else 1.6, 0.6, 1.6))   # 312: raised only while leaps are in range
            elif arch > ARCH_BAND[1] or pf > LEAP_75: m_ = float(np.clip(ARCH_BAND[1] / max(0.02, arch), 0.6, 1.0)) if arch > ARCH_BAND[1] else 0.85
            else: m_ = 1.0                                                                   # 315: inside the kept middle half: no step
            if m_ in (0.6, 1.6): big.add("amp")
            LK["amp"] = float(np.clip(LK["amp"] * m_, 1.5, AMP_CAP))                          # 315: the cap of 7
            ml = float(np.clip(LEAP_75 / max(1e-3, pf), 0.5, 1.0)) if pf > LEAP_75 else 1.0
            if ml == 0.5: big.add("leap")
            LK["leap"] = float(np.clip(LK["leap"] * ml, 0.05, 1.0)); pf_acc.clear()
            LK["widen"] = float(np.clip(LK["widen"] + 2.0 * (0.326 - wid), -1.0, 5.0))
            mf = float(np.clip(1.338 / max(0.1, fr), 0.6, 1.6))
            if mf in (0.6, 1.6): big.add("fresh")
            LK["fresh"] = float(np.clip(LK["fresh"] * mf, 0.5, 6))
            row["lines"] = dict(arch_span=(ARCH_BAND, round(arch, 3), round(LK["amp"], 3)), past_fifth=(LEAP_75, round(pf, 3), round(LK["leap"], 3)),
                                widening=(0.326, round(wid, 3), round(LK["widen"], 3)), fresh=(1.338, round(fr, 3), round(LK["fresh"], 3)), largest_steps=sorted(big))
            LK.update(keep); big -= FROZEN                                                     # 332: a frozen knob stays where it was frozen
            row["lines"]["largest_steps"] = sorted(big)
            if big & big_prev:                                                                  # 315/332: the largest step two rounds running
                FROZEN.update(big & big_prev)
                CAL_STOP.append(f"round {CAL_ROUNDS[0]}: {sorted(big & big_prev)} took the largest step two rounds running and are frozen at {[round(LK[k_], 3) for k_ in sorted(big & big_prev)]}; the other knobs finish their rounds")
                print(CAL_STOP[-1])
            big_prev = big
            lines_acc.clear()
        for p in ("V", "C"):
            for kn, m in pairs.items():
                if NEW and kn == "beat3": continue                                            # 285
                if p == "C" and kn == "turn": continue                                         # 304
                rd_ = float(np.mean(acc[p][kn])) if acc[p][kn] else MED[p][m]; tg = MED[p][m]
                KNOBS[p][kn] = float(np.clip(KNOBS[p][kn] * (max(0.02, tg) / max(0.02, rd_)) ** 1.0, 0.02 if kn == "gap16" else 1 / 3, 3))   # held to a third..three times, so a reading the design forces cannot starve the walk
                row[f"{p}:{kn}"] = (round(tg, 3), round(rd_, 3), round(KNOBS[p][kn], 3))
        full_prev = full_now; row["357: knobs at full step"] = sorted(full_now)
        log.append(row)
    return log

if __name__ == "__main__":
    import time; T0 = time.time()
    N = _N; SEED = 20261110 + 445
    rng = random.Random(SEED)
    cal_log = calibrate(random.Random(SEED + 1))
    made, deaths, alive, allb = 0, collections.Counter(), [], []
    would = collections.Counter(); every = []
    STATS.clear()
    while made < N:
        c, err = generate(rng); made += 1
        for n in c["notes"]: n.setdefault("dur", 12)
        rec = dict(n=made, fp=M.fingerprint(c), notes=[(n["on"], n["dur"], n["p"], n["sec"], n["line"], n.get("stress"), n.get("syl")) for n in c["notes"]],
                   cause=err, partial=bool(c.get("partial")), soft=None, hard=None, judge=None, win=dict(c["meta"]["win"]), registers=c["meta"].get("registers"))
        every.append(rec)
        if err: deaths[err] += 1; continue
        c["judge"] = judge(c["notes"]); rec["judge"] = {k: c["judge"][k] for k in ("combined", "content", "order")}
        fails = gate_fails(c, c["judge"]); fails.update(design_fails(c)); info = c["info"]
        rec["soft"], rec["hard"], rec["limits"], rec["limits7"], rec["lift"] = info["soft"], info["hard"], info["limits"], info["limits7"], info["lift"]
        for g in fails: would[g] += 1
        for k in info["soft"] + info["hard"]: would["limit broken: " + k] += 1
        r = reading(c); c["read"] = r; c["lines"] = line_readings(c["notes"]); lr = {k: v for k, v in c["lines"].items() if k != "rows"}
        allb.append(dict(meta=c["meta"], read=r, judge=rec["judge"], fails=list(fails), info=info, lines=lr, aims=aims_278(c),
                         kinds=dict(c["meta"]["kinds"]), notes=rec["notes"], fp=rec["fp"]))
        cert, m = evaluate(c)
        if cert: deaths[cert[0]] += 1; rec["cause"] = cert[0]; allb[-1]["cause"] = cert[0]; continue
        allb[-1]["cause"] = None; allb[-1]["meas"] = m
        c["meas"] = m; c["fp"] = rec["fp"]; alive.append(c)
    alive.sort(key=lambda c: (-c["meas"]["composite"], c["fp"]))
    order = hashlib.sha1("".join(c["fp"] for c in alive).encode()).hexdigest()[:12]
    byj = sorted(alive, key=lambda c: (-c["judge"]["combined"], c["fp"])); short = byj[:max(1, len(byj) // 2)]       # 255
    sfp = {c["fp"] for c in short}; pick_255 = next(c for c in alive if c["fp"] in sfp) if alive else None
    clean = [c for c in byj if not c["info"]["soft"]]                                      # 362: the judge's first among survivors with no soft break
    pick = clean[0] if clean else (byj[0] if byj else None); pick_352 = byj[0] if byj else None
    print(f"362: survivors with no soft break {len(clean)} of {len(byj)}" + ("" if clean else "; none qualified: the pick is the judge's first"))
    old = sorted(alive, key=lambda c: (-c["meas"]["composite_old_fit"], c["fp"]))                                    # 296: the pick under the old fit term
    pick_old = next(c for c in old if c["fp"] in sfp) if alive else None
    print(f"[{VAR}{_TAG}] {NBARS} bars; built {made}, survivors {len(alive)} ({100 * len(alive) / max(1, made):.1f}%), order {order}, {time.time() - T0:.0f}s")
    for k, v in deaths.most_common(): print(f"   {v:5d}  {k}")
    print("would fail:"); [print(f"   {would[g]:5d}  {g}") for g in DESIGN_GATES + list(GATES) + sorted(k for k in would if k not in GATES and k not in DESIGN_GATES)]
    if alive:
        for lab, c in (("composite first", alive[0]), ("pick (362)", pick), ("judge's first", pick_352), ("255's pick", pick_255), ("pick, old fit", pick_old)):
            print(f"{lab:16s} {c['fp']} comp {c['meas']['composite']:.3f} judge {c['judge']['combined']:.3f} (content {c['judge']['content']:.3f}, order {c['judge']['order']:.3f})"
                  f" soft {c['info']['soft']} lift {c['info']['lift']}")
    code = hashlib.sha1(open(__file__, "rb").read() + open("/home/claude/p49/lyric_p45.py", "rb").read() + open(f"{HERE}/judges.py", "rb").read()
                        + open("/home/claude/p36/melody_p36.py", "rb").read()).hexdigest()[:12]
    rerun = dict(seed=SEED, calibration_seed=SEED + 1, N=N, mode=MODE, code_sha=code, pythonhashseed=os.environ.get("PYTHONHASHSEED"), python=platform.python_version(),
                 numpy=np.__version__, tables={f: hashlib.sha256(open(f"{HERE}/tables/{f}", "rb").read()).hexdigest()[:16] for f in sorted(os.listdir(f"{HERE}/tables"))},
                 limits286=hashlib.sha256(open(f"{HERE}/limits286.json", "rb").read()).hexdigest()[:16],
                 cmd=f"PYTHONHASHSEED=0 python3 melody_p45.py {N} {MODE}", line_knobs=dict(LK), near_level=NEAR_LEVEL)
    rerun["calibration_stop"] = list(CAL_STOP); rerun["frozen"] = sorted(FROZEN); rerun["rate293"] = RATE293[0]
    rerun["calibration_rounds"] = CAL_ROUNDS[0]; rerun["stop356"] = list(STOP356); rerun["off"] = sorted(OFF)
    print("rerun:", rerun)
    pickle.dump(dict(would=would, deaths=deaths, made=made, survivors=len(alive), order_fp=order, alive=alive[:80], short=[c["fp"] for c in short],
                     pick=pick, pick_352=pick_352, clean=len(clean), pick_255=pick_255, pick_old_fit=pick_old, comp_first=alive[0] if alive else None, judge_first=byj[0] if byj else None, all=allb, every=every, stats=dict(STATS),
                     calibration=cal_log, knobs=KNOBS, line_knobs=dict(LK), rerun=rerun, form=FORM, chords=CHORD,
                     all_alive=[(c["fp"], c["judge"]["combined"], c["judge"]["content"], c["judge"]["order"], c["meas"]["composite"], c["meas"]["composite_old_fit"]) for c in alive]),
                open(f"/home/claude/p49/diag/melody_p45_{MODE}{_TAG}.pkl", "wb"))

print("DESIGN PARTS", dict(DCOUNT))
