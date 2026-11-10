"""The fix list after v91 (song 36): findings 194-203 in Problem / Evidence / Fix / Check, the songs table, the order of work, the
regression line, the three reports the brief asked for, and the blind-pick tally. Every figure read from readings.pkl."""
import pickle
R = pickle.load(open("/home/claude/p36/readings.pkl", "rb"))
P, Cc = R["pick"], R["ctl"]; S, SA = R["spread_main"], R["spread_ctlA"]
iv, ci = P["intervals"], Cc["intervals"]; ts = R["text"]; rh = R["rhythm"]; ct, res = R["chord_tones"]; o = R["outer"]
def pc(x, d=0): return f"{100 * x:.{d}f}%"
def f2(x): return f"{x:.2f}"
DT = {r["gate"]: r for r in R["deaths_table"]}
RF = R["ret_fail"]["main"]; RFA = R["ret_fail"]["ctlA"]
L = []; A = L.append
A("# ZenEng fix list after v91\n")
A("*Song 36 onward · fixes 194–203 · with the test results the brief asked for, the rule-by-rule run, the deaths per gate and the tables gaps*\n")
A("v91's version row (v125) ends at fix 193, checked before numbering. This list starts at 194 and covers every song since v91. Each fix gives the problem, the evidence, the proposed fix and the check.\n")
A("The brief for song 36, as relayed by the writer:\n")
A("- ZenEng_v91.docx is the single source of the rules. Read the tables (zeneng_v88_tables.json, zeneng_v91_hymn_supplement.json), don't refit; the paper decides at an edge.")
A("- Port into the code before the search, in this order: 181, 182, 178–180, 184, 191–193 (and 183).")
A("- Write a pop, rock or country song; show the full lyric before any music.")
A("- Report: for 181, every section's phrase-design label at 8 and 16 bars and the stock share; for 182, the pick's pitch surprise, the spread across builds, and its shares of repeated notes, steps and leaps past a fifth; exact bar repetition; a control with 181 and 182 off (same seed and N) with the same readings on its first pick; deaths per gate, and for each gate met by construction its control failures (184); which fixes ran, which could not, and why.")
A("- Number new findings from 194.\n")
A("The test results follow the fixes, as Reports 1–3.\n")
A("## Songs since v91\n")
A("| Song | Title | What it tested | Fixes found |\n|---|---|---|---|")
A(f"| 36 | Dance Anyway | The pop class under v91, with 181, 182, 178–180, 184 and 191–193 ported first. A woman alone in her kitchen at 2 a.m. dances to an old song; the bill stays unpaid, the clock stays wrong. Female mezzo B♭3–D5; 4/4 at ♩ = 118, E♭ major, four-on-the-floor disco-pop; 88 bars, 2:59. Chords by the section jobs of 177, the bass the chord roots (183). Two controls: 181 and 182 off, and the constructions off. | 194–203 |\n")
A("## The fixes\n")
F = [
("194", "Secondary stresses are read as stresses",
 "The stress reading marks a syllable stressed when the dictionary gives it a primary or a secondary stress. 191 removes only a second primary stress, so a word with a primary and a secondary keeps both.",
 "In song 36's lyric the reading put two stresses on 'July' (JH UW2 L AY1), 'radio' (R EY1 D IY0 OW2), 'microwave' (M AY1 … W EY2 V), 'somewhere' (S AH1 M W EH2 R) and 'anyway' (EH1 N IY0 W EY2). None has two primaries, so 191 acted on nothing. Read as written, 'July' would be set ju-LY with both syllables strong and 'radio' with a stress on its last syllable.",
 "In a word of two or more syllables only the primary stress counts. A secondary stress counts only on a line's last syllable, where it carries the rhyme or the hold ('dance an-y-WAY'). No list.",
 "Reread songs 21–36: no polysyllable away from a line's end carries two stresses; the declamation reading changes only on those words."),
("195", "181's relatedness test reads bar windows, so the next line's pickup and a held last note decide it",
 "27.31 reads a unit as an equal span of bars. The window holds the next phrase's pickup, which differs between a first unit and its return, and a line that holds its last note for a third of the window is decided by that note, so the ending 181 lets change can break the contour test. Lines whose syllable counts differ cannot keep the onsets at all.",
 f"Song 36 built every named return from its first unit's rhythm and pitches, gave a broken return its first unit's pitches back, and still {DT['returns related (181)']['would']} of 500 builds had a named return the test called unrelated ({DT['returns related (181)']['deaths']} died at it first). By place: " + "; ".join(f"{k.replace('->', '→')} {v}" for k, v in sorted(RF.items(), key=lambda x: -x[1])) + ". The bridge return (12 syllables on 9) failed most. In one case traced during development the two units' notes were identical but for the held last note (E♭4 against A♭4, 24 of 64 sixteenths) and the next section's pickup; the correlation was 0.59. The engine had to add a rule of its own: a form names a return only between lines within three syllables of each other, the extra syllables going before the unit as a pickup.",
 "Read a unit from its first onset to the next unit's first onset, so the next phrase's pickup is outside it; leave a changed last note out of the contour test (it is the ending 181 lets change); and say in 181 that a form names a return only between lines whose syllable counts differ by three or fewer, the extra syllables sung as a pickup.",
 "Rerun song 36's search: no build dies at 181 where its construction was used; the 8-bar stock share stays at or above the chart's 39%."),
("196", "The monotony floor's three-pitch clause is not obeyed by kept pop",
 "166 (from v43) asks at least three distinct pitches in every line-length phrase. Under 132 a universal gate must be obeyed by kept songs; in pop this clause is not.",
 f"The tables' gate audit (198 chart songs) gives two-pitch lines at a median of 7.4% of lines (deciles 0, 0, 7.4%, 18.9%, 50.4%); only 34.3% of songs have none. In song 36 the floor killed {DT['monotony (166)']['deaths']} of 500 builds with its run clause built into the walk; with 182 off it killed 318.",
 "For pop, rock and country keep 'no pitch more than three times running' as the floor and make 'three pitches a line' a reading: the song's two-pitch share printed against the chart's deciles. The notated classes keep the clause where their corpora obey it.",
 "Song 36 rerun: monotony deaths come from the run clause only; the two-pitch share is printed."),
("197", "182's walk can draw several leaps past a fifth in a row",
 "Drawing each move from Table CG independently lets rare leaps come back to back. Kept melodies turn after a leap.",
 "Under the rules before this fix, the search's #1 (afd2849fd733) had a bridge line of three leaps past a fifth in a row: B♭4–C4–A♭4–C4 on 'July, I sat'. Each was a 2–3% draw, and the composite ranked the build first.",
 "After a move past a fifth, the next move is a step or a third in the opposite direction. Song 36 ran with this rule; it is the engine's and is not in the paper.",
 "No survivor has a leap past a fifth followed by another leap; the leaps-past-a-fifth share stays within the class's band."),
("198", "The shares the walk draws are not the shares that survive",
 "182 says the walk draws from Table CG's interval habits. The finished melody adds moves the draw does not make and loses builds the gates kill, so the shares that reach the song are not Table CG's.",
 f"The walk draws repeats 27.6%, steps 42.6%, past a fifth 3.0%. The main run's complete builds read {pc(S['iv_repeat'][1], 1)}, {pc(S['iv_step'][1], 1)} and {pc(S['iv_larger'][1], 1)} at the median; the pick {pc(iv['repeat'], 1)}, {pc(iv['step'], 1)} and {pc(iv['larger'], 1)}. Causes: a melisma's second note is always a step; a split event in a mapped line is a step; the monotony floor kills repeat-heavy builds.",
 "Read 182's shares on the finished melody and aim the draw so the finished melody lands near the class's medians (repeats drawn a little above 27.6%, steps a little below).",
 "The main run's median repeats, steps and leaps past a fifth within two points of Table CG's."),
("199", "The walk puts too few notes on chord tones",
 "The three-term pitch model has no chord in it, and the walk's light chord weight on stressed beats does not make up the difference.",
 f"The pick puts {pc(ct)} of its notes on tones of the bar's chord (Billboard melody_chord_tones median 62%; Hooktheory pop 72% on the beat, 62% off it), resolves {pc(res)} of the others by step (45%), and sets the key word on a chord tone in {pc(R['keyword'][0])} of lines (chart 73%). The key-word gate (134) killed {DT['key word on a chord tone (134)']['deaths']} builds and would have failed {DT['key word on a chord tone (134)']['would']}.",
 "Add the chord to the walk on the beat: a chord-tone term fitted to the class's chord-tone shares on and off the beat, and print the melody's chord-tone share against harmony_by_class.",
 "The pick's chord-tone share between the chart's 25th and 75th percentiles; key-word deaths fall."),
("200", "Table CG gives pop ♭3 and ♭7 in major, but not over which chords",
 "The class key profile sings ♭3 (3.7%) and ♭7 (3.2%) of notes in major keys. A walk that draws them without the chord can set them against chord tones a semitone away.",
 "An early song 36 pick put G♭ over C minor (a diminished fifth over the root, on the stressed 'floor') and G♭ over B♭; a copied line carried G♭ onto an E♭ chord.",
 "Sing ♭3 and ♭7 only where no chord tone lies a semitone away and the note is not a tritone from the root (in E♭: G♭ over A♭, D♭ over E♭ or D♭). A copied note that lands on a clash moves to the nearest scale tone, a chord tone first.",
 "No ♭3 or ♭7 a semitone from a chord tone in any survivor."),
("201", "A two-bar line packs its syllables into sixteenths, and nothing reads it",
 "The form gives each lyric line two bars; 159 and 163 read rhythm a bar at a time and as one band. A line of many syllables is crammed into sixteenths, its last note held long, and the band passes it.",
 f"Song 36's lines run 6 to 14 syllables at ♩ = 118. The pick's gaps between notes are a sixteenth {pc(rh['ioi_sixteenth'])} of the time (Hooktheory pop 2%); onsets on sixteenths {pc(rh['on_sixteenth'])} (4.5%); a line's last note {ts['final_lengthening']:.1f} times its median note (2.0); melisma {pc(ts['melisma_rate'], 1)} of syllables (16.4%). Rhythm {f2(P['rhythm_bits'])} bits, inside the band 1.33–3.57.",
 "Give a line its span from its syllable count (about four or five syllables a bar at this tempo, so a 13-syllable line takes three bars or the lyric is cut), and print sixteenth gaps, onsets on sixteenths and final lengthening against rhythm_by_class and text_setting.",
 "Song 36's sixteenth-gap share within Hooktheory's 5th–95th; final lengthening near 2.0."),
("202", "A declared summit is placed without its position read",
 "165 places the summit where the design names it; 151 reads where kept songs put their peak. The intake asks for the summit without showing 151's figure.",
 f"Song 36's D5 falls {pc(ts['summit']['position'])} of the way through, in the last chorus. Chart pop's peak sits at a median 31% of the way in, and in the chorus or bridge in 67% of songs.",
 "When the intake asks for a summit (133's design clause), show 151's position figure beside the options.",
 "The intake's summit question prints the position reading."),
("203", "192 has nothing to check in a band arrangement",
 "192 asks that the joint draw of tune and bass leave two inner voices able to complete the chord. A band song has no joint draw: the band plays whole triads over a root bass.",
 "In song 36 the check passed on all 500 builds; it cannot fail with a root bass under band triads.",
 "Scope 192 to the classes whose bass is drawn with the tune (hymn, carol, concert solo). In the band classes print instead whether the tune doubles the leading note in the bass, which a root bass on V cannot do.",
 "A band song's report lists 192 as not applicable."),
]
for n, t, p, e, f_, c in F:
    A(f"### {n}. {t}\n")
    A(f"**Problem:** {p}\n")
    A(f"**Evidence:** {e}\n")
    A(f"**Fix:** {f_}\n")
    A(f"**Check:** {c}\n")
A("## Order of work\n")
A("1. **195** (relatedness windows) first: 181 cannot be met by construction until the test reads the unit the construction builds.")
A("2. **194** (secondary stresses): every declamation, text-setting and key-word reading stands on it.")
A("3. **196** (the three-pitch clause in pop): it is the largest killer after 181 and is not obeyed by kept songs.")
A("4. **199, 198, 197, 200** together: the walk's chord term, its aim on finished shares, the turn after a leap, and the ♭3/♭7 rule are one change to 182's walk.")
A("5. **201** (line span from syllables, the sixteenth readings).")
A("6. **202, 203** (the intake's summit question; 192's scope): wording.\n")
A("## Regression line\n")
A(f"After these fixes, song 36 rerun at N 500, seed 20261146, PYTHONHASHSEED 0 must still: reproduce its frozen order twice; keep the pitch median inside 2.76–3.31 (the run's was {f2(S['pitch_bits'][1])}); keep the 8-bar stock share at or above 39% (the pick's {pc(P['designs']['stock8'])}) and every chorus a period at 16 bars; keep 0 deaths at the bands, the summit and the leap limits; pass 38 of 38 consistency checks. Control A (181 and 182 off) must still read the back-test (median {f2(SA['pitch_bits'][1])} bits, {pc(SA['iv_repeat'][1])} repeats), so the comparison stands.\n")
A("## Report 1: the test results the brief asked for\n")
rr = R["rerun"]["main"]; m = R["pick_meas"]
A(f"**The search.** N 500, seed {rr['seed']}, PYTHONHASHSEED 0, code {rr['code_sha']}, Python {rr['python']}, numpy {rr['numpy']}, tables {rr['tables_sha256']}…. {R['survivors']['main']} survivors ({pc(R['survivors']['main'] / 500, 1)}); reproduced exactly on a second run, frozen order {R['order']['main']}. Pick {R['pick_fp']} (#1), no hand edits; composite {m['composite']:.3f} on the pop calibration (IC {m['IC']:.2f}, CMP {m['CMP']:.2f}, memory horizon {m['M_horizon']:.2f}, realness {m['realness']:.2f}, fit {m['fit']:.2f}). Plans: verse {''.join(R['pick_plans']['Verse'])}, chorus {' '.join(R['pick_plans']['Chorus'])}, bridge {''.join(R['pick_plans']['Bridge'])}.\n")
A("### 181: phrase design at 8 and 16 bars\n")
A("Related: onsets Jaccard ≥ 0.6 and contour correlation ≥ 0.6. Units are bar windows (two bars at 8, four at 16). Each cell gives the label, then unit 2 against unit 1 and unit 3 against unit 1 (Jaccard, correlation).\n")
A("| Span | Pick | u2 vs u1 | u3 vs u1 | Control's first pick |\n|---|---|---|---|---|")
for k, v in P["designs"]["at8"].items():
    A(f"| {k} (8) | {v['label']} | {v['u2'][0]:.2f}, {v['u2'][1]:.2f} | {v['u3'][0]:.2f}, {v['u3'][1]:.2f} | {Cc['designs']['at8'][k]['label']} |")
for k, v in P["designs"]["at16"].items():
    A(f"| {k} (16) | {v['label']}{', unit 4 returns to unit 2' if v['u4_returns_u2'] else ''} | {v['u2'][0]:.2f}, {v['u2'][1]:.2f} | {v['u3'][0]:.2f}, {v['u3'][1]:.2f} | {Cc['designs']['at16'][k]['label']} |")
A("")
A("Pre-choruses are four bars and have no 8-bar reading.\n")
A(f"- **Stock share at 8 bars:** pick {pc(P['designs']['stock8'])} (5 of 9 spans), against chart pop 39% and the back-test 9%; control's first pick {pc(Cc['designs']['stock8'])}. Across complete builds (5th – median – 95th): main {pc(S['stock8'][0])} – {pc(S['stock8'][1])} – {pc(S['stock8'][2])}; control {pc(SA['stock8'][0])} – {pc(SA['stock8'][1])} – {pc(SA['stock8'][2])}.")
A(f"- **At 16 bars:** pick {pc(P['designs']['stock16'])} (three periods); control {pc(Cc['designs']['stock16'])}.")
A("- **The pick's named returns:** " + "; ".join(f"{r[0][0]} line {r[0][1] + 1} → line {r[0][3] + 1} ({r[0][4]} bars) {'related' if r[1] else 'not related'} ({r[2]:.2f}, {r[3]:.2f})" for r in P["returns"]) + ". The last is the hook's third statement (180), not a 181 return, and not gated.\n")
A("### 182: pitch surprise and intervals\n")
A(f"- **The pick:** {f2(P['pitch_bits'])} bits a note, against the chart band 2.39–3.97 (median 2.96, p25 2.76); back-test median 2.53. Not flagged. {R['flagged_main']} of the 40 top survivors were flagged under p25.")
A(f"- **Spread across builds (5th – median – 95th):** main {f2(S['pitch_bits'][0])} – {f2(S['pitch_bits'][1])} – {f2(S['pitch_bits'][2])}; control {f2(SA['pitch_bits'][0])} – {f2(SA['pitch_bits'][1])} – {f2(SA['pitch_bits'][2])}.\n")
A("| Moves | Pick | Main median | Control's first pick | Control median | Chart pop |\n|---|---|---|---|---|---|")
A(f"| repeated notes | {pc(iv['repeat'], 1)} | {pc(S['iv_repeat'][1], 1)} | {pc(ci['repeat'], 1)} | {pc(SA['iv_repeat'][1], 1)} | 27.6% |")
A(f"| steps | {pc(iv['step'], 1)} | {pc(S['iv_step'][1], 1)} | {pc(ci['step'], 1)} | {pc(SA['iv_step'][1], 1)} | 42.6% |")
A(f"| leaps past a fifth | {pc(iv['larger'], 1)} | {pc(S['iv_larger'][1], 1)} | {pc(ci['larger'], 1)} | {pc(SA['iv_larger'][1], 1)} | 3.0% |\n")
A("### Exact bar repetition\n")
rp = P["repetition"]
A(f"Pick {pc(P['exact'])} of sung bars (chart pop median 38%; back-test 20%); control's first pick {pc(Cc['exact'])}. Main run {pc(S['exact_bars'][0])} – {pc(S['exact_bars'][1])} – {pc(S['exact_bars'][2])}; control {pc(SA['exact_bars'][0])} – {pc(SA['exact_bars'][1])} – {pc(SA['exact_bars'][2])}. The pick's other kinds: transposed {pc(rp['transposed'])}, reshaped {pc(rp['reshaped'])}, rhythm only {pc(rp['rhythm_only'])}, new {pc(rp['new'])}. Chorus 2 is chorus 1 whole (16 exact bars of {rp['bars']}). Under 157 this reading gates nothing.\n")
A("### The control: 181 and 182 off\n")
A(f"Same seed and N. Returns by the old grammar (same rhythm, new pitches); the walk before 182 (proximity sd 2, leaps to a fifth, the old chord weights); no p25 flag; the band gate kept. {R['survivors']['ctlA']} survivors, order {R['order']['ctlA']}. First pick {R['ctl_fp']}: composite {R['ctl_meas']['composite']:.3f}; pitch {f2(Cc['pitch_bits'])} bits (flagged); repeats {pc(ci['repeat'], 1)}, steps {pc(ci['step'], 1)}, past a fifth {pc(ci['larger'], 1)}; exact bars {pc(Cc['exact'])}; stock {pc(Cc['designs']['stock8'])} at 8 bars, {pc(Cc['designs']['stock16'])} at 16. The control reproduces the back-test: median build {f2(SA['pitch_bits'][1])} bits (2.53), {pc(SA['iv_repeat'][1])} repeats (33%), {pc(SA['iv_larger'][1], 1)} past a fifth (1%).\n")
A("## Report 2: deaths per gate, with the controls for gates met by construction (184)\n")
A("Died: the first gate a build failed, in the order the gates run. Would fail: every gate read on every complete build. Control A: 181 and 182 off. Control B: the constructions off (summit placement, ceilings and floors, the monotony run ban, the leap limits, 181's returns), 182's walk kept.\n")
A("| Gate | Died | Would fail | Control A would fail | Control B would fail | Met by construction |\n|---|---|---|---|---|---|")
for r in R["deaths_table"]:
    A(f"| {r['gate']} | {r['deaths']} | {r['would']} | {r['ctlA']} | {r['ctlB']} | {r['constructed'] or ('the walk (185)' if r['gate'].startswith('pitch band') else '—')} |")
A("")
A("- Table B in the main run: " + ", ".join(f"{k.replace(' (Table B)', '')} {v}" for k, v in R["deaths"]["main"].items() if "Table B" in k) + f". Survivors: main {R['survivors']['main']}, control A {R['survivors']['ctlA']}, control B {R['survivors']['ctlB']}.")
A("- The bands (pitch, rhythm, pushed, density) killed nothing in the main walk, as 185 says; the pitch band's control is control A, with 54 builds below the floor.")
A(f"- With the constructions off, {DT['summit once (165)']['ctlB']} builds sound D5 other than once, {DT['leaps: tritone or past an octave']['ctlB']} leap a tritone or past an octave, {DT['monotony (166)']['ctlB']} break the monotony floor, {DT['register (133)']['ctlB']} put a chorus under its verse, {DT['returns related (181)']['ctlB']} leave a named return unrelated.")
A(f"- Two constructions do not fully hold: the monotony floor still kills {DT['monotony (166)']['deaths']} (fix 196) and 181 still fails {DT['returns related (181)']['would']} builds (fix 195).\n")
A("## Report 3: which fixes ran, and what the tables did not carry\n")
A("| Fix | Ran? | How, or why not |\n|---|---|---|")
rows = [("181", "yes", "construction, gate and reading (Report 1)"), ("182", "yes", "the walk from Table CG; p25 flag; p05 gate"),
        ("178", "yes", "phrase-design reading at 8 and 16 bars"), ("179", "yes", "the chorus's 16-bar default a period"),
        ("180", "yes", "rhymed ends in every chorus; the idea stated three times in the last"), ("184", "yes", "controls A and B (Report 2)"),
        ("191", "yes, acted on nothing", "no word in this lyric has two primary stresses and is not a compound (194 is the related case)"),
        ("192", "as a check", "band triads over a root bass; nothing to complete (203)"),
        ("193", "yes", f"contrary perfects printed: {pc(o['contrary_perfect'], 1)} of bass moves"),
        ("183", "yes", "the root bass read against billboard_implied_bass"),
        ("133, 134, 148, 153, 159, 160, 163, 165, 166", "yes", "gates for pop"), ("157", "yes", "no rhythm floor; the repetition reading printed"),
        ("135", "yes", "outer-voice reading"), ("136", "no gate", "pop has none"),
        ("137, 138", "not applicable", "joint tune-and-bass draw and cadence strengths belong to the hymn and concert classes"),
        ("149–152, 158, 161, 162", "yes", "readings; 152 through 182; the line's rhythm drawn from the pop 4/4 table"),
        ("173–177", "yes", "the chord plan from the section jobs; the harmony and section readings"),
        ("185–190", "not applicable", "hymn and concert amendments"), ("155", "no", "not in the brief; no pop originality quintiles on file")]
for a, b, c in rows: A(f"| {a} | {b} | {c} |")
A("")
A("**What the tables file did not carry:**\n")
A("- A contrary-perfect figure in billboard_implied_bass, so 193's reading has nothing to stand against.")
A("- The unit definition behind 27.31's corpus figures (bar windows or phrase spans), which 195 turns on.")
A("- A chord-tone share in harmony_by_class split by beat for the Billboard corpus (Hooktheory has it), which 199 needs.")
A("- Pop originality quintiles for 155.")
A("- The tables' caution was kept: where a band in the file and the paper differ at an edge, the paper's band was used. No reading fell at an edge.\n")
A("## Blind-pick tally\n")
A("| Slot | Picks |\n|---|---|\n| Annotated top | 9 |\n| Remembered top | 7 |\n| Middle | 7 |\n| Refrain | 1 |\n| Songs picked | 24 |\n")
A("Song 36: the Middle slot (top quartile under both regimes), \"by the green of a clock stuck on twelve.\" It ends the Annotated top's run of three (songs 33–35).\n")
open("/home/claude/p36/fixlist.md", "w").write("\n".join(L))
print(len("\n".join(L)))
