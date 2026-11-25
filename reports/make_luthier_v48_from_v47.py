import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v47.docx")
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
T = J("studies/v48_trials/trial_readings.json"); H = J("studies/v48_trials/held_fit.json"); TL = J("studies/v48_trials/title_lines.json"); D = J("studies/v48_trials/drafts.json"); LL = J("studies/lyric_lines/result.json")["measures"]; RC = J("studies/lyric_lines/rhyme_check.json")
S3 = ("55", "54", "58"); l3 = lambda v: ", ".join(str(x) for x in v); pc = lambda x: round(100 * x)
sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v47")], "Luthier v47", "Luthier v48")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 47"))], "LUTHIER — VERSION 47", "LUTHIER — VERSION 48")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("204 Windows", "205 Windows"), ("Windows 1–204", "Windows 1–205"), ("204 scientific research windows", "205 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v219 (Luthier v48)")
oneL = [H[f"lyric{s}"]["one"]["live"] for s in S3]; banL = [H[f"lyric{s}"]["ban"]["live"] for s in S3]; offL = [H[f"lyric{s}"]["off"]["live"] for s in S3]
gv = D["gentle"]["repetition"]["major verse"]; ti = T["title_inside"]
set_cell(row.cells[1], f"THREE TRIALS, ALL FAILED; NOTHING BUILT; THE WORDS TESTED WITHIN A WRITER. The engine writes v47's notes. Review 32 listed three trials; each had its checks committed first (studies/v48_trials). (1) One leap past an octave allowed in a song, in place of none (749.176): living builds were to rise and fell ({l3([T['octave_one'][s]['live'] for s in S3])} against 223, 256, 294). 749.179: the engine fits its step and leap weights on trial runs that pass through the gates (fix 930), so a changed gate is a changed engine. On the same fitted engine, with only the gate changed, one leap allowed gives {l3(oneL)} living builds against the ban's {l3(banL)} and {l3(offL)} with no gate: a build that leaps past an octave nearly always does it twice. The ban stands. (2) The title line (749.177): in kept songs its longest note is on a stress in {pc(TL['by_line']['stressed'])} lines of 100, on a weak last syllable in {pc(TL['by_line']['weak, the line\'s last syllable'])}, on a weak syllable before the last word in {pc(TL['by_line']['weak, before the last word'])}. A gate on the last of these passed over {ti['54']['passed_over_in_100_living']} and {ti['49']['passed_over_in_100_living']} builds in 100 in songs 54 and 49, where 5 were allowed. Not built. (3) The gentler loop gate (749.178), redrawing only verses over the kept 75th: {pc(gv['written_at_or_under_the_kept_median'])} verses in 100 at or under the kept median where 45 to 60 were asked; all three checks fail; song 63 is not run and stays sealed. ON THE WORDS: a line test within artists (studies/lyric_lines; 356 artists, 50,834 songs, 672 on a Rolling Stone 500 list; rule first): rhyme, 'I' plus 'you', weight at the stanza's end and a feeling named late do not mark an artist's listed song; lines with 'you' run the other way ({LL['you_lines']['coef']} a standard deviation, p {LL['you_lines']['p']}). The session's test against covers, checked on an independent join: shorter lines hold, tied to repeated lines; 'I' plus 'you' does not. lib/luthier/lyric_people.py prints a lyric's 'I', 'you' and named feelings beside the hits', as advice.")
after_par("27.128", [
    (" Luthier v48 builds nothing into the engine (Window 205; Table HO; studies/v48_trials/RESULT.md). Three trial forms are in the code behind switches that are off and are marked as failed: LUTHIER_OCTAVE=one, LUTHIER_TITLE=inside, LUTHIER_LOOP=gentle. RULE FOR TRIALS OF A GATE (749.179): read it two ways, the whole engine with its fits, and the record's own fitted spec with only the gate changed (studies/v48_trials/held_fit.py). ADVICE ON THE WORDS: lib/luthier/lyric_people.py; it stops nothing. HOLD-OUTS: song 59 for everything; songs 50 and 63 banked, not run.", "27.129"),
])
P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 205: THREE TRIALS THAT FAILED, AND THE WORDS WITHIN A WRITER", H1)
W("Review 32 found v47 to reproduce and listed three trials in order: the octave gate in the shape kept songs have it; the gentler loop gate, with song 63 as its hold-out; the kept songs read for title lines, and a narrower title gate after. The writer also brought a round of research on lyrics and asked what the engine should take from it. This window reports both. Nothing passes, and nothing is built. Two of the failures say the same thing about where the engine's faults are.")
W("One leap past an octave (749.176)", H2)
W(f"The form: a build may hold one such leap in the song. The first check was that living builds rise in songs 55, 54 and 58. They fell: {l3([T['octave_one'][s]['live'] for s in S3])} against 223, 256, 294. The words' fit held and a random pool pick failed the rule {round(100 * T['octave_one_pools']['random_pool_pick'], 1)} times in 100 against 6.5, but the first check decides, and the ban stands.")
W("749.179 Why a looser gate gave fewer builds", H2)
W("Before it builds, the engine fits its step and leap weights to the song on short trial runs (fix 930), and the trial builds pass through the gates. With one leap allowed the fit landed elsewhere (song 55's leap weight 1.6, where the ban gave 0.64), the chosen key moved in two songs of three, and every build after was a different build. A gate cannot be tried as though it only removed builds. From here on a trial of a gate is read two ways: the whole engine, and the record's own fitted spec run again with only the gate changed.")
W(f"The second reading, made after the result, answers the question the trial asked. On the same fitted engine: the ban leaves {l3(banL)} living builds; one leap allowed, {l3(oneL)}; no gate, {l3(offL)}. One leap gives back 3, 6 and 6 of the 69, 66 and 111 builds the ban takes. A build that leaps past an octave nearly always leaps back. The kept-shaped form is the ban by another name. If the builds are wanted back, the question is why the draw leaps so far twice as often as kept songs, and that is a question about the draw.")
W("The title line (749.177)", H2)
W(f"The kept songs first, by a rule written before the reading: {TL['kept_songs_with_a_title_line']} kept songs, {TL['title_lines']} title lines whose words the lexicon holds. The longest note falls on a stressed syllable in {pc(TL['by_line']['stressed'])} lines of 100; on a weak syllable that is the line's last in {pc(TL['by_line']['weak, the line\'s last syllable'])}; on a weak syllable before the last word in {pc(TL['by_line']['weak, before the last word'])}. So kept songs do hold a weak last syllable long, one title line in six, which 961 as first written forbade; and a long note on a weak word inside the line is uncommon ({pc(TL['songs_with_any_weak_before_the_last_word'])} kept songs in 100 have one anywhere).")
W(f"Under 10 in 100, so the narrower gate was tried. It mends song 62. It passes over {ti['54']['passed_over_in_100_living']} of every 100 otherwise living builds in song 54, {ti['49']['passed_over_in_100_living']} in song 49, {ti['55']['passed_over_in_100_living']} in song 55 and none in song 58, where 5 were allowed. Not built; 961 stays the setting it was. The chosen tunes of v47, with no such gate, hold one such title line in 21. The draw makes the fault often; the judging already screens most of it.")
W("The gentler loop gate (749.178)", H2)
W(f"The form: a verse or bridge is drawn again only if its chord repetition is over the kept 75th. On a thousand drafted verses, major: {pc(gv['written_at_or_under_the_kept_median'])} in 100 at or under the kept median (asked: 45 to 60; no gate 45; the median gate 99); plain loops 21 in 100 (asked: 25 to 35; kept 30); the stage 4 reading of verse bigrams 0.022 further from held-out kept sections than the unpatched writer (allowed: 0.02), the bridge's last chord 0.035. Nearer than the median gate on every line and outside every bar. The unpatched writer puts 34 verses in 100 over the kept 75th, and the gate redraws all of them until none is left there, where kept songs keep a quarter. A gate that redraws to a line empties the far side of it. Song 63 was to be run once, and only if the seen songs passed. It is not run. 960 stays the setting it was.")
W("The words within a writer", H2)
W(f"The research round proposed that lyrics move people through persons and address more than through images, and listed line-level traits to test. I ran the first test it named, rule first (studies/lyric_lines): WASABI's lyrics with line breaks, 356 artists with a song on a Rolling Stone 500 list, 50,834 songs, 672 listed; each trait against the same artist's other songs. The rhyme detector, checked first against CoCoPops's hand marks, scores F1 {RC['f1']}. Nothing passes. Rhyme rate {LL['rhyme_rate']['coef']:+.2f} a standard deviation (p {LL['rhyme_rate']['p']:.2f}); 'I' plus 'you' {LL['iyou_rate']['coef']:+.2f} (p {LL['iyou_rate']['p']:.2f}); weight at the stanza's end and a feeling named late, nothing. Lines with 'you' are reversed: {LL['you_lines']['coef']:+.2f} (p {LL['you_lines']['p']:.3f}), in both halves. Unpredicted, so leads only: the listed song has shorter lines ({LL['syl_line']['mean_listed']:.1f} syllables against {LL['syl_line']['mean_other']:.1f}) and more lines that return.")
W("The songwriting session then ran the same traits against covers within a writer (studies/covers_lines), rule first, and I checked it on an independent join of the same sources. Shorter lines go with more covering artists in both joins (−0.029 and −0.031 a standard deviation), and cannot be told from repeated lines. 'I' plus 'you' passed in its join and not in mine (+0.008, p .30); underneath, both joins agree that 'I' goes with covers and 'you' does not. The session compared the joins song by song and withdrew that pass. So: what the round's document said about persons stands as advice for feeling, with no test of lasting value behind it; and 'you' leans the wrong way for critics and for covers alike.")
W("What was made of it: lib/luthier/lyric_people.py prints a lyric's 'I', 'you' and named feelings in 100 words beside the hits' medians, with a few plain notes. It stops nothing. Nothing of the round goes into the engine.")
for n_, title_, test_ in (
    ("749.180", "A build that leaps past an octave leaps back", "Test: the same fitted spec under the ban, one leap allowed, and no gate; living builds 223, 226, 292 (song 55); 256, 262, 320 (song 54); 294, 300, 405 (song 58)."),
    ("749.181", "A gate that redraws to a line empties the far side of it", "Test: verses over the kept 75th of chord repetition, in 100: kept 25, the writer 34, the gentle gate 0.1."),):
    W(f"{n_} {title_}", H2); W(test_)
W("Table HO — the three trials.")
rows = [("Trial", "Its deciding check", "Asked", "Found", "Verdict"),
        ("One leap past an octave allowed", "Living builds, songs 55, 54, 58", "above 223, 256, 294", l3([T['octave_one'][s]['live'] for s in S3]), "fails; the ban stands"),
        ("The same, on the same fitted engine (a reading)", "Living builds", "", l3(oneL) + " (no gate: " + l3(offL) + ")", "gives back 3, 6, 6"),
        ("Title gate, weak before the last word", "Builds passed over in 100, songs 54, 49", "5 at most", f"{ti['54']['passed_over_in_100_living']}, {ti['49']['passed_over_in_100_living']}", "fails; not built"),
        ("Gentle loop gate", "Verses at or under the kept median, in 100", "45 to 60", str(pc(gv['written_at_or_under_the_kept_median'])), "fails; song 63 not run")]
table_before(anchor, rows)
W("")
W("The records. None is made again: with every switch off the engine writes v47's notes (song 54 run again, byte for byte).")
W("What this window could not do. Rhythm scaling still leans low. The two faults found behind gates (the draw leaps too far; it holds weak title words long) and 749.171 (what the engine does inside a one-bar line) are all faults of the draw, and the draw is the next place to work. Not begun: 749.144, 749.147, the hymn items, 749.163.")
W("")
for lead in ("WINDOW 205", "27.129", "Table HO", "749.180 A build"):
    assert any(p_.text.strip().startswith(lead) or lead in p_.text[:40] for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v48.docx"); print("saved Luthier_v48.docx")
