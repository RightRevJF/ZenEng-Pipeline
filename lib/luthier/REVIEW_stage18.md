# Review 18: Luthier v31 (fixes 922–923)

Branch `luthier-v8-stage1` at 4ba7644, main merged in at 4f88e4b. Not an answer to a fix list: it comes from the studies on what makes a song last (`studies/gates_strengthened`, `session_lab`, `hymn_lab`, `gate`, `transfer`, `luthier_on_the_page_gate`).

## Byte for byte

- `make_kept_page_gate.py` writes `tables/kept_page_gate.json` byte for byte (167 kept songs).
- The song reruns reproduce every committed record.
- `soundness.py` reproduces `soundness.json`: sound; one lean past the middle half, rhythm scaling low.
- `neighbour.py` reproduces every field of `neighbour_v31.json`.

## The studies behind 922

The evidence is consistent, and small:
- Where the forgotten are counted, plainer and more foreseeable tunes are the ones kept: session tunes (+0.12 to +0.23 on unseen halves), hymn tunes (+0.04 to +0.19), and one artist's charted against uncharted songs (+0.066, +0.042).
- Among hits nothing on the written tune ranks them: covers, still loved, and the frozen session reader on 3,003 Hot 100 tunes all fail.

That is the shape of a gate under range restriction, and the studies say so with their caveats. The uncharted songs in the same-artist sets are ones fans chose to transcribe. Rhythm surprise carries nothing.

## Question 1: is a floor the right use of a gate that ranks nothing among hits?

Yes. A floor is the only use the evidence supports. An aim would push songs plainer, and among songs already as plain as hits, plainer buys nothing that anyone has measured. A floor only removes the tail that the session, hymn and same-artist studies say is less often kept.

Three things about this floor:
- **It almost never binds.** It removes 2 of 94 builds in song 55, none of 79 in 54 and none in 58. Run without it, song 55 picks the same build (658c9fb36f8d). The songs already stand plainer than most hits: 67th, 57th and 79th percentile of the kept tunes. So 922 is insurance against a later change producing an unforeseeable tune, not an improvement now. The test report should say that rather than count it as one.
- **It reads the notes before melismas** (`c["notes"]`). The words' gate reads them as sung (914), and the kept tunes it is measured against were read with their melismas. A melisma's second note is a step down, so leaving it out moves the build's steps, repeated figures and surprise against the table's (749.102).
- **Two of its ten parts pull where the engine already leans.** Narrower range and fewer leaps count as plainer. In the pools, range is already under the kept 25th in 44 builds in 100 and leaps in 49 (749.100). As a floor that costs nothing today. If 749.100 widens the melody, the floor could start to bind against the fix. Range held its sign in the hymn and same-artist studies but is not among the session tunes' parts that held, and leaps did not show in hymns. Watch it when 749.100 goes in; if it binds there, take range and leaps out of the floor's mean.

## Question 2: does the figure memory pull the songs toward the kept middle more than it is worth?

No, and I should correct how 749.94 read it.

**The random pool pick did not move.** The 15 against 17 in the question is the neighbour choice (the pool build nearest a randomly drawn kept song), not a random pick. A random pick from the engine's pool has a median of 19 song-checks outside the middle half (5th to 95th, 14 to 24) under v30 and under v31 alike.

**Check by check, the pools barely moved** (share of all pool builds outside the kept middle half, low / high; a kept song is 0.25 / 0.25):

| Check | v30 | v31 |
|---|---|---|
| moves by step | 0.01 / 0.50 | 0.00 / 0.55 |
| moves by leap | 0.49 / 0.06 | 0.49 / 0.04 |
| bars on a figure already sung | 0.49 / 0 | 0.49 / 0 |
| bars on a rhythm already sung | 0.47 / 0 | 0.43 / 0 |
| distinct rhythms over bars | 0 / 0.47 | 0 / 0.43 |
| pitch scaling | 0.02 / 0.78 | 0.01 / 0.73 |
| rhythm scaling | 0.90 / 0 | 0.89 / 0 |

A random pick from the pools passes the rule 96 times in 100 (v30: 93).

**What the memory buys is small.** It raises the builds' four-interval figures sung again from a median of 0.425 (no memory) to 0.450, against a kept median of 0.560 (`stage18_results.json`). That closes about a fifth of the gap. The bar-level figure check (rhythm and intervals together) does not move at all, and steps lean a little further high.

The picks' jump (0.385 to 0.492 in song 55) is mostly a different pick, not the memory's average effect. With the memory off, song 58 picks a different build (630ecc6bbc52 against 62c37a5d4af1). So it does steer the pick, but by little on average.

**And 749.94's measure was mine and was wrong.** Counting song-checks outside the middle half rewards a lean as much as variety. Of the pools' readings outside the middle half, almost all sit on one side of their check. Twice the smaller side, summed over the 21 checks, comes to 0.88 under v30 and 0.77 under v31, where kept songs give 10.5.

So the songs' "outside" was nearly all lean. Correcting a lean (as the memory partly does for figures) lowers that count and is still right. I retire the "at least 21" check and replace it with a two-sided one (749.103).

So keep 923. It costs little and corrects a real lean a little. It is not the lever for repetition (749.104).

## 922 and 923 in the code

- `page_gate.read` estimates the key by the Krumhansl profiles on duration-weighted pitch classes. It reads surprise under the kept counts with three intervals of context. The kept tunes are read with their own counts taken out, a build against the full counts; that is right, as a build is not one of the kept.
- The floor is applied after the words' gate and waived if it would empty the pool.
- `_figs` is rebuilt for each fresh line from the lines sung so far in song order. It is reset at each build, so a build never sees another's figures.
- The record carries `kept_page_gate.json`'s fingerprint.

All hold.

## Merged

`origin/luthier-v8-stage1` into main at 4f88e4b, no fast-forward. Song 58 rebuilt from the v31 record (ninth edition, D major, a four-bar turn).
