import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v44.docx")
P = d.paragraphs


def set_text(par, new):
    runs = par.runs
    if not runs: par.add_run(new); return
    runs[0].text = new
    for r in runs[1:]: r.text = ""


def sub(par, old, new):
    if old not in par.text: raise SystemExit(f"not found: {old!r} in {par.text[:60]!r}")
    for r in par.runs:
        if old in r.text: r.text = r.text.replace(old, new); return
    set_text(par, par.text.replace(old, new))


def set_cell(cell, new):
    set_text(cell.paragraphs[0], new)
    for extra in cell.paragraphs[1:]: set_text(extra, "")


def find_par(pred):
    for i, p in enumerate(d.paragraphs):
        if pred(p): return i
    raise SystemExit("paragraph not found")


def tbl_by_first(label):
    for t in d.tables:
        try:
            if t.rows[1].cells[0].text.strip() == label: return t
        except Exception: continue
    raise SystemExit(f"table not found: {label}")


H1 = next(p.style for p in P if p.style.name == "Heading 1")
H2 = next(p.style for p in P if p.style.name == "Heading 2")
BODY = P[find_par(lambda p: p.text.startswith("Information Content (IC) is how surprising"))].style


def before(anchor, text, style=BODY, lead=None):
    p = anchor.insert_paragraph_before("", style=style)
    if lead: p.add_run(lead).bold = True
    p.add_run(text); return p


def fill_table(T, rows):
    while len(T.rows) > 1: T._tbl.remove(T.rows[-1]._tr)
    hdr = T.rows[0]
    while len(hdr.cells) < len(rows[0]): hdr._tr.append(copy.deepcopy(hdr.cells[-1]._tc))
    while len(hdr.cells) > len(rows[0]): hdr._tr.remove(hdr.cells[-1]._tc)
    grid = T._tbl.tblGrid
    while len(grid) < len(rows[0]): grid.append(copy.deepcopy(grid[-1]))
    while len(grid) > len(rows[0]): grid.remove(grid[-1])
    for ci, v in enumerate(rows[0]): set_cell(hdr.cells[ci], v)
    for r in rows[1:]:
        T._tbl.append(copy.deepcopy(hdr._tr)); cells = T.rows[-1].cells
        for ci, v in enumerate(r):
            set_cell(cells[ci], v)
            for pp in cells[ci].paragraphs:
                for run in pp.runs: run.bold = False
                pp.style = BODY if ci else pp.style


def table_before(anchor, rows):
    src = tbl_by_first("β_pitch")
    tbl = copy.deepcopy(src._tbl); anchor._p.addprevious(tbl)
    fill_table(Table(tbl, anchor._parent), rows)


def after_par(prefix, paras):
    P_ = d.paragraphs
    i = next((k for k, p in enumerate(P_) if p.text.strip().startswith(prefix)), None)
    if i is None: raise SystemExit("after_par anchor missing: " + prefix)
    if P_[i].style.name.startswith("Heading"):
        j = i + 1
        while j < len(P_) and not P_[j].style.name.startswith("Heading"): j += 1
    else: j = i + 1
    anc = P_[j]
    for text, lead in paras: before(anc, text, BODY, lead)










RT = "/home/claude/rightrevjf/zeneng-pipeline/"; J = lambda p: json.load(open(RT + p)); import re, sys
sys.path[:0] = [RT + "lib/luthier", RT + "tables/metre_atlas"]; import lyric_room as LR
N5 = J("studies/soundness/neighbour_v45.json"); N4 = J("studies/soundness/neighbour_v44.json"); LV = J("studies/lever_range/result.json"); WA = J("studies/judging_checks/within_artist/result.json"); GP = J("studies/judging_checks/nights_1_2/gap.json")
S = {k: J(p) for k, p in (("55", "songs/p65/lyric55.song.json"), ("54", "songs/p64/lyric54.song.json"), ("58", "songs/p68/lyric58.song.json"), ("59", "songs/p69/lyric59.song.json"), ("60", "songs/p70/lyric60.v45.song.json"), ("49", "songs/p59/lyric49.song.json"), ("49w", "songs/p59/lyric49.without_958.song.json"))}
T5s = ("55", "54", "58", "60", "59"); T3 = ("55", "54", "58"); FN = [f"lyric{k}.json" for k in T3]; l3 = lambda v: ", ".join(str(x) for x in v); p1 = lambda x: round(100 * x, 1); PK = "the engine's pool"
def pool(N): return dict(nc=N["neighbour"]["rule_fails_share"], rp=[x["rule_fails_share"] for k, x in N["a_random_pick_from"].items() if k.startswith(PK)][0])
P5, P4 = pool(N5), pool(N4)
def find(o, k):
    if isinstance(o, dict):
        if k in o: return o[k]
        for v in o.values():
            r = find(v, k)
            if r is not None: return r
    return None
WF = {k: [v for kk, v in S[k]["checks"].items() if kk.startswith("the words' fit")][0] for k in S}; RG = {k: max(n["midi"] for n in S[k]["melody"]["notes"]) - min(n["midi"] for n in S[k]["melody"]["notes"]) for k in S}
RD = {k: LR.read([n["on"] for n in S[k]["melody"]["notes"]], 48) for k in S}; rs = lambda k: round(RD[k]["rhythm_scaling"], 3); rm = lambda k: round(RD[k]["room"], 3); BF = {k: find(S[k], "words_gate")["the_builds_median_fit"] for k in S}
SEC = {k: round(sum(b for _, _, b in S[k]["form"]) * 240 / S[k]["bpm"]) for k in S}; X = lambda N, c: [N["749.140"][c][f] for f in FN]; low = lambda N: N["pool_share_outside_middle_half_by_check"]["rhythm scaling"]["low"]
vr = lambda n, b=None: round(100 * (LV["verse"][str(n)]["one_bar_or_less"] if b is None else LV["verse"][str(n)]["by_tempo"][b]["one_bar_or_less"])); MID, SLOW, FAST = "middle", "slow (bar 2.6 s or more)", "fast (bar under 1.8 s)"
sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v44")], "Luthier v44", "Luthier v45")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 44"))], "LUTHIER — VERSION 44", "LUTHIER — VERSION 45")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("201 Windows", "202 Windows"), ("Windows 1–201", "Windows 1–202"), ("201 scientific research windows", "202 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v216 (Luthier v45)")
set_cell(row.cells[1], f"THE VERSE SUNG CLOSER, BUILT; A HOLD-OUT THAT DISAGREES. The songwriting session's Review 29 ruled that Window 201's form be built, with the words' check moved to the chosen tune. 958 (749.142): in 4/4, verse lines of 6 to 8 syllables that would take two bars take one, the shortest first, none side by side, an even count, to the kept middle of notes a bar. On songs 55, 54 and 58 every check written first is met: the builds' rhythm scaling {l3(X(N5, 'living_median_rhythm_scaling'))} ({l3(X(N4, 'living_median_rhythm_scaling'))} before; kept quartiles 0.605 to 0.721); the chosen tunes' words' fit {l3([WF[k] for k in T3])} (0.341, 0.275, 0.307 before); the three chosen tunes sound with no lean for the first time; the pools fail the soundness rule {p1(P5['rp'])} times in a hundred. 749.143: song 49 is made a second hold-out by the session's rule and run without the form and with it. Its rhythm scaling rises ({rs('49w')} to {rs('49')}) and its bars of rest reach the kept range ({rm('49w')} to {rm('49')}), but its chosen tune's words' fit falls from {WF['49w']} to {WF['49']} and its builds' middle from {BF['49w']} to {BF['49']}. Its verses are 8-syllable lines; kept songs give an 8-syllable verse line one bar {vr(8)} times in a hundred and a 6-syllable line {vr(6)} (749.146, studied), and the form takes both alike. The form stands as the session ruled; the hold-out says its reach is too long, and that is put to the session. Also in this window, from the nightly judging research: the one note finding the project holds (songs whose chords loop less within a section are covered more) is tested with the artist held still, rule first, and holds narrowly ({WA['within_artist']['beta']:.3f}, p {WA['within_artist']['p']:.3f}, against −0.071 across artists).")
after_par("27.125", [
    (f" The verse sung closer, built (Window 202; Table HL; studies/busy_sections, studies/lever_range, studies/judging_checks). THE VERSE SUNG CLOSER (958): in plan(), for a song in 4/4, in each verse, the lines of 6 to 8 syllables that would take two bars are ordered shortest first; lines are taken in that order, none beside a line already given one bar, an even count, as many as bring the verse's syllables a bar nearest 4.59 (the kept middle for verses); each taken line is given one bar. The record names the lines (spec.verse_closer). A lyric may switch it off (\"verse_closer\": false). The planner's rules for breaks and turns then act on the shorter song. A SECOND HOLD-OUT: song 49 (songs/p59/lyric49.json, from its locked lyric word for word) is read after every change beside song 59 and is never fitted to.", "27.126"),
])
P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 202: THE VERSE SUNG CLOSER, BUILT", H1)
W("Window 201 found the engine's lever on rhythm scaling, the one check on which Luthier's songs leaned, and left it unbuilt: it missed, by 0.008, a check of mine on the words' fit of song 54's builds. The songwriting session ran the three songs in full under the form (Review 29) and ruled: build it, and judge the words on the tune that is chosen, since that is the tune a song gets. It added a hold-out the lever can act on. This window builds the form, reads both hold-outs, and reports what the new one says.")
W("The form built (958; 749.142)", H2)
W(f"The checks were the session's, written into the repository before the build was run. All are met on songs 55, 54 and 58. The builds' rhythm scaling stands at {l3(X(N5, 'living_median_rhythm_scaling'))}, inside the kept quartiles in two songs of three ({l3(X(N4, 'living_median_rhythm_scaling'))} before). The chosen tunes' words' fit is {l3([WF[k] for k in T3])} against 0.341, 0.275 and 0.307 before: none falls by more than 0.02, and song 58's rises. Builds that live: {l3(X(N5, 'living_builds'))} of a thousand ({l3(X(N4, 'living_builds'))} before). The three chosen tunes pass the soundness rule and, for the first time since the rule was written, lean on no check; 10 checks stand outside the kept middle half, against 12. A random pick from the pools fails the rule {p1(P5['rp'])} times in a hundred and the neighbour choice {p1(P5['nc'])} ({p1(P4['rp'])} and {p1(P4['nc'])} before). The chosen tunes keep the floor and the ceiling. Every figure matches the session's own run. Song 58's chosen tune stays under the kept 10th of rhythm scaling ({rs('58')} against 0.574): its lyric leaves little room, and the second carrier, bars with nothing sung, is the session's 749.144, not begun here. The form is held to 4/4, where its kept figures come from; song 52, in 6/8, is byte for byte as it was.")
W("Song 49, a hold-out the lever can act on (749.143)", H2)
W(f"Song 59, the hold-out since Window 191, has no verse line of 6 to 8 syllables, so no form could be tested on it; its notes are the same in this window, note for note. The session chose a second hold-out by a rule written before any run: the most recent song in 4/4 not yet run by this engine with at least four such verse lines. That is song 49, The World Is Asking. Its lyric file is made from the locked lyric word for word, with its tempo, genre and voice from its intake. It was run without the form and with it, and neither was seen before the checks were written.")
W(f"With the form, lines 1 and 3 of each verse take one bar. The chosen tune's rhythm scaling rises from {rs('49w')} to {rs('49')}, into the kept middle half, and its bars with nothing sung from {rm('49w')} to {rm('49')}, into the kept range (0.12 to 0.28): on a song nothing was fitted to, the lever does what it was built to do. But the chosen tune's words' fit falls from {WF['49w']} to {WF['49']}, where the fitted songs were allowed 0.02, and the builds' middle falls from {BF['49w']} to {BF['49']}. The chosen tune is one draw from a small pool, so its fall is noisy; the builds' fall of {round(BF['49w'] - BF['49'], 3)} is not, and it is larger than song 54's in Window 201 (0.028). The chosen tune is over the kept floor (0.152) and under the kept 25th (0.248). Its range also falls, from {RG['49w']} to {RG['49']} semitones, against an asking of 17.9 and a floor of 14.6. I had expected the words' fit to move by under 0.03 and was wrong.")
W(f"Song 49's verse lines are all of 8 syllables but one. Eight syllables in one bar are eighth notes end to end, with no long note for a weighty syllable. That is the case I raised in Window 201; the session set it aside because song 54's chosen tune did not show it, which was a fair reading of the songs then in hand. The hold-out shows it. By the rule written before the run, the form stands or falls on the session's reading of the hold-out, not mine, so 958 is built and stands for now. My reading is that the lever is right and its reach too long.")
W("How often kept lines take one bar (749.146)", H2)
W(f"The session asked, from song 61, whether the lever's range should widen past 8 syllables, by a rule: a line of n syllables may be taken if kept verse lines that long take one bar at least as often as 8-syllable lines do. Read on the transcribers' lyric lines of the kept songs (studies/lever_range): a kept verse line takes one bar or less {l3([vr(n) for n in range(3, 13)])} times in a hundred at 3 to 12 syllables. Lines of 9, 10 and 11 stand under the 8's {vr(8)}, so by the rule the range does not widen. At a slow tempo alone, lines of 10 and 11 stand over the slow 8 ({vr(10, SLOW)} and {vr(11, SLOW)} against {vr(8, SLOW)}), on 24 and 17 lines: too few to build on. The table says two things that were not asked. The form takes 8-syllable lines as readily as 6-syllable ones, and kept songs do not: {vr(6)}, {vr(7)}, {vr(8)} in a hundred at 6, 7 and 8 syllables ({vr(6, MID)}, {vr(7, MID)}, {vr(8, MID)} at a middle tempo; {vr(6, SLOW)}, {vr(7, SLOW)}, {vr(8, SLOW)} at a slow one). And at a fast tempo kept lines of 7 and 8 syllables almost never take one bar ({vr(7, FAST)} and {vr(8, FAST)} in a hundred), so there the form should hardly act; no song run so far is that fast. A first run of this study read the kept corpus's own line index, which marks longer phrases and not lyric lines, and gave false figures; it was caught before it was reported, and it is the same kind of fault as 749.128.")
W("One neighbour block read a study, not the table (749.145)", H2)
W("The block of neighbour.py that tried the ceiling took its figure from a study's result file, where the engine takes it from the kept table; when fix 957 remade the table the block's figure lagged. It now reads the table, and a rerun matches the committed file.")
W("From the judging research: chords that move, with the artist held", H2)
W(f"The writer has set up a nightly research task on judging music by its notes; its first two nights were read in this window and their sources checked (studies/judging_checks). All eight papers exist and no figure that could be checked contradicts its source; three sets of figures could not be reached and are marked. The research's sharpest point was about the project's one note finding, that songs whose chords repeat less within a section are covered more (−0.124 and −0.071 on two cover sources): both results compare different artists' songs, so fame, voice, era and genre travel with the harmony. The test it named was run, with its rule committed before any cover count was on the machine: each artist's songs against that artist's own other songs. The covers study's figure was first reproduced on data fetched again (2,360 songs, −0.071). Within artists, on {WA['songs']:,} songs of {WA['artists']} artists, chord repetition against covers is {WA['within_artist']['beta']:.3f} (p {WA['within_artist']['p']:.3f}); the two halves of the artists give {WA['halves'][0]['beta']:.3f} and {WA['halves'][1]['beta']:.3f}. By the rule (−0.04 or stronger, p under .05, the same sign in both halves) it holds, by 0.002: the range runs from about −0.07 to −0.01, so it rules out no effect at all, and does not rule out a very small one. About four tenths of the across-artist figure was the artist's. Covers made early and late show it alike. The tune, again, shows nothing. Nothing of this is in the engine. It removes the main objection to a trial of sections that loop less in the chord writer, which is to be tried, rule first, in a later window. The research's spectral gap of a song's chord map was also built again from its written rules: its figures reproduce (−0.263 against repetition, where it reported −0.26), and its first half agrees with its second at {GP['split_half']['g']['rho']:.2f}, steadier than I expected.")
for n_, title_, test_ in (
    ("958", "The verse sung closer", "Test (the session's, written before the build): rhythm scaling of the builds inside the kept quartiles in two of songs 55, 54, 58; no chosen tune's words' fit more than 0.02 under the tune chosen without the form; 7 builds in 10 kept; the soundness rule and the pool standard; the guard; the floor and the ceiling. All met. The hold-outs are read and decide nothing: song 59 unchanged; song 49 gains in rhythm and loses 0.116 of its chosen tune's words' fit."),):
    W(f"{n_} {title_}", H2); W(test_)
W("Table HL — the verse sung closer: the chosen tunes (before; now), and the new hold-out without the form and with it.")
rows = [("", "Song 55", "Song 54", "Song 58", "Song 49 (hold-out): without; with")]
rows.append(("Rhythm scaling, the chosen tune (kept quartiles 0.605, 0.656, 0.721)", *[f"{rs(k)}" for k in T3], f"{rs('49w')}; {rs('49')}"))
rows.append(("Rhythm scaling, the builds' middle", *[f"{a}; {b}" for a, b in zip(X(N4, 'living_median_rhythm_scaling'), X(N5, 'living_median_rhythm_scaling'))], "not read"))
rows.append(("Words' fit, the chosen tune (kept floor 0.152, middle 0.318)", *[f"{a}; {WF[k]}" for a, k in zip((0.341, 0.275, 0.307), T3)], f"{WF['49w']}; {WF['49']}"))
rows.append(("Words' fit, the builds' middle", *[f"{a}; {b}" for a, b in zip(X(N4, 'living_median_words_fit'), X(N5, 'living_median_words_fit'))], f"{BF['49w']}; {BF['49']}"))
rows.append(("Bars with nothing sung, the chosen tune (kept quartiles 0.12, 0.19, 0.28)", *[f"{rm(k)}" for k in T3], f"{rm('49w')}; {rm('49')}"))
rows.append(("Range of the chosen tune, semitones", *[str(RG[k]) for k in T3], f"{RG['49w']}; {RG['49']}"))
rows.append(("Builds that live, of 1,000", *[f"{a}; {b}" for a, b in zip(X(N4, 'living_builds'), X(N5, 'living_builds'))], f"{S['49w']['melody']['survivors']}; {S['49']['melody']['survivors']}"))
rows.append(("Seconds", *[str(SEC[k]) for k in T3], f"{SEC['49w']}; {SEC['49']}"))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W(f"The records. Songs 55, 54 and 58 are written again and take new tunes; song 59's notes are unchanged; song 60 is read under this window as songs/p70/lyric60.v45.song.json and is unchanged in its notes (its verse lines run 10 to 12 syllables). Song 49 has two records: lyric49.song.json, with the form, and lyric49.without_958.song.json. Songs 52 and 53 are byte for byte as they were. Chosen tunes: range {l3([RG[k] for k in T5s])}, words' fit {l3([WF[k] for k in T5s])} (songs 55, 54, 58, 60, 59). One side effect to say plainly: the builds' middle range falls in song 55 from 17 to 15 semitones under the form, and song 55's chosen tune sits at the floor's edge. Both checks pass (song_from_lyric.py --check, lyric_room.py --check); every room file is read again, song 61's and song 49's among them.")
W("What this window could not do. The hold-out's verdict on the words' fit is not acted on: a form that takes lines by how often kept lines of that length take one bar at the song's tempo is the next trial, judged on songs 54 and 49. Song 58 is not mended (749.144, bars with nothing sung, not begun). 749.147 (a short line in a long slot holds its weak words) and the five hymn items (749.148 to 749.152) are not begun. The trial of sections that loop less, which the within-artist result now permits, is not begun.")
W("")
for lead in ("WINDOW 202", "27.126", "Table HL", "958 The verse"):
    assert any(p_.text.strip().startswith(lead) or lead in p_.text[:40] for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v45.docx"); print("saved Luthier_v45.docx")
