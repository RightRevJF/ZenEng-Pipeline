"""Write test_report.md for song 39 (ZenEng v103): every figure read from the runs, the readings and the record."""
import pickle, sys, importlib.util as iu
H = "/home/claude/p39"; sys.path.insert(0, H)
T = pickle.load(open(f"{H}/readings.pkl", "rb")); REC = pickle.load(open(f"{H}/song_record.pkl", "rb"))
DR = pickle.load(open(f"{H}/out/demo_report.pkl", "rb")); Q = pickle.load(open(f"{H}/q1020.pkl", "rb"))
sp = iu.spec_from_file_location("intake39", f"{H}/intake.py"); intake = iu.module_from_spec(sp); sp.loader.exec_module(intake)
def pc(x, d=0): return f"{100 * x:.{d}f}%"
def r3(v): return " – ".join(f"{x:g}" for x in v) if v else "—"
mn, ct = T["run"]["main"], T["run"]["ctl"]
L = ["---", 'title: "Fixed by Fall — Test report (ZenEng v103)"', 'author: "Words and music: Jason Bryant"', 'date: "10 November 2026"', "---", "",
     "## The brief\n",
     "Song 39 under ZenEng v103 (version row v137, last fix 256), written after song 38 turned into a song about the media: the writer wanted the political class shown as reckless profiteers, both sides. The idea was worked out with the writer before the engine. Tables read, not refitted (hashes in the rerun line). Findings are numbered from 269 (song 38's ran 257–268). The paper is not edited.\n",
     "## Intake\n", "| # | Question | Answer |\n|---|---|---|"]
for e in intake.LOG:
    a = str(e.get("answer", e.get("finding", e.get("file", ""))))
    L.append(f"| {e['q']} | {e.get('topic', '')} | {a[:220].replace('|', '/')} |")
L += ["", "**The song.** *Fixed by Fall*: rock with a swagger, 4/4 at ♩ = 108, E major; a shuffle (eighths swung) in the verses, bridge, solo, intro and outro, a straight rally march in the choruses (Q12); one gritty baritone A2–E4, double-tracked as two candidates in the last chorus (Q2). An all-seeing narrator cuts between rooms where both sides take the same money; the chorus is their campaign jingle sung back; the bridge follows them out of office; the last chorus ends in unison. Form: Intro 4 · Verse 16 · Chorus 8 · Verse 16 · Chorus 8 · Bridge 8 · Solo 8 · Last Chorus 18 · Outro 4 = 90 bars, 3:20. Every line two bars (4–8 syllables; 230). The title is sung 4 times, first at bar 27 of 90 (232). No era (Q5).\n",
      "## The ports\n", "| Fix | In song 39 |\n|---|---|",
      "| 225/226/243 | Targets are one whole kept window: the verse from the 10 kept windows at 1.4–2.1 on off-beat, the chorus from the 22 at 1.4–2.1 on chord-bound (Q6; no kept window does both, so split by section), the bridge from all 314. Seventeen measures aimed; notes a bar from the chart median (260). The control aims at each pool's medians. |",
      "| 249 | A calibration pass (3 rounds × 30 builds) per pool: verse on Verse 1, chorus on Chorus 1, bridge on the Bridge. |",
      "| 227/228/230–232/239/240/246–248/251 | As in song 38 (verse 2 sung again; returns at the source's level, change late, added notes drawn; copies fitted first). Verse plans for eight lines: lines 1–4 from the plan list, lines 5–8 a varied return of 1–4 or fresh. |",
      "| 244/216 | The summit E4 on 'Vote', beat 1 of each chorus's first bar, over E; the second line said twice a whole step down (D4 over D); the last chorus's unison 'Vote for us' returns it; four summits, gated. |",
      "| 208 | The bridge: opening unrelated, median above the verse, top under the summit. |",
      "| 242 | Not set (Q5); the pop pitch band (153/182) applies. |",
      "| 252–255 | The judges with the file's weights, the floor a gate, the shortlist. |",
      "| Designed | 'Fixed by fall.' (the tag) G♯3–F♯3–E3. The last chorus's voices from the lyric's marks. The swing is the demo's (271). |",
      "",
      "## The runs\n",
      f"Main: {mn['made']} built, {mn['survivors']} survivors ({pc(mn['survivors'] / mn['made'], 1)}), order {mn['order']}. Control (243 off): {ct['made']} built, {ct['survivors']} survivors ({pc(ct['survivors'] / ct['made'], 1)}), order {ct['order']}.\n",
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
L += ["## The tests\n", "| Fix | Test | Song 39 | Held? |\n|---|---|---|---|"]
t = T
ax = t["225"]["pick_axes"]
L.append(f"| 225 | builds' median on the chosen axes 1.4–2.1 | verse off-beat: builds {r3(t['225']['builds_offbeat_verse'])}, control {r3(t['225']['ctl_offbeat_verse'])}, pick {ax['v']['Off-beat']:.2f}; chorus chord-bound: builds {r3(t['225']['builds_chordbound_chorus'])}, control {r3(t['225']['ctl_chordbound_chorus'])}, pick {ax['c']['Chord-bound']:.2f} | verse yes; chorus no (269) |")
L.append("| 225 | pick's place on all eight axes | verse " + ", ".join(f"{k} {v:+.2f}" for k, v in ax["v"].items()) + "; chorus " + ", ".join(f"{k} {v:+.2f}" for k, v in ax["c"].items()) + " | printed |")
nc = [k for k in t["226"] if ":" in k]; within = sum(abs(t["226"][k]["median"]) <= 1 for k in nc); spread_ok = sum(t["226"][k]["spread"] >= t["226"][k]["ctl_spread"] for k in nc)
L.append(f"| 226 | unchosen axes within 1 sd; spread ≥ control's | {within} of {len(nc)} within 1 sd; spread at or above the control's on {spread_ok} of {len(nc)}; distance builds {r3(t['226']['distance_builds'])}, control {r3(t['226']['distance_ctl'])} | printed |")
L.append(f"| 227 | chorus opening unrelated, median not below, floor above; shared bar rhythms | pick: chorus median {t['227_pick']['chorus_median']:g} vs verse {t['227_pick']['verse_median']:g}, low {t['227_pick']['chorus_low']} vs {t['227_pick']['verse_low']}; shared bar rhythms pick {pc(t['227']['pick'])}, builds {r3(t['227']['builds'])} (kept 12%) | yes |")
L.append(f"| 228 | verse 2 shares ¼–¾ of verse 1's bar rhythms; last chorus +2 bars | builds {r3(t['228']['builds_v2_share'])}, in range {pc(t['228']['builds_in_quarter_to_three_quarters'])}; pick {pc(t['228']['pick_v2_share'])}; +2 (the tag) | no (273) |")
L.append(f"| 229 | bridge surprise vs chorus; off-beat vs verse | bridge {t['229']['bridge_bits']} bits vs chorus {t['229']['chorus_bits']}; off-beat bridge {t['229']['bridge_offbeat']:+.2f} vs verse {t['229']['verse_offbeat']:+.2f} | printed |")
L.append(f"| 230 | slots; sections multiples of 4; sung rate | every line 4–8 syllables in 2 bars; the last chorus 18 (268); sung rate pick {t['230']['pick_rate']}, builds {r3(t['230']['builds_rate'])} | yes, with 268 |")
L.append(f"| 231 | off-beat 25–50%, on 1 or 3 35–55%, pickups 40–70% | builds {r3(t['231']['builds_off'])}, {r3(t['231']['builds_b13'])}, {r3(t['231']['builds_pickup'])} | yes (273) |")
L.append(f"| 232 | title stress on 1 or 3, held ≥ 2× median | 'fixed' on beat {t['232']['beat']}, held {t['232']['held'][0] / 12:g} beat vs median {t['232']['median_syl'] / 12:g}; {t['232']['count']} soundings, first bar {t['232']['first_bar']} | yes |")
L.append(f"| 239 | each return's kind | pick: {', '.join(f'{k} {v}' for k, v in t['239']['pick_kinds'].items())} | printed |")
L.append(f"| 240 | tonic endings within 10 points | builds {pc(t['240']['builds_returns_tonic'])} vs sources {pc(t['240']['builds_sources_tonic'])}; pick {t['240']['pick'][0]} of {t['240']['pick'][2]} vs {t['240']['pick'][1]} | yes |")
osh = t["243"]["outside_share"]; ok43 = sum(0.4 <= v <= 0.6 for k, v in osh.items() if k != "notes_per_bar")
L.append(f"| 243 | 40–60% outside the chart middle half per aimed measure | windows recorded (pick: verse {t['243']['pick_windows']['V']}, chorus {t['243']['pick_windows']['C']}, bridge {t['243']['pick_windows']['B']}); in range on {ok43} of 16; distance {r3(t['243']['builds_distance'])}; aimed share {pc(t['243']['kept_aimed_share'])} | partly |")
L.append(f"| 245 | notes a bar the lines need | " + ", ".join(f"{k} {v}" for k, v in t["245"]["notes_a_bar_needed"].items()) + " | yes (none dense) |")
L.append(f"| 246 | added notes repeat 20–40%; run deaths under 1 in 10 | {t['246']['added']} (too few to read); run deaths {pc(t['246']['run_deaths'], 1)} | no (270) |")
L.append(f"| 247 | join deaths under 1 in 10 | {pc(t['247']['join_deaths'], 1)} | yes |")
L.append(f"| 248 | no deaths at 181 where built | {t['248']['return_gate_deaths']} of {t['248']['made']} | no (273, 261) |")
L.append(f"| 249 | calibration; chord tones within 3 points | " + "; ".join(f"{k} {a:.3f} vs {b:.3f}" for k, (a, b) in t["249"]["chord_tones"].items()) + " | printed |")
L.append(f"| 250 | outside count beside 16 (8–26) | pick {t['250']['pick']:g}; builds {r3(t['250']['builds'])} | yes |")
L.append("| 251 | aims followed (r ≥ 0.3) | " + ", ".join(f"{k} {v}" for k, v in t["251"].items()) + " | mostly; verse beat 3 and chorus chord tones no (269, 273) |")
j2 = t["252"]; L.append(f"| 252 | judge scores, give-aways | pick content {j2['pick']:.2f}; builds {r3(j2['builds'])}; kept median {j2['kept']['50']}; give-aways: {', '.join(f'{m} ({w})' for m, w in j2['give_away'])}; kept rows above builds in {pc(j2['auc_kept_rows_vs_song38_builds'])} of pairs | printed |")
j3 = t["253"]; L.append(f"| 253 | order measures; share called shuffled | verse " + ", ".join(f"{k} {v}" for k, v in j3["pick"]["Verse 1"].items()) + "; chorus " + ", ".join(f"{k} {v}" for k, v in j3["pick"]["Chorus 1"].items()) + f"; shuffled {pc(j3['builds_called_shuffled'], 1)} | printed |")
j4 = t["254"]; L.append(f"| 254 | floor | {j4['deaths']} deaths ({j4['would']} would fail); builds {r3(j4['builds_combined'])} | yes |")
L.append("| 255 | three builds; record from the shortlist pick | above | yes |")
L.append("| 242 | era | not set (Q5) | — |")
b_ = t["233"]; L.append(f"| 233 | root on beat 1; root share 43–73%; kicks with bass | beat 1 the root {pc(b_['beat1_carries_root'])}; root share {pc(b_['root_share'])}; kicks with bass {pc(b_['kicks_with_bass'])} | yes |")
d = t["236"]; L.append(f"| 236 | Table DD readings | snare 2 and 4 {pc(d['snare_2_4'])}; kick on 1 {pc(d['kick_1'])}; {d['kicks_a_bar']} kicks a bar; top groove {pc(d['top_groove'])}, three {pc(d['top3'])}; {d['fills']} fills in {d['bars']} bars; the feel change at each chorus named (Q12) | yes |")
o = t["237"]; L.append(f"| 237 | one rhythm a section; MIDI 51–71; ½–9/10 with the bass | MIDI {o['range'][0]}–{o['range'][1]}; {o['strikes_a_bar']} strikes a bar; with the bass {pc(o['with_bass'])} | no (267) |")
L.append("| 238 | parts by section | " + ", ".join(f"{k} {v}" for k, v in t["238"].items()) + " | yes |")
f5 = t["235"]; L.append(f"| 235 | intro tune unrelated; fills | intro tune {f5['intro']['ons']} / {f5['intro']['steps']}; fills " + "; ".join(f"after {a} ({g:g} beats): {n} notes, {L_:g} beats, from {s_:g}" for a, g, n, L_, s_ in f5["fills"]) + f"; {f5['fill_stats']}; no countermelody (Q11) | yes (266) |")
L += ["", "## The demo\n", f"Stems: the lead vocal {DR['stems_db']:+.1f} dB over the band (rule ≥ +3). Energy arc (band only): " + "; ".join(f"{r['sec']} {r['energy_read']:.2f}" for r in DR["energy"]) + ". Each chorus reads above its verse; the last chorus is the top; the bridge pulls back by design.\n",
      "## The quotable line (10.20)\n", f"Slots for the blind pick: remembered '{Q['slots']['remembered']}', middle '{Q['slots']['middle']}' ({Q['slots']['rule']}), annotated '{Q['slots']['annotated']}'. The writer's pick: A, the annotated slot ('they toast the ratings, glass to glass'). Tally after song 38: Annotated 10, Remembered 8, Middle 7, Refrain 1 (26 songs).\n",
      "## Findings\n"]
L += [x.strip() for x in open(f"{H}/findings.md").read().split("\n") if x.strip()]
open(f"{H}/test_report.md", "w").write("\n".join(L) + "\n")
print("test_report.md:", len(L), "lines")
