import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v48.docx")
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
K = J("studies/the_draw/kept.json"); BD = {s: J(f"studies/the_draw/builds_lyric{s}.json") for s in ("55", "54", "58", "49")}; WE = J("studies/the_draw/whole_engine.json"); CH = J("studies/the_draw/climb_held.json")
l3 = lambda v: ", ".join(str(x) for x in v); pc = lambda x: round(100 * x, 1); S4 = ("55", "54", "58", "49"); S8 = ("55", "54", "58", "49", "60", "59", "61", "62")
A = lambda s, k, f: BD[s]["A"][k][f]
sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v48")], "Luthier v48", "Luthier v49")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 48"))], "LUTHIER — VERSION 48", "LUTHIER — VERSION 49")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("205 Windows", "206 Windows"), ("Windows 1–205", "Windows 1–206"), ("205 scientific research windows", "206 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v220 (Luthier v49)")
live = lambda f: l3([f"{WE[s]['v47']['live']} to {WE[s][f]['live']}" for s in S8])
set_cell(row.cells[1], f"THE DRAW READ: THE PLANTED PEAK MAKES THE LEAPS; TWO FORMS OF A MEND TRIED AND NOT BUILT. The engine writes v47's notes. Review 33 turned the work to the draw. 749.186 (the reading of 749.182, rule first; each record's fitted spec run again): half to two thirds of the builds' leaps past an octave have the planted peak (fix 950) as their far note ({l3([A(s, 'as it is', 'far_note_is_the_builds_top_in_a_chorus') for s in S4])}; songs 55, 54, 58, 49), and with the plant taken out the builds holding such a leap fall from {l3([pc(A(s, 'as it is', 'builds_with_a_leap')) for s in S4])} in 100 to {l3([pc(A(s, 'the plant taken out', 'builds_with_a_leap')) for s in S4])}, under the kept songs' 17.5; but the builds' middle range falls to 13 or 14 semitones. A build with such a leap has a dozen, the carrying line being copied into every later chorus. 749.187 (the reading of 749.183): by title line the draw holds a weak word long as often as kept songs do ({l3([BD[s]['B']['cases_in_100_title_lines'] for s in S4])} lines in 100 against {K['B']['cases_in_100_title_lines']}), and the cases are of the kept kind; there is no fault of the draw there, and 749.177 closes. THE MEND, FIRST FORM (the carrying line drawn until it reaches the peak with no leap past an octave): living builds rise in six songs of six and the gate's cost about halves, but the test failed twice on marks set first (the gate's cut a build short of a half in songs 58 and 49; the hold-out's peak planted in 75 builds of 100 where 80 were allowed). The writer ruled: hold it. SECOND FORM (a way back at the last chorus line): living builds rise in eight songs of eight ({live('way_back')}; songs 55, 54, 58, 49, 60, 59, 61, 62), the words' fit holds, but the peak is planted in 80 to 91 builds of 100 in four songs where 95 were asked. 749.188: the way back fired in 2 to 16 builds of a thousand, being in the wrong line. Not built. 749.184: the two nits mended.")
after_par("27.129", [
    (" Luthier v49 builds nothing into the engine (Window 206; Table HP; studies/the_draw). The cause of the leaps past an octave is fix 950's planted peak: the carrying chorus line has its top raised and its centre left, and its copies carry the leap again. Two trial forms are in the code behind LUTHIER_PEAK_CLIMB (1: the carrying line holds no such leap; 2: with a way back at the last fresh chorus line), marked as not built. The next form: the way back in the carrying line itself (of its 60 draws, a climbing one if there is one, else the first that reached the peak), its marks written first, the first of them that the peak is planted as often as in v47. LUTHIER_LOOP now names a form or is off (749.184).", "27.130"),
])
P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 206: THE DRAW", H1)
W("Window 205 ended on two faults that seemed to lie in the draw: it leaps past an octave more than kept songs, and it holds weak title words long. Review 33 asked for each to be read before anything was changed, the rule for each reading written first and the fit held still (749.179). One reading found its cause. The other found there was no fault. A mend for the first was tried in two forms and is not built.")
W("749.186 The planted peak makes the leaps", H2)
W(f"Each v47 record's fitted spec, a thousand builds, the octave gate off. In songs 55, 54, 58 and 49 the builds holding a leap past an octave inside a line are {l3([pc(A(s, 'as it is', 'builds_with_a_leap')) for s in S4])} in 100, against 17.5 kept songs in 100; by notes, {l3([A(s, 'as it is', 'per_1000_notes') for s in S4])} such leaps in a thousand against the kept {K['A']['per_1000_notes']}. They are in choruses ({l3([round(100 * BD[s]['A']['as it is']['by_part'].get('Chorus', 0) / BD[s]['A']['as it is']['leaps']) for s in S4])} of 100; kept 44), and the far note is the tune's top in a chorus in {l3([A(s, 'as it is', 'far_note_is_the_builds_top_in_a_chorus') for s in S4])} of them (in kept songs the far note is the song's top one time in five). The rule had two parts and both hold in three songs of three: half or more of the leaps at the planted top; and with the plant taken out of the spec, the builds holding a leap at or under the kept share ({l3([pc(A(s, 'the plant taken out', 'builds_with_a_leap')) for s in S4])} in 100).")
W("Fix 950 gives one chorus line the song's peak by raising that line's top while its centre stays where it was. The line reaches the peak by leaping, and every later chorus copies the line. So a build that has such a leap has a dozen, where a kept song that has one has under three; and one leap allowed (Window 205) gave nothing back. The leaps are not mostly out and back: 17 to 24 in 100 are answered within two notes, as in kept songs (19). The plant cannot simply go: without it the builds' middle range is 13 or 14 semitones.")
W("749.187 The weak word held long in a title line is no fault of the draw", H2)
W(f"The spec as it is. Title lines whose longest note is a weak syllable with another word after it: {l3([BD[s]['B']['cases_in_100_title_lines'] for s in S4])} in 100 (songs 55, 54, 58, 49), against {K['B']['cases_in_100_title_lines']} in kept songs. The cases are what the kept cases are: a one-syllable function word ({K['B']['function_word']} of the kept cases) before the line's widest gap ({K['B']['before_the_widest_gap']}), a stressed note within a sixteenth of it beside it ({K['B']['longest_stressed_shorter_by_3']}). No source is at most half as common among the kept cases, so by the rule none is named. Window 205 said a quarter of song 49's builds held such a line and read that as a fault. It was the arithmetic of a gate: a build has five title lines and is passed over if any one fails. By line the draw is at the kept rate. 749.177 closes with no gate and no change.")
W("The mend, first form", H2)
W("The carrying line is drawn, 60 times at most, until its highest stressed note is the peak and it holds no leap past an octave. The marks were written first. On songs 55, 54 and 58 living builds rise (223, 256, 294 to 269, 268, 375), the peak is planted in 85 to 91 builds of 100 of v47's, every chosen tune is at or over its floor and wider than v47's (19, 19, 19), the words' fit holds, the three songs stay sound, and a random pool pick fails the rule 2.9 times in 100 against 6.5. One mark asked that the gate pass over at most half what it did: 33 and 26 do; in song 58, 56 where 55.5 was the line. A second test on songs 49, 60 and the hold-out, song 59, with the same marks written before the runs: living builds rise again (287, 178, 207 to 316, 242, 301); song 49 misses the same mark by one build (36 against 35), and in the hold-out the peak is planted in 75 builds of 100 where 80 were allowed. Twice failed by the rule, and the ruling was the writer's: hold it.")
W("The mend, second form, and 749.188", H2)
W(f"Where the song's last fresh chorus line could not climb but had reached the peak with a leap, the peak was planted there the old way. Fresh marks, written first, the halving left out as a line drawn at a round number: living builds above v47's; the peak planted in 95 builds of 100 of v47's; the words' fit within 0.02; on eight songs, 61 and 62 among them, which no form had touched. Living builds rise in all eight ({live('way_back')}). The words' fit holds in all eight. The peak is planted in {l3([round(100 * WE[s]['way_back']['planted'] / WE[s]['v47']['planted']) for s in S8])} builds of 100: four songs short. Not built. The clean reading says why: on v47's fitted specs the way back fired in {l3([CH[f'lyric{s}']['way back, gate on']['the_old_way'] for s in ('55', '54', '58')])} builds of a thousand. A line that cannot climb is nearly always an early one, and by the last line the peak is out of reach either way. The way back belongs in the carrying line itself. That is a third form; it was not in the prediction and is not tried in this window.")
W("Table HP — the two forms, the whole engine, a thousand builds a song.")
rows = [("", *[f"Song {s}" for s in S8])]
rows.append(("Living builds, v47", *[str(WE[s]["v47"]["live"]) for s in S8]))
rows.append(("first form", *[str(WE[s]["climb"]["live"]) if WE[s]["climb"] else "" for s in S8]))
rows.append(("second form", *[str(WE[s]["way_back"]["live"]) for s in S8]))
rows.append(("The gate passes over, v47", *[str(WE[s]["v47"]["oct"]) for s in S8]))
rows.append(("first form", *[str(WE[s]["climb"]["oct"]) if WE[s]["climb"] else "" for s in S8]))
rows.append(("second form", *[str(WE[s]["way_back"]["oct"]) for s in S8]))
rows.append(("The peak planted, of v47's in 100: first form", *[str(round(100 * WE[s]["climb"]["planted"] / WE[s]["v47"]["planted"])) if WE[s]["climb"] else "" for s in S8]))
rows.append(("second form", *[str(round(100 * WE[s]["way_back"]["planted"] / WE[s]["v47"]["planted"])) for s in S8]))
rows.append(("Chosen tune's range: v47; first; second", *[f"{WE[s]['v47']['range']}; {WE[s]['climb']['range'] if WE[s]['climb'] else ''}; {WE[s]['way_back']['range']}" for s in S8]))
table_before(anchor, [tuple(r) for r in rows])
W("")
W("749.184. LUTHIER_LOOP now turns a trial form on only when it names one; the comment on the title form says what its code does. In making the first of these I commented out a line and for part of an afternoon no song could be written from the branch; the trial runs that died told me, and song 54 is byte for byte v47's again.")
W("What this window could not do. The mend is not built, and rhythm scaling still leans low. What is known now that was not: where the leaps come from; that asking the carrying line to climb gives more living builds in every song tried; and that the mark to meet is the peak planted as often as before. 749.171 and the rest of the list are not begun.")
W("")
for lead in ("WINDOW 206", "27.130", "Table HP", "749.186 The planted"):
    assert any(p_.text.strip().startswith(lead) or lead in p_.text[:40] for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v49.docx"); print("saved Luthier_v49.docx")
