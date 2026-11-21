import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v43.docx")
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










RT = "/home/claude/rightrevjf/zeneng-pipeline/"; J = lambda p: json.load(open(RT + p)); import re
N4 = J("studies/soundness/neighbour_v44.json"); NA = J("studies/soundness/neighbour_v44_trial_verse_closer_apart.json"); NM = J("studies/soundness/neighbour_v44_trial_verse_closer.json"); PB = J("studies/sounder_pools/per_build.json"); WK = J("studies/weak_top_notes/result.json")
CT = J("tables/kept_commonest_pitch.json")["parts"]; TR = {k: J(f"studies/busy_sections/trial_{k}.json") for k in ("as_built", "kept", "all", "aim", "half", "apart")}
S = {k: J(p) for k, p in (("55", "songs/p65/lyric55.song.json"), ("54", "songs/p64/lyric54.song.json"), ("58", "songs/p68/lyric58.song.json"), ("59", "songs/p69/lyric59.song.json"), ("60", "songs/p70/lyric60.v44.song.json"))}
T5s = ("55", "54", "58", "60", "59"); T3 = ("55", "54", "58"); FN = [f"lyric{k}.json" for k in T3]; l3 = lambda v: ", ".join(str(x) for x in v); p1 = lambda x: round(100 * x, 1); g = lambda x: f"{x:g}"; PK = "the engine's pool"
def pool(N): return dict(nc=N["neighbour"]["rule_fails_share"], rp=[x["rule_fails_share"] for k, x in N["a_random_pick_from"].items() if k.startswith(PK)][0], rg=N["ranges_90"])
P4, PA = pool(N4), pool(NA); rg = lambda P_, k: f"{p1(P_['rg'][k][0])} to {p1(P_['rg'][k][1])}"; NC, RP = "neighbour choice", "a random pick from the engine's pool"
def find(o, k):
    if isinstance(o, dict):
        if k in o: return o[k]
        for v in o.values():
            r = find(v, k)
            if r is not None: return r
    return None
RC = {k: find(S[k], "range_choice") for k in T5s}; CP_ = {k: find(S[k], "pick_commonest_pitch") for k in T5s}; WF = {k: [v for kk, v in S[k]["checks"].items() if kk.startswith("the words' fit")][0] for k in T5s}
X = lambda N, c: [N["749.140"][c][f] for f in FN]; low = lambda N: N["pool_share_outside_middle_half_by_check"]["rhythm scaling"]["low"]; tr = lambda f, c: [TR[f][k][c] for k in T3]
sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v43")], "Luthier v43", "Luthier v44")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 43"))], "LUTHIER — VERSION 43", "LUTHIER — VERSION 44")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("200 Windows", "201 Windows"), ("Windows 1–200", "Windows 1–201"), ("200 scientific research windows", "201 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v215 (Luthier v44)")
wk = WK["kept"]["p10_25_50_75_90"]
set_cell(row.cells[1], f"THE VERSE SUNG CLOSER, TRIED AND NOT YET BUILT. The songwriting session's Review 28 (749.139 to 749.141; 749.138 carried). 957 (749.139): a part is told by its exact name, so a pre-chorus is neither verse nor chorus; 22 kept songs' pre-choruses had been pooled with their choruses. The chorus ceiling moves from 0.474 to {CT['Chorus']['ceiling']} and each ceiling is printed with its range (verse {l3(CT['Verse']['ceiling_range_90'])}; chorus {l3(CT['Chorus']['ceiling_range_90'])}). Song 55 takes back the tune it had before the ceiling; that change had turned inside the ceiling's range. 749.140: read per build, the pools with and without the planted peak do not differ ({p1(PB['pools']['under_the_kept_10th_with'])} and {p1(PB['pools']['under_the_kept_10th_without'])} builds in a hundred under the kept 10th of rhythm scaling; as large in {round(100 * PB['pools']['shuffles_as_large'])} shuffles in a hundred). The sounder pool figure was one small pool's draw (song 55's), not the gates. 749.141: kept songs sing their top note on a weak syllable in {round(100 * wk[2])} occurrences in a hundred at the middle and all of them at the kept 90th; Luthier's chosen tunes stand at 0 to 0.46; not a fault by the rule, nothing built. 749.138: the engine's lever on rhythm scaling is found. Verse lines of 6 to 8 syllables given one bar (the shortest first, none side by side, as many as bring the verse to the kept middle of notes a bar) move the builds' rhythm scaling from {l3(X(N4, 'living_median_rhythm_scaling'))} to {l3(X(NA, 'living_median_rhythm_scaling'))} (kept quartiles 0.605 to 0.721), keep the builds, and leave the pools with no failure of the soundness rule. It misses one check written first: song 54's words' fit falls by 0.028 where 0.02 was allowed. It is not built; the switch is in the engine and off.")
after_par("27.124", [
    (f" A part told by its name; the verse sung closer, a trial (Window 201; Table HK; studies/busy_sections, studies/sounder_pools, studies/weak_top_notes). A PART BY ITS NAME (957): make_kept_commonest_pitch.kind reads a section's name word by word; a name holding 'chorus' or 'refrain' is a chorus, one holding 'verse' a verse, and any name with a word beginning 'pre' is neither. The table carries each ceiling's range (songs resampled 2,000 times). THE VERSE SUNG CLOSER (not built; LUTHIER_VERSE_CLOSER=apart, for trials): in plan(), in each verse, lines of 6 to 8 syllables that would take two bars are taken shortest first, never two side by side, an even count, as many as bring the verse's syllables a bar nearest the kept middle for verses (4.59), and given one bar; the planner's rules for breaks and turns then act on the shorter song as they always do.", "27.125"),
])
P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 201: THE VERSE SUNG CLOSER, TRIED", H1)
W("The songwriting session reviewed Window 200, found every table and record to reproduce and both checks to pass, and kept 954, 955 and 956. It confirmed the reading of a tag, found that the kept table pooled pre-choruses with choruses, asked that the sounder pools be read per build, reported a new worry (the top note on weak words), and left rhythm scaling as the main work. This window answers the three and makes the first engine trial on rhythm scaling.")
W("A pre-chorus is not a chorus (957; 749.139)", H2)
W(f"The table's reading of a part called anything whose name held the word chorus a chorus, so 22 kept songs' pre-choruses were pooled with their choruses, and Luthier's choruses never hold one. A part is now told by its exact name. The chorus ceiling moves from 0.474 to {CT['Chorus']['ceiling']}; the verse ceiling stays {CT['Verse']['ceiling']}. Each is now printed with its range: verse {l3(CT['Verse']['ceiling_range_90'])}, chorus {l3(CT['Chorus']['ceiling_range_90'])}. One pick changes: song 55's tune before the ceiling read 0.476 in the chorus, over 0.474 and under {CT['Chorus']['ceiling']}, so song 55 takes that tune back (range {RC['55']['the_pick_range']}, words' fit {WF['55']}). The change of Window 200 and the change back both turn inside the ceiling's range; a ceiling drawn from 139 songs cannot tell 0.474 from 0.479, and a tune that near it is neither clearly over nor clearly under. Songs 54, 58, 60 and 59 keep their tunes.")
W("The sounder pools were one pool's draw (749.140)", H2)
W(f"Window 200 ruled range out and could not tell the gates from chance. The session saw why: the rate I had read is the rate at which all three songs fail at once, which multiplies three shares and their noise, and the 43 and 28 in a hundred I gave were worked back from it, not read. Read per build (studies/sounder_pools, rule written first): in the three pools together {p1(PB['pools']['under_the_kept_10th_with'])} builds in a hundred stand under the kept 10th of rhythm scaling with the planted peak and {p1(PB['pools']['under_the_kept_10th_without'])} without, a gap as large in {round(100 * PB['pools']['shuffles_as_large'])} shuffles in a hundred; among all living builds {p1(PB['living']['under_the_kept_10th_with'])} and {p1(PB['living']['under_the_kept_10th_without'])}. The pools do not differ. The joint rate moved because of one pool: song 55's, of 39 builds, holds {p1(PB['pools']['by_song']['lyric55.json'][0])} in a hundred under the kept 10th with the peak and {p1(PB['pools']['by_song']['lyric55.json'][1])} without, and the three shares multiplied give 2 and 10 in a hundred. So the gain in the pool figure of Windows 199 and 200 was chance, and I should not have printed it beside the fixes as if it were theirs.")
W("The top note on weak words (749.141)", H2)
W(f"The session heard song 58's highest note held on \"the\" and counted top notes on weak syllables in every record. The rule was written first (studies/weak_top_notes): if two of the four songs stand over the kept 90th, plant only on stressed syllables. Kept songs put {round(100 * wk[2])} of a song's top-note occurrences in a hundred on a weak syllable at the middle, {round(100 * wk[3])} at the 75th, and every one of them at the 90th. Luthier's chosen tunes stand at {l3([WK['songs'][k]['share'] for k in T5s])} (songs 55, 54, 58, 60, 59). None is over the kept 75th. By the rule it is not a fault and nothing is built. I had guessed a kept 90th near 0.6; kept songs do this more freely than either of us thought. What the share does not read is how long a weak word is held at the top, and that is what the session heard; no reading of it is made here.")
W("Rhythm scaling: the engine's lever (749.138)", H2)
W(f"Rhythm scaling is the one check on which Luthier's songs lean, and Window 197 found what carries it in kept songs: slow change in how busy the singing is, and bars with nothing sung. How busy a stretch is, in notes a bar, is the lyric's syllables over the bars the engine gives them, and the engine gave nearly every line of 6 to 8 syllables two bars, verse and chorus alike. Kept verses run 4.6 notes a bar at the middle and Luthier's 3.7; the kept verse is 1.15 times as busy as its chorus. The lever is the bars a verse line is given. The rule was written before anything was run (studies/busy_sections), and the prediction with it: that the lever would be weak. It is not.")
W(f"Five forms were tried, each read first on 40 quick tunes a song. Verse lines in one bar as often as kept lines that long are (22 or 36 in a hundred): rhythm scaling {l3(tr('kept', 'rhythm_scaling'))} against {l3(tr('as_built', 'rhythm_scaling'))} as built; too little, as I expected. Every such line in one bar, read only to find the lever's reach: {l3(tr('all', 'rhythm_scaling'))}, but songs 55 and 54 all but stop building and the verse runs at twice the chorus, outside anything kept songs do. So a guard was written: the verse over the chorus must stay inside the kept 10th to 90th, 0.83 to 1.48. Then the form that follows the kept middle: as many one-bar lines, the shortest first and an even count, as bring the verse nearest 4.59 notes a bar. On a thousand builds a song it moved the builds' rhythm scaling to {l3(X(NM, 'living_median_rhythm_scaling'))}, inside the kept quartiles in all three, against my expectation; but song 58 kept {round(100 * X(NM, 'living_builds')[2] / X(N4, 'living_builds')[2])} builds in a hundred, where 70 were asked. The builds were dying where three one-bar lines stood side by side with no room to fit their syllables. The last form keeps one-bar lines apart.")
W(f"The last form, on a thousand builds a song (songs 55, 54, 58): rhythm scaling {l3(X(NA, 'living_median_rhythm_scaling'))} (as built {l3(X(N4, 'living_median_rhythm_scaling'))}; kept quartiles 0.605, 0.656, 0.721); builds that live {l3(X(NA, 'living_builds'))} (as built {l3(X(N4, 'living_builds'))}); the words' fit {l3(X(NA, 'living_median_words_fit'))} (as built {l3(X(N4, 'living_median_words_fit'))}); the verse {l3(tr('apart', 'verse_over_chorus'))} times as busy as the chorus. A random pick from its pools fails the soundness rule {p1(PA['rp'])} times in a hundred and the neighbour choice {p1(PA['nc'])} ({p1(P4['rp'])} and {p1(P4['nc'])} as built), and the three first builds lean on no check. Pool builds under the kept 25th of rhythm scaling fall from {round(100 * low(N4))} in a hundred to {round(100 * low(NA))}; the pools' spread of rhythm scaling rises from {N4['749.140']['pool_spread_over_kept_spread']} of the kept spread to {NA['749.140']['pool_spread_over_kept_spread']}. The songs are shorter ({l3(tr('apart', 'seconds'))} seconds against {l3(tr('as_built', 'seconds'))}), and in song 55 the planner's own rule then lets the eight-bar break in.")
W(f"Four of the five checks written first are met: rhythm scaling inside the kept quartiles in two songs of three; seven builds in ten kept in each; the soundness rule and the pool standard; the guard. The fifth is not: the words' fit of the builds may fall by no more than 0.02 in each song, and in song 54 it falls by {round(X(N4, 'living_median_words_fit')[1] - X(NA, 'living_median_words_fit')[1], 3)}. Song 54's verse lines run 7 to 9 syllables; eight in one bar are eighth notes end to end, with no long note for a weighty syllable. So the form is not built. The switch is in the engine and off. The words' fit check was my own addition; the session's check did not ask it, and by the session's check the form passes. Whether a fall of that size in one song's builds, still over the kept 10th and gated again when the tune is chosen, is a fair price is the session's to say; the other way on is to give one bar only to lines of seven syllables or fewer, which will move song 54 less.")
for n_, title_, test_ in (
    ("957", "A part told by its exact name", "Test: the maker rebuilds the table byte for byte; the record check passes; the paper says which pick changed (song 55's) and that it changed inside the ceiling's range."),):
    W(f"{n_} {title_}", H2); W(test_)
W("Table HK — the verse sung closer, tried on a thousand builds a song (as built; the last form). Not built.")
rows = [("", "Song 55", "Song 54", "Song 58")]
rows.append(("Rhythm scaling, the builds' middle (kept quartiles 0.605, 0.656, 0.721)", *[f"{a}; {b}" for a, b in zip(X(N4, 'living_median_rhythm_scaling'), X(NA, 'living_median_rhythm_scaling'))]))
rows.append(("Builds that live", *[f"{a}; {b}" for a, b in zip(X(N4, 'living_builds'), X(NA, 'living_builds'))]))
rows.append(("Words' fit, the builds' middle (allowed to fall 0.02)", *[f"{a}; {b}" for a, b in zip(X(N4, 'living_median_words_fit'), X(NA, 'living_median_words_fit'))]))
rows.append(("Pool, as neighbour.py counts", *[f"{a}; {b}" for a, b in zip(N4['ranges_90']['pool_sizes'].values(), NA['ranges_90']['pool_sizes'].values())]))
rows.append(("Verse over chorus, notes a bar (kept 10th to 90th 0.83 to 1.48)", *[f"-; {b}" for b in tr('apart', 'verse_over_chorus')]))
rows.append(("Bars with nothing sung, 40 quick tunes (kept quartiles 0.12, 0.19, 0.28)", *[f"{a}; {b}" for a, b in zip(tr('as_built', 'room'), tr('apart', 'room'))]))
rows.append(("Seconds", *[f"{a}; {b}" for a, b in zip(tr('as_built', 'seconds'), tr('apart', 'seconds'))]))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W(f"The records. Songs 55, 54, 58 and 59 are written again under the remade table; only song 55's notes change. Song 60 is read under this window as songs/p70/lyric60.v44.song.json. Songs 52 and 53 are byte for byte as they were. Chosen tunes: range {l3([RC[k]['the_pick_range'] for k in T5s])}, words' fit {l3([WF[k] for k in T5s])} (songs 55, 54, 58, 60, 59). The three songs pass the soundness rule with one lean past the kept quartiles (rhythm scaling, low). The neighbour choice fails the rule {p1(P4['nc'])} times in a hundred (range {rg(P4, NC)}); a random pick from the engine's pool {p1(P4['rp'])} (range {rg(P4, RP)}). Both checks pass (song_from_lyric.py --check, lyric_room.py --check), and every room file is read again.")
W("What this window could not do. Rhythm scaling is not mended in the engine as built: the lever is found, measured and one check short. Song 58 stays under the kept 25th even with it (0.592); its lyric leaves little room, as its room file says. The hold-out, song 59, has no verse line of 6 to 8 syllables, so it could not test the lever; a hold-out it can act on is wanted. The top-note reading does not hear a weak word held at the peak.")
W("")
for lead in ("WINDOW 201", "27.125", "Table HK", "957 A part"):
    assert any(p_.text.strip().startswith(lead) or lead in p_.text[:40] for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v44.docx"); print("saved Luthier_v44.docx")
