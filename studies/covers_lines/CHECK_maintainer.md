# Design B, checked by the maintainer

25 November 2026. Scripts: `check_repro.py`, `check_analyze.py` (they read WASABI's `json.zip` and my own reduction of Discogs-VI, `/home/claude/shape/discogs_cliques.json`, 348,796 cliques, made on 22 November for the covers study; neither is in the repository).

## What I could and could not check

- **The order.** `PREDICTION.md` is at cf89d36 (11:40), the result at 748e834 (12:04). The rule, the measures and the signs are fixed in the first. `linefeat.py` is mine, unchanged. `analyze.py` does what the prediction says (writer means out, errors clustered, Holm over seven, both halves, with zeros).
- **Not the same files.** The session's join reads the data scout's `songs_meta.csv` and `cliques.csv`, which I do not have. So this is not a rerun. It is the same rule on an independent reduction of the same two sources: WASABI read again from the archive, and my own clique table (recording artists counted as distinct normalised artist names).

## The independent run

1,045 writers, 25,953 songs, median 4 recording artists (the session: 972; 24,284; 4).

| Measure | The session | Mine | Mine, two halves | Mine, repeats held |
|---|---|---|---|---|
| `syl_line` | −0.029 (p .001) | **−0.031 (p .0004)** | −0.043, −0.022 | −0.014 (p .12) |
| `iyou_rate` | +0.021 (p .002) | **+0.008 (p .30)** | +0.012, +0.001 | +0.002 (p .77) |
| `i_rate` | +0.030 | +0.019 (p .006) | +0.029, +0.010 | +0.016 (p .018) |
| `you_lines` | −0.009 (p .20) | −0.017 (p .012) | −0.022, −0.014 | −0.018 (p .007) |
| `rhyme_rate` | +0.012 (p .086) | +0.013 (p .046) | +0.012, +0.015 | +0.019 (p .006) |
| `line_cv` | −0.014 (p .047) | −0.015 (p .021) | −0.012, −0.017 | −0.019 (p .004) |
| `repeat_share` | +0.077 | +0.070 | +0.079, +0.060 | |
| `emo_rate` | +0.023 | +0.021 (p .003) | | |

## What I make of it

1. **Shorter lines reproduce**, to the size, and in both halves. With repeated lines held it weakens the same way (−0.014). The session's reading stands: it cannot be told from repetition in this data.
2. **"I" plus "you" does not reproduce as a pass.** Same sign, a third of the size, p .30. The two joins agree on what is underneath it: **"I" goes with covers (+0.03, +0.02) and "you" does not (−0.009, −0.017).** The sum passed in one join because "I" carried it. So the sentence "a song with a speaker and someone spoken to is one other singers take up" says more than the data: the speaker, yes, in both joins; the someone spoken to, no, in either.
3. **"You" leans down again.** Critics (−0.13, reversed), covers in the session's join (−0.009), covers in mine (−0.017, p .012, both halves). Three readings, one sign. That is against the round-two advice to address someone, as far as acclaim or covers go.
4. **Rhyme and regular lines** are at the edge in both joins and firmer with repeats held in mine. Unsettled by the rule; the first place I would look with a cleaner outcome.
5. A pass that moves from p .002 to p .30 when the clique table is rebuilt is telling us the join matters as much as the trait. The two tables should be compared song by song before `iyou_rate` is called settled either way.

## Verdict

- `syl_line`: **confirmed** as a pass by the rule, tied to repetition.
- `iyou_rate`: **not confirmed.** Read it as "I", small, and say so in the room. `lyric_people.py`'s notes are changed to match.
- Nothing becomes a gate. Agreed.
