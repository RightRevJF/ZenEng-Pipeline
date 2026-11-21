import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v38.docx")
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










RT = "/home/claude/rightrevjf/zeneng-pipeline/"; J = lambda p: json.load(open(RT + p)); import subprocess, re
WS = J("studies/words_to_shape/result.json"); OU = J("studies/words_to_shape/ours.json"); SE = J("studies/shape_from_the_song/sections.json"); OW = J("studies/shape_from_the_song/own.json"); OB = J("studies/shape_from_the_song/own_with_borrows_from_words.json")
N9 = J("studies/soundness/neighbour_v39.json"); NB = J("studies/shape_from_the_song/neighbour_with_borrows_from_words.json"); N7 = J("studies/soundness/neighbour_v37.json"); CP = J("studies/holdout59/compare.json"); snd = open("/tmp/claude-0/t32/sound.txt").read()
T4 = ("55", "54", "58", "59"); FN = {"55": "lyric55.json", "54": "lyric54.json", "58": "lyric58.json", "59": "lyric59.json"}; PTH = {"55": "songs/p65/lyric55", "54": "songs/p64/lyric54", "58": "songs/p68/lyric58", "59": "songs/p69/lyric59"}
REC = {k: J(PTH[k] + ".song.json") for k in T4}; OLD = {k: json.loads(subprocess.check_output(["git", "-C", RT, "show", "HEAD~3:" + PTH[k] + ".song.json"])) for k in T4}
l3 = lambda v: ", ".join(str(x) for x in v); pc = lambda x: f"{100 * x:.0f}"; g = lambda x: f"{x:g}"; p1 = lambda x: round(100 * x, 1); PK = "the engine's pool"
def pool(N): return dict(nc=N["neighbour"]["rule_fails_share"], rp=[x["rule_fails_share"] for k, x in N["a_random_pick_from"].items() if k.startswith(PK)][0], rg=N["ranges_90"], var=N["variety_two_sided"]["sum_of_twice_the_smaller_side"])
P9, PB, P7 = pool(N9), pool(NB), pool(N7); rg = lambda P_, k: f"{p1(P_['rg'][k][0])} to {p1(P_['rg'][k][1])}"; NC, RP = "neighbour choice", "a random pick from the engine's pool"
C = lambda k, c, w="builds_median", O=OW: O[FN[k]]["checks"][c][w]; rd = WS["readings"]; rng_ = lambda R_: max(n["midi"] for n in R_["melody"]["notes"]) - min(n["midi"] for n in R_["melody"]["notes"])
out_half = [int(x) for x in re.findall(r"outside the middle half (\d+)", snd)]; FIG, RHY = "bars on a figure already sung", "bars on a rhythm already sung"

sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v38")], "Luthier v38", "Luthier v39")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 38"))], "LUTHIER — VERSION 38", "LUTHIER — VERSION 39")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("195 Windows", "196 Windows"), ("Windows 1–195", "Windows 1–196"), ("195 scientific research windows", "196 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v210 (Luthier v39)")
set_cell(row.cells[1], f"THE SHAPE FROM THE SONG. Since Window 187 each 4/4 song drew one kept song and took its numbers. Jason asked whether the engine was picking a song to emulate; it was not copying a note, and it was taking one song's shape. His ruling: other songs are a style guide, not a model; the engine's own theory must write the music; the writer may override, and the default is to trust the engine. A study asked first whether a song's own words decide its tune's shape (studies/words_to_shape, rule written first, songs held out by artist). They do in part: how much a tune sings its bars again is predicted by how much its words repeat (+{rd[FIG]['held_out_rank_correlation']}, +{rd[RHY]['held_out_rank_correlation']}), and its range by its length and era (+{rd['range']['held_out_rank_correlation']}); how it moves is not. 944: no kept song is drawn. A song's range comes from its own words; its movement is the middle of what kept melodies do, the paper's invariants, unless the writer asks for smooth, leaping or chant; the chorus's lift is the kept middle. The paper's rule that verses step and choruses leap was tested on the kept songs and does not hold; it is struck. The picks are sound. Setting repetition from the words was tried and breaks the pools, as in Window 195; it is recorded and not acted on. One fault now stands plain with the draw's scatter gone: every Luthier song's rhythm scaling is low.")

after_par("27.119", [
    (f" The shape from the song (Window 196; Table HF; lib/luthier/words_to_shape.py; tables/kept_words_to_shape.json; studies/words_to_shape, studies/shape_from_the_song). NO SONG IS DRAWN (944): the draw of one kept song (920) and everything taken from it (the lift 925, the run 926, the range 927, the melismas 932, the aim of the fits 930 and 936) is replaced. THE RANGE: from the song's own words and form, by a ridge regression fitted on the kept 4/4 songs as a body (twelve predictors: syllables in the song, syllables a line and their unevenness, syllables a word, different words over all words, lines said again, words in a three-word run already sung, kinds of section, the chorus's share, a bridge, mode, year held at the kept middle year), held inside the kept 10th to 90th; the parts' tops are set to it as 927 set them. THE MOVEMENT: the shares of steps, leaps and repeated notes, the longest run of one pitch and the share of syllables on two notes are the kept middle, and the fit of 27.114 brings each song's builds to them. The writer may set \"movement\" in the lyric file to smooth (steps at the kept upper quartile, leaps at the lower), leaping (the reverse) or chant (repeated notes and the longest run at the kept upper quartile); the default is the engine's. THE LIFT: the kept middle lift of the chorus over the verse. REPETITION: what the words ask for bars sung again is written in the record (target, from_its_words) and is not yet acted on; the borrows stay at 0.8 and 0. The old way is kept in the code for the record (SHAPE_FROM). Tested: the soundness rule on the picks; the pools by both figures with their ranges; song 59 read and not fitted.", "27.120"),
])

P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 196: THE SHAPE FROM THE SONG", H1)
W("The question that sent the engine back", H2)
W("After Window 195 Jason asked a plain question: the engine is not just picking a song to emulate, is it? It was not copying any song's notes, tune, chords or rhythm. But since Window 187 each 4/4 song had drawn one kept song by the title's seed and taken that song's numbers as its own: its range, its shares of steps, leaps and repeated notes, its lift, its longest run, its melismas. Song 58 was told to be shaped like Bird Dog. The draw had been made to stop every song coming out the same, and seven windows had then gone to making the engine follow its drawn song more closely. Jason's ruling was that other songs may be a style guide and no more; that Luthier's theory should be able to write the music without them; that the engine should decide from its theory, the writer may override, and the default is to trust the engine. He was right about what was wrong. The engine had no reason of its own for a song's shape, and it had been borrowing one.")
W("Do a song's words decide its tune's shape?", H2)
W(f"Before rebuilding, one thing had to be known: in real songs, is the tune's shape something the words and form decide, or a free choice? The rule was written first (studies/words_to_shape/PREDICTION.md). On the {WS['songs']} kept songs, twelve things known from the words and form alone were set to predict seven readings of shape, each song predicted only from other artists' songs, chance read from five hundred shuffles. Three of the seven are predicted, which the rule had named as the mark that the words decide the shape. How much a tune sings its bars again follows how much its words say their lines and phrases again: bars on a figure already sung +{rd[FIG]['held_out_rank_correlation']}, bars on a rhythm already sung +{rd[RHY]['held_out_rank_correlation']} (chance under {rd[FIG]['shuffles_95th']}). Range follows the song's length, era and word length: +{rd['range']['held_out_rank_correlation']}; part of that is arithmetic, for a longer song has more notes with which to reach its extremes. How a tune moves is not in the words: steps +{rd['moves by step']['held_out_rank_correlation']}, repeated notes +{rd['repeated notes']['held_out_rank_correlation']}, leaps {rd['moves by leap']['held_out_rank_correlation']}, none over the line. The method's check, notes a bar, was predicted at +{rd['notes a bar']['held_out_rank_correlation']}, as it should be.")
W(f"The draw had often worked against the words. Read by the kept songs' own link, song 59's lyric, which says its lines again more than the other three, asks for {OU['songs']['59']['from_its_own_words'][FIG]} of its bars on a figure already sung; the song it drew told it {OU['songs']['59']['told_by_the_song_it_drew'][FIG]}. Song 58's words ask for a range of {round(OU['songs']['58']['from_its_own_words']['range'])}; Bird Dog told it {g(OU['songs']['58']['told_by_the_song_it_drew']['range'])}.")
W("The engine's own theory of movement, tested", H2)
W(f"If movement is not in the words, the engine must decide it from its theory. The paper's theory of movement is the melodic contour checklist of Part XII: the verse uses mostly stepwise motion; the chorus carries a leap of a fourth or fifth; the highest pitch is kept for the chorus or bridge. A theory the engine is to write by should be true of the songs people kept, so it was tested, rule first, on the {SE['songs']} kept songs with a verse and a chorus (studies/shape_from_the_song/sections.py). The verse steps more than the chorus in {pc(SE['verses_step_more']['share_of_songs'])} songs in a hundred, and the chorus leaps more in {pc(SE['choruses_leap_more']['share_of_songs'])}: neither holds. The verse's and the chorus's middle shares are {SE['verses_step_more']['verse_middle']} and {SE['verses_step_more']['chorus_middle']} for steps, {SE['choruses_leap_more']['verse_middle']} and {SE['choruses_leap_more']['chorus_middle']} for leaps. Kept songs move the same way in verse and chorus. The third part holds: the chorus's highest note is at or over the verse's in {pc(SE['the_top_is_the_choruss']['share_of_songs'])} in a hundred. So items 5 and 6 of the checklist are struck as rules of movement, and what stands is older and firmer: Module 0.4's invariants, that every melody's steps and leaps fall in one band whatever its kind. That is the theory the engine now moves by.")
W("What was built (944)", H2)
W(f"No kept song is drawn. A song's range comes from its own words. Its steps, leaps, repeated notes, longest run and melismas are the kept middle, and the fit brings its builds there; the writer may ask for smooth, leaping or chant, and the default is the engine's. The chorus's lift is the kept middle. For songs 55, 54, 58 and 59 the words ask for ranges of {l3([round(REC[k]['spec']['target']['from_its_words']['range'], 1) for k in T4])} semitones; every living build's range is {l3([g(C(k, 'range')) for k in T4])}, and the picks span {l3([rng_(REC[k]) for k in T4])} ({l3([rng_(OLD[k]) for k in T4])} under the draw). The builds' steps are {l3([C(k, 'moves by step') for k in T4])} against the kept middle of {C('55', 'moves by step', 'asked')}; leaps {l3([C(k, 'moves by leap') for k in T4])} against {C('55', 'moves by leap', 'asked')}; repeated notes {l3([C(k, 'repeated notes') for k in T4])} against {C('55', 'repeated notes', 'asked')}.")
W("Judged by the rule written for it", H2)
W(f"The rule for adopting the change was written before the full runs (studies/shape_from_the_song/PREDICTION.md), with four checks. One: the picks pass the soundness rule. They do, standing outside the kept middle half on {l3(out_half)} checks of the 23. Three: movement lands where the engine put it, within a quarter of a kept width in three songs of four. It does in all four. Four: range within three semitones of what the words ask in three songs of four. It does in three. Two: the pools hold no worse than the top of Window 194's ranges. The neighbour choice does: it fails the soundness rule {p1(P9['nc'])} times in a hundred (range {rg(P9, NC)}; Window 194: {p1(P7['nc'])}, {rg(P7, NC)}). The random pick from the engine's pool does not: {p1(P9['rp'])} in a hundred (range {rg(P9, RP)}), against Window 194's {p1(P7['rp'])} ({rg(P7, RP)}) and a line drawn at 6.1. It is still inside the standard's own bar of ninety passes in a hundred. By the rule as written, the change fails one check of four.")
W(f"It is kept all the same, and the reason is set down so it can be argued with. The change was not made to improve a figure. It was made because the writer ruled that the engine may not take its shape from one other song, and no figure can overrule that; what the rule can do is say what the ruling costs, and it has. The cost has one cause. With every song at the kept middle in movement, the three practice songs fail the soundness rule together on one check, rhythm scaling, where all Luthier's songs stand low: the builds' rhythm scaling is {l3([C(k, 'rhythm scaling') for k in T4])} against kept quartiles of {l3(OW[FN['55']]['checks']['rhythm scaling']['kept_quartiles'])}. The draw had scattered the songs enough to hide that. It is not a cost of the redesign so much as a fault the redesign uncovers, and it is the next thing to mend. If Jason judges otherwise, one word in the code (SHAPE_FROM) restores the draw and Window 194's records, byte for byte.")
W("Repetition from the words: tried, and not acted on", H2)
W(f"The strongest link the study found is that a lyric which repeats is sung on bars that repeat. The engine's only dial for that is its borrows, and Window 195 found that more borrowing lowers rhythm scaling and breaks the pools. It was tried again, aimed now at what each song's own words ask. The fit chose more borrowing in three songs of four, and the builds moved toward the words' asking on bars on a figure already sung ({l3([C(k, FIG) for k in T4])} to {l3([C(k, FIG, O=OB) for k in T4])}, asked {l3([C(k, FIG, 'asked') for k in T4])}). The pools broke again: the neighbour choice {p1(PB['nc'])} in a hundred (range {rg(PB, NC)}), the random pool pick {p1(PB['rp'])} ({rg(PB, RP)}). So, as the rule said, the borrows stay at 0.8 and 0, and what the words ask is written in each record and not acted on. Until Luthier can repeat a bar the way kept songs do, keeping rhythm scaling up, the words' asking cannot be met honestly.")
for n_, title_, test_ in (
    ("944", "The shape from the song", "Test: the picks pass the soundness rule: met. The pools no worse than the top of Window 194's ranges: the neighbour choice met; the random pool pick not met (inside the standard's bar of ninety). Movement within a quarter of a kept width of the kept middle in three songs of four: met in four. Range within three semitones of the words' asking in three of four: met in three."),):
    W(f"{n_} {title_}", H2); W(test_)
W("Table HF — the four songs: what the song's words ask, and every living build's median (asked; builds). Song 59 is the hold-out.")
rows = [("", "Song 55", "Song 54", "Song 58", "Song 59 (hold-out)")]
for c, lab in (("range", "Range, from the words"), ("moves by step", "Moves by step, the kept middle"), ("moves by leap", "Moves by leap, the kept middle"), ("repeated notes", "Repeated notes, the kept middle"), (FIG, "Bars on a figure already sung, from the words (not acted on)"), (RHY, "Bars on a rhythm already sung, from the words (not acted on)")):
    rows.append((lab, *[f"{g(round(C(k, c, 'asked'), 3))}; {g(C(k, c))}" for k in T4]))
rows.append(("Rhythm scaling (kept quartiles " + l3(OW[FN['55']]['checks']['rhythm scaling']['kept_quartiles']) + ")", *[g(C(k, 'rhythm scaling')) for k in T4]))
rows.append(("Checks outside the kept middle half, of 21 read on single kept songs", *[str(CP['songs'][k]['outside_middle_half']) for k in T4]))
rows.append(("Builds that survive, of 1,000: under the draw; now", *[f"{OLD[k]['melody']['survivors']}; {REC[k]['melody']['survivors']}" for k in T4]))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W(f"The records. Songs 55, 54, 58 and 59 are written again: keys {l3([REC[k]['key']['key'] for k in T4])} ({l3([OLD[k]['key']['key'] for k in T4])} before). The kept tables are as they were, and one is added (kept_words_to_shape.json). Song 52, in 6/8, and song 53 are byte for byte as they were: they never drew a song. Read on single kept songs, songs 55, 54, 58 and 59 stand outside the kept middle half on {l3([CP['songs'][k]['outside_middle_half'] for k in T4])} checks of 21. The songs are more alike than under the draw, as was written beforehand: their lyrics are alike in size and in how much they repeat, and movement is now the same for all by the engine's theory. The paper's own finding (Module 0.4 amended) is that the repertoire keeps the typical. A lyric that differs will now be what makes a song differ, and the writer's override.")
W(f"What this window could not do. Rhythm scaling is low in every Luthier song and has been since it was first read; with the draw gone it is the one check the songs fail together, and it is the next study: what in a kept song's rhythm gives it its long memory, and why Luthier's line-by-line rhythm lacks it. Repetition from the words waits on the same thing. The study's link from words to range leans partly on a song's length. Song 54's builds span {g(C('54', 'range'))} semitones where its words ask {round(C('54', 'range', 'asked'), 1)}. The writer's override (smooth, leaping, chant) is built and has not been tried on a song. The findings of Windows 189 to 195 were made under the draw; those about the engine's mechanics stand (the page floor, the run tested where it is made, the melismas carried, the ranges on the pool figures), and those about a song following its drawn song are history. The songwriting session reviewed Windows 194 and 195 while this window was being made (its list for this window, 749.123 to 749.127, is in main and is not answered here). It agreed that withdrawing 943 was right, and it corrected Window 195's title: the amount of repetition leans low, four songs of five under the kept middle, and the clearer fault is where the repeats come from, far back and not near. That correction stands, and it points at the same next study. It also wrote a sixth song, song 60, \"Everything That Moves\"; built under this window from its own words it spans 15 semitones (its words ask 16), its longest run of one pitch is 6, and 80 of its builds survive, 805 dying at the join before a copy (the session's 749.126, not mended here). Its delivered record is left as the session and the writer left it; this window's is songs/p70/lyric60.v39.song.json. The session's scripts that read a song's drawn kept song (studies/review19/aimpool.py, studies/holdout59/aimpool59.py) no longer apply; studies/shape_from_the_song/own.py reads each song against its own asking instead.")
W("")
for lead in ("WINDOW 196", "27.120", "Table HF", "944 The shape"):
    assert any(p_.text.strip().startswith(lead) or lead in p_.text[:40] for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v39.docx"); print("saved Luthier_v39.docx")
