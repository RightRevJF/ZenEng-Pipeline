"""Luthier v27 -> v28: the session's fix list for v28 (749.90 to 749.92) answered
(Window 185, Module 27.109, Table GU; fixes 913-915). Evidence: lib/luthier/stage15_results.json, REVIEW_stage14.md, songs/p68/fixlist_v28.md.
Run: python3 make_luthier_v28_from_v27.py"""
import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v27.docx")
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










R = json.load(open("/home/claude/rightrevjf/zeneng-pipeline/lib/luthier/stage15_results.json")); SG = R["songs"]; K = R["kept"]; SE = R["session"]
pc = lambda x: f"{100 * x:.0f}"; O = ("55", "54", "58", "52"); T3 = ("55", "54", "58"); l3 = lambda v: ", ".join(str(x) for x in v)
def ba(k, key, f=lambda x: x):
    a, b = SG[k]["before"].get(key), SG[k]["after"].get(key); return f"{f(a) if a is not None else ''}; {f(b) if b is not None else ''}" if (a is not None or b is not None) else ""
af = lambda key: l3([SG[k]["after"][key] for k in T3]); bf = lambda key: l3([SG[k]["before"][key] for k in T3])

sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v27")], "Luthier v27", "Luthier v28")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 27"))], "LUTHIER — VERSION 27", "LUTHIER — VERSION 28")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("184 Windows", "185 Windows"), ("Windows 1–184", "Windows 1–185"), ("184 scientific research windows", "185 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v199 (Luthier v28)")
set_cell(row.cells[1], f"THE BEAT LET GO. Version 27 let every kept rhythm in and held the pick to the builds that fit their words best; the session showed that the two together made the songs squarer, not looser. The weight that pulls each syllable to its kept place in the bar had been fitted when twelve rhythms were on offer; with hundreds on offer it picked the most stress-aligned of them, and the gate on the whole fit, a third of which is place, pushed the same way: song 58's stressed syllables fell on a beat {pc(SG['58']['before']['stressed_on_beat'])} times in a hundred against a kept {pc(K['stressed_on_a_beat'][1])}. The place weight is halved, refitted to the kept median of the fit by place; the gate holds a pick to the better half of its builds by length and by height and leaves place to the floor; the gate reads each build as sung, its melismas placed; and a line that would run with the next past twelve beats ends in a breath. The three 4/4 picks now stand inside the kept middle half on stressed syllables on a beat ({af('stressed_on_beat')}), on onsets on the beat ({af('on_beat')}, the kept median {K['onsets_on_the_beat'][1]}), on the fit whole, by place and by height, on rest share, and on the verse's place in the voice.")

after_par("27.108 The session's fix list for v27", [
    (" The beat let go; the session's fix list for v28 (Window 185; Table GU; songs/p68/fixlist_v28.md). THE PLACE WEIGHT REFITTED (913; answers 749.90; amends 879, 908): the power of the place term is 0.75, fitted with every kept rhythm on offer so that the builds' fit by place meets the kept median; the words' gate holds a build to its song's median by length and by height, and the whole fit only to the kept tenth. THE GATE READS THE SONG AS SUNG (914; answers 749.91; amends 848, 908): the melismas are drawn on every build before the words' gate, by the draw that will place them on the pick. A LINE LOOKS AHEAD (915; answers 749.92; amends 909): where the phrase from its start to the end of the next line would pass twelve beats, the line ends in half a beat of rest at the least.", "27.109"),
])

P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 185: THE BEAT LET GO", H1)
W("What the session found in 908 and 912 (913)", H2)
W(f"The session reviewed Luthier v27 (lib/luthier/REVIEW_stage14.md); all five makers ran from the repo and every record reproduced. It checked fixes 908 and 912 hardest and answered the question Window 184 had put to it: whether the words' gate should leave place out. Its answer was yes, and that this alone would do little, because the builds were already square before the gate saw them. It ran each song's thousand builds. Their stressed syllables fell on a beat {l3(SE['builds_stressed_on_a_beat_at_1_5'])} of the time at the median against a kept {l3(K['stressed_on_a_beat'])} by quartile; only {pc(SE['builds_in_kept_middle_half'][2])} in a hundred of song 58's builds stood in the kept middle half. The cause was a constant of this engine's own. The power of the place term, 1.5, was fitted in Window 179 when a line was drawn from the twelve best of sixty rhythms. Fix 912 put every kept rhythm on offer, several hundred for a line, and the same power then chose the most stress-aligned of them all. A weight fitted to one field of choice was left standing when the field was widened thirtyfold.")
W(f"The session swept the power. At 1.5 the builds' fit by place stood at {l3(SE['sweep']['at_1_5']['place'])} on songs 55 and 58, over the kept median of {K['by_place'][1]}; at 0.75, {l3(SE['sweep']['at_0_75']['place'])}, with the whole fit at {l3(SE['sweep']['at_0_75']['fit'])} beside the kept {K['fit'][2]}; at nothing the fit by place fell under the kept lower quartile. So the power is 0.75. And the gate of 908, which held a pick to its builds' median on the whole fit, a third of which is place, now holds it to the median by length and by height, the two parts no rule draws for, and holds the whole fit only to the kept tenth. The picks' stressed syllables on a beat fall from {bf('stressed_on_beat')} to {af('stressed_on_beat')}; their onsets on the beat from {bf('on_beat')} to {af('on_beat')}, at the kept median of {K['onsets_on_the_beat'][1]}; their fit by place from {bf('by_place')} to {af('by_place')}. The squareness this paper has carried since Window 183 is gone from the picks.")
W("The gate reads the song as sung (914)", H2)
W(f"The gate read each build before its melismas were placed, and a melisma halves its syllable's first note, as kept melismas do. Song 58's pick passed the gate at {SE['length_at_gate_and_as_sung_song58'][0]} by length and stood at {SE['length_at_gate_and_as_sung_song58'][1]} as sung (749.91). The draw of 848 is now a function of the notes alone, seeded as before by the title, and is made on every build before the words' gate; the pick's melismas are the ones the gate saw. The picks' fits by length as sung stand at {af('by_length')}, each at or over its builds' median as sung ({l3([SG[k]['after']['gate']['the_builds_median_fit_by_length'] for k in T3])}); song 54's is under the kept median of {K['by_length'][1]} and inside the kept middle half.")
W("A line looks ahead (915)", H2)
W(f"Fix 909 ended a line in a breath once its phrase had passed eight beats, read at the line's last note. The session found that every long phrase left was two lines run together, the first not yet at eight beats when its end was drawn (749.92). A line now looks ahead: where the phrase from its start to the end of the next line would pass twelve beats, it ends in half a beat of rest at the least. Phrases over twelve beats stand at {l3([SG[k]['after']['phrases'][0] for k in T3])} of each song's phrases against a kept {K['phrases']['share_over_12_beats']}, with longest phrases of {l3([SG[k]['after']['phrases'][1] for k in T3])} beats. Song 55 keeps one phrase of seventeen beats, a single long line with no rest inside it, over the kept upper quartile of {K['phrases']['each_songs_longest_quartiles'][2]}.")
for n_, title_, test_ in (
    ("913", "The place weight refitted; the gate by length and height", "Test: each 4/4 pick's stressed syllables on a beat, and its fit whole, by place and by height, in the kept middle half (749.90's check)."),
    ("914", "The words' gate reads the song as sung", "Test: the pick's fit by length as sung at or over its builds' median as sung (749.91's check)."),
    ("915", "A line looks ahead to the next", "Test: phrases over twelve beats at or under 0.06 of a song's phrases; the longest at or under 15.5 beats (749.92's check).")):
    W(f"{n_} {title_}", H2); W(test_)
W("Table GU — the four songs written again from their lyrics: as v27 left them; after this window. Kept figures are quartiles by song, tie starts read.")
rows = [("", "Kept songs", "Song 55", "Song 54", "Song 58", "Song 52, 6/8")]
rows.append(("Stressed syllables on a beat", l3(K["stressed_on_a_beat"]), *[ba(k, "stressed_on_beat") for k in O]))
rows.append(("Onsets on the beat", l3(K["onsets_on_the_beat"]), *[ba(k, "on_beat") for k in O]))
rows.append(("The fit of words to notes", l3(K["fit"][1:4]), *[ba(k, "fit") for k in O]))
rows.append(("The fit by place in the bar", l3(K["by_place"]), *[ba(k, "by_place") for k in O]))
rows.append(("The fit by length", l3(K["by_length"]), *[ba(k, "by_length") for k in O]))
rows.append(("The fit by height", l3(K["by_height"]), *[ba(k, "by_height") for k in O]))
rows.append(("Sung phrases over twelve beats, share; the longest in beats", f"{K['phrases']['share_over_12_beats']}; {l3(K['phrases']['each_songs_longest_quartiles'])}", *[f"{SG[k]['before']['phrases'][0]}, {SG[k]['before']['phrases'][1]}; {SG[k]['after']['phrases'][0]}, {SG[k]['after']['phrases'][1]}" for k in O]))
rows.append(("Rest share inside sung sections", l3(K["rest_share"]), *[ba(k, "rest_share") for k in O]))
rows.append(("The verse's median note from the voice's middle, semitones", "", *[ba(k, "verse_off") for k in O]))
rows.append(("Builds taken away by: the old charge; the joint gate; the words' gate, after", "", *[(lambda r: f"{r['old_charge']}; {r['joint_gate']}; {r['words_gate'] if r['words_gate'] is not None else 'not read'}")(SG[k]["after"]["removed"]) for k in O]))
rows.append(("Rhythm exponent of the pick", l3(K["rhythm_scaling"]), *[ba(k, "rhythm_scaling") if k != "52" else "" for k in O]))
rows.append(("Pitch exponent of the pick", l3(K["pitch_scaling"]), *[ba(k, "pitch_scaling") if k != "52" else "" for k in O]))
rows.append(("Key", "", *[ba(k, "key") for k in O]))
rows.append(("Length in seconds", "165, 206, 243", *[ba(k, "seconds") for k in O]))
rows.append(("Builds that survive, of 1,000", "", *[ba(k, "survivors") for k in O]))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W(f"What this window could not do. The rhythm exponent of every pick ({af('rhythm_scaling')}) is under the kept middle half ({l3(K['rhythm_scaling'])}), as it has been since Window 178: the engine's rhythm still has less order across scales than a kept song's, and taking the turns out for length (888) did not help it. The pitch exponent of the picks of songs 54 and 58 is over the kept upper quartile. Song 55's fit by length is over the kept middle half and its longest phrase over the kept upper quartile. Songs 54 and 58 are past the kept lengths because their lyrics are. The words' gate now takes three builds in four of those that pass the other gates, on two parts of a reading that does not tell a great song from a good one. The old 4/4 judge's data is of the old parse. Song 52 in 6/8 has no kept pop corpus and is carried again. And there is still no stated point at which this engine is called sound: each window has mended what the last one's review found, and a review can always find a reading that stands outside the kept middle half.")
W("")
for lead in ("WINDOW 185", "27.109 The beat let go", "Table GU", "915 A line looks ahead"):
    assert any(p_.text.strip().startswith(lead) for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v28.docx"); print("saved Luthier_v28.docx")
