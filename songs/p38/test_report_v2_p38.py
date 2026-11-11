"""Song 38 rerun under v107 (v2): the test report, written from the three runs, the readings and the v2 record. test_report_v2.md."""
import sys, json, pickle
sys.argv = ["x", "1", "B"]; sys.path.insert(0, "/home/claude/p38")
import melody_v2_p38 as P
H = "/home/claude/p38"; R = json.load(open(f"{H}/readings_v2.json")); TB = json.load(open(f"{H}/tableb_v2.json"))
RUN = {v: pickle.load(open(f"{H}/melody_v2_{v}.pkl", "rb")) for v in "ABC"}; RF = pickle.load(open(f"{H}/riff_v2_p38.pkl", "rb"))
pB = RUN["B"]["pick"]; rr = RUN["B"]["rerun"]
def f3(x): return "—" if x is None else (f"{x:.3f}".rstrip("0").rstrip(".") if isinstance(x, float) else str(x))
def trio(v): return "—" if not v else " · ".join(f3(x) for x in v)
def pc(x): return f"{100 * x:.1f}%"
md = []
A = md.append
A("# Stay Tuned: the rerun under ZenEng v107 (test report)\n\n*Song 38, a regression run for debugging · Words and music: Jason Bryant*\n")
A("The locked lyric, every intake answer, the form (114 bars, 3:27), A major, ♩ = 132 and the chords are song 38's as written under v103. "
  "No intake question was asked. The judges' weights are the selector file's, fitted through song 37, not refitted, so the scores compare with the first run. "
  "Every v1 file is kept; the new code and outputs sit beside them as v2. The paper was not edited. Findings are numbered from 286.\n")
A("Read first: Modules 27.48 to 27.51 (fixes 257–285) and four tables, read and not refitted: zeneng_v104_line_in_time.json (43325ed4…), "
  "zeneng_v105_kept_windows.json (3633a24e…), zeneng_v105_song38_checks.json (69cbe713…), zeneng_v106_gate_limits.json (ca3e6a8b…).\n")
A("Design gates in force (the writer's choices at intake; fix 278): the summit A4 on 'tuned' (216, 244) and the bridge's register (208, question 10). Nothing else in 278's list killed a build.\n")
A("## The three runs\n")
A("- **Run A, gates only:** the v1 generator with 276 and 277 (eight limits; a build dies on a hard limit or its third soft break), 278 (comparisons are aims), 270 (the walk's ban on a fourth repeat lifted, and the repair step's re-walk of runs removed), 264 (the era gate) and 267 (the return gate).")
A("- **Run B, full v107:** Run A plus 265 and 266, 257, 258, 259, 260 with 269, 262, 268, 281, 282 (the writer's addition), 271 as amended by 285, and 272–274.")
A("- **Run C, control:** Run B with 243 off (each build aimed at its pool's medians).\n")
A(f"3,000 builds each; seed {rr['seed']}, calibration seed {rr['calibration_seed']}, PYTHONHASHSEED 0; code {rr['code_sha']}; Python {rr['python']}, numpy {rr['numpy']}. "
  f"Each run made twice. Rerun line: `PYTHONHASHSEED=0 python3 melody_v2_p38.py 3000 A|B|C`. Every build is on file, dead or alive: fingerprint, notes, cause of death, soft breaks and the judge's three scores (`every` in melody_v2_A/B/C.pkl). "
  "Builds that died while being made keep their partial notes; they have no judge scores, since their Verse 1 and Chorus 1 windows are incomplete.\n")

A("## 1. Survivors and frozen orders\n")
A("| Run | Survivors | Frozen order | Second run | Reproduced |\n|---|---|---|---|---|")
for v in "ABC":
    x = R["1"][v]; A(f"| {v} | {x['survivors']} of 3,000 ({pc(x['share'])}) | {x['order']} | {x['rerun_order']} | {'yes' if x['reproduced'] else 'no'} |")
A(f"| v1 (v103) | {R['1']['v1']['survivors']} of 3,000 (1.4%); control {R['1']['v1']['ctl_survivors']} | {R['1']['v1']['order']} | — | (reproduced in the first session) |\n")
lk = R["1"]["B"]["line_knobs"]
A(f"249's pass set Run B's and C's line strengths to contour amplitude {lk['amp']:.2f}, widening {lk['widen']:.2f}, fresh-start spread {lk['fresh']:.2f} semitones "
  f"(round 3 read arch term {RUN['B']['calibration'][-1]['lines']['arch'][1]}, widening {RUN['B']['calibration'][-1]['lines']['widening'][1]}, first note's extra surprise {RUN['B']['calibration'][-1]['lines']['fresh'][1]} bits, against the kept 1.452, 0.326, 1.338).\n")

A("## 2. Deaths per gate, beside the first run\n")
A("| Gate (v107) | v1 | A | B | C |\n|---|---|---|---|---|")
for r in R["2"]["rows"]:
    parts = "; ".join(f"{k.split(':')[0]} {n}" for k, n in r["v1_parts"].items() if n) if r["v1_parts"] else ""
    A(f"| {r['gate']} | {r['v1']}{' (' + parts + ')' if parts else ''} | {r['A']} | {r['B']} | {r['C']} |")
A(f"| Survivors | {R['2']['v1_survivors']} | {R['2']['survivors']['A']} | {R['2']['survivors']['B']} | {R['2']['survivors']['C']} |\n")
A("The v1 row for the limits adds the six gates 276 turned into limits (leaps 153, the run clause 261, the chorus floor 45). The death order is v1's (a build dies at the first gate it fails), so a gate's count depends on what dies before it. "
  "The 'would fail' counts, every gate read on every complete build:\n")
A("| Gate | A | B | C |\n|---|---|---|---|")
for g in R["2"]["would"]["A"]:
    if any(R["2"]["would"][v][g] for v in "ABC"): A(f"| {g} | {R['2']['would']['A'][g]} | {R['2']['would']['B'][g]} | {R['2']['would']['C'][g]} |")
A("")

A("## 3. Fix 277: soft breaks and hard limits\n")
A("| Run | Complete builds | 0 soft | 1 | 2 | 3+ | Deaths on a hard limit | Deaths on a third soft break | Pick's soft breaks |\n|---|---|---|---|---|---|---|---|---|")
for v in "ABC":
    x = R["3"][v]; s = x["soft_share"]
    A(f"| {v} | {x['complete']} | {pc(s['0'])} | {pc(s['1'])} | {pc(s['2'])} | {pc(s['3'])} | {x['deaths_on_hard']} | {x['deaths_on_three_soft']} | {len(x['pick_soft'])} {x['pick_soft'] or ''} |")
k = R["3"]["kept_soft_share"]; A(f"| kept songs | — | {pc(k[0])} | {pc(k[1])} | {pc(k[2])} | {pc(k[3])} | — | — | — |\n")
A("Soft breaks by limit: " + "; ".join(f"Run {v}: " + (", ".join(f"{a} {b}" for a, b in R['3'][v]['soft_by_limit'].items()) or "none") for v in "ABC") + ".\n")
A("Each limit, the builds' median and the pick, beside Table DL (Run B; Run A and C alongside):\n")
A("| Limit | Soft | Hard | B builds' median | B pick | A median | C median |\n|---|---|---|---|---|---|---|")
for lim, (med, pk, s, h) in R["3"]["B"]["limits"].items():
    if lim == "run_max": s, h = "under 10", "under 15"
    A(f"| {lim} | {s} | {h} | {f3(med)} | {f3(pk)} | {f3(R['3']['A']['limits'][lim][0])} | {f3(R['3']['C']['limits'][lim][0])} |")
A(f"\nThe builds still sit at one point on two readings: the most note lengths in any eight bars is 5 in every build of all three runs (5th to 95th: {trio(R['3']['B']['lengths_builds'])}; kept median 6, 4 to 8), "
  f"and the chorus's top is 10 semitones over the verse's at the median (kept: 0 at the median, 9 at the 95th). The longest run in a line now spreads ({trio(R['3']['B']['run_max_builds'])} in B; kept 2 · 4 · 5 · 7 · 10). "
  f"A tritone leap appears in {pc(R['3']['B']['tritone_leap_any'])} of B's builds and a leap past an octave in {pc(R['3']['B']['octave_any'])} (kept songs: 34% and 41% have one); in A, {pc(R['3']['A']['tritone_leap_any'])} and {pc(R['3']['A']['octave_any'])}.\n")

A("## 4. Fixes 275 and 280: the kept pass rate of every gate in the search\n")
A("| Gate | Kept pass rate | Source |\n|---|---|---|")
for g, rate, src, _ in R["4"]["gates"]:
    flag = " ⚑" if rate is not None and rate < 0.9 else ""
    A(f"| {g} | {pc(rate) + flag if rate is not None else '—'} | {src.split(':')[0] if g.endswith('(session, 280)') else src} |")
A(f"\nThe seven gates of fix 280 were run with the engine's own functions on its calibration pairs: **{TB['corpus']}**. "
  f"The five Table B readings pass together on {pc(TB['table_b_together'])} of the {TB['pairs']} pairs; all seven together on {pc(TB['all_seven'])} (breaks per pair: {', '.join(f'{k}: {v}' for k, v in sorted(TB['breaks'].items()))}). "
  "The family is under 275's nine in ten and is flagged (⚑); by the writer's ruling the seven stayed as gates in all three runs. Table B's floors were set on these pairs at the 5th percentile (the spectral band at the 5th and 95th), so each passes about 95% (90%) alone by its making; the joint rate is the new reading. "
  "The sequence-legs gate was read with bars counted from the pair's own first bar (the engine's bar_cells counts the song's sung bars); the rhythm band with the engine's rhythm table on the pairs' sixteenth grid.\n")

A("## 5. The line readings of Table DJ\n")
A(f"Builds' 5th · median · 95th; the pick; the kept middle half (25th · median · 75th). Every complete build is read; v1's are its {R['5']['v1_builds_read']:,} complete builds (the first run kept notes for these, not for the builds that died while being made).\n")
A("| Reading | Kept | v1 | A | B | B pick | B outside kept middle half | C |\n|---|---|---|---|---|---|---|---|")
L5 = R["5"]
for k in L5["kept"]:
    A(f"| {k.replace('_', ' ')} | {trio(L5['kept'][k][1:4])} | {trio(L5['v1'][k])} | {trio(L5['A']['builds'][k])} | {trio(L5['B']['builds'][k])} | {f3(L5['B']['pick'][k])} | {pc(L5['B']['outside_mid'][k])} | {trio(L5['C']['builds'][k])} |")
A("\nContour kinds (share of lines): kept " + ", ".join(f"{a} {pc(b)}" for a, b in list(L5["kept_kinds"].items())[:5]) + "; Run B " + ", ".join(f"{a} {pc(b)}" for a, b in list(L5["B"]["kinds"].items())[:5]) +
  "; the B pick " + ", ".join(f"{a} {pc(b)}" for a, b in list(L5["B"]["pick_kinds"].items())[:5]) + ".\n")
A(f"The move between lines a fourth or more: A {trio(L5['A']['join_fourth'])}; B {trio(L5['B']['join_fourth'])} (pick {f3(L5['B']['pick_join_fourth'])}); kept 34% of joins.\n")
A("**Line entry, two readings side by side (285).**\n")
A("| Run | 231: lines with a pickup | 231: last stress on 1 or 3 | 231: last stress off the beat | 260: after the downbeat | 260: on it | 260: on beat 4 |\n|---|---|---|---|---|---|---|")
for v in "ABC":
    e1, e2 = L5[v]["entry_231"], L5[v]["entry_260"]
    A(f"| {v} | {trio(e1['builds_pickup'])} | {trio(e1['builds_b13'])} | {trio(e1['builds_off'])} | {trio(e2['builds_after'])} | {trio(e2['builds_on'])} | {trio(e2['builds_pickup'])} |")
A("| kept | 40–70% asked | 35–55% asked | — | 33 · 52 · 78% | 7 · 18 · 37% | 3 · 14 · 36% |\n")
A("Section endings, the B pick (scale degree of the last sung note): " + ", ".join(f"{s} {d}" for s, d in L5["B"]["ends_pick"].items()) +
  ". Across B's builds Chorus 1 ends " + ", ".join(f"{d} {n}" for d, n in L5["B"]["ends_builds"]["Chorus 1"].items()) + "; Verse 1 " + ", ".join(f"{d} {n}" for d, n in L5["B"]["ends_builds"]["Verse 1"].items()) +
  f". The last note over the line's mean note {trio(L5['B']['builds']['last_over_mean'])} (kept 1.18 · 1.48 · 1.71); the last note the line's longest in {trio(L5['B']['last_longest'])} of lines (kept 61%).\n")

A("## 6. Fix 255: the three builds\n")
A("| Run | Build | Composite | Content | Order | Combined |\n|---|---|---|---|---|---|")
for v in "ABC":
    for lab in ("composite first", "shortlist pick", "judge first"):
        x = R["6"][v][lab]; A(f"| {v} | {lab}: {x['fp']} | {f3(x['composite'])} | {f3(x['content'])} | {f3(x['order'])} | {f3(x['combined'])} |")
A("")
for v in "ABC":
    x = R["6"][v]; A(f"- Run {v}: the composite's first is {x['comp_first_rank_by_judge']}th of {x['survivors']} by the judge, inside the upper half ({x['shortlist_size']}), so the shortlist did not change the pick. "
                     f"Builds: content {trio(x['builds']['content'])}, order {trio(x['builds']['order'])}, combined {trio(x['builds']['combined'])}.")
A("- v1: the composite's first was 23rd of 43 and the shortlist changed the pick. Kept windows: content 4.565, order 1.58, combined 3.11 (medians).\n")
A("The content judge's heaviest give-aways (weight × z, mean over 400 builds): " + "; ".join(f"{lab}: " + ", ".join(f"{m.replace('_', ' ')} ({x})" for m, x in R["give_away"][lab][:4]) for lab in ("v1", "A", "B")) + ".\n")

A("## 7. Distance, the outside count, reciting, the era\n")
A("| Run | Distance from the centre | Outside both kept middle halves (of 56) | Verse on reciting (sd) |\n|---|---|---|---|")
for v in "ABC":
    x = R["7"][v]; A(f"| {v} | {trio(x['distance'])} (pick {f3(x['pick_distance'])}) | {trio(x['outside'])} (pick {f3(x['pick_outside'])}) | {trio(x['reciting_verse'])} (pick {f3(x['pick_reciting'])}) |")
x = R["7"]["v1"]; A(f"| v1 | {trio(x['distance'])} (pick {x['pick_distance']}) | {trio(x['outside'])} (pick {x['pick_outside']}) | {trio(x['reciting'])} (pick {x['pick_reciting']}) |\n")
A("The five era readings for the B pick (median of Verse 1, Chorus 1 and the Bridge), CLASSIC's middle half and 5th–95th:\n")
A("| Reading | Pick | Middle half | 5th–95th |\n|---|---|---|---|")
x = R["7"]["B"]
for k in P.ERA_K: A(f"| {k} | {f3(x['era_pick'][k])} | {x['era_mid'][k][0]}–{x['era_mid'][k][1]} | {x['era_95'][k][0]}–{x['era_95'][k][1]} |")
A(f"\nInside the middle halves on {len(x['pick_inside_mid'])} of five ({', '.join(x['pick_inside_mid'])}); inside the 5th–95th on {len(x['pick_inside_95'])}. Builds with four or more inside the 5th–95th: A {pc(R['7']['A']['era_inside_four_builds'])}, B {pc(x['era_inside_four_builds'])}, C {pc(R['7']['C']['era_inside_four_builds'])} (kept songs of the era 91%).\n")

A("## 8. The tests of fixes 257–285\n")
T = R["8"]["tests"]; B_ = T["B"]; Af = T["A"]
rows = [
("257", "median 50–78% arched or falling; arch term positive in half or more; no survivor outside 31–94% or with valleys over 33%",
 f"B {pc(B_['257']['median_arch_or_falling'])}, positive {pc(B_['257']['median_arch_positive'])}; {B_['257']['survivors_outside_31_94']} of {B_['257']['n_survivors_read']} survivors outside, {B_['257']['survivors_valley_over_33']} with valleys over 33%; pick's contours: " + ", ".join(f"{a} {pc(b)}" for a, b in list(L5['B']['pick_kinds'].items())[:3]), "median yes; survivors no (12)"),
("258", "median widening −0.1 to +1.1; no survivor outside −1.4 to +1.9; the pick's interval by fifths printed",
 f"B {f3(B_['258']['median'])}; {B_['258']['survivors_outside']} survivors outside; pick by fifths 1.58 · 2.35 · 1.71 · 1.67 · 3.14 (A {f3(Af['258']['median'])})", "median yes; survivors no"),
("259", "first pitch from the contour; median extra surprise 0.8–1.9 bits; joins a fourth or more in 25–40%; no survivor under −0.1; a copy keeps its first note",
 f"B {f3(B_['259']['median_extra_bits'])} bits; joins {pc(B_['259']['median_join_fourth'])}; {B_['259']['survivors_under_minus_01']} survivors under −0.1 (A {f3(Af['259']['median_extra_bits'])}, {pc(Af['259']['median_join_fourth'])})", "median yes; survivors no (2)"),
("260", "median 33–78% after the downbeat; no survivor under 10%; a section entering one way named a design",
 f"B {pc(B_['260']['median_after'])}; {B_['260']['survivors_under_10']} survivors under 10% (A {pc(Af['260']['median_after'])}, {Af['260']['survivors_under_10']}); the chant lines are designed pickups", "median yes; survivors no (2)"),
("261", "a reading: last note over mean (kept 1.2–1.7), last note the longest", f"B {trio(B_['261']['last_over_mean'])}; longest {trio(B_['261']['last_longest'])}", "printed (long)"),
("262", "last chorus on the tonic; an earlier chorus on the tonic triad; the verse off the tonic", f"B: last chorus {pc(B_['262']['last_chorus_tonic'])}, chorus 1 {pc(B_['262']['chorus1_triad'])}, verse 1 off {pc(B_['262']['verse1_off_tonic'])} (910 last notes moved)", "yes"),
("263", "intake count of windows both reciting and CLASSIC", "the first session's Q14; not asked again (no intake questions)", "n/a here"),
("264", "rejected only when fewer than four of five bands inside the 5th–95th; deaths under one in five; the pick inside the middle halves on three of five", f"deaths A {Af['264']['era_deaths']}, B {B_['264']['era_deaths']}, C {T['C']['264']['era_deaths']} of 3,000; B pick {B_['264']['pick_inside_mid']} of five", "yes"),
("265", "the drawn window's year recorded and in the era", f"chorus pool all to 1979 ({pc(B_['265']['chorus_windows_to_1979'])}); B pick: verse window {B_['265']['pick_window']['V']} ({B_['265']['years']['V']}), chorus {B_['265']['pick_window']['C']} ({B_['265']['years']['C']}); the verse pool keeps any year (the writer)", "chorus yes; verse by ruling (294)"),
("266", "no aimed measure from a class median", f"B none ({B_['266']['not_in_rows'] or 'all from the window'}); A: notes a bar from the chart median (the v1 rows)", "yes (B)"),
("267", "no build dies at the return gate where 239 built the return", f"deaths A {Af['267']['deaths']}, B {B_['267']['deaths']}, C {T['C']['267']['deaths']}; near-level used {B_['267']['by_reading'].get('near-level', 0)} times in B", "no (287)"),
("268", "verse 2 shares 25–75% of verse 1's bar rhythms at the median", f"B {trio(B_['268']['v2_share'])}, in range {pc(B_['268']['in_range'])} (A {trio(Af['268']['v2_share'])})", "at the edge (293)"),
("269", "260's test; last stresses on 1 or 3 in 35–55%", f"B after {pc(B_['269']['after'])}; on 1 or 3 {trio(B_['269']['b13'])}", "entry yes; landing no (289)"),
("270", "dies only at ten or more; a fifth of lines (±half) with a run of four; reciting median 1.4–2.1", f"runs ≥10: {B_['270']['run_deaths_only_10'][0]} soft breaks, {B_['270']['run_deaths_only_10'][1]} hard (276/277 govern); lines with a run of four {pc(B_['270']['lines_with_run4'])}; reciting B {f3(B_['270']['reciting_median'])}, A {f3(Af['270']['reciting_median'])}, C {f3(T['C']['270']['reciting_median'])}", "runs yes; reciting no in B (by 0.02)"),
("271/285", "every aim kept followed at r ≥ 0.3; dropped after two songs running under it", "turns per move: verse " + f3(R['8']['aims_followed']['B']['v:turns_per_move']) + ", chorus " + f3(R['8']['aims_followed']['B']['c:turns_per_move']) + " (song 39 0.56, 0.33); beat 3 via the landing draw: verse " + f3(R['8']['aims_followed']['B']['v:on_beat3']) + ", chorus " + f3(R['8']['aims_followed']['B']['c:on_beat3']), "no (290)"),
("272", "fills against gaps of 2.75 beats or more; seven in ten filled", f"{RF['fill_stats'].get('filled', 0)} of {RF['fill_stats'].get('filled', 0) + RF['fill_stats'].get('gap left open (30%)', 0) + RF['fill_stats'].get('no fill fits', 0)} eligible gaps filled; short gaps {RF['fill_stats'].get('filled (short gap)', 0)} filled with a beat and a half", "yes"),
("273", "chord strikes with a bass note printed beside the bass cell; 16% or more", "100% (eighth-note bass cell), see the record", "yes"),
("274", "the extension named; every other section a multiple of four", "the last chorus's 18 bars named; all others multiples of four", "yes"),
("275", "every gate printed with its kept pass rate; families under 90% flagged", f"section 4; flagged: the seven unaudited gates together ({pc(TB['all_seven'])}), the spectral band alone ({pc(TB['alone']['spectral'])})", "printed"),
("276", "the eight limits on every build; pick and median beside Table DL", "section 3", "yes"),
("277", "deaths on a hard limit or third soft break under one in five; the pick's soft breaks printed", f"B {R['3']['B']['deaths_on_hard'] + R['3']['B']['deaths_on_three_soft']} death of 3,000; pick {len(pB['info']['soft'])} soft breaks", "yes"),
("278", "no death for a comparison, a return's first or top note, or a tritone unless chosen; design gates listed; kept rates beside the builds'", "design gates: the summit, the bridge's register; aims in the table below", "yes"),
("279", "a record", "the six sound gates as they stand", "—"),
("280", "the seven unaudited gates' pass rates on the calibration songs and together", f"section 4; together {pc(TB['all_seven'])}", "printed; under 90%"),
("281", "with a section's character chosen, the median on that axis in 1.4–2.1 whatever is designed; free notes printed", f"verse reciting B {f3(B_['270']['reciting_median'])}; free notes in the pick: " + ", ".join(f"{a} {b}" for a, b in R['8']['281']['free_notes_pick'].items()), "no, narrowly (293)"),
("282", "a line said twice keeps its source's intervals except notes changed for 276's tritone reading", f"B: notes changed {trio(R['8']['282']['changed_twice_notes'])}; the pick 0; 'tuned' on G4 over G", "yes"),
("283", "the feel of each section stated", "every section straight", "n/a (no swing)"),
("284", "a record", "song 39's", "—"),
]
A("| Fix | The test | The reading | Held? |\n|---|---|---|---|")
for r in rows: A("| " + " | ".join(r) + " |")
A("\nFixes that did not apply to this song: 263 (an intake count; the writer had already settled reciting against CLASSIC at Q14 and no intake question was asked), 283 (no section is swung), 279 and 284 (records), 261 (a reading only). "
  "Fixes 257–262, 265, 266, 268, 269, 271, 281 and 282 ran in Run B and C only, by the brief's design.\n")
A("**278's aims: the builds' rate beside the kept rate.**\n")
A("| Aim | Kept | A | B | C |\n|---|---|---|---|---|")
for k in P.AIMS_278:
    A(f"| {k} | {pc(R['8']['278']['kept'][k])} | {pc(R['8']['278']['A'][k])} | {pc(R['8']['278']['B'][k])} | {pc(R['8']['278']['C'][k])} |")
A("\n**Aims followed (285's two readings), correlation of target and reading across Run B's builds:** " +
  ", ".join(f"{k} {f3(v)}" for k, v in R["8"]["aims_followed"]["B"].items()) + ". Run C aims every build at the same medians, so it has no correlation to read.\n")

A("## 9. The regression line from the fix list after v103\n")
G = R["9"]
reg = [("Both orders reproduced twice at PYTHONHASHSEED 0", f"A {G['orders']['A'][0]}, B {G['orders']['B'][0]}, C {G['orders']['C'][0]}, each the same on the second run", "held"),
       ("The six A4s on 'tuned' over A", "six, bars 21, 29, 49, 57, 89, 97", "held"),
       ("The chorus opening unrelated", "yes", "held"),
       ("The chorus floor above the verse's", f"{G['chorus_floor'][0]} against {G['chorus_floor'][1]} (now an aim, 278)", "held"),
       ("The pick inside CLASSIC's five bands", f"5th–95th on five; middle halves on four ({', '.join(G['era_pick_mid'])})", "held as 264 reads it"),
       ("Under one build in five at the era gate (258 → 264)", f"A {G['era_deaths']['A']}, B {G['era_deaths']['B']}, C {G['era_deaths']['C']} of 3,000", "held"),
       ("None at 181 where the return was built (261 → 267)", f"A {G['return_deaths']['A']}, B {G['return_deaths']['B']}, C {G['return_deaths']['C']}", "not held (287)"),
       ("Verse median on reciting inside 1.4–2.1 (264 → 270)", f"A {G['reciting']['A']}, B {G['reciting']['B']}, C {G['reciting']['C']}", "B not held by 0.02; C held"),
       ("Verse 2's shared bar rhythms inside 25–75% (262 → 268)", f"A {f3(G['v2_share']['A'])}, B {f3(G['v2_share']['B'])}, C {f3(G['v2_share']['C'])}", "B at the floor; A and C not held"),
       ("Every consistency check", (lambda ok: f"{sum(v for _, v in ok)} of {len(ok)}")(pickle.load(open(f"{H}/out_v2/consistency.pkl", "rb"))), "held"),
       ("The controls stay as the comparison", "Run C beside Run B throughout", "held"),
       ("The judges' claim stays what 27.47 says", "like a kept song in content and order, not good; no claim made beyond it", "held")]
A("| Item | Reading | Held? |\n|---|---|---|")
for r in reg: A("| " + " | ".join(r) + " |")
A("")

A("## The record\n")
A(f"Built from Run B's shortlist pick, {pB['fp']} (composite {pB['meas']['composite']:.3f}, combined {pB['judge']['combined']:.3f}), with no hand edits: verse window {pB['meta']['win']['V']}, chorus window {pB['meta']['win']['C']}; "
  f"plans: verse {''.join(pB['meta']['plans']['Verse'])}, bridge {''.join(pB['meta']['plans']['Bridge'])}, pre {''.join(pB['meta']['plans']['Pre'])}, chorus tail {pB['meta']['plans']['tail']}. "
  f"Range B2–A4. The band as v1 (build_v2_p38.py); the intro tune, fills and solo drawn again against the new voice (riff_v2_p38.py; fix 272). "
  "Delivered: the demo (MP3, General MIDI, GarageBand MIDI), the lead sheet and the number chart (the parts were engraved too, for the readback). "
  + (lambda ok: f"Consistency: {sum(v for _, v in ok)} of {len(ok)} checks pass (consistency_v2_p38.py), every document read against the record.\n")(pickle.load(open(f"{H}/out_v2/consistency.pkl", "rb"))))

A("## Readings the paper did not spell out\n")
A("Every place this rerun had to choose a number or a reading that v107 does not give, by fix, so the paper can be corrected. The writer ruled on the first five before the runs.\n")
RD = [
("270, 276, 277", "The run clause is one of 276's eight limits: a run of 10–14 in a line is a soft break, 15 or more hard (the writer's ruling). 270 contributes only the lifted ban: the walk may repeat a fourth time, and the v1 repair step no longer re-walks runs of four. The repair step still re-walks leaps past a sixth and tritones."),
("268, 269", "In verse 2 each line takes its source line's entry kind, and the rest of the rhythm walk is tilted toward verse 1's onsets (the writer's ruling). The tilt multiplies a source onset's weight by 8, the session's number, chosen by trial (4 left the median at the same 25%), not calibrated."),
("267", "Near-level means both shared-event pitch series span 2 semitones or less: the session's number, uncounted (the writer's ruling)."),
("267", "'The first three-quarters of the events it shares' is read by time, the shared events before 0.75 of the line's span, which is the quarter in which v1's 239 makes its late change. Read by count, a build whose change lay in the last quarter by time but not the last quarter by count died; 31 of the first 60 test builds did."),
("280", "The seven unaudited gates stay as gates in all three runs; their pass rates are printed on the 515 POP909 major-key pairs (the writer's ruling). They did not join 277's count: the paper gives no soft or hard values for them."),
("282", "Run B and C build the said-twice line as its source moved whole; Run A keeps v1's way (the writer's ruling). A note is changed only where it is a tritone from its chord's root on a beat or held a beat (276's reading), to the nearer semitone that is not."),
("278", "A return's first or top note: vary_return's six tries steer toward keeping both, and if none of the six does, the last try is kept."),
("264", "Run A keeps v1's chorus pool (windows inside three of the four CLASSIC middle-half bands the old rows carry) as the way the middle halves are aimed at."),
("265", "Run B's chorus and bridge pool is every kept window to 1979 (200), with no band filter. The verse pool keeps its 20 reciting windows of any year (the writer's ruling: Q14 let the verses recite against CLASSIC)."),
("260, 269", "Entry rates: the kept song medians (on 0.179, after 0.525, pickup 0.143) normalised to 21%, 62%, 17%. 'After the downbeat' is the 'and' of 1 to the 'and' of 3 on the eighth grid; 'pickup' is beat 4 of the bar before or its 'and'. A stressed first syllable cannot be a pickup; the kind is then redrawn between on and after. The chant lines are designed pickups."),
("259", "In B and C the v1 join repair (a line's pickup re-walked when the join leaps past an octave or a tritone) and the steering of a line's last note toward the next line's first are dropped. The first pitch is drawn around h0 = the section's centre + N(0, s) − the contour's mean, kept inside the section's register, with a spread of 1.5 semitones around h0; s is 249's fresh-start knob."),
("257", "Contour kinds are drawn at Window 124's kept shares of lines. Each kind is a piecewise line through the line's time (arch: 0 → +1 at 0.3 → −0.2; falling 0 → −1; valley 0 → −1 at 0.5 → 0; and so on), scaled by 249's amplitude knob × U(0.7, 1.3); the walk is pulled toward it with a Gaussian of 2.5 semitones. Designed lines, copies, returns and re-sung lines keep their own notes."),
("258", "Widening is a tilt on the walk's interval categories through the line: repeats and steps × exp(−W(x − ½)), thirds and larger × exp(W(x − ½)), x the time through the line, W 249's widening knob."),
("249", "The three line strengths are calibrated in the same 3 × 30 pass toward Table DJ's kept medians (arch term 1.452, widening 0.326, first note's extra surprise 1.338): multiplicative for amplitude and spread, additive for widening, with caps."),
("285", "The window's beat-3 share tilts the b3 share of 231's landing draw by (target ÷ pool median)^1.5; the walk's beat-3 tilt and its calibration knob are removed."),
("262", "Verse 1's last note is kept off the tonic and Chorus 1's on A, C♯ or E. A fresh last line is redrawn up to seven times, then (and for a returning last line) its last note moves by the smallest step to an allowed scale tone (910 times in B). The pre-chorus and the bridge have no rule; verse 2 inherits verse 1's ending."),
("281", "No compensation was computed: verse 1's only non-free notes are returns of its own free lines, so the free lines carry the whole aim. The free-note counts are printed."),
("27.48 (Table DJ)", "Lines are the engine's lyric lines, not found by rule, with three notes or more. A song's value is the median over its lines for the arch and falling terms, the last note less the mean and the last note over the mean; the mean for shares and the widening. The first note's extra surprise is the mean surprise of each line's first note (from the line before's last note) less the mean of all other notes, under the v104 file's first-order model."),
("276", "The limits are read on the whole song's sung notes in order, moves across line joins included; the run inside a line; the tritone from the root on notes on a beat or a beat or longer; the chorus comparisons on Chorus 1 and Verse 1 as whole sections."),
("272", "A short fill starts half a beat after the voice stops and ends as it returns, with no margin; short gaps are offered a fill at the same 70% and are not counted in the rate."),
("264", "The five era readings are v1's: the median of the first 8-bar windows of Verse 1, Chorus 1 and the Bridge."),
("All runs", "Builds that died while being made keep their partial notes and fingerprint; their judge scores are empty."),
]
A("| Fix | The reading taken |\n|---|---|")
for a, b in RD: A(f"| {a} | {b} |")
A("")
A("## Findings\n")
for blk in open(f"{H}/findings_v2.md").read().strip().split("\n\n"): A(blk + "\n")
open(f"{H}/test_report_v2.md", "w").write("\n".join(md)); print("test_report_v2.md:", len(md), "lines")
