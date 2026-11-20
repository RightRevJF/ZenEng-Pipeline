import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v32.docx")
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










R = json.load(open("/home/claude/rightrevjf/zeneng-pipeline/lib/luthier/stage20_results.json")); SG = R["songs"]; PL = R["pools"]; V3 = PL["v33"]; V2 = PL["v32"]; VT = PL["trial_with_aim_repeats"]; WH = R["where"]["kept"]; WP = R["where"]["pool"]; T3 = ("55", "54", "58"); l3 = lambda v: ", ".join(str(x) for x in v); pc = lambda x: f"{100 * x:.0f}"; g = lambda x: f"{x:g}"; p1 = lambda x: round(100 * x, 1)
nm = lambda s: s.split("_")[1] if "_" in s else s; A = lambda k, c, w="builds", src="aimpool": SG[k][src][c][w]
FIG, RHY, DIS, STP, LEP = "bars on a figure already sung", "bars on a rhythm already sung", "distinct rhythms over bars", "moves by step", "moves by leap"

sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v32")], "Luthier v32", "Luthier v33")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 32"))], "LUTHIER — VERSION 32", "LUTHIER — VERSION 33")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("189 Windows", "190 Windows"), ("Windows 1–189", "Windows 1–190"), ("189 scientific research windows", "190 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v204 (Luthier v33)")
set_cell(row.cells[1], f"A FAULT MENDED, AND THE RUN TESTED WHERE IT IS MADE. The songwriting session's list for this window (749.105 to 749.109). 928 (749.105): Window 189 broke the hymn engine; the cap on a run of one pitch was kept on the class and the hymn engine never set it. The cap is now each engine's own, and song 53 builds again, byte for byte. 929 (749.106): the cap is tested on every path that writes a line (a copy, a line sung again, a borrowed line, a melisma), and a returning line that would run past it moves its first note a step; the whole-build gate, which had removed {l3([SG[k]['deaths_926_before'] for k in T3])} builds of a thousand, now removes {l3([SG[k]['deaths_926'] for k in T3])}. 930 (749.108): each song's step and leap weights are fitted on short trial runs until its builds meet the aimed song; the builds' steps stand at {l3([A(k, STP) for k in T3])} against aims of {l3([A(k, STP, 'aim') for k in T3])} ({l3([A(k, STP, src='aimpool_v32') for k in T3])} before). The picks are sound; a random pool pick fails the rule {p1(V3['neighbour_fails'])} times in a hundred ({p1(V2['neighbour_fails'])} before). TRIED AND NOT ADOPTED (749.109): setting the borrows from the aimed song moved the builds' repeated bars by three hundredths and cost the pools their soundness (studies/v33_trials). Carried: 749.109, 749.104's fix, 749.103, 749.101, 749.61.")

after_par("27.113", [
    (f" The run tested where it is made; the moves fitted (Window 190; Table GZ; studies/review19, studies/v33_trials). THE CAP IS THE ENGINE'S OWN (928): the longest run of one pitch allowed is held by each engine and passed to the test; the hymn engine and a song with no aim use three. ONE TEST ON EVERY PATH (929): the run carried in from the lines before, plus the line, is tested wherever a line's pitches are written: drawn fresh, copied, sung again, or borrowed from an earlier line of its section. A returning line that fails at its join moves its first note one scale step toward its next note, on a tone that does not clash with the chord; a line sung again or borrowed that cannot be mended so is drawn fresh, and a copy is left to the whole-build gate, which stays as a backstop. A melisma whose lower step would make a run past the cap takes the upper step, or is not placed. THE MOVES FITTED (930): before the run, up to six rounds of eighty trial builds; each round reads the living builds' median share of moves by step and by leap, as sung, and scales the step weight (between 0.3 and 6) and the leap weight (between 0.3 and 5) toward the aimed song's shares, stopping within an eighth of the kept middle half's width. The weights and every round are in the record (target, moves_fit). Tested: the soundness rule on the picks and on the pools; song 53's records byte for byte.", "27.114"),
])

P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 190: A FAULT MENDED, AND THE RUN TESTED WHERE IT IS MADE", H1)
W("The list", H2)
W("The songwriting session reviewed Window 189, merged it and rebuilt song 58. It found a fault of mine, answered the two questions I had put to it, and sent five items (749.105 to 749.109). On the questions: the cap on a run is right but the gate as built was too heavy, and range and leaps should stay in the page floor. This window mends the fault, answers 749.106 and 749.108 with fixes, tries 749.109 and does not adopt it, and carries the rest.")
W("The hymn engine runs again (928; 749.105)", H2)
W("Window 189 kept the cap on a run of one pitch on the engine's class and set it when a 4/4 engine was made. The hymn engine is never made that way, so its first test of a run stopped with an error, and song 53 could not be built. In one process a second song would also have read the cap of the song before it. The cap is now each engine's own and is passed to the test; where none is given it is three. Song 53's run and parts are remade and are byte for byte what they were.")
W("One test on every path that writes a line (929; 749.106)", H2)
W(f"Window 189 stopped a long run only where a fresh line is drawn, and then removed whole builds for runs made elsewhere: {l3([SG[k]['deaths_926_before'] for k in T3])} builds of a thousand in songs 55, 54 and 58. The session traced where those runs were made: across the join of a copied or borrowed line, and by a melisma whose second note lands on the next note's pitch. It also found that the builds removed were the ones that repeat their figures most. Now the run carried in plus the line is tested on every path. A returning line that would run past the cap moves its first note one scale step toward its next note, as 839 lifts a held note; a melisma takes the step above, or is not placed. The whole-build gate stays as a backstop and now removes {l3([SG[k]['deaths_926'] for k in T3])}. First notes moved, over a thousand builds: {l3([SG[k]['moved_929'] for k in T3])}. Builds that survive: {l3([SG[k]['survive'] for k in T3])} ({l3([SG[k]['survive_before'] for k in T3])} before). Every pick's longest run is at or under its aimed song's ({l3([SG[k]['run'] for k in T3])} against {l3([SG[k]['run_cap'] for k in T3])}).")
W(f"The session's third check was that the pools should sing their figures again at least as much as in Window 188. Every build's median share of four-interval figures already sung: {l3([SG[k]['every_build_figures']['v33'] for k in T3])} now; {l3([SG[k]['every_build_figures']['v32'] for k in T3])} in Window 189; {l3([SG[k]['every_build_figures']['v31'] for k in T3])} in Window 188. Songs 55 and 58 meet the check; song 54 stands a little under its Window 188 figure.")
W("The steps and leaps fitted to each song (930; 749.108)", H2)
W(f"Window 189 weighted a step 1.2 and a leap 1.6 in every song. The session showed the builds did not follow their aims: song 58, aimed at the fewest steps, stepped most. Each song's weights are now fitted before its run, as 885 fitted the words' weights: rounds of eighty trial builds, each weight scaled until the builds' median, read as sung, meets the aimed song's. The fitted weights for songs 55, 54 and 58 are {l3([g(SG[k]['moves']['step']) for k in T3])} for a step and {l3([g(SG[k]['moves']['leap']) for k in T3])} for a leap. Every living build's median share of moves by step is {l3([A(k, STP) for k in T3])} against aims of {l3([A(k, STP, 'aim') for k in T3])} ({l3([A(k, STP, src='aimpool_v32') for k in T3])} before); by leap {l3([A(k, LEP) for k in T3])} against {l3([A(k, LEP, 'aim') for k in T3])} ({l3([A(k, LEP, src='aimpool_v32') for k in T3])} before). The order of the three songs on steps now follows the order of their aims. In songs 54 and 58 the step weight ends at its limit (6 and 0.3); song 54's builds stay a little short of its aim, for the register and the returns hold a song's steps more than the weight can move them.")
W("Tried and not adopted: the borrows set from the aimed song (749.109)", H2)
W(f"The session asked that, with 929 in, the figure borrow and the rhythm borrow be set from the aimed song again. It was tried on full runs (studies/v33_trials). In song 58 the builds' bars on a figure already sung moved from {A('58', FIG, src='aimpool_v32')} to {A('58', FIG, src='aimpool_trial')} against an aim of {A('58', FIG, 'aim')}, and bars on a rhythm already sung from {A('58', RHY, src='aimpool_v32')} to {A('58', RHY, src='aimpool_trial')} against {A('58', RHY, 'aim')}; song 54 moved as little. The check was not met, and a random pick from the pools failed the soundness rule {p1(VT['neighbour_fails'])} times in a hundred. So it is not adopted. The reason it tops out is plain in song 58, whose figure borrow was already at its limit of one: a borrowed line is refitted to new words of a different syllable count, so its bars are seldom the same bars. Bars return when a line is fitted to an earlier line's bars by splitting and merging notes, which is the fix 749.104 names. The two findings are one.")
W(f"The sentence in Window 189 that song 58 \"now sounds like\" the kept song it aims at was too wide. It is true of its range and its runs. It is the reverse of the truth for its repetition and rhythm: Bird Dog sings {pc(A('58', FIG, 'aim'))} bars in a hundred on a figure already sung and song 58's builds {pc(A('58', FIG))}.")
for n_, title_, test_ in (
    ("928", "The cap on a run is the engine's own", "Test: song 53's run and parts byte for byte; an aimed song built and then song 53 in one process leaves song 53 unchanged."),
    ("929", "One test on every path that writes a line", "Test: the whole-build gate removes under ten builds in a hundred in each song; every pick's longest run, as sung, at or under its aimed song's."),
    ("930", "The steps and leaps fitted to each song", "Test: across the three songs the builds' order on steps follows their aims' order; each song's builds within a quarter of the kept middle half's width of its aim on leaps, and on steps where the weight is inside its limits.")):
    W(f"{n_} {title_}", H2); W(test_)
W("Table GZ — every living build's median against the aimed kept song (aim; Window 189; now).")
rows = [("", "Song 55", "Song 54", "Song 58"), ("Aims at", *[nm(SG[k]['aims_at']) for k in T3])]
for c, lab in ((STP, "Moves by step"), (LEP, "Moves by leap"), ("range", "Range"), ("repeated notes", "Repeated notes"), (FIG, "Bars on a figure already sung"), (RHY, "Bars on a rhythm already sung"), (DIS, "Distinct rhythms over bars"), ("rhythm scaling", "Rhythm scaling")):
    rows.append((lab, *[f"{g(A(k, c, 'aim'))}; {g(A(k, c, src='aimpool_v32'))}; {g(A(k, c))}" for k in T3]))
rows.append(("Builds removed by the run gate, of 1,000: Window 189; now", *[f"{SG[k]['deaths_926_before']}; {SG[k]['deaths_926']}" for k in T3]))
rows.append(("Builds the page floor passed over: Window 189; now", *[f"{SG[k]['page_gate_before']['read'] - SG[k]['page_gate_before']['passed']} of {SG[k]['page_gate_before']['read']}; {SG[k]['page_gate']['read'] - SG[k]['page_gate']['passed']} of {SG[k]['page_gate']['read']}" for k in T3]))
rows.append(("Checks outside the kept middle half, of 23", *[str(x) for x in R['soundness']['outside_middle_half']]))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
leans = R['soundness']['engine']['lean_beyond_25th_75th']
W(f"The records. Songs 55, 54 and 58 are written again: keys {l3([SG[k]['key'] for k in T3])} ({l3([SG[k]['key_before'] for k in T3])} before); {l3([SG[k]['seconds'] for k in T3])} seconds; ranges {l3([SG[k]['range'] for k in T3])} semitones against aims of {l3([g(SG[k]['range_aim']) for k in T3])}; chorus lifts as sung {l3([g(SG[k]['lift_sung']) for k in T3])} against the aimed songs' {l3([g(SG[k]['kept_lift']) for k in T3])}. Their picks stand outside the kept middle half on {l3(R['soundness']['outside_middle_half'])} checks of the 23 and pass the soundness rule" + (f", with all three leaning the same way past the kept quartiles on {' and '.join(x[0] for x in leans)}" if leans else "") + f". A random pick from the pools fails the rule {p1(V3['neighbour_fails'])} times in a hundred ({p1(V2['neighbour_fails'])} before); a random pick from every build that lived, {pc(V3['random_build_fails'])} ({pc(V2['random_build_fails'])} before). The kept tables are byte for byte as they were. Songs 52 and 53 are unchanged, byte for byte.")
W(f"What this window could not do. 749.109, repeats and rhythm following the aimed song: tried and not adopted, as above; it waits on 749.104's fix. 749.104's fix, fitting a section's later lines to its earlier bars, is still untried outside the engine and is now the one thing three findings wait on (749.104, 749.109, 749.101). 749.103, variety counted on both sides: {V3['variety']['sum_of_twice_the_smaller_side']} against the kept {V3['variety']['kept']} ({V2['variety']['sum_of_twice_the_smaller_side']} before); the pooled width {V3['variety']['median_spread_ratio_all_three_pooled']} against the 0.75 asked. Not met. 749.107: the page floor passes over {SG['55']['page_gate']['read'] - SG['55']['page_gate']['passed']} of {SG['55']['page_gate']['read']} builds in song 55 ({SG['55']['page_gate_before']['read'] - SG['55']['page_gate_before']['passed']} of {SG['55']['page_gate_before']['read']} before). Song 55's builds span {g(A('55', 'range'))} semitones against an aim of {g(A('55', 'range', 'aim'))}; widening how far a line strays from its register was tried in the fit and does not move it. The small thing the session named, that one record reads repeated figures two ways (the builds past the gates as sung, every build before melismas), is not yet mended. 749.61, song 52 in 6/8: no kept 6/8 table.")
W("")
for lead in ("WINDOW 190", "27.114", "Table GZ", "930 The steps"):
    assert any(p_.text.strip().startswith(lead) or lead in p_.text[:40] for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v33.docx"); print("saved Luthier_v33.docx")
