"""Song 40: writes fixlist_p40.md, the cumulative fix list after v108 (fixes from 298), from the findings, the readings and the report."""
import pickle, re
R = pickle.load(open("/home/claude/p40/readings_p40.pkl", "rb")); F = open("/home/claude/p40/findings_p40.md").read()
TR = open("/home/claude/p40/test_report_p40.md").read()
reads = TR.split("## Readings the paper does not give\n", 1)[1].split("\n## Findings", 1)[0].strip()
fx = []
for para in F.split("\n", 2)[2].strip().split("\n\n"):
    n, title, body = re.match(r"\*\*(\d+)\. (.+?)\*\* (.*)", para, re.S).groups()
    for k in ("Problem", "Evidence", "Fix", "Check"): body = body.replace(f"*{k}:*", f"\n\n**{k}:**")
    fx.append(f"### {n}. {title}\n\n{body.strip()}")
r1 = R["1"]; L = R["lift"]; S6 = R["6"]
pct = lambda d: " · ".join(f"{100 * d[k]:.1f}%" for k in "0123")
md = f"""# ZenEng fix list after v108

*Song 40, Nothing Else on Earth · fixes 298–307 · with the runs, the lift, the tests of 257–297 and the readings the paper does not give*

v108's last fix is 297 (Window 128). This list starts at 298 and covers every song since v108: one, song 40, *Nothing Else on Earth*, a new song on the default path, written as a debugging song. Each fix gives the problem, the evidence, the proposed fix and the check. The paper was not edited.

## Songs since v108

| Song | Title | What it tested | Fixes found |
|---|---|---|---|
| 40 | Nothing Else on Earth | v108 on the default path: riff-led rock, 4/4 straight eighths, ♩ = 116, D major, mezzo; verse, pre-chorus, chorus, bridge; lines of mixed length; no era, character, summit, bridge register, lift or countermelody chosen; the chorus said twice as a plain repeat. Off the default path, named: half-time verse drums (Q19, an arrangement design) and the two-bar long lines (Q21, 230's design). 1,000 builds main and 1,000 control (243 off), each twice. Survivors {r1['main']['survivors']} and {r1['ctl']['survivors']}; both orders reproduced. Record from the main run's shortlist pick. | 298–307 |

## The fixes

""" + "\n\n".join(fx) + f"""

## Order of work

1. 298 (the default lift and the hook): the writer asked for a world-class hook and the default path drew a chorus under its verse; nothing after 296 prefers a lift.
2. 299 (the judge's floor): the largest killer, reading the writer's chorus design as unkept.
3. 300 and 301 (the limits' corpus and the hard limits' compounding): realness on POP909 against chart windows; seven 1% tails kill 7% of the pairs they were read on.
4. 302 and 306 (endings and last-note lengths): draw the ending first; draw the last length from the kept ratio.
5. 303 (verse 2's copied bars), 305 (the arch term at its cap).
6. 304 (drop turns per move in the chorus), 307 (a reading for the top note).

## Regression line

After these fixes, song 40 reruns at PYTHONHASHSEED 0, seed 20261511 (calibration 20261512), N 1000, main and control, and must reproduce its frozen orders twice (today's: main {r1['main']['order']}, control {r1['ctl']['order']}; they will change with the code). It must keep the locked lyric, every syllable sung, chorus 2 = chorus 1, the hook said twice in the chorus, 'earth' on beat 1 and held, the tag the hook's tail on the tonic; lose no build at 267 where 239 built the return (287) and under one in five at the spectral reading (286); spread the most note lengths in eight bars across 4–8 (288); land lines at 289's shares; and pass every consistency check (65 of 65 today). After 298–306 it should also show the lift figure at intake; lose under one build in ten at the judge's floor; bring main's realness deaths within twice the control's; keep 95% of the calibration pairs under the seven's hard limits; need the ending move in under one build in ten and end the last chorus on the tonic in every build; share 25–75% of verse 1's bar rhythms in verse 2 in three builds of four; and read the last note over the mean inside 1.2–1.7. Song 38's regression line from the list after v107 stands beside it.

## Reports

- **Runs:** main {r1['main']['survivors']} of 1,000 (order {r1['main']['order']}), control {r1['ctl']['survivors']} of 1,000 (order {r1['ctl']['order']}); each reproduced on its second making. Code {r1['main']['code']}.
- **The three builds of 255:** main composite first = shortlist pick = {S6['main']['shortlist pick']['fp']}; judge first {S6['main']['judge first']['fp']}; under the old fit term {S6['main']['pick under the old fit term (296)']['fp']} (differs). Control: {S6['ctl']['shortlist pick']['fp']} for all but the judge's first ({S6['ctl']['judge first']['fp']}).
- **The lift:** builds' chorus median over the verse {L['main']['builds']['median'][2]:g} at the median (kept 1); the pick {L['main']['pick']['median']:g} median, {L['main']['pick']['top']:g} top. Spectral reading by lift: {L['main']['spectral_by_lift']['within 2'][1]}, {L['main']['spectral_by_lift']['3 to 5'][1]}, {L['main']['spectral_by_lift']['6 or more'][1]} (kept 0.83, 1.08, 1.23); deaths decided at it {L['main']['deaths_spectral_decisive']}.
- **Soft breaks, fifteen limits:** 0 · 1 · 2 · 3+ = {pct(R['3']['main']['soft_share'])} (main); the eight alone {pct(R['3']['main']['soft_share_eight_only'])}; kept (the eight) 70.7 · 22.9 · 5.7 · 0.7%.
- **The most note lengths in eight bars:** {' · '.join(f'{x:g}' for x in R['3']['main']['lengths'])} (main, 5th–95th); the pick {R['3']['main']['lengths_pick']}.
- The full report, with every test of 257–297, is the song's test report.

## Readings the paper does not give

Every place song 40 had to choose a number or a reading that v108 does not give, by fix.

{reads}

## Blind-pick tally

Song 40's blind pick is offered after delivery; the tally stands at 27 songs until it is answered: Annotated top 11, Remembered top 8, Middle 7, Refrain 1.
"""
open("/home/claude/p40/fixlist_p40.md", "w").write(md); print(len(md.encode()), "bytes")
