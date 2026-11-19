"""Luthier v25 -> v26: the kept corpus read whole. The session found that the parser dropped every sung note that begins a tie (749.82); the parser is mended
and every kept 4/4 table with a maker is rebuilt; the phrase check reads a breath at half a beat (749.83)
(Window 183, Module 27.107, Tables GQ and GR; fixes 904-906). Evidence: lib/luthier/stage13_results.json, REVIEW_stage12.md, songs/p68/fixlist_v26.md.
Run: python3 make_luthier_v26_from_v25.py"""
import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v25.docx")
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










R = json.load(open("/home/claude/rightrevjf/zeneng-pipeline/lib/luthier/stage13_results.json")); PA = R["parser"]; AT = R["atlas"]; TB = R["tables"]; SG = R["songs"]; BU = R["builds"]; W2 = R["way2_again_on_the_corrected_parse"]; RP = R["register_plan"]
pc = lambda x: f"{100 * x:.0f}"; O = ("55", "54", "58", "52"); l3 = lambda v: ", ".join(str(x) for x in v)
def ba(k, key, f=lambda x: x):
    a, b = SG[k]["before"].get(key), SG[k]["after"].get(key); return f"{f(a) if a is not None else ''}; {f(b) if b is not None else ''}" if (a is not None or b is not None) else ""
WWb, WWa = TB["kept_word_weight"]["before"], TB["kept_word_weight"]["after"]; LEb, LEa = TB["kept_line_ends"]["before"], TB["kept_line_ends"]["after"]; qb, qa = AT["quartiles_before"], AT["quartiles_after"]

sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v25")], "Luthier v25", "Luthier v26")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 25"))], "LUTHIER — VERSION 25", "LUTHIER — VERSION 26")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("182 Windows", "183 Windows"), ("Windows 1–182", "Windows 1–183"), ("182 scientific research windows", "183 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v197 (Luthier v26)")
set_cell(row.cells[1], f"THE KEPT CORPUS READ WHOLE. Reviewing version 25, the songwriting session found a fault under every kept table of 4/4 song this engine has: the parser of the kept corpus dropped each sung note that begins a tie, {PA['sung_notes_beginning_a_tie']:,} of them, and kept the tie's end in its place. A note tied over a bar line or a beat is a syncopation; read by its end it lands on the beat. So the kept songs had been read squarer than they are. With the parser mended, kept onsets on the bar's first beat fall from {pc(AT['onset_place_shares_before'][0])} in a hundred to {pc(AT['onset_place_shares_after'][0])}, onsets on any beat from {pc(qb['onsets on the beat'][1])} to {pc(qa['onsets on the beat'][1])} at the median, and notes slurred to a syllable from {pc(PA['melisma_share_before'])} to {pc(PA['melisma_share_after'])}. The 4/4 kept table, the kept songs' joint readings, the tables of words' weights, line ends and returns, and the register plan are rebuilt from the mended parse, each by a maker that runs inside the repo, and the four songs are written again against them. The findings of the last four versions hold in direction; their figures move. What was not rebuilt is listed, because some constants set before version 12 have no maker.")

after_par("27.106 How a line ends", [
    (" The kept corpus read whole (Window 183; Tables GQ, GR; songs/p68/fixlist_v26.md). TIE STARTS READ (904; answers 749.82): the parser reads a note's length after a leading tie, slur or phrase mark; a tie's end still lengthens the note it is tied to. THE KEPT TABLES REBUILT (905; answers 749.82): make_kept_4_4_tables.py writes the 4/4 pop table of the metre atlas (812, 817, 863, 864, 867) and the 4/4 rows of the kept readings (860) from the kept corpus inside the repo, and reproduces the old tables from the old parse; with make_kept_word_weight.py, make_kept_returns.py, make_kept_line_ends.py and kept_plan.py every kept 4/4 table that has a maker is rebuilt; a record carries the fingerprints of the tables it read. A BREATH AT HALF A BEAT (906; answers 749.83; amends 831): the phrase check splits at half a beat of silence and prints the share of phrases over twelve beats beside the kept share.", "27.107"),
])

P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 183: THE KEPT CORPUS READ WHOLE", H1)
W("What the session found (904)", H2)
W(f"The session reviewed Luthier v25 (lib/luthier/REVIEW_stage12.md), reproduced every record and the new table, agreed that fixes 871 and 890 were rightly retired (its recount: {R['weak_endings_recounted']['session_as_parsed'][0]} line ends, the weak syllable outlasting the stressed one in {pc(R['weak_endings_recounted']['session_as_parsed'][1])} in a hundred), closed its own 749.77 with a kept figure for returning lines, and rebuilt song 58. In recounting, it read the corpus files beside the parsed table and found that they did not agree. In the corpus's notation a note that begins a tie carries a bracket before its length. The parser read a length only at the head of the token, found none, and dropped the note and its syllable; the tie's end, which carries no syllable, was then kept as a note slurred to the syllable before, or merged into an earlier note of the same pitch. {PA['sung_notes_beginning_a_tie']:,} sung notes begin a tie.")
W("The fault is older than the session knew. The parser was written at Window 42, and every table of kept 4/4 song since has been built on its output: the kept two-bar rhythms a line is drawn from, the places in the bar, the quartiles every build is charged against, the joint gate, the words' weights, the line ends. And the error is not noise. A singer who comes in an eighth before the bar and holds across it has sung a syncopation; read by the tie's end, the note lands on the bar line. The kept songs had been read with their anticipations squared off.")
W("What moved (905)", H2)
W(f"With the tie starts read, the kept songs have {PA['voice_notes_after']:,} sung notes where they had {PA['voice_notes_before']:,}; one more song reaches the hundred and fifty notes the tables ask, so the kept songs are {PA['kept_songs_after']}. Kept onsets on the bar's first beat fall from {pc(AT['onset_place_shares_before'][0])} in a hundred to {pc(AT['onset_place_shares_after'][0])}, and onsets on an off-beat eighth rise from {pc(AT['onset_place_shares_before'][3])} to {pc(AT['onset_place_shares_after'][3])}. By song, the share of onsets on a beat stood at {l3(qb['onsets on the beat'])} by quartile and stands at {l3(qa['onsets on the beat'])}; on the bar's first beat, {l3(qb[chr(111) + 'nsets on the bar' + chr(39) + 's first beat'])} and now {l3(qa[chr(111) + 'nsets on the bar' + chr(39) + 's first beat'])}. A kept stressed syllable falls on the bar's first beat {pc(WWa['place_share_by_tier'][2][0])} times in a hundred, not {pc(WWb['place_share_by_tier'][2][0])}. Notes slurred to a syllable are {pc(PA['melisma_share_after'])} in a hundred of sung notes, not {pc(PA['melisma_share_before'])}: two in five of the kept 'melismas' had been tie ends.")
W(f"The tables of the last four versions move with it (Table GQ). The words' fit rises, because the notes that were dropped carried syllables and the tie ends that stood for them carried none: the kept quartiles are {l3(WWa['fit_percentiles_10_25_50_75_90'][1:4])} where they were {l3(WWb['fit_percentiles_10_25_50_75_90'][1:4])}, the fit by length {WWa['fit_by_length'][2]} at the median where it was {WWb['fit_by_length'][2]}, and {pc(WWa['songs_above_their_shuffled_words_95th'])} kept songs in a hundred beat their shuffled words. The words' gate, the kept tenth, moves from {WWb['fit_percentiles_10_25_50_75_90'][0]} to {WWa['fit_percentiles_10_25_50_75_90'][0]}. At a line's end a held note is now read at its full length when it is tied and was before read at its end's: a stressed last syllable is held a half note or more {pc(LEa['held_a_half_or_more_by_tier'][2])} times in a hundred, a function word {pc(LEa['held_a_half_or_more_by_tier'][0])} where the old parse said {pc(LEb['held_a_half_or_more_by_tier'][0])}; lines run on {pc(LEa['lines_run_on_with_under_a_beat_of_rest_share'])} times in a hundred. The rest share inside sung sections is lower than was thought, {l3(RP['rest_share'][1][1:4])} by quartile against {l3(RP['rest_share'][0][1:4])}: the notes that were cut at their ties had been read as rest. What a returning line keeps of its source barely moves. Pitch scaling and rhythm scaling barely move.")
W(f"No finding of the last four versions is overturned. Kept songs still marry weight to salience; kept lines still run on; kept singers still hold a word's weak last syllable ({pc(R['weak_endings_recounted']['session_with_ties'][1])} in a hundred with ties read); the fit still does not rank kept songs by their chart record ({WWa['fit_vs_weeks_on_chart'][0]} against weeks). The one reading with a claim on the chart record was run again on the mended parse: pitch scaling against weeks {W2['weeks'][0]} and against peak {W2['peak'][0]} on {W2['new_songs']} songs the first run had not seen, and the critics' list still does not agree ({W2['rs_against_cb_auc']}). The constants fitted to the old tables (the powers of the place, step and length terms) were tried on the builds against the new figures and stand: the builds' fit {l3(BU['fit'])}, by length {l3(BU['by_length'])}, by place {l3(BU['by_place'])}, against the kept {WWa['fit_percentiles_10_25_50_75_90'][2]}, {WWa['fit_by_length'][2]} and {WWa['fit_by_place'][2]}.")
W("What the engine does with it", H2)
W(f"The engine draws a fresh line's rhythm whole from the kept two-bar rhythms, so the mended table changes what it draws without a rule being touched: the rhythms with a note tied over the bar are now in the table. The builds' onsets on the bar's first beat stand at {l3(BU['on_bar'])}, at the kept median of {qa[chr(111) + 'nsets on the bar' + chr(39) + 's first beat'][1]}. Their onsets on any beat stand at {l3(BU['on_beat'])}, at the kept upper quartile and over the kept median of {qa['onsets on the beat'][1]}: the builds are still squarer than kept songs. Three rules set before version 12 pull that way and were set on the old parse: the shares of lines that enter before, on and after the bar line (771), the death of a build with too few stressed syllables on the beat (731), and the title line's stresses pulled to the beat (840). They have no maker and are not rebuilt here; they are the first work of the next version.")
W("A breath at half a beat (906)", H2)
W(f"Since 899 lets lines run on, the check of 831 that counted sung phrases over eight seconds, splitting at a whole beat of silence, reported five to seven long phrases a song. Kept singers sing the same phrases and breathe in half a beat. The check now splits at half a beat and prints the share of phrases over twelve beats beside the kept share, {LEa['phrases_split_at_half_a_beat']['share_over_12_beats']}, with each kept song's longest phrase at {l3(LEa['phrases_split_at_half_a_beat']['each_songs_longest_quartiles'])} beats by quartile. The songs stand at {SG['55']['after']['phrases'][0]}, {SG['54']['after']['phrases'][0]} and {SG['58']['after']['phrases'][0]}, with longest phrases of {SG['55']['after']['phrases'][1]}, {SG['54']['after']['phrases'][1]} and {SG['58']['after']['phrases'][1]} beats: over the kept share and inside the kept spread of longest phrases.")
for n_, title_, test_ in (
    ("904", "The parser reads a note that begins a tie", "Test: no sung note dropped for want of a length (749.82's check, first part)."),
    ("905", "The kept 4/4 tables rebuilt, each by a maker in the repo", "Test: the maker of the 4/4 table reproduces the old table from the old parse; the tables are rebuilt and committed; a record names the tables it read (749.82's check)."),
    ("906", "A breath read at half a beat", "Test: the phrase check splits at half a beat and prints the kept figure (749.83's check).")):
    W(f"{n_} {title_}", H2); W(test_)
W("Table GQ — the kept songs as parsed before and with tie starts read.")
rows = [("", "Before", "With tie starts read")]
rows.append(("Sung notes; kept songs of 150 notes or more", f"{PA['voice_notes_before']:,}; {PA['kept_songs_before']}", f"{PA['voice_notes_after']:,}; {PA['kept_songs_after']}"))
rows.append(("Onsets: bar's first beat, half bar, another beat, off-beat eighth, finer", l3(AT["onset_place_shares_before"]), l3(AT["onset_place_shares_after"])))
for k in ("onsets on the beat", "onsets on the bar's first beat", "notes a bar", "repeated notes", "distinct rhythms over bars", "bars on a rhythm already sung", "pitch scaling", "rhythm scaling"): rows.append((f"{k[0].upper() + k[1:]}, by song (quartiles)", l3(qb[k]), l3(qa[k])))
rows.append(("Notes slurred to a syllable, share of sung notes", PA["melisma_share_before"], PA["melisma_share_after"]))
rows.append(("The words' fit: 10th, quartiles, 90th", l3(WWb["fit_percentiles_10_25_50_75_90"]), l3(WWa["fit_percentiles_10_25_50_75_90"])))
rows.append(("The fit by length; by place; by height (medians)", f"{WWb['fit_by_length'][2]}; {WWb['fit_by_place'][2]}; {WWb['fit_by_height'][2]}", f"{WWa['fit_by_length'][2]}; {WWa['fit_by_place'][2]}; {WWa['fit_by_height'][2]}"))
rows.append(("A stressed syllable on the bar's first beat; a function word there", f"{WWb['place_share_by_tier'][2][0]}; {WWb['place_share_by_tier'][0][0]}", f"{WWa['place_share_by_tier'][2][0]}; {WWa['place_share_by_tier'][0][0]}"))
rows.append(("Line ends read", LEb["line_ends"], LEa["line_ends"]))
rows.append(("Last syllable a half note or more: function word, weak, stressed", l3(LEb["held_a_half_or_more_by_tier"]), l3(LEa["held_a_half_or_more_by_tier"])))
rows.append(("Last syllable an eighth or less: function word, weak, stressed", l3(LEb["an_eighth_or_less_by_tier"]), l3(LEa["an_eighth_or_less_by_tier"])))
rows.append(("Lines that run on with under a beat of rest", LEb["lines_run_on_with_under_a_beat_of_rest_share"], LEa["lines_run_on_with_under_a_beat_of_rest_share"]))
rows.append(("Rest share inside sung sections (quartiles)", l3(RP["rest_share"][0][1:4]), l3(RP["rest_share"][1][1:4])))
rows.append(("A returning line of another count keeps of its source's rhythm (quartiles)", l3(TB["kept_returns"]["before"]["verse"]["other_count_rhythm_kept"]), l3(TB["kept_returns"]["after"]["verse"]["other_count_rhythm_kept"])))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W("Table GR — the four songs written again against the rebuilt tables: as v25 left them; after this window.")
rows = [("", "Song 55", "Song 54", "Song 58", "Song 52, 6/8")]
rows.append((f"Onsets on the bar's first beat (kept now {l3(qa[chr(111) + 'nsets on the bar' + chr(39) + 's first beat'])})", *[ba(k, "on_bar") for k in O]))
rows.append((f"Onsets on the beat (kept now {l3(qa['onsets on the beat'])})", *[ba(k, "on_beat") for k in O]))
rows.append((f"The pick's fit of words to notes (kept now {l3(WWa['fit_percentiles_10_25_50_75_90'][1:4])}; gate {WWa['fit_percentiles_10_25_50_75_90'][0]})", *[ba(k, "fit") for k in O]))
rows.append((f"The pick's fit by length (kept now {WWa['fit_by_length'][2]})", *[ba(k, "by_length") for k in O]))
rows.append((f"Lines that run on (kept now {LEa['lines_run_on_with_under_a_beat_of_rest_share']})", *[ba(k, "run_on") for k in O]))
rows.append(("Silences of a beat or more per hundred beats (kept 7.0, 9.1, 11.1 on the old parse)", *[ba(k, "silences") for k in O]))
rows.append((f"Rest share inside sung sections (kept now {l3(RP['rest_share'][1][1:4])})", *[ba(k, "rest_share") for k in O]))
rows.append((f"Sung phrases over twelve beats, share; the longest in beats (kept {LEa['phrases_split_at_half_a_beat']['share_over_12_beats']})", *[(f"{SG[k]['after']['phrases'][0]}; {SG[k]['after']['phrases'][1]}" if SG[k]["after"].get("phrases") else "") for k in O]))
rows.append(("The pick's old charge; the builds' median", *[f"{SG[k]['before']['charge']}, {SG[k]['before']['median_charge']}; {SG[k]['after']['charge']}, {SG[k]['after']['median_charge']}" for k in O]))
rows.append(("Builds taken away by: the old charge; the joint gate; the words' gate, after", *[(lambda r: f"{r['old_charge']}; {r['joint_gate']}; {r['words_gate'] if r['words_gate'] is not None else 'not read'}")(SG[k]["after"]["removed"]) for k in O]))
rows.append(("Rhythm exponent of the pick", *[ba(k, "rhythm_scaling") if k != "52" else "" for k in O]))
rows.append(("Pitch exponent of the pick", *[ba(k, "pitch_scaling") if k != "52" else "" for k in O]))
rows.append(("Key", *[ba(k, "key") for k in O]))
rows.append(("Builds that survive, of 1,000", *[ba(k, "survivors") for k in O]))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W(f"What this window could not do. Not everything built on the old parse has a maker. The shares of lines entering before, on and after the bar line (771), the least share of stressed syllables on the beat (731, 0.4), the title line's stresses on a beat (840, kept 0.73), the weights of a word's stressed syllable against its other (847), the share of fresh lines sung in one bar (876) and the counts of long silences (877) are constants in the code, read from the old parse and not read again. The old 4/4 judge, the withheld reading of every version since 20, holds data built on the old parse and is printed here for continuity and no more. The register plan was rebuilt on {RP['songs'][1]} songs where it had {RP['songs'][0]}, because the private selection behind it reads lines and the lines changed. The session's own studies that read the corpus by another parser (the melisma shares of 848, the slots of 869, the degrees of 846, the breath and silence figures) were not checked here; the session is asked to say which of them read ties. The builds' median charge rose on songs 54 and 58 ({SG['54']['before']['median_charge']} to {SG['54']['after']['median_charge']}, {SG['58']['before']['median_charge']} to {SG['58']['after']['median_charge']}): there the engine stands further from the kept songs as they are than it stood from the kept songs as they were misread, most of all in how often it lands on the beat. One thing the old parse had made a fault is no fault: the picks' rest share, under the old kept middle half in v25, is inside the true one. Song 58's pick fits its words at {SG['58']['after']['fit']}, just past the new gate. And the pick is still the first build of the old charge's better half.")
W("")
for lead in ("WINDOW 183", "27.107 The kept corpus read whole", "Table GQ", "Table GR", "906 A breath"):
    assert any(p_.text.strip().startswith(lead) for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v26.docx"); print("saved Luthier_v26.docx")
