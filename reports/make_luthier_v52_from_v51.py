import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v51.docx")
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
D = J("studies/loop_chance/drafts.json"); LC = J("tables/loop_chance.json"); R63 = J("studies/loop_chance/lyric63.chance.song.json"); V63 = J("studies/loop_chance/lyric63.v50.song.json")
pc = lambda x: round(100 * x, 1); mv = lambda f: D[f]["repetition"]["major verse"]; s4 = lambda f, k: D[f]["stage4"]["major"][k]
sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v51")], "Luthier v51", "Luthier v52")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 51"))], "LUTHIER — VERSION 51", "LUTHIER — VERSION 52")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("208 Windows", "209 Windows"), ("Windows 1–208", "Windows 1–209"), ("208 scientific research windows", "209 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v223 (Luthier v52)")
dl = lambda k: ", ".join(f"{s4('chance', k)['written'][m] - s4('off', k)['written'][m]:+.3f}" for m in ("first", "last", "chords", "bigrams", "bars"))
set_cell(row.cells[1], f"FIX 965: THE LOOP GATE WITH A CHANCE, A SETTING. Where a lyric asks for chords that loop less, fix 960 drew a verse or bridge again until its chord repetition was at or under the kept median, which left {pc(mv('median')['written_at_or_under_the_kept_median'])} verses in 100 under a line that half of kept verses are over; a gentler form (749.178) redrew every section over the kept 75th and left none there. Any gate that redraws to a line empties the far side of the line. From v52 a section over the kept 75th is drawn again with a chance, set per kind and mode so that about a quarter stay over it. Form, rule and marks first (749.185). On a thousand drafted sections a kind, major: verses at or under the kept median {pc(mv('chance')['written_at_or_under_the_kept_median'])} in 100 (kept 50; no gate {pc(mv('off')['written_at_or_under_the_kept_median'])}), over the kept 75th {pc(mv('chance')['written_over_the_kept_75th'])} (kept 25; no gate {pc(mv('off')['written_over_the_kept_75th'])}), plain loops {pc(s4('chance', 'verse')['loops_kept_written'][1])} (kept {pc(s4('chance', 'verse')['loops_kept_written'][0])}), and every stage 4 reading within 0.02 of the unpatched writer's. All four marks met. Sealed song 63, marks and ledger row first, run once: pool 10 against a mark of 10 or more, the builds' middle words' fit {R63['judge7']['words_gate']['the_builds_median_fit']} over a floor of {R63['judge7']['words_gate']['at_least']}. Both hold, the first with nothing to spare; song 63 is spent. No lyric in the repository asks for the setting, so no record changes. It is not a default.")
after_par("27.132", [
    (f" Fix 965 (Window 209; Table HU; studies/loop_chance). chord_writer.section(): where the writer's loop_less is \"chance\" (set by song_from_lyric.py for a lyric with \"chords\": \"loop_less\"), a verse or bridge is drawn; if its chord repetition is over the kept 75th for its kind and mode, then with the chance in tables/loop_chance.json (major verse {LC['chance']['major verse']}, major bridge {LC['chance']['major bridge']}, minor verse {LC['chance']['minor verse']}, minor bridge {LC['chance']['minor bridge']}; lib/luthier/make_loop_chance.py: 1 less 0.25 over the unpatched writer's own share over the 75th, a thousand drafts, seed 749185) it is drawn again until at or under the 75th, 30 times at most, the least-looping draw where none is; otherwise it stands. The table is stamped into such a song's record. LUTHIER_LOOP=median (960's first form) and =gentle (749.178) are kept for studies; both failed their checks. Not a default. HOLD-OUTS: song 59 for everything; songs 50, 63 and 66 are spent and are seen songs; songs 64, 65 and 67 banked, not run.", "27.133")
])
P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 209: THE LOOP GATE WITH A CHANCE", H1)
W("A small window and a small fix, for a setting a lyric may ask for. It finishes a thing begun in Window 205 and tried twice.")
W("Why the first two forms failed", H2)
W(f"A verse's chord repetition is the share of its chord three-grams already heard in it. The writer with no gate sits near the kept songs: {pc(mv('off')['written_at_or_under_the_kept_median'])} major verses in 100 at or under the kept median, {pc(mv('off')['written_over_the_kept_75th'])} over the kept 75th where kept songs have 25 by definition, plain loops {pc(s4('off', 'verse')['loops_kept_written'][1])} against {pc(s4('off', 'verse')['loops_kept_written'][0])}. It is a little too loopy at the top and nowhere else. Fix 960 redrew to the kept median and left {pc(mv('median')['written_at_or_under_the_kept_median'])} in 100 under it and plain loops at {pc(s4('median', 'verse')['loops_kept_written'][1])}. The gentler form redrew only sections over the 75th, and left {pc(mv('gentle')['written_over_the_kept_75th'])} in 100 there. Both cut off a part of the range that kept songs occupy.")
W("749.185 The form", H2)
W(f"Thin the top; do not cut it off. A section over the kept 75th is drawn again with a chance, and that chance is what would leave a quarter of sections over the line: 1 less 0.25 over the unpatched writer's own share over it, measured on a seed the checks do not use (major verse {LC['share_over']['major verse']} over, chance {LC['chance']['major verse']}; major bridge {LC['share_over']['major bridge']} and {LC['chance']['major bridge']}). Judged on the kept songs' rate alone, since the two readings of which way covers lean point opposite ways and neither is settled (R06-2).")
W("The drafts: four marks of four", H2)
W(f"A thousand drafted sections a kind, major, on the draws the earlier forms were read on. Verses at or under the kept median {pc(mv('chance')['written_at_or_under_the_kept_median'])} in 100 (asked: 45 to 60). Over the kept 75th {pc(mv('chance')['written_over_the_kept_75th'])} (20 to 30). Plain loops {pc(s4('chance', 'verse')['loops_kept_written'][1])} (within 5 of {pc(s4('chance', 'verse')['loops_kept_written'][0])}). Stage 4, the distance from held-out kept sections against the unpatched writer's, for first chord, last chord, chords, bigrams and bars: verse {dl('verse')}; bridge {dl('bridge')} (asked: no more than +0.02). Seven of the ten are nearer the kept sections. Table HU.")
W("The sealed song", H2)
W(f"Song 63, reserved for this gate since Window 205 and never run. Marks as written then, set down again with the ledger row before the run; the setting given by the switch, the lyric file untouched. Pool {R63['judge7']['range_choice']['builds_in_the_pool']}, where 10 or more was asked. The builds' middle words' fit {R63['judge7']['words_gate']['the_builds_median_fit']}, over the gate's floor of {R63['judge7']['words_gate']['at_least']}. The chosen plan's verse and bridge are under the kept 75th as drawn. Both marks hold and the form is built. The first holds with nothing to spare, and that should be said: read afterwards and deciding nothing, v50 without the form gives song 63 a pool of {V63['judge7']['range_choice']['builds_in_the_pool']} from {V63['melody']['survivors']} living builds, against {R63['melody']['survivors']} with it. The form does not touch the melody; the two runs choose different chord drafts of the twelve, and the melody's builds live or die on the plan they are given. One song cannot say whether that is the form or the luck of the drafts. Song 63 is spent.")
W("Table HU — the loop gate: major, a thousand drafted sections a kind (kept; no gate; 960, median; gentle; with a chance).")
rows = [("", "Kept", "No gate", "960 (median)", "Gentle", "With a chance")]
rows.append(("Verses at or under the kept median, in 100", "50", *[f"{pc(mv(f)['written_at_or_under_the_kept_median']):g}" for f in ("off", "median", "gentle", "chance")]))
rows.append(("Verses over the kept 75th, in 100", "25", *[f"{pc(mv(f)['written_over_the_kept_75th']):g}" for f in ("off", "median", "gentle", "chance")]))
rows.append(("Verses that are plain loops, in 100", f"{pc(s4('off', 'verse')['loops_kept_written'][0]):g}", *[f"{pc(s4(f, 'verse')['loops_kept_written'][1]):g}" for f in ("off", "median", "gentle", "chance")]))
rows.append(("Stage 4, verse bigrams", "", *[f"{s4(f, 'verse')['written']['bigrams']:g}" for f in ("off", "median", "gentle", "chance")]))
rows.append(("Stage 4, bridge last chord", "", *[f"{s4(f, 'bridge')['written']['last']:g}" for f in ("off", "median", "gentle", "chance")]))
table_before(anchor, [tuple(r) for r in rows])
W("")
W("The records. No lyric in the repository asks for chords that loop less, so no song record changes; songs 54 and 55 are byte for byte v50's; every room file is read again and both checks pass. Song 63's test records are in studies/loop_chance and are not the song made for the writer. Whether that song, in the gospel family where vamps belong to the style, should ask for the setting is the writer's choice.")
W("What this window could not do. It does not say that chords that loop less are better: the covers question that would say so is unsettled, which is why this is a setting. And song 63's pool at the mark's edge is a reason to watch the pool the first time a lyric asks for it.")
W("")
for lead in ("WINDOW 209", "27.133", "Table HU", "749.185 The form"):
    assert any(p_.text.strip().startswith(lead) or lead in p_.text[:40] for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v52.docx"); print("saved Luthier_v52.docx")
