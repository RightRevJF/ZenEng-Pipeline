"""Luthier v23 -> v24: the session's fix list for v23 (findings 749.66 to 749.75, with 749.58 and 749.61 carried) answered
(Window 181, Module 27.105, Tables GM and GN; fixes 890-898). Evidence: lib/luthier/stage11_results.json, tables/kept_returns.json,
songs/p68/fixlist_v23.md, REVIEW_stage8.md, REVIEW_stage9.md. Run: python3 make_luthier_v24_from_v23.py"""
import copy
import copy
import json
from docx import Document
from docx.table import Table

d = Document("Luthier_v23.docx")
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










R = json.load(open("/home/claude/rightrevjf/zeneng-pipeline/lib/luthier/stage11_results.json")); SG = R["songs"]; KR = R["kept_returns"]["verse"]; RE = R["returns_engine"]; SS = R["stressed_sixteenths"]; LC = R["last_chorus_kept"]
pc = lambda x: f"{100 * x:.0f}"; O = ("55", "54", "58", "52"); PATH = {"55": "songs/p65/lyric55", "54": "songs/p64/lyric54", "58": "songs/p68/lyric58", "52": "songs/p62/lyric52"}
def ba(k, key, f=lambda x: x):
    a, b = SG[PATH[k]]["before"].get(key), SG[PATH[k]]["after"].get(key); return f"{f(a) if a is not None else ''}; {f(b) if b is not None else ''}" if (a is not None or b is not None) else ""

sub(P[find_par(lambda p_: p_.text.strip() == "Luthier v23")], "Luthier v23", "Luthier v24")
sub(P[find_par(lambda p_: p_.text.strip().startswith("LUTHIER — VERSION 23"))], "LUTHIER — VERSION 23", "LUTHIER — VERSION 24")
for p_ in d.paragraphs:
    t = p_.text
    for x, y in (("180 Windows", "181 Windows"), ("Windows 1–180", "Windows 1–181"), ("180 scientific research windows", "181 scientific research windows")):
        if x in t: sub(p_, x, y)
vh = d.tables[0]; last = vh.rows[-1]
vh._tbl.append(copy.deepcopy(last._tr)); row = vh.rows[-1]
set_cell(row.cells[0], "v195 (Luthier v24)")
set_cell(row.cells[1], f"THE SESSION'S FIX LIST FOR V23. The songwriting session reviewed versions 21 and 22, merged them, rebuilt song 58, and sent ten new findings with two carried. Nine are mended or measured here, one is answered from kept data and not built, and two stay carried. The one a listener would hear first: under a low voice the guitar had dropped out, because the rule that the accompaniment stays under the tune came from piano song; song 58's guitar sounded under 3 sung notes in a hundred and now sounds under {pc(SG[PATH['58']]['after']['guitar_under'])} (892). A line sung again may no longer leave a stressed syllable a sixteenth without a charge (891). How much of its source a returning line keeps was measured in kept songs for the first time: {KR['other_count_rhythm_kept'][0]} to {KR['other_count_rhythm_kept'][2]} of the rhythm by quartile, and the engine's lines stand inside or just over that (896). The harmony voice has a singer's range (893). A song has one length, counted once, and the intake now says how long a lyric will run before a note is written (894). The kept tables have makers that run inside the repo (895). The record says which gate took away how many builds, and says plainly that in 4/4 only the old charge takes any (897).")

after_par("27.104 Repairs after way 3", [
    (" The session's fix list for v23 (Window 181; Tables GM, GN; songs/p68/fixlist_v23.md). A WEAK ENDING, ANY WORD (890; answers 749.71; widens 871): a line ending on a word's weak syllables gives that word's stressed syllable a quarter at least, whatever the word's length. NO STRESSED SIXTEENTH WITHOUT A CHARGE (891; answers 749.66; amends 882): each stressed syllable a line sung again would leave a sixteenth long is charged half the cost of a change. THE GUITAR IN ITS OWN REGISTER (892; answers 749.73; amends 828): a guitar's chords are voiced in the guitar's kept register whatever the voice, and keep off the seconds either side of every note sung while they sound; the piano stays under the tune. THE HARMONY VOICE'S RANGE (893; answers 749.74; amends 829): no note under E2 or over A5; above the lead, by the kept shares for a voice above, only where no chord tone below is in range. ONE LENGTH (894; answers 749.69): the song's length is counted once, after the form is final; the flag says how many lines fewer or what tempo would bring it inside the kept lengths; 'song_from_lyric.py lyric.json 0' prints the length at intake and writes nothing. MAKERS IN THE REPO (895; answers 749.70): kept_corpus.py, cocopops_parse.py, make_kept_word_weight.py and make_kept_returns.py run on paths inside the repo, name the corpus they need and where to fetch it, and stop if it is not there. RETURNS MEASURED (896; answers 749.67): tables/kept_returns.json. THE GATES' REMOVALS (897; answers 749.68): the record gives the builds each gate took away. ONE FIT (898; answers 749.72): the words' fit is read once, on the notes as sung, and one set of kept figures stands.", "27.105"),
])

P = d.paragraphs
anchor = P[find_par(lambda p_: p_.text.strip().startswith("MODULE 0 EXTENSION") and p_.style.name.startswith("Heading"))]
def W(text, style=BODY, lead=None): return before(anchor, text, style, lead)
W("WINDOW 181: THE SESSION'S FIX LIST FOR V23", H1)
W("What the session sent", H2)
W("The songwriting session reviewed Luthier v21 and v22 (lib/luthier/REVIEW_stage8.md, REVIEW_stage9.md), found that every record reproduces byte for byte, merged both into main, confirmed findings 749.57 to 749.64 against the records (six closed, 749.58 and 749.61 carried), rebuilt song 58's scores and songbook, and filed ten findings, 749.66 to 749.75. Its list was written against v22. Version 23 had been written in the meantime and had already moved three of its items: the rests between lines (749.58), the song's length (749.69) and the fit by length it lists as not met. This window answers the list against the songs as v23 left them. Table GM gives each finding its answer.")
W("The guitar under a low voice (892)", H2)
W(f"The session heard it in song 58: the verses were bass and drums under the voice, and the guitar played only where the singer rested. The cause was a rule of this engine's own. Fix 828 voices every chord below the lowest note sung while it sounds, a rule taken from piano song, where the right hand stays under the tune. A guitar does not: its kept register runs from D3 to G4, around and above a man's voice, and under a baritone no three-note chord fits below the tune at all. Read on the songs as v23 left them, the chordal part sounded under {pc(SG[PATH['55']]['before']['guitar_under'])}, {pc(SG[PATH['54']]['before']['guitar_under'])} and {pc(SG[PATH['58']]['before']['guitar_under'])} sung notes in a hundred in songs 55, 54 and 58. The guitar is now voiced in its own kept register whatever the voice, and keeps off the seconds either side of every sung note; where no such chord is to be had it falls back to the old rule, and where that fails it rests. It now sounds under {pc(SG[PATH['55']]['after']['guitar_under'])}, {pc(SG[PATH['54']]['after']['guitar_under'])} and {pc(SG[PATH['58']]['after']['guitar_under'])}, with no chord a second from the sung note and every voicing inside the low-interval limits. The check that counted 'sung notes with accompaniment above them' as a fault now reads as a description for a guitar.")
W("The last chorus (749.75, answered and not built)", H2)
W(f"The session asked that the last chorus be the song's top, as Module 9.12 asks, where every chorus stands at one level. The kept figure was already in the repo and says otherwise for the accompaniment: in {LC['source']}, the last chorus's piano density minus the first chorus's has a median of {LC['last_minus_first_chorus_piano_density_median']:.0f} and is over nothing in {pc(LC['share_positive'])} songs in a hundred. Kept songs do not, as a rule, play the last chorus thicker. So no level is raised. Half of what the session read was the guitar's absence, which made the two-bar turn the loudest place in the song; with 892 that is gone. Whether a kept song lifts its last chorus by other means (a key change, an added voice, a held note) is not measured, and Module 9.12 stands as the writer's rule against a kept figure that does not support it: that is the writer's to settle.")
W("Lines sung again (890, 891, 896)", H2)
W(f"Two findings were about fix 882, which lets a returning line choose how it sits on its source's notes. The first (749.66): a split could halve the note under a stressed syllable and leave it a sixteenth; in song 54's pick, 19 of 134 stressed syllables in lines sung again against 4 of 82 elsewhere. Kept songs give a stressed syllable a sixteenth {pc(SS['kept_inside_lines'])} times in a hundred inside lines, so the thing itself is not a fault; a rate three times the song's other lines is. Version 23's term for time by weight (885) had already brought the builds' rates to {pc(SS['builds_charge_0']['55'][0])}, {pc(SS['builds_charge_0']['54'][0])} and {pc(SS['builds_charge_0']['58'][0])}; a charge on each stressed sixteenth, half the cost of a change, brings them to {pc(SS['builds_charge_4']['55'][0])}, {pc(SS['builds_charge_4']['54'][0])} and {pc(SS['builds_charge_4']['58'][0])}, beside {pc(SS['builds_charge_4']['55'][1])}, {pc(SS['builds_charge_4']['54'][1])} and {pc(SS['builds_charge_4']['58'][1])} in the other lines. With it 871 is widened (749.71): the stressed syllable of a line's last word gets a quarter whatever the word's length, where before only words stressed on the syllable before last were read.")
W(f"The second (749.67) was the better question: 882 trades a return's likeness to its source for the words' fit, and nothing kept bounded the trade. It is now measured (lib/luthier/make_kept_returns.py). In {KR['songs']} kept songs with a second verse, {pc(KR['share_of_lines_with_the_same_count'])} lines in a hundred of a later verse have the same count of notes as the first verse's line, and of those {pc(KR['identical_among_same_count'])} in a hundred are note for note the same. Where the counts differ, the later line keeps {KR['other_count_pitch_kept'][0]}, {KR['other_count_pitch_kept'][1]} and {KR['other_count_pitch_kept'][2]} of its source's pitches in order by quartile and {KR['other_count_rhythm_kept'][0]}, {KR['other_count_rhythm_kept'][1]} and {KR['other_count_rhythm_kept'][2]} of its rhythm. Before 882 the engine's returning lines kept {RE['v21']['54'][1]}, {RE['v21']['55'][1]} and {RE['v21']['58'][1]} of the rhythm: at or over the kept upper quartile, which is to say that the engine's second verses were more like their first than kept songs' are. They now keep {RE['v24']['54'][1]}, {RE['v24']['55'][1]} and {RE['v24']['58'][1]}, songs 54 and 55 inside the kept middle half and song 58 a little over its upper quartile. The engine's returns still keep more of their source than a kept song's do at the median, so the cost of a change stays at 8 and is not raised.")
W("Gates that take nothing away (897)", H2)
W("The session found that in 4/4 the joint gate and the words' gate pass nearly every build (749.68). It is so, and more so after v23: on songs 55, 54 and 58 the joint gate now takes away no build of the old charge's least half and the words' gate none. The record now gives each gate's removals. The session offered two mends: say it, or set the gates where they bind. This paper says it. A gate set at the kept 25th percentile would turn away one kept song in four, and by the rule of fix 858 a gate is a floor under damage and not a chooser; a floor the builder now clears is a floor doing its work. In 4/4 the old charge's least half is the only gate that takes builds away, and the pick is the first build made in that half. In 6/8 the joint gate takes all 38 (749.61, carried): song 52 is read against kept tunes that are not pop.")
for n_, title_, test_ in (
    ("890", "A weak ending in a word of any length", "Test: no line-final word holds a weak syllable longer than its stressed one (749.71's check)."),
    ("891", "No stressed sixteenth without a charge", "Test: stressed syllables a sixteenth long in lines sung again at the rate of the song's other lines, or under the kept 12 in a hundred (749.66's check)."),
    ("892", "The guitar in its own register", "Test: the guitar sounds under most sung notes, inside the low-interval limits, no voicing a second from a sung note (749.73's check)."),
    ("893", "The harmony voice has a range", "Test: no harmony note under E2 (749.74's check)."),
    ("894", "One length, and the length at intake", "Test: the flag and the check agree; the intake prints the length (749.69's check)."),
    ("895", "Makers that run in the repo", "Test: make_kept_word_weight.py rewrites the table byte for byte, or says which corpus it could not find (749.70's check)."),
    ("896", "Returns measured against kept songs", "Test: the share of its source a line sung again keeps, inside the kept quartiles (749.67's check)."),
    ("897", "The record says what each gate took away", "Test: the record names each gate's removals (749.68's check, its first half)."),
    ("898", "One fit, as sung", "Test: the record's two fields agree; the docstring matches the table (749.72's check).")):
    W(f"{n_} {title_}", H2); W(test_)
W("Table GM — the session's findings and their answers.")
rows = [("Finding", "Answer", "Fix", "Met?")]
rows += [("749.66 a stressed syllable left a sixteenth", f"Charged. Picks, lines sung again; other lines: song 54 {SS['picks']['54']}, song 55 {SS['picks']['55']}, song 58 {SS['picks']['58']}", "891", "Songs 54 and 58 yes; song 55 near the kept rate, a little over its other lines"),
         ("749.67 no kept figure bounds what a return keeps", f"Measured: kept rhythm {KR['other_count_rhythm_kept'][0]}–{KR['other_count_rhythm_kept'][2]}, pitch {KR['other_count_pitch_kept'][0]}–{KR['other_count_pitch_kept'][2]}; engine rhythm {RE['v24']['54'][1]}, {RE['v24']['55'][1]}, {RE['v24']['58'][1]}", "896", "Rhythm yes; song 58 a hair over the upper quartile"),
         ("749.68 the gates pass nearly every build", "Said plainly; removals in the record. The gates are not moved", "897", "Its first half; no second gate takes builds in 4/4"),
         ("749.69 one song, two lengths", "One count, after the form is final; the intake prints it", "894 (and 888)", "Yes; songs 54 and 58 still long"),
         ("749.70 no maker in the repo", "Makers for the two kept tables of words and returns; the parser; where to fetch the corpus", "895", "The tables yes; the stage results files are still records of runs"),
         ("749.71 871 reads only one kind of word", "Widened to any word", "890", f"One of {sum(R['weak_endings']['final_words_ending_weak'].values())} line-final words still holds its weak syllable longer (song 55, a line sung again)"),
         ("749.72 two fits, two sets of kept figures", "One fit, as sung; the docstring corrected", "898", "Yes"),
         ("749.73 the guitar drops out", f"Voiced in its own register. Under sung notes: {pc(SG[PATH['55']]['after']['guitar_under'])}, {pc(SG[PATH['54']]['after']['guitar_under'])}, {pc(SG[PATH['58']]['after']['guitar_under'])} in a hundred", "892", "Yes"),
         ("749.74 the harmony voice has no range", "E2 to A5; above the lead only where below has no room", "893", "Yes: lowest note E2"),
         ("749.75 the last chorus is not the top", "Not built: kept songs' last chorus is no thicker than their first", "none", "The writer's to settle against Module 9.12"),
         ("749.58 rests between lines (carried)", f"Mended in v23 by 887 for 4/4: median {SG[PATH['55']]['after']['rest_median']:.0f}, {SG[PATH['54']]['after']['rest_median']:.0f}, {SG[PATH['58']]['after']['rest_median']:.0f} twelfths (kept 24)", "887", "4/4 yes; song 52 still at 12"),
         ("749.61 6/8 and the joint gate (carried)", "No kept pop corpus in 6/8", "none", "No")]
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W("Table GN — the four songs written again from their lyrics, as v23 left them; after this window.")
rows = [("", "Song 55", "Song 54", "Song 58", "Song 52, 6/8")]
rows.append(("Sung notes with the guitar or piano under them, share", *[ba(k, "guitar_under") for k in O]))
rows.append(("Sung notes with a chord a second away, share", *[ba(k, "second_away") for k in O]))
rows.append(("Harmony voice: lowest note; notes under E2", *[ba(k, "harmony_low", lambda x: f"{x[0]}, {x[1]}") for k in O]))
rows.append(("Harmony voice: summed miss over six classes", *[ba(k, "harmony_miss") for k in O]))
rows.append(("Rest after a line, median in twelfths (kept 15, 24, 48)", *[ba(k, "rest_median", lambda x: f"{x:.0f}") for k in O]))
rows.append(("Rest share inside sung sections (kept 0.21, 0.30, 0.39)", *[ba(k, "rest_share") for k in O]))
rows.append(("The pick's fit of words to notes (kept 0.20, 0.29, 0.38)", *[ba(k, "fit") for k in O]))
rows.append(("The pick's fit by length (kept 0.13)", *[ba(k, "by_length") for k in O]))
rows.append(("Builds taken away by: the old charge; the joint gate; the words' gate", *[(lambda r: f"{r['old_charge']}; {r['joint_gate']}; {r['words_gate'] if r['words_gate'] is not None else 'not read'}")(SG[PATH[k]]["after"]["removed"]) for k in O]))
rows.append(("Rhythm exponent of the pick (kept 0.61, 0.66, 0.72)", *[ba(k, "rhythm_scaling") if k != "52" else "" for k in O]))
rows.append(("Pitch exponent of the pick (kept 0.79, 0.90, 1.00)", *[ba(k, "pitch_scaling") if k != "52" else "" for k in O]))
rows.append(("Length in seconds (kept 165, 206, 243)", *[ba(k, "seconds") for k in O]))
rows.append(("Builds that survive, of 1,000", *[ba(k, "survivors") for k in O]))
table_before(anchor, [tuple(str(x) for x in r) for r in rows])
W("")
W(f"What this window could not do. The last chorus is not raised, and the paper's own Module 9.12 and a kept figure now disagree in print. No gate but the old charge takes a build away in 4/4, so the pick is the first build of the better half and nothing more; the one reading with a claim to choose, pitch scaling, waits on a third set of songs. Song 58's pick fits its long notes to its words no better than before ({SG[PATH['58']]['after']['by_length']} against a kept {0.13}): the builds' median is at the kept figure and the pick is one draw. Song 54's guitar still rests under a third of its sung notes, where no chord in its register clears the tenor's line by more than a second. One line-final word in twenty still holds its weak syllable longer than its stressed one. The stage results files (stage8 to stage11) are records of runs, some of them made with the old 4/4 judge's data, and have no single maker. Songs 54 and 58 are long because their lyrics are; the intake now says so before a note is written. Song 52 in 6/8 has no kept pop corpus: its rests sit at the floor, no build passes the joint gate, and its words' weights are not read.")
W("")
for lead in ("WINDOW 181", "27.105 The session's fix list for v23", "Table GM", "Table GN", "898 One fit"):
    assert any(p_.text.strip().startswith(lead) for p_ in d.paragraphs), f"missing after build: {lead}"
d.save("Luthier_v24.docx"); print("saved Luthier_v24.docx")
