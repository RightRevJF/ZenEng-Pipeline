import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v31.docx")
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










R = json.load(open("/home/claude/rightrevjf/zeneng-pipeline/lib/luthier/stage19_results.json")); SG = R["songs"]; K = R["kept"]; PL = R["pools"]; V2 = PL["v32"]; V1 = PL["v31"]; WH = R["where"]["kept"]; WP = R["where"]["pool"]; T3 = ("55", "54", "58"); l3 = lambda v: ", ".join(str(x) for x in v); pc = lambda x: f"{100 * x:.0f}"; g = lambda x: f"{x:g}"
nm = lambda s: s.split("_")[1] if "_" in s else s

sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v31")], "Luthier v31", "Luthier v32")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 31"))], "LUTHIER — VERSION 31", "LUTHIER — VERSION 32")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("188 Windows", "189 Windows"), ("Windows 1–188", "Windows 1–189"), ("188 scientific research windows", "189 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v203 (Luthier v32)")
set_cell(row.cells[1], f"THE AIMED SONG'S OWN SHAPE. The songwriting session's list for this window (749.98 to 749.104). Each 4/4 song already aims at one kept song; it now takes more of that song's shape from it. 924 (749.102): the page floor reads each build as sung, melismas placed, as the kept tunes in its table were read. 925 (749.98): the chorus's lift over the verse is the aimed song's own, known for {K['lifts_known']} of the {K['songs']} kept songs. 926 (749.99): one pitch may repeat as long as it does in the aimed song (to ten at most), counted across the lines; before, never past three. 927 (749.100): the tops are set so the song spans the aimed song's range, each part's centre follows its top, and a fresh line steps a little more ({g(SG['55']['moves']['step'])}) and leaps more ({g(SG['55']['moves']['leap'])}). The picks' ranges are {l3([SG[k]['range'] for k in T3])} semitones against aims of {l3([g(SG[k]['range_aim']) for k in T3])} ({l3([SG[k]['range_before'] for k in T3])} before). A random pick from the pools fails the soundness rule {round(100 * V2['neighbour_fails'], 1)} times in a hundred ({round(100 * V1['neighbour_fails'], 1)} before). A STUDY, not a build (749.104): kept tunes sing a figure again from within two bars in {pc(WH['within_2_bars'][1])} of their repeats in a hundred and from more than sixteen bars back in {pc(WH['over_16_bars'][1])}; the builds of songs 55 and 54 do so in {l3([pc(WP[k]['within_2_bars']['median']) for k in ('55', '54')])} and in {l3([pc(WP[k]['over_16_bars']['median']) for k in ('55', '54')])}: their repeats are whole sections come round again, and the near answer is missing. That is the next fix. Carried: 749.103, 749.104's fix, 749.101, 749.61.")

after_par("27.112", [
    (f" The aimed song's own shape (Window 189; Table GY; studies/repeated_figures). Each 4/4 song aims at one kept song drawn from the kept readings. THE PAGE FLOOR AS SUNG (924): the floor of 27.112 reads a build with its melismas placed, as the kept tunes of its table were read. THE LIFT (925): where the aimed song's chorus lift over its verse is known ({K['lifts_known']} of {K['songs']} kept songs; tables/metre_atlas/kept_readings.json, lifts), the song's plan takes that lift, inside the old limits; where it is not known the lift is drawn as before. THE RUN (926): one pitch may repeat as long as the aimed song's longest run, between three and ten, counted across the lines and tested on the whole build as sung; a song with no aim keeps the old cap. THE RANGE AND THE MOVES (927): the parts' tops are set so that floor to top spans the aimed song's range and one semitone over; each part's centre rises half as far as its top; a line keeps to its register as closely as a song of that range would (spread 50 times the square of the aimed range over the kept median, between 0.6 and 2.5 times); a move by step is weighted {g(SG['55']['moves']['step'])} and a leap of a fourth or more {g(SG['55']['moves']['leap'])}. Tested: the soundness rule on the picks and on the pools.", "27.113"),
])

P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 189: THE AIMED SONG'S OWN SHAPE", H1)
W("The list", H2)
W("The songwriting session read Window 188, merged it, rebuilt song 58 and sent its list: three new findings (749.102 to 749.104) and five carried (749.98 to 749.101, 749.61). It agreed that the page gate belongs in the engine as a floor, and it corrected one reading of mine: by a random pick from the pools the figure memory does not draw the songs toward the kept middle (19 checks outside the middle half before and after). This window answers four findings with fixes, one with the study it asked for first, and carries the rest with reasons.")
W("The page floor reads the notes as sung (924; 749.102)", H2)
W(f"The kept tunes in the page gate's table are the tunes as sung. The floor read Luthier's builds before their melismas were placed. It now reads them after. Builds read and passed in songs 55, 54 and 58: {l3([str(SG[k]['page_gate']['passed']) + ' of ' + str(SG[k]['page_gate']['read']) for k in T3])} ({l3([str(SG[k]['page_gate_before']['passed']) + ' of ' + str(SG[k]['page_gate_before']['read']) for k in T3])} in Window 188).")
W("The lift from the aimed song (925; 749.98)", H2)
W(f"A song's chorus sits over or under its verse by a lift that was drawn from the kept songs' lifts at large, while everything else aimed at one kept song. The kept table now carries each kept song's own lift where it has both a verse and a chorus ({K['lifts_known']} of {K['songs']}), and the plan takes the aimed song's. Songs 55, 54 and 58 aim at {l3([nm(SG[k]['aims_at']) for k in T3])}, whose lifts are {l3([g(SG[k]['kept_lift']) for k in T3])} semitones; as sung the picks' choruses stand {l3([g(SG[k]['lift_sung']) for k in T3])} over their verses. The plan's gate allows two semitones either way, and the limits on a lift (three down, four up) are unchanged, so song 54's aim of {g(SG['54']['kept_lift'])} is asked at -3.")
W("A pitch repeats as long as it does in the aimed song (926; 749.99)", H2)
W(f"No line could hold one pitch past three notes, and a fresh line not past two. Kept tunes' longest runs are {l3([g(x) for x in K['run_10_25_50_75_90']])} notes at the 10th, 25th, middle, 75th and 90th. The cap is now the aimed song's own longest run, between three and ten, and it is counted across the lines and tested on the whole build as sung. The aimed songs' runs are {l3([g(SG[k]['kept_song_run']) for k in T3])}; the picks' longest runs are {l3([SG[k]['run'] for k in T3])} ({l3([SG[k]['run_before'] for k in T3])} before).")
W("The range and the moves (927; 749.100)", H2)
W(f"The session found the pools stepping too much, leaping too little and spanning too little. The cause of the narrow span was in the registers: a part's top was moved toward the aimed song's range, but its centre stayed where it was, four semitones over its floor, so lines seldom reached the top. The tops are now set so that the song's floor to top is the aimed song's range and one semitone over, and each centre rises half as far as its top. A fresh line's steps are weighted {g(SG['55']['moves']['step'])} and its leaps of a fourth or more {g(SG['55']['moves']['leap'])} (tried: leaps at 1, 1.6; steps at 1, 1.2, 1.3; the centre fixed and following). The picks span {l3([SG[k]['range'] for k in T3])} semitones against aims of {l3([g(SG[k]['range_aim']) for k in T3])} ({l3([SG[k]['range_before'] for k in T3])} before); they move by step at {l3([SG[k]['step'] for k in T3])} (aims {l3([SG[k]['step_aim'] for k in T3])}) and by leap at {l3([SG[k]['leap'] for k in T3])} (aims {l3([SG[k]['leap_aim'] for k in T3])}).")
W(f"On the pools: builds stepping more than the kept 75th fell from {pc(V1['step_over_75'])} to {pc(V2['step_over_75'])} in a hundred, builds leaping less than the kept 25th from {pc(V1['leap_under_25'])} to {pc(V2['leap_under_25'])}. The gate on runs counted across the lines is a heavy one: it removes {l3([SG[k]['deaths'].get("926: a run of one pitch longer than the kept song's longest, across the lines", 0) for k in T3])} builds of a thousand in songs 55, 54 and 58, and {l3([SG[k]['survive'] for k in T3])} survive. Builds spanning less than the kept 25th rose, from {pc(V1['range_under_25'])} to {pc(V2['range_under_25'])}, and that is the aim at work and not a fault: of these three songs one aims at a kept song of range {g(SG['58']['range_aim'])} and one at {g(SG['54']['range_aim'])}, and their builds now reach those ranges. The pools' spread in range, set against the kept songs' spread, rose from {V1['spread']['range']} to {V2['spread']['range']}; in repeated notes from {V1['spread']['repeated notes']} to {V2['spread']['repeated notes']}. The session warned that the page floor might bind once tunes span and leap more. It does a little in song 55, whose aim is the widest: {SG['55']['page_gate']['read'] - SG['55']['page_gate']['passed']} of {SG['55']['page_gate']['read']} builds were passed over ({SG['55']['page_gate_before']['read'] - SG['55']['page_gate_before']['passed']} of {SG['55']['page_gate_before']['read']} before), none in songs 54 and 58. Range and leaps stay among its parts for now; taking them out is the session's to ask.")
W("Where kept tunes sing a figure again (the study for 749.104)", H2)
W(f"The session asked for a study before any fix: where do kept tunes' repeated figures sit? For each four-interval figure a tune has already sung, the distance back to its last singing was read on the {R['where']['kept_songs']} kept 4/4 tunes (studies/repeated_figures/where.py) and on a hundred tries at each song's builds (pool.py). In a kept tune at the median, {pc(WH['within_2_bars'][1])} repeats in a hundred come from within two bars, {pc(WH['bars_2_to_8'][1])} from two to eight bars back, {pc(WH['bars_8_to_16'][1])} from eight to sixteen and {pc(WH['over_16_bars'][1])} from further; the middle distance is {g(WH['median_back_bars'][1])} bars, and {pc(WH['exact_1_2_4_8_bars'][1])} in a hundred sit exactly one, two, four or eight bars back.")
W(f"The builds of songs 55 and 54 are different. Their repeats come from within two bars in {l3([pc(WP[k]['within_2_bars']['median']) for k in ('55', '54')])} in a hundred and from more than sixteen bars back in {l3([pc(WP[k]['over_16_bars']['median']) for k in ('55', '54')])}; the middle distance is {l3([round(WP[k]['median_back_bars']['median']) for k in ('55', '54')])} bars, and {l3([pc(WP[k]['within_2_bars']['under_kept_25th']) for k in ('55', '54')])} builds in a hundred stand under the kept lower quartile for near repeats. Their repeated figures are whole verses and choruses come round again. Song 58, which aims at a kept song that repeats much, stands with the kept tunes ({pc(WP['58']['within_2_bars']['median'])} within two bars, {pc(WP['58']['over_16_bars']['median'])} from past sixteen). One pick can mislead here: the picks of songs 55, 54 and 58 sit exactly one, two, four or eight bars back in {l3([pc(SG[k]['where']['exact_1_2_4_8_bars']) for k in T3])} repeats in a hundred, inside the kept middle half, while their pools do not.")
W("So the missing thing is named: a phrase answered by its own figure within a bar or two, and again within the section, before the section itself returns. Fitting a section's later lines to its earlier ones at those distances, by splitting and merging notes for the new words, is the fix this points to. It is not built in this window: it has not yet been tried outside the engine.")
for n_, title_, test_ in (
    ("924", "The page floor reads the notes as sung", "Test: the record says the floor read the build as sung; every pick at or over the floor."),
    ("925", "The lift from the aimed song", "Test: each plan's lift is its aimed song's, inside the old limits, where that song's lift is known; the picks' lifts within two semitones of the plan."),
    ("926", "A pitch repeats as long as it does in the aimed song", "Test: no pick's longest run of one pitch, as sung, is over its aimed song's (ten at most); a song with no aim is unchanged."),
    ("927", "The range and the moves", "Test: pool builds stepping over the kept 75th and leaping under the kept 25th both fewer than in Window 188; the soundness rule still passed on the picks and on the pools.")):
    W(f"{n_} {title_}", H2); W(test_)
W("Table GY — the three songs and the kept songs they aim at.")
rows = [("", "Song 55", "Song 54", "Song 58"), ("Aims at", *[nm(SG[k]['aims_at']) for k in T3]),
        ("Chorus lift: the kept song's; as sung", *[f"{g(SG[k]['kept_lift'])}; {g(SG[k]['lift_sung'])}" for k in T3]),
        ("Range: the kept song's; before; now", *[f"{g(SG[k]['range_aim'])}; {SG[k]['range_before']}; {SG[k]['range']}" for k in T3]),
        ("Longest run of one pitch: the kept song's; before; now", *[f"{g(SG[k]['kept_song_run'])}; {SG[k]['run_before']}; {SG[k]['run']}" for k in T3]),
        ("Moves by step: the kept song's; now", *[f"{SG[k]['step_aim']}; {SG[k]['step']}" for k in T3]),
        ("Moves by leap: the kept song's; now", *[f"{SG[k]['leap_aim']}; {SG[k]['leap']}" for k in T3]),
        ("Builds' repeats from within two bars, in 100 (kept " + l3([pc(x) for x in WH['within_2_bars']]) + ")", *[pc(WP[k]['within_2_bars']['median']) for k in T3]),
        ("Builds' repeats from over sixteen bars back, in 100 (kept " + l3([pc(x) for x in WH['over_16_bars']]) + ")", *[pc(WP[k]['over_16_bars']['median']) for k in T3]),
        ("Checks outside the kept middle half, of 23", *[str(x) for x in R['soundness']['outside_middle_half']])]
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W(f"The records. Songs 55, 54 and 58 are written again: keys {l3([SG[k]['key'] for k in T3])} ({l3([SG[k]['key_before'] for k in T3])} before); {l3([SG[k]['seconds'] for k in T3])} seconds. Their picks stand outside the kept middle half on {l3(R['soundness']['outside_middle_half'])} checks of the 23 and pass the soundness rule. Song 58 stands outside on the most, and outside the kept 10th to 90th on {R['soundness']['outside_10_90'][2]}: it aims at a narrow, much-repeating kept song and now sounds like it. A random pick from the pools fails the rule {round(100 * V2['neighbour_fails'], 1)} times in a hundred ({round(100 * V1['neighbour_fails'], 1)} before); a random pick from every build that lived, {pc(V2['random_build_fails'])} ({pc(V1['random_build_fails'])} before). The kept tables are byte for byte as they were except kept_readings.json, which gains each kept song's name and lift and keeps its rows. Song 52, in 6/8, has no aim and its melody is unchanged; its record changes only in the kept table's fingerprint and a note.")
W(f"What this window could not do. 749.103, variety counted on both sides: the session's measure is in neighbour.py and stands at {V2['variety']['sum_of_twice_the_smaller_side']} against the kept {V2['variety']['kept']}, the pooled width at {V2['variety']['median_spread_ratio_all_three_pooled']} against the 0.75 asked; the check is not met. Range and repeated notes widened because they now follow the aimed song; the rhythm checks did not (notes a bar {V2['spread']['notes a bar']}, rhythm scaling {V2['spread']['rhythm scaling']}, longest phrase {V2['spread']['longest phrase']}, stressed line ends held {V2['spread']['stressed line ends held']}), for they are set by the words and the rhythm draw, which do not yet take their values from the aimed song. That is the next step for 749.103. 749.104's fix waits on a trial of the study's finding outside the engine. 749.101, varied returns at the kept share, was not reached. The picks' lifts stand one or two semitones from the aimed songs': the plan's gate allows two. Song 55's pick spans {SG['55']['range']} semitones against an aim of {g(SG['55']['range_aim'])}. Pool builds with few bars on a figure already sung rose from {pc(V1['figure_under_25'])} to {pc(V2['figure_under_25'])} in a hundred, which the study above speaks to. 749.61, song 52 in 6/8, is carried: there is still no kept 6/8 table.")
W("")
for lead in ("WINDOW 189", "27.113", "Table GY", "927 The range"):
    assert any(p_.text.strip().startswith(lead) or lead in p_.text[:40] for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v32.docx"); print("saved Luthier_v32.docx")
