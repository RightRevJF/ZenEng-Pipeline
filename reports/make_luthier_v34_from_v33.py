import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v33.docx")
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










R = json.load(open("/home/claude/rightrevjf/zeneng-pipeline/lib/luthier/stage21_results.json")); SG = R["songs"]; PL = R["pools"]; V4 = PL["v34"]; V3 = PL["v33"]; T3 = ("55", "54", "58"); l3 = lambda v: ", ".join(str(x) for x in v); pc = lambda x: f"{100 * x:.0f}"; g = lambda x: f"{x:g}"; p1 = lambda x: round(100 * x, 1)
nm = lambda s: s.split("_")[1] if "_" in s else s; A = lambda k, c, w="builds", src="aimpool": SG[k][src][c][w]; KRD = lambda k: SG[k]["fit"][SG[k]["kept_round"] - 1]
FIG, RHY, DIS, STP, LEP = "bars on a figure already sung", "bars on a rhythm already sung", "distinct rhythms over bars", "moves by step", "moves by leap"; PK = lambda k, f: SG[k]["peak"]["forms"][f]

sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v33")], "Luthier v33", "Luthier v34")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 33"))], "LUTHIER — VERSION 33", "LUTHIER — VERSION 34")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("190 Windows", "191 Windows"), ("Windows 1–190", "Windows 1–191"), ("190 scientific research windows", "191 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v205 (Luthier v34)")
set_cell(row.cells[1], f"THE MELISMAS FROM THE AIMED SONG; THE FIT BOUNDED BY THE FRESH LINES. The songwriting session's list for this window (749.110 to 749.112). 931 (749.112): the record's counts are the run's thousand builds; before, they also counted the fit's trial builds. 932 (749.110): a song's share of syllables sung on two notes is its aimed song's own ({l3([g(SG[k]['melisma_share']) for k in T3])} in a hundred for songs 55, 54 and 58; {l3([g(SG[k]['melisma_share_before']) for k in T3])} before), and the fit of the step and leap weights stops where the fresh lines' own shares would leave the kept 10th to 90th. Song 58's step weight comes back inside its limits ({g(SG['58']['moves']['step'])}; 0.3 before) with its builds' steps at {A('58', STP)} against an aim of {A('58', STP, 'aim')}. With Bird Dog's melismas, song 58's builds sing {pc(A('58', FIG))} bars in a hundred on a figure already sung ({pc(A('58', FIG, src='aimpool_v33'))} before; aim {pc(A('58', FIG, 'aim'))}). 933: the record reads repeated figures one way, as sung. The picks are sound; a random pool pick fails the rule {p1(V4['neighbour_fails'])} times in a hundred ({p1(V3['neighbour_fails'])} before). TRIED OUTSIDE THE ENGINE AND NOT BUILT (749.111): planting the peak, in two forms; neither met its check (studies/plant_the_peak). Carried: 749.111, 749.104's fix, 749.109, 749.103, 749.101, 749.61.")

after_par("27.114", [
    (f" The melismas from the aimed song; the fit bounded (Window 191; Table HA; studies/review20, studies/plant_the_peak). THE COUNTS (931): the engine's counts are cleared after the fit of 27.114, so a record's stats are its run's builds; the fit's own number of trial builds is in the record (target, moves_fit, trial_builds). THE MELISMAS (932): each kept song's share of syllables sung on more than one note is in the kept table (tables/metre_atlas/kept_readings.json, melismas; rows unchanged); a song with an aim takes its aimed song's share, inside the kept 10th to 90th, and a song with no aim draws from the kept quartiles as before. THE FIT BOUNDED (932): each round also reads the share of steps and of leaps inside the lines drawn fresh, where the weights act; a weight is scaled no further once that share would leave the kept 10th to 90th, and is drawn back if it has; the weights kept are those of the round nearest the aim among the rounds whose fresh lines stayed inside. Where the aim lies past what that allows, the shortfall is accepted. ONE READING (933): every build's repeated figures are read as sung, as the builds past the gates are, and the record says so. Tested: the soundness rule on the picks and on the pools.", "27.115"),
])

P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 191: THE MELISMAS FROM THE AIMED SONG; THE FIT BOUNDED BY THE FRESH LINES", H1)
W("The list", H2)
W("The songwriting session reviewed Window 190 and found that 928, 929 and 930 hold as written. It answered my two questions. The step weight at its limit is a symptom: the weight acts only on lines drawn fresh, about 13 notes in 100, and in song 58 it was pressing those lines to undo steps that the melismas add and Bird Dog never sings. And song 55's tunes never reach their top. It sent three items (749.110 to 749.112).")
W("The record's counts (931; 749.112)", H2)
W(f"The fit's trial builds ran on the same engine as the run and their counts were left in the record. Window 190's \"first notes moved, over a thousand builds: 923, 1785, 3070\" was over 1,160, 1,480 and 1,480 builds. The counts are now cleared after the fit. Per thousand builds, in songs 55, 54 and 58: first notes moved at a join, {l3([SG[k]['moved_929'] for k in T3])}; lines sung again that could not be fitted and were drawn fresh, {l3([SG[k]['stat_712'] for k in T3])}. The fit's own trial builds ({l3([SG[k]['trial_builds'] for k in T3])}) are recorded beside it.")
W("The melismas from the aimed song, and the fit bounded by the fresh lines (932; 749.110)", H2)
W(f"A song's share of syllables sung on two notes was drawn from the kept quartiles: {l3([g(SG[k]['melisma_share_before']) for k in T3])} in a hundred for songs 55, 54 and 58, against {l3([g(SG[k]['kept_song_melisma_share']) for k in T3])} in the songs they aim at. It is now the aimed song's own, as the lift (925) and the run (926) are, inside the kept 10th to 90th: {l3([g(SG[k]['melisma_share']) for k in T3])}. The fit then reads, each round, the shares of steps and leaps inside the fresh lines, and scales a weight no further once those would leave the kept 10th to 90th ({l3(SG['55']['fresh_bounds'][STP])} for steps, {l3(SG['55']['fresh_bounds'][LEP])} for leaps).")
W(f"The fitted weights are {l3([g(SG[k]['moves']['step']) for k in T3])} for a step ({l3([g(SG[k]['moves_before']['step']) for k in T3])} before) and {l3([g(SG[k]['moves']['leap']) for k in T3])} for a leap ({l3([g(SG[k]['moves_before']['leap']) for k in T3])} before). In the round kept, the fresh lines step at {l3([KRD(k)['fresh_lines_step'] for k in T3])} and leap at {l3([KRD(k)['fresh_lines_leap'] for k in T3])}. Every living build's steps: {l3([A(k, STP) for k in T3])} against aims of {l3([A(k, STP, 'aim') for k in T3])}; leaps {l3([A(k, LEP) for k in T3])} against {l3([A(k, LEP, 'aim') for k in T3])}. Song 58's weight is back inside its limits and its builds are within the quarter-width asked. Song 54's aim ({A('54', STP, 'aim')}) lies past the kept 90th; its fresh lines cannot carry it there inside the bound, and the shortfall is accepted, as the session said: the rest of the reach is in the lines that return.")
W(f"The melismas moved more than the steps. With Bird Dog's share, song 58's builds sing {pc(A('58', FIG))} bars in a hundred on a figure already sung ({pc(A('58', FIG, src='aimpool_v33'))} before; Bird Dog {pc(A('58', FIG, 'aim'))}) and {pc(A('58', RHY))} on a rhythm already sung ({pc(A('58', RHY, src='aimpool_v33'))} before; Bird Dog {pc(A('58', RHY, 'aim'))}). Song 54 moved the same way ({pc(A('54', FIG, src='aimpool_v33'))} to {pc(A('54', FIG))}; {pc(A('54', RHY, src='aimpool_v33'))} to {pc(A('54', RHY))}). Song 55, whose aimed song has more melismas than it was given, moved the other way: {pc(A('55', FIG, src='aimpool_v33'))} to {pc(A('55', FIG))} bars on a figure already sung against an aim of {pc(A('55', FIG, 'aim'))}, and {pc(A('55', RHY, src='aimpool_v33'))} to {pc(A('55', RHY))} on a rhythm already sung against {pc(A('55', RHY, 'aim'))}. A melisma splits a note, and a line that returns to new words does not get its melismas in the same places, so each melisma is a bar that no longer matches. This is part of why the songs repeated their bars less than kept songs do, and it belongs with 749.104: when a line is fitted to an earlier line's bars, its melismas should come with it.")
W("One reading of repeated figures (933)", H2)
W(f"The record read the builds past the gates as sung and every build before its melismas. Both are now read as sung, and the record says so. Every build's median share of four-interval figures already sung, as sung: {l3([SG[k]['every_build_figures']['now_as_sung'] for k in T3])}; the builds past the gates: {l3([SG[k]['every_build_figures']['gate_builds_as_sung'] for k in T3])}. The gap between them is now two hundredths; most of the earlier gap was the reading.")
W("Tried outside the engine and not built: plant the peak (749.111)", H2)
W(f"The session proposed that, in the section where the aimed song first reaches its top, the first line drawn fresh should sing its highest stressed note at the floor plus the aimed range, so that the lines that return carry the peak. It asked for a trial outside the engine first. The rule was written before the trial (studies/plant_the_peak/PREDICTION.md): on a hundred tries a song, the builds' span within two semitones of the aim in at least half the builds, and the share of notes on the top note inside the kept 10th to 90th in nine builds in ten. Two forms were tried: A, every part's top at the peak; B, every other fresh line held two semitones under it.")
W(f"Neither form met the rule. Builds spanning within two semitones of the aim, as built, form A, form B: song 55, {l3([pc(PK('55', f)['span_within_2_of_aim']) for f in ('as built', 'A', 'B')])} in a hundred; song 54, {l3([pc(PK('54', f)['span_within_2_of_aim']) for f in ('as built', 'A', 'B')])}; song 58, {l3([pc(PK('58', f)['span_within_2_of_aim']) for f in ('as built', 'A', 'B')])}. Builds with the top note's share inside the kept 10th to 90th: song 55, {l3([pc(PK('55', f)['share_on_top_inside_kept_10th_90th']) for f in ('as built', 'A', 'B')])}; song 54, {l3([pc(PK('54', f)['share_on_top_inside_kept_10th_90th']) for f in ('as built', 'A', 'B')])}; song 58, {l3([pc(PK('58', f)['share_on_top_inside_kept_10th_90th']) for f in ('as built', 'A', 'B')])}. Planting helps song 55's span, which was the complaint, and makes song 58 sit on its top more. The trial has a weakness of its own: the peak was planted by redrawing the line in a raised register up to twelve times, and that took in only {l3([pc(PK(k, 'A')['planted_share']) for k in T3])} builds in a hundred. So this is a fair test of the idea drawn that way and not of the idea. It is not built. The next trial should place the peak note directly and draw the line around it.")
for n_, title_, test_ in (
    ("931", "The record's counts are the run's", "Test: the record's stats come from the run's thousand builds; the fit's trial builds are counted beside them."),
    ("932", "The melismas from the aimed song; the fit bounded by the fresh lines", "Test: in each song the fresh lines' step and leap shares, in the round kept, inside the kept 10th to 90th; song 58's step weight inside its limits and its builds' steps within a quarter of the kept middle half's width of the aim; the soundness rule on the pools."),
    ("933", "One reading of repeated figures", "Test: the record names the reading for every build and for the builds past the gates, and they are the same.")):
    W(f"{n_} {title_}", H2); W(test_)
W("Table HA — every living build's median against the aimed kept song (aim; Window 190; now).")
rows = [("", "Song 55", "Song 54", "Song 58"), ("Aims at", *[nm(SG[k]['aims_at']) for k in T3]), ("Melismas, syllables in 100: the kept song's; before; now", *[f"{g(SG[k]['kept_song_melisma_share'])}; {g(SG[k]['melisma_share_before'])}; {g(SG[k]['melisma_share'])}" for k in T3]),
        ("Step weight; leap weight", *[f"{g(SG[k]['moves']['step'])}; {g(SG[k]['moves']['leap'])}" for k in T3])]
for c, lab in ((STP, "Moves by step"), (LEP, "Moves by leap"), ("range", "Range"), ("repeated notes", "Repeated notes"), (FIG, "Bars on a figure already sung"), (RHY, "Bars on a rhythm already sung"), (DIS, "Distinct rhythms over bars"), ("rhythm scaling", "Rhythm scaling")):
    rows.append((lab, *[f"{g(A(k, c, 'aim'))}; {g(A(k, c, src='aimpool_v33'))}; {g(A(k, c))}" for k in T3]))
rows.append(("Checks outside the kept middle half, of 23", *[str(x) for x in R['soundness']['outside_middle_half']]))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
leans = R['soundness']['engine']['lean_beyond_25th_75th']
W(f"The records. Songs 55, 54 and 58 are written again: keys {l3([SG[k]['key'] for k in T3])} ({l3([SG[k]['key_before'] for k in T3])} before); {l3([SG[k]['seconds'] for k in T3])} seconds; ranges {l3([SG[k]['range'] for k in T3])} semitones against aims of {l3([g(SG[k]['range_aim']) for k in T3])} ({l3([SG[k]['range_before'] for k in T3])} before); chorus lifts as sung {l3([g(SG[k]['lift_sung']) for k in T3])} against the aimed songs' {l3([g(SG[k]['kept_lift']) for k in T3])}. Their picks stand outside the kept middle half on {l3(R['soundness']['outside_middle_half'])} checks of the 23 and pass the soundness rule" + (f", with all three leaning the same way past the kept quartiles on {' and '.join(x[0] for x in leans)}" if leans else "") + f". A random pick from the pools fails the rule {p1(V4['neighbour_fails'])} times in a hundred ({p1(V3['neighbour_fails'])} before); a random pick from every build that lived, {pc(V4['random_build_fails'])} ({pc(V3['random_build_fails'])} before). Variety counted on both sides rose from {V3['variety']['sum_of_twice_the_smaller_side']} to {V4['variety']['sum_of_twice_the_smaller_side']} against the kept {V4['variety']['kept']}, and the pooled width from {V3['variety']['median_spread_ratio_all_three_pooled']} to {V4['variety']['median_spread_ratio_all_three_pooled']} against the 0.75 asked. The kept tables are byte for byte as they were except kept_readings.json, which gains each kept song's melisma share and keeps its rows. Song 53 is unchanged. Song 52's melody is unchanged; its record changes only in that table's fingerprint.")
W(f"What this window could not do. 749.111, the peak: tried and not built, as above; song 55's builds still span {g(A('55', 'range'))} semitones against an aim of {g(A('55', 'range', 'aim'))}. 749.104's fix, fitting a section's later lines to its earlier bars, with their melismas: still untried outside the engine, and 749.109, 749.101 and song 54's steps wait on it. Song 55's repeated bars moved away from its aim when it was given its aimed song's melismas. 749.103: not met, though it moved. The three picks all leap at or under the kept lower quartile ({l3([SG[k]['leap'] for k in T3])}), while their pools' medians sit on their aims: the pick is not yet drawn to the middle of its own pool. 749.61, song 52 in 6/8: no kept 6/8 table.")
W("")
for lead in ("WINDOW 191", "27.115", "Table HA", "933 One reading"):
    assert any(p_.text.strip().startswith(lead) or lead in p_.text[:40] for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v34.docx"); print("saved Luthier_v34.docx")
