"""Luthier v29 -> v30: soundness read on the pools, not on one draw; turns of four bars; melismas that return with their lines; a song aimed at a kept song
(Window 187, Module 27.111, Table GW; fixes 918-921). Evidence: lib/luthier/stage17_results.json, studies/soundness/, REVIEW_stage16.md, songs/p68/fixlist_v30.md.
Run: python3 make_luthier_v30_from_v29.py"""
import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v29.docx")
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










R = json.load(open("/home/claude/rightrevjf/zeneng-pipeline/lib/luthier/stage17_results.json")); SG = R["songs"]; K = R["kept"]; PL = R["pools"]; V29 = R["v29"]; T3 = ("55", "54", "58"); l3 = lambda v: ", ".join(str(x) for x in v); pc = lambda x: f"{100 * x:.0f}"
passes = lambda k: f"{100 * (1 - PL[k]['fails']):.0f}"; outs = lambda k: f"{PL[k]['outside'][1]:.0f} ({PL[k]['outside'][0]:.0f} to {PL[k]['outside'][2]:.0f})"

sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v29")], "Luthier v29", "Luthier v30")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 29"))], "LUTHIER — VERSION 29", "LUTHIER — VERSION 30")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("186 Windows", "187 Windows"), ("Windows 1–186", "Windows 1–187"), ("186 scientific research windows", "187 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v201 (Luthier v30)")
set_cell(row.cells[1], f"SOUND ON THE POOLS. Window 186 called the engine sound by three thousandths, and asked the session whether that held. It did not: the pick is one draw from each song's gated pool, and a fresh draw of the same three songs would have leaned past the bound {pc(V29['fresh_draw_leans'])} times in a hundred. The rule is now read on the pools as well as on the picks: sound when the picks pass and a pick drawn at random from each song's pool passes at least ninety times in a hundred, where three kept songs pass ninety-three. By that reading version 29 passed about {pc(V29['pool_passes'])} times. Three repairs follow. A song's turns are drawn at the kept split with one of four bars at the least, because a two-bar silence seldom empties a four-bar stretch. A line that returns note for note returns with its melismas, where they had been scattered afresh on every return and broke the repetition. And each song is aimed at one kept song drawn from its title, in how it moves and how wide it ranges, not at the kept middle. The pools now pass {passes('aim')} times in a hundred and the picks pass; a random pick stands outside the kept middle half on {PL['aim']['outside'][1]:.0f} song-checks where it stood on {PL['without_aim']['outside'][1]:.0f} and three kept songs stand on about thirty.")

after_par("27.110 Sound, by a stated rule", [
    (" Sound on the pools (Window 187; Table GW; studies/soundness/; songs/p68/fixlist_v30.md). TURNS AT THE KEPT SPLIT (918; answers 749.95; amends 916): each turn is two bars 62 times in a hundred and four bars 38, whatever the song's length, and a song with a turn has one of four bars at the least; the bars in and out give way first. A RETURN KEEPS ITS MELISMAS (919; answers 749.97; amends 848, 818): a line copied note for note takes its source's melismas, syllable for syllable; a fresh line sings an earlier line of its section again 0.8 of the time, where it was 0.6. A SONG IS AIMED AT A KEPT SONG (920; answers 749.94 in part): one kept song is drawn from the title's seed; its shares of repeated notes, steps and leaps lean the song's moves and set the middle of the old charge's bounds for those readings, and half its range over the kept median's raises or lowers the song's tops. THE RULE READ ON THE POOLS (921; answers 749.96; amends 917): the engine is sound when the three picks pass the rule and a pick drawn at random from each song's gated pool passes it at least ninety times in a hundred; studies/soundness/neighbour.py reads the pools after every version.", "27.111"),
])

P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 187: SOUND ON THE POOLS", H1)
W("A pass by three thousandths (921)", H2)
W(f"Window 186 said its pass was narrow and asked the session whether a pass by three thousandths holds. The session's answer (lib/luthier/REVIEW_stage16.md) was no, and not for want of a margin. The pick is the first build in order past the gates: one draw from each song's pool. Read on the pools, rhythm scaling stood under the kept tenth in {l3([pc(x) for x in V29['share_under_10th']])} of a hundred pool builds of songs 55, 54 and 58; a fresh draw of the three would lean past the bound {pc(V29['fresh_draw_leans'])} times in a hundred, where three kept songs lean so on a given check once in a thousand. The bound itself is known only to about fourteen thousandths. So the rule was being read on luck. The session's amendment is adopted as written: the engine is sound when the three picks pass the rule and a pick drawn at random from each song's gated pool passes at least ninety times in a hundred. Three kept songs drawn at random pass ninety-three. By that reading version 29 was not sound, and this paper's claim of the window before is withdrawn.")
W("Turns of four bars, and melismas that return (918, 919)", H2)
W(f"Two things held the pools down. Fix 916 kept the turns and made them two bars in a long song; but what a kept song's rhythm scaling follows is the four-bar stretches with no sung note, and a two-bar silence seldom empties one. Each turn is now drawn at the kept split whatever the length, with one of four bars at the least. The second was repetition: with every kept rhythm on offer (912) the songs repeated their bar figures less than kept songs do. Raising the share of fresh lines that sing an earlier line again, from 0.6 to 0.8, brings the builds' bars on a figure already sung to {l3(R['builds_figure']['borrow_0_8'])} against a kept median of {R['builds_figure']['kept_median']}. But the builds were not where the repetition was being lost. Fix 848 scattered the melismas afresh over the whole song, so a chorus copied note for note came back with its melismas on other syllables, and each one changed its bar. A copy now takes its source's melismas, syllable for syllable. With these two the pools pass the rule {passes('without_aim')} times in a hundred; rhythm scaling leans past the kept tenth in {pc(PL['without_aim']['lean_tenths'].get('rhythm scaling', 0))} draws in a hundred, and no repetition check leans past the middle half in more than two.")
W("A song aimed at a kept song (920)", H2)
W(f"The session's first item was its finding of the window before: the songs sit nearer the kept middle than kept songs do, and it showed that choosing differently among the builds does not widen them, because the builds themselves are aimed at the kept medians. A random pick from the pools stood outside the kept middle half on {outs('without_aim')} song-checks across the three songs; three kept songs stand on about thirty. Its mend: aim each song at a kept song. One kept song is now drawn from the title's seed, as the lift is. Its shares of repeated notes, steps and leaps lean the weights of the song's moves, and the old charge's bounds for those three readings are set about the kept song's own figures; and the song's tops are raised or lowered by half the kept song's range over the kept median's. Song 58 drew a kept song of narrow range and many repeated notes; song 54 one that moves by step six times in ten.")
W(f"It was tried two ways. Aiming also at how much the kept song repeats, by the share of lines sung again, widened the picks to {outs('aim_with_repeats')} and lowered rhythm scaling until the three first picks leaned past the kept tenth together: the session had found that borrowing moves rhythm scaling the wrong way, and so it did. That half is not adopted. Aiming at the moves and the range alone gives {outs('aim')}, with the pools passing {passes('aim')} times in a hundred and the picks passing. The session's check asks twenty-one. It is not met: the aim moves three readings of twenty-one and one song's range, and most of what a song is here is still drawn at the kept shares.")
for n_, title_, test_ in (
    ("918", "Turns at the kept split, one of four bars", "Test: in each song's pool, rhythm scaling under the kept 10th in no more than 37 builds in a hundred (749.95's check)."),
    ("919", "A return keeps its melismas; more lines sung again", "Test: in the pools no repetition check leans past the middle half more than ten times in a hundred (749.97's check)."),
    ("920", "A song is aimed at a kept song", "Test: a random pick from the pools outside the middle half on 21 song-checks at the median, the rule still passed ninety times in a hundred (749.94's check)."),
    ("921", "The rule read on the pools", "Test: the picks pass, and a random pick from each pool passes at least ninety times in a hundred (749.96's check).")):
    W(f"{n_} {title_}", H2); W(test_)
W("Table GW — soundness read on the pools (a pick drawn at random from each song's gated pool, 4,000 times) and on the three picks.")
rows = [("", "With 918 and 919", "And the aim at moves and range (adopted)", "And the aim at repeats (tried, not adopted)")]
O3 = ("without_aim", "aim", "aim_with_repeats")
rows.append(("The pools pass the rule, times in a hundred (three kept songs: 93)", *[passes(k) for k in O3]))
rows.append(("Song-checks outside the kept middle half, median (5th to 95th); three kept songs about 30", *[outs(k) for k in O3]))
rows.append(("Rhythm scaling leans past the kept 10th, draws in a hundred", *[pc(PL[k]["lean_tenths"].get("rhythm scaling", 0)) for k in O3]))
rows.append(("Rhythm scaling leans past the kept 25th", *[pc(PL[k]["lean_quartiles"].get("rhythm scaling", 0)) for k in O3]))
rows.append(("Pitch scaling leans past the kept 75th", *[pc(PL[k]["lean_quartiles"].get("pitch scaling", 0)) for k in O3]))
rows.append(("Bars on a figure already sung leans past the kept 25th", *[pc(PL[k]["lean_quartiles"].get("bars on a figure already sung", 0)) for k in O3]))
rows.append(("The three first picks pass the rule", *[("yes" if PL[k]["first"]["sound"] else "no: " + ", ".join(PL[k]["first"]["leans_10_90"])) for k in O3]))
rows.append(("The first picks' checks outside the middle half", *[l3(PL[k]["first"]["outside_middle_half"]) for k in O3]))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W(f"The records. Songs 55, 54 and 58 are written again with all four fixes: keys {l3([SG[k]['key'] for k in T3])}; {l3([SG[k]['seconds'] for k in T3])} seconds; each with a four-bar turn. Their picks stand outside the kept middle half on {l3([SG[k]['outside_middle_half'] for k in T3])} checks of the 23 and pass the rule, with rhythm scaling (low) and pitch scaling (high) the two leans it allows.")
W(f"What this window could not do. The picks' rhythm scaling is again on the bound ({l3([SG[k]['readings']['rhythm scaling'] for k in T3])} against {round(K['rhythm scaling'][0], 3)}); it is the pools that say the engine does not lean past it, and seven draws in ten still lean under the kept lower quartile: the engine's rhythm has less order across scales than a kept song's, inside what the rule allows and no further. A random pick stands outside the kept middle half on {PL['aim']['outside'][1]:.0f} song-checks, not the twenty-one asked: the songs are still more alike the median kept song than kept songs are alike. Song 58 sings a chorus ten semitones over its verse, past the kept ninetieth, and its pitch scaling goes with it. Four-bar turns add to songs already long: {SG['54']['seconds']} and {SG['58']['seconds']} seconds. The pools are read by a study that rebuilds each song's thousand builds; the record of a song does not hold its pool. Song 52 in 6/8 is carried. And the pick is still the first build in the pool: the rule now says the pool is sound, and nothing says which build in it is the best song.")
W("")
for lead in ("WINDOW 187", "27.111 Sound on the pools", "Table GW", "921 The rule read on the pools"):
    assert any(p_.text.strip().startswith(lead) for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v30.docx"); print("saved Luthier_v30.docx")
