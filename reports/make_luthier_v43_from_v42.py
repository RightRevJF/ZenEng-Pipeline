import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v42.docx")
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
N3 = J("studies/soundness/neighbour_v43.json"); N2 = J("studies/soundness/neighbour_v42.json"); NP = J("studies/soundness/neighbour_v43_without_the_peak.json"); TR = J("studies/pitch_ceiling/trial_neighbour_before_956.json"); CM = J("studies/commonest_pitch/result.json")
WT = J("tables/kept_words_to_shape.json")["range_less_the_asking_held_out"]; CT = J("tables/kept_commonest_pitch.json")["parts"]; SD = J("studies/soundness/soundness.json")
S = {k: J(p) for k, p in (("55", "songs/p65/lyric55.song.json"), ("54", "songs/p64/lyric54.song.json"), ("58", "songs/p68/lyric58.song.json"), ("59", "songs/p69/lyric59.song.json"), ("60", "songs/p70/lyric60.v43.song.json"))}
T5s = ("55", "54", "58", "60", "59"); l3 = lambda v: ", ".join(str(x) for x in v); p1 = lambda x: round(100 * x, 1); g = lambda x: f"{x:g}"; PK = "the engine's pool"
def pool(N): return dict(nc=N["neighbour"]["rule_fails_share"], rp=[x["rule_fails_share"] for k, x in N["a_random_pick_from"].items() if k.startswith(PK)][0], rg=N["ranges_90"])
P3, P2 = pool(N3), pool(N2); rg = lambda P_, k: f"{p1(P_['rg'][k][0])} to {p1(P_['rg'][k][1])}"; NC, RP = "neighbour choice", "a random pick from the engine's pool"
def find(o, k):
    if isinstance(o, dict):
        if k in o: return o[k]
        for v in o.values():
            r = find(v, k)
            if r is not None: return r
    return None
RC = {k: find(S[k], "range_choice") for k in T5s}; PC = {k: find(S[k], "pitch_ceiling") for k in T5s}; CP_ = {k: find(S[k], "pick_commonest_pitch") for k in T5s}; rng_ = lambda R_: max(n["midi"] for n in R_["melody"]["notes"]) - min(n["midi"] for n in R_["melody"]["notes"])
WF = {k: [v for kk, v in S[k]["checks"].items() if kk.startswith("the words' fit")][0] for k in T5s}; q = WT["p10_25_50_75_90"]; A7 = lambda N, w, f: p1(N["749.137"][w][f]); RF, NF = "a_random_pick_from_the_pool_fails", "neighbour_choice_fails"
T4c = TR["749.134"]; fs = ("lyric55.json", "lyric54.json", "lyric58.json"); out_half = [v["outside_middle_half"] if isinstance(v, dict) and "outside_middle_half" in v else None for v in SD.get("songs", {}).values()]
sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v42")], "Luthier v42", "Luthier v43")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 42"))], "LUTHIER — VERSION 42", "LUTHIER — VERSION 43")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("199 Windows", "200 Windows"), ("Windows 1–199", "Windows 1–200"), ("199 scientific research windows", "200 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v214 (Luthier v43)")
picks = l3([RC[k]['the_pick_range'] for k in T5s]); fits = l3([WF[k] for k in T5s])
set_cell(row.cells[1], f"A FLOOR AND A CEILING. The songwriting session's Review 27 (749.135 to 749.138, and 749.134 carried). 954 (749.135): the session judged 951 fair in kind and a judge in degree, and showed it: held out by artist, the words miss a kept song's range by sd {WT['sd']} semitones, and only {round(100 * WT['within_2'])} kept songs in a hundred fall within 2 of their own asking, where 951 held every chosen tune there. The fault had been a bias (the picks ran short), and a floor mends a bias. The chosen tune is now the first build no narrower than the asking plus the kept 25th of range less the asking ({q[1]}), with 872 above the floor; the figure is written by the table's maker. Song 54 spans 16 with its words' fit at {WF['54']} (951: 17 at 0.163). 955 (749.136): song_from_lyric.py --check compares every record's table stamps with the tables at hand. 956 (749.134): a ceiling on the commonest pitch's share, tried first against the pool standard and passed: a build whose verses or choruses put more of their notes on one pitch than nine kept songs in ten is passed over. No chosen tune is over it now; songs 55 and 58 change tunes. Chosen tunes span {picks} (songs 55, 54, 58, 60, 59), words' fits {fits}. The pools stand: neighbour choice fails the rule {p1(P3['nc'])} times in a hundred, a random pool pick {p1(P3['rp'])}. 749.137: range does not explain the sounder pools; the session's guess and mine were wrong. Every failure is rhythm scaling under the kept 10th in all three songs at once, and the planted peak changes no rhythm; whether the gates or chance thinned those builds is not separated. 749.138 (rhythm scaling in the engine) is not begun.")
after_par("27.123", [
    (f" A floor under the range; a ceiling on one pitch (Window 200; Table HJ; studies/review27_range_spread, studies/pitch_ceiling, studies/sounder_pools). THE FLOOR (954; amends 951): make_kept_words_to_shape.py reads each kept song's range less what its words ask, the asking made with the song's artist held out (five folds), and writes the quantiles ({l3(q)} at the 10th, 25th, middle, 75th, 90th). Among the builds past every gate the pick is the first, in the order built, whose range is at least the asking plus the 25th; where none is, the widest. THE CEILING (956): make_kept_commonest_pitch.py writes, for kept verses pooled and choruses pooled, the share of sung notes on the commonest pitch (a part of under 20 notes left out; a part is told by its name); the kept 90th is {CT['Verse']['ceiling']} for verses and {CT['Chorus']['ceiling']} for choruses. After the page gate, a build over either, read as sung, is passed over; where none passes the ceiling is waived and the record says so. THE STAMPS (955): song_from_lyric.py --check reads every song record's kept-table hashes against the tables at hand; a record kept under an earlier version's name is not read.", "27.124"),
])
P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 200: A FLOOR AND A CEILING", H1)
W("The songwriting session reviewed Window 199 and found every table and record to reproduce. It kept 950, 952 and 953. Of 951 it said: fair in kind, a judge in degree. It sent four items (749.135 to 749.138) and asked that the ceiling of 749.134 be tried. This window answers three of the four and the ceiling. The fourth, rhythm scaling in the engine, is not begun.")
W("The range a floor, not a band (954; 749.135)", H2)
W(f"951 took the first build within 2 semitones of the range the words ask. The session measured how well the words know a range: with a song's artist held out, the asking misses the song's range by sd {WT['sd']} semitones, and {round(100 * WT['within_2'])} kept songs in a hundred fall within 2 of their own asking. All five of Luthier's chosen tunes did. So 951 treated a loose prediction as exact, and in song 54 it paid for that with the words' fit (0.282 to 0.163), which is what a judge does. The fault it was built for was a bias: under 872 alone the chosen tunes ran short of their askings by 2.9 semitones on average, song 58 by 8.9. A floor mends a bias and asks nothing more. The session tried one and sent the result; I have built it as it proposed. A kept song's range less its asking stands at {q[1]} at the kept 25th. The chosen tune is the first build, in the order built, no narrower than the asking plus that; above the floor 872 decides. The figure is written by the table's maker from the held-out residuals and matches the session's.")
W(f"Read on a thousand builds a song, before the ceiling: songs 55, 60 and 59 keep the tune 872 alone would choose; song 54 takes a tune of 16 semitones whose words fit at 0.275; song 58 the tune of 19 that 951 chose. The three songs were sound with 11 checks outside the kept middle half, against 15 under 951. Each is as the session's trial found.")
W("The records name their tables (955; 749.136)", H2)
W("Four records of Window 199 named the words-to-shape table by a hash from before fix 952 changed it. The notes were right, for only song 60's asking had moved, but the records said they had read a table they had not. song_from_lyric.py --check now compares every record's stamped hashes with the tables at hand, as lyric_room.py --check does the room files, and both are run in every window. Records kept under an earlier version's name (song 60's v39, v41 and v42) stand as those versions made them and are not read.")
W("A ceiling on one pitch (956; 749.134)", H2)
W(f"Window 199 measured the fault and proposed a ceiling. The rule for the trial was written first (studies/pitch_ceiling): every song keeps a pool of ten; the pool standard holds; the chosen tunes are sound; no chosen tune's words' fit falls by more than 0.02 unless the old tune was over the ceiling. Outside the engine, on the same builds, the pools fall from {l3([T4c['pool_sizes'][f] for f in fs])} to {l3([T4c['pool_sizes_under_the_ceiling'][f] for f in fs])} (songs 55, 54, 58); a random pick from them fails the soundness rule {p1(T4c['rates_under_the_ceiling'][RF])} times in a hundred ({p1(T4c['rates_without'][RF])} without the ceiling) and the neighbour choice {p1(T4c['rates_under_the_ceiling'][NF])} ({p1(T4c['rates_without'][NF])}). It passed. I had expected song 58's pool to fall hardest, perhaps under ten; {round(100 * T4c['living_builds_under_the_ceiling']['lyric58.json'])} of its living builds in a hundred are under the ceiling, and its pool keeps {T4c['pool_sizes_under_the_ceiling']['lyric58.json']}.")
W(f"One thing changed in the building. The trial told a chorus by the engine's own kind, in which a tag counts as a chorus. The kept table tells a part by its name, and the engine now reads as the table does. By that reading song 55's tune stood at 0.476 in the chorus against a ceiling of {CT['Chorus']['ceiling']}, so song 55 changes tunes as well as song 58. In the engine the ceiling passes {l3([str(PC[k]['passed']) + ' of ' + str(PC[k]['read']) for k in T5s])} builds past the other gates (songs 55, 54, 58, 60, 59). The chosen tunes' commonest pitch takes {l3([CP_[k]['Verse'] for k in T5s])} of the verse's notes and {l3([CP_[k]['Chorus'] for k in T5s])} of the chorus's; none is over the kept 90th. The cost is in the words' fit of the two songs that changed: song 55, 0.341 to {WF['55']}; song 58, 0.361 to {WF['58']}. Both are near the kept middle (0.318).")
W("Why the pools grew sounder (749.137)", H2)
W(f"Window 199 left this untraced. The session guessed that the planted peak had moved range to the kept middle, and I expected the same. The rule was written first (studies/sounder_pools): if range explains it, the engine without the peak and the engine with it should read alike once range is left out of the soundness rule. They do not. A random pool pick fails the rule {A7(NP, 'with_range', RF)} times in a hundred without the peak and {A7(TR, 'with_range', RF)} with it; with range left out, {A7(NP, 'range_left_out', RF)} and {A7(TR, 'range_left_out', RF)}. Range was never what failed. In both engines every failure is one event: all three songs' builds under the kept 10th of rhythm scaling at once. The planted peak changes no rhythm; it changes which builds pass the lift gate and so which reach the pools. Either the gates now pass fewer builds of very low rhythm scaling, or it is chance: the two ranges overlap (3.7 to 11.4 in Window 198; 0.6 to 5.0 in Window 199). I have not separated the two. The gain is not a mend of rhythm scaling: nine pool builds in ten are still under the kept 25th.")
for n_, title_, test_ in (
    ("954", "The range a floor", "Test (the session's): no chosen tune under the floor; the pick is 872's wherever 872's first build clears it (songs 60 and 59; and song 55 before the ceiling); no pick's words' fit more than 0.02 under 872's pick unless 872's pick is under the floor; the soundness rule and the pool standard hold. All met."),
    ("955", "The records name their tables", "Test: the check passes on every record; with a kept table changed it fails and names the record and the table."),
    ("956", "A ceiling on the commonest pitch's share", "Test (written first): pools of at least ten; the pool standard; sound picks; the words' fit. All met in the trial; in the engine the pool standard holds and no chosen tune is over the kept 90th.")):
    W(f"{n_} {title_}", H2); W(test_)
W("Table HJ — the floor, the ceiling and the tune chosen. Song 59 is the hold-out.")
rows = [("", "Song 55", "Song 54", "Song 58", "Song 60", "Song 59 (hold-out)")]
rows.append(("Range the words ask; the floor", *[f"{g(RC[k]['asked'])}; {g(RC[k]['floor'])}" for k in T5s]))
rows.append(("Builds past the other gates; under the ceiling; of them at or over the floor", *[f"{PC[k]['read']}; {PC[k]['passed']}; {RC[k]['at_or_over_the_floor']}" for k in T5s]))
rows.append(("The chosen tune's range (Window 199)", *[f"{RC[k]['the_pick_range']} ({w})" for k, w in zip(T5s, (17, 17, 19, 19, 19))]))
rows.append(("Its words' fit (Window 199)", *[f"{WF[k]} ({w})" for k, w in zip(T5s, (0.341, 0.163, 0.361, 0.359, 0.32))]))
rows.append((f"Commonest pitch's share, verse (ceiling {CT['Verse']['ceiling']})", *[str(CP_[k]['Verse']) for k in T5s]))
rows.append((f"Commonest pitch's share, chorus (ceiling {CT['Chorus']['ceiling']})", *[str(CP_[k]['Chorus']) for k in T5s]))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W(f"The records. Songs 55, 54, 58 and 59 are written again; song 60 is read under this window as songs/p70/lyric60.v43.song.json (range {rng_(S['60'])}), its delivered record untouched. Songs 52 and 53 are byte for byte as they were. The three songs pass the soundness rule with one lean past the kept quartiles (rhythm scaling, low). The neighbour choice fails the rule {p1(P3['nc'])} times in a hundred (range {rg(P3, NC)}); a random pick from the engine's pool {p1(P3['rp'])} (range {rg(P3, RP)}); Window 199: {p1(P2['nc'])} and {p1(P2['rp'])}. The pools are smaller under the ceiling ({l3(list(N3['ranges_90']['pool_sizes'].values()))} as neighbour.py counts them). One kept table is new (kept_commonest_pitch.json) and one gains a block (kept_words_to_shape.json). Every room file is read again and names this engine.")
W("What this window could not do. Rhythm scaling is the one lean left and the largest gap, and its engine side (749.138: sections that differ in how busy they are, bars of rest planned where the lyric leaves room) is not begun; it is the next window's work, rule first. Why the pools hold fewer builds of very low rhythm scaling is not settled between the gates and chance. Song 54's builds are still no wider in the middle (15 against an asking of 18.8); the floor asks less of it. The ceiling and the floor both choose among builds; neither makes the draw itself spread its notes or climb, so the pools are smaller than they were.")
W("")
for lead in ("WINDOW 200", "27.124", "Table HJ", "956 A ceiling"):
    assert any(p_.text.strip().startswith(lead) or lead in p_.text[:40] for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v43.docx"); print("saved Luthier_v43.docx")
