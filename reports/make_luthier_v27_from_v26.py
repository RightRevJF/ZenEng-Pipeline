"""Luthier v26 -> v27: the session's fix list for v27 (749.84 to 749.89) answered, and every kept rhythm let in
(Window 184, Module 27.108, Tables GS and GT; fixes 907-912). Evidence: lib/luthier/stage14_results.json, REVIEW_stage13.md, songs/p68/fixlist_v27.md.
Run: python3 make_luthier_v27_from_v26.py"""
import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v26.docx")
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










R = json.load(open("/home/claude/rightrevjf/zeneng-pipeline/lib/luthier/stage14_results.json")); SG = R["songs"]; EN = R["entries"]; WN = R["windows"]["rows"]; BU = R["builds"]; LF = R["lifts"]
pc = lambda x: f"{100 * x:.0f}"; O = ("55", "54", "58", "52"); l3 = lambda v: ", ".join(str(x) for x in v)
def ba(k, key, f=lambda x: x):
    a, b = SG[k]["before"].get(key), SG[k]["after"].get(key); return f"{f(a) if a is not None else ''}; {f(b) if b is not None else ''}" if (a is not None or b is not None) else ""

sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v26")], "Luthier v26", "Luthier v27")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 26"))], "LUTHIER — VERSION 26", "LUTHIER — VERSION 27")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("183 Windows", "184 Windows"), ("Windows 1–183", "Windows 1–184"), ("183 scientific research windows", "184 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v198 (Luthier v27)")
set_cell(row.cells[1], f"THE PICK AMONG ITS OWN BUILDS, AND EVERY KEPT RHYTHM. The session reviewed version 26, confirmed the mended parse note for note, checked its own studies for the same fault (two had it; no conclusion changed), and sent six findings. The two a listener would hear first: song 58's verses sat at the bottom of the baritone, because a chorus lift drawn past the voice's room was clamped to the room and the key followed; and its pick fitted its words worse than nine kept songs in ten while three in four of its own builds fitted better than the median kept song. The lift is now drawn from the kept lifts the voice has room for and the key puts the verse at the voice's middle. The words' fit now gates as the old charge does, at the builds' better half, whole and by length; the picks' fits stand at {SG['55']['after']['fit']}, {SG['54']['after']['fit']} and {SG['58']['after']['fit']}. And a cause of the engine's squareness was found in its own table: only the sixty commonest kept rhythms for each length of line were kept, a quarter to two fifths of kept lines, and the commonest are the squarest. Every kept rhythm may now be drawn at its kept share.")

after_par("27.107 The kept corpus read whole", [
    (" The session's fix list for v27, and every kept rhythm (Window 184; Tables GS, GT; songs/p68/fixlist_v27.md). THE LIFT WITHIN THE VOICE'S ROOM (907; answers 749.84; amends 838, 804): the plan's lift is drawn from the kept lifts no greater than the voice's range less an octave; the key is the instrument's key, among those that put the verse's median note within three semitones of the voice's middle. THE WORDS' FIT GATES AT THE BETTER HALF (908; answers 749.85; amends 881): past the old charge's gate and the joint gate, a build must fit its words at least as well as the median of its song's builds, whole and by length, and no worse than the kept tenth. A LONG PHRASE ENDS IN A BREATH (909; answers 749.88; amends 899): where the phrase running into a line's end is already past eight beats, the last syllable's length is drawn from those that leave half a beat of rest. THE PLAN'S MAKER IN THE REPO (910; answers 749.86). CONSTANTS GIVEN MAKERS (911; answers 749.89): the shares of lines entering before, on and after the bar line (771) and the least share of stressed syllables on a beat (731) are read from tables/kept_line_ends.json; 847's figure is recounted in tables/kept_word_weight.json and stands; 876's share is 0.09. EVERY KEPT RHYTHM (912; amends 653, 812): the table holds every kept two-bar rhythm and every kept bar; a fresh line's rhythm is drawn from all that fit, each at its kept count times its score, with no cut to the twelve best.", "27.108"),
])

P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 184: THE PICK AMONG ITS OWN BUILDS, AND EVERY KEPT RHYTHM", H1)
W("What the session sent", H2)
W("The session reviewed Luthier v26 (lib/luthier/REVIEW_stage13.md). The mended parse matched its own tie-aware parse note for note and the tables rebuilt byte for byte. It checked its own studies for the fault of 749.82: only the silences and the last-chorus studies had read the old parse, and rerun, neither changes its conclusion; the melisma shares behind 848, the slots behind 869, the degrees behind 846 and the 0.73 behind 840 were read by parsers that kept tie starts, and stand. It rebuilt song 58 in its new key and sent six findings (749.84 to 749.89).")
W("The lift and the key (907)", H2)
W(f"Version 26 had moved song 58 from C to A. The session found why. The plan draws one lift from the kept songs' lifts, which stand at {l3(LF['kept_quartiles'])} semitones by quartile and {LF['kept_90th']:.0f} at the ninetieth; song 58 drew 12, song 54 drew 11. A lift past the voice's room was clamped to the room, so every such draw landed on the room itself, 9 for a baritone and for a tenor, and the key was then chosen to fit the whole span: the verses went to the floor of the voice, six semitones under a baritone's middle. The lift is now drawn from the kept lifts the voice has room for, and the key is chosen by the verse: among the keys that put the verse's median note within three semitones of the voice's middle, the instrument's keys first. Songs 55 and 54 now sing their verses half a semitone from the voice's middle. Song 58 drew 9 again, the largest lift a baritone has room for, and its verse sits three and a half semitones under the middle with the chorus at the voice's ceiling: with a lift that spans the voice there is nowhere else to put it.")
W("The pick among its own builds (908)", H2)
W(f"The session read each pick's fit beside its own builds'. Song 58's builds fitted their words at {l3(SG['58']['before']['builds_fit'])} by quartile and the pick at {SG['58']['before']['fit']}; song 54's at {l3(SG['54']['before']['builds_fit'])} and {SG['54']['before']['fit']}. The gate at the kept tenth passed nearly every build, and the first build past the gates was taken wherever its fit fell. The session offered two mends: a gate at the kept 25th, or the first build at or over the builds' median fit. The second is taken, because it is what this engine already does with the old charge (874): a reading that tells damage and not grade may hold a build to the better half of its own song's builds without claiming to rank songs. The fit is held so whole and by length, with the kept tenth still the floor. It takes away 199 to 230 builds of each song's 320 to 360 that pass the other gates, and the picks' fits now stand at {SG['55']['after']['fit']}, {SG['54']['after']['fit']} and {SG['58']['after']['fit']} (kept quartiles {l3(R['fit_kept'][1:4])}), by length at {SG['55']['after']['by_length']}, {SG['54']['after']['by_length']} and {SG['58']['after']['by_length']} (kept median {R['fit_by_length_kept']}).")
W("Why the engine is square (911, 912)", H2)
W(f"Window 183 closed on the engine's builds landing on the beat more often than kept songs do, and named three constants from the old parse. They are recounted here, with makers. The shares of lines that enter within a beat before a bar line, on it, or elsewhere stood in the code at {l3(EN['old_constants']['stressed'])} for a line opening on a stress; read from {EN['kept']['lines'][0]:,} kept lines they are {l3(EN['kept']['stressed'])}: a stressed opening lands on the bar line {pc(EN['kept']['stressed'][1])} times in a hundred, not {pc(EN['old_constants']['stressed'][1])}. For an unstressed opening {l3(EN['kept']['unstressed'])} where the code had {l3(EN['old_constants']['unstressed'])}. A kept song's stressed syllables fall on a beat {pc(R['stressed_on_a_beat_by_song'][3])} times in a hundred at the median and {pc(R['stressed_on_a_beat_by_song'][1])} at the tenth; the floor under a build, 0.4 by hand, is now that tenth. The stressed syllable of a word stands higher than its other syllable, level with it, or lower {l3(R['within_word'])} of the time over {R['within_word_pairs']:,} pairs, as 847 had it.")
W(f"None of the three moved the builds much. The larger cause was in the table itself. Since 653 a fresh line's rhythm has been a kept two-bar rhythm taken whole; since 812 the table has held the sixty commonest for each count of notes; and the engine scores those and draws among the twelve best. For a line of seven notes the kept songs sing {WN['7'][0]} distinct two-bar rhythms, and the sixty commonest carry {pc(WN['7'][1])} lines in a hundred. The commonest are the squarest: over all kept rhythms of six notes {pc(WN['6'][2])} onsets in a hundred are on a beat, over the sixty commonest {pc(WN['6'][3])}, over the twelve commonest {pc(WN['6'][4])}. The cut that was made for the table's size, and the second cut for speed, both leaned the engine toward the beat, and toward sameness. It is the fault stage 7 found in the judge, aiming at the commonest, standing in the builder since Window 153. The table now holds every kept rhythm, and a fresh line is drawn from all that fit, each at its kept count times its score. The builds' onsets on the beat fall from {l3(BU['before'])} to {l3(BU['after'])}, against a kept {l3(BU['kept'])} by quartile: nearer, and still over the kept median. What remains is that two lines in three are not fresh, and that the words' fit and the title's rule each reward a stress on the beat.")
W("Phrases, the plan's maker, and one field (909, 910)", H2)
W(f"With breaths read at half a beat the picks' long phrases ran at twice the kept share, because 899 drew each line's rest alone and lines could run on in a chain (749.88). A phrase already past eight beats now ends in half a beat of rest at the least. The share of phrases over twelve beats stands at {SG['55']['after']['phrases'][0]}, {SG['54']['after']['phrases'][0]} and {SG['58']['after']['phrases'][0]} against a kept {R['phrases_kept']['share_over_12_beats']}; song 54 is still over. The maker of the register plan now reads the kept corpus inside the repo, on the kept songs' own list ({LF['songs_in_plan']} songs with a verse and a chorus), and its stray output is gone (749.86). And the maker of the 4/4 table gives back every field of the old table from the old parse but one: the quartiles of surprise differ in the third place ({l3([2.73, 2.956, 3.146])} in the old table, {l3([2.741, 2.963, 3.152])} remade), the old figure was written by a script of stage 7 that is not in the repo, and the step that differs was not found; the README now names the field (749.87).")
for n_, title_, test_ in (
    ("907", "The lift within the voice's room; the key by the verse", "Test: no pile of lifts at the room; the verse's median note within three semitones of the voice's middle (749.84's check)."),
    ("908", "The words' fit gates at the builds' better half", "Test: each 4/4 pick's fit as sung in the kept middle half, and its fit by length (749.85's check)."),
    ("909", "A long phrase ends in a breath", "Test: phrases over twelve beats at or under 0.06; the longest at or under the kept 75th (749.88's check)."),
    ("910", "The plan's maker in the repo", "Test: kept_plan.py writes the table on a fresh clone (749.86's check)."),
    ("911", "Constants given makers", "Test: each constant has a maker or a line saying where it came from (749.89's check)."),
    ("912", "Every kept rhythm may be drawn", "Test: the builds' onsets on the beat nearer the kept median than before on every 4/4 song.")):
    W(f"{n_} {title_}", H2); W(test_)
W("Table GS — the kept two-bar rhythms, by the count of notes in them.")
rows = [("Notes in the two bars", "Distinct kept rhythms", "Lines in the sixty commonest, share", "Onsets on a beat: all kept", "the sixty commonest", "the twelve commonest")]
for k in ("5", "6", "7", "8", "9"): rows.append((k, *WN[k]))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W("Table GT — the four songs written again from their lyrics: as v26 left them; after this window.")
rows = [("", "Song 55", "Song 54", "Song 58", "Song 52, 6/8")]
rows.append(("Key; the notes sung (midi)", *[f"{SG[k]['before']['key']}, {SG[k]['before']['sung'][0]}–{SG[k]['before']['sung'][1]}; {SG[k]['after']['key']}, {SG[k]['after']['sung'][0]}–{SG[k]['after']['sung'][1]}" for k in O]))
rows.append(("The verse's median note; the voice's middle", *[f"{SG[k]['before']['verse_centre']:.0f}; {SG[k]['after']['verse_centre']:.0f}; {SG[k]['after']['voice_middle']}" for k in O]))
rows.append(("The plan's lift; the lift sung (kept 0, 1, 4)", *[f"{SG[k]['before']['lift_plan']}, {SG[k]['before']['lift_sung']:.0f}; {SG[k]['after']['lift_plan']}, {SG[k]['after']['lift_sung']:.0f}" for k in O]))
rows.append((f"The pick's fit of words to notes (kept {l3(R['fit_kept'][1:4])})", *[ba(k, "fit") for k in O]))
rows.append((f"The pick's fit by length (kept {R['fit_by_length_kept']})", *[ba(k, "by_length") for k in O]))
rows.append(("The builds' fit, quartiles, after", *[(l3(SG[k]["after"]["builds_fit"]) if SG[k]["after"].get("builds_fit") else "") for k in O]))
rows.append(("Builds taken away by: the old charge; the joint gate; the words' gate, after", *[(lambda r: f"{r['old_charge']}; {r['joint_gate']}; {r['words_gate'] if r['words_gate'] is not None else 'not read'}")(SG[k]["after"]["removed"]) for k in O]))
rows.append((f"Sung phrases over twelve beats, share; the longest (kept {R['phrases_kept']['share_over_12_beats']}; {l3(R['phrases_kept']['each_songs_longest_quartiles'])})", *[f"{SG[k]['before']['phrases'][0]}, {SG[k]['before']['phrases'][1]}; {SG[k]['after']['phrases'][0]}, {SG[k]['after']['phrases'][1]}" for k in O]))
rows.append((f"Onsets on the beat (kept {l3(BU['kept'])})", *[ba(k, "on_beat") for k in O]))
rows.append((f"Stressed syllables on a beat (kept by song {l3(R['stressed_on_a_beat_by_song'][2:])})", *[ba(k, "stressed_on_beat") for k in O]))
rows.append((f"Rest share inside sung sections (kept {l3(R['rest_share_kept'][1:4])})", *[ba(k, "rest_share") for k in O]))
rows.append(("Rhythm exponent of the pick", *[ba(k, "rhythm_scaling") if k != "52" else "" for k in O]))
rows.append(("Pitch exponent of the pick", *[ba(k, "pitch_scaling") if k != "52" else "" for k in O]))
rows.append(("Builds that survive, of 1,000", *[ba(k, "survivors") for k in O]))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W(f"What this window could not do. The picks' stressed syllables fall on a beat {pc(SG['55']['after']['stressed_on_beat'])}, {pc(SG['54']['after']['stressed_on_beat'])} and {pc(SG['58']['after']['stressed_on_beat'])} times in a hundred against a kept {pc(R['stressed_on_a_beat_by_song'][3])} at the median and {pc(R['stressed_on_a_beat_by_song'][4])} at the upper quartile: the gate of 908 holds a pick to the builds that fit their words best, the fit counts a stress on a strong beat in its favour, and so the mend of one finding leans against the mend of another. The engine is still squarer than kept songs. Song 58's verse is half a semitone outside the three the session asked. Song 54's long phrases are still over the kept share, and song 55's longest is half a beat over the kept upper quartile. The picks' rest share stands at or under the kept lower quartile on songs 55 and 54 ({SG['55']['after']['rest_share']}, {SG['54']['after']['rest_share']}). The rhythm exponent of every pick is under the kept middle half. The old 4/4 judge's data is still of the old parse. Song 52 in 6/8 is carried once more. And the pick is the first build past three gates of which none tells a great song from a good one.")
W("")
for lead in ("WINDOW 184", "27.108 The session's fix list for v27", "Table GS", "Table GT", "912 Every kept rhythm"):
    assert any(p_.text.strip().startswith(lead) for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v27.docx"); print("saved Luthier_v27.docx")
