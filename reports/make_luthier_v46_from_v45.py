import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v45.docx")
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
T4 = ("55", "54", "58", "49"); C = {(s, f): J(f"studies/busy_sections/shares_trial/cap_{f}_lyric{s}.json") for s in T4 for f in ("off", "shares", "apart")}; l3 = lambda v: ", ".join(str(x) for x in v)
col = lambda f, c: [C[(s, f)][c] for s in T4]; N6 = J("studies/soundness/neighbour_v46.json"); p1 = lambda x: round(100 * x, 1)
rp = [x["rule_fails_share"] for k, x in N6["a_random_pick_from"].items() if k.startswith("the engine's pool")][0]; nc = N6["neighbour"]["rule_fails_share"]
sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v45")], "Luthier v45", "Luthier v46")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 45"))], "LUTHIER — VERSION 45", "LUTHIER — VERSION 46")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("202 Windows", "203 Windows"), ("Windows 1–202", "Windows 1–203"), ("202 scientific research windows", "203 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v217 (Luthier v46)")
set_cell(row.cells[1], f"THE VERSE SUNG CLOSER, TURNED OFF; A GENTLER FORM TRIED AND FAILED. The songwriting session's Review 30 read song 49 as I did: the hold-out lost words' fit under 958, so 958 is off unless a lyric asks for it (749.153), and songs 55, 54 and 58 return to their tunes of Window 201. It approved the gentler form I proposed, with six checks written before any run: each verse line of 6 to 8 syllables carries the kept share of lines that long taking one bar at the song's tempo, and a verse takes the rounded sum of the shares. The trial fails. Rhythm scaling rises in all four songs ({l3(col('off', 'rhythm_scaling'))} to {l3(col('shares', 'rhythm_scaling'))}; songs 55, 54, 58, 49), but the builds' words' fit falls past the 0.02 allowed in song 54 ({C[('54','off')]['words_fit']} to {C[('54','shares')]['words_fit']}) and song 49 ({C[('49','off')]['words_fit']} to {C[('49','shares')]['words_fit']}); the chosen tunes of songs 55 and 54 fall by 0.040 and 0.076; and song 49's verse runs {C[('49','shares')]['verse_over_chorus']} times its chorus, past the guard. The cost in words' fit does not shrink with the lines taken: song 49 loses more with three lines taken than it did with four. The form stays off, no other is tried in this window, and song 50, the new hold-out, is not run and stays sealed. 749.154: read in every living build, song 49's untouched verse lines do not fall (0.137 to 0.140), and its one-bar lines fit their words better within the line (0.247 to 0.334) while the song's whole fit falls: the whole fit ranks note lengths across lines, so a line sung quickly counts against the song. Whether that is a fault of the form or of the measure is put to the kept songs in a later window.")
after_par("27.126", [
    (" The verse sung closer is off by default (Window 203; Table HM; studies/busy_sections/RESULT_shares.md). From Luthier v46 plan() gives a verse line one bar under fix 958 only where the lyric asks (\"verse_closer\": true for the form of Window 202, or a form's name). The trial form \"shares\" is in the code and is not built: it failed its checks. HOLD-OUTS: song 59 for everything; song 49 is now a seen song; song 50 (songs/p60/lyric50.json) and song 63 are banked and have not been run by the engine in any way.", "27.127"),
])
P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 203: THE VERSE SUNG CLOSER, TURNED OFF", H1)
W("Window 202 built the engine's lever on rhythm scaling and reported that the new hold-out, song 49, disagreed with it on the words. The songwriting session's Review 30 found every record to reproduce and ruled as the hold-out asked: 958 off by default, and the gentler form I had proposed to be tried under checks written before the run, with a fresh hold-out, song 50. This window does both. The trial fails.")
W("958 off by default (749.153)", H2)
W(f"A lyric may still ask for the form. With it off, songs 55, 54 and 58 take back the tunes of Window 201, note for note; songs 59 and 60 are unchanged; song 49's record is the one made without the form, and the record made with it is kept as lyric49.v45_with_958.song.json. The three chosen tunes pass the soundness rule and lean again on rhythm scaling, low. The pools stand where Window 201 left them: the neighbour choice fails the rule {p1(nc)} times in a hundred and a random pool pick {p1(rp)}.")
W("The trial by kept shares", H2)
W(f"The form and its six checks were committed before anything was run under it, with no refinement of mine. It takes about half the lines 958 took: one a verse in songs 55 and 54, two in song 58, one and two in song 49's two verses. On a thousand builds a song, rhythm scaling rises in all four ({l3(col('off', 'rhythm_scaling'))} to {l3(col('shares', 'rhythm_scaling'))}), about half of what 958 gave. The builds' words' fit moves from {l3(col('off', 'words_fit'))} to {l3(col('shares', 'words_fit'))}: within the 0.02 allowed in songs 55 and 58, past it in song 54 and well past it in song 49. The chosen tunes of songs 55 and 54 fall from 0.341 to 0.301 and from 0.275 to 0.199. Song 49's verse stands at {C[('49','shares')]['verse_over_chorus']} times its chorus in notes a bar, past the kept 90th of 1.48; it stands at {C[('49','off')]['verse_over_chorus']} with no form at all, its verse lines being longer than its chorus's. Three checks of six fail, and a part of a fourth. I had given the trial an even chance, expecting the cost in words' fit to fall with the lines taken. It does not: song 49 loses {round(C[('49','off')]['words_fit'] - C[('49','shares')]['words_fit'], 3)} with three lines taken and lost 0.040 under 958 with four.")
W("By the rule, the form stays off and no other variant is tried in this window. Song 50 was to be run only after the trial was frozen, and its verdict was to bind only if the seen songs passed. They did not, so running it could change nothing and would spend it. It is not run. Its lyric file is made from the locked lyric word for word (folk, baritone, 88 beats a minute by its intake's last ruling; its intake asks for a swing, which the engine does not read), and nothing of the engine has touched it.")
W("Where the fall is (749.154)", H2)
W(f"The session read song 49's two chosen tunes line by line and found the larger fall in the verse lines the form had left alone, and asked that the builds be read the same way. In every living build of song 49: the verse lines given one bar fit their words better within the line under the form, 0.247 to 0.334; the other verse lines do not move, 0.137 to 0.140 (and 0.141 to 0.127 under 958); the rest of the song moves from 0.338 to 0.321. So the fall the session saw in the untouched lines was the draw of one tune. But then no group of lines falls, and the song's whole fit still falls by 0.049. The whole fit is one rank correlation over every note of the song, of each syllable's weight against its note's salience; length is a third of salience and is ranked across the whole song. A line sung in one bar has every note short, so its weighty syllables rank short against the song, though each still stands out in its own line. That is a reading of the figures and not yet a test. Song 54 agrees less cleanly: its untouched verse lines do fall under the trial form, 0.252 to 0.202.")
W("If the reading is right, the check that has now stopped two forms measures pace between lines as misfit within them, and a kept song whose verse is busier than its chorus would be marked down the same way. The kept songs can say: whether, at the same line-by-line fit, kept songs with more change of pace have a lower whole fit. That is a study for a later window, rule first. It is not a reason to pass the form now.")
for n_, title_, test_ in (
    ("749.153", "The form off by default; the trial by kept shares", "Test (the session's, frozen first): words' fit of the builds within 0.02 in songs 55, 54, 58, 49 (fails: 54, 49); of the chosen tunes in songs 55, 54, 58 (fails: 55, 54); of the verse lines left at two bars in songs 54 and 49 (fails: 54); rhythm scaling higher in three songs of four (holds in four); soundness, pools, guard, floor, ceiling, builds, range (the guard fails in song 49); song 50 (not run). Not built."),):
    W(f"{n_} {title_}", H2); W(test_)
W("Table HM — the trial by kept shares: the builds' middle with the form off; under the trial form; under 958.")
rows = [("", "Song 55", "Song 54", "Song 58", "Song 49")]
for lab, c in (("Words' fit (may fall 0.02)", "words_fit"), ("Rhythm scaling (kept quartiles 0.605, 0.656, 0.721)", "rhythm_scaling"), ("Bars with nothing sung (kept 0.12, 0.19, 0.28)", "bars_unsung"), ("Verse over chorus, notes a bar (kept 0.83 to 1.48)", "verse_over_chorus"), ("Builds that live, of 1,000", "live"), ("Range, semitones", "range")):
    rows.append((lab, *[f"{C[(s, 'off')][c]:g}; {C[(s, 'shares')][c]:g}; {C[(s, 'apart')][c]:g}" for s in T4]))
rows.append(("The chosen tune's words' fit, off; trial", "0.341; 0.301", "0.275; 0.199", "0.307; 0.339", "0.326; 0.343"))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W("The records. Songs 55, 54 and 58: the notes of Window 201. Songs 59, 60 (songs/p70/lyric60.v46.song.json), 52 and 53: unchanged. Song 49: the record without the form. Both checks pass and every room file is read again. A ledger for hold-outs is added to studies/judging_data/README.md (749.169), after the session and I each ran the fresh-songs test on the same hold-out on 22 November without knowing of the other.")
W("What this window could not do. Rhythm scaling leans low again, and the one lever found for it is off. Nothing here answers whether the words' check is right to stop it. The session's other items are not begun: the trial of sections that loop less (749.159), the flagged patches from song 62 (749.160 to 749.170), song 58's bars of rest (749.144), a short line in a long slot (749.147), and the hymn items.")
W("")
for lead in ("WINDOW 203", "27.127", "Table HM", "749.153 The form"):
    assert any(p_.text.strip().startswith(lead) or lead in p_.text[:40] for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v46.docx"); print("saved Luthier_v46.docx")
