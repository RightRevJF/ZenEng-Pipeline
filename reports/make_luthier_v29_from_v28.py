"""Luthier v28 -> v29: a stated point at which the engine is sound (the session's 23 checks and one rule), and the one fault that stood between v28 and it
(Window 186, Module 27.110, Table GV; fixes 916-917). Evidence: lib/luthier/stage16_results.json, studies/soundness/, REVIEW_stage15.md, songs/p68/fixlist_v29.md.
Run: python3 make_luthier_v29_from_v28.py"""
import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v28.docx")
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










R = json.load(open("/home/claude/rightrevjf/zeneng-pipeline/lib/luthier/stage16_results.json")); SG = R["songs"]; K = R["kept"]; T3 = ("55", "54", "58"); l3 = lambda v: ", ".join(str(x) for x in v); pc = lambda x: f"{100 * x:.0f}"
rs = lambda w: l3([SG[k][w]["rhythm scaling"] for k in T3])

sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v28")], "Luthier v28", "Luthier v29")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 28"))], "LUTHIER — VERSION 28", "LUTHIER — VERSION 29")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("185 Windows", "186 Windows"), ("Windows 1–185", "Windows 1–186"), ("185 scientific research windows", "186 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v200 (Luthier v29)")
set_cell(row.cells[1], f"SOUND, BY A STATED RULE. The writer asked whether the engine would ever be debugged, and Window 185 closed on the want of a point at which it is called sound. The session has set one: 23 fixed checks, each read the same way on the 160 kept songs and on the three 4/4 songs, and a rule that reads a lean of the engine and not each song's place. The engine is sound when no check has all three songs past the kept 10th or 90th on one side, and no more than two have all three past the kept 25th or 75th. Three kept songs drawn at random fail it {pc(R['random_kept_fail_rate'])} times in a hundred. Version 28 failed on one check: rhythm scaling, under the kept 10th in all three songs, because fix 888 had taken out the turns in which the voice stops. The turns are kept at two bars whatever a song's length, and the bars in and out give way first. The rule now holds, narrowly: rhythm scaling stands at {rs('after')} against a kept 10th of {round(K['rhythm scaling'][0], 3)}, with one song over the bound by three thousandths. From here a finding is an improvement and not a fault, and the check runs after every version.")

after_par("27.109 The beat let go", [
    (" Sound, by a stated rule (Window 186; Table GV; studies/soundness/SOUNDNESS.md; songs/p68/fixlist_v29.md). THE TURNS STAY (916; answers 749.93; amends 877, 888): a song's turns are kept whatever its length, at two bars where the song would run past the kept 75th of lengths; the bars in and out are read again once the turns are in and take the kept lower quartiles before any turn is given up. THE STANDING TEST (917): studies/soundness/soundness.py is run on the three 4/4 records after every version. The engine is sound when no check of the 23 has all three songs beyond the kept 10th or 90th on the same side and no more than two have all three beyond the kept 25th or 75th. A finding made while the rule holds is an improvement, numbered as before and not owed before the next version.", "27.110"),
])

P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 186: SOUND, BY A STATED RULE", H1)
W("The rule (917)", H2)
W(f"Each of the last nine windows mended what the window before had been found to lack, and a review can always find a reading on which a song stands outside the kept middle half: a kept song stands outside it on about half of any set of readings, {l3([int(x) for x in R['per_kept_song_outside'][:3]])} of 21 by quartile. So the question is not whether every reading of every song is in the middle, which almost no kept song could pass, but whether the engine leans: whether all three songs fall on the same side of the same kept bound. One song outside is that song. Three on one side is the engine. The session set 23 checks (studies/soundness/SOUNDNESS.md): five of the words' placing and fit, six of rhythm, six of pitch, four of breath and line ends, and the chorus's lift and the rest share; every one is read on the notes as sung, on the kept songs and on the engine's alike. Its rule: no check with all three songs beyond the kept 10th or 90th on one side, and no more than two with all three beyond the kept 25th or 75th. Three kept songs drawn at random, twenty thousand times, fail the rule {pc(R['random_kept_fail_rate'])} times in a hundred. It is a bar the kept songs clear thirteen times in fourteen, and this paper adopts it as the session wrote it.")
W("The one check that failed (916)", H2)
W(f"Under version 28 one check failed the first half of the rule: rhythm scaling, at {rs('before')} against a kept tenth of {round(K['rhythm scaling'][0], 3)}. The session found what it follows. Across the kept songs rhythm scaling goes with how much the density of sung onsets changes from one four-bar stretch to the next (0.65), and with the stretches in which the voice does not sing at all (0.56): a kept song has a median of two silences of two bars or more, and one four-bar stretch in twelve with no sung note. The engine's three songs had none, one and none. Window 180 had taken the turns out of any song that ran past the kept lengths (888), and all three did; this paper said then that it cost the rhythm exponent and chose length. The session's reading is that the cost was the whole of the fault. The turns now stay, at two bars, and the bars in and out give way first. Song 55 keeps its length, {SG['55']['seconds']} seconds; songs 54 and 58 are four and five seconds longer, {SG['54']['seconds']} and {SG['58']['seconds']}.")
W(f"The rule now holds. It holds narrowly, and that is to be said plainly: rhythm scaling stands at {rs('after')}; two songs are still under the kept tenth and the third is over it by three thousandths. The engine still leans low on this check, which is one of the two leans the rule allows; the other is pitch scaling, high, which follows the large lifts two of the songs drew, as it does in kept songs. No check leans past the tenth or ninetieth. What would lift rhythm scaling off the bound is more of what kept songs have and these songs lack room for: a break, longer turns, lines that leave a bar empty. Two of the three lyrics are a minute too long for any of it.")
W("What the songs look like by the checks", H2)
W(f"Table GV gives the 23 checks. By song, {SG['55']['outside_middle_half'][1]}, {SG['54']['outside_middle_half'][1]} and {SG['58']['outside_middle_half'][1]} checks stand outside the kept middle half, where a kept song has {l3([int(x) for x in R['per_kept_song_outside'][:3]])} by quartile. The engine's songs sit nearer the middle than kept songs do. The session filed that as its second finding and named it an improvement, not a fault (749.94): every gate pulls a pick toward the kept middle, so the three songs are more like the median kept song than kept songs are like one another. It is the fault stage 7 found in the old judge, now measured in the engine's output. It is not mended here. It is the first improvement owed, and it is the door back to the question this work began with: a sound engine writes songs that are not wrong, and nothing in the 23 checks says which of them is good.")
for n_, title_, test_ in (
    ("916", "The turns stay, at two bars", "Test: each 4/4 song has a silence of two bars or more; rhythm scaling not under the kept 10th in all three (749.93's check)."),
    ("917", "The standing test of soundness", "Test: studies/soundness/soundness.py on the three 4/4 records reports the engine sound; run after every version.")):
    W(f"{n_} {title_}", H2); W(test_)
W("Table GV — the 23 checks of soundness: the kept songs (10th, 25th, median, 75th, 90th by song) and the three songs after this window (in: the middle half; near: between a quartile and the 10th or 90th; out: beyond).")
rows = [("Check", "Kept songs", "Song 55", "Song 54", "Song 58")]
for nm in K:
    f = lambda k: f"{SG[k]['after'].get(nm)} {SG[k]['places'].get(nm, '')}"
    rows.append((nm, l3([round(x, 3) for x in K[nm]]), f("55"), f("54"), f("58")))
rows.append(("Checks outside the middle half; outside the 10th to 90th", f"{l3([int(x) for x in R['per_kept_song_outside'][:3]])} (quartiles, of 21)", *[f"{SG[k]['outside_middle_half'][1]}; {SG[k]['outside_10_90'][1]}" for k in T3]))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W(f"What this window could not do. The rule holds by three thousandths on one song, and a rerun with another lyric could fail it; the standing test is there to say so. The rule is read on three songs of one writer in one metre. Song 52 in 6/8 has no kept pop corpus and stands outside it, as do the hymns. Songs 54 and 58 are past the kept lengths because their lyrics are. The old 4/4 judge's data is of the old parse. And soundness is likeness to kept songs without a lean: it is not worth. Of the writer's five ways to tell a great song by its notes, three have been tried and none ranks the kept songs; one reading, pitch scaling, kept a small relation to the chart record on songs it had not seen and has not been let to choose. The engine that this window calls sound still takes the first build past its gates.")
W("")
for lead in ("WINDOW 186", "27.110 Sound, by a stated rule", "Table GV", "917 The standing test"):
    assert any(p_.text.strip().startswith(lead) for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v29.docx"); print("saved Luthier_v29.docx")
