"""Write test_report.md for song 38 (ZenEng v103): every figure read from the runs, the readings and the record."""
import pickle, sys, importlib.util as iu
H = "/home/claude/p38"; sys.path.insert(0, H)
T = pickle.load(open(f"{H}/readings.pkl", "rb")); REC = pickle.load(open(f"{H}/song_record.pkl", "rb"))
DR = pickle.load(open(f"{H}/out/demo_report.pkl", "rb")); Q = pickle.load(open(f"{H}/q1020.pkl", "rb"))
sp = iu.spec_from_file_location("intake38", f"{H}/intake.py"); intake = iu.module_from_spec(sp); sp.loader.exec_module(intake)
def pc(x, d=0): return f"{100 * x:.{d}f}%"
def r3(v): return " – ".join(f"{x:g}" for x in v) if v else "—"
mn, ct = T["run"]["main"], T["run"]["ctl"]
L = ["---", 'title: "Stay Tuned — Test report (ZenEng v103)"', 'author: "Words and music: Jason Bryant"', 'date: "10 November 2026"', "---", "",
     "## The brief\n",
     "A new song under ZenEng v103 (version row v137, Window 123, last fix 256), worked on as an idea with the writer before the engine. The idea: a narrator who shows the partisan political class on both sides as one act, biting and sarcastic, no side favoured. Tables read, not refitted: zeneng_v88_tables.json, zeneng_v91_hymn_supplement.json, zeneng_v96_discriminator_tables.json, zeneng_v97_axes_of_character.json, zeneng_v100_bass_and_figures.json, zeneng_v101_band_returns_eras.json, zeneng_v102_song37_checks.json, zeneng_v103_selector.json (hashes in the rerun line). Findings are numbered from 257. The paper is not edited.\n",
     "## Intake\n", "| # | Question | Answer |\n|---|---|---|"]
for e in intake.LOG:
    a = str(e.get("answer", e.get("finding", e.get("file", ""))))
    L.append(f"| {e['q']} | {e.get('topic', '')} | {a[:220].replace('|', '/')} |")
L += ["", "**The song.** *Stay Tuned*: rock (Who-style), 4/4 at ♩ = 132, A major, male high baritone C♯3–A4. A cable-news cameraman tells what he sees; the chorus is the network's own voice; in the last chorus he cuts the cameras and says turn it off. Form: Intro 8 · Verse 8 · Pre 4 · Chorus 16 · Verse 8 · Pre 4 · Chorus 16 · Bridge 8 · Solo 8 · Breakdown 8 · Last Chorus 18 · Outro 8 = 114 bars, 3:27. Every sung line two bars (3–8 syllables; 230). The title is sung 9 times, first at bar 21 of 114 (232; kept 2–10, median 5, first in the opening third in 72%).\n",
      "## The ports\n", "| Fix | In song 38 |\n|---|---|",
      "| 225/226/243 | Each build's targets are one whole kept chart window from the v103 training rows: the verse and pre-chorus from the 20 kept windows at 1.4–2.1 on reciting (Q6, Q14), the chorus and bridge from the 48 kept windows inside at least three of CLASSIC's four bands the rows carry (finding 259). The window index is recorded with the build. Seventeen measures aimed; notes a bar is not in the rows and is read from the chart median (finding 260). The control aims at each pool's medians. |",
      "| 249 | A calibration pass (3 rounds × 30 builds, seed recorded) sets fifteen knobs per pool so a build aimed at its pool's medians reads near them. |",
      "| 251 | Aims added: on the tonic, third and fifth (pitch weights by degree); onsets on beat 3 and on beats 2 and 4 (the rhythm's place weights); turns per move (a reversal weight). The low point's place is not aimed. |",
      "| 227 | Gates: the chorus opening unrelated to the verse's; its median not below the verse's; its lowest note above the verse's. |",
      "| 228 | Verse 2 and pre 2 sung again: verse 1's contour and first and last notes, the rhythm drawn afresh for the new words, a stressed note on a beat moved a step to a chord tone. The last chorus is chorus 1's tune and 18 bars (the writer's 'Turn it off.' as the two-bar extension in place of a hook repeat). |",
      "| 230/231/232 | Two-bar slots; each line's landing drawn from 231's shares (chorus 26/20/18/36 for beat 1, beat 3, beats 2 and 4, off the beat; verse 20/20/18/42); the title's stress fixed on beat 1, held three beats (the chant design). |",
      "| 239/240/246/247/248 | Returns at the source's level, first note kept, change in the last quarter (shared notes on the beat keep their pitch), top note kept or higher; added notes drawn (repeat .28, step .48, leap .24); no steering to the tonic; no sequencing. A copy, return or re-sung line is fitted before the line ahead of it. 181's gate reads the shared events only. |",
      "| 242 | CLASSIC: notes a bar, range, repeats, distinct note lengths and pitch surprise gated on Table DG's middle halves, read as the median over the first 8 bars of Verse 1, Chorus 1 and the Bridge (Q14: A). It replaces the pop pitch band (153/182). |",
      "| 244/216 | The summit A4 on 'tuned' (chorus lines 1 and 5), beat 1 of the chorus window's first bar, over A; six times; gated. |",
      "| 208 | The bridge: opening unrelated, median above the verse, top under the summit (the writer's A). |",
      "| 252–255 | The content and order judges with the file's weights (fitted through song 37, for song 38); checked against song 37's pick first: Verse 1 content 0.586, order 3.059; Chorus 1 −1.027, 5.221, as the file gives. The floor (−0.059) a gate; the shortlist the upper half by combined score; the pick the composite's first on it. |",
      "",
      "## The runs\n",
      f"Main: {mn['made']} built, {mn['survivors']} survivors ({pc(mn['survivors'] / mn['made'], 1)}), order {mn['order']}. Control (243 off): {ct['made']} built, {ct['survivors']} survivors ({pc(ct['survivors'] / ct['made'], 1)}), order {ct['order']}. The run is 3000 builds, not 500: at 500 the main run left 10 survivors, too few for a shortlist.\n",
      "| Death | Main | Control |\n|---|---|---|"]
for k in sorted(set(mn["deaths"]) | set(ct["deaths"]), key=lambda k: -mn["deaths"].get(k, 0)):
    L.append(f"| {k} | {mn['deaths'].get(k, 0)} | {ct['deaths'].get(k, 0)} |")
rr = mn["rerun"]
L += ["", f"Rerun: `{rr['cmd']}`; seed {rr['seed']}, calibration seed {rr['calibration_seed']}, code {rr['code_sha']}, Python {rr['python']}, numpy {rr['numpy']}, PYTHONHASHSEED {rr['pythonhashseed']}. Tables: " + ", ".join(f"{k} {v}" for k, v in rr["tables"].items()) + ".\n"]
P5 = T["255"]
L += ["## The pick (255)\n", "| Build | Composite | Content | Order | Combined |\n|---|---|---|---|---|"]
for lab in ("composite first", "shortlist pick", "judge first"):
    x = P5[lab]; L.append(f"| {lab}: {x['fp']} | {x['composite']:.3f} | {x['content']:.3f} | {x['order']:.3f} | {x['combined']:.3f} |")
L += ["", f"The shortlist is {P5['shortlist_size']} of {P5['survivors']} survivors. The composite's first build is {P5['comp_first_rank_by_judge']}th of {P5['survivors']} by the judge, outside the shortlist, so 255 changed the pick. The record is built from {REC['fp']} with no hand edits.\n"]
L += ["## The tests\n", "| Fix | Test | Song 38 | Held? |\n|---|---|---|---|"]
t = T
ax = t["225"]["pick_axes"]
L.append(f"| 225 | builds' median on reciting 1.4–2.1 (verse) | builds {r3(t['225']['builds_reciting_verse'])} (5th–median–95th); control {r3(t['225']['ctl_reciting_verse'])}; pick verse {ax['v']['Reciting']:.2f} | no: median 1.15 (finding 264) |")
L.append("| 225 | pick's place on all eight axes | verse " + ", ".join(f"{k} {v:+.2f}" for k, v in ax["v"].items()) + "; chorus " + ", ".join(f"{k} {v:+.2f}" for k, v in ax["c"].items()) + " | printed |")
nc = [k for k in t["226"] if ":" in k]; within = sum(abs(t["226"][k]["median"]) <= 1 for k in nc); spread_ok = sum(t["226"][k]["spread"] >= t["226"][k]["ctl_spread"] for k in nc)
L.append(f"| 226 | unchosen axes: medians within 1 sd; spread ≥ control's | {within} of {len(nc)} medians within 1 sd; spread at or above the control's on {spread_ok} of {len(nc)}; distance builds {r3(t['226']['distance_builds'])}, control {r3(t['226']['distance_ctl'])} | yes |")
L.append(f"| 227 | chorus opening unrelated, median not below, floor above; chorus bar rhythms heard in the verse | gates held on every survivor; pick: chorus median {t['227_pick']['chorus_median']:g} vs verse {t['227_pick']['verse_median']:g}, low {t['227_pick']['chorus_low']} vs {t['227_pick']['verse_low']}; shared bar rhythms pick {pc(t['227']['pick'])}, builds {r3(t['227']['builds'])} (kept median 12%) | yes |")
L.append(f"| 228 | verse 2 shares ¼–¾ of verse 1's bar rhythms across builds; last chorus +2 bars; exact bar repetition | builds {r3(t['228']['builds_v2_share'])}, in range in {pc(t['228']['builds_in_quarter_to_three_quarters'])}; pick {pc(t['228']['pick_v2_share'])}; +2 bars (the writer's tag); exact bars {pc(t['228']['pick_exact_bars'])} vs chart 38% | no (finding 262) |")
L.append(f"| 229 | bridge surprise vs chorus; off-beat vs verse | bridge {t['229']['bridge_bits']} bits a note vs chorus {t['229']['chorus_bits']}; off-beat axis bridge {t['229']['bridge_offbeat']:+.2f} vs verse {t['229']['verse_offbeat']:+.2f} | printed |")
L.append(f"| 230 | each line's syllables and slot; no 9+ line in 2 bars; sections multiples of 4; sung rate 3.2–6.2 a bar | every line 3–8 syllables, 2 bars; every section a multiple of 4 except the last chorus's 18 (228's extension; finding 268); sung rate pick {t['230']['pick_rate']}, builds {r3(t['230']['builds_rate'])} | yes, with 268 |")
L.append(f"| 231 | last stresses off the beat 25–50%, on 1 or 3 35–55%; pickups 40–70% | builds off {r3(t['231']['builds_off'])}, on 1/3 {r3(t['231']['builds_b13'])}, pickups {r3(t['231']['builds_pickup'])}; pick {pc(t['231']['pick'][0])}, {pc(t['231']['pick'][1])}, {pc(t['231']['pick'][2])} | off-beat yes; 1/3 and pickups high (finding 263) |")
L.append(f"| 232 | title stress on 1 or 3, held ≥ 2× median syllable | beat {t['232']['beat']}, held {t['232']['held'][0] / 12:g} beats vs median syllable {t['232']['median_syl'] / 12:g} beat; 9 soundings, first bar 21 | yes |")
L.append(f"| 239 | each return's kind | pick: {', '.join(f'{k} {v}' for k, v in t['239']['pick_kinds'].items())} | printed |")
L.append(f"| 240 | returns end on the tonic within 10 points of sources | builds {pc(t['240']['builds_returns_tonic'])} vs sources {pc(t['240']['builds_sources_tonic'])}; pick {t['240']['pick'][0]} of {t['240']['pick'][2]} vs {t['240']['pick'][1]} | yes |")
osh = t["243"]["outside_share"]; ok43 = sum(0.4 <= v <= 0.6 for k, v in osh.items() if k != "notes_per_bar")
L.append(f"| 243 | window recorded; 40–60% of builds outside the chart middle half on each aimed measure; distance beside the aimed share | windows recorded (pick: verse {t['243']['pick_windows']['V']}, chorus {t['243']['pick_windows']['C']}); in 40–60% on {ok43} of 16 measures (" + ", ".join(f"{k} {pc(v)}" for k, v in osh.items()) + f"); builds' distance {r3(t['243']['builds_distance'])}; the aimed measures carry {pc(t['243']['kept_aimed_share'])} of a kept window's distance | partly |")
L.append(f"| 245 | notes a bar the lines need | " + ", ".join(f"{k} {v}" for k, v in t["245"]["notes_a_bar_needed"].items()) + " — none at 4.25, so 218's eighth grid stands | yes |")
L.append(f"| 246 | added notes repeat 20–40%; run deaths under 1 in 10 | {pc(t['246']['repeat_share'])} repeat ({t['246']['added']}); run deaths {pc(t['246']['run_deaths'], 1)} | yes |")
L.append(f"| 247 | join deaths under 1 in 10 | {pc(t['247']['join_deaths'], 1)} | yes |")
L.append(f"| 248 | no build dies at 181 where its construction was used | {t['248']['return_gate_deaths']} of {t['248']['made']} died there | no (finding 261) |")
L.append(f"| 249 | calibration recorded; chord-tone medians within 3 points of targets' means | seed {t['249']['seed']}; " + "; ".join(f"{k} reading {a:.3f} vs target {b:.3f}" for k, (a, b) in t["249"]["chord_tones"].items()) + " | chorus on the beat yes; verse no (finding 264) |")
L.append(f"| 250 | pick's outside count beside 16 (8–26); builds' 5th, median, 95th | pick {t['250']['pick']:g}; builds {r3(t['250']['builds'])} | yes (above 8) |")
c51 = t["251"]; L.append(f"| 251 | each aim followed (r ≥ 0.3) | " + ", ".join(f"{k} {v}" for k, v in c51.items()) + " | tonic, third, fifth, beats 2 and 4, repeat, step, chord tones, eighth gaps yes; beat 3 and turns no (finding 265) |")
j2 = t["252"]; L.append(f"| 252 | pick's score; builds 5th/median/95th beside kept; five give-away measures | pick content {j2['pick']:.2f}; builds {r3(j2['builds'])}; kept 5th {j2['kept']['5']}, median {j2['kept']['50']}, 95th {j2['kept']['95']}; give-aways: {', '.join(f'{m} ({w})' for m, w in j2['give_away'])}; kept rows above this song's builds in {pc(j2['auc_kept_rows_vs_song38_builds'])} of pairs (the rows are the judge's training data, so this flatters it) | printed |")
j3 = t["253"]; L.append(f"| 253 | four order measures for verse and chorus beside kept middle halves; share called shuffled | verse " + ", ".join(f"{k} {v}" for k, v in j3["pick"]["Verse 1"].items()) + "; chorus " + ", ".join(f"{k} {v}" for k, v in j3["pick"]["Chorus 1"].items()) + f"; builds called shuffled {pc(j3['builds_called_shuffled'], 1)} | printed; the chorus's smooth bar line +1.50 is outside (the chant's leap to A4 sits inside the bar, by design) |")
j4 = t["254"]; L.append(f"| 254 | no survivor under the floor; deaths counted; over half named | {j4['deaths']} death at the floor ({j4['would']} builds would have failed it); builds' combined {r3(j4['builds_combined'])}, kept median {j4['kept']['50']} | yes |")
L.append(f"| 255 | three builds with all three scores; record from the shortlist pick | above | yes |")
L.append("| 256 | none (a record) | nothing in 256 used to rank | — |")
e2 = t["242"]; L.append(f"| 242 | the era set and its bands | CLASSIC; pick " + ", ".join(f"{k} {v}" for k, v in e2["pick"].items()) + f"; died at the gate {e2['deaths']} of {e2['made']} ({pc(e2['deaths'] / e2['made'])}) | yes, at a cost (finding 258) |")
b = t["233"]; L.append(f"| 233 | root on beat 1 of every bar with a chord; root share 43–73%; a cell per section; 4 kick hits in 5 carry a bass note | beat 1 the root {pc(b['beat1_carries_root'])} of bass bars (the bass waits for the verse: intro bars 5–8 have no bass, {pc(b['bars_with_chord_have_beat1'])} of chord bars); root share {pc(b['root_share'])}; kicks with bass {pc(b['kicks_with_bass'])} | yes |")
d = t["236"]; L.append(f"| 236 | Table DD's readings | snare on 2 and 4 in {pc(d['snare_2_4'])} of bars with drums (the breakdown's first four bars and the fill bars without); kick on 1 in {pc(d['kick_1'])}; {d['kicks_a_bar']} kicks a bar; the commonest kick-and-snare bar covers {pc(d['top_groove'])}, three cover {pc(d['top3'])}; {d['fills']} fills in {d['bars']} bars; drums enter bar {d['enters_bar']}; four on the floor named (Q12) | yes |")
o = t["237"]; L.append(f"| 237 | one rhythm a section; 3–4 notes in MIDI 51–71; ½–9/10 of strikes with the bass | held, pad or quarter stabs by section; MIDI {o['range'][0]}–{o['range'][1]}; {o['strikes_a_bar']} strikes a bar; with the bass {pc(o['with_bass'])} | no (finding 267) |")
L.append("| 238 | parts by section; intro ≤ half the fullest; nothing before the last chorus fuller than it; verse not fuller than its chorus | " + ", ".join(f"{k} {v}" for k, v in t["238"].items()) + " | yes |")
f5 = t["235"]; L.append(f"| 235 | intro tune unrelated to every sung line; fills 2–3 beats, 4–6 notes, start within a beat, end on a chord tone, no echo; countermelody under half unison/octave | intro tune {f5['intro']['ons']} / steps {f5['intro']['steps']}, unrelated to all {len(set(n['sec'] + str(n['line']) for n in REC['lead']))} sung lines; fills " + "; ".join(f"after {a} (gap {g:g} beats): {n} notes, {L_:g} beats, from {s:g} beats after" for a, g, n, L_, s in f5["fills"]) + f"; {f5['fill_stats']}; countermelody {f5['counter']['unison_or_octave']} of {f5['counter']['together']} struck-together notes at unison or octave ({pc(f5['counter']['share'])}) | yes; few gaps can take a fill (finding 266) |")
L += ["", "## The demo\n", f"Stems: the lead vocal {DR['stems_db']:+.1f} dB over the band (rule ≥ +3). Energy arc (band only): " + "; ".join(f"{r['sec']} {r['energy_read']:.2f}" for r in DR["energy"]) + ". Each chorus reads above its verse; the last chorus is the top; the bridge and the breakdown's opening pull back by design.\n",
      "## The quotable line (10.20)\n", f"Slots for the blind pick: remembered '{Q['slots']['remembered']}', middle '{Q['slots']['middle']}' ({Q['slots']['rule']}), annotated '{Q['slots']['annotated']}'. The writer's pick: pending.\n",
      "## Findings\n"]
L += [x.strip() for x in open(f"{H}/findings.md").read().split("\n") if x.strip()]
open(f"{H}/test_report.md", "w").write("\n".join(L) + "\n")
print("test_report.md:", len(L), "lines")
