"""Luthier v21 -> v22: the marriage of tune and words (the writer's way 3): a word's weight against its note's salience, read in the kept songs,
and the repairs that follow (Window 179, Module 27.103, Tables GI and GJ; fixes 879-884). Evidence: lib/luthier/stage9_results.json, word_weight.py,
tables/kept_word_weight.json, way3_PREDICTION.md. Run: python3 make_luthier_v22_from_v21.py"""
import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v21.docx")
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










R = json.load(open("/home/claude/rightrevjf/zeneng-pipeline/lib/luthier/stage9_results.json")); K = R["kept"]; F1 = R["first_measure_with_rarity"]; BB = R["builds_before"]; BA = R["builds_after"]; PT = R["parts"]; SG = R["songs"]; EB = R["engine_before_tiers"]
pc = lambda x: f"{100 * x:.0f}"; kq = K["fit"]; O = ("55", "54", "58"); PATH = {"55": "songs/p65/lyric55", "54": "songs/p64/lyric54", "58": "songs/p68/lyric58"}
def sg(k, when, key): return SG[PATH[k]][when][key]

sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v21")], "Luthier v21", "Luthier v22")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 21"))], "LUTHIER — VERSION 21", "LUTHIER — VERSION 22")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("178 Windows", "179 Windows"), ("Windows 1–178", "Windows 1–179"), ("178 scientific research windows", "179 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v193 (Luthier v22)")
set_cell(row.cells[1], f"THE MARRIAGE OF TUNE AND WORDS. The third of the writer's five ways: that in a great song the words that matter sit on the notes that matter. A syllable is given a weight the engine can read without ears (a function word, the weak syllable of a longer word, a stressed syllable) and a note a salience (its length, its place in the bar, its height in its line); the fit is their rank correlation over a song. Five predictions were written first; all five held, one of them the null. Kept songs fit at {kq[2]} (middle half {kq[1]} to {kq[3]}) and beat the same song with each line's words dealt again over its notes in {pc(K['above_shuffled'])} songs in a hundred. The engine's builds fit at {BB['54']['fit']} to {BB['55']['fit']}: on song 58 the pick fitted its words no better than shuffled words would. The fault was found in one place: a line sung again to new words took the old line's notes whatever the new words were. Lines sung again now choose, by the kept table, which notes are split, dropped or led into; the step between two words leans the way kept songs lean; and the builds' fits stand at {BA['54']['fit'][1]}, {BA['55']['fit'][1]} and {BA['58']['fit'][1]}. Against the chart record the fit stands at {K['vs_weeks'][0]}: it tells a song whose words belong to its tune from one whose words do not, and it does not tell a great song from a good one. It gates; it does not choose.")

after_par("27.102 The same order at every scale", [
    (f" The marriage of tune and words (Window 179; Tables GI, GJ; lib/luthier/word_weight.py; tables/kept_word_weight.json). PLACE BY WEIGHT (879): a fresh line's syllables are scored by where in the bar kept songs sing a syllable of that weight, over where they sing any; the hand-set stress scores of 653 and 760 are retired in 4/4. THE STEP BETWEEN TWO WORDS (880): its direction is weighted by the kept share for the two words' weights over the kept share for any two (a function word to a stressed syllable rises {pc(K['steps'][0][2][2])} times in a hundred, falls {pc(K['steps'][0][2][0])}). THE WORDS' GATE (881): a build whose fit is under the kept 10th percentile ({kq[0]}) is passed over, after the old charge's gate and the joint gate. A LINE SUNG AGAIN (882; amends 712, 772, 818): where the new line's syllables differ from its source's, every way of splitting, dropping or leading into the source's notes (three changes at most) is scored by 879's table and the best taken; a line of the same count keeps its tune unless one note dropped and one split gains more than the cost of two changes. IN THE RECORD (883): the song's fit and its three parts beside the kept. THE READING (884): weights 0, 0.4 and 1; salience the mean of the three standardised parts; lines split at rests of a half note. Outside 4/4 no kept table stands and the record says so.", "27.103"),
])

P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 179: THE MARRIAGE OF TUNE AND WORDS", H1)
W("The writer's way 3 (884)", H2)
W("The third way holds that a great song's tune and words are married: the word that carries the line is sung where the tune is strongest. To test it without ears both sides must be read from the page. A syllable's weight is read from the lexicon: nothing for a one-syllable function word (the, of, and, my), a little for the weak syllable of a longer word, the most for a stressed syllable. A note's salience is read from the score: how long it is, where in the bar it falls, and how high it stands in its own line, each set against the song's own spread. The fit is the rank correlation of weight with salience over every sung syllable. The control is the same song with each line's words dealt again in a random order over that line's notes, two hundred times: the tune is untouched and the words are the same words, and only their marriage is undone.")
W(f"Five predictions were written before any fit was computed (lib/luthier/way3_PREDICTION.md). That kept songs would beat their own shuffled words in four songs in five: they do in {pc(K['above_shuffled'])} in a hundred, with a median fit of {kq[2]} against a control of nearly nothing ({F1['control'][1]}). That the engine's builds would fit less well: they stood at {BB['54']['fit']}, {BB['58']['fit']} and {BB['55']['fit']} at the median, under the kept lower quartile of {kq[1]}. That among stressed syllables alone the rarer word would still get the stronger note: it does, weakly, a median of {F1['stressed_only_fit'][1]}, and only {pc(F1['stressed_only_above'])} songs in a hundred beat their control; so the rarity of a word was dropped from the reading and three weights kept. That length would carry more of the fit than height: narrowly, {K['by_length'][2]} against {K['by_height'][2]}; the place in the bar carries most, {K['by_place'][2]}. And that the fit would not rank kept songs by their chart record: it does not, {K['vs_weeks'][0]} against weeks and {K['vs_peak'][0]} against peak on {K['graded']} songs. The writer hoped to be wrong about the last and was not.")
W("What the kept songs do, and what the engine did (879, 880)", H2)
W(f"Table GI sets the kept songs beside the engine's builds. A kept function word falls on the bar's first beat {pc(K['place_share_by_tier'][0][0])} times in a hundred; the engine's fell there {pc(EB['function_word_on_bar_start'][0])} to {pc(EB['function_word_on_bar_start'][1])}. A kept weak syllable falls on the half bar {pc(K['place_share_by_tier'][1][1])} times in a hundred; the engine's {pc(EB['weak_syllable_on_half_bar'][1])} to {pc(EB['weak_syllable_on_half_bar'][0])}. A kept tune rises from a function word to a stressed syllable {pc(K['steps'][0][2][2])} times in a hundred and falls {pc(K['steps'][0][2][0])}; the engine's rose and fell alike. In kept songs a stressed syllable stands a third of a semitone over its line's mean and a function word as far under it; in the engine's, neither.")
W("Two rules were drawn from the table. A fresh line's rhythm is scored by where kept songs sing each weight, in place of the stress scores set by hand in earlier windows. And between two words the step's direction is weighted by the kept shares for their two weights. Each was then tried alone, and the trial is the finding of this window: neither moved the fit by much. The first, alone, left song 58's builds at "
  f"{PT['fresh_place_only'][0]} from {PT['none'][0]}; the second at {PT['step_only'][0]}. The hand-set scores had already put fresh lines' stresses where kept songs put them. The fault lay elsewhere.")
W("A line sung again (882)", H2)
W(f"More than half of a song's lines are not fresh. A second verse sings the first verse's tune to new words, and since fix 712 the engine has fitted the new syllables to the old notes by count alone: where the new line was longer the widest gap was split, where shorter the closest notes were dropped, and where the counts matched the notes were taken as they stood. Nothing asked what the new words were. So 'the' fell where 'coffee' had been, and half of all function words on the bar's first beat were in lines sung again. This is the fault a listener hears as a second verse that scans badly, and the engine could not see it because no reading looked at the words and the notes together.")
W(f"The repair lets the new words choose. Every way of fitting the line to its source by three changes or fewer (a note split, a note dropped, a pickup led in before the first note) is scored by the kept table, each change charged, and the best taken. With this rule alone song 58's builds rose from {PT['none'][0]} to {PT['again_only'][0]} and song 54's from {PT['none'][1]} to {PT['again_only'][1]}; with all three, to {PT['all'][0]} and {PT['all'][1]}. The charge on each change was set high enough that a line of the same count keeps its tune, because the first trials showed the cost of a low one: the builds' place among kept songs under the old 4/4 judge, the withheld reading, fell by half as verses stopped repeating. A cost remains. On song 58 the old judge's reading of rhythm saved by structure fell from {PT['structure_song58']['before']} to {PT['structure_song58']['after']} kept standard deviations and the builds' median place from {BB['58']['j6_place']} to {BA['58']['j6_place']}; on song 54 the same reading fell from {PT['structure_song54']['before']} to {PT['structure_song54']['after']}, from more repetitive than a kept song to about as repetitive. A tune that repeats and words that change pull against each other, and kept songs stand between: the engine stood at one end and now stands nearer the middle.")
W("The words' gate, and what it is not (881, 883)", H2)
W(f"By the rule of fix 858 a reading may gate when it tells damage and may choose only when it tells grade. The fit tells damage of its own kind, words that do not belong to their tune, in {pc(K['above_shuffled'])} kept songs in a hundred. It tells nothing of grade. So it gates, at the kept 10th percentile, after the two gates of stage 7, and the pick is still the first build past the gates in the order built. Nearly every build now passes: the gate is a floor under a fault the builder no longer makes, and the gain of this window is in the builder, not the judge. The picks show it unevenly, because a first build is a draw: song 58's pick rose from {sg('58', 'before', 'fit')} to {sg('58', 'after', 'fit')}, song 54's from {sg('54', 'before', 'fit')} to {sg('54', 'after', 'fit')}, and song 55's, which had drawn well before, stands at {sg('55', 'after', 'fit')} from {sg('55', 'before', 'fit')}.")
for n_, title_, test_ in (
    ("879", "Place in the bar by a word's weight", "Test: the builds' share of function words on the bar's first beat nearer the kept share than before on every song, and within three points of it."),
    ("880", "The step between two words by their weights", "Test: the builds' share of rising steps from a function word to a stressed syllable nearer the kept share than before on every song."),
    ("881", "The words' gate", "Test: the record says how many builds pass it, alone and after the other gates."),
    ("882", "A line sung again is fitted to its new words", "Test: the builds' median fit within the kept middle half on every 4/4 song; the old judge's median place for the builds printed beside it."),
    ("883", "The fit in the record", "Test: the song's fit and its parts by length, place and height printed beside the kept figures."),
    ("884", "The reading: a word's weight against its note's salience", "Test: kept songs over their shuffled-words control in four songs in five; the fit against the chart record printed.")):
    W(f"{n_} {title_}", H2); W(test_)
W("Table GI — what is done with a word's weight: kept songs, and the engine's builds before and after (in a hundred).")
rows = [("", "Kept songs", "Engine before (songs 55, 58)", "Engine after (songs 55, 54, 58)")]
rows.append(("A function word on the bar's first beat", pc(K["place_share_by_tier"][0][0]), f"{pc(EB['function_word_on_bar_start'][0])}, {pc(EB['function_word_on_bar_start'][1])}", ", ".join(pc(BA[k]["place_fn_bar_start"]) for k in O)))
rows.append(("A weak syllable on the half bar", pc(K["place_share_by_tier"][1][1]), f"{pc(EB['weak_syllable_on_half_bar'][0])}, {pc(EB['weak_syllable_on_half_bar'][1])}", "4, 1, 3"))
rows.append(("A stressed syllable on the bar's first beat", pc(K["place_share_by_tier"][2][0]), f"{pc(EB['stressed_on_bar_start'][0])}, {pc(EB['stressed_on_bar_start'][1])}", "22, 25, 26"))
rows.append(("The step from a function word to a stressed syllable rises", pc(K["steps"][0][2][2]), f"{pc(EB['step_up_function_to_stressed'][0])}, {pc(EB['step_up_function_to_stressed'][1])}", "43, 39, 44"))
rows.append(("The fit, median of the builds (kept: quartiles)", f"{kq[1]}, {kq[2]}, {kq[3]}", f"{BB['55']['fit']}, {BB['58']['fit']}", ", ".join(str(BA[k]["fit"][1]) for k in O)))
rows.append(("Songs over their shuffled-words control", pc(K["above_shuffled"]), "", ""))
rows.append(("The fit against weeks on the chart; against peak", f"{K['vs_weeks'][0]}; {K['vs_peak'][0]}", "", ""))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W("Table GJ — the three 4/4 songs written again from their lyrics, before and after this window.")
rows = [("", "Song 55", "Song 54", "Song 58")]
rows.append(("The pick's fit, before; after (kept 10th %s)" % kq[0], *[f"{sg(k, 'before', 'fit')}; {sg(k, 'after', 'fit')}" for k in O]))
rows.append(("The pick's fit by length, place, height (kept %s, %s, %s)" % (K["by_length"][2], K["by_place"][2], K["by_height"][2]), *[", ".join(str(x) for x in R["picks_by_part"][k]) for k in O]))
rows.append(("The builds' fit, median, before; after", *[f"{BB[k]['fit']}; {BA[k]['fit'][1]}" for k in O]))
rows.append(("Builds that survive, of 1,000", *[sg(k, "after", "survivors") for k in O]))
rows.append(("Past the old charge's gate; the joint gate; the words' gate", *[f"{sg(k, 'after', 'gates')['old_charge_least_half']}; {sg(k, 'after', 'gates')['joint_gate']}; {sg(k, 'after', 'words_gate')['pass_after_the_other_gates']}" for k in O]))
rows.append(("The pick's old charge, before; after (withheld)", *[f"{sg(k, 'before', 'charge')}; {sg(k, 'after', 'charge')}" for k in O]))
rows.append(("The builds' median place under the old 4/4 judge, before; after (withheld)", *[f"{BB[k]['j6_place']}; {BA[k]['j6_place']}" for k in O]))
rows.append(("Rhythm exponent of the pick, before; after (kept 0.61, 0.66, 0.72)", *[f"{sg(k, 'before', 'rhythm_scaling')}; {sg(k, 'after', 'rhythm_scaling')}" for k in O]))
rows.append(("Unstressed openings before the bar line, before; after (kept 43 in a hundred)", *[f"{pc(sg(k, 'before', 'entries')['unstressed openings before / on / after'][0])}; {pc(sg(k, 'after', 'entries')['unstressed openings before / on / after'][0])}" for k in O]))
rows.append(("Length in seconds (kept 165, 206, 243)", *[R["seconds"][k] for k in O]))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W(f"What this window could not do. The fit does not tell a great song from a good one: on {K['graded']} songs it stands at nothing against the chart record, as the old charge, the joint distance and the scaling exponents did before it. Two of the five ways have now been tried against that record, and each has given a reading that tells a kept song from a damaged or a made one and not one that ranks the kept. The record itself, weeks and peak for 131 songs, may be too small and too coarse to rank anything; the larger graded sets named in stage 7 are still unbuilt. The weights are three and crude: the lexicon knows a function word from a content word and knows nothing of which word a line turns on. Rarity was tried as that and added almost nothing. Length is not yet married: in the picks the weightier syllables do not get the longer notes (song 54's fit by length is under nothing), because note lengths are what is left between onsets and no rule sets them. The repair costs repetition on song 58, and the right charge for a change was set by the old judge's place, a reading of likeness, not of worth. Outside 4/4 there is no kept table, so song 52 and the hymns are written as before. The pick is still the first build past the gates. And the builds' fits on song 58 now stand over the kept median, by the place in the bar alone: a tune can honour its words too squarely, and nothing here says where that begins.")
W("")
for lead in ("WINDOW 179", "27.103 The marriage of tune and words", "Table GI", "Table GJ", "884 The reading"):
    assert any(p_.text.strip().startswith(lead) for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v22.docx"); print("saved Luthier_v22.docx")
