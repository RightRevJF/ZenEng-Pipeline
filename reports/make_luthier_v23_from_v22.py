"""Luthier v22 -> v23: long notes for the words that carry weight, the rest after a line, melismas at line ends, a song's length, and the harmony voice
fitted to its song (Window 180, Module 27.104, Tables GK and GL; fixes 885-889). Evidence: lib/luthier/stage10_results.json, tables/kept_word_weight.json.
Run: python3 make_luthier_v23_from_v22.py"""
import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v22.docx")
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










R = json.load(open("/home/claude/rightrevjf/zeneng-pipeline/lib/luthier/stage10_results.json")); SG = R["songs"]; K = R["kept"]; B = R["builds"]; EB = R["engine_before"]
pc = lambda x: f"{100 * x:.0f}"; O = ("55", "54", "58", "52"); PATH = {"55": "songs/p65/lyric55", "54": "songs/p64/lyric54", "58": "songs/p68/lyric58", "52": "songs/p62/lyric52"}
def ba(k, key, f=lambda x: x): return f"{f(SG[PATH[k]]['before'].get(key, ''))}; {f(SG[PATH[k]]['after'].get(key, ''))}" if key in SG[PATH[k]]["after"] else ""

sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v22")], "Luthier v22", "Luthier v23")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 22"))], "LUTHIER — VERSION 22", "LUTHIER — VERSION 23")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("179 Windows", "180 Windows"), ("Windows 1–179", "Windows 1–180"), ("179 scientific research windows", "180 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v194 (Luthier v23)")
set_cell(row.cells[1], "REPAIRS AFTER WAY 3. Five faults left open by the last three versions are mended, each against a kept figure. Inside a line a stressed syllable is now given more time than a function word, as kept songs give it (885). A line's last note takes a kept length for its syllable's weight and is no longer held as long as the rest allows; the rest after a line rose from a quarter to the kept half note on two songs of three (887). Melismas no longer crowd the line ends (886). A song that runs past the kept lengths takes no turns and the shorter kept edges; song 55 now stands inside the kept lengths, and songs 54 and 58 are shorter and still long, because their lyrics are (888). The harmony voice's weights are fitted to each song, and its fourths fell from as many as 35 in a hundred to the kept 12 (889). Two studies were run beside this version and built nothing into it: the writer's way 4 failed on a graded set of 2,500 songs, and way 2's pitch scaling kept its relation to the chart record on songs it had not seen (0.14 on 313) and failed the critics' test.")

after_par("27.103 The marriage of tune and words", [
    (" Repairs after way 3 (Window 180; Tables GK, GL). TIME BY WEIGHT (885): the score of a line's rhythm (879) gains a term for the time each syllable has before the next, by the kept shares of each length for the syllable's weight over the shares for any; its power, 2, is fitted to the kept fit by length. MELISMAS AT LINE ENDS (886; amends 848): the share of a song's melismas at line ends is the kept odds for a phrase's last syllable (2.9 to 1) applied to the song's own count of line ends; inside a line a note an eighth long may take one, a quarter-long note four times as readily. THE LAST NOTE OF A LINE (887; amends 832, 844): its length is drawn from the kept lengths of last notes for its syllable's weight, among those that leave the quarter's rest; 871's cap on a weak last syllable stands. A SONG'S LENGTH (888; amends 825, 877): a turn is added only while the song stays inside the kept 75th of lengths, as the break is; a song past it takes the kept lower quartiles of bars in and out. THE HARMONY VOICE FITTED (889; amends 829): the voice is written, its shares of each interval class read against the kept shares, each weight moved by kept over written, and written again, ten rounds at most, the nearest round kept.", "27.104"),
])

P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 180: REPAIRS AFTER WAY 3", H1)
W("Where the last three versions left off", H2)
W("Versions 20 to 22 each closed with a list of what was not met. This window takes five of them: long notes that did not follow the words, rests between lines at their floor, melismas crowded at line ends, songs over the kept lengths, and a harmony voice with too many fourths. Each is mended against a figure read from kept songs, and each repair is tried on the builds before the songs are written again. The pick is not touched: it is still the first build past the gates, and by the writer's instruction no reading is to choose until one is known to work.")
W("Time by weight, and the last note of a line (885, 887)", H2)
W(f"Window 179 found that in the engine's picks the weightier syllables did not get the longer notes. Looked at closely, the fault was two faults. Inside a line, kept songs give a stressed syllable more time than a function word or a weak syllable: set against each song's own spread of note lengths, kept stressed syllables stand at {K['inside_lines_z_length_by_tier'][2]} and function words at {K['inside_lines_z_length_by_tier'][0]}; in the engine's picks the three weights stood alike, near -0.25. And at a line's end the engine held the last note as long as the rest allowed, so that a line ending on a function word ('on me', 'of it') got the song's longest notes, a half note or more, where a kept line's last note is a quarter at the median whatever word it carries.")
W(f"Two rules follow. The score that places a line's syllables (879) now also reads the time each syllable has before the next, by the kept shares for its weight; the kept differences are small (a stressed syllable gets a quarter {pc(K['length_share_by_tier'][2][3])} times in a hundred, a weak one {pc(K['length_share_by_tier'][1][3])}), so the term's power was fitted until the builds' fit by length met the kept {K['fit_by_length'][0]}. And a line's last note now takes a length drawn from the kept last notes for its syllable's weight (a stressed last syllable is held a half note or more {pc(sum(K['last_note_share_by_tier'][2][5:]))} times in a hundred, a function word {pc(sum(K['last_note_share_by_tier'][0][5:]))}), among the lengths that leave a quarter's rest. The second rule alone moved the rest after a line from {B['before']['55']['rest']}, {B['before']['54']['rest']} and {B['before']['58']['rest']} twelfths of a quarter to {B['last_note_only']['55']['rest']}, {B['last_note_only']['54']['rest']} and {B['last_note_only']['58']['rest']} at the builds' median, against the kept {K['rest_after_line'][1]}: the short rests of 749.58 were the long last notes all along, and no onset had to move.")
W("Melismas, length, and the harmony voice (886, 888, 889)", H2)
W("Fix 848 asked that a melisma sit on a note a quarter long or more. Inside a line few notes are, so line ends took most of them: 64, 38 and 65 in a hundred against a kept 20. The kept 20 is itself for songs in which 8 syllables in a hundred end a phrase; here one syllable in seven ends a line, and the same odds give about 32. The share at line ends is now drawn to that figure for each song, and an eighth-long note inside a line may take a melisma.")
W(f"The break has been added only while a song stays inside the kept 75th of lengths (842); the turns of 877 were added whatever the length. They now follow the break's rule, and a song already past the kept 75th takes the kept lower quartiles of bars in and out. Song 55 goes from {SG[PATH['55']]['before']['seconds']} seconds to {SG[PATH['55']]['after']['seconds']}, inside the kept lengths. Songs 54 and 58 go from {SG[PATH['54']]['before']['seconds']} and {SG[PATH['58']]['before']['seconds']} to {SG[PATH['54']]['after']['seconds']} and {SG[PATH['58']]['after']['seconds']}: their lyrics are long for their tempos and the engine does not cut words. There is a cost, and it was foreseen in Window 178: the turns were the long silences that carried the rhythm's order across scales, and without them the rhythm exponent of the picks of songs 55 and 54 fell from {SG[PATH['55']]['before']['rhythm_scaling']} and {SG[PATH['54']]['before']['rhythm_scaling']} to {SG[PATH['55']]['after']['rhythm_scaling']} and {SG[PATH['54']]['after']['rhythm_scaling']}. The study run beside this version found no sign that a higher rhythm exponent goes with a song faring better, so length was preferred.")
W(f"The harmony voice's six weights were fitted once, to all songs together. A song's chords decide which intervals are to be had under its tune, and on song 55 the one set of weights gave {pc(SG[PATH['55']]['before']['fourths'])} fourths in a hundred against the kept 12. The weights are now fitted to the song: written, read, corrected by kept over written, and written again. The summed miss over the six classes fell from {SG[PATH['55']]['before']['harmony_miss']}, {SG[PATH['54']]['before']['harmony_miss']}, {SG[PATH['58']]['before']['harmony_miss']} and {SG[PATH['52']]['before']['harmony_miss']} to {SG[PATH['55']]['after']['harmony_miss']}, {SG[PATH['54']]['after']['harmony_miss']}, {SG[PATH['58']]['after']['harmony_miss']} and {SG[PATH['52']]['after']['harmony_miss']}.")
W("Two studies beside this version", H2)
W("Two studies were run between versions 22 and 23 and neither built anything into the engine; they are recorded here because they bear on the pick. A graded set was built: 1,795 Hooktheory songs joined to the Hot 100 record, 210 CoCoPops Billboard whole songs, 194 Rolling Stone whole songs and 318 BiMMuDa songs, where the record until then was 131 songs (studies/way4/graded.py). On it the writer's way 4 was tried, with two of another model's proposals folded in: a stranger who knows other songs and a learner who has also heard this one so far, and the share of the stranger's surprise that the song teaches away. No measure met the rule set beforehand; the share stood at -0.03 and -0.01 against peak and weeks on 1,795 songs (studies/way4/RESULTS.md). Then way 2 was run again on whole songs the first run had not seen. The writer had predicted that pitch scaling's relation to the chart record would shrink to nothing. It did not: 0.16 against weeks and 0.18 against peak on 147 new songs, 0.14 on all 313 holding year, length and source. It failed the other half of the rule: the songs critics chose do not scale higher than the others (studies/way2_again/RESULTS.md). It is the first reading in this work to keep its size on songs it had not seen, it is small, and it waits on a third set before it is let to choose.")
for n_, title_, test_ in (
    ("885", "Time by a word's weight", "Test: the builds' fit by length at the kept median (0.13) within five hundredths on every 4/4 song."),
    ("886", "Melismas at line ends at the kept odds", "Test: the share of a song's melismas at line ends within ten points of the kept odds applied to its line ends."),
    ("887", "A line's last note takes a kept length", "Test: the median last note a quarter; the median rest after a line inside the kept quartiles (15, 24, 48 twelfths)."),
    ("888", "Turns and edges inside the kept lengths", "Test: no song is taken past the kept 75th of lengths by a turn; the record flags what the lyric alone makes long."),
    ("889", "The harmony voice fitted to its song", "Test: the summed miss of the six interval classes against the kept shares under 0.15; fourths within five points of the kept 12.")):
    W(f"{n_} {title_}", H2); W(test_)
W("Table GK — time and rest by a word's weight: kept songs, and the engine's builds before and after (medians of 40 builds a song; songs 55, 54, 58).")
rows = [("", "Kept songs", "Before", "With 887 alone", "With 885 and 887")]
f3 = lambda key, when: ", ".join(str(B[when][k][key]) for k in ("55", "54", "58"))
rows.append(("The fit by length", K["fit_by_length"][0], f3("length", "before"), f3("length", "last_note_only"), f3("length", "after")))
rows.append(("The rest after a line, twelfths of a quarter", "15, 24, 48 (quartiles)", f3("rest", "before"), f3("rest", "last_note_only"), f3("rest", "after")))
rows.append(("A line's last note, twelfths", K["last_note_median"], f3("last_note", "before"), f3("last_note", "last_note_only"), f3("last_note", "after")))
rows.append(("Rest share inside sung sections", "0.21, 0.30, 0.39 (quartiles)", f3("rest_share", "before"), f3("rest_share", "last_note_only"), f3("rest_share", "after")))
rows.append(("The builds' median place under the old 4/4 judge (withheld)", "", ", ".join(str(B["j6_before"][k]) for k in ("55", "54", "58")), "", f3("j6", "after")))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W("Table GL — the four songs written again from their lyrics, before; after this window.")
rows = [("", "Song 55", "Song 54", "Song 58", "Song 52, 6/8")]
rows.append(("Length in seconds (kept 165, 206, 243)", *[ba(k, "seconds") for k in O]))
rows.append(("Rest after a line, median in twelfths (kept 15, 24, 48)", *[ba(k, "rest_median", lambda x: f"{x:.0f}") for k in O]))
rows.append(("A line's last note, median in twelfths (kept 12)", *[ba(k, "last_note_median", lambda x: f"{x:.0f}") for k in O]))
rows.append(("Rest share inside sung sections (kept 0.21, 0.30, 0.39)", *[ba(k, "rest_share") for k in O]))
rows.append(("Melismas at a line's end, in a hundred (kept odds give about 32)", *[ba(k, "melisma_ends", lambda x: x[0]) for k in O]))
rows.append(("The pick's fit of words to notes (kept 0.20, 0.29, 0.38)", *[ba(k, "fit") for k in O]))
rows.append(("The pick's fit by length (kept 0.13)", *[ba(k, "by_length") for k in O]))
rows.append(("Harmony voice: fourths, share (kept 0.12)", *[ba(k, "fourths") for k in O]))
rows.append(("Harmony voice: summed miss over six classes", *[ba(k, "harmony_miss") for k in O]))
rows.append(("Rhythm exponent of the pick (kept 0.61, 0.66, 0.72)", *[ba(k, "rhythm_scaling") if k != "52" else "" for k in O]))
rows.append(("Pitch exponent of the pick (kept 0.79, 0.90, 1.00)", *[ba(k, "pitch_scaling") if k != "52" else "" for k in O]))
rows.append(("Builds that survive, of 1,000", *[ba(k, "survivors") for k in O]))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W("What this window could not do. The picks' fit by length rose on song 55 and not on songs 54 and 58, though their builds' medians rose: the pick is one draw, and nothing chooses the build whose long notes sit best. Songs 54 and 58 are still a minute and more over the kept lengths; only a shorter lyric or a faster tempo will mend that, and the engine can say so and no more. Taking the turns out lowered the rhythm exponent on two songs, a reading this engine itself raised two versions ago. Song 52 and the hymns have no kept table of words' weights and no kept last notes outside 4/4; their melodies are as they were, and song 52's rests still sit at the floor. The harmony voice is fitted to interval classes and not to how the two voices move. And the pick is still the first build past the gates: pitch scaling is the one reading with a claim to choose, and it waits on a third set of songs.")
W("")
for lead in ("WINDOW 180", "27.104 Repairs after way 3", "Table GK", "Table GL", "889 The harmony voice"):
    assert any(p_.text.strip().startswith(lead) for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v23.docx"); print("saved Luthier_v23.docx")
