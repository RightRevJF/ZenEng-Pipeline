import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v34.docx")
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










R = json.load(open("/home/claude/rightrevjf/zeneng-pipeline/lib/luthier/stage22_results.json")); SG = R["songs"]; PL = R["pools"]; V5 = PL["v35"]; V4 = PL["v34"]; T3 = ("55", "54", "58"); T4 = ("55", "54", "58", "59"); l3 = lambda v: ", ".join(str(x) for x in v); pc = lambda x: f"{100 * x:.0f}"; g = lambda x: f"{x:g}"; p1 = lambda x: round(100 * x, 1)
nm = lambda s: s.split("_")[1] if "_" in s else s; A = lambda k, c, w="builds", src="aimpool": SG[k][src][c][w]; REP, STP, LEP = "repeated notes", "moves by step", "moves by leap"; PK = lambda k, f: SG[k]["peak"]["forms"][f]; TRC = lambda k, w, src="trace": SG[k][src]["repeated_notes"][w]

sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v34")], "Luthier v34", "Luthier v35")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 34"))], "LUTHIER — VERSION 34", "LUTHIER — VERSION 35")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("191 Windows", "192 Windows"), ("Windows 1–191", "Windows 1–192"), ("191 scientific research windows", "192 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v206 (Luthier v35)")
set_cell(row.cells[1], f"THE HOLD-OUT. A new lyric the engine had never seen, song 59, was written on Window 191 as it stood, and is kept as a hold-out: read after every fix, never fitted to. It was sound and too central: where the song it aims at leaves the kept middle, its builds stayed in the middle. The session's list (749.113 to 749.116). 934 (749.115): each round of the fit draws until forty builds pass the gates; song 59's rounds had read 9 to 17. 935 (749.114): half of song 59's builds died in the rhythm draw. The trace found one line, the bridge's three-syllable last line in a one-bar slot, squeezed between the line before it and the chorus's early entry; the line before now gives way. Deaths fell from {SG['59']['rhythm_deaths_before']} to {SG['59']['rhythm_deaths']} in a thousand. 936 (749.113): the weight on a repeated note is fitted with the step and leap weights; the builds' repeated notes stand at {l3([A(k, REP) for k in T4])} against aims of {l3([A(k, REP, 'aim') for k in T4])} ({l3([A(k, REP, src='aimpool_v34') for k in T4])} before). The picks are sound; a random pool pick fails the rule {p1(V5['neighbour_fails'])} times in a hundred ({p1(V4['neighbour_fails'])} before). TRIED OUTSIDE THE ENGINE AGAIN AND NOT BUILT (749.111): the peak placed more surely helps the wide aims and harms the narrow one. Carried: 749.116, 749.111, 749.104's fix, 749.109, 749.103, 749.101, 749.61.")

after_par("27.115", [
    (f" The hold-out, and three fixes it found (Window 192; Table HB; studies/holdout59, studies/v35_traces, studies/plant_the_peak). THE HOLD-OUT: song 59 (songs/p69) is read after every fix beside songs 55, 54 and 58; no weight or setting is fitted to it. ENOUGH BUILDS TO FIT ON (934): a round of the fit of 27.114 draws until forty builds pass the gates, with four hundred tries at most, and records its tries. A LINE GIVES WAY TO A SHORT LINE (935): where a line of one bar or less stands between this line and a copied or designed line that comes in early, this line's last syllable must leave the short line room: the short line's latest end, less an eighth for each of its syllables after the first, less a beat. THE REPEATED NOTE (936): a note on the pitch before it carries its own weight, fitted with the step and leap weights (between 0.2 and 5) toward the aimed song's share of repeated notes, bounded as they are by the fresh lines' own share staying inside the kept 10th to 90th; a round whose fresh lines leave that band is followed by one halfway back to the last round that stayed inside. Tested: the soundness rule on the picks and on the pools; song 59 read and not fitted.", "27.116"),
])

P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 192: THE HOLD-OUT", H1)
W("A song the engine had not seen", H2)
W(f"For many windows every fix was tuned and read on the same three lyrics. Jason asked whether a new song was needed to test it all, and the fair test was a new 4/4 lyric written on the engine as it stood, with no change during the song and the pick taken as drawn. The songwriting session wrote song 59, \"Before the Bread Goes Cold\", on Window 191: heartland rock at 120 beats a minute, aimed at Two Hearts (Phil Collins, 1989). Its readings are in studies/holdout59.")
W(f"It was sound: no check past the kept 10th to 90th, and the three-song rule passes on every three of songs 55, 54, 58 and 59. It was also too central. Of the 21 checks read on single kept songs it stood outside the kept middle half on {SG['59']['compare_v34']['outside_middle_half']}; a kept song stands outside on ten at the median, and one kept song in 147 is as central. And it was near its aim only where its aim is ordinary. Where Two Hearts leaves the kept middle (a range of 24, few repeated notes) the builds stayed in the middle. On the three practice songs the aim had looked stronger than it is. That is what a hold-out is for. Song 59 stays a hold-out: it is read after every fix and nothing is fitted to it.")
W("Enough builds to fit on (934; 749.115)", H2)
W(f"The fit's rounds drew eighty trial builds and read those that passed the gates. In song 59 half the builds died, the rounds read {l3(SG['59']['rounds_before'])} builds, and the fit wandered. A round now draws until forty builds pass, with four hundred tries at most. Every round in all four songs reads forty. Rerun on song 59 with a second trial seed, the fitted weights are {g(R['fit_seed_59']['second_seed']['step'])}, {g(R['fit_seed_59']['second_seed']['leap'])} and {g(R['fit_seed_59']['second_seed']['repeat'])} for a step, a leap and a repeat, against {g(R['fit_seed_59']['first_seed']['step'])}, {g(R['fit_seed_59']['first_seed']['leap'])} and {g(R['fit_seed_59']['first_seed']['repeat'])}.")
W("The line that could not fit (935; 749.114)", H2)
W(f"Half of song 59's thousand builds died with \"the syllables cannot fit the window\". The session read this as long verse lines at a quick tempo and asked for a trace before any change. The trace (studies/v35_traces) found something else: every one of those deaths was one line, the bridge's last, \"To be fed\": three syllables in a one-bar slot. The line before it ran late into that bar, and the chorus after it is a copy that comes in early, so the short line was asked to begin after it had to end. The engine already makes a line give way to a copied line that comes in early (816); it now also gives way when a line of one bar or less stands between. Song 59's rhythm deaths fell from {SG['59']['rhythm_deaths_before']} to {SG['59']['rhythm_deaths']} in a thousand, and {SG['59']['survive']} builds survive ({SG['59']['survive_before']} before). The long verse lines were not at fault.")
W("The repeated note fitted (936; 749.113)", H2)
W(f"In all four songs the builds repeated a pitch more often than the aimed song does. The trace asked where: in the lines drawn fresh a note repeats the one before it {l3([pc(TRC(k, 'fresh_lines', 'trace_v34')) for k in T4])} times in a hundred (songs 55, 54, 58, 59), in the lines that return {l3([pc(TRC(k, 'returning_lines', 'trace_v34')) for k in T4])}, and across the joins between lines {l3([pc(TRC(k, 'joins', 'trace_v34')) for k in T4])}. The returning lines carry what the fresh lines sang, so the fresh lines are the place to act. A repeated note now has its own weight, fitted with the step and leap weights and bounded the same way. The fitted weights are {l3([g(SG[k]['moves']['repeat']) for k in T4])}. Fresh lines now repeat at {l3([pc(TRC(k, 'fresh_lines')) for k in T4])} in a hundred. Every living build's share of repeated notes: {l3([A(k, REP) for k in T4])} against aims of {l3([A(k, REP, 'aim') for k in T4])} ({l3([A(k, REP, src='aimpool_v34') for k in T4])} before). Songs 58 and 59 are within the quarter-width asked; the hold-out moved most, from {A('59', REP, src='aimpool_v34')} to {A('59', REP)} against {A('59', REP, 'aim')}, with nothing fitted to it but its own aim. Songs 55 and 54 are not: their aims lie under the kept 10th, their fresh lines are held inside the kept band, and the lines that return still repeat at {l3([pc(TRC(k, 'returning_lines')) for k in ('55', '54')])} in a hundred.")
W("Tried outside the engine again and not built: the peak placed more surely (749.111)", H2)
W(f"Window 191's trial planted the peak in too few builds to be a fair test. The rule was written again before a second trial (studies/plant_the_peak/PREDICTION2.md), with two surer ways: up to sixty redraws (A60), and the line moved whole by scale steps until its highest stressed note is the peak (C). The peak was planted in {l3([pc(PK(k, 'C')['planted_share']) for k in T3])} builds in a hundred in form C. Neither form met the rule in all three songs. Builds spanning within two semitones of the aim, as built, A60, C: song 55, {l3([pc(PK('55', f)['span_within_2_of_aim']) for f in ('as built', 'A60', 'C')])}; song 54, {l3([pc(PK('54', f)['span_within_2_of_aim']) for f in ('as built', 'A60', 'C')])}; song 58, {l3([pc(PK('58', f)['span_within_2_of_aim']) for f in ('as built', 'A60', 'C')])}. Builds with the top note's share inside the kept band: song 55, {l3([pc(PK('55', f)['share_on_top_inside_kept_10th_90th']) for f in ('as built', 'A60', 'C')])}; song 54, {l3([pc(PK('54', f)['share_on_top_inside_kept_10th_90th']) for f in ('as built', 'A60', 'C')])}; song 58, {l3([pc(PK('58', f)['share_on_top_inside_kept_10th_90th']) for f in ('as built', 'A60', 'C')])}.")
W(f"The pattern is clear all the same. Planting the peak helps a wide aim and harms a narrow one. Song 55 (aim 19) reaches its span twice as often. The hold-out, read and not counted, shows it most: aimed at a range of 24, none of song 59's builds comes within two semitones as built, and {pc(PK('59', 'A60')['span_within_2_of_aim'])} in a hundred do with the peak planted, though few builds then survive ({PK('59', 'A60')['builds']} of a hundred), for the peak is set near the top of the voice. Song 58 (aim 9) already reaches its span and, planted, sits on its top note far more than kept tunes do. The next trial, with its rule written first, is to plant the peak only where the aim is wider than the kept middle. It is not built.")
for n_, title_, test_ in (
    ("934", "A round of the fit draws until enough builds pass", "Test: every round reads forty builds in all four songs; song 59's fitted weights hold under a second trial seed."),
    ("935", "A line gives way to a short line before a copy", "Test: in song 59, deaths in the rhythm draw under ten in a hundred."),
    ("936", "The repeated note fitted", "Test: the builds' median share of repeated notes within a quarter of the kept middle half's width of the aim, where the aim lies inside the kept 10th to 90th; the soundness rule on the pools.")):
    W(f"{n_} {title_}", H2); W(test_)
W("Table HB — the four songs: every living build's median against the aimed kept song (aim; Window 191; now). Song 59 is the hold-out.")
rows = [("", "Song 55", "Song 54", "Song 58", "Song 59 (hold-out)"), ("Aims at", *[nm(SG[k]['aims_at']) for k in T4]), ("Step; leap; repeat weights", *[f"{g(SG[k]['moves']['step'])}; {g(SG[k]['moves']['leap'])}; {g(SG[k]['moves']['repeat'])}" for k in T4])]
for c, lab in ((REP, "Repeated notes"), (STP, "Moves by step"), (LEP, "Moves by leap"), ("range", "Range"), ("bars on a figure already sung", "Bars on a figure already sung"), ("bars on a rhythm already sung", "Bars on a rhythm already sung"), ("rhythm scaling", "Rhythm scaling")):
    rows.append((lab, *[f"{g(A(k, c, 'aim'))}; {g(A(k, c, src='aimpool_v34'))}; {g(A(k, c))}" for k in T4]))
rows.append(("Builds that survive, of 1,000: Window 191; now", *[f"{SG[k]['survive_before']}; {SG[k]['survive']}" for k in T4]))
rows.append(("Checks outside the kept middle half, of 21 read on single kept songs: Window 191; now", *[f"{SG[k]['compare_v34']['outside_middle_half']}; {SG[k]['compare']['outside_middle_half']}" for k in T4]))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
leans = R['soundness']['engine']['lean_beyond_25th_75th']
W(f"The records. Songs 55, 54, 58 and 59 are written again: keys {l3([SG[k]['key'] for k in T4])} ({l3([SG[k]['key_before'] for k in T4])} before); {l3([SG[k]['seconds'] for k in T4])} seconds; ranges {l3([SG[k]['range'] for k in T4])} semitones against aims of {l3([g(SG[k]['range_aim']) for k in T4])}. The picks of songs 55, 54 and 58 stand outside the kept middle half on {l3(R['soundness']['outside_middle_half'])} checks of the 23 and pass the soundness rule" + (f", with all three leaning the same way past the kept quartiles on {' and '.join(x[0] for x in leans)}" if leans else "") + f". A random pick from the pools fails the rule {p1(V5['neighbour_fails'])} times in a hundred ({p1(V4['neighbour_fails'])} before); a random pick from every build that lived, {pc(V5['random_build_fails'])} ({pc(V4['random_build_fails'])} before). The kept tables, song 52 and song 53 are byte for byte as they were.")
W(f"What this window could not do. The hold-out's main finding stands: the songs are sound and too like the middle. Song 59's pick now stands outside the kept middle half on {SG['59']['compare']['outside_middle_half']} checks of 21 ({SG['59']['compare_v34']['outside_middle_half']} before), more central still, and its range is {SG['59']['range']} against an aim of {g(SG['59']['range_aim'])}. Variety counted on both sides is {V5['variety']['sum_of_twice_the_smaller_side']} against the kept {V5['variety']['kept']} ({V4['variety']['sum_of_twice_the_smaller_side']} before): 749.103 is not met and did not move. The pools fail the soundness rule more often than in Window 191 ({p1(V5['neighbour_fails'])} against {p1(V4['neighbour_fails'])} in a hundred). Songs 55 and 54 still repeat notes more than their aims, and song 55's builds leap a little more than its aim ({A('55', LEP)} against {A('55', LEP, 'aim')}; {A('55', LEP, src='aimpool_v34')} before). 749.116, the break reading louder than the last chorus in the demo: not reached; it is in the band's arrangement and needs the demo's reading to check. 749.111: tried twice, not built. 749.104's fix, with 749.109 and 749.101 waiting on it: still untried outside the engine. 749.61: no kept 6/8 table.")
W("")
for lead in ("WINDOW 192", "27.116", "Table HB", "936 The repeated"):
    assert any(p_.text.strip().startswith(lead) or lead in p_.text[:40] for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v35.docx"); print("saved Luthier_v35.docx")
