import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v50.docx")
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










RT = "/home/claude/rightrevjf/zeneng-pipeline/"; J = lambda p: json.load(open(RT + p)); B = "studies/borrow_kept/"
LR = J("tables/kept_line_repeat.json"); AR = J(B + "again_read.json")["six songs"]["all"]; KC_ = J(B + "kept_counts.json"); CA = J(B + "count_a.json"); CA.update(J(B + "count_b.json")); TI = J(B + "tie_a.json"); TI.update(J(B + "tie_b.json")); JO = J(B + "join_a.json"); JO.update(J(B + "join_b.json"))
PW = J(B + "pair_whole.json"); PB = J(B + "pair_whole_builds.json"); S66 = J(B + "song66.json"); CL = J(B + "clash_read.json"); BK = J(B + "bands_kept.json"); BB = J(B + "bands_builds.json"); DK = J(B + "direction_kept.json"); DB = J(B + "direction_builds.json"); NP = J("studies/soundness/neighbour_trial_borrow_count_true_chord_tie.json")
l3 = lambda v: ", ".join(str(x) for x in v); S6 = ("55", "54", "58", "49", "50", "59"); F2 = "by the count, a true repeat"; PR = "by the count, a true repeat, the chord tie"; ly = lambda s: "lyric" + s
sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v50")], "Luthier v50", "Luthier v51")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 50"))], "LUTHIER — VERSION 50", "LUTHIER — VERSION 51")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("207 Windows", "208 Windows"), ("Windows 1–207", "Windows 1–208"), ("207 scientific research windows", "208 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v222 (Luthier v51)")
cz = lambda F, k, f: l3([F[ly(s)][f][k] for s in S6])
set_cell(row.cells[1], f"NOTHING BUILT: THE ONE-PITCH VERSES TRACED TO THE BORROW, A MEND THAT PASSED SIX MARKS OF SEVEN ON A SEALED SONG AND FAILED THE SEVENTH. No note of any song changes; fixes still end at 964. Window 208 followed the verses that sit on one pitch (749.195, 749.196) down a ladder of the draw's parts to fix 818, the borrow, and read kept songs for how a line repeats. 749.206: kept verse lines repeat a nearby line {round(100 * LR['share']['Verse'], 1)} times in 100 and at the same pitch four times in five; the engine's borrow fires 8 times in 10 and holds a line at the height of the line two before. 749.208: seven borrows in ten land on a line of another length, and nine in ten of those stop being repeats; kept repeats live on lines of the same count. 749.209 and 749.210: the borrow's chance set by the lines' counts, a borrowed line kept a true repeat, and the chord tie of 749.198 on top (the pair). On the seen songs through the whole engine the pair brings verses over the pitch ceiling to {l3([PB[s]['form']['over_the_ceiling_in_100'] for s in S6])} in 100 (v50 {l3([PB[s]['v50']['over_the_ceiling_in_100'] for s in S6])}), pools to {l3([PW[s]['pair']['pool'] for s in S6])} (v50 {l3([PW[s]['v50']['pool'] for s in S6])}), on-beat chord tones to the kept share, and misses two marks: surprise, and pitch scaling. 749.217: on sealed song 66, marks written first, six marks of seven hold and pitch scaling fails ({S66['pair']['builds']['pitch_scaling']} against v50's {S66['v50']['builds']['pitch_scaling']}; kept middle 0.905). Not built; song 66 is spent. 749.215, 749.216, 749.218: the rise is at 8 to 16 notes; the joins between lines are too small under the pair, and mending them does not move it; inside a line the tune does not hold its direction more than kept songs. The line of work was closed for the version under a stopping rule written before the last reading. The switches stay, all off. Also: the two sessions now talk through the repository (coord/).")
after_par("27.131", [
    (" Window 208 (studies/line_repeats, studies/ladder, studies/borrow_kept; Tables HR, HS, HT). NOTHING BUILT. Trial switches, all off, each absent from every record: LUTHIER_BORROW_KEPT=1 (the borrow's chance the kept share of a part's lines that repeat a nearby line), =count (the chance by the part and by how far the two lines' syllable counts differ, tables/kept_line_repeat.json, lib/luthier/make_kept_line_repeat.py), =count_true (and a line borrowed by 818 is not snapped to the chord on the beat); LUTHIER_JOIN_MOVES=1 (a fresh line's first note by the kept moves across a join, tables/kept_line_join.json, lib/luthier/make_kept_line_join.py); LUTHIER_CHORD_TIE=1 and LUTHIER_LINE_HEIGHTS=1 as before; spec keys borrow_kept, join_moves, ladder_off (studies only). With all off, songs 54 and 55 are byte for byte v50's. THE PAIR is LUTHIER_BORROW_KEPT=count_true with LUTHIER_CHORD_TIE=1: it met six marks of seven on sealed song 66 and failed pitch scaling (749.217); a later version may start from it. HOLD-OUTS: song 59 for everything; songs 50 and 66 are spent and are seen songs; song 63 reserved for the loop gate (749.185); songs 64, 65 and 67 banked, not run (64 named for the next form that passes both readings; 67 to be made for the writer, not spent). METHOD: a clash, in marks from here on, is counted apart from the blue notes fix 846 allows; a test counts toward the shared bar only with power of 0.2 or more (R06-5); the songwriting session and the maintainer post in coord/ and settle method there (coord/THREAD.md).", "27.132")
])
P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 208: THE BORROW", H1)
W("This window built nothing, and it is the nearest a thing not built has come. It began with song 50's pool of five tunes and the verses that sit on one pitch, went through six wrong guesses of mine, each stated and each put to a rule written first, and ended at one old fix, the borrow (818). A mend for it, with the chord's tie loosened to the kept odds, mended the verses on every seen song and on a sealed one, and failed there on a single mark that had been written to catch exactly its cost. The mend is kept as a switch, off.")
W("How the fault was found", H2)
W("Verses over the pitch ceiling (956: more than 0.44 of a verse's notes on one pitch) were 55 to 65 builds in 100 in songs 58, 49 and 50. I guessed, in turn: the low voice; the families of chord repeats (952); the chord's pull; the tie of every on-beat note to the chord (749.198), which measured true (on-beat chord tones 0.88 to 0.95 against the kept 0.64) but whose mend alone made the easy songs worse (749.199); the register's centre; the lines' heights (749.202); the joins between lines. Each failed its rule. The ladder (749.203, 749.204) then added the draw's parts one at a time from the barest draw and took each out of the full engine alone: the spread between a verse's lines falls from 2.4 to 0.97 at the rung of the borrow and returns to 2.45 without it, a step five times any other's. The borrow sets the lines' heights.")
W("749.206 How a kept line repeats", H2)
W(f"A repeat: two lines of a part, four notes or more, read as steps of the scale and aligned from the first note, whose intervals agree in four places of five. Kept verse lines repeat the line before or two before {round(100 * LR['share']['Verse'], 1)} times in 100 (choruses {round(100 * LR['share']['Chorus'], 1)}; by the best of three alignments {round(100 * LR['described']['best_of_three_alignments']['Verse'], 1)} and {round(100 * LR['described']['best_of_three_alignments']['Chorus'], 1)}), and at the same pitch about four times in five, whether the words return or are new. So a first form, a borrowed line sung at another height, had no kept ground and was withdrawn before it was built. What the builds do instead: the borrow is set to 0.8 in every record, the line it makes is usually altered past being a repeat, and it keeps its source's height. A fresh verse line sits within a step of the line two before it in 0.51 to 0.76 of the builds' lines against the kept 0.36; with the borrow off, 0.19 to 0.38.")
W("749.207 The borrow at the kept rate", H2)
W("The chance set to the kept share. Four clean marks of six met (heights, spreads, the figure share, living builds); the ceiling in songs 50, 58 and 49 came to 46, 43 and 35 in 100 against a mark of 30, and clashes rose by a hair over the margin in two songs. Held. True verse repeats fell to 1 to 8 in 100, under the kept 11.5: at the kept rate, the engine's line sung again is not a repeat.")
W("749.208 The count differs", H2)
W(f"Of {AR['kept']} borrowed lines in the builds, {round(100 * AR['A the count differs'] / AR['kept'])} in 100 are sung onto a line whose syllables are not the source's notes, and {round(100 * AR['A the count differs, a repeat'] / AR['A the count differs'])} in 100 of those are still repeats; one syllable's difference is enough. They are 77 in 100 of the borrowed lines that end up not repeating; the snap of on-beat notes to the chord is second, 15. Kept songs agree from the other side: a nearby pair of verse lines of the same count is a repeat {round(100 * KC_['Verse']['count differs by 0']['repeat_strict'])} times in 100, an unequal pair about 5 (choruses {round(100 * KC_['Chorus']['count differs by 0']['repeat_strict'])} and 6). A craft note follows for the lyric side: a line meant to share a tune should match its partner's syllable count.")
W("749.209 and 749.210 The pair", H2)
W(f"Form 2: the borrow's chance by the part and by the difference in count (verse {l3(LR['by_count']['Verse'])} for counts 0, 1, 2, 3 or more apart), and a borrowed line left unsnapped to the chord so that it stays a repeat. Clean reading, six marks of seven; the ceiling in the three hard songs {cz(CA, 'over_the_ceiling_in_100', F2).split(', ')[2]}, {cz(CA, 'over_the_ceiling_in_100', F2).split(', ')[3]} and {cz(CA, 'over_the_ceiling_in_100', F2).split(', ')[4]} against 30. The writer ruled that mark stays at 30 and that the chord tie be tried on top. The tie alone had piled the easy songs' verses on one pitch (33, 42, 38 over the ceiling in 100); over form 2 they sit at 10, 10 and 14, and the hard songs at 28.5, 18.0 and 35.3. So much of what 749.199 called the draw sitting on one pitch was the borrow. Table HR.")
W("749.211 The rise in clashes is blue notes", H2)
W(f"Under the pair, clashes rose in songs 55 and 49 and nowhere else. They are the two songs drawn with blue notes (846), which the draw's clash rule lets stand beside a chord tone on purpose. Clashes on a blue note: {CL['55']['v50']['by_source_per_100_notes']['a blue note (846 allows it)']} to {CL['55']['the pair']['by_source_per_100_notes']['a blue note (846 allows it)']} and {CL['49']['v50']['by_source_per_100_notes']['a blue note (846 allows it)']} to {CL['49']['the pair']['by_source_per_100_notes']['a blue note (846 allows it)']} per 100 notes; clashes on any other note fall, {CL['55']['v50']['by_source_per_100_notes']['not a blue note']} to {CL['55']['the pair']['by_source_per_100_notes']['not a blue note']} and {CL['49']['v50']['by_source_per_100_notes']['not a blue note']} to {CL['49']['the pair']['by_source_per_100_notes']['not a blue note']}. v50's tight pull to the chord had all but shut blue notes out: 1 note in 100 in the builds against about 14.5 in kept blue songs of the family; the pair sings 4 to 5. The blue-note split was counted after the rule had named the fresh line, and is a description. Standing in v50 and apart from the pair (749.212): song 55's returning lines carry 1.15 clashes per 100 notes, where a line sung again meets another chord and the clash rule finds no chord tone in reach.")
W("749.213 The pair through the whole engine", H2)
W(f"Seen songs, the fits made again. Five marks of seven. The three songs of the rule are sound; a pool pick fails the rule {round(100 * [x['rule_fails_share'] for k, x in NP['a_random_pick_from'].items() if k.startswith(chr(116) + 'he engine')][0], 1)} times in 100 (v50 3.2). Pools {l3([PW[s]['pair']['pool'] for s in S6])} against {l3([PW[s]['v50']['pool'] for s in S6])}; song 50's pool 23 where it was 5. The words' fit is higher in six. Verses over the ceiling {l3([PB[s]['form']['over_the_ceiling_in_100'] for s in S6])} in 100. Missed: surprise (no chosen tune as plain as the kept middle; a mark on one tune a song, since rewritten for the builds), and pitch scaling, the builds' middle {l3([PB[s]['form']['pitch_scaling'] for s in S6])} where 0.79 to 1.02 was asked in five songs and four are inside. Table HS.")
W("749.214 to 749.216 and 749.218 Looking for the cost", H2)
W(f"The pair's tunes move from under the kept middle of pitch scaling to over it. I guessed the long scales (lines at freer heights); it is the short ones. By bands, the local slope over 8 to 16 notes is over the kept 75th ({BK['8 to 16'][2]}) in five songs of six: {l3([BB[s]['the pair']['8 to 16'] for s in S6])}. The joins between lines were named with it: under the pair a line starts {l3([BB[s]['the pair']['move across a join, mean semitones'] for s in S6])} semitones from where the last one ended, under the kept 25th of {BK['move across a join, mean semitones'][0]}; under v50 the borrowed lines had made the joins by accident. A form for the joins (a fresh line's first note by the kept moves across a join) brings them back, {cz(JO, 'across_a_join', 'the three')}, and does not move the band or the scaling: it failed two of its own three marks. The last reading, under a stopping rule written first, asked whether the pair's lines hold their direction: turns after a leap, after two steps and after three or more moves one way are all inside the kept middle half, and the longest run one way in a line is under the kept 25th under v50 and the pair alike ({l3([DB[s]['the pair']['e longest run one way'] for s in S6])} against {l3(DK['e longest run one way'])}). Nothing named. The engine's lines change direction more than kept lines, not less: a standing thing. What remains is a description, untested: lines that each stay near their own height, at heights further apart than the kept middle, would be steep at the scale of one to two lines without any line holding its direction.")
W("749.217 The sealed song", H2)
s6 = lambda k: f"{S66['v50']['builds'][k]} and {S66['pair']['builds'][k]}"
W(f"Song 66, never run by anything, the songwriting session's seven marks committed with the ledger row before the run, the pair frozen. The pool {S66['v50']['record']['pool']} and {S66['pair']['record']['pool']}; the builds' middle words' fit {S66['v50']['record']['words_fit_builds_middle']} and {S66['pair']['record']['words_fit_builds_middle']}; verses over the ceiling {s6('verses_over_the_ceiling_in_100')} in 100; true verse repeats {s6('true_verse_repeats')}; clashes other than blue notes {s6('clashes_not_blue_per_100_notes')} per 100 notes; the builds' middle surprise {s6('surprise')} (kept middle 3.18). Six hold. The seventh asked pitch scaling inside the kept 10th to 90th and no further from the kept middle, 0.905, than v50's builds by more than 0.03: {s6('pitch_scaling')}. It fails. That mark was written to forgive a cost that might be even-handed, as far over the middle as v50 was under it. On song 66 v50 sits on the middle and the pair is as far over as on every other song, so the cost is not even-handed, and the mark caught what it was there to catch. The pair is not built. Song 66 is spent. Table HT.")
W("Table HR — the pair, the clean reading: each v50 record's fitted spec, a thousand builds (v50; form 2; the pair).")
rows = [("", *[f"Song {s}" for s in S6])]
for lab, k in (("Verses over the ceiling, in 100", "over_the_ceiling_in_100"), ("Height two lines back", "height_two_back"), ("True verse repeats", "verse_lines_that_repeat"), ("Between-line spread", "between_lines"), ("Bars on a figure already sung", "bars_on_a_figure_already_sung"), ("On-beat chord tones", "on_beat_chord_tones"), ("Living builds", "living")):
    rows.append((lab, *[f"{CA[ly(s)]['v50'][k]:g}; {CA[ly(s)][F2][k]:g}; {TI[ly(s)][PR][k]:g}" for s in S6]))
table_before(anchor, [tuple(r) for r in rows])
W("")
W("Table HS — the pair through the whole engine, seen songs (v50; the pair).")
rows = [("", *[f"Song {s}" for s in S6])]
for lab, k in (("Living builds", "living"), ("The pool", "pool"), ("Builds' middle words' fit", "fit"), ("The peak planted, builds", "planted")): rows.append((lab, *[f"{PW[s]['v50'][k]:g}; {PW[s]['pair'][k]:g}" for s in S6]))
for lab, k in (("Verses over the ceiling, in 100", "over_the_ceiling_in_100"), ("Pitch scaling", "pitch_scaling"), ("Clashes not blue, per 100 notes", "clashes_not_blue_per_100_notes"), ("Blue notes in 100", "blue_notes_in_100"), ("On-beat chord tones", "on_beat_chord_tones"), ("True verse repeats", "true_verse_repeats")): rows.append((lab, *[f"{PB[s]['v50'][k]:g}; {PB[s]['form'][k]:g}" for s in S6]))
table_before(anchor, [tuple(r) for r in rows])
W("")
W("Table HT — sealed song 66: the seven marks (v50; the pair).")
rows = [("Mark", "v50", "The pair", ""), ("1. The pool", S66['v50']['record']['pool'], S66['pair']['record']['pool'], "holds"), ("2. Builds' middle words' fit", S66['v50']['record']['words_fit_builds_middle'], S66['pair']['record']['words_fit_builds_middle'], "holds")]
for lab, k, v in (("3. Verses over the ceiling, in 100", "verses_over_the_ceiling_in_100", "holds"), ("4. True verse repeats", "true_verse_repeats", "holds"), ("5. Clashes not blue, per 100 notes", "clashes_not_blue_per_100_notes", "holds"), ("6. Builds' middle surprise", "surprise", "holds"), ("7. Pitch scaling", "pitch_scaling", "fails")): rows.append((lab, S66['v50']['builds'][k], S66['pair']['builds'][k], v))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W("The records. No song record changes in this version. Songs 54 and 55 written through with every switch off are byte for byte v50's; every room file is read again and both checks pass. Song 66's two test records are in studies/borrow_kept and are not the song made for the writer, which the songwriting session makes on v50 in songs/p76.")
W("What this window could not do, and where a later one may start. The pair is one mark from a build on a sealed song. What stands between is why its tunes are steeper than kept songs' at the scale of one to two lines; the join is not the cause, nor a line holding its direction; the lines' heights, further apart than the kept middle, are the reading not yet made in a form. Standing in v50: returning lines that clash (749.212); lines that change direction more than kept lines; blue-note songs that sing a fourteenth of their blue notes; rhythm scaling low. Next by the list: 749.185, the loop gate with a chance, song 63 reserved. A note on numbering: the session's list gives 749.204 to the ladder's finding and 749.205 to the withdrawn form; my first notes of the morning used 749.204 for what is 749.206 here.")
W("")
for lead in ("WINDOW 208", "27.132", "Table HR", "Table HT", "749.217 The sealed"):
    assert any(p_.text.strip().startswith(lead) or lead in p_.text[:40] for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v51.docx"); print("saved Luthier_v51.docx")
