# 749.239, rhythm from a grammar where the phrasebook has no entry: the model, the fit, the bar and the trial, before any code

27 November 2026, 19:06 ET. Asked by Jason (18:50 ET: "mathematically extrapolate from what we know into what we don't, test it, then try again if we fail"); accepted and numbered by the songwriting session (18:58 ET), whose bar is written here as given.

## What is wrong now
A line's rhythm is drawn from kept windows: rhythms counted in the table for that many notes in two bars (or one). Where no kept window meets the line's limits, the build stops ("the syllables cannot fit the window"). Every failure of today was that one.

## The grammar
A window is n onsets on the table's grid (sixteenths: every third twelfth of a quarter) across a span of two bars or one. Its chance, given n and the span:

**P(window) is proportional to the product, over its onsets, of L(level of the onset's place, n) times G(the step from the onset before).**

- **Levels,** from the metre itself and not chosen: the bar's first beat; another beat; the beat's first division (the eighths between beats); anything finer.
- **L** depends on the density through n: for each level, a weight and a slope in notes a bar, in the exponent. Eight numbers; one level is the reference, so six are free.
- **G** has one weight for each step length counted in the fitting half (in sixteenths). A step never counted is never generated. The first onset has no step.
- The proportion is taken over every way of placing n onsets in the span, so the chances of the windows of one count sum to one.

**Fitted, not set:** by maximum likelihood on the fitting half's windows (each occurrence counts once), by gradient ascent on the exact likelihood until the largest change in any weight is under 0.0001. No constant of ours enters the model. The fitted weights are printed to `grammar_fit.json` by the fit, and stand in the result before any engine code is written. (They cannot stand here: the rule comes before the code that finds them.)

One grammar for each table: Essen 6/8, and the Hooktheory pop 3/4 table. The same weights serve two-bar and one-bar spans.

## The held-out check (the songwriting session's bar)
- The table's songs are split in two by a hash of the song (md5 of its name or number, even and odd). Fit on one half.
- A cell is a count n of the other half's two-bar windows with 20 windows or more. Every such cell is read.
- **(a)** In at least 9 cells of 10: the generated windows' share of onsets on a beat, and on the bar's first beat, each lie inside the cell's counted middle half (25th to 75th over the held-out windows, each occurrence one). *Settled:* notes a bar is n over two for every window of a cell, so it is met by construction and said so, not counted as evidence. Where a cell's 25th and 75th are one value, the generated share must be within one onset in n of it (the grain of the measure).
- **(b)** In those cells, the windows counted in the held-out half carry at least 0.60 of the generated chance.
- **(c)** The generated five likeliest windows hold at least three of the held-out half's five commonest, in at least 8 cells of 10.
- Read on Essen 6/8 and on Hooktheory 3/4 pop, each alone. **A table that misses any of (a), (b), (c) does not get the grammar.** A miss is followed by a changed equation under a new rule file, not a moved bar.
- Reported: the same three for one-bar rhythms; the fitted weights; the halves' sizes.

## Where the engine would use it (`LUTHIER_GRAMMAR=1`, unset by default)
Only where the build now stops: no kept window meets the line's limits (its earliest start, its latest end, its count). There the line draws from the grammar's windows of its count that do meet the limits, each at its chance among those. Kept windows are untouched wherever one fits. Every generated window is recorded as generated.

## The rest before a title line, from the table (6/8; with the grammar's trial)
`LUTHIER_TITLE_ENTRY=table`: the line ahead of a title line keeps its slot (no bar more). The silence between its last note and the title line's bar line is drawn from Essen 6/8's counted rests (`essen_6_8_rests.json`, each rest at its counted share), and the line must end ahead of it. The title line enters on its bar line or as a pickup.

## The trial, only for a table that passes the check; marks unchanged
- **6/8:** song 61's words and song 52, each alone: `LUTHIER_PLAN_6_8=folk LUTHIER_TITLE_ROOM=0.9 LUTHIER_COPY_JOIN=1 LUTHIER_TITLE_ENTRY=table LUTHIER_TITLE_NOWAIT=1 LUTHIER_TITLE_FRESH=1 LUTHIER_GRAMMAR=1`. S1 to S7 and U1 to U4 on the living median and the pick; both lyrics must pass.
- **Pop 3/4:** song 55's words as the pop trial stood (deduced stress table), with `LUTHIER_GRAMMAR=1`. K1 to K8, K3 at 0.45 and 0.26.
- Reported: generated windows used, line by line, and their share of the song's lines; builds never made, by reason and line; the silence before each title line.
- Byte for byte, every switch unset: 54, 55, 52, song 53's Essen arm.

## What I expect
- **The check:** (a) passes on both tables. (b) is the hard one: a product of place and step cannot know a rhythm's repeats, and I think the counted windows carry about half the chance in the busy cells; (c) passes in Essen, less surely in pop. **One chance in three that Essen passes all three; one in four for pop.**
- If (b) misses, the next equation adds the one thing this one lacks: a term for a bar that repeats the bar before.
- **The trial, if reached:** builds are made on song 61's words. Whether notes a bar reaches 3.60 there I cannot call; the grammar does not change the plan's bars.
