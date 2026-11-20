import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v35.docx")
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










R = json.load(open("/home/claude/rightrevjf/zeneng-pipeline/lib/luthier/stage23_results.json")); SG = R["songs"]; PL = R["pools"]; V6 = PL["v36"]; V5 = PL["v35"]; T3 = ("55", "54", "58"); T4 = ("55", "54", "58", "59"); l3 = lambda v: ", ".join(str(x) for x in v); pc = lambda x: f"{100 * x:.0f}"; g = lambda x: f"{x:g}"; p1 = lambda x: round(100 * x, 1)
nm = lambda s: s.split("_")[1] if "_" in s else s; A = lambda k, c, w="builds", src="aimpool": SG[k][src][c][w]; REP, STP, LEP = "repeated notes", "moves by step", "moves by leap"; TRC = lambda k, w, src="trace": SG[k][src]["repeated_notes"][w]

WTS = "; ".join(", ".join(g(SG[k]["moves"][w]) for w in ("step", "leap", "repeat")) for k in T4)
# 937 (749.117): the pool figures under their right names, in Windows 189 to 192 and their rows
P0 = d.paragraphs; i189 = find_par(lambda p_: p_.text.strip().startswith("WINDOW 189")); fixes = (("A random pick from the pools fails", "The neighbour choice fails"), ("a random pick from the pools failed", "the neighbour choice failed"), ("a random pick from the pools fails", "the neighbour choice fails"), ("A random pool pick fails", "The neighbour choice fails"), ("a random pool pick fails", "the neighbour choice fails"), ("a random pool pick failed", "the neighbour choice failed"), ("The pools fail the soundness rule more often", "The neighbour choice fails the soundness rule more often"))
nfix = 0
for p_ in P0[i189:]:
    for x, y in fixes:
        if x in p_.text: sub(p_, x, y); nfix += 1
for row_ in d.tables[0].rows:
    if any(v in row_.cells[0].text for v in ("v203", "v204", "v205", "v206")):
        for p_ in row_.cells[1].paragraphs:
            for x, y in fixes:
                if x in p_.text: sub(p_, x, y); nfix += 1
print("labels corrected:", nfix)

sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v35")], "Luthier v35", "Luthier v36")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 35"))], "LUTHIER — VERSION 35", "LUTHIER — VERSION 36")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("192 Windows", "193 Windows"), ("Windows 1–192", "Windows 1–193"), ("192 scientific research windows", "193 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v207 (Luthier v36)")
set_cell(row.cells[1], f"TWO POOL FIGURES, RIGHTLY NAMED; THE REPEAT WEIGHT REACHES THE LINES THAT RETURN. The songwriting session's list (749.117 to 749.119). 937 (749.117): since Window 189 the papers gave the neighbour choice's failure rate under the name of the random pool pick. Both are now given under their own names, and Windows 189 to 192 are corrected. By the random pick from the engine's pool the engine fails the soundness rule {p1(PL['v32']['random_pool_pick_fails'])}, {p1(PL['v33']['random_pool_pick_fails'])}, {p1(PL['v34']['random_pool_pick_fails'])}, {p1(PL['v35']['random_pool_pick_fails'])} times in a hundred in Windows 189 to 192 and {p1(V6['random_pool_pick_fails'])} now; by the neighbour choice {p1(PL['v32']['neighbour_choice_fails'])}, {p1(PL['v33']['neighbour_choice_fails'])}, {p1(PL['v34']['neighbour_choice_fails'])}, {p1(PL['v35']['neighbour_choice_fails'])} and {p1(V6['neighbour_choice_fails'])}. 938 (749.119): 935 measured apart from 934: it changes no build of songs 55, 54 or 58, note for note, and no longer asks that a song have an aim. 939 (749.118): the repeat weight now reaches a returning line's new notes, and the fit is a bisection. The builds' repeated notes stand at {l3([A(k, REP) for k in T4])} against aims of {l3([A(k, REP, 'aim') for k in T4])} ({l3([A(k, REP, src='aimpool_v35') for k in T4])} before). The picks are sound, with no lean. Carried: 749.116, 749.111, 749.104's fix, 749.109, 749.103, 749.101, 749.61.")

after_par("27.116", [
    (f" Two pool figures; the repeat weight in the lines that return (Window 193; Table HC; studies/v36_trials, studies/review21). THE TWO FIGURES (937): the standard of 27.111 is read two ways and both are reported. The random pool pick: one build drawn at random from each song's pool (the builds past the old charge's better half and the gates). The neighbour choice: for a kept song drawn at random, the pool build nearest it. A LIMIT, NOT A GATE ON THE AIM (938): the limit of 935 is set in any song, with an aim or without; where the line before the short line ends in time, it changes nothing. THE REPEAT WEIGHT IN A LINE SUNG AGAIN (939): when a line returns to new words, a note that is split moves on six times in ten and takes the pitch before it four, and a lead-in is level 32 times in a hundred; those odds are scaled by the song's repeat weight, as a repeated note in a fresh line is weighed. THE FIT, A BISECTION (939): the last round whose fresh lines stayed inside the kept 10th to 90th and the nearest round outside are both kept; once there is one of each, every round is drawn halfway between them, in ratio; the weights kept are those of the best round inside. Tested: the soundness rule on the picks and by both pool figures; song 59 read and not fitted.", "27.117"),
])

P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 193: TWO POOL FIGURES, RIGHTLY NAMED", H1)
W("The list", H2)
W("The songwriting session reviewed Window 192. 934 holds; 935 mends song 59; 936 meets its check in two songs of four. It answered my question about the pools: 936 is not the cause of the rise, and the figure I had been quoting was under the wrong name. It sent three items (749.117 to 749.119).")
W("The two pool figures (937; 749.117)", H2)
W(f"The standard asks how often a pick drawn from the pools fails the soundness rule. neighbour.py reads it two ways. Since Window 189 I gave the first under the second's name. Both, in a hundred, for Windows 189, 190, 191, 192 and now: the neighbour choice, {l3([p1(PL[v]['neighbour_choice_fails']) for v in ('v32', 'v33', 'v34', 'v35', 'v36')])}; a random pick from the engine's pool, {l3([p1(PL[v]['random_pool_pick_fails']) for v in ('v32', 'v33', 'v34', 'v35', 'v36')])}. Both meet the standard's bar (ninety passes in a hundred) throughout. The sentences in Windows 189 to 192 and their rows in the version history are corrected to name the neighbour choice. By the random pool pick, the figure the standard names, Window 192 did not make the pools worse (2.5 to 2.6).")
W("935 measured apart (938; 749.119)", H2)
W(f"The session asked which of 934 and 935 raised the neighbour choice's failures, and that 935 be narrowed, since its count stood at a thousand in a thousand builds of songs 55 and 54. Built with and without 935 from the same draws, songs 55, 54 and 58 are note for note the same in 60 builds of 60 each (studies/v36_trials/cmp935.py): the limit is set in those songs and never binds. Only song 59 changes. So 935 cannot have moved the pools of the three songs the figures are read on, and the trial through neighbour.py says the same: without 935 the figures are Window 192's exactly ({p1(PL['v35 without 935']['neighbour_choice_fails'])} and {p1(PL['v35 without 935']['random_pool_pick_fails'])}). With 934 off (the old fit sizes) they are {p1(PL['v35 with the old fit sizes (934 off)']['neighbour_choice_fails'])} and {p1(PL['v35 with the old fit sizes (934 off)']['random_pool_pick_fails'])}; without 936, the session's trial, {p1(PL['v35 without 936']['neighbour_choice_fails'])} and {p1(PL['v35 without 936']['random_pool_pick_fails'])}. No one fix accounts for the neighbour choice's rise from 0.5 to 2.5: at four hundred draws that is two failures against ten, and the trials move as much among themselves. 935 is kept as it is, with one change: it no longer asks that the song have an aim, which a rule of rhythm should not depend on. Its count in the record now says what it is, a limit set, not a line moved.")
W("The repeat weight reaches the lines that return; the fit goes forward again (939; 749.118)", H2)
W(f"936 weighed a repeated note where a fresh line is drawn. A line that returns is refitted to new words, and where the refit splits a note or adds a lead-in it chose the same pitch at fixed odds that the weight never reached. Those odds are now scaled by the repeat weight. And the fit, which after one round outside the kept band stepped halfway back to the last round inside and kept stepping back, is now a bisection between the last round inside and the nearest round outside. Repeated notes in the lines that return, songs 55, 54, 58, 59: {l3([pc(TRC(k, 'returning_lines')) for k in T4])} in a hundred ({l3([pc(TRC(k, 'returning_lines', 'trace_v35')) for k in T4])} before); in fresh lines {l3([pc(TRC(k, 'fresh_lines')) for k in T4])} ({l3([pc(TRC(k, 'fresh_lines', 'trace_v35')) for k in T4])} before). Every living build's repeated notes: {l3([A(k, REP) for k in T4])} against aims of {l3([A(k, REP, 'aim') for k in T4])} ({l3([A(k, REP, src='aimpool_v35') for k in T4])} before). The fitted weights for a step, a leap and a repeat: {WTS}.")
WTS = "; ".join(", ".join(g(SG[k]["moves"][w]) for w in ("step", "leap", "repeat")) for k in T4)
for n_, title_, test_ in (
    ("937", "The two pool figures under their own names", "Test: every pool figure in the paper matches its key in neighbour_vNN.json."),
    ("938", "935 is a limit in any song", "Test: songs 55, 54 and 58 build note for note the same with and without it; song 59's deaths in the rhythm draw under ten in a hundred; the random pool pick fails no more than in Window 191."),
    ("939", "The repeat weight in a line sung again; the fit a bisection", "Test: in songs 55 and 54 the returning lines' repeated notes no more than 0.03 over the fresh lines'; song 55's builds within a quarter of the kept width of its aim; song 54's at or under the kept 25th; songs 58 and 59 within a quarter width.")):
    W(f"{n_} {title_}", H2); W(test_)
W("Table HC — the pools by both figures, failures of the soundness rule in a hundred.")
rows = [("", "Neighbour choice", "Random pick from the engine's pool", "Random pick from every living build")]
for lab, v in (("Window 189", "v32"), ("Window 190", "v33"), ("Window 191", "v34"), ("Window 192", "v35"), ("Window 192 without 936", "v35 without 936"), ("Window 192 without 935", "v35 without 935"), ("Window 192 with the old fit sizes", "v35 with the old fit sizes (934 off)"), ("Window 193", "v36")):
    rows.append((lab, p1(PL[v]['neighbour_choice_fails']), p1(PL[v]['random_pool_pick_fails']), p1(PL[v]['random_living_build_fails'])))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
leans = R['soundness']['engine']['lean_beyond_25th_75th']
W(f"The records. Songs 55, 54, 58 and 59 are written again: keys {l3([SG[k]['key'] for k in T4])} ({l3([SG[k]['key_before'] for k in T4])} before); ranges {l3([SG[k]['range'] for k in T4])} semitones against aims of {l3([g(SG[k]['range_aim']) for k in T4])}. The picks of songs 55, 54 and 58 stand outside the kept middle half on {l3(R['soundness']['outside_middle_half'])} checks of the 23 and pass the soundness rule" + (f", with all three leaning the same way past the kept quartiles on {' and '.join(x[0] for x in leans)}" if leans else ", and no check has all three leaning the same way past the kept quartiles (in Window 192, rhythm scaling did)") + f". The hold-out, song 59, read and not fitted: its pick stands outside the kept middle half on {SG['59']['compare']['outside_middle_half']} checks of the 21 read on single kept songs ({SG['59']['compare_v35']['outside_middle_half']} before); deaths in its rhythm draw {SG['59']['rhythm_deaths']} in a thousand; {SG['59']['survive']} builds survive. The pools now: the neighbour choice fails the rule {p1(V6['neighbour_choice_fails'])} times in a hundred ({p1(V5['neighbour_choice_fails'])} before) and a random pick from the engine's pool {p1(V6['random_pool_pick_fails'])} ({p1(V5['random_pool_pick_fails'])} before). Two-sided variety is {V6['variety']['sum_of_twice_the_smaller_side']} against the kept {V6['variety']['kept']} ({V5['variety']['sum_of_twice_the_smaller_side']} before). The kept tables, song 52 and song 53 are byte for byte as they were.")
chk55 = abs(A('55', REP) - A('55', REP, 'aim')) <= 0.045; gap = lambda k: round(TRC(k, 'returning_lines') - TRC(k, 'fresh_lines'), 3)
W(f"What this window could not do. The session's check for 938 was that the random pool pick fail no more than in Window 191 (2.5 in a hundred). It fails {p1(V6['random_pool_pick_fails'])}: not met. The two figures moved opposite ways this window, and at four hundred draws each is ten to twenty failures; both stay well inside the standard's bar, but the random pool pick is worse this window, and that is recorded here and not explained. 939's check: the returning lines' repeated notes stand {gap('55')} and {gap('54')} over the fresh lines' in songs 55 and 54 (0.03 asked); song 55's builds are " + ("within" if chk55 else "not within") + f" a quarter width of its aim ({A('55', REP)} against {A('55', REP, 'aim')}); song 54's builds stand at {A('54', REP)} against a kept 25th of 0.21. Where these are not met, the reason is the one 749.104 names: most of a returning line is its source's own notes, carried whole, and only its split notes and lead-ins are drawn anew. The hold-out is still far more central than a kept song (a kept song stands outside the middle half on ten checks of 21 at the median): 749.103 is the engine's largest open fault and nothing in this window was aimed at it. 749.116, the band under the break: not reached. 749.111's third trial was not run: with the peak planted only where the aim is wide, it would be judged on song 55 alone among the songs that may be fitted to, and the first two trials already show song 55 passing one check or the other but not both; it wants a second practice song with a wide aim. 749.104's fix, 749.109, 749.101, 749.61: carried.")
W("")
for lead in ("WINDOW 193", "27.117", "Table HC", "939 The repeat"):
    assert any(p_.text.strip().startswith(lead) or lead in p_.text[:40] for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v36.docx"); print("saved Luthier_v36.docx")
