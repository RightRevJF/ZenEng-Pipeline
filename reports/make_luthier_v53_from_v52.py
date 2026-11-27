import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v52.docx")
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










RT = "/home/claude/rightrevjf/zeneng-pipeline/"; J = lambda p: json.load(open(RT + p)); B = "studies/returning_clash/"
RD = J(B + "read.json"); CA = J(B + "clean_a.json"); CA.update(J(B + "clean_b.json")); C2 = J(B + "clean2b_a.json"); C2.update(J(B + "clean2b_b.json")); PB = J(B + "whole_builds_pair.json"); PR = J(B + "pair_records.json"); S64 = J(B + "song64.json"); V53 = J(B + "v53_records.json"); NB = J("studies/soundness/neighbour_v53.json")
S6 = ("55", "54", "58", "49", "50", "59"); ly = lambda s: "lyric" + s; l3 = lambda v: ", ".join(str(x) for x in v)
rp = [x["rule_fails_share"] for k, x in NB["a_random_pick_from"].items() if k.startswith("the engine's pool")][0]; nc = NB["neighbour"]["rule_fails_share"]
sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v52")], "Luthier v52", "Luthier v53")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 52"))], "LUTHIER — VERSION 52", "LUTHIER — VERSION 53")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("209 Windows", "210 Windows"), ("Windows 1–209", "Windows 1–210"), ("209 scientific research windows", "210 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v224 (Luthier v53)")
set_cell(row.cells[1], f"FIXES 966 AND 967: THE CLASHES NO RULE SAW. The first change to the engine's notes since v50. A clash is a sung note a beat long or more, off its chord and a semitone from a chord tone, other than the blue notes fix 846 allows. Reading where the returning lines' clashes come from (749.212) found two causes and no single one: a copied line is its source's notes as they stand, blind to a changed chord (72 in 100 of song 55's); and a melisma's second note (848), the scale step below, is added after the tune is chosen with no look at the chord, and is the larger half of all the engine's clashes in five songs of six. Fix 966: the clash rule of 833 applied to a copied line's long notes where the chord differs from the source's. Fix 967: when the chosen tune is written out, a second note that would be a long clash takes the step above, or the syllable keeps one note; no melisma moves and the engine chooses its tune reading the melismas as before. A first form of 967 that shut clashing syllables out of the draw moved other melismas and so the chosen tune, and missed soundness; it is kept for studies. On the seen songs together: all clashes {l3([PB[ly(s)]['v52']['clashes_per_100'] for s in S6])} per 100 notes become {l3([PB[ly(s)]['the pair']['clashes_per_100'] for s in S6])}. Sealed song 64, nine marks written first, run once: all hold; clashes {S64['v52']['builds']['clashes_per_100']} to {S64['pair']['builds']['clashes_per_100']}. Song 64 has no copied line over a changed chord, so it tested 967 and gave 966 nothing to do; 966 stands on the seen songs, the standing hold-out song 59 among them. Song 64 is spent. Every 4/4 engine record is run again; the writer's delivered editions are not remade.")
after_par("27.133", [
    (" Fixes 966 and 967 (Window 210; Table HV; studies/returning_clash). 966, metre_engine.build(), a copied line (how copy): a note that is the last of its line or a beat or more from the next onset, where the chord under it differs from the chord under the same place of its source, and it is off the chord and a semitone from a chord tone and not a blue note (846), is moved to the nearest chord tone within four semitones, in the scale and inside the line's register; left where there is none. spec.copy_clash (4/4; COPY_CLASH; LUTHIER_COPY_CLASH=0 for studies). 967, song_from_lyric.melisma_notes() as called by melismas() when the chosen tune is written out: a melisma's second note that would be a beat long or more, off its chord and a semitone from a chord tone takes the scale step above where that is clear of the chord, the run cap and the range; where it is not, the syllable keeps its one note. The draw of melismas and the engine's own reading of each build as sung (the words' gate) are unchanged, so the chosen build is the one v52 would choose from the same builds. spec.melisma_clear = \"after\" (4/4; MELISMA_CLEAR; LUTHIER_MELISMA_CLEAR=0 for studies, =1 the form of 749.224 that failed). HOLD-OUTS: song 59 for everything; songs 50, 63, 64 and 66 are spent and are seen songs; song 65 banked, not run; song 67 banked, to be made for the writer and not tested on.", "27.134")
])
P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 210: THE CLASHES NO RULE SAW", H1)
W("Window 208 noticed, on its way to something else, that song 55's returning lines carried more than one clash in every hundred notes. This window asked where they came from, found two places the engine's clash rule had never looked, mended each, and found that the second was most of the engine's clashes everywhere.")
W("749.212 Two causes, and a rule of the wrong shape", H2)
r55 = RD["55"]["shares"]; ro = RD["the other five together"]
W(f"The rule written first asked for one cause holding half of the returning lines' clashes in song 55 and half in the other five songs together. Song 55: a copied line over another chord {r55['A a copied line over another chord']}, the same chord as the source's {r55[chr(68) + ' the same chord as the source' + chr(39) + 's']}. The other five: {ro['A a copied line over another chord']} and {ro[chr(68) + ' the same chord as the source' + chr(39) + 's']}. Neither is named, and that is recorded; the rule was the wrong shape for a fault with two causes. Where again() applies the clash rule to a line sung again it never fails to find a chord tone. A copied line is not looked at. And the clashes that sit under the same chord as their source's, which the draw forbids on a long note, turned out to be on a melisma's second note: {ro['as sung: a melisma' + chr(39) + 's second note, long only as sung']} of the other five songs' returning-line clashes, all of song 50's. That note is added after the tune is chosen, the scale step below the first, and nothing checks it against the chord; every return of the line carries it.")
W("749.223 The copy (fix 966)", H2)
W(f"The clash rule of 833, as again() has it, on a copied line's long notes where the chord differs from the source's. Alone, on each v52 record's fitted spec: clashes in a copied line over another chord {l3([CA[ly(s)]['v52']['copy_over_another_chord_per_100'] for s in S6])} per 100 notes become {l3([CA[ly(s)]['form 1']['copy_over_another_chord_per_100'] for s in S6])}; the cost in bars on a figure already sung is 0.012, 0.009 and 0.013 in songs 55, 54 and 58 and nothing elsewhere; living builds within three of v52's. Through the whole engine: sound, pools 33, 22, 20, a pool pick failing the rule 1.5 times in 100.")
W("749.224 and 749.225 The melisma's second note (fix 967)", H2)
W(f"The first form shut a syllable out of the draw of melismas where both the step below and the step above would clash. It cleared the clashes ({l3([CA[ly(s)]['v52']['melisma_second_per_100'] for s in S6])} per 100 notes to none) and met every clean mark. Through the whole engine it missed one: with other melismas moved, the words' gate read song 55 differently, another build was chosen, and its rhythm scaling sat on the kept 10th where two of the three songs of the rule already sat under it; by the rule, not sound. The second form leaves the draw and the engine's reading alone and acts only when the chosen tune is written out: the second note takes the step above, or the syllable keeps one note. Its written records have v52's chord plan, pick, pool, living builds and first note on every syllable; in the six chosen tunes nine second notes are raised and one melisma is dropped; the three are sound; melismas in 100 syllables fall by 0.04 of a point at most ({l3([C2[ly(s)]['v52']['melismas_in_100_syllables'] for s in S6])} to {l3([C2[ly(s)]['form 2b']['melismas_in_100_syllables'] for s in S6])}).")
W("The two together, and the sealed song", H2)
W(f"On the seen songs together every mark is met: all clashes {l3([PB[ly(s)]['v52']['clashes_per_100'] for s in S6])} per 100 notes become {l3([PB[ly(s)]['the pair']['clashes_per_100'] for s in S6])} (song 49's remainder is in lines sung again and fresh lines); the record's own count of long clashes in the chosen tune, {l3([PR[s]['long_clash_count'][0] for s in S6])}, becomes {l3([PR[s]['long_clash_count'][1] for s in S6])}. Song 64, never run, nine marks agreed on the thread and committed with the ledger row first. Pool {S64['v52']['record']['pool']} and {S64['pair']['record']['pool']}; living builds {S64['v52']['record']['living']} and {S64['pair']['record']['living']}; clashes {S64['v52']['builds']['clashes_per_100']} and {S64['pair']['builds']['clashes_per_100']} per 100 notes; words' fit, the figure share, pitch scaling and surprise unchanged to the second decimal; melismas {S64['v52']['builds']['melismas_in_100_syllables']} and {S64['pair']['builds']['melismas_in_100_syllables']} in 100 syllables. All nine hold.")
W("What the sealed song did not test. Song 64's plan gives every copied line the chords of its source. It has no copy clash under v52, and fix 966 moved no note in it: the two records share their chord plan and their chosen build and differ by one second note. So song 64 is a test of fix 967 and not of fix 966, whose marks held there because it had nothing to do. Fix 966 rests on the six seen songs, clean and whole, alone and with 967, song 59 among them, which is read and never fitted to. That is less than a sealed song, and it is said here so that nobody reads Table HV as more.")
W("Table HV — fixes 966 and 967: clashes per 100 notes on each record's fitted spec (v52; both fixes), and the records run again.")
rows = [("", *[f"Song {s}" for s in S6])]
rows.append(("All clashes", *[f"{PB[ly(s)]['v52']['clashes_per_100']:g}; {PB[ly(s)]['the pair']['clashes_per_100']:g}" for s in S6]))
rows.append(("In a copied line over another chord", *[f"{PB[ly(s)]['v52']['copy_over_another_chord_per_100']:g}; {PB[ly(s)]['the pair']['copy_over_another_chord_per_100']:g}" for s in S6]))
rows.append(("On a melisma's second note", *[f"{PB[ly(s)]['v52']['melisma_second_per_100']:g}; {PB[ly(s)]['the pair']['melisma_second_per_100']:g}" for s in S6]))
rows.append(("Living builds, the records", *[f"{V53[s]['living'][0]}; {V53[s]['living'][1]}" for s in S6]))
rows.append(("The pool", *[f"{V53[s]['pool'][0]}; {V53[s]['pool'][1]}" for s in S6]))
rows.append(("Builds' middle words' fit", *[f"{V53[s]['fit'][0]:g}; {V53[s]['fit'][1]:g}" for s in S6]))
rows.append(("Chosen tune's range (floor)", *[f"{V53[s]['range']} ({V53[s]['floor']:g})" for s in S6]))
table_before(anchor, [tuple(r) for r in rows])
W("")
W(f"The records. Songs 55, 54, 58, 49, 50, 59 and 61 are run again; song 60's is songs/p70/lyric60.v53.song.json, its delivered record untouched; song 66, made for the writer on v52, is not remade. Songs 54 and 50 keep v52's chosen build and change only in second notes raised (1 and 6). Song 52 (6/8) is byte for byte as it was: the fixes are set for 4/4. The three songs of the rule are sound with the one lean; the neighbour choice fails the rule {round(100 * nc, 1)} times in 100 and a random pool pick {round(100 * rp, 1)}; pools 33, 22, 20. The hold-out, song 59: living builds 320 to 323, pool 21, its chosen tune 19 over a floor of 15.46. Every chosen tune's own count of long clashes is nil. Every room file is read again and both checks pass.")
W("What this window could not do. Song 49 keeps 0.22 clashes per 100 notes in lines sung again and fresh lines, and the blue-note songs still sing about a fourteenth of the blue notes kept songs do (749.211). Fix 966 has not met a sealed song that has its fault. Song 58's living builds fall from 366 to 314 with 966, inside no mark of the whole engine's but worth watching. Rhythm scaling still leans low, and it was that lean, not the melismas, that the first form of 967 tripped on. Next by the list: 749.171, then 749.219 to 749.222 from song 66.")
W("")
for lead in ("WINDOW 210", "27.134", "Table HV", "749.223 The copy"):
    assert any(p_.text.strip().startswith(lead) or lead in p_.text[:40] for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v53.docx"); print("saved Luthier_v53.docx")
