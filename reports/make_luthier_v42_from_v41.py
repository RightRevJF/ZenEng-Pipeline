import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v41.docx")
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










RT = "/home/claude/rightrevjf/zeneng-pipeline/"; J = lambda p: json.load(open(RT + p)); import re
OW = J("studies/shape_from_the_song/own.json"); N2 = J("studies/soundness/neighbour_v42.json"); N1 = J("studies/soundness/neighbour_v41.json"); CP = J("studies/holdout59/compare.json"); CM = J("studies/commonest_pitch/result.json")
T6 = J("studies/plant_the_peak/trial6.json"); T5 = J("studies/plant_the_peak/trial5.json"); T4_ = J("studies/plant_the_peak/trial4.json"); FM = J("tables/kept_words_to_shape.json")["repeated_notes_by_family"]
S = {k: J(p) for k, p in (("55", "songs/p65/lyric55.song.json"), ("54", "songs/p64/lyric54.song.json"), ("58", "songs/p68/lyric58.song.json"), ("59", "songs/p69/lyric59.song.json"), ("60", "songs/p70/lyric60.v42.song.json"))}
T4 = ("55", "54", "58", "59"); T5s = ("55", "54", "58", "60", "59"); FN = {k: f"lyric{k}.json" for k in T4}; l3 = lambda v: ", ".join(str(x) for x in v); p1 = lambda x: round(100 * x, 1); g = lambda x: f"{x:g}"; PK = "the engine's pool"
def pool(N): return dict(nc=N["neighbour"]["rule_fails_share"], rp=[x["rule_fails_share"] for k, x in N["a_random_pick_from"].items() if k.startswith(PK)][0], rg=N["ranges_90"])
P2, P1 = pool(N2), pool(N1); rg = lambda P_, k: f"{p1(P_['rg'][k][0])} to {p1(P_['rg'][k][1])}"; NC, RP = "neighbour choice", "a random pick from the engine's pool"
C = lambda k, c, w="builds_median": OW[FN[k]]["checks"][c][w]
def find(o, k):
    if isinstance(o, dict):
        if k in o: return o[k]
        for v in o.values():
            r = find(v, k)
            if r is not None: return r
    return None
RC = {k: find(S[k], "range_choice") for k in T5s}; rng_ = lambda R_: max(n["midi"] for n in R_["melody"]["notes"]) - min(n["midi"] for n in R_["melody"]["notes"])
WF = {k: [v for kk, v in S[k]["checks"].items() if kk.startswith("the words' fit")][0] for k in T5s}; F6 = lambda k, f, c: T6[k]["forms"][f][c]; fam = FM["families"]
D4 = lambda k, f: T4_[k]["forms"][f]["deaths"].get("838: the chorus's lift is not the plan's", 0); cm = lambda k, part: CM["songs"][k][part]["share"]; K9 = {p_: CM["kept"][p_]["p10_25_50_75_90"] for p_ in ("Verse", "Chorus")}
sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v41")], "Luthier v41", "Luthier v42")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 41"))], "LUTHIER — VERSION 41", "LUTHIER — VERSION 42")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("198 Windows", "199 Windows"), ("Windows 1–198", "Windows 1–199"), ("198 scientific research windows", "199 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v213 (Luthier v42)")
asked = l3([g(round(C(k, 'range', 'asked'), 1)) for k in T4]); builds = l3([g(C(k, 'range')) for k in T4]); picks = l3([RC[k]['the_pick_range'] for k in T5s]); firsts = l3([RC[k]['the_first_build_past_the_gates_range'] for k in T5s])
set_cell(row.cells[1], f"THE RANGE THE WORDS ASK. The range had not followed the words: they asked {asked} semitones (songs 55, 54, 58, 59) and the builds spanned 14 or 15. Four trials, each with its rule written first (studies/plant_the_peak). Three failed and said why: a planted line drawn in a raised register lifts the chorus's median, and the lift gate (838) refuses the build. 950: the peak is planted as a note. Each fresh chorus line in turn keeps its own centre, has its top set to the peak, and is redrawn until its highest stressed note is the peak; the first line to reach it carries it. The builds' middle range is now {builds}. 951: among the builds past every gate, the choice is the first whose range is within 2 semitones of the asking (studies/choose_the_range); the chosen tunes span {picks} (songs 55, 54, 58, 60, 59) where the first build past the gates spans {firsts}. The pools are sounder: the neighbour choice fails the rule {p1(P2['nc'])} times in a hundred ({p1(P1['nc'])} before), a random pick from the engine's pool {p1(P2['rp'])} ({p1(P1['rp'])} before). The session's Review 26: 952 (749.131, 749.133) the family middles of repeated notes are made by the table's maker, given with their ranges, shrunk by family size, and required; 953 (749.132) each room file names the engine that made it. 749.134 is studied and is the engine's: two chosen tunes of four sit on one pitch more than nine kept songs in ten, in verses and in choruses; a floor is proposed and not yet tried.")
after_par("27.122", [
    (f" The peak planted as a note; the choice reads the range (Window 199; Table HI; studies/plant_the_peak, studies/choose_the_range, studies/commonest_pitch). THE PEAK (950): where a song's range comes from its words, the peak is the floor of the verse and chorus plus the asked range, inside the parts' tops, on the scale. In each build, each fresh chorus line in turn is drawn with its own centre and its top set to the peak, sixty times at most, until its highest stressed note is the peak; the first line that reaches it carries the peak and the lines after are drawn as before. No part's top or centre is moved. THE CHOICE (951): among the builds past every gate the pick is the first, in the order built, whose range is within 2 semitones of the asking; where none is, the nearest; 872 decides among builds that meet the asking. The record prints the asking, the pool, how many builds meet it, and whether the pick is the first build past the gates. THE FAMILY MIDDLES (952): make_kept_words_to_shape.py writes the family middles of repeated notes with each family's bootstrap range; the engine takes a middle pulled toward the kept middle by weight n / (n + k), k = {FM['k']} (soul {fam['soul']['middle']} to {fam['soul']['shrunk']}, country {fam['country']['middle']} to {fam['country']['shrunk']}, others {fam['other']['shrunk']}), and stops with a message where a family is missing. THE ROOM FILES (953): lyric_room.py writes hashes of the engine's code and of the kept tables into each room file; lyric_room.py --check lists files no longer made by the engine at hand.", "27.123"),
])
P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 199: THE RANGE THE WORDS ASK", H1)
W(f"Window 198 ended on a fault: the words ask {asked} semitones (songs 55, 54, 58 and the hold-out 59), and the builds spanned 14 or 15. A part's top is a ceiling the draw is cut at, and the tune seldom climbs to it. This window mends it in two steps, each tried before it was built, and answers the songwriting session's Review 26.")
W("Four trials of planting the peak", H2)
W("No song is drawn any more, so nothing says where a peak should go but the engine's own theory. Of the paper's claims about sections, the one that held in kept songs (Window 196) is that the top is the chorus's, in 75 songs in a hundred. So the peak goes to a chorus line: its highest stressed note at the floor plus the range the words ask. Each trial had its rule written first: the builds within 2 semitones of the asking in at least half; the share of notes on the top note inside the kept 10th to 90th in 8 builds in 10; 7 in 10 as many builds past the gates; the words' fit down by no more than 0.02; each in three of songs 55, 54, 58 and 60, with song 59 read and deciding nothing.")
W(f"The third trial (the peak in the first fresh chorus line, the verse's and bridge's tops lowered under it) failed, mostly on builds surviving. The fourth changed one thing, leaving the tops alone, and read where the builds died. I expected the builds to survive, and was wrong. Nearly every dead build, planted or not, dies at one gate: 838, the chorus's lift is not the plan's (as built {l3([D4(k, 'as built') for k in ('55', '54', '58', '60')])} tries in a hundred; planted {l3([D4(k, 'redrawn') for k in ('55', '54', '58', '60')])}). The planted line had been drawn in a register centred three semitones under the peak, so the whole line sat high and lifted the chorus's median. The fifth trial planted the peak as a note: the line keeps its own centre and only its top is the peak. Builds and words then held in all four songs, but the first chorus line reached the peak in only {l3([round(100 * T5[k]['forms']['note']['planted_share']) for k in ('55', '54', '58', '60')])} tries in a hundred, and the range was reached in two songs. The sixth lets each fresh chorus line try in turn, and passes: the peak is planted in {l3([round(100 * F6(k, 'note', 'planted_share')) for k in ('55', '54', '58', '60')])} tries in a hundred; the builds within 2 semitones of the asking rise from {l3([F6(k, 'as built', 'span_within_2_of_the_asking') for k in ('55', '54', '58', '60')])} to {l3([F6(k, 'note', 'span_within_2_of_the_asking') for k in ('55', '54', '58', '60')])}. Against my expectation the top-note check is met too: a planted peak is sung once or twice, so the share of notes on the top falls into the kept band.")
W("The peak planted as a note (950)", H2)
W(f"Built, and read on a thousand builds a song. The builds' middle range is {builds} (songs 55, 54, 58, 59) where it was 14, 15, 15, 15. Fewer builds live ({l3([OW[FN[k]]['builds'] for k in T4])}, where 398, 337, 508, 420 did), for more die at the lift gate. Song 54's builds are no wider in the middle. A trial outside the engine passed once before (943) and failed inside it, so the standards were read before this stood: the three songs are sound, and the pools are sounder than before. The neighbour choice fails the soundness rule {p1(P2['nc'])} times in a hundred (range {rg(P2, NC)}); a random pick from the engine's pool {p1(P2['rp'])} (range {rg(P2, RP)}). Window 198: {p1(P1['nc'])} ({rg(P1, NC)}) and {p1(P1['rp'])} ({rg(P1, RP)}). I did not expect that and have not traced why.")
W("The choice reads the range (951)", H2)
W(f"Wider builds did not give wider songs. The pick is the first build past the gates in the order built (872), and that choice does not read the range: with 950 alone the chosen tunes spanned 18, 14, 12, 19 and 15 semitones (songs 55, 54, 58, 59, 60), and song 58, which the session named as the widest case, was unchanged at 12 against an asking of 19.9. So among the builds past every gate, the pick is now the first whose range is within 2 semitones of the asking; where none is, the nearest. The asking is the song's own, from its words, and not a judgement that one tune is better than another, so 872 stands for everything else. The rule was written first (studies/choose_the_range). The chosen tunes span {picks} (songs 55, 54, 58, 60, 59), every one within 2 of its asking; in songs 55, 60 and 59 the pick is the build 872 alone would choose. The soundness rule holds and the pools are the same builds. One cost: song 54's wider tune sets its words less well, a fit of {WF['54']} where the tune 872 alone chose had 0.282; it is over the kept floor (0.152) and near it.")
W("The session's Review 26", H2)
W(f"The session reviewed Windows 197 and 198, found every record to reproduce, and sent four items. 749.131: the family middles of repeated notes were in the kept table but no script wrote them, so a rebuilt table lost them and the engine fell back in silence. The table's maker now writes them and the engine stops where a family is missing (952). 749.133: soul and country rest on 18 kept songs each, and the test of Window 198 passes at 2.2 shuffles in a hundred against a bar of 1.7 once corrected for its three tests; the paper says so here. Each middle is now given with its range (soul {fam['soul']['middle']}, {fam['soul']['range_90'][0]} to {fam['soul']['range_90'][1]}; country {fam['country']['middle']}, {fam['country']['range_90'][0]} to {fam['country']['range_90'][1]}; others {fam['other']['middle']}, {fam['other']['range_90'][0]} to {fam['other']['range_90'][1]}), and the engine takes a middle pulled toward the kept middle ({FM['kept_middle']}) by the family's size: soul {fam['soul']['shrunk']}, country {fam['country']['shrunk']}, others {fam['other']['shrunk']}. Only song 60's asking moves. 749.132: a room file was read once and went stale as the engine changed; each now names the engine and tables that made it, by hashes of their contents, and all five are read again (953).")
W(f"749.134: a section can sit on one pitch for half its notes with no long run. The rule was written first (studies/commonest_pitch): if two of the four songs' chosen tunes stand over the kept 90th, it is the engine's. It is. Kept songs put {K9['Verse'][2]} of a verse's notes on its commonest pitch in the middle and {K9['Verse'][4]} at the 90th; choruses {K9['Chorus'][2]} and {K9['Chorus'][4]}. Luthier's verses: {l3([cm(k, 'Verse') for k in T5s])} (songs 55, 54, 58, 60, 59); its choruses: {l3([cm(k, 'Chorus') for k in T5s])}. Songs 54 and 58 are over in the verse, songs 55 and 58 in the chorus. A floor would remove builds from the pool, so it is to be tried against the pool standard before it is built; it is not built here.")
for n_, title_, test_ in (
    ("950", "The peak planted as a note", "Test (written first): in three of songs 55, 54, 58, 60 the builds span within 2 semitones of the asking in half the builds, the top-note share is inside the kept band in 8 builds in 10, 7 in 10 as many builds live, and the words' fit falls by no more than 0.02: met in 3, 3, 4 and 3 songs. In the engine: the soundness rule and the pool standard hold."),
    ("951", "The choice reads the range", "Test (written first): the chosen tune within 2 semitones of the asking in three songs of four; the three-song soundness rule holds; no pick's words' fit under the kept floor; the pools unchanged. All met."),
    ("952", "The family middles made, shrunk and required", "Test: every maker rebuilds its table byte for byte; with the block deleted the engine refuses; song 60's asking stands no further from the kept middle than its family's range allows."),
    ("953", "The room files name their engine", "Test: lyric_room.py --check finds every room file made by the engine at hand; a rerun gives the same file byte for byte.")):
    W(f"{n_} {title_}", H2); W(test_)
W("Table HI — the range the words ask, the builds, and the tune chosen. Song 59 is the hold-out.")
rows = [("", "Song 55", "Song 54", "Song 58", "Song 60", "Song 59 (hold-out)")]
rows.append(("Range the words ask, semitones", *[g(RC[k]['asked']) for k in T5s]))
rows.append(("Builds' middle range, Window 198", "14", "15", "15", "17", "15"))
rows.append(("Builds within 2 of the asking, as built; planted (sixth trial)", *[f"{F6(k, 'as built', 'span_within_2_of_the_asking')}; {F6(k, 'note', 'span_within_2_of_the_asking')}" for k in T5s]))
rows.append(("Builds past every gate; of them within 2 of the asking", *[f"{RC[k]['builds_in_the_pool']}; {RC[k]['within_2_of_the_asking']}" for k in T5s]))
rows.append(("The first build past the gates (872 alone)", *[str(RC[k]['the_first_build_past_the_gates_range']) for k in T5s]))
rows.append(("The chosen tune", *[str(RC[k]['the_pick_range']) for k in T5s]))
rows.append(("The chosen tune's words' fit (kept floor 0.152, middle 0.318)", *[str(WF[k]) for k in T5s]))
rows.append(("Commonest pitch's share, verse (kept 90th 0.44)", *[str(cm(k, 'Verse')) for k in T5s]))
rows.append(("Commonest pitch's share, chorus (kept 90th 0.474)", *[str(cm(k, 'Chorus')) for k in T5s]))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W(f"The records. Songs 55, 54, 58 and 59 are written again. Song 60 is read under this window as songs/p70/lyric60.v42.song.json (range {rng_(S['60'])}); its delivered record is untouched. Song 52, in 6/8, and song 53, the hymn, are byte for byte as they were: neither takes a range from its words. One kept table changes (kept_words_to_shape.json, the family block). Rhythm scaling is where it was (the builds' middle {l3([g(C(k, 'rhythm scaling')) for k in T4])}), and is the one check on which the three songs lean past the kept quartiles.")
W("What this window could not do. Song 54's builds are no wider in the middle (15 against an asking of 18.8); its chosen tune is wide only because the choice now looks for one, and it pays in the words' fit. Fewer builds live in every song. Why the pools grew sounder is not traced. The commonest-pitch fault is measured and not mended. Rhythm scaling's engine side (sections that differ in how busy they are, bars of rest) is untried. The top-note share of the songs as built stands outside the kept band more often than a kept song's would, and planting mends it only in part.")
W("")
for lead in ("WINDOW 199", "27.123", "Table HI", "953 The room"):
    assert any(p_.text.strip().startswith(lead) or lead in p_.text[:40] for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v42.docx"); print("saved Luthier_v42.docx")
