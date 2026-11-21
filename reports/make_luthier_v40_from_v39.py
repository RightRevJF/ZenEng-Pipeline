import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v39.docx")
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










RT = "/home/claude/rightrevjf/zeneng-pipeline/"; J = lambda p: json.load(open(RT + p)); RM = J("studies/rhythm_memory/result.json"); LR = J("studies/lyric_room/result.json"); S = LR["songs"]; CA = RM["carries"]
l3 = lambda v: ", ".join(str(x) for x in v); pc = lambda x: f"{100 * x:.0f}"; T3 = ("55", "54", "58"); T5 = ("55", "54", "58", "59", "60"); SLOW, SIL, NEAR, FAR = "slow change in how busy the singing is", "silence", "near answers", "far returns"
sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v39")], "Luthier v39", "Luthier v40")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 39"))], "LUTHIER — VERSION 39", "LUTHIER — VERSION 40")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("196 Windows", "197 Windows"), ("Windows 1–196", "Windows 1–197"), ("196 scientific research windows", "197 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v211 (Luthier v40)")
set_cell(row.cells[1], f"THE LYRIC'S ROOM. Window 196 left one fault plain: every Luthier song's rhythm scaling is low. A study, its rule written first, asked what gives a kept song's rhythm its long memory (studies/rhythm_memory). Two things carry it: slow change in how busy the singing is (+{CA[SLOW]['rank_correlation']}) and bars in which nothing is sung (+{CA[SIL]['rank_correlation']}). Where a bar's rhythm comes back from, near or far, does not ({CA[NEAR]['rank_correlation']}, +{CA[FAR]['rank_correlation']}): my guess after Window 195 and the session's 749.123 were both wrong. Luthier's three practice songs sing at one busyness all through, and two of them rest too little; the hold-out, with long verse lines against short chorus lines and an eight-bar break, stands with the kept songs on both and on rhythm scaling. Part of the fault is in the words: songs 54 and 58 run 307 and 337 seconds, and a lyric that fills every bar cannot be given a kept song's rhythm by any setting. 945: a check of the lyric's room, run when a lyric is locked and before any music (lib/luthier/lyric_room.py). It passed its rule: it agrees with the long way in eight verdicts of eight, it answers to the words, and it takes two minutes. No song and no record changes. The engine's side of the fault, sections that differ in how busy they are, is the next trial.")
after_par("27.120", [
    (f" The lyric's room (Window 197; Table HG; lib/luthier/lyric_room.py; tables/kept_rhythm_room.json; studies/rhythm_memory, studies/lyric_room). THE CHECK (945): when a lyric is locked, with the mouth tests and before any music, the song is laid out as the engine will lay it out and forty quick tunes are drawn; no pick is made and nothing is kept but the reading (lyricNN.room.json). Three things are read as sung and set against the kept 4/4 songs: room, the share of bars between the first and last sung note in which nothing is sung (kept quartiles 0.12, 0.19, 0.28); contrast, the spread across windows of four bars of onsets a bar, over the mean (0.34, 0.42, 0.56); and rhythm scaling (0.61, 0.66, 0.72). Where room or contrast stands under the kept 25th the check says so in plain words and names what in the lyric is behind it: the song's length against its sung bars, and the verse's lines against the chorus's. It advises; it does not refuse a lyric. python3 lib/luthier/lyric_room.py songs/pNN/lyricNN.json.", "27.121"),
])
P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 197: THE LYRIC'S ROOM", H1)
W("What gives a kept song's rhythm its long memory", H2)
W(f"With the draw gone (Window 196) every Luthier song showed the same fault at once: its rhythm scaling is low. Rhythm scaling lays the sung tune's onsets on a grid of sixteenths through the whole song, silences included, and asks how far the density of onsets keeps its memory across longer and longer spans. A high reading means stretches where the voice is busy and stretches where it is sparse or silent, lasting many bars. The rule was written first (studies/rhythm_memory/PREDICTION.md), and with it what had been looked at beforehand. Four things that might carry rhythm scaling were read on the {RM['kept_songs']} kept songs. Slow change in how busy the singing is carries it: a rank correlation of +{CA[SLOW]['rank_correlation']}. Bars in which nothing is sung carry it: +{CA[SIL]['rank_correlation']}. A bar's rhythm answered within the eight bars before does not ({CA[NEAR]['rank_correlation']}); nor does a rhythm returning from more than sixteen bars back (+{CA[FAR]['rank_correlation']}). After Window 195 I had written that the engine's way of repeating was the thing to study, and the session's 749.123 had named near against far repeats as the likely cause. Both were wrong. It is not how a song repeats. It is whether the voice changes its pace and stops.")
W(f"On the two things that carry it, the builds of songs 55, 54 and 58 stand at {l3([RM['luthier'][k]['medians'][SLOW] for k in T3])} for slow change (kept quartiles {l3(CA[SLOW]['kept_quartiles'])}), all three under the kept 25th, and at {l3([RM['luthier'][k]['medians'][SIL] for k in T3])} for silence (kept {l3(CA[SIL]['kept_quartiles'])}), two of the three under. The hold-out answers without being asked: song 59 stands at {RM['luthier']['59']['medians'][SLOW]} and {RM['luthier']['59']['medians'][SIL]}, in the kept middle on both, and its rhythm scaling, {RM['luthier']['59']['medians']['rhythm_scaling']}, is in the kept middle too. It is the one song of the four with long verse lines against short chorus lines and an eight-bar break.")
W("Whose fault it is", H2)
W("Two things make Luthier's songs so. The engine gives every line a slot of about the same length and fills it at about the same rate, verse and chorus alike: that is the engine's, and it is the next trial. And the words: songs 54 and 58 have four and three verses of eight lines and run 307 and 337 seconds, against 243 for the kept upper quartile, so there is no bar left in which nobody sings; and in songs 55, 54 and 58 the verse's lines and the chorus's are near one length. A lyric that fills every bar at one pace cannot be given a kept song's rhythm by any setting. That has to be caught while the words can still change.")
W("The check of the lyric's room (945)", H2)
W(f"So a check was built for the moment a lyric is locked, beside the mouth tests and before any music is written. It lays the song out as the engine will, draws forty quick tunes with no pick made, reads room, contrast and rhythm scaling as sung, and says in plain words what in the lyric is behind a low reading. Its rule was written before it was run (studies/lyric_room/PREDICTION.md). It agrees with the long way: on songs 55, 54, 58 and 59 its verdicts on room and on contrast are the rhythm study's in {LR['checks']['1 agrees with the long way (of 8)']} cases of eight. It answers to the words: cut to its first two verses and choruses, song 54's lyric reads {S['54 cut']['readings']['room']} of its bars unsung where the whole lyric reads {S['54']['readings']['room']}, and its contrast rises from {S['54']['readings']['contrast']} to {S['54 cut']['readings']['contrast']}, for a shorter song is given a turn and a break. And it is quick, about two minutes a lyric. It passed and is added to what is run when a lyric is locked. Song 60, which no study had read, has room and contrast in its words ({S['60']['readings']['room']} and {S['60']['readings']['contrast']}) and a rhythm scaling of {S['60']['readings']['rhythm_scaling']}, in the kept middle, with nothing done to the engine.")
for n_, title_, test_ in (("945", "A check of the lyric's room", "Test: its verdicts on room and contrast match the rhythm study's in at least seven of eight cases on songs 55, 54, 58 and 59: eight. Song 54 cut to two verses reads at least 0.03 more room: 0.07. Under five minutes a lyric: two."),):
    W(f"{n_} {title_}", H2); W(test_)
W("Table HG — the lyric's room on the five songs (kept quartiles in the head).")
rows = [("", "Bars with nothing sung (0.12, 0.19, 0.28)", "Change in how busy the singing is (0.34, 0.42, 0.56)", "Rhythm scaling (0.61, 0.66, 0.72)", "Syllables a line: verse; chorus")]
for k, nm in (("55", "Song 55"), ("54", "Song 54"), ("58", "Song 58"), ("59", "Song 59 (hold-out)"), ("60", "Song 60"), ("54 cut", "Song 54, cut to two verses")):
    rows.append((nm, S[k]["readings"]["room"], S[k]["readings"]["contrast"], S[k]["readings"]["rhythm_scaling"], f"{S[k]['syllables_a_line']['verse']}; {S[k]['syllables_a_line']['chorus']}"))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W("The records. No song and no record changes in this window; the engine builds as Window 196 left it. One kept table is added (kept_rhythm_room.json), and each 4/4 lyric has its reading beside it (lyricNN.room.json).")
W("What this window could not do. The engine's side is untouched: every line is still given much the same slot and filled at much the same rate, so a lyric with room and contrast in its words gets a kept song's rhythm and a lyric without them does not. Letting sections differ in how busy they are, a chorus of held notes against a verse of quick ones, and keeping bars of rest between sections, is the next trial, with its own rule. Until then repetition from the words (Window 196) still cannot be acted on. The check advises and does not refuse; songs 55, 54 and 58 stand as written. The songwriting session's list for Window 196 (749.123 to 749.127) is still unanswered; this window shows 749.123's cause to be otherwise than it named.")
W("")
for lead in ("WINDOW 197", "27.121", "Table HG", "945 A check"):
    assert any(p_.text.strip().startswith(lead) or lead in p_.text[:40] for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v40.docx"); print("saved Luthier_v40.docx")
