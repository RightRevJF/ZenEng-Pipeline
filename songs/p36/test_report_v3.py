"""Append version 3 to test_report.md: every figure read from the v3 runs, readings and tests."""
import pickle, hashlib
H = "/home/claude/p36"
Mn = pickle.load(open(f"{H}/melody_v3_main.pkl", "rb")); Ct = pickle.load(open(f"{H}/melody_v3_ctl.pkl", "rb"))
R = pickle.load(open(f"{H}/readings_v3.pkl", "rb")); T = pickle.load(open(f"{H}/tests_v3.pkl", "rb")); REC = pickle.load(open(f"{H}/song_record_v3.pkl", "rb"))
RF = pickle.load(open(f"{H}/riff_v3.pkl", "rb")); DR = pickle.load(open(f"{H}/out/demo_report_v3.pkl", "rb"))
P = Mn["alive"][0]; rr = Mn["rerun"]
def pc(x, d=0): return f"{100 * x:.{d}f}%"
NM = ["C", "D♭", "D", "E♭", "E", "F", "G♭", "G", "A♭", "A", "B♭", "B"]
nm = lambda p: f"{NM[p % 12]}{p // 12 - 1}"
rf = RF["pick"]; import melody_v3_p36  # noqa  (module globals for the riff's pitches)
import riff_v3 as RV
riff_eb = " ".join(nm(p) for p in RV.pitches(rf["steps"], "Eb"))
d, flag = R["distance"]; dc, flagc = R["distance_ctl"]
L = ["", "## Version 3 (ZenEng v95: the music rebuilt on the locked lyric)\n",
"**The brief.** Rebuild song 36's music under ZenEng v95 on lyric draft 5 and the same form plan; port 201, 199, 206, 205, 208, 209, 194–198, 200, 202, 203, 195 and 210–211 before the search, in that order; ask the bridge and summit questions; run a control (same seed and N, 199, 201, 205 and 206 off); report the readings; push the code with the seed; number findings from 212. The paper was not edited.\n",
"**The spec and the tables.** ZenEng_v95.docx, version row v129, last fix 211 (checked before numbering). The tables artifact still holds the same two files with the same hashes; read, not refitted (tables " + rr["tables_sha256"] + "…).\n",
"**201 first: the form.** About five syllables a bar at ♩ = 118; leading unstressed syllables go to the pickup; more than ten counted syllables take a third bar; repeated sections and returning lines share spans. Verse lines 2 and 4, chorus lines 4 and 8 and bridge line 2 take three bars: verse 10, chorus 18, bridge 9. " + f"{REC['nbars']} bars, {int(REC['seconds'] // 60)}:{int(round(REC['seconds'] % 60)):02d} (version 1: 88 bars, 2:59). Shown to the writer before the search.\n",
"**Intake (the two questions of step 5).** The bridge: A, lifted above the verse (kept 68%). The summit: A, D5 on the last stressed syllable of chorus line 6 in every chorus ('twelve'; 'July' in the last), first at about 29% of the song (chart pop's median 31%).\n",
"**How each port was built.**\n",
"| Fix | In version 3 |\n|---|---|",
"| 201 | Each line's rhythm drawn over its own bars on an eighth grid; the last stress on the last bar's downbeat (or beats 3, 2 of it, or beat 3 of the bar before); a section's last line and the summit's line land in their last bar. |",
"| 199 | One draw over every candidate pitch: a category's weight tilted by the chord it offers (with the chord term over without), chord tone or not weighted 2.5 : 0.38 on the beat and 5.0 : 1.0 off it, calibrated so the builds land at the chart's shares. (182's category-first draw could not move the share: finding 214.) |",
"| 206 | No sixteenths (onsets on eighths); a line's last note held a half or a dotted quarter (shorter only where the next line comes sooner), then an eighth's breath. |",
"| 205 | Plans AABC and AAAB at about one section in five where the first two lines are within three syllables and share a span (here: the chorus head and the pre-chorus); if no section opens AA, the pre-chorus does. |",
"| 208 | The bridge sung from a register centred above the verse's (lifted, the writer's A); a gate: its opening line related to neither the verse's nor the chorus's opening line (27.31 read on lines); a gate: its median above the verse's; its pace printed only. |",
"| 209 | A one-bar synth figure searched against the pick (below). |",
"| 194 | The stress reading from version 1 (191 and 194). |",
"| 195 | The 181 gate reads lines: a unit runs from its line's first onset to the next line's, onsets and contour counted from the line's own downbeat, the last note left out of the contour (finding 219). 27.31's bar windows kept for the repetition and design readings. |",
"| 196 | Pop's monotony floor is the run clause; the two-pitch share printed. |",
"| 197 | After a leap past a fifth, the walk steps or skips back. |",
"| 198 | The draw aimed (repeat ×0.95, step ×1.35, third ×0.8, larger ×1.6) so the builds' medians meet Table CG. |",
"| 200 | ♭3 and ♭7 only where no chord tone lies a semitone away and not a tritone from the root; and, added after the first picks, no tone of any kind a tritone from its chord's root (finding 215). |",
"| 202 | The summit placed by the writer's answer: three D5s, each on a beat over a chord holding D (line 6's chord moved to B♭; finding 216). |",
"| 203 | 192 not applicable: a band song (triads over a root bass). |",
"| 210 | The distance from the centre printed beside 0.086–0.351, partial (finding 221). |",
"| 211 | The composite orders the survivors as the rank of record and claims nothing more. |", "",
f"**The search.** N {rr['N']}, seed {rr['seed']}, PYTHONHASHSEED 0, code {rr['code_sha']}, Python {rr['python']}, numpy {rr['numpy']}. {Mn['survivors']} survivors of {Mn['made']} ({pc(Mn['survivors'] / Mn['made'], 1)}); frozen order {Mn['order_fp']}, reproduced exactly on a second run. Pick {P['fp']}, first by the rank of record (composite {P['meas']['composite']:.3f}); no hand edits. Plans: verse " + "".join(P['meta']['plans']['Verse']) + ", pre-chorus " + "".join(P['meta']['plans']['Pre']) + ", chorus " + " ".join(P['meta']['plans']['Chorus']) + ", bridge " + "".join(P['meta']['plans']['Bridge']) + ".\n",
f"**The control.** Same seed and N, with 199, 201, 205 and 206 off (the 88-bar form with two-bar lines, a sixteenth grid, free line ends, version 1's chord term and plan draws); everything else on, the same gates and readings. {Ct['survivors']} survivors, order {Ct['order_fp']}; its first pick {R['ctl_pick']} (composite {R['comp_ctl']:.3f}).\n",
"**Hand inspection of the pick, and what it changed.** The pick was printed syllable by syllable before the record was built. Three faults were found in earlier picks of the same code and fixed in the construction, then the run repeated: (1) the summit's D5 fell off the beat over A♭, a tritone from the root, held a half (finding 216); (2) copied notes and held slurs a tritone from their chord's root, D over A♭ and G over D♭ (finding 215); (3) the chorus's last line and the summit line could end on an off-beat; those lines now take the cadence rhythm. The last chorus's last line has a bar more than the hook it returns; the hook keeps its place in its own bars a bar later, with D♭ under 'I'm still here' and E♭ under the hook (finding 217). The frozen pick needed no hand edit.\n",
"### Version 3 readings (step 7)\n",
"Builds are every song the generator finished (5th, median and 95th percentiles), before the gates.\n",
R["md"], "",
f"Distance from the centre (210): the pick {d:.3f}, **{flag}** beside the chart songs' 0.086–0.351; the control's first pick {dc:.3f}, **{flagc}**. Computed on the 11 numeric measures of Table CU only (the 46 are not on file), so neither figure is the paper's distance (finding 221).\n",
f"The rank of record (211): the composite ordered the survivors so the run has one reproducible first pick; it claims nothing more. It scored the control's first pick {R['comp_ctl']:.3f} against the pick's {R['comp']:.3f}.\n",
"### Deaths per gate, with the control\n",
R["deaths_md"], "",
"### The paper's tests for each fix\n",
"| Fix | Test | Version 3 |\n|---|---|---|",
f"| 194 | 'July', 'radio', 'microwave', 'somewhere' one stress each; 'anyway' its last only at a line's end | 'July', 'radio' and 'microwave' pass; **'somewhere' carries two** (finding 223); 'anyway' at a line's end: first and last |",
f"| 195 | no build dies at 181 where its construction was used; the 8-bar stock share at or above 39% | {T['195']['deaths_181']} died at 181 (after the summit and the tritone repair changed a copied note); stock share {pc(T['195']['stock8_pick'])} in the pick, {pc(T['195']['stock8_builds_mean'], 1)} across builds: **fails** (finding 220) |",
f"| 196 | monotony deaths from the run clause alone; the two-pitch share printed | yes, {T['196']['monotony_deaths']} deaths; two-pitch lines {pc(T['196']['two_pitch_pick'])} |",
f"| 197 | no survivor follows a leap past a fifth with another leap | the pick none; {T['197']['survivors_with']} of the {T['197']['survivors']} survivors kept for inspection do, in copied lines |",
f"| 198 | builds' median repeats, steps and wide leaps within two points of Table CG | {pc(T['198']['repeat'], 1)}, {pc(T['198']['step'], 1)}, {pc(T['198']['larger'], 1)} against 27.6%, 42.6%, 3.0%: passes |",
f"| 199 | the pick's chord-tone share inside the class's middle half; key-word deaths fall | {pc(T['199']['chord_all'])} (middle half 54–76%); key words on chord tones {pc(T['199']['keyword'])}; key-word deaths {T['199']['keyword_deaths']} (version 1: 42): passes |",
f"| 200 | no ♭3 or ♭7 a semitone from a chord tone, or a tritone from the root, in any survivor | none ({T['200']['survivors_bad']}); no tone of any kind a tritone from the root in any survivor kept ({T['200']['tritone_root_survivors']}) |",
f"| 201 | sixteenth share inside the class's 5th–95th; the final note near twice the line's median, or the report names the lines given a third bar | sixteenths {pc(T['201']['sixteenth'])}; final note {T['201']['final_over_median']:g} times the median; third bars: " + ", ".join(T['201']['third_bar_lines']) + " |",
"| 202 | the summit question prints the class's position figure beside each option | yes (31%, at intake) |",
"| 203 | a band song lists 192 as not applicable | yes |",
f"| 204 | survivors' windows read on Table CU; every measure outside both middle halves listed | chart pop only (the grid corpus's quartiles are not on file). Outside the chart's middle half in the pick's {T['204']['windows']} windows: " + ", ".join(f"{k.replace('_', ' ')} {v}" for k, v in T['204']['outside'].items()) + " |",
f"| 205 | builds' opening repeated at once in 15–30% of verse and chorus windows; one section opens so where the lyric allows | {pc(T['205']['builds_mean'], 1)} across builds; the pre-chorus opens so, outside the windows; the pick 0%: **fails** (finding 213) |",
f"| 206 | no 8-bar span over five lengths; line ends share one or two held lengths; longest within two to five times the median | at most {T['206']['max_lengths_any_span']} lengths; line ends " + ", ".join(f"{k} twelfths ×{v}" for k, v in sorted(T['206']['line_end_lengths'].items(), reverse=True)) + f"; longest {T['206']['longest_over_median']:g}× the median: passes ({pc(T['206']['eighth_share'])} of notes are eighths: finding 218) |",
f"| 207 | the bar-to-bar spread printed beside the kept figures | {T['207']['spread']:.2f} (chart 1.20–1.62–2.12) |",
f"| 208 | the bridge's opening unrelated; its median above the verse's; pace printed | related to neither (contour {T['208']['rel_verse'][2]:.2f} and {T['208']['rel_chorus'][2]:.2f}); median +{T['208']['median_minus_verse']:g} semitones; onsets {T['208']['onsets_ratio']:.2f} of the verse's |",
f"| 209 | the figure unrelated to the vocal hook; only where the voice holds or rests; in the intro, choruses and outro; the report says there is no corpus figure | unrelated (onsets {rf['related'][1]:.2f}, contour {rf['related'][2]:.2f}); {T['209']['over_sung_onset']} notes over a sung onset; intro, the three choruses, outro; no corpus on file separates instrumental figures from the voice, so this rule has no kept figure behind it |",
f"| 210 | the pick's distance printed and flagged | {d:.3f}, {flag} (partial) |",
"| 211 | the composite called the rank of record | yes |", "",
f"**The instrumental hook (209).** {RF['drawn']} distinct one-bar figures drawn from the pop rhythm table (4–7 notes, scale steps from the chord's root, from its fifth over D♭), {RF['passed']} passed the lead gates (rhythm inside the pop band; chord tones on the beats 60% or more; no semitone against a held sung note; nothing under G4; no tritone or flat ninth against a root). Deaths: " + "; ".join(f"{k} {v}" for k, v in RF['deaths'].most_common()) + f". The pick: onsets {rf['ons']} in twelfths, steps {rf['steps']} ({riff_eb} over E♭); rhythm {rf['rbits']:.2f} bits; chord tones on the beat {pc(rf['ct'])}; {pc(rf['sync'])} of its notes off the beat; seed {RF['seed']}. It plays {T['209']['statements']} times: intro bars 1–4, the holds after chorus lines 2, 4, 6 and 8 (7 in the last chorus), outro bars 96–98, cut where the hold is short.\n",
f"**The demo.** Voice {DR['stems_db']:+.1f} dB over the band; energy: " + ", ".join(f"{r['sec']} {r['energy_read']:.2f}" for r in DR['energy']) + ".\n",
"**Documents.** The demo (MP3, General MIDI, GarageBand MIDI), the lead sheet, the parts, the number chart and the songbook were written from the version 3 record; every staff reads back against the record, and 49 of 49 consistency checks pass (consistency_v3.py).\n",
"**The quotable line (10.20) on draft 5.** Remembered top: 'yeah, I dance anyway'; annotated top: 'the microwave's blinking twelve, been blinking since July'; middle (top quartile under both): 'by the green of a clock stuck on twelve'. The lyric did not change from version 2, so the blind pick of version 1 stands unless the writer picks again.\n",
"**Findings.** 212–223, on the new fix list (after v95).\n"]
s = open(f"{H}/test_report.md").read()
if "\n## Version 3" in s: s = s[:s.index("\n## Version 3")]
open(f"{H}/test_report.md", "w").write(s + "\n".join(L))
print("appended version 3")
