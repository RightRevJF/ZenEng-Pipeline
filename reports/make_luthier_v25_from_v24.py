"""Luthier v24 -> v25: the session's fix list for v25 (findings 749.76 to 749.81, and the kept evidence on 749.75) answered
(Window 182, Module 27.106, Tables GO and GP; fixes 899-903). Evidence: lib/luthier/stage12_results.json, tables/kept_line_ends.json,
songs/p68/fixlist_v25.md, REVIEW_stage10_11.md, studies/last_chorus/. Run: python3 make_luthier_v25_from_v24.py"""
import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v24.docx")
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










R = json.load(open("/home/claude/rightrevjf/zeneng-pipeline/lib/luthier/stage12_results.json")); SG = R["songs"]; KL = R["kept_line_ends"]; KW = R["kept_weak_endings"]; B = R["builds"]; LCK = R["last_chorus_kept"]
pc = lambda x: f"{100 * x:.0f}"; O = ("55", "54", "58", "52"); T3 = ("55", "54", "58")
def ba(k, key, f=lambda x: x):
    a, b = SG[k]["before"].get(key), SG[k]["after"].get(key); return f"{f(a) if a is not None else ''}; {f(b) if b is not None else ''}" if (a is not None or b is not None) else ""
l3 = lambda v: ", ".join("none" if x is None else str(x) for x in v)

sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v24")], "Luthier v24", "Luthier v25")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 24"))], "LUTHIER — VERSION 24", "LUTHIER — VERSION 25")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("181 Windows", "182 Windows"), ("Windows 1–181", "Windows 1–182"), ("181 scientific research windows", "182 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v196 (Luthier v25)")
set_cell(row.cells[1], f"HOW A LINE ENDS. The session reviewed versions 23 and 24, merged them, rebuilt song 58, and showed that fix 887 had bought the rest after a line by cutting the line's last word short, and that the voice now stopped after nearly every line. Both come from one cause and are mended by one table. How a kept line ends was read from {KL['line_ends']} lyric lines: the time from the last syllable to the next line, and how long the syllable is held, by the syllable's weight. The two are now drawn as a pair. Kept lines run into the next with under a beat of rest {pc(KL['lines_run_on_with_under_a_beat_of_rest_share'])} times in a hundred; the engine's ran on never, and now run on {pc(B['after']['run_on'][2])} to {pc(B['after']['run_on'][0])}. Silences of a beat or more fell from 12 to 14 in a hundred beats to 9 to 10, inside the kept middle half, and the last word of a line is held a half note as often as kept singers hold it. The same table overturned an earlier fix: 871 and 890 forbade a line-final word's weak syllable to outlast its stressed one, and kept singers do exactly that at {pc(KW['weak_held_longer_share'])} such endings in a hundred. The rule is retired. The guitar now plays two notes of the chord where three would clash, and sounds under every sung note. The last chorus is read as kept songs lift it, by length, and all three songs pass.")

after_par("27.105 The session's fix list for v23", [
    (" How a line ends; the session's fix list for v25 (Window 182; Tables GO, GP; tables/kept_line_ends.json; songs/p68/fixlist_v25.md). THE LAST SYLLABLE AND ITS REST AS A PAIR (899; answers 749.76, 749.80; replaces 887, amends 844, 870): a line's last syllable takes a length drawn from the kept lengths for its weight and for the time to the next line's first note; a line may begin a beat after the last line's last syllable began (the kept 10th), where 844 asked an eighth and a quarter's rest; a fresh line's distance from the line before is drawn from the kept distances where the slot leaves room. TWO NOTES WHERE THREE WOULD CLASH (900; answers 749.79; amends 892): a guitar chord with no three notes clear of the voice is played as two; the share of sung notes with the accompaniment above them is read for a piano only. THE WEAK ENDING RULE RETIRED (901; answers 749.78 against the finding; retires 871 and 890 where the kept line ends stand). EACH FLAG ONCE (902; answers 749.81). THE LAST CHORUS AS KEPT SONGS LIFT IT (903; answers 749.75): Module 9.12 is read as the last chorus, with any tag after it, at least as long as the first; no level is raised.", "27.106"),
])

P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 182: HOW A LINE ENDS", H1)
W("What the session found in 887", H2)
W("The session reviewed Luthier v23 and v24 (lib/luthier/REVIEW_stage10_11.md), reproduced every record and both kept tables byte for byte, merged both versions into main, and rebuilt song 58 from its v24 record. It checked fix 887 hardest and found what this paper had missed. 887 drew a line's last note from the kept lengths, but only from those that left a quarter's rest before the next line; in a two-bar slot the long lengths seldom fit, so the short ones took their share. The rest reached the kept median by taking time from the held word: stressed last syllables an eighth or less stood at 29, 54 and 44 in a hundred against a kept 22, and held a half note or more at 29, 3 and 11 against a kept 31 (749.76). And with every line ending in a rest of about two beats the voice stopped after nearly every line, 12 to 14 silences of a beat or more in a hundred beats against a kept 7 to 11 (749.80). Kept songs hold the line's last word and still rest; and they run some lines into the next.")
W("One table (899)", H2)
W(f"Both findings are one fact about how a line ends, and it was read from the kept songs directly (lib/luthier/make_kept_line_ends.py). The transcribers of the kept corpus set a capital at the head of each lyric line, so a kept line can be read as the writer wrote it and not as a run of notes between rests. Over {KL['line_ends']} line ends the time from a line's last syllable to the next line's first note stands at {KL['G_percentiles_10_25_50_75_90'][1]:.0f}, {KL['G_percentiles_10_25_50_75_90'][2]:.0f} and {KL['G_percentiles_10_25_50_75_90'][3]:.0f} twelfths of a quarter by quartile, and a tenth of lines leave a single beat. The rest after the last syllable stands at {KL['rest_percentiles_10_25_50_75_90'][1]:.0f}, {KL['rest_percentiles_10_25_50_75_90'][2]:.0f} and {KL['rest_percentiles_10_25_50_75_90'][3]:.0f}; {pc(KL['lines_run_on_with_under_a_beat_of_rest_share'])} lines in a hundred run into the next with under a beat of rest, and by song that share is {pc(KL['run_on_share_by_song_quartiles'][0])}, {pc(KL['run_on_share_by_song_quartiles'][1])} and {pc(KL['run_on_share_by_song_quartiles'][2])} at the quartiles. The engine had forbidden all of it: since 844 a line could not begin until an eighth and a quarter's rest after the last line's last note began, and no line ran on.")
W("The table holds, for each weight of last syllable and each distance to the next line, the counts of each held length. The engine now draws the held length from it, so the note and the rest are a pair: where the next line is close the syllable is short or the line runs on, and where it is far the syllable may be held a half note and still leave a rest. The floor under a line's start is the kept tenth, one beat. And a fresh line's distance from the line before is drawn from the kept distances, where 870 drew a rest. Nothing is set by hand but the table's two grids.")
W(f"On the builds the silences of a beat or more fell from {B['before']['silences'][0]}, {B['before']['silences'][1]} and {B['before']['silences'][2]} in a hundred beats to {B['after']['silences'][0]}, {B['after']['silences'][1]} and {B['after']['silences'][2]}, inside the kept middle half, with their median at {B['after']['median_silence'][0]} to {B['after']['median_silence'][2]} beats; lines run on {pc(B['after']['run_on'][0])}, {pc(B['after']['run_on'][1])} and {pc(B['after']['run_on'][2])} times in a hundred; and the last syllable's length stands within ten points of the kept shares at both ends for every weight (Table GO).")
W("The rule that kept singers break (901)", H2)
W(f"The session's third finding asked that 871 be made a rule and not a weight: that at a line's end a word's weak syllable never be held longer than its stressed one (749.78). Fix 871 was this engine's answer to the session's own 749.64, and 890 widened it. Neither was ever read against kept songs. The table of line ends made the reading possible, and the first trial of the session's rule broke the table's own check: weak last syllables came out short {pc(0.70)} times in a hundred against a kept {pc(KL['an_eighth_or_less_by_tier'][1])}. So the thing itself was counted. In {KW['cases']} kept line ends on a word's weak syllable after its stressed one ('morning', 'summers', 'tomorrow'), the weak syllable is held longer than the stressed one in {pc(KW['weak_held_longer_share'])} in a hundred; the stressed syllable is given under a quarter in {pc(KW['stressed_under_a_quarter'])}, and a sixteenth in {pc(KW['stressed_a_sixteenth'])}. Kept singers land on the stressed syllable and hold the one after it, about as often as not. 871 and 890 are retired wherever the kept table stands, and 749.78 is answered against itself. The engine had been mending, for four versions, a thing that was not a fault.")
W("The guitar, the last chorus, and the small things (900, 902, 903)", H2)
W(f"Under song 54's tenor the guitar still rested under a third of the sung notes: with the seconds either side of the voice struck out, no three notes of the chord were left (749.79). It now plays the two that are, and sounds under every sung note in the three 4/4 songs ({SG['54']['after']['two_note_chords']} of song 54's {SG['54']['after']['chords']} strums are two notes). The share of sung notes with the accompaniment above them, a rule measured on piano song, is no longer printed against a guitar.")
W(f"On the last chorus the session did what Window 181 asked and brought kept evidence (studies/last_chorus/). The accompaniment does not thicken, as POP909 had said; what changes is length. The last chorus is longer than the first in {pc(LCK['longer'])} kept songs in a hundred and shorter in {pc(LCK['shorter'])}; its top note is higher in {pc(LCK['top_higher'])}; the recording is louder at its sung notes in {pc(LCK['louder'])}; a key change is rare ({LCK['key_change']}). So Module 9.12 stands, read as kept songs meet it: the last chorus, with any tag after it, at least as long as the first. The record prints the reading, and songs 55, 54 and 58 pass at {SG['55']['after']['nine12'][0]} bars against {SG['55']['after']['nine12'][1]}, {SG['54']['after']['nine12'][0]} against {SG['54']['after']['nine12'][1]}, and {SG['58']['after']['nine12'][0]} against {SG['58']['after']['nine12'][1]}. No level is raised and nothing is built: the lyrics here already end as kept songs end.")
W("Two findings are answered without a change to the builder. On stressed sixteenths in lines sung again (749.77), the session's count for song 54 included the halves of melismas; read on syllables, song 54's pick stands at 17 of 124 against a kept 12 in a hundred inside lines, and the builds' median at 8. The engine's other lines, at 5, are under the kept figure, so a check that holds returns to the other lines' rate holds them to a rate kept songs do not keep. The charge is not raised; the record now prints the reading on syllables. And on what is gated (749.81): only the whole fit is gated, never its parts, and a pick whose long notes sit badly passes; this paper says so. Each flag is printed once.")
for n_, title_, test_ in (
    ("899", "The last syllable and its rest drawn as a pair", "Test: by weight, line-final lengths within ten points of the kept shares at an eighth or less and at a half or more (749.76's check); silences of a beat or more per hundred beats and their median inside the kept quartiles (749.80's check)."),
    ("900", "Two notes where three would clash", "Test: the guitar under nine sung notes in ten in every 4/4 song with a guitar lead; no check read against a part it was not measured for (749.79's check)."),
    ("901", "The weak ending rule retired", "Test: line-final weak syllables' lengths at the kept shares; the kept rate of a weak syllable outlasting its stressed one printed beside the song's."),
    ("902", "Each flag once", "Test: no flag twice (749.81's check)."),
    ("903", "The last chorus as kept songs lift it", "Test: the last chorus, with its tag, at least as long as the first (749.75's check as the session set it).")):
    W(f"{n_} {title_}", H2); W(test_)
W("Table GO — how a line ends: kept songs, and the engine's builds before and after (40 builds a song; songs 55, 54, 58; shares by the last syllable's weight: function word, weak syllable, stressed).")
rows = [("", "Kept songs", "Song 55's builds, before; after", "Song 54's", "Song 58's")]
rows.append(("Last syllable an eighth or less", l3(KL["an_eighth_or_less_by_tier"]), *[f"{l3(B['before']['short'][i])}; {l3(B['after']['short'][i])}" for i in range(3)]))
rows.append(("Last syllable a half note or more", l3(KL["held_a_half_or_more_by_tier"]), *[f"{l3(B['before']['half'][i])}; {l3(B['after']['half'][i])}" for i in range(3)]))
rows.append(("From the last syllable to the next line, twelfths: 10th, quartiles, 90th", l3([int(x) for x in KL["G_percentiles_10_25_50_75_90"]]), *[f"{l3(B['before']['G'][i])}; {l3(B['after']['G'][i])}" for i in range(3)]))
rows.append(("The rest after the last syllable: 10th, quartiles, 90th", l3([int(x) for x in KL["rest_percentiles_10_25_50_75_90"]]), *[f"{l3(B['before']['rest'][i])}; {l3(B['after']['rest'][i])}" for i in range(3)]))
rows.append(("Lines that run on with under a beat of rest", f"{KL['lines_run_on_with_under_a_beat_of_rest_share']} (by song {l3(KL['run_on_share_by_song_quartiles'])})", *[f"{B['before']['run_on'][i]}; {B['after']['run_on'][i]}" for i in range(3)]))
rows.append(("Silences of a beat or more per hundred beats", "7.0, 9.1, 11.1", *[f"{B['before']['silences'][i]}; {B['after']['silences'][i]}" for i in range(3)]))
rows.append(("The builds' median place under the old 4/4 judge (withheld), after", "", *[B["after"]["j6"][i] for i in range(3)]))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W("Table GP — the four songs written again from their lyrics, as v24 left them; after this window.")
rows = [("", "Song 55", "Song 54", "Song 58", "Song 52, 6/8")]
rows.append(("Silences of a beat or more per hundred beats (kept 7.0, 9.1, 11.1)", *[ba(k, "silences") for k in O]))
rows.append(("Their median, beats (kept 1.5, 2.0, 3.0)", *[ba(k, "median_silence") for k in O]))
rows.append(("Lines that run on (kept songs 0.06, 0.20, 0.39)", *[ba(k, "run_on") for k in O]))
rows.append(("Stressed last syllables a half note or more (kept 0.27)", *[ba(k, "half", lambda x: x[2]) for k in O]))
rows.append(("Stressed last syllables an eighth or less (kept 0.24)", *[ba(k, "short", lambda x: x[2]) for k in O]))
rows.append(("Rest share inside sung sections (kept 0.21, 0.30, 0.39)", *[ba(k, "rest_share") for k in O]))
rows.append(("Sung notes with the guitar or piano under them, share", *[ba(k, "guitar_under") for k in O]))
rows.append(("Stressed sixteenths, of syllables: lines sung again; other lines, after (kept 0.12)", *[f"{SG[k]['after']['st16'][0]}; {SG[k]['after']['st16'][1]}" if k != "52" else "" for k in O]))
rows.append(("The last chorus's bars with its tag; the first's (903)", *[(f"{SG[k]['after']['nine12'][0]}; {SG[k]['after']['nine12'][1]}" if SG[k]["after"].get("nine12") else "") for k in O]))
rows.append(("The pick's fit of words to notes (kept 0.20, 0.29, 0.38)", *[ba(k, "fit") for k in O]))
rows.append(("The pick's fit by length (kept 0.13)", *[ba(k, "by_length") for k in O]))
rows.append(("Builds taken away by: the old charge; the joint gate; the words' gate, after", *[(lambda r: f"{r['old_charge']}; {r['joint_gate']}; {r['words_gate'] if r['words_gate'] is not None else 'not read'}")(SG[k]["after"]["removed"]) for k in O]))
rows.append(("Rhythm exponent of the pick (kept 0.61, 0.66, 0.72)", *[ba(k, "rhythm_scaling") if k != "52" else "" for k in O]))
rows.append(("Pitch exponent of the pick (kept 0.79, 0.90, 1.00)", *[ba(k, "pitch_scaling") if k != "52" else "" for k in O]))
rows.append(("Builds that survive, of 1,000", *[ba(k, "survivors") for k in O]))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W(f"What this window could not do. The builds end their lines as kept songs do; a single pick need not, for a song has a dozen line-final function words and their shares in one pick stand far from the table ({SG['54']['after']['half'][0]} held a half note in song 54's pick against a kept {KL['held_a_half_or_more_by_tier'][0]}). The engine's long distances between lines are still short of the kept: a quarter of kept lines leave six beats or more before the next and the engine's upper quartile is four and a half, because a two-bar slot holds no more; with the lines now running on, the rest share inside sung sections fell under the kept middle half in the picks of songs 55 and 54 ({SG['55']['after']['rest_share']}, {SG['54']['after']['rest_share']}). Song 54's pick fits its words less well than before ({SG['54']['after']['fit']}), inside the gate: the pick is one draw. A fifth of song 54's guitar strums are two notes, which no kept figure for a guitar speaks to. The retiring of 871 rests on one corpus's reading of where lyric lines begin. Song 52 in 6/8 has none of this: no kept line ends, no kept words, no build past the joint gate. And the pick is still the first build of the old charge's better half.")
W("")
for lead in ("WINDOW 182", "27.106 How a line ends", "Table GO", "Table GP", "903 The last chorus"):
    assert any(p_.text.strip().startswith(lead) for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v25.docx"); print("saved Luthier_v25.docx")
