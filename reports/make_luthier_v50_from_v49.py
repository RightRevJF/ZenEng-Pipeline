import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v49.docx")
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
RD = J("studies/the_peak_line/reading.json"); WE = J("studies/the_peak_line/whole_engine.json"); TH = J("studies/the_peak_line/tail_held.json"); TT = J("studies/the_peak_line/tail_tries_held.json"); S50 = J("studies/the_peak_line/song50_held.json")["lyric50"]; LH = J("studies/the_draw/line_held.json"); OT = J("tables/kept_octave_tail.json"); N5 = J("studies/soundness/neighbour_v50.json")
l3 = lambda v: ", ".join(str(x) for x in v); pc = lambda x: round(100 * x, 1); S8 = ("55", "54", "58", "49", "60", "59", "61", "62"); S6 = ("55", "54", "58", "49", "59", "60"); S4 = ("55", "54", "58", "49")
rp = [x["rule_fails_share"] for k, x in N5["a_random_pick_from"].items() if k.startswith("the engine's pool")][0]; nc = N5["neighbour"]["rule_fails_share"]
sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v49")], "Luthier v49", "Luthier v50")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 49"))], "LUTHIER — VERSION 49", "LUTHIER — VERSION 50")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("206 Windows", "207 Windows"), ("Windows 1–206", "Windows 1–207"), ("206 scientific research windows", "207 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v221 (Luthier v50)")
lv = l3([f"{WE[s]['v47']['live']} to {WE[s]['shared']['live']}" for s in S8]); pa = lambda k: RD[k]["approach"].get("past an octave", 0)
set_cell(row.cells[1], f"FIX 964: THE OCTAVE BIN SHARED AS KEPT SONGS SHARE IT. The first change to the engine's notes since v47. After two forms of a mend for the leaps past an octave had failed (Window 206), a third (the way back in the carrying line itself) failed too: 749.189, the peak and the leaps trade one for one, since about one planted build in six reaches its peak only by leaping. The session's 749.191, a reading of where the top-carrying line sits, rule first: its centre is not the fault (the builds' reach and lift are the kept songs'); the difference is the approach, the top reached from past an octave in {l3([pc(pa('lyric' + s)) for s in S4])} lines of 100 against the kept {pc(pa('kept'))}. 749.192, read in the code: the kept interval table holds every interval of an octave or more in its +12 and -12 bins, and the draw gave the whole bin to each pitch past an octave, so such leaps were offered at several times their kept odds. Kept songs divide the bins {OT['up']['octave']} octaves to {OT['up']['past']} past it upward and {OT['down']['octave']} to {OT['down']['past']} downward. FIX 964 shares the bin so. On the eight 4/4 songs, marks first: living builds rise in all eight ({lv}); the words' fit holds; every chosen tune is at or over its floor; with no gate the builds holding such a leap fall to {l3([pc(TH['lyric' + s]['shared, gate off']['builds_with_a_leap']) for s in S6])} in 100 (kept 17.5); but the peak is planted in 74 to 92 builds of 100 of v47's, where I had asked 95, and it was not built. With the plant given 240 draws the peak is planted more often than in v47 and the leaps return (749.193: drawing until the peak arrives selects for the leap; v47's count was itself made by the fault). The writer ruled that a sealed song decide, by marks written before it was run with the range in place of the count: song 50, run once. All four hold (living builds 154 to 243; words' fit 0.248 and 0.248; the chosen tune 17 over a floor of 14.55; builds holding a leap {pc(S50['shared, gate off']['builds_with_a_leap'])} in 100). Built. Songs 55, 54, 58, 59, 49, 61 run again; sound, one lean (rhythm scaling, low); pools 25, 22, 24; a random pool pick fails the rule {pc(rp)} times in 100 (v47 6.5). The octave gate stays on; whether it is still wanted is put to the session.")
after_par("27.130", [
    (f" Fix 964 (Window 207; Table HQ; studies/the_peak_line). The kept interval table's +12 and -12 bins count every interval of an octave or more. pitches1() gave each candidate pitch the weight of its bin, so every pitch past an octave took the whole bin. From v50, where spec.octave_tail is set (4/4; OCTAVE_TAIL), the bin is shared: the octave takes its kept share (tables/kept_octave_tail.json, made by lib/luthier/make_kept_octave_tail.py: {OT['up']['octave_share']} upward, {OT['down']['octave_share']} downward) and the pitches past it that are in reach share the rest equally. The plant (950) and the octave gate (959) are unchanged. LUTHIER_OCTAVE_TAIL=0 is for studies. The forms of 749.182 and 749.189 (LUTHIER_PEAK_CLIMB) and LUTHIER_PEAK_TRIES are trial switches, off. HOLD-OUTS: song 59 for everything; song 50 is spent and is a seen song; songs 63 and 64 banked, not run.", "27.131"),
])
P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 207: THE OCTAVE BIN", H1)
W("Window 206 found that the planted peak makes the leaps past an octave and tried two forms of a mend, each a rule for choosing among the carrying line's draws. Both failed. This window tried a third such form, which failed and showed why none could pass; read where the kept songs' highest lines sit, which cleared the line's centre; and then found the fault in the draw itself, older than the plant. Its mend failed one mark on the seen songs, a mark I came to think was wrong, and was put to a sealed song under a rule written before the song was run. It passed and is built.")
W("749.189 The peak and the leaps trade one for one", H2)
W(f"The third form kept, of the carrying line's 60 draws, a climbing one if any climbed, else the first that reached the peak. The peak was then planted as often as in v47 (96 to 104 in 100 on the fitted specs), and the leaps were back: builds holding one, with no gate, {l3([pc(LH['lyric' + s]['in the line, gate off']['builds_with_a_leap']) for s in S6])} in 100 against the kept 17.5. Three forms, one trade. About one planted build in six reaches its peak only by a leap past an octave, and those builds live at a high rate. Refuse them and the peak is planted a sixth less often; allow them and the leaps return. I took this to mean the carrying line's centre sat too far under its top.")
W("The carrying line's centre is not the fault (the session's 749.191)", H2)
W(f"The rule was written first: the centre would be named only if the builds' reach (the top less the line's middle pitch) was over the kept 75th and their lift (the line's middle over its part's) two semitones under the kept one, in three songs of four. Kept songs' top-carrying lines: reach {l3(RD['kept']['reach_quartiles'])} at the quartiles, lift {l3(RD['kept']['lift_quartiles'])}. The builds': reach {'; '.join(l3(RD['lyric' + s]['reach_quartiles']) for s in S4)}; lift {'; '.join(l3(RD['lyric' + s]['lift_quartiles']) for s in S4)}. The rule holds in one song. The lines that carry the planted peak sit about where kept songs' do. What differs is the last step: kept songs begin the line on its top {pc(RD['kept']['approach'].get('first note', 0))} times in 100 or step to it {pc(RD['kept']['approach'].get('step', 0))}, and come to it from past an octave {pc(pa('kept'))}; the builds come from past an octave {l3([pc(pa('lyric' + s)) for s in S4])} times in 100. The session had reserved a new sealed song, song 64, for a form that raised the centre. That form is not tried and song 64 stays sealed.")
W("749.192 Every pitch past an octave was given the whole bin", H2)
W(f"How does the draw come to offer such a leap? The kept interval table is made with every interval clamped to an octave (make_kept_4_4_tables.py), so its +12 bin counts the octave and everything past it together, and its -12 bin likewise. The draw clamps the same way when it looks a candidate's interval up (ivp). So the ninth, the tenth, the eleventh and the twelfth each take the weight kept songs give to all intervals of an octave or more together. A part's register spans about 19 semitones, so four or five such pitches are usually in reach, and the draw is offered a leap past an octave at several times its kept odds. A line's pull to its own centre hides most of this. The plant takes that pull away for one line by raising its top, and the leaps show. This is not a figure that needs a rule to name it. It is what the code does, and it is older than the plant: it is why the octave gate was needed (749.160), why the plant brought the leaps (749.186) and why no choice among draws could mend them (749.189).")
W(f"In the kept songs the bins divide: upward, {OT['up']['octave']} octaves and {OT['up']['past']} intervals past it; downward, {OT['down']['octave']} and {OT['down']['past']} (tables/kept_octave_tail.json). The mend shares the bin so: the octave takes its kept share, and the pitches past it that are in reach share the rest equally. No gate, no redraw, the plant as it was.")
W("The seen songs: five marks of six", H2)
W(f"The marks were the session's for the third form, with one of mine. On the eight 4/4 songs, the whole engine: living builds rise in every one ({lv}); the builds' middle words' fit stays within 0.02; every chosen tune is at or over its floor. Songs 55, 54 and 58 stay sound with the one lean, and a random pool pick fails the rule 3.2 times in 100 against 6.5. On v47's fitted specs with only the form changed and no gate, the builds holding a leap past an octave are {l3([pc(TH['lyric' + s]['shared, gate off']['builds_with_a_leap']) for s in S6])} in 100 (v47: {l3([pc(TH['lyric' + s]['v47, gate off']['builds_with_a_leap']) for s in S6])}; kept 17.5), and by notes {l3([TH['lyric' + s]['shared, gate off']['leaps_per_1000_notes'] for s in S6])} in a thousand (kept 1.5). The sixth mark asked that the peak be planted in 95 builds of 100 of v47's. It is planted in {l3([round(100 * TH['lyric' + s]['shared, gate off']['planted'] / TH['lyric' + s]['v47, gate off']['planted']) for s in S6])}. By the rule, not built; the writer ruled to hold it and try the plant with more draws.")
W("749.193 Drawing until the peak arrives selects for the leap", H2)
W(f"With the bin shared and the plant given 240 draws where it had 60 (a number set before any run, and not searched), the peak is planted in {l3([round(100 * TT['lyric' + s]['shared, gate off']['planted'] / TT['lyric' + s]['v47, gate off']['planted']) for s in S6])} builds for v47's 100, and the builds holding a leap rise to {l3([pc(TT['lyric' + s]['shared, gate off']['builds_with_a_leap']) for s in S6])} in 100: over the kept share in three songs. The plant draws a line again until it happens to touch a top set far above it, and the likeliest way to touch a far top is to leap. Every draw more is a chance more for the leap. So the number of draws is the size of a side effect, and at 60 with the odds right the side effect is about what kept songs show. And v47's count of planted peaks, which my sixth mark had taken as the standard, was itself made by the fault: the plant reached its top so often because the leap was offered so freely. A mark that can be met only by restoring the fault does not measure the mend.")
W("The sealed song", H2)
W(f"A mark cannot be struck after the fact. What could be done was to write the mark I would now set, before a song that had met none of this was run, and let that song bind. The writer ruled to spend song 50 on it. The form was frozen as the seen songs had tested it. The marks, committed with the ledger line before the song was run by anything: living builds above v47's; the builds' middle words' fit within 0.02; the range kept (the chosen tune at or over its floor, and the builds' middle range no more than a semitone under v47's); and with no gate, on the fitted spec, builds holding a leap at or under 17.5 in 100. Song 50, a thousand builds each way: living builds 154 and 243; words' fit 0.248 and 0.248; the chosen tune's range 17 over a floor of 14.55, the builds' middle range {S50['shared, gate on']['median_range']} against {S50['v47, gate on']['median_range']}; builds holding a leap {pc(S50['shared, gate off']['builds_with_a_leap'])} in 100, where v47's were {pc(S50['v47, gate off']['builds_with_a_leap'])}. All four hold. Fix 964 is built, on by default.")
W("Reported of song 50 and deciding nothing: its peak is planted in 84 builds of 100 of v47's, as on the seen songs; its pool is small with or without the form (4 builds and 5), and its chosen tune under the form fits its words at 0.209 where v47's fitted at 0.399, the builds behind the two being the same to three places. A chosen tune is one draw (749.175), but this is the one the writer would hear, and song 50's thin pool is a thing to look at for its own sake. Song 50 is spent and is a seen song from here.")
for n_, title_, test_ in (
    ("749.194", "With the odds right, is the octave gate still wanted?", "For the session and the writer: with fix 964 and no gate, 6 to 15 builds in 100 hold a leap past an octave, under the kept songs' 17.5, and such leaps run 0.7 to 2.3 in a thousand notes against the kept 1.5. The gate (959) now passes over 18 to 54 builds in a thousand. It was asked for by ear, after song 62. It stays on until ruled otherwise."),):
    W(f"{n_} {title_}", H2); W(test_)
W("Table HQ — fix 964: the whole engine, a thousand builds a song (v47; v50).")
rows = [("", *[f"Song {s}" for s in S8])]
for lab, c in (("Living builds", "live"), ("The octave gate passes over", "oct"), ("Builds' middle words' fit", "builds_fit"), ("The peak planted, builds", "planted"), ("Chosen tune's range", "range")):
    rows.append((lab, *[f"{WE[s]['v47'][c]:g}; {WE[s]['shared'][c]:g}" for s in S8]))
rows.append(("Chosen tune's floor", *[f"{WE[s]['shared']['floor']:g}" for s in S8]))
table_before(anchor, [tuple(r) for r in rows])
W("")
W(f"The records. Songs 55, 54, 58, 59, 49 and 61 are run again and their notes change; song 60's is songs/p70/lyric60.v50.song.json, its delivered record untouched; song 50 has two records, the engine as it was (lyric50.v47.song.json) and as it is. Song 52 (6/8) and song 53 (the hymn) are byte for byte as they were: the fix is set for 4/4. The three songs of the rule are sound with the one lean; the neighbour choice fails the rule {pc(nc)} times in 100 and a random pool pick {pc(rp)}; pools 25, 22, 24. The hold-out, song 59: living builds 207 to 320, its chosen tune 17 over a floor of 15.46. Every room file is read again and both checks pass.")
W("What this window could not do. Rhythm scaling still leans low. The peak is planted in fewer builds than before (74 to 92 in 100), and though no chosen tune has lost its floor, the plant itself, a line drawn again until it touches a far top, is a poor way to reach one: kept songs begin the line there or step to it. That is the next thing to read in the draw, with 749.171. A numbering note: the session's 749.191 is the centre reading; the bin is 749.192 here, and some of my earlier notes of this afternoon called it 749.191 before the session's list reached me.")
W("")
for lead in ("WINDOW 207", "27.131", "Table HQ", "749.192 Every pitch"):
    assert any(p_.text.strip().startswith(lead) or lead in p_.text[:40] for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v50.docx"); print("saved Luthier_v50.docx")
