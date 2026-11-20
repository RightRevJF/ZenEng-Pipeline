"""Luthier v31 from v30: Window 188, Module 27.112 (the page gate, a floor; the song's own figures sung again). Fixes 922, 923. Table GX."""
import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v30.docx")
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










R = json.load(open("/home/claude/rightrevjf/zeneng-pipeline/lib/luthier/stage18_results.json")); SG = R["songs"]; BF = R["before"]; K = R["kept"]; EV = R["evidence"]; PL = R["pools"]; T3 = ("55", "54", "58"); l3 = lambda v: ", ".join(str(x) for x in v); pc = lambda x: f"{100 * x:.0f}"
KP = K["percentiles"]; mem = EV["memory_tried"]

sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v30")], "Luthier v30", "Luthier v31")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 30"))], "LUTHIER — VERSION 30", "LUTHIER — VERSION 31")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("187 Windows", "188 Windows"), ("Windows 1–187", "Windows 1–188"), ("187 scientific research windows", "188 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v202 (Luthier v31)")
set_cell(row.cells[1], f"THE PAGE GATE. A day of studies outside the engine asked what in a song's notes marks the songs that last, each test with its rule written first and judged on songs it had not seen (studies/). Among songs that are already hits, nothing in the written tune did. Where there is no recording and the forgotten are counted, the written tune does: a reader of plain page measures picks the session tunes players keep at +{EV['session_reader_unseen']} on {EV['session_tunes']:,} unseen tunes and the hymn tunes hymnals reprint at +{EV['hymn_reader_unseen']} on {EV['hymn_tunes']:,}, and inside one artist's work the charted songs are the plainer (+{EV['within_artist'][0]}, +{EV['within_artist'][1]}). It is a gate and not a grade. It enters the engine as a FLOOR (922): a build less plain than nine kept tunes in ten is passed over, after the words' gate; none of the songs' picks was near it. One part stood low in every song, the share of a tune's four-note figures it has already sung; a fresh line's notes now favour completing a figure the song has sung (923), which lifts the picks from {l3([BF[k]['page']['repeated_figures'] for k in T3])} to {l3([SG[k]['page']['repeated_figures'] for k in T3])} against a kept middle of {KP['repeated_figures'][2]}. The picks and the pools still pass the soundness rule ({pc(PL['v31']['pass_share'])} draws in a hundred). Fixes 922, 923. Table GX. Module 27.112. Window 188.")

after_par("27.111 Sound on the pools", [
    (f" The page gate, a floor (Window 188; Table GX; lib/luthier/page_gate.py; tables/kept_page_gate.json; studies/gates_strengthened, studies/luthier_on_the_page_gate). THE FLOOR (922): each build past the words' gate is read for the parts of the page gate against the kept 4/4 tunes: how hard its next interval is to foresee from the three before (bits, under the kept tunes' own counts), its share of notes on six and on five notes of the scale, its time on the tonic, how many different pitches and intervals it uses, its leaps, its range, its repeated notes, and the share of its four-interval figures already sung. Each is set against the kept mean and spread and turned the plain way; their mean is the build's plainness. A build under the kept 10th percentile ({round(K['floor'], 2)}) is passed over; if none is left the floor is waived and the record says so. It is a floor and not an aim: among songs already hits no part of it ranked anything. FIGURES SUNG AGAIN (923): when a fresh line's notes are drawn, a note that completes a four-interval figure the song has already sung, in the order sung, is favoured eightfold. Both are for 4/4 with the kept pop table; other metres are untouched. The record gives the gate's count, the builds' quartiles and the pick's parts, and the style checks give each part beside the share of kept tunes the song is plainer than.", "27.112"),
])

P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 188: THE PAGE GATE", H1)
W("What the studies found, and what they did not", H2)
W(f"Between Windows 187 and 188 the question of what makes a song last was taken outside the engine (studies/shape, arena, session_lab, hymn_lab, devotion, next_tests, transfer, gate, preordained_shape, combination, gates_strengthened; reports/Human preference and lasting music.md). The yardstick was Jason's: a song is great if it is still loved long after release and covered by many. Every test had its rule written before the data was read, and every measure was judged on songs it had not seen. Most failed, and the failures are of one kind: among songs that reached the Hot 100, nothing measured on the written tune or its chords tells the lasting from the rest. That covers repetition, contour, range, surprise, the scaling exponent, chord tones, form and some seven hundred further measures tried by six researchers on a locked half.")
W(f"Four things held. Two are in the recording and are not the engine's to write: lasting hits stand apart from the hits of the years before them, and they share a concentrated, still, uncrowded sound; a third, on which recordings listeners return to, is also in the sound. The fourth is on the page. Where there is no recording, no star and no chart, and the forgotten are counted with the kept, a reader of the written notes picks the Irish session tunes that players keep at +{EV['session_reader_unseen']} on {EV['session_tunes']:,} unseen tunes (its first form scored +{EV['first_session_reader']}), and the hymn tunes that hymnals reprint, from their opening notes alone, at +{EV['hymn_reader_unseen']} on {EV['hymn_tunes']:,}. Inside one artist's work the songs that charted are plainer than those that did not (+{EV['within_artist'][0]} and +{EV['within_artist'][1]}, artist held). The tunes that are kept have a next note easy to foresee, stay on five or six notes of the scale, come home to the tonic, use few different pitches and few leaps, and sing their own short figures again. Rhythm carries none of it.")
W("It is a gate and not a grade. The same reader, frozen, does not rank chart hits by how much they are covered or how long they are loved: every song on the chart is already through. It may measure ease of carrying rather than greatness. So it is used here as the engine's other floors are: to rule out, never to aim at.")
W("The floor (922)", H2)
W(f"The parts were read on the {K['songs']} kept 4/4 tunes (tables/kept_page_gate.json, made by lib/luthier/make_kept_page_gate.py, each kept tune's surprise read with its own counts taken out) and on the songs as Window 187 left them. As a whole the three songs stood plainer than {l3([BF[k]['place']['plainness'] for k in T3])} kept tunes in a hundred: clear of a floor at the kept 10th. A build past the words' gate is now read the same way and passed over if it falls under that floor. Of the builds read, {l3([str(SG[k]['page_gate']['passed']) + ' of ' + str(SG[k]['page_gate']['read']) for k in T3])} passed in songs 55, 54 and 58. The floor changes little today; it is there for the tune that would not be carried.")
W("The song's own figures, sung again (923)", H2)
W(f"One part stood low in every song. Of a kept tune's four-interval figures, {KP['repeated_figures'][2]} at the median are figures it has already sung (quartiles {KP['repeated_figures'][1]} and {KP['repeated_figures'][3]}); the three songs stood at {l3([BF[k]['page']['repeated_figures'] for k in T3])}, plainer than {l3([BF[k]['place']['repeated_figures'] for k in T3])} kept tunes in a hundred. The words are not the cause: the lyrics' lines match the syllable count of a neighbouring line as often as kept songs' lines do (the 49th to the 82nd place among them), and later verses and choruses return at 0.84 to 0.89 of their notes. The cause is in how fresh lines are drawn, note by note, with no memory of the figures already sung. A note that completes a four-interval figure the song has sung is now favoured. The weight was tried at 1, 4, 8 and 16 on song 55: the builds' median share rose from {mem['1'][1]} to {mem['4'][1]}, {mem['8'][1]} and {mem['16'][1]}; eight is kept, since sixteen adds nothing.")
W(f"With it the picks stand at {l3([SG[k]['page']['repeated_figures'] for k in T3])} ({l3([SG[k]['place']['repeated_figures'] for k in T3])} in a hundred), and every build of songs 55, 54 and 58 at medians of {l3([SG[k]['page_gate']['every_build_figures_again_quartiles'][1] for k in T3])}. The picks' next note is easier to foresee as well: surprise {l3([BF[k]['page']['surprise'] for k in T3])} bits before, {l3([SG[k]['page']['surprise'] for k in T3])} after, against a kept middle of {KP['surprise'][2]}.")
for n_, title_, test_ in (
    ("922", "The page gate, a floor", "Test: every pick's plainness at or over the kept 10th percentile; the record gives the gate's count and the pick's parts."),
    ("923", "A fresh line favours a figure already sung", "Test: the picks' share of four-interval figures already sung inside the kept middle half (0.470 to 0.676), the soundness rule still passed on the picks and on the pools.")):
    W(f"{n_} {title_}", H2); W(test_)
W("Table GX — the page gate on the kept 4/4 tunes and on the three songs, before (Window 187) and after (in brackets: the share of kept tunes the song is plainer than).")
names = (("plainness", "Plainness, all parts together"), ("surprise", "Surprise, bits per interval (lower is plainer)"), ("six_note_share", "Share of notes on six notes of the scale"), ("five_note_share", "Share on five notes of the scale"), ("time_on_tonic", "Time on the tonic"), ("different_pitches", "Different pitches, bits (lower is plainer)"), ("leaps", "Leaps (lower is plainer)"), ("range", "Range, semitones (lower is plainer)"), ("repeated_notes", "Repeated notes"), ("repeated_figures", "Four-interval figures already sung"))
rows = [("", "Kept 10th, middle, 90th", "55 before", "55 after", "54 before", "54 after", "58 before", "58 after")]
for c, nm in names:
    rows.append((nm, f"{KP[c][0]}, {KP[c][2]}, {KP[c][4]}", *[f"{d_[k]['page'][c]} ({d_[k]['place'][c]})" for k in T3 for d_ in (BF, SG)]))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W(f"The records. Songs 55, 54 and 58 are written again: keys {l3([SG[k]['key'] for k in T3])}; {l3([SG[k]['seconds'] for k in T3])} seconds. Their picks stand outside the kept middle half on {l3(R['outside_middle_half'])} checks of the 23 and pass the soundness rule; a pick drawn at random from each song's pool passes {pc(PL['v31']['pass_share'])} times in a hundred ({pc(PL['v30']['pass_share'])} before). Song 52, in 6/8, has no kept table for the gate and is unchanged by it.")
W(f"What this window could not do. Song 55's picks and builds still sing their own figures again less than a kept tune does (builds' median {SG['55']['page_gate']['every_build_figures_again_quartiles'][1]} against a kept lower quartile of {KP['repeated_figures'][1]}); in its opening 120 notes each song stands under the kept middle ({l3([SG[k]['page']['first_120'] for k in T3])} against {KP['first_120_figures_again'][2]}), for a memory of figures has little to draw on at a song's start, and most lines are returns fitted to new words, which the memory does not touch. Preferring, for a return, the nearest earlier line of the same syllable count was tried and moved the builds' median by a hundredth; it is not adopted. The memory also draws the songs a little toward the kept middle, against the finding of 749.94: a random pick from the pools stands outside the kept middle half on {PL['v31']['outside'][2]:.0f} song-checks at the median, where it stood on {PL['v30']['outside'][2]:.0f}. The three findings in the recording (a sound apart from its years; concentrated, still and uncrowded; what listeners return to) are not built: they are read from recordings, and the same ideas read on written arrangements fell short of their bar. And the page gate itself is small: about a twentieth to a fifth of a rank correlation, on what makes a tune kept, not on what makes it loved.")
W("")
for lead in ("WINDOW 188", "27.112", "Table GX", "923 A fresh line"):
    assert any(p_.text.strip().startswith(lead) or lead in p_.text[:40] for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v31.docx"); print("saved Luthier_v31.docx")
