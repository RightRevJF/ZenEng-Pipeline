import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v36.docx")
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










R = json.load(open("/home/claude/rightrevjf/zeneng-pipeline/lib/luthier/stage24_results.json")); SG = R["songs"]; PL = R["pools"]; V7 = PL["v37"]; V6 = PL["v36"]; RG = V7["ranges_90"]; T3 = ("55", "54", "58"); T4 = ("55", "54", "58", "59"); l3 = lambda v: ", ".join(str(x) for x in v); pc = lambda x: f"{100 * x:.0f}"; g = lambda x: f"{x:g}"; p1 = lambda x: round(100 * x, 1)
A = lambda k, c, w="builds", src="aimpool": SG[k][src][c][w]; REP, STP, LEP, FIG, RHY = "repeated notes", "moves by step", "moves by leap", "bars on a figure already sung", "bars on a rhythm already sung"
BFm = lambda k, f, c: SG[k]["bar_fit"]["forms"][f][c]; MC = lambda k, f, c: SG[k]["melismas_carried"]["forms"][f][c]; E_, B_ = "the engine's refit", "the bar fit"; WF = "the words' fit, whole"; M0, M1 = "as the engine places them", "carried with a line sung again"
rg = lambda k: f"{p1(RG[k][0])} to {p1(RG[k][1])}"; NC, RP, RA = "neighbour choice", "a random pick from the engine's pool", "a random pick from every build that lived"

sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v36")], "Luthier v36", "Luthier v37")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 36"))], "LUTHIER — VERSION 36", "LUTHIER — VERSION 37")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("193 Windows", "194 Windows"), ("Windows 1–193", "Windows 1–194"), ("193 scientific research windows", "194 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v208 (Luthier v37)")
set_cell(row.cells[1], f"THE BAR FIT, TRIED AND NOT BUILT; THE MELISMAS CARRIED, TRIED AND BUILT. The fix that many findings waited on, fitting a returning line to its source's bars, was taken head on outside the engine with its rule written first (studies/bar_fit). The bars return, and the words' fit falls under the kept 10th in every song: the bars and the words trade against each other. It is not built. The same trial showed that, before melismas, the songs already sing their bars again as often as the songs they aim at; the shortfall is made when the melismas are placed. A second trial passed its rule and is built: 942, a line sung again takes its source's melismas. Also: 940 (749.120) every pool figure carries its 90% range (the neighbour choice fails the rule {p1(V7['neighbour_choice_fails'])} times in a hundred, range {rg(NC)}; a random pick from the engine's pool {p1(V7['random_pool_pick_fails'])}, range {rg(RP)}); 941 (749.121) each weight is fitted against its own band, and song 54's fit no longer keeps its starting weights. The picks are sound, with no lean. Carried: 749.104's first half (now a question about the lyric), 749.109, 749.111, 749.116, 749.103, 749.101, 749.61.")

after_par("27.117", [
    (f" The ranges; each weight on its own; the melismas carried (Window 194; Table HD; studies/bar_fit). THE RANGES (940): neighbour.py resamples each song's pool, with replacement at its own size, two hundred times, reads each pool figure again on every resample, and gives the 5th and 95th percentiles as the figure's 90% range; a fix's check on a pool figure is read against the last window's range and not its point. EACH WEIGHT ON ITS OWN (941): in the fit of 27.114 each weight's fresh-line share is tested against its own kept 10th to 90th, and each weight is bisected on its own between its last value inside and its nearest value outside; a weight whose aim lies past the band stops at the band's edge and the others go on; a round counts as at the edge when its fresh lines read within 0.03 of the band, which is what forty builds can tell. THE MELISMAS CARRIED (942): a line sung again to new words takes its source's melismas, syllable for syllable, where the two lines have the same number of syllables, as a copied line does (919). Tested: the soundness rule on the picks and by both pool figures; song 59 read and not fitted.", "27.118"),
])

P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 194: THE BAR FIT, TRIED AND NOT BUILT; THE MELISMAS CARRIED", H1)
W("A change of course", H2)
W("Windows 189 to 193 answered the session's lists item by item, and the hold-out stood where it began: sound, and far nearer the kept middle than a kept song is. Two faults lay under most of the items. The songs are too like the middle (749.103), and a line that returns does not repeat as a kept song's does (749.104). I asked the session whether to stop answering small items and take those two head on. Its answer: take 749.104 head on, outside the engine, with its rule written first; do not take 749.103 head on, for it is the sum of the checks the aim does not set, and pushing on it would game the measure. It is to be read as the outcome.")
W("The ranges (940; 749.120)", H2)
W(f"The pools the figures are read on hold some fifty to ninety builds, and which builds land in a pool moves a rate more than a fix does. neighbour.py now gives each figure's 90% range by resampling the pools. This window: the neighbour choice fails the soundness rule {p1(V7['neighbour_choice_fails'])} times in a hundred (range {rg(NC)}); a random pick from the engine's pool {p1(V7['random_pool_pick_fails'])} (range {rg(RP)}); a random pick from every build that lived {p1(V7['random_living_build_fails'])} (range {rg(RA)}). Window 193's figures were {p1(V6['neighbour_choice_fails'])}, {p1(V6['random_pool_pick_fails'])} and {p1(V6['random_living_build_fails'])}; the session's reading of Window 193 put the random pool pick's range at 2.6 to 8.6. Read so, Window 193's \"not met\" on the random pool pick (5.1 against 2.5 asked) was inside the noise, and so is every window-to-window move in these figures since Window 189.")
W("Each weight against its own band (941; 749.121)", H2)
W(f"The fit tested the fresh lines against the kept band on all three moves at once and drew all three weights back together. Where one weight's aim lies past the band, as song 54's steps do, its overshoot pulled the others back, and song 54 kept its starting weights. Each weight is now tested and bisected on its own. Song 54's fit keeps round {SG['54']['kept_round']}, with weights {g(SG['54']['moves']['step'])}, {g(SG['54']['moves']['leap'])} and {g(SG['54']['moves']['repeat'])} for a step, a leap and a repeat. Every living build's repeated notes, songs 55, 54, 58, 59: {l3([A(k, REP) for k in T4])} against aims of {l3([A(k, REP, 'aim') for k in T4])} ({l3([A(k, REP, src='aimpool_v36') for k in T4])} before); steps {l3([A(k, STP) for k in T4])} against {l3([A(k, STP, 'aim') for k in T4])}; leaps {l3([A(k, LEP) for k in T4])} against {l3([A(k, LEP, 'aim') for k in T4])}.")
W("The bar fit, tried outside the engine and not built (749.104 with 749.122)", H2)
W("When a line returns to new words the engine refits its source's notes to them: over the whole line it chooses which notes to split, drop or lead into by where the new words' stresses fall. That serves the words and moves notes all along the line. The bar fit keeps the source's bars instead: it changes only as many notes as the syllable counts differ by, splits the longest note, drops the note the bar misses least, and never makes a repeat by a split or a drop. The rule was written first (studies/bar_fit/PREDICTION.md): the bars must move toward the aimed song's; the returning lines must not repeat more than the fresh lines by over 0.03; the words must still sit.")
W(f"It did what it was made to do. Read before melismas, the builds' bars on a rhythm already sung rose in every song: {l3([f'{BFm(k, E_, RHY)} to {BFm(k, B_, RHY)}' for k in T4])} (songs 55, 54, 58, 59); on a figure already sung {l3([f'{BFm(k, E_, FIG)} to {BFm(k, B_, FIG)}' for k in T4])}. The returning lines' excess of repeated notes over the fresh lines fell from {SG['55']['bar_fit']['returning_over_fresh_before']} to {SG['55']['bar_fit']['returning_over_fresh']} in song 55 and from {SG['54']['bar_fit']['returning_over_fresh_before']} to {SG['54']['bar_fit']['returning_over_fresh']} in song 54. And it failed its rule twice over. First, read before melismas, songs 55 and 54 were already at or over their aimed songs on bars sung again ({BFm('55', E_, FIG)} against {SG['55']['bar_fit']['aim'][FIG]}; {BFm('54', E_, FIG)} against {SG['54']['bar_fit']['aim'][FIG]}), so more was the wrong way for them. Second, and worse, at a cost the rule had not named: the words' fit, whole, fell from {l3([BFm(k, E_, WF) for k in T3])} to {l3([BFm(k, B_, WF) for k in T3])}, under the kept 10th (0.152) in every song.")
W("So the bars and the words trade against each other. The engine's refit moves notes so that the new words' stresses fall where kept songs sing them; keeping the bars undoes that. A kept song has both, and the only way to have both is for the later verse's words to be written to the first verse's stresses. That is a fact about the lyric and not the tune. The next question for 749.104 is therefore on the lyric's side: how closely do kept songs' returning lines match their sources stress for stress, and how closely do Luthier's lyrics? It is not built, and the finding redirects it.")
W("The melismas carried with a line sung again (942)", H2)
W(f"The first trial showed something else. Before melismas the songs sing their bars again as often as the songs they aim at; the shortfall that every window since 189 has reported is in the tune as sung. A copied line takes its source's melismas (919). A line sung again to new words did not: its melismas were drawn afresh, and each was a bar that no longer matched. A second rule was written (PREDICTION2.md) and a second trial read the same builds both ways. As sung, bars on a figure already sung: {l3([f'{MC(k, M0, FIG)} to {MC(k, M1, FIG)}' for k in T4])}; on a rhythm already sung: {l3([f'{MC(k, M0, RHY)} to {MC(k, M1, RHY)}' for k in T4])}; the words' fit: {l3([f'{MC(k, M0, WF)} to {MC(k, M1, WF)}' for k in T4])}. Both checks held. The gain is small, two or three hundredths, and it costs nothing, so it is built. On the hold-out it moves bars on a figure already sung away from its aim (0.32), and that is recorded.")
for n_, title_, test_ in (
    ("940", "Every pool figure with its range", "Test: every pool figure in the paper carries its 90% range, and a check on one is read against the last window's range."),
    ("941", "Each weight against its own band", "Test: song 54's kept round is not round 1; its builds' repeated notes at or under the kept 25th (0.210); its fresh lines' steps at the band's edge."),
    ("942", "A line sung again takes its source's melismas", "Test: as sung, bars on a figure already sung and on a rhythm already sung rise in at least two of songs 55, 54 and 58 and fall by more than 0.01 in none; the words' fit falls by more than 0.01 in none.")):
    W(f"{n_} {title_}", H2); W(test_)
W("Table HD — the four songs: every living build's median against the aimed kept song (aim; Window 193; now). Song 59 is the hold-out.")
nm = lambda s: s.split("_")[1] if "_" in s else s
rows = [("", "Song 55", "Song 54", "Song 58", "Song 59 (hold-out)"), ("Step; leap; repeat weights", *[f"{g(SG[k]['moves']['step'])}; {g(SG[k]['moves']['leap'])}; {g(SG[k]['moves']['repeat'])}" for k in T4])]
for c, lab in ((REP, "Repeated notes"), (STP, "Moves by step"), (LEP, "Moves by leap"), ("range", "Range"), (FIG, "Bars on a figure already sung"), (RHY, "Bars on a rhythm already sung"), ("rhythm scaling", "Rhythm scaling")):
    rows.append((lab, *[f"{g(A(k, c, 'aim'))}; {g(A(k, c, src='aimpool_v36'))}; {g(A(k, c))}" for k in T4]))
rows.append(("Checks outside the kept middle half, of 21 read on single kept songs: Window 193; now", *[f"{SG[k]['compare_v36']['outside_middle_half']}; {SG[k]['compare']['outside_middle_half']}" for k in T4]))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
leans = R['soundness']['engine']['lean_beyond_25th_75th']
W(f"The records. Songs 55, 54, 58 and 59 are written again: keys {l3([SG[k]['key'] for k in T4])} ({l3([SG[k]['key_before'] for k in T4])} before); ranges {l3([SG[k]['range'] for k in T4])} semitones against aims of {l3([g(SG[k]['range_aim']) for k in T4])}. The picks of songs 55, 54 and 58 stand outside the kept middle half on {l3(R['soundness']['outside_middle_half'])} checks of the 23 and pass the soundness rule" + (f", with all three leaning the same way past the kept quartiles on {' and '.join(x[0] for x in leans)}" if leans else ", with no check on which all three lean the same way past the kept quartiles") + f". The hold-out, read and not fitted: song 59's pick stands outside the kept middle half on {SG['59']['compare']['outside_middle_half']} checks of 21 ({SG['59']['compare_v36']['outside_middle_half']} before). Two-sided variety is {V7['variety']['sum_of_twice_the_smaller_side']} against the kept {V7['variety']['kept']} ({V6['variety']['sum_of_twice_the_smaller_side']} before). The kept tables and song 53 are byte for byte as they were. Song 52's record changes, and this is 942: its lines sung again now take their sources' melismas; its notes before melismas are the same.")
c54 = A('54', REP) <= 0.21
W(f"What this window could not do. 941's check on song 54's repeated notes: {A('54', REP)} against the kept 25th of 0.210, " + ("met" if c54 else "not met") + f". The fits are noisy from window to window: the hold-out's repeated notes went the wrong way ({A('59', REP, src='aimpool_v36')} to {A('59', REP)} against an aim of {A('59', REP, 'aim')}), song 55's builds step {A('55', STP)} against {A('55', STP, 'aim')}, and song 58's pick spans {SG['58']['range']} semitones against an aim of {g(SG['58']['range_aim'])}. A fit read on forty builds a round moves by two or three hundredths on its own. 749.104's first half, bars returning: tried and not built; it is now a question about the lyric. 749.109 waited on it and waits still. 749.103 was read and not pushed on: the hold-out stands outside the kept middle half on {SG['59']['compare']['outside_middle_half']} checks of 21, where a kept song stands on ten. 749.111's third trial waits on a second practice song with a wide aim, which the session has offered to write. 749.116, the band under the break, and 749.61, the 6/8 table: not reached.")
W("")
for lead in ("WINDOW 194", "27.118", "Table HD", "942 A line"):
    assert any(p_.text.strip().startswith(lead) or lead in p_.text[:40] for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v37.docx"); print("saved Luthier_v37.docx")
