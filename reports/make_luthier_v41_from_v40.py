import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v40.docx")
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
WS = J("studies/words_to_shape/result.json"); W0 = J("studies/words_to_shape/result_v39.json"); MF = J("studies/movement_by_family/result.json"); OW = J("studies/shape_from_the_song/own.json"); O9 = J("studies/shape_from_the_song/own_v39.json")
N1 = J("studies/soundness/neighbour_v41.json"); N9 = J("studies/soundness/neighbour_v39.json"); CP = J("studies/holdout59/compare.json"); snd = open("/tmp/claude-0/t32/sound.txt").read(); S60 = J("songs/p70/lyric60.v41.song.json"); S69 = J("songs/p70/lyric60.v39.song.json")
T4 = ("55", "54", "58", "59"); FN = {k: f"lyric{k}.json" for k in T4}; l3 = lambda v: ", ".join(str(x) for x in v); p1 = lambda x: round(100 * x, 1); g = lambda x: f"{x:g}"; PK = "the engine's pool"; FIG, RHY = "bars on a figure already sung", "bars on a rhythm already sung"
def pool(N): return dict(nc=N["neighbour"]["rule_fails_share"], rp=[x["rule_fails_share"] for k, x in N["a_random_pick_from"].items() if k.startswith(PK)][0], rg=N["ranges_90"])
P1, P9 = pool(N1), pool(N9); rg = lambda P_, k: f"{p1(P_['rg'][k][0])} to {p1(P_['rg'][k][1])}"; NC, RP = "neighbour choice", "a random pick from the engine's pool"
C = lambda k, c, w="builds_median", O=OW: O[FN[k]]["checks"][c][w]; rd, r0 = WS["readings"], W0["readings"]; out_half = [int(x) for x in re.findall(r"outside the middle half (\d+)", snd)]; R = MF["readings"]["repeated notes"]
JD = "join before a copy (780)"; rng_ = lambda R_: max(n["midi"] for n in R_["melody"]["notes"]) - min(n["midi"] for n in R_["melody"]["notes"])
sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v40")], "Luthier v40", "Luthier v41")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 40"))], "LUTHIER — VERSION 40", "LUTHIER — VERSION 41")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("197 Windows", "198 Windows"), ("Windows 1–197", "Windows 1–198"), ("197 scientific research windows", "198 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v212 (Luthier v41)")
set_cell(row.cells[1], f"THE WORDS MEASURED ONE WAY. The songwriting session's review of Window 196 (749.128 to 749.130, and 749.124, 749.126 carried). 946 (749.128): the session found a fault in my measure. The words-to-shape table had split a kept song's words into lines by the lines' notes while reading Luthier's real lines, so it asked Luthier's songs for too much repetition and too little range. Each kept word is now tied to its notes, the study is run again, and the links hold and are stronger (bars on a figure already sung +{rd[FIG]['held_out_rank_correlation']}, on a rhythm already sung +{rd[RHY]['held_out_rank_correlation']}, range +{rd['range']['held_out_rank_correlation']}). Measured rightly, Luthier's builds already sing their bars again about as often as their words ask; what Window 196 recorded as not yet acted on needs no acting on. 947 (749.129): of steps, leaps and repeated notes, only repeated notes differ by genre family in kept songs; that one is now the family's middle. 948 (749.126): a line its own copy follows leaves the copy room; song 60's deaths at that join fall from {S69['melody']['deaths'].get(JD, 0)} to {S60['melody']['deaths'].get(JD, 0)} in a thousand. 949 (749.124): the neighbour range read on a thousand inner draws. 749.130 was answered in Window 197. The picks are sound, with no lean. One thing is now plainly unmet: the words ask ranges of 18 to 20 semitones and the builds span 14 or 15.")
after_par("27.121", [
    (f" The words read one way; repeated notes by family; room for a copy (Window 198; Table HH; studies/words_to_shape, studies/movement_by_family). THE WORDS READ ONE WAY (946): in the kept table of 27.120 each kept word is tied to its notes by its syllables, and a line's words are the words that begin in it (words_to_shape.kept_lines), as a Luthier lyric's lines are read. REPEATED NOTES BY FAMILY (947): the default share of repeated notes is the kept middle of the song's genre family (soul and R&B {R['family_middles']['soul']}, country {R['family_middles']['country']}, others {R['family_middles']['other']}); steps and leaps stay at the kept middle for every song, for they do not differ by family. ROOM FOR A COPY (948): where the very next line copies this line, this line's last syllable may stand no further from its first than leaves the copy room to begin one slot on; a line sung again or borrowed that would not is drawn fresh, and a fresh rhythm that would not is drawn again, twelve times at most. THE RANGES (949): every pool figure's range is read on a thousand inner draws a resample.", "27.122"),
])
P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 198: THE WORDS MEASURED ONE WAY", H1)
W("The review", H2)
W("The songwriting session reviewed Window 196 and kept 944: it is the writer's ruling, its cost is stated, and the pools stay inside the standard's bar. It found one fault in the measure under it, and sent three items (749.128 to 749.130) with 749.123 to 749.127 carried. Its 749.130, on rhythm scaling, was written before it had seen Window 197, which answers it: the contrast between songs 59 and 60 and songs 55, 54 and 58 is that the first two change their pace and rest, and the same two readings carry rhythm scaling in kept songs.")
W("The words measured one way (946; 749.128)", H2)
W(f"The corpus does not tie a kept song's words to its lines, and to make the table of Window 196 I had split each song's words among its lines in proportion to the lines' notes. A Luthier lyric's lines are read as they are written. So one predictor, lines said again word for word, was nearly missed in kept songs and read at full strength in Luthier's lyrics, and the table asked Luthier's songs for more repetition and less range than their words warrant. The session measured it: the asks were off by 0.06 to 0.10 on bars sung again and by one to two semitones on range. Each kept word is now tied to its notes by its syllables, and a line's words are the words that begin in it. The study of Window 196 was run again under its own rule. The links hold and the two that matter are stronger: bars on a figure already sung +{rd[FIG]['held_out_rank_correlation']} (+{r0[FIG]['held_out_rank_correlation']} before), bars on a rhythm already sung +{rd[RHY]['held_out_rank_correlation']} (+{r0[RHY]['held_out_rank_correlation']}), range +{rd['range']['held_out_rank_correlation']} (+{r0['range']['held_out_rank_correlation']}). Kept songs say their lines again in 0.08, 0.32 and 0.52 of their lines at the 10th, middle and 90th; Luthier's five lyrics in 0.23, 0.14, 0.19, 0.33 and 0.28. They read alike now, and Luthier's lyrics say their lines again a little less than kept songs do.")
W(f"What the words ask has moved. Range, songs 55, 54, 58, 59: {l3([g(round(C(k, 'range', 'asked', O9), 1)) for k in T4])} before, {l3([g(round(C(k, 'range', 'asked'), 1)) for k in T4])} now. Bars on a figure already sung: {l3([g(round(C(k, FIG, 'asked', O9), 2)) for k in T4])} before, {l3([g(round(C(k, FIG, 'asked'), 2)) for k in T4])} now; the builds sing {l3([C(k, FIG) for k in T4])}. Bars on a rhythm already sung: {l3([g(round(C(k, RHY, 'asked'), 2)) for k in T4])} asked; the builds sing {l3([C(k, RHY) for k in T4])}. Measured rightly, the builds already sing their bars again about as often as their words ask. Window 196 recorded repetition from the words as a thing asked and not yet acted on, and tried to act on it and broke the pools. It needs no acting on. The fault was in my measure, and the session found it.")
W("Repeated notes by genre family (947; 749.129)", H2)
W(f"The session asked whether the default movement should come from the kept songs of the song's own genre family, if the families differ. The rule was written first (studies/movement_by_family/PREDICTION.md). In the three families the engine already uses for its scale degrees, steps do not differ (a spread of {MF['readings']['moves by step']['spread']} between the family middles, as large in {round(100 * MF['readings']['moves by step']['share_of_shuffles_as_large'])} shuffles in a hundred) and leaps do not ({MF['readings']['moves by leap']['spread']}, {round(100 * MF['readings']['moves by leap']['share_of_shuffles_as_large'])} in a hundred). Repeated notes do: soul and R&B tunes repeat a note {R['family_middles']['soul']} of the time, country {R['family_middles']['country']}, the rest {R['family_middles']['other']}, a spread as large in {round(100 * R['share_of_shuffles_as_large'])} shuffles in a hundred. By the rule that one reading is taken from the family. Song 60, soul and R&B, is the only one of the six it moves; the two small families have eighteen kept songs each, which is a caution.")
W("Room for a copy (948; 749.126)", H2)
W(f"{S69['melody']['deaths'].get(JD, 0)} of song 60's thousand builds died at a join before a copy. The trace found one join: the bridge's sixth line copies its fifth, five syllables in a one-bar slot, and the fifth line, drawn or borrowed, ran too late in its bar for its own copy to begin a bar on. The engine tells a line to give way to a copied line that follows (816), but could not when the line to be copied was the line itself, not yet written. Now such a line is held to a span that leaves its copy room. Song 60's deaths at the join are {S60['melody']['deaths'].get(JD, 0)}; {S60['melody']['survivors']} builds survive ({S69['melody']['survivors']} before); its fit of the moves, which had too few builds to read, now runs. No other song has such a line, and none changes by this.")
W("The ranges read on more draws (949; 749.124)", H2)
W(f"The neighbour choice's range had been read on two hundred inner draws a resample, and at failure rates this low that is mostly the inner draws' own noise. All three figures are now read on a thousand. This window: the neighbour choice fails the soundness rule {p1(P1['nc'])} times in a hundred (range {rg(P1, NC)}); a random pick from the engine's pool {p1(P1['rp'])} (range {rg(P1, RP)}). Window 196, on the old ranges: {p1(P9['nc'])} ({rg(P9, NC)}) and {p1(P9['rp'])} ({rg(P9, RP)}). Nothing has moved; the pools stand where the redesign left them, inside the standard's bar.")
for n_, title_, test_ in (
    ("946", "The words read one way", "Test: lines said again read alike in kept songs and in Luthier's lyrics; the held-out prediction for range and the two repetition readings stays over the shuffled-chance line: all three do, and two rise."),
    ("947", "Repeated notes by genre family", "Test: by the rule written first, a reading is taken from the family only if the families differ beyond chance and by a quarter width: repeated notes do; steps and leaps do not."),
    ("948", "Room for a copy", "Test: song 60's survivors rise by at least half with no other song's record changed by it: 84 to " + str(S60['melody']['survivors']) + "."),
    ("949", "The ranges on a thousand inner draws", "Test: the neighbour range is recomputed and is the pools', not the inner draws'.")):
    W(f"{n_} {title_}", H2); W(test_)
W("Table HH — what each song's words ask, and every living build's median (asked; builds). Song 59 is the hold-out.")
rows = [("", "Song 55", "Song 54", "Song 58", "Song 59 (hold-out)")]
for c, lab in (("range", "Range"), (FIG, "Bars on a figure already sung"), (RHY, "Bars on a rhythm already sung"), ("repeated notes", "Repeated notes (the family's middle)"), ("moves by step", "Moves by step (the kept middle)"), ("moves by leap", "Moves by leap (the kept middle)")):
    rows.append((lab, *[f"{g(round(C(k, c, 'asked'), 3))}; {g(C(k, c))}" for k in T4]))
rows.append(("Rhythm scaling (kept quartiles 0.61, 0.66, 0.72)", *[g(C(k, 'rhythm scaling')) for k in T4]))
rows.append(("Checks outside the kept middle half, of 21 read on single kept songs", *[str(CP['songs'][k]['outside_middle_half']) for k in T4]))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W(f"The records. Songs 55, 54, 58 and 59 are written again, for what their words ask has changed. Their picks stand outside the kept middle half on {l3(out_half)} checks of the 23 (songs 55, 54, 58) and pass the soundness rule, with no check on which all three lean the same way. Song 60 is added to the songs that are fitted to and read, under this window as songs/p70/lyric60.v41.song.json: key {S60['key']['key']}, range {rng_(S60)}; the delivered record is as the session and the writer left it. Song 59 stays the one hold-out. Songs 52 and 53 are byte for byte as they were. One kept table changes (kept_words_to_shape.json, refitted, with the families' repeated notes added).")
W(f"What this window could not do. The range does not follow the words. They ask {l3([g(round(C(k, 'range', 'asked'), 1)) for k in T4])} semitones and the builds span {l3([g(C(k, 'range')) for k in T4])}: every song is four or five short, and the check of Window 196 that range fall within three semitones of the asking is now met in none of the four. The cause is the one the session named in 749.111 and Window 192 measured: a part's top is a ceiling the draw is cut at, and the tune seldom climbs to it. Window 192's second trial showed that planting the peak helps a wide aim, and every song's asking is now wide; that trial is the next thing to run, with its rule written first. Rhythm scaling is still low in songs 55, 54 and 58 ({l3([g(C(k, 'rhythm scaling')) for k in T4[:3]])}); Window 197 showed why, and the engine's side of it, sections that differ in how busy they are, is not yet tried. 749.127, a line in each rule saying what was seen first, is kept from Window 197 on. 749.111, 749.116, 749.103, 749.101, 749.61: carried.")
W("")
for lead in ("WINDOW 198", "27.122", "Table HH", "949 The ranges"):
    assert any(p_.text.strip().startswith(lead) or lead in p_.text[:40] for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v41.docx"); print("saved Luthier_v41.docx")
