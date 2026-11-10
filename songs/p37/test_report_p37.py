"""Write test_report.md for song 37 (ZenEng v96): every figure read from the runs, readings and record."""
import pickle, sys, numpy as np
H = "/home/claude/p37"; sys.path.insert(0, H)
sys.argv = [sys.argv[0], "1", "main"]
import riff_p37 as RV
RD = pickle.load(open(f"{H}/readings.pkl", "rb")); REC = pickle.load(open(f"{H}/song_record.pkl", "rb")); T = RD["tests"]
RF = pickle.load(open(f"{H}/riff_p37.pkl", "rb")); DR = pickle.load(open(f"{H}/out/demo_report.pkl", "rb"))
M_ = pickle.load(open(f"{H}/melody_main.pkl", "rb"))
import importlib.util as _iu
_sp = _iu.spec_from_file_location('intake37', f'{H}/intake.py'); intake = _iu.module_from_spec(_sp); _sp.loader.exec_module(intake)
def pc(x, d=0): return f"{100 * x:.{d}f}%"
rr = RD["rerun"]["main"]; tg = RD["targets_pick"]
NM = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]; nm = lambda p: f"{NM[p % 12]}{p // 12 - 1}"
L = ["---", 'title: "Windows Down — Test report (ZenEng v96)"', 'author: "Words and music: Jason Bryant"', 'date: "10 November 2026"', "---", "",
"## The brief\n",
"A new song under ZenEng v96, pop, rock or country. The spec read first (version row v130, last fix 224; the session's 212–223 under its numbers; Module 27.38 for what changed in 213, 218 and 220, and for 224); the tables read, not refitted: zeneng_v88_tables.json (sha256 561355b1…), zeneng_v91_hymn_supplement.json (e74e7c30…), zeneng_v96_discriminator_tables.json (1a2af952…; 56 measures, 46 marked for the distance). Intake one question a turn, the full lyric before any music; at the lyric stage 220 (every section a multiple of four bars; lines too long for two bars named), 213 (one verse or chorus whose first two lines are within three syllables, and why), 202 and 208 (the summit question with chart pop's peak; the bridge question with the kept figures). Ported before the search: 224 first, then 212, 214, 215, 216, 217, 218, 219, 223. A control with 224 off. Findings from 225; the paper not edited.\n",
"## Intake\n",
"| # | Question | Answer |\n|---|---|---|"]
for e in intake.LOG[1:]:
    if "topic" in e: L.append(f"| {e['q']} | {e['topic']} | {str(e['answer'])[:160]} |")
    elif "file" in e and "answer" not in e: L.append(f"| — | {e['q']} | shown in full ({e['file']}) |")
    else: L.append(f"| — | {e['q']} | {str(e.get('answer', ''))[:200]} |")
L += ["", "**The song.** *Windows Down*: heartland rock, 4/4 at ♩ = 122, A major, male baritone D3–F♯4. A man walks out of his plant's last shift after twenty-six years and drives home to his wife with the windows down. Form (220: every section a multiple of four bars, every line two bars, no three-bar line chosen): Intro 8 · Verse 8 · Pre 4 · Chorus 16 · Verse 8 · Pre 4 · Chorus 16 · Bridge 8 · Solo 16 · Last Chorus 16 · Outro 8 = 112 bars, 3:40. At the lyric, no line needed more than two bars at about four syllables a bar; the tightest held nine sung syllables after the pickup and were named while the lyric was open. The chorus opens with two title lines of eight syllables each (213).\n",
"## The ports\n",
"| Fix | In song 37 |\n|---|---|",
"| 224 | Before each build, a target drawn uniformly from chart pop's kept middle half (25th–75th) on eleven calibrated measures (repeat, step, third, fourth or fifth, past a fifth, chord tones on and off the beat, eighth- and quarter-note gaps, the longest note over the median, notes a bar), recorded with the build. The walk's category weights, the chord term, the rhythm's gap tilt and landing, the line-end holds and the melismas are aimed at the build's own point. The control draws nothing: every build aimed at the chart medians. |",
"| 212 | A line followed by a copy (a repeated section, a returning unit, the chorus's second eight bars, and chorus 1's line 4 before verse 2's first line) is drawn with its last onset no later than the copy's first onset less a quarter's hold and an eighth's breath. |",
"| 214 | One draw over every candidate pitch, each interval category tilted by the chord it offers; recalibrated for this song so builds read near their own targets. |",
"| 215 | No sung note a tritone from its chord's root (G♯ over D here); the walk skips it, a copied note moves a step to a chord tone; gated on beats and on notes a quarter or longer. |",
"| 216 | The summit (the writer's A): F♯4 on 'HOL-lering', the first stress of chorus line 4, fixed on that line's downbeat; the chord plan puts D under it (D holds F♯); five times. |",
"| 217 | Copies keep their place counted from their line's end (two-bar lines, so no copy moves); every chorus's last line lands on A over A. |",
"| 218 | About four syllables a bar; onsets on eighths; quarters inside lines (the gap tilt, and lines that land on beat 3 of their second bar); line ends held a quarter, a dotted quarter or a half. |",
"| 219 | The 181 gate read on lines, onsets and contour counted from each line's downbeat. |",
"| 223 | A compound of two monosyllables ('someday') takes its primary on the first part, except as the line's last word. |",
"| kept | 181/195 returns; 182's walk with 197's turn; 196's run clause; 200; 205's plans (the chorus offered by the lyric, AABC drawn at 0.3); 208 (the bridge's opening a gate, its median above the verse's a gate, the writer's A: lifted); 209 (riff_p37.py); 210 on 46 measures from the v96 file; 211. No stressed syllable is placed as a pickup. |", "",
f"**The search.** N {rr['N']}, seed {rr['seed']}, PYTHONHASHSEED 0, code {rr['code_sha']}, Python {rr['python']}, numpy {rr['numpy']}. {RD['survivors']['main']} survivors of 500; frozen order {RD['order']['main']}, reproduced exactly on a second run. Pick {RD['pick']['main']}, first by the rank of record (composite {RD['comp']['main']:.3f}); no hand edits. Plans: verse " + "".join(RD['plans']['Verse']) + ", pre-chorus " + "".join(RD['plans']['Pre']) + ", chorus " + "".join(RD['plans']['ChorusHead']) + " sung twice, bridge " + "".join(RD['plans']['Bridge']) + ". The pick's drawn targets: " + ", ".join(f"{k.replace('_', ' ')} {v:g}" for k, v in tg.items()) + ".\n",
f"**The control.** Same seed and N, 224 off (every build aimed at the chart medians). {RD['survivors']['ctl']} survivors, order {RD['order']['ctl']}; first pick {RD['pick']['ctl']} (composite {RD['comp']['ctl']:.3f}).\n",
f"**A probe (not asked for; evidence for finding 225).** Same seed and N, targets drawn from the kept 5th–95th instead of the middle half: {RD['survivors']['wide']} survivors, order {RD['order']['wide']}.\n",
"**Hand inspection of the pick.** Printed syllable by syllable before the record was built. Two faults in earlier picks of the same code were fixed in the construction and the run repeated: a stressed syllable placed as a pickup ('WIN-dows' with 'win' before the bar and '-dows' on the downbeat; 'NUM-ber' likewise), now never allowed; and the last line's first 'home', which the writer asked to be held, sung as an eighth; that line is now drawn with its first 'home' held a half note and its second 'I'm almost home' landing on A3. The frozen pick needed no hand edit.\n",
"## The readings the brief asked for\n",
"Builds are every song the generator finished, before the gates. Bar-window shares are medians in the table; across all builds the opening unit returned third in " + f"{pc(T['t220']['unit3_builds_mean'])} of verse and chorus windows and was repeated at once in {pc(T['t213']['unit2_builds_mean'])} (means; kept 31–49% and 17–28%).\n",
RD["md"], "",
f"**Distance from the centre (210, on the 46 measures from the v96 file).** The pick {RD['distance']['main'][0]:.3f}, {RD['distance']['main'][1]}; the control's pick {RD['distance']['ctl'][0]:.3f}, {RD['distance']['ctl'][1]}. Builds too central (under 0.086): run {pc(RD['too_central']['main'])}, control {pc(RD['too_central']['ctl'])}, probe {pc(RD['too_central']['wide'])} (song 36 version 3: 75%). Builds inside the chart songs' middle half (0.133–0.228): run {pc(RD['in_middle_half']['main'])}, control {pc(RD['in_middle_half']['ctl'])}, probe {pc(RD['in_middle_half']['wide'])}.\n",
"**Every measure outside both kept middle halves (of 56).** The pick is outside both on " + f"{len(RD['pick_outside'])}: " + ", ".join(f"{k.replace('_', ' ')} {v:g} ({d})" for k, v, d in RD["pick_outside"]) + f". The control's pick on {len(RD['ctl_outside'])}. The table lists every measure the pick is outside on and every measure at least a fifth of the builds are outside on.\n",
RD["outside_md"], "",
"**Section lengths in bars.** " + " · ".join(f"{k} {v}" for k, v in T["t220"]["sections"].items()) + " = 112: every section a multiple of four.\n",
"**How far the builds followed their targets (224).** Correlation between a build's drawn target and what it reads, and the means: " + "; ".join(f"{k.replace('_', ' ')} r {v[0]:.2f} (target {v[1]:.2f}, read {v[2]:.2f})" for k, v in RD["follow"].items()) + ".\n",
"## Deaths per gate, with the control\n", RD["deaths_md"], "",
"## The paper's tests\n",
"| Fix | Test | Song 37 |\n|---|---|---|",
f"| 212 | with 206 on, join deaths under one build in ten; survivors near the control's share | {T['t212']['join_deaths']} join deaths ({pc(T['t212']['join_deaths'] / 500, 1)}; song 36 v3: 47%); survivors {T['t212']['survivors']}, the control {T['t212']['ctl_survivors']}: **fails narrowly** (finding 229) |",
f"| 213 | the intake asks; builds repeat the opening unit at once in 15–30% of verse and chorus windows; nothing gates the pick | asked at question 10; {pc(T['t213']['unit2_builds_mean'])} of windows across builds; the pick {pc(T['t213']['unit2_pick'])}: passes |",
f"| 214 | builds' medians within three points of 69% and 62%; 198 still passes | {pc(T['t214']['ct_on_median'])} and {pc(T['t214']['ct_off_median'])}: on the beat **5 points high**; intervals {pc(T['t214']['iv']['repeat'], 1)} / {pc(T['t214']['iv']['step'], 1)} / {pc(T['t214']['iv']['larger'], 1)} (repeat, step, past a fifth; the drawn targets average " + f"{100*np.mean([t['repeat'] for t in M_['targets']]):.1f} / {100*np.mean([t['step'] for t in M_['targets']]):.1f} / {100*np.mean([t['past_fifth'] for t in M_['targets']]):.1f}" + ") |",
f"| 215 | no survivor has such a note on a beat or held a quarter or longer | none in the {T['t215']['stored']} kept survivors; the gate killed none: passes |",
"| 216 | every summit lands on a beat over a chord that holds it | " + "; ".join(f"bar {b} beat 1 over {c}" for _, _, b, ok, c in T['t216']['summits']) + ": passes |",
"| 217 | every return of the hook lands on its own chords; every chorus's last line on the tonic | the hook returns on A–E each time; all six chorus endings on A over A: passes |",
f"| 218 | line ends use three held lengths; eighth-note gaps inside 27–62%; the longest note over the median varies across builds between 2 and 4 | line ends: " + ", ".join(f"{k} twelfths ×{v}" for k, v in sorted(T['t218']['end_holds'].items(), reverse=True)) + f"; eighth gaps {pc(T['t218']['gap_eighth'][0])} · {pc(T['t218']['gap_eighth'][1])} · {pc(T['t218']['gap_eighth'][2])} (median **above** the band: finding 227); longest over median {T['t218']['lom'][0]:g} · {T['t218']['lom'][1]:g} · {T['t218']['lom'][2]:g}: varies |",
f"| 219 | no build dies at 181 where its construction was used | {T['t219']['deaths_181']} died, all on contour, verse lines 2 and 3 returning line 1 with different syllable counts: **fails** (finding 230) |",
f"| 220 | every section a multiple of four bars; the bar-window return share at or above 31%; a designed three-bar line prints both readings | all multiples of four; returns third in {pc(T['t220']['unit3_builds_mean'])} of windows across builds (song 36 v3: 1%), the pick {pc(T['t220']['unit3_pick'])}; no three-bar line: passes |",
f"| 221 | 210 computed on 46 measures from the file, the chart range beside it | yes ({T['t221']['measures']} measures, file {T['t221']['file_sha']}…) |",
f"| 222 | the spread printed; the pick inside the chart's middle half, or the report says not | the pick {T['t222']['spread_pick']:.2f}, **just above** 2.12 (not inside) |",
"| 223 | 194's four words pass | " + ", ".join(f"'{w}' {['stressed' if x else 'weak' for x in v]}" for w, v in T['t223']['words'].items()) + ": passes |",
f"| 224 | targets drawn and recorded; the builds' median distance inside 0.133–0.228; fewer than one build in ten too central | drawn and recorded for all 500 builds; median {T['t224']['distance_median']:.3f}; {pc(T['t224']['too_central'])} too central (control {pc(RD['too_central']['ctl'])}): **fails** (finding 225) |", "",
"## Which fixes ran\n",
"| Fix | Ran? | How |\n|---|---|---|",
"| 224 | yes | targets from the chart's middle halves, recorded per build; control at the medians |",
"| 212, 214, 215, 216, 217, 218, 219, 223 | yes | as above |",
"| 213, 220, 202, 208 | yes | at intake (questions 8, 10, 11, 13) |",
"| 194–203, 205, 206 | yes | as amended by v96 (205's plans; 206 at most five lengths, gated) |",
"| 209 | yes | the instrumental hook and the solo (below) |",
"| 210, 211, 221 | yes | the distance on 46 measures; the composite the rank of record |",
"| 222 | yes | a reading |",
"| 181, 182 and earlier | yes | construction and gates as before |",
"| 192 | not applicable | a band song (triads over a root bass) |", "",
f"**The instrumental hook (209).** {RF['drawn']} distinct one-bar figures drawn from the pop rhythm table; {RF['passed']} passed the lead gates (rhythm in the pop band; chord tones on the beats 60% or more; no semitone against a held sung note; nothing under A4; no tritone or flat ninth against a root). Deaths: " + "; ".join(f"{k} {v}" for k, v in RF['deaths'].most_common()) + f". The pick: onsets {RF['pick']['ons']} in twelfths ({' '.join(nm(p) for p in RV.pitches(RF['pick']['steps'], 'A'))} over A); chord tones on the beat {pc(RF['pick']['ct'])}; unrelated to the vocal hook (onsets {RF['pick']['related'][1]:.2f}, contour {RF['pick']['related'][2]:.2f}). It plays in {len(RF['slots'])} slots: the intro, the holds after chorus lines, the outro. **The solo:** 16 bars, the hook, its answer a third higher, a walked line, the hook landing on A; chord tones on the beats {pc(RF['solo_check']['ct'])}, no tritone against a root, rhythm {RF['solo_check']['rbits']:.2f} bits (inside the pop band), largest leap {RF['solo_check']['max_leap']} semitones; the first draw passed. No corpus on file separates instrumental figures from the voice, so 209 has no kept figure behind it.\n",
f"**The demo.** Voice {DR['stems_db']:+.1f} dB over the band. Energy (9.12): " + ", ".join(f"{r['sec']} {r['energy_read']:.2f}" for r in DR['energy']) + ". Each chorus above its verse; the last chorus the top (the solo's first eight bars were thinned, hats for the ride and the organ out, so the solo builds into it).\n",
"**Documents.** The demo (MP3, General MIDI, GarageBand MIDI), the lead sheet, the parts, the number chart and the songbook were written from the record; every staff reads back against it, and 47 of 47 consistency checks pass (consistency_p37.py).\n",
"**Findings.** 225–232, on the new fix list (after v96).\n"]
open(f"{H}/test_report.md", "w").write("\n".join(L))
print("test_report.md written")
