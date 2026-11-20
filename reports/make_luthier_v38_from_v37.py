import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v37.docx")
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










R = json.load(open("/home/claude/rightrevjf/zeneng-pipeline/studies/verse_match/in_engine_943.json")); SG = R["songs"]; PL = R["pools"]; V8 = PL["v38"]; V7 = PL["v37"]; RG = V8["ranges_90"]; RG7 = V7["ranges_90"]; T3 = ("55", "54", "58"); T4 = ("55", "54", "58", "59"); l3 = lambda v: ", ".join(str(x) for x in v); pc = lambda x: f"{100 * x:.0f}"; g = lambda x: f"{x:g}"; p1 = lambda x: round(100 * x, 1)
A = lambda k, c, w="builds", src="aimpool": SG[k][src][c][w]; REP, STP, LEP, FIG, RHY = "repeated notes", "moves by step", "moves by leap", "bars on a figure already sung", "bars on a rhythm already sung"; WF = "the words' fit, whole"; ER = "the engine's refit"; ON = "one note's worth"
NC, RP, RA = "neighbour choice", "a random pick from the engine's pool", "a random pick from every build that lived"; rg = lambda G, k: f"{p1(G[k][0])} to {p1(G[k][1])}"; KV = R["kept"]["verse_match"]; KN = R["kept"]["near"]
B3 = lambda k, f, c: SG[k]["bar_fit3"]["forms"][f][c]; t2 = lambda k: SG[k]["trial2"]; t1 = lambda k: SG[k]["trial1"]; bw = lambda k: f"{g(SG[k]['borrow']['figure'])} and {g(SG[k]['borrow']['rhythm'])}"
inside = lambda G, x: G[0] <= x <= G[1]

sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v37")], "Luthier v37", "Luthier v38")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 37"))], "LUTHIER — VERSION 37", "LUTHIER — VERSION 38")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("194 Windows", "195 Windows"), ("Windows 1–194", "Windows 1–195"), ("194 scientific research windows", "195 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v209 (Luthier v38)")
set_cell(row.cells[1], f"THERE WAS NO FAULT OF REPETITION. A window of measuring, done without a list, at the writer's word, to settle what Window 194 left open. No change is made to how songs are built; the records are Window 194's, byte for byte. Four findings. The bars and the words trade on the tune's side with no free part (a third trial of the bar fit; not built). The lyric is not the fault: Luthier's later verses match their first verses bar for bar as well as kept songs' do. The songs never repeated too little: they sing a bar's rhythm again as often as kept songs at large; the shortfall reported since Window 189 was against each song's own aimed song, which is the fault of sameness (749.103) seen from one side. And 943, the two borrows fitted to the aimed song, passed its trial outside the engine on the second try and held on the hold-out, was built in, and was withdrawn: in the engine a pick from the pools failed the soundness rule {p1(V8['neighbour_choice_fails'])} times in a hundred (range {rg(RG, NC)}; Window 194: {p1(V7['neighbour_choice_fails'])}, {rg(RG7, NC)}), under the standard's bar. More borrowing moves the bars toward the aim and rhythm scaling away from it. The code is kept, switched off. Carried: 749.109, 749.111, 749.116, 749.103, 749.101, 749.61.")

after_par("27.118", [
    (f" The borrows fitted to the aimed song: tried, built in, and withdrawn (Window 195; Table HE; studies/verse_match, studies/bar_fit). THE BORROWS (943, off): a fresh line may sing an earlier line of its section again (the figure borrow, 818) or take its rhythm with new notes (the rhythm borrow). Both are the same for every song (0.8 and 0). The fit of 943 tries five settings of the two (0 and 0; 0.8 and 0; 1 and 0; 0.5 and 0.5; 0 and 1), each on a short run that draws until forty builds pass the gates, reads each as sung, and keeps the setting nearest the aimed song on bars on a figure already sung and on a rhythm already sung together, among the settings whose words' fit is no more than 0.03 under the old setting's. It is in the code (song_from_lyric.py, BORROW_FIT) and is switched off, because with it the pools fall under the soundness standard of 27.111. With it off the engine is Window 194's.", "27.119"),
])

P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 195: THERE WAS NO FAULT OF REPETITION", H1)
W("Why this window has no list", H2)
W("Window 194 ended on a question: the bar fit made the bars return and cost the words, and I inferred that a kept song has both because its later verses are written to its first verse's stresses, so the fault lay in the lyric. Jason asked whether I could settle it without the songwriting session, and to go ahead. This window is that work. Every trial had its rule written first; song 59 was read and never fitted to. The inference was wrong, and finding that out was the most useful thing in the window.")
W("The bar fit where the words allow: tried and not built", H2)
W(f"If keeping a returning line's bars costs the words, keep them only where it does not. For each returning line both fits were made and scored as the engine scores a refit, and the bar fit was taken only where the words sat at least as well (studies/bar_fit/PREDICTION3.md). It was taken in {l3([pc(B3(k, 'strict', 'bar_fit_taken_share')) for k in T3])} lines in a hundred, the words held, and the bars did not rise: bars on a rhythm already sung went {l3([str(B3(k, ER, RHY)) + " to " + str(B3(k, "strict", RHY)) for k in T3])}. Where the bar fit seats the words as well as the refit, it is nearly the same fit. Given one moved note's worth of leave, it was taken in nearly every line, the bars rose, and the words' fit fell to {l3([B3(k, ON, WF) for k in T3])}. On the tune's side the trade has no free part.")
W("Is it the lyric? No", H2)
W(f"Verse 1 was set against each later verse, bar by bar, in the {R['kept']['verse_songs']} kept songs with two verses or more and in Luthier's four songs (studies/verse_match/match.py). Bars with the same number of syllables: kept songs {l3(KV['bars_same_syllable_count'][1:4])} at the quartiles; songs 55, 54, 58, 59 at {l3([SG[k]['verse_match']['record']['bars_same_syllable_count'] for k in T4])}. Bars sung on the same rhythm: kept {l3(KV['bars_same_rhythm'][1:4])}; Luthier's {l3([SG[k]['verse_match']['record']['bars_same_rhythm'] for k in T4])}, more than {l3([pc(SG[k]['verse_match']['share_of_kept_songs_at_or_under']['bars_same_rhythm']) for k in T4])} kept songs in a hundred. Luthier's later verses match their first verses as well as kept songs' do, and on rhythm better than most. Kept songwriters do not hold their later verses to the first verse's bars more closely than Luthier does. The lyrics are not at fault, and nothing need change in how they are written.")
W("Do the songs repeat too little at all? No", H2)
W(f"Then the plainest question, which should have been asked first. Of the bars a tune sings, how many are on a rhythm it has sung before? Kept tunes: {l3(KN['sung_again'])} at the quartiles. Songs 55, 54, 58, 59: {l3([SG[k]['near']['sung_again'] for k in T4])} (near.py, read on Window 194's records). By how far back the rhythm comes from, the songs stand in the kept middle half on nearly every row. There was never a general fault of repetition. The shortfall reported in every window since 189 was against each song's own aimed song. Songs 54 and 58 aim at kept songs that repeat far more than most, and the engine gave every song the same amount of repeating whatever it aimed at. This is the fault of sameness, 749.103, seen from one side: where the aim does not reach, every song lands at the kept middle.")
W("The borrows fitted to the aimed song (943; 749.109)", H2)
W(f"One dial already in the engine moves these readings a long way: how many fresh lines sing an earlier line of their section again, and how many take its rhythm. It stood at 0.8 and 0 for every song. Across its range a song's bars on a figure already sung move by about a tenth (reach.py). Window 190 had tried setting it from the aim by a formula and gave it up; a fit is a different thing. The rule was written (studies/verse_match/PREDICTION.md): fit the two borrows to the aimed song on one set of draws, read on another, against the fixed setting; the gap to the aim must shrink in two of the three practice songs and grow in none, the words' fit must not fall by more than 0.03, and eight builds in ten must still pass. Because I had looked at the dial before writing the rule, a prediction was also written for the hold-out, which aims low where the practice songs aim high: its fit would choose less borrowing, and its gap would shrink. If the practice songs passed and the hold-out's prediction failed, it would not be built.")
W(f"The first trial moved every song nearer its aim and the hold-out's prediction held, and it failed: song 55's words' fit fell {abs(t1('55')['words_fit_change'])} when its fit chose to borrow every line. It was not built on that. The amendment, written as a second rule (PREDICTION2.md), is that the fit may not buy bars with the words: only settings whose words' fit is within 0.03 of the old setting's may be chosen. The second trial, on new draws, held on every check. Gap to the aim, in kept widths, before and after: {l3([str(t2(k)["the_engines_setting"]["gap"]) + " to " + str(t2(k)["the_fitted_setting"]["gap"]) for k in T4])} (songs 55, 54, 58, 59). The words' fit changed by {l3([t2(k)['words_fit_change'] for k in T4])}. The hold-out's fit chose no borrowing at all; its gap halved, and {pc(t2('59')['builds_share'] - 1)} in a hundred more of its builds passed the gates. So it was built.")
W("Built into the engine, and withdrawn", H2)
W(f"In the engine the fit chose, for songs 55, 54, 58 and 59, {l3([bw(k) for k in T4])} for the figure borrow and the rhythm borrow. Every living build's bars on a figure already sung: {l3([A(k, FIG) for k in T4])} against aims of {l3([A(k, FIG, 'aim') for k in T4])} ({l3([A(k, FIG, src='aimpool_v37') for k in T4])} before); on a rhythm already sung: {l3([A(k, RHY) for k in T4])} against {l3([A(k, RHY, 'aim') for k in T4])} ({l3([A(k, RHY, src='aimpool_v37') for k in T4])} before). The picks passed the soundness rule. The pools did not hold. Each figure with its 90% range: the neighbour choice failed the rule {p1(V8['neighbour_choice_fails'])} times in a hundred ({rg(RG, NC)}), where Window 194 stood at {p1(V7['neighbour_choice_fails'])} ({rg(RG7, NC)}); a random pick from the engine's pool {p1(V8['random_pool_pick_fails'])} ({rg(RG, RP)}), against {p1(V7['random_pool_pick_fails'])} ({rg(RG7, RP)}). The standard asks ninety passes in a hundred; both fell just under it, and both rose clear of Window 194's ranges. This is the first use of the ranges of 940, and they did their work: this rise is not noise.")
W(f"The cause can be read in the table. More borrowing moves a song's bars toward its aim and its rhythm scaling away. The builds' rhythm scaling went from {l3([A(k, 'rhythm scaling', src='aimpool_v37') for k in T3])} to {l3([A(k, 'rhythm scaling') for k in T3])} in songs 55, 54 and 58, against aims of {l3([A(k, 'rhythm scaling', 'aim') for k in T3])} and a kept middle of 0.656. Two of the three practice songs aim at kept songs that repeat much, the fit gave them all the borrowing there is, and all three songs then leaned low on rhythm scaling together, which is what the soundness rule forbids: in a random pick from the pools all three stood under the kept 10th on rhythm scaling 9.9 times in a hundred, where they had 1.8, and that one check is nearly the whole of the failures. Window 190 dropped the borrows-by-formula for the same reason and said so in a line; this window has measured it. The kept songs that repeat most have high rhythm scaling: Bird Dog sings {pc(A('58', RHY, 'aim'))} bars in a hundred on a rhythm already sung with a rhythm scaling of {A('58', 'rhythm scaling', 'aim')}. Luthier's songs, made to repeat by borrowing whole lines, get lower. So the engine's way of repeating is not the kept songs' way, and that, not the amount, is the thing to study next. 943 is withdrawn. Its code stays, switched off, and with it off every record is Window 194's, byte for byte.")

for n_, title_, test_ in (
    ("943", "The borrows fitted to the aimed song (withdrawn)", "Test: outside the engine, on new draws: the summed gap to the aim shrinks in at least two of songs 55, 54 and 58 and grows by more than 0.05 kept widths in none; the words' fit falls by no more than 0.03; eight builds in ten still pass; on the hold-out the fit chooses less borrowing and the gap shrinks: met on the second trial. In the engine: the soundness rule on the picks, met; by both pool figures, ninety passes in a hundred: not met. Withdrawn."),):
    W(f"{n_} {title_}", H2); W(test_)
W("Table HE — the four songs with 943 built in, before it was withdrawn: every living build's median against the aimed kept song (aim; Window 194; with 943). Song 59 is the hold-out.")
rows = [("", "Song 55", "Song 54", "Song 58", "Song 59 (hold-out)"), ("Figure borrow and rhythm borrow the fit chose (0.8 and 0 in the engine)", *[bw(k) for k in T4])]
for c, lab in ((FIG, "Bars on a figure already sung"), (RHY, "Bars on a rhythm already sung"), ("distinct rhythms over bars", "Distinct rhythms over bars"), ("rhythm scaling", "Rhythm scaling"), (REP, "Repeated notes"), (STP, "Moves by step"), (LEP, "Moves by leap"), ("range", "Range")):
    rows.append((lab, *[f"{g(A(k, c, 'aim'))}; {g(A(k, c, src='aimpool_v37'))}; {g(A(k, c))}" for k in T4]))
rows.append(("Builds that survive, of 1,000: Window 194; with 943", *[f"{SG[k]['survive_before']}; {SG[k]['survive']}" for k in T4]))
rows.append(("Checks outside the kept middle half, of 21 read on single kept songs: Window 194; with 943", *[f"{SG[k]['compare_v37']['outside_middle_half']}; {SG[k]['compare']['outside_middle_half']}" for k in T4]))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W(f"The records. No record changes in this window. With 943 switched off, songs 52, 54, 55, 58 and 59 rebuild byte for byte as Window 194 left them, and so do the kept tables and song 53. The figures of Window 194 stand: the neighbour choice fails the soundness rule {p1(V7['neighbour_choice_fails'])} times in a hundred ({rg(RG7, NC)}); a random pick from the engine's pool {p1(V7['random_pool_pick_fails'])} ({rg(RG7, RP)}).")
W(f"What this window could not do. It built nothing that stayed. What it leaves is a corrected account. For six windows the papers said the songs repeat too little; they do not. For one window the papers said the lyric might be the cause; it is not. The one real fault under all of it is that the aim reaches a song's pitch moves and not its rhythm, so on rhythm every song comes out at the kept middle, or, pushed by the borrows, below it. The next study is how the kept songs that repeat much keep a high rhythm scaling, and it should be done outside the engine with its rule written first. The practice songs are three and the hold-out one; a second and third practice song, with wide and narrow aims, would test every finding here better than more work on these. 749.111, the peak; 749.116, the band under the break; 749.101; 749.61: not reached. The songwriting session has not reviewed this window.")
W("")
for lead in ("WINDOW 195", "27.119", "Table HE", "943 The borrows"):
    assert any(p_.text.strip().startswith(lead) or lead in p_.text[:40] for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v38.docx"); print("saved Luthier_v38.docx")
