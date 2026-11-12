"""ZenEng v127 Run 2 (Modules 27.69-27.71) onto Run 1 (songs/p52), by gen_v127.py. ZE_PART: 0 = the judge (470-473), 464, 459; 1 = and 434, 435;
2 = and 452, 455, 406, 465, 457, 458; 3 = and 408/468, 467, 461/450, 456. ZE_OFF switches a fix off (side runs only).
"""
"""ZenEng v124 Run 1 (Modules 27.64-27.68): repairs 405, 409, 412-415 and 428 onto the v119 port (songs/p51), by gen_v124.py.
Readings 417, 419 and v121-v123's (426, 431-433, 436, 437, 441-443) in readings_v124_block.py and new_readings_v124.py. ZE_OFF switches a fix off (side runs only).
"""
"""ZenEng v119 port (Module 27.63, Window 139), fixes 384-401, onto the v118 search (songs/p50), by gen_v119.py.
Steps (ZE_STEP): 1 = 384-387, 389, 394, 395; 2 = 388's side runs only (ZE_OFF=378, ZE_PIN388=1; 399 and 401 withdrawn, v120 421); 3 = and 398, 400, 390-393, 424 (v120).
"""
"""ZenEng v118 -- song 43, Blue Movie, run again on the v118 port (fixes 365-383 in force; findings from 384). Up-tempo dance-pop, q = 118, four on the floor,
straight; A minor for a light tenor (row C3-A4); 80 bars. The range centred in the row (314/333). Designs in force, named:
  Q15 A  the chorus's 'blue movie, blue movie' is one rhythmic figure sung twice, the second a scale step lower: a falling sequence
         from the chorus's high note; 'starring nobody but you' lifts back to the chorus's top (it carries 329's high extreme);
         the post-chorus chants: 'blue, blue' and 'no one else in the' on one pitch each, each line ending on the figure.
         A design gate (317), its pass rate printed.
  Q16 A  the arrangement (no melody gate). Q14 A: the lyric's density kept as written (342).
The frame: the search's tables are major-keyed (the key profile, the PPM) and draw on the relative major (C); its endings are on
its own tonic, A (ETON); 353: the window measures and the degrees aimed are read on A with the natural minor scale.
Usage: PYTHONHASHSEED=0 python3 melody_v127_p43.py N main|ctl [tag]
The v118 port it is built on:
ZenEng v118 PORT (fixes 365-383; Windows 137 and 138, 27.61 and 27.62) on the v116 port. Songs 40, 42, 43, 44 and 45 run again on it,
same lyrics, intakes, designs and seeds; song 43 twice more with fix 358 off and with fix 361 off (368's diagnostic runs).
  365 one calibration a measure: 249's gap knobs (gap16, gap8, gap4) leave its aimed calibration and stay at one; the gaps are set once,
      by the 354 knobs on unaimed builds.
  366 a share is set by a draw: each drawn line is drawn as one that may run sixteenths or may not, at a rate set on unaimed builds
      toward the kept 31% in runs; a line that may not is placed with no run, and falls back to runs only when nothing fits (counted).
  367 356's stop read against the rhythm band's kept quartiles, read with the table in use (372): 1.93 and 2.74 bits a note (the pooled
      kept table on 105 kept songs; 2.20 and 2.94 with the v88 table).
  368 the report's: song 43 run with 358 off and with 361 off; memory read with 373's limit.
  369 the kept windows' songs and modes on file (zeneng_v117_kept_songs_and_modes.json): 359 ported as written (the report's readings
      and costs for a minor song against the 70 kept minor windows; the judge of record kept); 364 read on the true songs.
  370 a failed bar is fitted within one onset: the copy's onsets, then the copy with its weakest onset dropped, then with one onset
      added at the bar's weakest free place, each strict; the bar kept when it comes within one onset of the copy.
  371 unit returns on the bar grid in every section of eight bars or more, at rates set on unaimed builds toward the kept readings
      (unit 2 returns unit 1 17.2%, unit 3 returns unit 1 31.5%, unit 4 returns unit 2 18.8%); 346/350's line-plan returns retired; a
      drawn unit return takes the bars it covers from 310's pairing.
  372 the rhythm table is the kept songs': an onset's gap to the next drawn from zeneng_v117_kept_rhythm_tables.json, the table for the
      band of the section's notes a bar (its syllables over its bars), in place of the v88 pop table; the melisma's sixteenth split at
      the band's kept share. The knobs of 354, 355, 365 and 366 start at one; a knob ending more than a factor of two from one is reported.
  373 limits read on the kept songs: the rhythm band read with the pooled kept table, soft 1.62-3.38, hard 1.43-3.61; memory soft 0.12,
      no hard limit; cmp unchanged.
  374 the report's (the yardstick, 0.57 and 0.63).
  375 a chord's own tones outside the scale are chord tones for its bar; a sung note a semitone from one clashes; 349's target read on
      the notes whose chord allows an outside pitch class.
  376 the frozen knob's message reads the round counter.
  377, 380 song designs (songs 44 and 45). 378 a line fills its slot: where the next line is in the same section, the line's span
      (first onset to the end of its last note, over the time to the next line's first onset) is drawn first inside the kept middle
      half for its notes (43-75% for up to five, 53-80% for six to eight, 66-88% for nine to twelve, 78-94% for more; Window 138) and the
      rhythm fills it; given up only when nothing fits (counted).
  379 an arrangement rule. 381 358's passing notes taken from the song's sung extra pitch classes. 382 surprisal soft 0.24, hard 0.08.
  383 the report's.
Usage: PYTHONHASHSEED=0 python3 melody_v127_p40.py N main|ctl [tag]
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
sys.path[:0] = ["/home/claude/p45", "/home/claude/p40", "/home/claude/p36", "/home/claude/carol", "/home/claude/pop"]
import melody_p36 as M
import lyricsearch; lyricsearch.OVERRIDE["pleather"] = ("P L EH1 DH ER0",)          # not in the pronouncing dictionary
import lyric_p43 as L
import judges as J
from measures import beta_pitch, s_spectral, cmp_score, m_horizon, PPM, ic_profile, feature_vec
MODE = _MODE; HERE = "/home/claude/p40"; H109 = "/home/claude/p41"; H110 = "/home/claude/p42"; H111 = "/home/claude/p43"; H112 = "/home/claude/p44"; H113 = "/home/claude/p45"; H114 = "/home/claude/p45"; H115 = "/home/claude/p46"; H116 = "/home/claude/p47"; H118 = "/home/claude/p53"; VAR = MODE; NEW = True
F = dict(f243=MODE == "main")
KW = json.load(open(f"{HERE}/tables/zeneng_v105_kept_windows.json"))
LIT = json.load(open(f"{HERE}/tables/zeneng_v104_line_in_time.json"))
GL = json.load(open(f"{HERE}/tables/zeneng_v106_gate_limits.json"))
SR = json.load(open(f"{HERE}/tables/zeneng_v108_spectral_and_registers.json"))
L286 = json.load(open(f"{HERE}/limits286.json"))["limits"]
KT = json.load(open(f"{H118}/tables/zeneng_v117_kept_rhythm_tables.json"))                  # 372
SS118 = json.load(open(f"{H118}/tables/zeneng_v118_slot_and_surprisal.json"))                # 378, 382
YS117 = json.load(open(f"{H118}/tables/zeneng_v117_yardstick.json"))                         # 373, 374
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
M.TONIC = 0; M.SCALE = {0, 2, 4, 5, 7, 9, 11}; M.SUNGPC = M.SCALE | {8, 6}               # the frame: C (relative major); G-sharp and F-sharp sung (344)
ETON = 9                                                                              # the song's tonic: A (endings)
OUT_PCS = (8, 6)
M.CH = {"Am": (9, {9, 0, 4}), "F": (5, {5, 9, 0}), "C": (0, {0, 4, 7}), "G": (7, {7, 11, 2}), "Dm": (2, {2, 5, 9}), "Em": (4, {4, 7, 11}), "E": (4, {4, 8, 11})}
M.ROMAN = {"Am": "i", "F": "VI", "C": "III", "G": "VII", "Dm": "iv", "Em": "v", "E": "V"}
M.QBPM = 118; M.SEC_PER_TW = 60 / M.QBPM / BEAT; M.LO = 48; TOP = 69; M.SUMMIT = TOP     # the voice row C3-A4 (Q10 A)
M.DEG = sorted(p for p in range(36, 90) if p % 12 in M.SCALE)
FEEL = "up-tempo dance-pop, q = 118, four on the floor, straight"
PLAN = {"Intro": ["Am", "F", "C", "G"] * 2, "Verse": ["Am", "F", "C", "G"] * 2, "Pre": ["Dm", "Em", "F", "G"],
        "Chorus": ["F", "G", "Am", "C", "F", "G", "F", "G"], "LastChorus": ["F", "G", "Am", "C", "F", "G", "F", "G"],
        "Post": ["Am", "F", "C", "G"], "LastPost": ["Am", "F", "G", "Am"], "Bridge": ["Dm", "Am", "F", "C", "Dm", "Am", "E", "E"], "Outro": ["Am", "F", "G", "Am"]}
FORM = [("Intro", "Intro", 8), ("Verse 1", "Verse", 8), ("Pre 1", "Pre", 4), ("Chorus 1", "Chorus", 8), ("Post 1", "Post", 4),
        ("Verse 2", "Verse", 8), ("Pre 2", "Pre", 4), ("Chorus 2", "Chorus", 8), ("Post 2", "Post", 4), ("Bridge", "Bridge", 8),
        ("Last Chorus", "Chorus", 8), ("Post 3", "Post", 4), ("Outro", "Outro", 4)]
BAR0, CHORD = {}, []
b = 0
for nm, kind, nb in FORM: BAR0[nm] = b; CHORD += PLAN["LastChorus" if nm == "Last Chorus" else "LastPost" if nm == "Post 3" else kind]; b += nb
NBARS = b; assert NBARS == 80 and len(CHORD) == NBARS
STOP_BARS = set()
KIND = {nm: kind for nm, kind, _ in FORM}; SECLEN = {nm: nb for nm, _, nb in FORM}
SUNG = ["Verse 1", "Pre 1", "Chorus 1", "Post 1", "Verse 2", "Pre 2", "Chorus 2", "Post 2", "Bridge", "Last Chorus", "Post 3"]
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
SLOTS = {"Verse": [2] * 4, "Pre": [2] * 2, "Chorus": [2] * 4, "Post": [2] * 2, "Bridge": [2] * 4, "Last Chorus": [2] * 4}      # every line two bars
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

def rhythm_bits_kept(notes):
    """372/373: the rhythm band, bits a note, read with the pooled kept table."""
    ons = [n["on"] for n in notes] + [NBARS * BAR]; out = []
    T_ = KRT["all"]
    for a, b2 in zip(ons, ons[1:]):
        d = min(96, b2 - a); d -= d % 3
        out.append(-math.log2(max(1e-9, T_[a % BAR - a % 3][d])))
    return float(np.mean(out))
M.rhythm_bits = rhythm_bits_kept
# ---- 375: a chord's own tones outside the scale are chord tones; a sung note a semitone from one clashes ----
_clash200 = M.clash
def clash375(p, ch):
    if _clash200(p, ch): return True
    if "375" in OFF: return False
    out = [t for t in M.CH[ch][1] if t not in M.SCALE]
    return any((p - t) % 12 in (1, 11) for t in out) and p % 12 not in M.CH[ch][1]
M.clash = clash375
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
        self.turn = LK["turn400"] if ON("400") else (K["turn"] * r("turns_per_move") if p == "V" else 1.0)   # 400 (reverses 304)               # 304: turns per move not aimed in the chorus
        self.b3, self.b24 = K["beat3"] * r("on_beat3"), K["beats24"] * r("on_beats_2_4")
        self.b3land, self.b3 = 1.0, 1.0                                                 # 290: onsets on beat 3 are no longer aimed
        g16 = K["gap16"] * r("gap_sixteenth")                                          # 288: the sixteenth (and dotted eighth) offered, aimed from the window
        self.tilt = {3: g16, 6: K["gap8"] * r("gap_eighth"), 9: g16, 12: K["gap4"] * r("gap_quarter"), 18: 1.6, 24: 1.6}
        H = min(36, max(12, 6 * t["longest_over_median_note"]))
        self.holds = {L_: math.exp(-(L_ - H) ** 2 / (2 * 9.0 ** 2)) for L_ in (12, 18, 24, 36)}
        x = max(0.0, t["notes_per_bar"] / 3.9 - 1.0)
        self.mel_inner, self.mel_final = min(0.40, 0.04 + 1.2 * x), min(0.5, 0.08 + 1.5 * x)
AIMS = {}; AIM = None
LK = dict(amp=5.0, widen=1.0, fresh=2.0, leap=1.0, s16=1.0, ctl=1.0, offb=1.0, dpk=1.0, k44=1.0, g8=1.0, g4=1.0, glong=1.0, run=1.0, on16=1.0,
          ct398=1.0, ctb398=1.0, ctd398=1.0, res398=1.0, turn400=1.0, ff424=1.0, lt424=1.0, eb424=0.25)   # 424: the empty-bar rate starts at a quarter                            # 398, 400: one knob each, from one   # 366: run is the rate at which a line may run; 372: every gap knob starts at one
GAPKNOBS = ("s16", "g8", "g4", "glong", "run", "on16")                                     # 372: the knobs of 354, 355, 365 and 366 (reported if they end more than a factor of two from one)
UR_KEPT = {1: (0, 0.172, "unit2_returns"), 2: (0, 0.315, "unit3_returns"), 3: (1, 0.188, "unit4_to_unit2")}   # 371: the kept readings
UR_RATE = {j: v[1] for j, v in UR_KEPT.items()}                                             # 371: drawn at rates set on unaimed builds (they start at the kept readings)
# ---- 372: the kept rhythm tables, by the band of the section's notes a bar, on the twelfth grid ----
KBANDS = [("under 3.5", 0, 3.5), ("3.5 to 4.5", 3.5, 4.5), ("4.5 to 5.5", 4.5, 5.5), ("5.5 and over", 5.5, 99)]
def kband(npb): return next(b for b, lo_, hi_ in KBANDS if lo_ <= npb < hi_)
def _rt12(tab):
    out = [[0.0] * 97 for _ in range(48)]
    for p16 in range(16):
        for g in range(1, 33): out[3 * p16][3 * g] = float(tab[p16][g])
    return out
KRT = {b: _rt12(KT["tables"][b]) for b in list(KT["tables"])}
KSH = KT["gap shares (sixteenth, eighth, quarter, longer than a quarter)"]
SEC_NPB = {}; SEC_BAND = {}
SH16_NOW = [float(KSH["all"][0])]                                                         # the melisma's sixteenth split: the band's kept share
for _s in SUNG:
    SEC_NPB[_s] = len([x for l_ in LINES[_s] for x in l_]) / SECLEN[_s]; SEC_BAND[_s] = kband(SEC_NPB[_s])
DU = [(0, 3.5, (0.04, 0.40, 0.24, 0.29)), (3.5, 4.5, (0.11, 0.50, 0.17, 0.18)), (4.5, 5.5, (0.14, 0.55, 0.16, 0.11)), (5.5, 99, (0.28, 0.49, 0.08, 0.09))]   # 354: Table DU
GAPS = ("gap_sixteenth", "gap_eighth", "gap_quarter", "gap_longer")
def du_target(npb): return tuple(KSH[kband(npb)])                                    # 372 (with 365): the four gaps toward the kept table's shares for the density
RUNW, PUSHW = 0.25, 1.5                                                               # 341: a sixteenth-position onset continued by a sixteenth / held an eighth or more
KEPT355 = dict(in_runs=0.31, on_sixteenth=0.094)                                          # 355
_dd = sorted(r_["distinct_durations"] for r_ in KRW if np.isfinite(r_.get("distinct_durations", np.nan)))
MID356 = dict(distinct_durations=(float(np.percentile(_dd, 25)), float(np.percentile(_dd, 75))),
              rhythm_bits=(1.934, 2.735))                                                       # 367 with 372: the kept quartiles read with the pooled kept table
STOP356 = []
KEPT398 = dict(chord_tones=0.639, chord_tones_on_beat=0.669, chord_tones_on_downbeat=0.722, non_chord_resolved_by_step=0.501)   # 398 (zeneng_v119_families.json)
KEPT400 = 0.584                                                                          # 400
_SC120 = {r_["measure"]: r_ for r_ in json.load(open(f"{H118}/tables/zeneng_v120_second_collection.json"))["every measure: collections' gap in sd, means (CoCoPops, BiMMuDa 1958-1991, builds v118)"]}
KEPT424 = {m_: round((314 * _SC120[m_]["cocopops"] + 231 * _SC120[m_]["bimmuda"]) / 545, 4) for m_ in ("fourth_fifth", "last_note_tonic", "empty_bars")}   # 424: both collections pooled (314 and 231 windows)
PIN388 = os.environ.get("ZE_PIN388") == "1"                                                # 388: a side run only
def _runs_kept(T):
    """389: of onsets on a sixteenth position, the share in runs (a sixteenth before and after), read off a kept table as a chain on the bar's 16 positions."""
    T = np.array(T, float); P_ = np.zeros((16, 16))
    for p_ in range(16):
        for g_ in range(1, 33): P_[p_, (p_ + g_) % 16] += T[p_][g_]
    P_ = P_ / P_.sum(1, keepdims=True); w_, v_ = np.linalg.eig(P_.T); pi_ = np.real(v_[:, np.argmin(abs(w_ - 1))]); pi_ = pi_ / pi_.sum()
    return float(sum(pi_[p_ - 1] * T[p_ - 1][1] / T[p_ - 1][1:].sum() * T[p_][1] / T[p_][1:].sum() for p_ in range(1, 16, 2)) / sum(pi_[p_] for p_ in range(1, 16, 2)))
RUN_POOLED = _runs_kept(KT["tables"]["all"])
RUN_KEPT_BAND = {b_: round(0.31 * _runs_kept(KT["tables"][b_]) / RUN_POOLED, 3) for b_ in KT["tables"] if b_ != "all"}   # 389: the kept 31%, scaled by the band's table
RUNR = {b_: 1.0 for b_ in RUN_KEPT_BAND}                                                 # 389: the run rate of each band, set on unaimed builds
def s16_bands(notes, dr=None):
    """389: onsets on a sixteenth position and those in runs, by the band of their section."""
    out = {}
    for s_ in SUNG:
        ons = sorted({n_["on"] for n_ in notes if n_["sec"] == s_}); S_ = set(ons); b_ = SEC_BAND[s_]; n6, r6 = out.get(b_, (0, 0))
        D_ = {n_["on"] for n_ in notes if n_["sec"] == s_ and (dr is None or dr.get(n_["line"]))}   # 405: the drawable lines' onsets
        for t_ in ons:
            if t_ not in D_: continue
            if t_ % 6 == 3: n6 += 1; r6 += (t_ - 3) in S_ and (t_ + 3) in S_
        out[b_] = (n6, r6)
    return out
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
    on_ = set(notes_on) | {x["on"] for x in ns}; cand = []
    elig = len(ns) if ("375" in OFF or ON("385")) else sum(1 for j in range(len(ns) - 1) if any(not M.clash(ns[j]["p"] + d_, M.chord_for(ns[j], on_)) and (ns[j]["p"] + d_) % 12 in extra
                                                                                 and not tri(ns[j]["p"] + d_, M.chord_for(ns[j], on_)) for d_ in (-1, 1)))   # 375: the notes whose chord allows one
    want = OS_T[0] * elig + meta.get("os_carry", 0.0); k = int(want)
    for j in range(0, len(ns) - 1):                                                       # not a line's last note (its ending)
        n = ns[j]; ch = M.chord_for(n, on_)
        for q in (n["p"] - 1, n["p"] + 1):
            if j > 0 and n["on"] % BEAT and q % 12 in (M.SUNGPC - M.SCALE if "381" not in OFF else set(range(12)) - M.SCALE) and "358" not in OFF \
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
        if pas: ns[j]["pre358"] = ns[j]["p"]                                               # 394: the note it replaced
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
SPAN_TO = [None]; SPAN_E = [None]
SPAN_MID = [(5, SS118["378 kept lines: the share of the time to the next line that a line sings (first onset to the end of its last note)"]["by note count"]["3 to 5"]),
            (8, SS118["378 kept lines: the share of the time to the next line that a line sings (first onset to the end of its last note)"]["by note count"]["6 to 8"]),
            (12, SS118["378 kept lines: the share of the time to the next line that a line sings (first onset to the end of its last note)"]["by note count"]["9 to 12"]),
            (999, SS118["378 kept lines: the share of the time to the next line that a line sings (first onset to the end of its last note)"]["by note count"]["13 to 24"])]
def span_wide(n): return next((q[0], q[4]) for k_, q in SPAN_MID if n <= k_)               # 391: the kept 5th to 95th percentiles
def span_mid(n): return next((q[1], q[3]) for k_, q in SPAN_MID if n <= k_)                # 378: the kept middle half for a line's notes
def line_rhythm(sy, rng, tmin, sec, last_max=None, fix=None, entry=None, prior=None, i=None, copybars=None, pair=False, stressbars=None, fallback=None, allbars=False, span_to=None):
    se = slot_end(sec, i); end = se if last_max is None else min(se, last_max)
    RTS = KRT[SEC_BAND[sec]] if "372" not in OFF else M.RT; SH16_NOW[0] = float(KSH[SEC_BAND[sec]][0]) if "372" not in OFF else SIXTEENTH   # 372
    SPAN_E[0] = None
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
    may_run = [runs_ok or "366" in OFF or rng.random() < (RUNR[SEC_BAND[sec]] if ON("389") else LK["run"])]                          # 366: a line may run sixteenths, drawn at a rate
    STATS["366: lines drawn that may run" if may_run[0] else "366: lines drawn that may not run"] += 1
    mr405 = may_run[0]                                                                    # 405: the draw before any fallback
    eb424 = bool(ON("424") and not ON("428") and i is not None and slot_len(sec, i) >= 2 and not fix and rng.random() < LK["eb424"])   # 424: bars left empty, at a rate
    sp = span_mid(n) if (span_to is not None and not fix) else None                          # 378: the span drawn first
    if sp and ON("414") and span_to * M.SEC_PER_TW > 0:                                     # 414: inside the band and the kept 1.4-2.3 syllables a second (423)
        T_ = span_to * M.SEC_PER_TW; d_ = (n / (2.3 * T_), n / (1.4 * T_)); a_, b_ = max(sp[0], d_[0]), min(sp[1], d_[1])
        if a_ <= b_: sp = (a_, b_); STATS["414: span inside the band and the density"] += 1
        else: sp = span_wide(n); STATS["414: band and density apart: the kept 5th-95th"] += 1
    s_span = rng.uniform(*sp) if sp else None
    def tw(tp, k, d):
        w = RTS[tp % BAR][d] * H(k - 1, d) * tilt.get(d, 1.0)                               # 372: the kept table for the section's band
        if "354" not in OFF: w *= LK["s16"] if d in (3, 9) else LK["g8"] if d == 6 else LK["g4"] if d == 12 else LK["glong"] if d > 12 else 1.0   # 354: the gaps together
        if tp % 6 == 3 and d < 6 and not may_run[0] and "348" not in OFF: w = 0.0               # 366 (amends 355): a line that may not run is placed with no run
        return w
    pal = PALS.get(KIND[sec])
    def dp(kind_, tgt, cb, sb=None, strict=()):
        def cbw(t, k=0):
            w = 1.0 if not cb or (t // BAR) not in cb or t in cb[t // BAR] else (0.0 if (t // BAR) in strict else 0.04)   # 360: a bar fitted again
            if sb and st[k] and (t // BAR) in sb and t not in sb[t // BAR]: w *= 0.04           # 322: a stressed syllable on the partner's stresses
            return w
        alpha = [dict() for _ in range(n)]
        for t in G:
            if tgt is not None and t > tgt: break
            if Ls == 0 and tgt is not None and t != tgt: continue
            if 0 in fix and t != fix[0]: continue
            if st[0] and t < 0: continue
            if kind_ is not None:
                if not ENTRY_T[kind_](t): continue
                alpha[0][(t, 1)] = A(0, t) * cbw(t, 0); continue
            alpha[0][(t, 1)] = (1.0 if t < 0 else (0.35 if t == 0 else 0.5)) * A(0, t) * cbw(t, 0)
        for k in range(1, n):
            for t in G:
                if k == Ls and tgt is not None and t != tgt: continue
                if k < Ls and tgt is not None and t >= tgt: continue
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
        key = (sec, i, tmin, end, tuple(lands), tuple(sorted(pal)) if pal else None, may_run[0])
        if key not in FITS: FITS[key] = {(k_, t) for k_ in ENTRY for t in lands if dp(k_, t, {})[0][n - 1]}   # cached: what fits depends on the slot alone
        fits = FITS[key]
        STATS["316: long lines"] += 1
        if not fits: STATS["316: long line with no entry and landing that fit"] += 1
    NT = 20 if copybars else 14
    if n >= 9: NT = 60
    for _try in range(NT + 10):
        if ON("389") and not may_run[0] and (_try == NT // 2 or (_try == 0 and fits is not None and not fits)):   # 389: falls back before it dies
            may_run[0] = True; STATS["366: fallback to runs (nothing fitted without)"] += 1; STATS["389: fallback at half the tries" if _try else "389: fallback at once (no entry and landing fit)"] += 1
            if n >= 9 and not fix:                                                         # the entries and landings that fit, read again with runs allowed
                key = (sec, i, tmin, end, tuple(lands), tuple(sorted(pal)) if pal else None, True)
                if key not in FITS: FITS[key] = {(k_, t) for k_ in ENTRY for t in lands if dp(k_, t, {})[0][n - 1]}
                fits = FITS[key]
        if ON("391") and s_span is not None and _try == NT // 2: s_span = rng.uniform(*span_wide(n)); STATS["391: span widened to the kept 5th-95th"] += 1
        free = _try >= NT or (fits is not None and not fits)
        if free and _try == NT: STATS["rhythm: placed with a free entry and landing"] += 1
        if _try == NT and not may_run[0]: may_run[0] = True; STATS["366: fallback to runs (nothing fitted without)"] += 1; STATS["389: fallback at the free tries" if ON("389") else "366: fallback at the free tries"] += 1
        if _try == NT and s_span is not None: s_span = None; STATS["378: span given up (nothing fitted inside it)"] += 1
        if free and pal is not None: pal = None; STATS["343: palette dropped for a line"] += 1
        kind_ = None
        if NEW and not fix and not free:
            ek = list(ENTRY) if fits is None else [k_ for k_ in ENTRY if any(f[0] == k_ for f in fits)]
            if entry in ENTRY_T and (fits is None or entry in ek): kind_ = entry
            else: kind_ = rng.choices(ek, [ENTRY[k_] for k_ in ek])[0]
            if kind_ == "pickup" and st[0] and fits is None: kind_ = rng.choices(["on", "after"], [ENTRY["on"], ENTRY["after"]])[0]
        spa = None
        if s_span is not None and not free:                                                   # 378: the landing inside the drawn span
            f0g = {"on": 0, "after": 12, "pickup": -6}.get(kind_, max(0, tmin))
            E0 = f0g + s_span * (span_to - f0g)
            spa = {t for t in range(-12, end + 1, 3) if E0 - 48 <= t <= E0 - 3 * (post + 1)}
        if Ls in fix: tgt = fix[Ls]
        elif free: tgt = rng.choice(list(range(max(0, tmin + step * Ls), end - step * post + 1, step)) or [end])
        elif fits is not None:
            al_ = {t for k_, t in fits if k_ == kind_}
            if spa is not None and al_ & spa: al_ = al_ & spa
            tgt = land_draw(rng, sec, n, i, allowed=al_)
        else: tgt = land_draw(rng, sec, n, i, allowed=spa if spa else None)
        if PIN388 and not free and Ls not in fix: tgt = None; STATS["388: landing left to the draw (side run)"] += 1
        cb = {}; sb = {}
        if copybars and _try < (NT if (allbars and ON("413")) else 14) and not free: cb = {bb: ts for bb, ts in copybars.items() if pair or allbars or rng.random() < RATE293[0]}   # 293 at 331's rate; 310 and 361: every bar
        elif copybars and _try == (NT if (allbars and ON("413")) else 14) and not (pair and fallback): STATS["361: unit return given up for a line" if allbars else "293: copy given up for a line" if not pair else "310: partner's rhythm given up for a line"] += 1
        if pair and fallback and 14 <= _try < NT and not free: sb = fallback                  # 330: the copy failed: the partner's stresses
        elif pair and fallback and _try == NT: STATS["330: partner given up after its stresses"] += 1
        if stressbars and _try < 14 and not free: sb = stressbars                         # 322
        elif stressbars and _try == 14: STATS["322: partner's stresses given up for a line"] += 1
        if tgt is not None and (tgt + step * post > end or tgt - step * Ls < tmin): continue
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
        if eb424 and not free and _try < NT // 2 and max(ons) >= (slot_len(sec, i) - 1) * BAR: STATS["424: redrawn to leave the slot's last bar empty"] += 1; continue
        if eb424 and _try >= NT // 2 and max(ons) >= (slot_len(sec, i) - 1) * BAR: STATS["424: empty bar given up for a line"] += 1; eb424 = False
        if eb424: STATS["424: line leaves its slot's last bar empty"] += 1
        if s_span is not None and not free:                                                   # 378: the line ends inside its drawn span
            E = ons[0] + s_span * (span_to - ons[0])
            if not (ons[-1] + 3 <= E <= ons[-1] + 48): STATS["378: rhythm outside its span, redrawn"] += 1; continue
            SPAN_E[0] = E
        if cb:                                                                             # 303 with 351: a bar off by more than one onset leaves the copy
            badf = lambda o_: [bb for bb, ts in cb.items() if len(set(ts) ^ {t for t in o_ if t // BAR == bb}) > 1]
            bad = badf(ons)
            if bad and "360" not in OFF:                                                   # 360 with 370: the failed bars fitted again within one onset
                def _drop(ts_): wk = min(ts_, key=lambda t: (M.mw(t), -t)); return [t for t in ts_ if t != wk] if len(ts_) > 1 else list(ts_)
                def _add(bb, ts_):
                    fr = [t for t in range(bb * BAR, (bb + 1) * BAR, 6) if t not in ts_ and tmin <= t <= end]
                    return sorted(ts_ + [min(fr, key=lambda t: (M.mw(t), -t))]) if fr else list(ts_)
                variants = [cb, {bb: (_drop(ts) if bb in bad else ts) for bb, ts in cb.items()}, {bb: (_add(bb, ts) if bb in bad else ts) for bb, ts in cb.items()}]
                kept_ = False
                for vi, cbv in enumerate(variants if "370" not in OFF else variants[:1]):
                    a2, _ = dp(kind_, tgt, cbv, sb, strict=set(bad))
                    o2 = sample(a2) if a2[n - 1] else None
                    if o2 is not None and len(badf(o2)) < len(bad):
                        STATS["360: bars fitted again and kept"] += len(bad) - len(badf(o2)); STATS[f"370: kept by variant {('copy', 'one dropped', 'one added')[vi]}"] += len(bad) - len(badf(o2))
                        ons = o2; bad = badf(o2); kept_ = True; break
                if not kept_: STATS["360: bars fitted again without success"] += len(bad)
            if bad and allbars: STATS["413: unit-return bars left out (more than one onset off)"] += len(bad)
            if bad: STATS["351: bars left out of a copy"] += len(bad); cb = {bb: ts for bb, ts in cb.items() if bb not in bad}
        STATS["361: unit bars copied" if allbars else "293: bars copied" if not pair else "310: partner bars copied"] += len(cb)
        if sb and not pair: STATS["322: partner's stresses kept"] += 1
        if sb and pair: STATS["330: copy failed, partner's stresses kept"] += 1
        if ON("405") and i is not None and CUR405[0] is not None:                         # 405: a line that could be placed without runs
            CUR405[0][f"{sec}:{i}"] = bool(not runs_ok and (mr405 or not may_run[0])); STATS["405: line drawable without runs" if CUR405[0][f"{sec}:{i}"] else ("405: line with no room on the eighth grid" if runs_ok else "405: line fell back to runs")] += 1
        return ons
    return None
RATE293 = [0.40]                                                                     # 331: set in the calibration (kept verse 2 share 50%)
V2_KEPT = 0.50
def v2_share(notes):
    """331 (and 313's reading): verse 2's bars whose onsets are within one of verse 1's same bar."""
    eq_ = {i_ for i_ in range(min(len(LINES["Verse 1"]), len(LINES["Verse 2"]))) if len(LINES["Verse 2"][i_]) == len(LINES["Verse 1"][i_])} if (ON("393") and not ON("415") and "Verse 2" in LINES) else None   # 393 (415 reads bars)
    if eq_ is not None and not eq_: eq_ = None
    def bars(s):
        out = collections.defaultdict(set)
        for n in notes:
            if n["sec"] == s and (eq_ is None or s != "Verse 2" or int(n["line"].rsplit(":", 1)[1]) in eq_): out[n["on"] // BAR - BAR0[s]].add(n["on"] % BAR)
        return out
    a, c = bars("Verse 2"), bars("Verse 1")
    if ON("415"):                                                                          # 415: the bars with the same count of syllable onsets
        def syl(s):
            out = collections.Counter(); seen = set()
            for n in notes:
                if n["sec"] == s and (n["line"], n["syl"]) not in seen: seen.add((n["line"], n["syl"])); out[n["on"] // BAR - BAR0[s]] += 1
            return out
        sa, sc = syl("Verse 2"), syl("Verse 1"); keep = [k for k in a if k in c and abs(sa[k] - sc[k]) <= (1 if ON7("459") else 0)]
        if keep: STATS["415: verse 2 read on bars of equal syllables"] += 1; return sum(1 for k in keep if len(a[k] ^ c[k]) <= 1) / len(keep)
        STATS["415: no bar of equal syllables (all bars read)"] += 1
    return sum(1 for k, x in a.items() if k in c and len(x ^ c[k]) <= 1) / max(1, len(a))
LONG_SHARE = 0.57                                                                    # 308: the kept 75th percentile of the fullest bar's share
SIXTEENTH = 0.147                                                                     # 288: the class's kept share of sixteenth gaps (v88, pop, mean)
def melismas(ons, rng, end, pal=None):
    rows = []
    ok = lambda *g: pal is None or all(x in pal for x in g)                                # 343: a split's lengths in the palette
    for k, t in enumerate(ons):
        rows.append([t, k, False]); nxt = ons[k + 1] if k + 1 < len(ons) else None
        sx = rng.random() < SH16_NOW[0] / 0.431 * LK["s16"]                                # a sixteenth split at the band's kept share (372), 341's knob
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
    if ON("398") and (DRAWN398[0] or not ON("412")) and p % 12 in tones: w *= LK["ct398"] * (LK["ctb398"] if on_beat else 1.0) * (LK["ctd398"] if n["on"] % BAR == 0 else 1.0)   # 398: overall, on a beat, on a downbeat
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
                rs_ = LK["res398"] if (ON("398") and (DRAWN398[0] or not ON("412")) and PREV_NC[0] and 0 < abs(p - prev) <= 2 and p % 12 in M.CH[ch][1]) else 1.0   # 398: a note off its chord left by step
                lt_ = LK["lt424"] if (LAST424[0] and (p - mton()) % 12 == 0) else 1.0             # 424: the window's last note on the tonic
                cands.append(p); ws.append(w0 * chord_w(p, n, ch) * deg_w(p) * sf * extra_w(p) * rs_ * lt_); base += w0
        if c[0] == "larger": c = (c[0], c[1] * LK["leap"], c[2])
        if c[0] == "fourth_fifth" and ON("424"): c = (c[0], c[1] * LK["ff424"], c[2])         # 424: leaps of a fourth or fifth                            # 312: leaps past a fifth held to the kept 75th percentile
        if cands and base > 0 and c[1] > 0:
            wd = math.exp(LK["widen"] * (SHAPE[1] - 0.5) * (-1 if c[0] in ("repeat", "step") else 1)) if SHAPE is not None else 1.0   # 258: on the category
            for p, w in zip(cands, ws): allc.append(p); allw.append(c[1] * wd * w / base)
    if allc and sum(allw) > 0: return rng.choices(allc, allw)[0]
    return None
SHAPE = None
PREV_NC = [False]
CUR424 = [None]; LAST424 = [False]
WL409 = {}
def wlast409(sec, j):
    """409: the line is the last of its section to begin inside the section's first eight bars (the window's last line)."""
    if sec not in WL409: WL409[sec] = max([k for k in range(len(LINES[sec])) if line_start(sec, k) < (BAR0[sec] + 8) * BAR] or [-1])
    return j == WL409[sec]
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
            w409 = ON("409") and ON("424") and isinstance(CUR424[0], tuple) and i == len(notes) - 1 and wlast409(*CUR424[0])   # 409: a slurred last note too
            if w409: STATS["409: the window's last note weighted (slurred)"] += 1
            p = rng.choices(opts, [(3 if x < q_ else 1) * chord_w(x, n, ch_) * (LK["lt424"] if (w409 and (x - mton()) % 12 == 0) else 1.0) for x in opts])[0] if opts else q_
        elif shape is not None and i == 0:
            p = first_note(rng, n, M.chord_for(n, notes_on), shape[0][0], lo, hi)       # 259: not the next step from the line before
        else:
            tw = fixed.get(i + 1) if fixed else None
            SHAPE = shape[i] if shape is not None else None
            PREV_NC[0] = bool(out) and i > 0 and out[-1] % 12 not in M.CH[M.chord_for(notes[i - 1], notes_on)][1]   # 398: the note before off its chord
            LAST424[0] = ON("424") and CUR424[0] is not None and i == len(notes) - 1 and (wlast409(*CUR424[0]) if ON("409") else (n["on"] // BAR - BAR0[CUR424[0]]) % 8 == 7)   # 424: a window's last note
            if LAST424[0] and isinstance(CUR424[0], tuple): STATS["409: the window's last note weighted (walk)"] += 1
            p = next_pitch(rng, prev, run, n, M.chord_for(n, notes_on), mu, lo, hi, last_iv, toward=tw); SHAPE = None; LAST424[0] = False
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
    ons = line_rhythm(sy, rng, tmin, sec, last_max, fix, entry=entry, i=i, span_to=SPAN_TO[0], **kw)
    if ons is None: return None
    E_ = SPAN_E[0]
    se = slot_end(sec, i); me_ = se if last_max is None else min(se, last_max)
    if E_ is not None: me_ = min(me_, int(E_) - 3)                                          # 378: a final melisma inside the span
    rows = melismas(ons, rng, me_, PALS.get(KIND[sec])) if not fix or len(fix) < len(sy) else [[t, k, False] for k, t in enumerate(ons)]
    ns_ = [dict(on=U + t, p=None, syl=k, slur=s, stress=(sy[k][1] and not s)) for t, k, s in rows]
    if E_ is not None and U + E_ - ns_[-1]["on"] >= 3:                                       # 378: the last note held to the span's end
        ns_[-1]["hold"] = int(U + E_ - ns_[-1]["on"]); STATS["378: lines drawn to a span"] += 1
    return ns_

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
    if ON7("434"):                                                                         # 434, 435: verse 1's pitch where both strike the same place, the rest drawn
        src_at = {m_["on"] - SU: m_["p"] for m_ in S}; mapped = [n_["p"] for n_ in ns]; fx = {0: ns[0]["p"], len(ns) - 1: ns[-1]["p"]}
        for j_, n_ in enumerate(ns[1:-1], 1):
            t_ = n_["on"] - U
            if t_ in src_at:
                STATS["435: verse 2 strikes verse 1's place"] += 1
                if rng.random() < K435: fx[j_] = src_at[t_]; STATS["435: verse 1's pitch kept"] += 1
        d_ = [n_["dur"] for n_ in ns]; DRAWN398[0] = True                                  # 434: verse 2's chord tones from 398's knobs, as verse 1's
        ps_ = walk_notes(rng, ns, None, 1, float(np.median(mapped)), lo, hi, on_all, fixed=fx, shape=[(h_, 0.0) for h_ in mapped]); DRAWN398[0] = False
        for n_, x_ in zip(ns, d_): n_["dur"] = x_
        if ps_ is None: STATS["434: walk failed, the mapped pitches kept"] += 1; ps_ = mapped
        srep = {(m_["on"] - SU) for k_, m_ in enumerate(S) if k_ and m_["p"] == S[k_ - 1]["p"]}
        for j_ in range(1, len(ns)):                                                          # 434: no repeat the source line did not sing
            if j_ in fx or ps_[j_] != ps_[j_ - 1] or ns[j_]["slur"]: continue
            x_ = (ns[j_]["on"] - U - n0) / max(1, n1 - n0) * (s1 - s0) + s0; sj_ = min(srel, key=lambda e: abs(e[0] - x_))[0]
            if sj_ in srep: continue
            ch_ = M.chord_for(ns[j_], on_all)
            op_ = [ps_[j_] + d for d in (1, -1, 2, -2) if lo <= ps_[j_] + d <= hi and (ps_[j_] + d) % 12 in M.SCALE and not tri(ps_[j_] + d, ch_) and (j_ + 1 >= len(ns) or ps_[j_] + d != ps_[j_ + 1])]
            if op_: ps_[j_] = max(op_, key=lambda q_: chord_w(q_, ns[j_], ch_)); STATS["434: a repeat the source did not sing, moved"] += 1
        for n_, p_ in zip(ns, ps_): n_["p"] = p_
    for n in ns:
        ch = M.chord_for(n, on_all); tones = M.CH[ch][1]
        if (n["stress"] and n["on"] % BEAT == 0 and n["p"] % 12 not in tones and not ON7("434")) or tri(n["p"], ch):   # 434: the move to a chord tone removed
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
    if len(pl) >= 4 and all(x == 2 for x in slots_of(sec)) and "371" in OFF:              # 346: retired by 371 (unit returns on the bar grid in every section)
        for j, src, rate in ((1, 0, 0.172), (2, 0, 0.315), (3, 1, 0.188)):                     # 346; 350: unit 3 returns unit 1
            if pl.index(pl[j]) == j and rng.random() < rate:
                tr = pl[:j] + [pl[src]] + pl[j + 1:]
                if admissible(sec, "".join(tr)): pl = tr; STATS[f"346: line {j + 1} returns line {src + 1}"] += 1
    return pl
SRC = {"Verse 2": "Verse 1", "Pre 2": "Pre 1", "Chorus 2": "Chorus 1", "Last Chorus": "Chorus 1", "Post 2": "Post 1"}

# ---- 288: section registers drawn from the kept distribution (chorus and bridge against the verse) ----
QS = [1, 5, 25, 50, 75, 95, 99]
REG = SR["section registers, kept percentiles (1, 5, 25, 50, 75, 95, 99)"]
def kept_draw(key, u): return float(np.interp(100 * u, QS, REG[key]))
V_MU, V_CAP, V_FLOOR = 64, 69, 57                                                     # replaced per build by 314's draw (below)
ROW_LO, ROW_HI = M.LO, TOP; PLACE = "centre"                                           # 314: the row, and the writer's placement (centre unless chosen)
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
    R["Post"] = R["Chorus"]                                                            # the post-chorus sings in the chorus's register
    R = {k: widen_329(v, lo, hi) for k, v in R.items()}
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
TRIAD = {9, 0, 4}
ENDING_NEEDS.update(Post={ETON})                                                     # 311: the last post-chorus (the song's last line) ends on the tonic
def end_ok(sec, i, p):
    if i != len(LINES[sec]) - 1: return True
    if sec == "Verse 1": return (p - ETON) % 12 != 0                                     # the verse ends off the tonic
    if sec == "Post 3": return (p - ETON) % 12 == 0                                      # 'scene after scene': home
    return True
def end_target(sec, i, h_end, lo, hi, mu=None):
    """295: the contour of an ending line is drawn toward the nearest permitted ending; 314: a tonic ending toward the tonic nearest the
    section's median."""
    c = [p for p in range(lo, hi + 1) if p % 12 in M.SCALE and end_ok(sec, i, p)]
    if mu is not None and c and all((p - ETON) % 12 == 0 for p in c): return min(c, key=lambda p: (abs(p - mu), p))
    return min(c, key=lambda p: abs(p - h_end)) if c else h_end
def end_rule(sec, i, ns, notes_on, lo, hi):
    if end_ok(sec, i, ns[-1]["p"]): return
    n = ns[-1]; ch = M.chord_for(n, set(notes_on) | {x["on"] for x in ns}); q0 = n["p"]
    opts = [q0 + d for d in (-1, 1, -2, 2, -3, 3) if lo <= q0 + d <= max(hi, q0) and (q0 + d) % 12 in M.SCALE and not tri(q0 + d, ch) and end_ok(sec, i, q0 + d)]
    if opts: n["p"] = opts[0]; STATS["262: last note moved"] += 1

def generate(rng, cal=None):
    """one build. cal: a calibration build (targets at the pools' medians)."""
    global AIM
    meta = dict(returns=[], kinds={}, win={}, targets={}, drawable405={}); CUR405[0] = meta["drawable405"]   # 405
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
    plans = dict(Verse=draw_plan(rng, "Verse 1", VERSE_PLANS), Bridge=draw_plan(rng, "Bridge", BRIDGE_PLANS), Pre=draw_plan(rng, "Pre 1", PRE_PLANS),
                 tail=rng.choice(["return", "fresh"]), line5=rng.choice(["return", "fresh"]))
    meta["plans"] = plans
    UR = {}                                                                              # 361: unit returns on the bar grid, for sections not all of two-bar lines
    for k_ in sorted({KIND[s_] for s_ in SUNG}):
        s1_ = next(s_ for s_ in SUNG if KIND[s_] == k_)
        if SECLEN[s1_] < 8 or "361" in OFF or ("371" in OFF and all(x == 2 for x in slots_of(s1_))): continue   # 371: every section of eight bars or more
        UR[k_] = {}
        for j, (src, kept_, _m) in UR_KEPT.items():
            if rng.random() < UR_RATE[j]: UR[k_][j] = src; STATS[f"361: unit {j + 1} returns unit {src + 1} (bar grid), drawn"] += 1
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
        if sec == "Post 2": return ("copy", "Post 1", i)
        if sec == "Last Chorus": return ("copy", "Chorus 1", i) if i < 3 else ("return", "Chorus 1", 3)   # 'starring only me and you'
        if sec in ("Verse 2", "Pre 2"): return ("again", SRC[sec], i)
        if sec == "Chorus 1" and i == 2: return ("figure", None, None)                     # Q15 A: the falling sequence
        if sec == "Post 1": return ("chant", None, None)                                   # Q15 A: the chant on the figure
        if kind in ("Chorus", "Post"): return ("fresh", None, None)
        plan = plans[kind]; first = plan.index(plan[i])
        return ("plan", sec, first) if first < i else ("fresh", None, None)
    if ON("390"):                                                                          # 390: a unit the plan already returns is not drawn again
        meta["ur_given"] = {}
        for k_, d_ in UR.items():
            s1_ = next(s_ for s_ in SUNG if KIND[s_] == k_); g_ = {}
            for j, (src, kept_, _m) in UR_KEPT.items():
                ls_ = [ii for ii in range(len(LINES[s1_])) if 2 * j * BAR <= line_start(s1_, ii) - BAR0[s1_] * BAR < 2 * (j + 1) * BAR]
                def _given(ii):
                    h_, s_, i_ = how(s1_, ii)
                    return h_ in ("plan", "return", "copy") and s_ == s1_ and line_start(s1_, ii) - line_start(s1_, i_) == 2 * (j - src) * BAR
                if ls_ and all(_given(ii) for ii in ls_):
                    g_[j] = True; STATS[f"390: unit {j + 1} returned by the plan"] += 1
                    if j in d_: d_.pop(j); STATS["390: drawn unit return dropped (the plan gives it)"] += 1
            meta["ur_given"][k_] = g_
        meta["unit_returns"] = {k_: dict(v) for k_, v in UR.items()}
    # 329: one fresh line carries the song's lowest drawn note (a verse or the bridge), one its highest (a chorus or the bridge)
    xlo = min(p for p in range(meta["registers"]["song_lo"], meta["registers"]["song_hi"] + 1) if p % 12 in M.SCALE)
    xhi = max(p for p in range(meta["registers"]["song_lo"], meta["registers"]["song_hi"] + 1) if p % 12 in M.SCALE)
    lowc = [(s_, j) for s_ in SUNG if s_ in CARRY_LOW for j in range(len(LINES[s_])) if how(s_, j)[0] == "fresh"]
    highc = [(s_, j) for s_ in SUNG if s_ in CARRY_HIGH for j in range(len(LINES[s_])) if how(s_, j)[0] == "fresh"]
    car_lo = rng.choice(lowc) if lowc else None
    highc = [x for x in highc if x != car_lo] or highc
    car_hi = ("Chorus 1", 3)                                                               # Q15 A: 'starring nobody but you' lifts to the chorus's top
    CARRY = {}
    if "329" in OFF: car_lo = car_hi = None                                                 # diagnostics only
    if car_lo: CARRY[car_lo] = xlo
    if car_hi: CARRY[car_hi] = xhi
    meta["carriers"] = dict(low=(car_lo, xlo), high=(car_hi, xhi))
    for (s_, j), x in CARRY.items():                                                       # the carrying section's register reaches it
        k_ = KIND[s_]; mu_, cap_, fl_ = REGS[k_]; REGS[k_] = (mu_, max(cap_, x), min(fl_, x))
    def endok_of(sec, i):
        rule = sec in ("Verse 1", "Post 3") and i == len(LINES[sec]) - 1
        return (lambda p: end_ok(sec, i, p)) if rule else None
    def prefit(sec, i):
        """247: a copy, return or re-sung line is fitted to its words before the line ahead of it is drawn."""
        if (sec, i) in pending: return pending[(sec, i)]
        h, s0, i0 = how(sec, i); U = line_start(sec, i); r = None
        if h in ("figure", "chant"):                                                         # Q15 A: the designed lines
            r = ("ns", design_line(rng, h, sec, i, U, meta, notes_on_all), "design")
        elif h in ("copy", "return", "plan", "tail") and (s0, i0) in built:
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
            last_max = None; f0 = None
            if nxt:
                pf = prefit(*nxt)
                if pf and pf[0] == "fail": globals().__setitem__("WHERE", ("prefit",) + tuple(nxt) + (how(*nxt)[0],)); return _fail(("align: the words do not fit the returning tune" if pf[1] == "align" else "rhythm: no placement"))
                f0 = None
                if pf and pf[1]: f0 = (pf[1][0]["on"] - line_start(*nxt)) if pf[0] == "ns" else pf[1][0]
                if f0 is not None: last_max = (line_start(*nxt) + f0 - U) - GAP_MIN
            h, s0, i0 = how(sec, i)
            SPAN_TO[0] = (line_start(*nxt) - U + (f0 if f0 is not None else 0)) if (nxt and nxt[0] == sec and "378" not in OFF) else None   # 378
            if h in ("copy", "return", "plan", "tail", "figure", "chant") and (prefit(sec, i) or ("",))[0] == "ns":
                _, ns, kd = pending[(sec, i)]; ns = [dict(n) for n in ns]
                for n in ns: n.pop("hold", None); n.pop("title", None)
                meta["kinds"][(sec, i)] = kd if h != "tail" else "tail"
                if h in ("figure", "chant"): meta["kinds"][(sec, i)] = "design"
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
                if ub and partner is not None:                                                # 371: a drawn unit return takes its bars from 310's pairing
                    if "371" in OFF: STATS["361: unit return under a paired line (310 kept)"] += 1; ub, upit = {}, {}
                    else: STATS["371: unit return over a paired line (the return kept)"] += 1; partner = None
                ns = fresh_line(sy, rng, U, tmin, sec, last_max, None, i=i, partner=partner, unitbars=ub or None)
                if ns is None and ub: STATS["413: build lost on a unit-return line (no rhythm)"] += 1
                if ns is None: globals().__setitem__("WHERE", (sec, i)); return _fail("rhythm: no placement")
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
                            last_p = tgt if tgt in cands and all((p - ETON) % 12 == 0 for p in cands) else rng.choices(cands, [math.exp(-(p - tgt) ** 2 / 4.5) * (LK["lt424"] if (ON("424") and (p - mton()) % 12 == 0 and (wlast409(sec, i) if ON("409") else (ns[-1]["on"] // BAR - BAR0[sec]) % 8 == 7)) else 1.0) for p in cands])[0]   # 314; 424
                            if ns[-1]["slur"] and len(ns) > 1: fx = {len(ns) - 1: last_p}
                            else: fx = {len(ns) - 1: last_p}
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
                            elif q_ is not None and j_ not in fx: STATS["413: unit-return pitch not kept (range, slur or chord), a try"] += 1
                    CUR424[0] = (sec, i) if ON("409") else sec                                  # 409: the line, to find the window's last
                    DRAWN398[0] = True                                                          # 412: the drawn notes
                    ps = walk_notes(rng, ns, prev, run, mu, lo, hi, notes_on_all, fixed=fx, shape=shape); CUR424[0] = None; DRAWN398[0] = False
                    if ps is None: continue
                    if need_end and not end_ok(sec, i, ps[-1]) and _try < 7: ps = None; continue
                    break
                if ps is None: globals().__setitem__("WHERE", (sec, i)); return _fail("walk: no note")
                for n, p in zip(ns, ps): n["p"] = p
                if need_end and not end_ok(sec, i, ns[-1]["p"]): end_rule(sec, i, ns, notes_on_all, lo, hi); meta["moved"] += 1
                place_outside(rng, ns, notes_on_all, meta)                                       # 349
                if need_end:                                                                   # 324: a tonic ending, against its register's centre
                    tc = [p for p in range(lo, hi + 1) if p % 12 in M.SCALE and end_ok(sec, i, p)]
                    if tc and all((p - ETON) % 12 == 0 for p in tc):
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
    if ON("394"):                                                                          # 394: a passing note in a tune that returns, in every occurrence or none
        def root394(k):
            seen = {k}
            while True:
                h_, s_, i_ = how(*k)
                if h_ in ("copy", "return", "plan", "tail", "again") and (s_, i_) in built and (s_, i_) not in seen: k = (s_, i_); seen.add(k)
                else: return k
        occ = collections.defaultdict(list)
        for k in built: occ[root394(k)].append(k)
        for r_, ks in occ.items():
            if len(ks) < 2: continue
            RU_ = line_start(*r_)
            for n in built[r_]:
                if not n.get("pass358") or "pre358" not in n: continue
                rel_ = n["on"] - RU_; ok = True; spots = []
                for k in ks:
                    if k == r_: continue
                    L = built[k]; LU = line_start(*k); j = next((jj for jj, m in enumerate(L) if m["on"] - LU == rel_), None)
                    if j is None or j == 0 or j == len(L) - 1 or L[j].get("pin"): ok = False; break
                    m = L[j]
                    if m.get("pass358") or m["p"] == n["p"]: m["pass358"] = True; m["outside"] = True; m.setdefault("pre358", n["pre358"]); continue   # it already sings the passing note
                    q = m["p"] + (n["p"] - n["pre358"])
                    if q % 12 in (M.SUNGPC - M.SCALE) and 1 <= abs(q - L[j - 1]["p"]) <= 2 and 1 <= abs(L[j + 1]["p"] - q) <= 2: spots.append((m, q))
                    else: ok = False; break
                if ok:
                    for m, q in spots: m["pre358"] = m["p"]; m["p"] = q; m["pass358"] = True; m["outside"] = True
                    STATS["394: passing note placed in every occurrence"] += 1; STATS["394: occurrences given the passing note"] += len(spots)
                else:
                    pp_ = n["p"]; pr_ = n["pre358"]
                    for k in ks:
                        LU = line_start(*k)
                        for m in built[k]:
                            if m["on"] - LU == rel_ and (m.get("pass358") or m["p"] == pp_):
                                m["p"] = pr_ if m["p"] == pp_ else m.get("pre358", m["p"]); m.pop("pass358", None); m.pop("outside", None)
                    STATS["394: passing note withdrawn (an occurrence could not take it)"] += 1
    notes = sorted([n for l in lines for n in l], key=lambda n: n["on"])
    on = {n["on"] for n in notes}
    built_ret = {f"{sec}:{i}" for sec, i, s0, i0, kd in meta["returns"] if kd != "sung again"}
    built_ret |= {f"{sec}:{i}" for (sec, i), kd in meta["kinds"].items() if kd == "design" or (sec, i) in (("Chorus 2", 2), ("Last Chorus", 2), ("Post 2", 0), ("Post 2", 1))}   # the design and its copies left alone
    for n in notes:
        n.setdefault("dur", 12)
        if n["line"] in built_ret or n.get("pass358"): continue                            # 287: a built return is left alone (the limits read it); 358: a passing note stays
        ch_ = M.chord_for(n, on)
        if n["p"] % 12 in OUT_PCS and M.clash(n["p"], ch_):
            tones = M.CH[ch_][1]; n["p"] = min((n["p"] - 1, n["p"] + 1), key=lambda q_: (q_ % 12 not in tones, q_ % 12 not in M.SCALE))
        if tri(n["p"], ch_):                                                                # 215: a copied note moves a step to a chord tone
            tones = M.CH[ch_][1]; n["p"] = min((n["p"] + 1, n["p"] - 1, n["p"] + 2, n["p"] - 2), key=lambda q_: (q_ % 12 not in tones, abs(q_ - n["p"])))
    if ON("386"):                                                                          # 386: 375's clash read on returning and copied lines too
        for n in notes:
            if n.get("pin") or (n.get("pass358") and n["on"] % BEAT and n.get("dur", 12) < BEAT): continue
            ch_ = M.chord_for(n, on)
            if clash375(n["p"], ch_) and not _clash200(n["p"], ch_):
                tones = M.CH[ch_][1]; q0 = n["p"]
                opts = [q_ for q_ in (q0 + 1, q0 - 1, q0 + 2, q0 - 2) if not clash375(q_, ch_) and not tri(q_, ch_)]
                if opts:
                    n["p"] = min(opts, key=lambda q_: (q_ % 12 not in tones, q_ % 12 not in M.SCALE and q_ % 12 not in tones, abs(q_ - q0))); n["moved386"] = q0
                    STATS["386: notes moved off a semitone from a chord's outside tone"] += 1; STATS[f"386: moved in a {meta['kinds'].get(tuple(n['line'].split(':')[:1]) + (int(n['line'].split(':')[1]),), 'line')} line"] += 1
                else: STATS["386: a clashing note with no move"] += 1
    finish(notes, rng)
    return dict(notes=notes, meta=meta), None

# ---- the discriminator (v96 feats on 8-bar windows) ----
MAJ = {0, 2, 3, 5, 7, 8, 10}                                                         # 353: the natural minor scale, read on the tonic
MTON = ETON; OS_SCALE = 4.5 / 7.1                                                     # 353: the measures on A; 349: the kept minor rate
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
RJ = json.load(open(f"{H118}/tables/zeneng_v126_judge.json"))["content_judge"]                 # 470
exec(next(v_ for k_, v_ in json.load(open(f"{H118}/tables/zeneng_v121_blind_spots.json")).items() if k_.startswith("code: cand")))   # cand(): the four new measures
RJ_MU, RJ_SD, RJ_W, RJ_F = (np.array(RJ[k_], float) for k_ in ("mean", "sd", "weight", "fill_missing_with"))
def refit_score(f, N):
    """470: intercept + sum of weight x (value - mean) / sd over the 37 measures; a measure the window lacks takes the kept median."""
    f = f or {}; c_ = cand(sorted(N)) or {}; x_ = []
    for m_, fill_ in zip(RJ["measures"], RJ_F):
        v_ = f.get(m_) if m_ in f else c_.get(m_)
        x_.append(fill_ if v_ is None or not np.isfinite(v_) else v_)
    return float(RJ["intercept"] + RJ_W @ ((np.array(x_, float) - RJ_MU) / RJ_SD))
def judge(notes):
    """252-254: the mean over Verse 1's and Chorus 1's windows (8 bars from the section's first bar)."""
    rows = {}
    for s in ("Verse 1", "Chorus 1"):
        N = win_N(notes, BAR0[s]); f = feats(N, mton()); rows[s] = dict(J.score_window(f, N), feats=f); rows[s]["refit"] = refit_score(f, N)
    return dict(refit_content=float(np.mean([r["refit"] for r in rows.values()])), refit_combined=float(np.mean([(r["refit"] + r["order"]) / 2 for r in rows.values()])),   # 470: the order judge and the combining unchanged
                combined=float(np.mean([r["combined"] for r in rows.values()])), content=float(np.mean([r["content"] for r in rows.values()])),
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
        R = {n["on"] - U: n.get("moved386", n["p"]) for n in notes if a2 <= n["on"] < b2}; S_ = {n["on"] - U0: n.get("moved386", n["p"]) for n in notes if a0 <= n["on"] < b0}   # 386 (Q1 A): read before its moves
        sh = sorted(set(R) & set(S_))
        if not sh: out.append(((sec, i, s0, i0, kind), False, "no shared events")); continue
        q4 = 0.75 * max(R)                                                             # read on the quarter 239 builds: the last quarter of the line's span
        keep = all(R[t] == S_[t] for t in sh if t < q4)
        if not keep:                                                                       # a reading: what changed early
            NB_ = {n["on"]: n for n in notes}
            for t in sh:
                if t < q4 and R[t] != S_[t]:
                    r_, s_ = NB_.get(t + U, {}), NB_.get(t + U0, {})
                    STATS["267: changed early, " + kind + (", the return's note a passing note" if r_.get("pass358") else "") + (", the source's note a passing note" if s_.get("pass358") else "")
                          + (", the return's note placed outside" if r_.get("outside") and not r_.get("pass358") else "") + (", the source's note placed outside" if s_.get("outside") and not s_.get("pass358") else "")] += 1
        lvl = (max(R[t] for t in sh) - min(R[t] for t in sh) <= NEAR_LEVEL) and (max(S_[t] for t in sh) - min(S_[t] for t in sh) <= NEAR_LEVEL)
        out.append(((sec, i, s0, i0, kind), keep or lvl, "kept" if keep else "near-level" if lvl else "changed early"))
    return out
# ---- 286: the seven unaudited gates join 277's count as soft limits, hard at the 1st or 99th ----
SPEC = SR["spectral reading (the engine's beta_pitch on Verse 1 then the first 8 bars of Chorus 1)"]
LIM7 = {"spectral": ("between", SPEC["soft limits (kept 5th, 95th)"], SPEC["hard limits (kept 1st, 99th)"]),
        "cmp": ("at least", L286["cmp"]["soft"], L286["cmp"]["hard"]), "memory": ("at least", 0.12, -1e9),                  # 373: memory soft 0.12, no hard limit
        "surprisal": ("at least", 0.24, 0.08),                                                                          # 382: read on the kept songs
        "rhythm band": ("between", [1.62, 3.38], [1.43, 3.61]),                                                          # 373: with the pooled kept table (372)
        "sequence legs": ("at most", L286["sequence legs"]["soft"], L286["sequence legs"]["hard"])}
LIM_CORPUS = {"spectral": "kept chart songs (286, Window 128)", "realness": "withdrawn; printed (300)", "rhythm band": "kept chart songs, the pooled kept table (373)",
              "memory": "kept chart songs (373)", "surprisal": "kept chart songs (382)", "cmp": "POP909 pairs; unchanged, 94% of kept songs pass (373)", "sequence legs": "a count (286)"}
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
DESIGN_GATES = ["design: 'blue movie' a falling sequence from the chorus's top; 'starring nobody but you' lifts back to it; the post-chorus chants the figure (Q15 A)"]
FIG_RH = [((0, 24, 30), 0.35), ((12, 24, 30), 0.30), ((18, 24, 30), 0.15), ((0, 24, 36), 0.20)]      # 'BLUE MO-vie': 'mo' on beat 1 or 3 (232)
FIG = {}
def sstep(p, k):
    """k scale steps from p (down when k < 0)."""
    q = p
    for _ in range(abs(k)):
        q += -1 if k < 0 else 1
        while q % 12 not in M.SCALE: q += -1 if k < 0 else 1
    return q
def design_line(rng, h, sec, i, U, meta, notes_on):
    """Q15 A. 'figure' (Chorus 1, line 3): the figure on 'blue movie', then again a scale step lower, from the chorus's top.
    'chant' (Post 1): 'blue, blue' on the figure's first pitch, then the figure; 'no one else in the' on its third, then the figure lower."""
    sy = LINES[sec][i]
    if h == "figure":
        xhi = meta["carriers"]["high"][1]; r_ = rng.choices([x for x, _ in FIG_RH], [w for _, w in FIG_RH])[0]
        for T in (xhi, sstep(xhi, -1), sstep(xhi, -2)):
            b1 = [T, sstep(T, -1), sstep(T, -2)]; b2 = [sstep(p, -1) for p in b1]
            ons = [U + o for o in r_] + [U + BAR + o for o in r_]
            if not any(tri(p, M.chord_at(t)) for p, t in zip(b1 + b2, ons)): break
            STATS["design: figure moved below the top (a tritone from the root)"] += 1
        FIG.clear(); FIG.update(r=r_, T=T, b1=b1, b2=b2)
        return [dict(on=t, p=p, syl=k, slur=False, stress=sy[k][1]) for k, (t, p) in enumerate(zip(ons, b1 + b2))]
    r_, b1, b2 = FIG["r"], FIG["b1"], FIG["b2"]
    if i == 0: pre, cp, fig = [0, 24], b1[0], b1                                              # 'Blue, blue,' | 'blue movie'
    else: pre, cp, fig = [12, 18, 24, 30, 36], b1[2], b2                                       # 'no one else in the' | 'blue movie', a step lower
    ons = [U + o for o in pre] + [U + BAR + o for o in r_]; ps = [cp] * len(pre) + fig
    assert len(ons) == len(sy), (sec, i, len(ons), len(sy))
    return [dict(on=t, p=p, syl=k, slur=False, stress=sy[k][1]) for k, (t, p) in enumerate(zip(ons, ps))]
def design_fails(c):
    """317: the writer's design, read on what is sung; outside 275, its pass rate printed."""
    notes = c["notes"]; f = {}; g = DESIGN_GATES[0]
    by = collections.defaultdict(list)
    for n in notes: by[n["line"]].append(n)
    fl, l3, p0, p1 = by.get("Chorus 1:2", []), by.get("Chorus 1:3", []), by.get("Post 1:0", []), by.get("Post 1:1", [])
    ch = [n for n in notes if n["sec"] == "Chorus 1"]
    if not (len(fl) == 6 and l3 and len(p0) >= 3 and len(p1) >= 3): f[g] = "missing"; return f
    U = line_start("Chorus 1", 2); r1 = [n["on"] - U for n in fl[:3]]; r2 = [n["on"] - U - BAR for n in fl[3:]]
    seq = r1 == r2 and all(sstep(a["p"], -1) == b_["p"] for a, b_ in zip(fl[:3], fl[3:]))
    top_ = max(n["p"] for n in ch); fall = fl[0]["p"] >= max(n["p"] for n in ch if n["line"] in ("Chorus 1:0", "Chorus 1:1")) and fl[0]["p"] >= top_ - 2
    lift = max(n["p"] for n in l3) == top_ and max(n["p"] for n in l3) >= fl[0]["p"]
    chant = [n["p"] for n in p0[-3:]] == [n["p"] for n in fl[:3]] and [n["p"] for n in p1[-3:]] == [n["p"] for n in fl[3:]] and \
            len({n["p"] for n in p0[:-3]}) == 1 and len({n["p"] for n in p1[:-3]}) == 1
    if not (seq and fall and lift and chant): f[g] = dict(seq=seq, fall=fall, lift=lift, chant=chant)
    return f
def design_reg(R_, info):
    """325: the figure falls three scale steps from the song's top inside the chorus's register."""
    lo, hi = info["song_lo"], info["song_hi"]; xhi = max(p for p in range(lo, hi + 1) if p % 12 in M.SCALE)
    return sstep(xhi, -3) >= lo
DESIGN_REG.append(("the figure's fall inside the song's range (Q15 A)", design_reg))
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
V119 = int(os.environ.get("ZE_STEP", "3"))                                             # v119: the fixes ported in three steps, runs between them
STEP119 = {f_: 1 for f_ in ("384", "385", "386", "387", "389", "394", "395")} | {f_: 2 for f_ in ("388",)} | {f_: 3 for f_ in ("398", "400", "390", "391", "392", "393", "424")}
def ON(f_): return STEP119.get(f_, 0) <= V119 and f_ not in OFF
FIX124 = ("405", "409", "412", "413", "414", "415", "428")                                  # v124 Run 1: the session's repairs (on unless ZE_OFF names one)
DIAG450 = os.environ.get("ZE_DIAG450") == "1"                                           # diagnostics only (song 45): 267 reads the bridge's G before the raise to G-sharp
CUR405 = [None]; DRAWN398 = [False]
V127 = int(os.environ.get("ZE_PART", "3"))                                              # v127 Run 2: the parts, runs between them
P127 = {f_: 0 for f_ in ("470", "471", "472", "473", "464", "459")} | {f_: 1 for f_ in ("434", "435")} | {f_: 2 for f_ in ("452", "455", "406", "465", "457", "458")} | {f_: 3 for f_ in ("408", "468", "467", "461", "456")}
def ON7(f_): return P127.get(f_, 0) <= V127 and f_ not in OFF
PICK108 = [None, None]
K435 = 0.75                                                                              # 435: the kept three in four
def calibrate(rng, n=30, rounds=6):                                                    # 357: up to six rounds
    """249: the knobs are set on this song so that a build aimed at its pool's medians reads near them."""
    log = []; lines_acc = []; big_prev = set(); pf_acc = []; v2_acc = []
    pairs = {"repeat": "repeat", "step": "step", "third": "third", "fourth_fifth": "fourth_fifth", "larger": "past_fifth", "ct_on": "chord_tones_on_beat",
             "ct_off": "chord_tones_off_beat", "on_tonic": "on_tonic", "on_third": "on_third", "on_fifth": "on_fifth", "turn": "turns_per_move",
             "beat3": "on_beat3", "beats24": "on_beats_2_4"}                                    # 365: gap8, gap4 and gap16 leave 249's aimed calibration (they stay at one)
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
            n6, r6, p6 = s16_shape(c2["notes"]); ua["_n6"].append(n6); ua["_r6"].append(r6)
            if ON("389"):
                for b_, (n_, r_) in s16_bands(c2["notes"], c2["meta"].get("drawable405") if ON("405") else None).items(): ua["_n6b" + b_].append(n_); ua["_r6b" + b_].append(r_)
                       # 355
            for s_ in ("Verse 1", "Chorus 1"):                                                             # 371: the unit returns as read
                f_ = win_feats(c2["notes"], BAR0[s_])
                for j_, (_src, _kp, m_) in UR_KEPT.items():
                    if f_ and np.isfinite(f_.get(m_, np.nan)) and not (ON("390") and c2["meta"].get("ur_given", {}).get(KIND[s_], {}).get(j_)): ua["_ur" + str(j_)].append(f_[m_])   # 390: read on the free units
            ua["_bits"].append(M.rhythm_bits(c2["notes"]))                                                 # 356
            for s_ in ("Verse 1", "Chorus 1"):
                f_ = win_feats(c2["notes"], BAR0[s_])
                for m_ in list(KEPT114) + list(GAPS) + ["notes_per_bar", "on_sixteenth", "distinct_durations"] + list(KEPT398) + ["turns_per_move"] + list(KEPT424):
                    if f_ and np.isfinite(f_.get(m_, np.nan)): ua[m_].append(f_[m_])
        row["338: unaimed builds read"] = k2
        row["372: knobs"] = {k_: round(LK[k_], 4) for k_ in GAPKNOBS}
        if ua:                                                                              # 341, 344-346: each knob toward its kept figure
            rd = {m_: (float(np.mean(ua[m_])) if ua.get(m_) else KEPT114[m_]) for m_ in KEPT114}
            tg = du_target(float(np.mean(ua["notes_per_bar"])))                              # 354: the four gaps toward the kept means for the density
            on16 = float(np.mean(ua["on_sixteenth"])) if ua.get("on_sixteenth") else KEPT355["on_sixteenth"]
            dd = float(np.median(ua["distinct_durations"])) if ua.get("distinct_durations") else 4.0; bits = float(np.median(ua["_bits"]))
            out356 = [m_ for m_, v_ in (("distinct_durations", dd), ("rhythm_bits", bits)) if not (MID356[m_][0] <= v_ <= MID356[m_][1])]
            if out356 and not STOP356 and "354" not in OFF:                                    # 356: the 354 knobs stop when either reading leaves the kept middle half
                STOP356.append(f"round {CAL_ROUNDS[0]}: {out356} outside the kept middle half (distinct lengths {dd}, rhythm bits {round(bits, 3)}); "
                               + ("a reading (387): no knob stops" if ON("387") else f"the 354 knobs stop at {[round(LK[k_], 3) for k_ in ('s16', 'g8', 'g4', 'glong')]}")); print(STOP356[-1])
            for kn_, m_, t_ in zip(("s16", "g8", "g4", "glong"), GAPS, tg):
                if (STOP356 and not ON("387")) or "354" in OFF: break                          # 387: the stop no longer moves or freezes a knob
                r_ = float(np.mean(ua[m_])) if ua.get(m_) else t_
                f_ = float(np.clip(max(0.01, t_) / max(0.01, r_), 0.6, 1.6))
                if kn_ == "s16" and f_ > 1.0 and on16 > KEPT355["on_sixteenth"]: f_ = 1.0         # 357: s16 aimed with the onsets on a sixteenth
                if f_ in (0.6, 1.6): full_now.add(kn_)
                LK[kn_] = float(np.clip(LK[kn_] * f_, 0.05, 5.0))
            if "348" not in OFF:                                                             # 366: the run rate; 355: the sixteenth-onset knob
                ir = sum(ua["_r6"]) / max(1, sum(ua["_n6"]))
                if not ON("389"):
                    f_ = float(np.clip(KEPT355["in_runs"] / max(0.02, ir), 0.6, 1.6)); LK["run"] = float(np.clip(LK["run"] * f_, 0.0, 1.0))   # a rate, at most one
                    if f_ in (0.6, 1.6) and 0.0 < LK["run"] < 1.0: full_now.add("run")
                else:                                                                        # 389: a rate for each band, toward its kept share
                    rb_ = {}
                    for b_ in RUNR:
                        n_ = sum(ua.get("_n6b" + b_, [])); r_ = sum(ua.get("_r6b" + b_, []))
                        if n_ < 30: continue
                        f_ = float(np.clip(RUN_KEPT_BAND[b_] / max(0.02, r_ / n_), 0.6, 1.6)); RUNR[b_] = float(np.clip(RUNR[b_] * f_, 0.0, 1.0))
                        if f_ in (0.6, 1.6) and 0.0 < RUNR[b_] < 1.0: full_now.add("run " + b_)
                        rb_[b_] = (RUN_KEPT_BAND[b_], round(r_ / n_, 3), round(RUNR[b_], 3))
                    row["389 (band: kept, unaimed reading, rate)"] = rb_
                f_ = float(np.clip(KEPT355["on_sixteenth"] / max(0.01, on16), 0.6, 1.6)); LK["on16"] = float(np.clip(LK["on16"] * f_, 0.05, 5.0))
                if f_ in (0.6, 1.6): full_now.add("on16")
                row["355 (kept, unaimed reading, knob)"] = dict(in_runs=(0.31, round(ir, 3), round(LK["run"], 3)), on_sixteenth=(0.094, round(on16, 3), round(LK["on16"], 3)))
            if "371" not in OFF:                                                             # 371: the unit-return rates toward the kept readings
                for j_, (_src, kp_, m_) in UR_KEPT.items():
                    if ua.get("_ur" + str(j_)):
                        rd_u = float(np.mean(ua["_ur" + str(j_)])); f_ = float(np.clip(max(0.02, kp_) / max(0.02, rd_u), 0.6, 1.6))
                        UR_RATE[j_] = float(np.clip(UR_RATE[j_] * f_, 0.0, 1.0))
                row["371 (kept, unaimed reading, rate)"] = {UR_KEPT[j_][2]: (UR_KEPT[j_][1], round(float(np.mean(ua["_ur" + str(j_)])), 3) if ua.get("_ur" + str(j_)) else None, round(UR_RATE[j_], 3)) for j_ in UR_KEPT}
            row["356 (middle half, unaimed reading)"] = dict(distinct_durations=(MID356["distinct_durations"], dd), rhythm_bits=(tuple(round(x, 3) for x in MID356["rhythm_bits"]), round(bits, 3)))
            row["354 (band target, unaimed reading, knob)"] = {m_: (t_, round(float(np.mean(ua[m_])), 3) if ua.get(m_) else None, round(LK[k_], 3)) for k_, m_, t_ in zip(("s16", "g8", "g4", "glong"), GAPS, tg)}
            LK["ctl"] = float(np.clip(LK["ctl"] * np.clip((KEPT114["chord_tones_on_long_notes"] / max(0.05, rd["chord_tones_on_long_notes"])) ** 2, 0.6, 2.0), 0.5, 8.0))
            LK["offb"] = float(np.clip(LK["offb"] * np.clip(KEPT114["on_offbeat_eighth"] / max(0.05, rd["on_offbeat_eighth"]), 0.6, 1.6), 0.3, 3.0))
            LK["dpk"] = float(np.clip(LK["dpk"] * np.clip((rd["distinct_pitches"] / KEPT114["distinct_pitches"]) ** 2, 0.6, 2.0), 0.5, 8.0))
            if ON("398"):                                                                     # 398: each rate toward its kept mean by one knob on unaimed builds
                for kn_, m_ in (("ct398", "chord_tones"), ("ctb398", "chord_tones_on_beat"), ("ctd398", "chord_tones_on_downbeat"), ("res398", "non_chord_resolved_by_step")):
                    if not ua.get(m_): continue
                    r_ = float(np.mean(ua[m_])); f_ = float(np.clip((max(0.02, KEPT398[m_]) / max(0.02, r_)) ** 2, 0.6, 1.6)); LK[kn_] = float(np.clip(LK[kn_] * f_, 0.1, 10.0))
                    if f_ in (0.6, 1.6): full_now.add(kn_)
                row["398 (kept, unaimed reading, knob)"] = {m_: (KEPT398[m_], round(float(np.mean(ua[m_])), 3) if ua.get(m_) else None, round(LK[kn_], 3)) for kn_, m_ in (("ct398", "chord_tones"), ("ctb398", "chord_tones_on_beat"), ("ctd398", "chord_tones_on_downbeat"), ("res398", "non_chord_resolved_by_step"))}
            if ON("424"):                                                                     # 424: toward the pooled kept means
                for kn_, m_ in (("ff424", "fourth_fifth"), ("lt424", "last_note_tonic")):
                    if not ua.get(m_): continue
                    r_ = float(np.mean(ua[m_])); f_ = float(np.clip((max(0.02, KEPT424[m_]) / max(0.02, r_)) ** 2, 0.6, 1.6)); LK[kn_] = float(np.clip(LK[kn_] * f_, 0.1, 10.0))
                    if f_ in (0.6, 1.6): full_now.add(kn_)
                if ua.get("empty_bars") and not ON("428"):                                   # 428: empty bars are not aimed
                    r_ = float(np.mean(ua["empty_bars"])); f_ = float(np.clip(max(0.02, KEPT424["empty_bars"]) / max(0.02, r_), 0.6, 1.6)); LK["eb424"] = float(np.clip(LK["eb424"] * f_, 0.0, 1.0))
                    if f_ in (0.6, 1.6) and 0.0 < LK["eb424"] < 1.0: full_now.add("eb424")
                row["424 (pooled kept, unaimed reading, knob)"] = {m_: (KEPT424[m_], round(float(np.mean(ua[m_])), 3) if ua.get(m_) else None, round(LK[k_], 3)) for k_, m_ in (("ff424", "fourth_fifth"), ("lt424", "last_note_tonic"), ("eb424", "empty_bars"))}
            if ON("400") and ua.get("turns_per_move"):                                        # 400: turns per move toward the kept 0.58 by one knob on unaimed builds
                r_ = float(np.mean(ua["turns_per_move"])); f_ = float(np.clip((KEPT400 / max(0.05, r_)) ** 2, 0.6, 1.6)); LK["turn400"] = float(np.clip(LK["turn400"] * f_, 0.1, 10.0))
                if f_ in (0.6, 1.6): full_now.add("turn400")
                row["400 (kept, unaimed reading, knob)"] = (KEPT400, round(r_, 3), round(LK["turn400"], 3))
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
                if (p == "C" or ON("400")) and kn == "turn": continue                          # 304; 400: one knob, on unaimed builds
                if ON("398") and kn in ("ct_on", "ct_off"): continue                            # 398: one knob a measure
                if ON("424") and kn == "fourth_fifth": continue                                  # 424: one knob, on unaimed builds                                         # 304
                rd_ = float(np.mean(acc[p][kn])) if acc[p][kn] else MED[p][m]; tg = MED[p][m]
                KNOBS[p][kn] = float(np.clip(KNOBS[p][kn] * (max(0.02, tg) / max(0.02, rd_)) ** 1.0, 0.02 if kn == "gap16" else 1 / 3, 3))   # held to a third..three times, so a reading the design forces cannot starve the walk
                row[f"{p}:{kn}"] = (round(tg, 3), round(rd_, 3), round(KNOBS[p][kn], 3))
        full_prev = full_now; row["357: knobs at full step"] = sorted(full_now)
        log.append(row)
    return log

if __name__ == "__main__":
    import time; T0 = time.time()
    N = _N; SEED = 20261110 + 443
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
        c["judge"] = judge(c["notes"]); rec["judge"] = {k: c["judge"][k] for k in ("combined", "content", "order", "refit_content", "refit_combined")}
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
    if ON7("472"):                                                                          # 472: the refit's first among survivors with no soft break
        byr = sorted(alive, key=lambda c: (-c["judge"]["refit_combined"], c["fp"])); clean_r = [c for c in byr if not c["info"]["soft"]]
        old_ = pick; pick = clean_r[0] if clean_r else (byr[0] if byr else None)
        rk_ = lambda L, c: next((j_ + 1 for j_, x_ in enumerate(L) if c is not None and x_["fp"] == c["fp"]), None)
        PICK108[0] = old_; PICK108[1] = dict(v108_pick=old_["fp"] if old_ else None, refit_pick=pick["fp"] if pick else None, v108_pick_rank_under_refit=rk_(clean_r, old_),
                                             refit_pick_rank_under_v108=rk_(clean, pick), clean=len(clean_r))
        print("472:", PICK108[1])
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
    code = hashlib.sha1(open(__file__, "rb").read() + open(f"{H114}/lyric_p43.py", "rb").read() + open(f"{HERE}/judges.py", "rb").read()
                        + open("/home/claude/p36/melody_p36.py", "rb").read()).hexdigest()[:12]
    rerun = dict(seed=SEED, calibration_seed=SEED + 1, N=N, mode=MODE, code_sha=code, pythonhashseed=os.environ.get("PYTHONHASHSEED"), python=platform.python_version(),
                 numpy=np.__version__, tables={f: hashlib.sha256(open(f"{HERE}/tables/{f}", "rb").read()).hexdigest()[:16] for f in sorted(os.listdir(f"{HERE}/tables"))},
                 limits286=hashlib.sha256(open(f"{HERE}/limits286.json", "rb").read()).hexdigest()[:16],
                 cmd=f"PYTHONHASHSEED=0 python3 melody_v127_p43.py {N} {MODE}", line_knobs=dict(LK), near_level=NEAR_LEVEL)
    rerun["calibration_stop"] = list(CAL_STOP); rerun["frozen"] = sorted(FROZEN); rerun["rate293"] = RATE293[0]
    rerun["calibration_rounds"] = CAL_ROUNDS[0]; rerun["stop356"] = list(STOP356); rerun["off"] = sorted(OFF)
    rerun["knobs398_400"] = {k_: round(LK[k_], 4) for k_ in ("ct398", "ctb398", "ctd398", "res398", "turn400")}
    rerun["v127_part"] = V127; rerun["v127_on"] = sorted(f_ for f_ in P127 if ON7(f_))
    rerun["v124"] = [f_ for f_ in FIX124 if ON(f_)]; rerun["diag450"] = DIAG450
    rerun["knobs424"] = {k_: round(LK[k_], 4) for k_ in ("ff424", "lt424", "eb424")}; rerun["kept424"] = KEPT424
    rerun["v119_step"] = V119; rerun["fixes_on"] = sorted(f_ for f_ in STEP119 if ON(f_)); rerun["pin388"] = PIN388
    rerun["run_rates389"] = dict(kept=RUN_KEPT_BAND, rate={b_: round(v_, 4) for b_, v_ in RUNR.items()}, pooled_table_reading=round(RUN_POOLED, 3))
    rerun["tables118"] = {f: hashlib.sha256(open(f"{H118}/tables/{f}", "rb").read()).hexdigest()[:16] for f in sorted(os.listdir(f"{H118}/tables"))}
    rerun["knobs372"] = {k_: dict(final=round(LK[k_], 4), past_a_factor_of_two=bool(LK[k_] > 2.0 or LK[k_] < 0.5)) for k_ in GAPKNOBS}
    rerun["unit_return_rates371"] = {UR_KEPT[j_][2]: round(UR_RATE[j_], 4) for j_ in UR_KEPT}
    rerun["limits"] = {k_: dict(rule=LIM7[k_], corpus=LIM_CORPUS[k_]) for k_ in LIM7} | {"realness": dict(rule="printed", corpus=LIM_CORPUS["realness"])}
    rerun["section_bands372"] = {s_: (round(SEC_NPB[s_], 2), SEC_BAND[s_]) for s_ in SUNG}
    print("372: gap knobs", {k_: (round(LK[k_], 3), "PAST A FACTOR OF TWO" if (LK[k_] > 2.0 or LK[k_] < 0.5) else "") for k_ in GAPKNOBS}, "| 371: rates", rerun["unit_return_rates371"])
    print("rerun:", rerun)
    pickle.dump(dict(would=would, deaths=deaths, made=made, survivors=len(alive), order_fp=order, alive=alive[:80], short=[c["fp"] for c in short],
                     pick=pick, pick_v108=PICK108[0], pick_ranks=PICK108[1], pick_352=pick_352, clean=len(clean), pick_255=pick_255, pick_old_fit=pick_old, comp_first=alive[0] if alive else None, judge_first=byj[0] if byj else None, all=allb, every=every, stats=dict(STATS),
                     calibration=cal_log, knobs=KNOBS, line_knobs=dict(LK), rerun=rerun, form=FORM, chords=CHORD,
                     all_alive=[(c["fp"], c["judge"]["combined"], c["judge"]["content"], c["judge"]["order"], c["meas"]["composite"], c["meas"]["composite_old_fit"]) for c in alive]),
                open(f"{H118}/melody_v127_p43_{MODE}{_TAG}.pkl", "wb"))
