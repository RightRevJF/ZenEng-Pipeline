import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v46.docx")
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










RT = "/home/claude/rightrevjf/zeneng-pipeline/"; J = lambda p: json.load(open(RT + p))
R = J("studies/proposed_v47/build_readings.json"); N7 = J("studies/soundness/neighbour_v47.json"); p1 = lambda x: round(100 * x, 1)
rp = [x["rule_fails_share"] for k, x in N7["a_random_pick_from"].items() if k.startswith("the engine's pool")][0]; nc = N7["neighbour"]["rule_fails_share"]
S6 = ("55", "54", "58", "60", "59", "49"); l3 = lambda v: ", ".join(str(x) for x in v); g = lambda c: [R[s][c] for s in S6]
sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v46")], "Luthier v46", "Luthier v47")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 46"))], "LUTHIER — VERSION 46", "LUTHIER — VERSION 47")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("203 Windows", "204 Windows"), ("Windows 1–203", "Windows 1–204"), ("203 scientific research windows", "204 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v218 (Luthier v47)")
set_cell(row.cells[1], f"FIVE PATCHES TESTED ONE AT A TIME; TWO BUILT, THREE MADE SETTINGS, ONE LEFT OUT. The songwriting session's Review 30 flagged five patches from song 62 and a trial of sections that loop less. Each was run alone on a thousand builds a song under rules written first (studies/proposed_v47). BUILT, ON BY DEFAULT: fix 959, no leap past an octave inside a line in 4/4 (no chosen tune holds one; it passes over about 3 living builds in 10); fix 962, a section that returns whole has its longest held notes lifted to a chord tone (songs 58, 60, 59, 49: {l3([len(R[s]['varied']) for s in ('58','60','59','49')])} notes). SETTINGS A LYRIC ASKS FOR: fix 960, chords that loop less (\"chords\": \"loop_less\"; the gate form alone held its first check, and it overdoes it: 99 verses in 100 at or under the kept median); fix 961, the title line's longest note on a stressed syllable (\"title_stress\": true); fix 963, no lowered thirds (\"blue_notes\": false). NOT BUILT: the plain-but-not-monotone region gate (6 to 22 builds of 3,000 left). The first build had 961 on by default and failed its own check: song 54's pool fell to 7, because 961 passed over 194 builds in song 54 and 213 in song 49, whose title lines end on a weak held syllable. The amendment was written before the second run. Second build: living builds {l3(g('live')[:3])} (v46: 342, 309, 419); builds' middle words' fit {l3(g('builds_fit')[:3])} (v46: 0.265, 0.221, 0.306); pools 24, 23, 22; the neighbour choice fails the rule {p1(nc)} times in a hundred, a random pool pick {p1(rp)} (v46: 2.2). 749.172 (the session's): my reading of 749.154, that the whole fit marks down change of pace, does not hold on kept songs (-0.03, p .53).")
after_par("27.127", [
    (" Fixes 959 to 963 (Window 204; Table HN; studies/proposed_v47/RESULT.md, RESULT_build.md). 959: gates() refuses a 4/4 build with a leap past an octave inside a line, read as sung (OCTAVE_GATE). 962: write() calls vary_returns(): in a section whose every line is a copy, the longest held note of each line after the first is lifted a scale step or more onto a chord tone, the leaps beside it kept within a fifth, never above the tune's top (VARY_RETURNS; recorded as melody.varied_returns). 960: \"chords\": \"loop_less\" redraws a verse or bridge, up to 30 times, until its chord repetition is at or under the kept median. 961: \"title_stress\": true refuses a build whose title line's longest note is on an unstressed syllable. 963: \"blue_notes\": false draws no lowered third. A chosen tune's words' fit is one draw and moves by up to 0.10 with any change; the builds' middle is the figure to check. HOLD-OUTS: song 59 for everything; songs 50 and 63 banked, not run.", "27.128"),
])
P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 204: THE FLAGGED PATCHES, TESTED AND BUILT", H1)
W("Review 30 left a list from song 62: five patches the session had written as flags and not turned on, and a trial of chords that loop less, after the covers finding (songs whose chords move are covered a little more). The writer asked that the rhythm be mended first and the looping chords not be forgotten. The rhythm lever failed in Window 203. This window takes the list. Each patch was run alone, rule first; then the kept ones were built together under seven checks written before the build.")
W("The patches one at a time", H2)
W("Songs 58, 60, 61 and 62, a thousand builds a song a flag. The octave gate: no chosen tune keeps a leap past an octave inside a line; it passes over about 10 tries in 100, which is 3 in 10 of the builds that would otherwise live; the builds' words' fit does not move. Read the same way, 28 kept songs of 160 hold such a leap at all, so a ban is a little stricter than the kept songs. Kept. The title gate: on these four songs it cost 0.2 to 5 tries in 100 and mended song 62's title line. Kept, then (below). Blue notes off: no lowered third, no cost; a setting, never a default. Varied returns: held notes lifted in the second chorus, nothing else moved. Kept. The region gate, asking a tune to be plain and not monotone together: it does what it says and leaves 6 to 22 builds of 3,000, with the words' fit down in three songs. Not built. The finding behind it stands (749.170); the remedy is in the draw, not at the gate.")
W("One thing learned on the way: a chosen tune's words' fit moved by up to 0.10 under flags that left the builds behind it unmoved. A chosen tune is one draw, and any change picks another. The builds' middle is the figure that can be checked to 0.02.")
W("Chords that loop less (749.159)", H2)
W("Three forms, on a thousand drafted sections a kind. The session's patch, filtering kept templates, leaves song 61's verse at 0.64 and fails its first check; so does its first repair. Its second, a gate that redraws a verse or bridge until its repetition is at or under the kept median, holds the first check in four songs of four and costs the words nothing. But it puts 99 verses in 100 under a line that half the kept verses are over, and its verses simply loop 17 times in 100 where kept verses do 30 and the unpatched writer 32. It moves the writer past the kept songs, not back to them. And the finding it serves is not settled: 0.071 across artists, 0.042 within artists, 0.028 on fresh songs. So it is a setting a lyric can ask for, fix 960, and not the default. Song 63 was kept for the day a default is at stake and is not run. A gentler gate, trimming only verses over the kept 75th, is the form to try next.")
W("The first build, and the title gate", H2)
W("With 959, 961 and 962 on, song 54's pool fell to 7 builds, under the floor of 10 the checks had set. The title gate was the cause: it passed over 194 builds in song 54 and 213 in song 49. Song 49's title line is \"The world is asking\". Its last syllable is weak; a line's last note is usually its longest; song 49's own intake asked for that syllable to be held. The gate is right for song 62's \"remembered\" and wrong as a law: it forbids a feminine ending in every title. Four songs had been too few to see that its cost hangs on the title's last syllable. The amendment, written before the second run, makes it a setting. Before it could be more, the kept songs must be read for where a title line's longest note falls.")
W("The second build", H2)
W(f"959 and 962 on. Living builds of a thousand: {l3(g('live'))} (songs 55, 54, 58, 60, 59, 49). No chosen tune holds a leap past an octave. The builds' middle words' fit in the three songs of the rule: {l3(g('builds_fit')[:3])}, against 0.265, 0.221, 0.306 before. The chosen tunes pass the soundness rule with the one lean they had, rhythm scaling, low. Range floors and pitch ceilings hold. The pools are 24, 23 and 22 (v46: 39, 25, 39): the neighbour choice fails the rule {p1(nc)} times in a hundred and a random pool pick {p1(rp)}, where v46's was 2.2. That is inside the standard of 10 and nearer to it; the octave gate's cost in builds is where it comes from. If later windows need the builds back, a ceiling of one such leap a song is the kept-shaped form.")
W("Returning choruses now vary: 1 note in song 58, 2 in song 60, 4 in song 59 (the hold-out), 4 in song 49. The two-line tags of songs 55 and 54 still return note for note; nothing in them could be lifted inside the rules, and a tag is a repeat by design. Song 52, in 6/8, changes by one note: its second chorus returned whole and 962 lifts one held note a third. Song 53, the hymn, is byte for byte the same.")
for n_, title_, test_ in (
    ("749.174", "The title gate's cost depends on the title's last syllable", "Test: builds passed over by 961 in a thousand, songs 58, 60, 61, 62 (2 to 53) against songs 54 and 49 (194, 213); song 54's pool with 961 on (7). A setting until the kept songs are read."),
    ("749.175", "A chosen tune's words' fit is a draw", "Test: the chosen tune's words' fit under each flag against the builds' middle (song 61: 0.363, 0.272, 0.265 over builds at 0.238, 0.244, 0.242). Checks to 0.02 are read on the builds from here on."),):
    W(f"{n_} {title_}", H2); W(test_)
W("Table HN — Luthier v47, the second build: a thousand builds a song.")
rows = [("", "Song 55", "Song 54", "Song 58", "Song 60", "Song 59", "Song 49")]
for lab, c in (("Builds that live", "live"), ("Passed over by the octave gate", "killed_959"), ("Builds' middle words' fit", "builds_fit"), ("Chosen tune's words' fit", "fit"), ("Chosen tune's range, semitones", "range"), ("Chosen tune's rhythm scaling (kept 0.608, 0.656, 0.721)", "rs"), ("Leaps past an octave in a line", "leaps")):
    rows.append((lab, *[f"{R[s][c]:g}" for s in S6]))
rows.append(("Held notes varied in returning sections", *[str(len(R[s]["varied"])) for s in S6]))
rows.append(("Title lines with the longest note stressed (gate off)", *[f"{R[s]['title'][0]} of {R[s]['title'][1]}" for s in S6]))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W("The records. Songs 55, 54, 58, 59, 49 and 52 are run again; song 60's is songs/p70/lyric60.v47.song.json, its delivered record untouched; song 53 unchanged. Every room file is read again and both checks pass. Songs 50 and 63 have not been run.")
W("What this window could not do. Rhythm scaling still leans low and nothing here touches it; the session's 749.171, what the engine does inside a one-bar line, is where that goes next. My reading of 749.154 is withdrawn: the session put it to the kept songs and it does not hold (749.172). Not begun: song 58's bars of rest (749.144), a short line in a long slot (749.147), the hymn items (749.148 to 749.152), the ruling on strings (749.163).")
W("")
for lead in ("WINDOW 204", "27.128", "Table HN", "749.174 The title"):
    assert any(p_.text.strip().startswith(lead) or lead in p_.text[:40] for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v47.docx"); print("saved Luthier_v47.docx")
