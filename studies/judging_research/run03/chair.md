# Run 03: the chair's picks

23 November 2026. This is research only; nothing here goes into the Luthier engine. The yardstick is unchanged: lasting love plus covers by other artists. Jason asked that mathematics lead tonight, so both picks test a theorem-backed property of the chord graph.

No outcome was opened before the two rules were written: no cover count, version, release, first year or `discogs_versions_matched.json`. My checks used the notes only, on 2,764 songs (2,672 of them with at least 3 chords).

## Tonight's two tests

Two tests run tonight, so each needs p < .025 to count.

### 1. Does the song's chord graph have a bridge? (`experiments/bridge/`)
**This is the bold new idea.**

A bridge is a link between two chords that nothing else in the song connects, so it cannot be routed around. Card 2's Theorem 2 picks it out exactly: its conductance times its effective resistance equals 1.

**Prediction:** within each artist's own songs, a song with a bridge is covered less, by −0.025 SD per SD of the indicator.

**Why I picked it:**
- It is a new axis: its largest correlation with any size, repetition, surprise or rhythm measure is 0.18.
- It has no settings, and its audit is exact: the resistance definition agreed with a standard bridge search on all 2,764 songs.
- It has the better power of the two, about 0.29 at .025. That is low, and the rule says so.

**The confounder** both imaginers and the Skeptic named is clips per song. The share of songs with a bridge rises with it: 25% with one clip, 34% with two, 40% with three or more. Clips per song is held in the model.

### 2. Ollivier curvature beyond size, repetition and surprise (`experiments/curvature/`)
**This one builds on the earlier finding.**

It asks whether a geometric quantity carries anything beyond the one note finding that holds within artists (chords that move) and beyond chord surprise. The quantity is kbar: the move-weighted mean of lazy Ollivier curvature.

- **Size** is removed by holding chord-count dummies, links and clips.
- **The rule** keeps the Listener's surprise check: if holding surprise removes more than half of the effect, curvature is surprise renamed.

**Why run it when power is only about 0.10?**
1. It is the only direct test of Ricci curvature, the non-Euclidean idea closest to Jason's.
2. Its audit checks a theorem on every song: Prop. 29 says the lazy gap is at least the smallest curvature. My check found 0 violations.
3. It can kill: if nothing is there, the estimate falls at or below zero half the time.

A pass is unlikely, and the rule says so.

### Settings
Both rules use the maintainer's within-artist model unchanged. They add chord-count dummies, which explain 0.46 of kbar against 0.27 for a straight line, plus the number of links and clips per song. A split between the artist halves blocks a pass but does not kill, since at this power one half often disagrees by chance.

## The spectral gap g on Hooktheory: settled tonight without an outcome
The Geometer proposed a gate that needs no outcome. I ran it with McGill's rule: per clip, not lazy, averaged over clips.

| Check | Needed | Found |
|---|---|---|
| Correlation with chord count | under 0.3 | 0.26 (passes) |
| Clip-to-clip agreement | at least 0.5 | 0.17 (fails) |
| Same, after removing size (the second gate) | at least 0.5 | 0.21 (fails) |

37% of songs have g below 0.01. Hooktheory clips are mostly loops, and a loop's g is zero.

So **g stays out of every Hooktheory model.** That includes Jason's S = 1 + g/π, which also changes only g's scale and so adds nothing to a test on ranks. g remains a McGill-only measure: it is stable there (0.58 split-half) and still untested against any outcome.

The curvature test reproduces these numbers as a check that decides nothing.

## Ranked for later (up to three)
1. **The McGill hold-out, for whichever of tonight's measures passes.** Freeze the same rule and run it once, counted. This only happens if a measure passes here first, because the hold-out has already been read twice.
2. **Tonic resistance H (I2) or the obtuse statue (G3), whichever proves more stable.**
   - H passed its surprise gate (ρ −0.14) but tracks size (−0.43).
   - First it needs a clip-to-clip stability check and the full controls, clips per song included.
   - G3 is the more direct form of Jason's "song in a Hilbert space", but its split-half is only 0.37.
3. **I1 revised: melody transport minus chord-tone transport.** It drops the unstable ratio. It is a tune measure (and tune measures have failed five runs), and its clip-to-clip agreement is 0.19. So it goes ahead only after a stability recheck.

## Not ranked, and why
- **G1 as its own test:** merged into tonight's curvature test.
- **The Geometer's shuffle-relative curvature:** it correlates −0.62 with chord repetition, which makes it chords-that-move renamed. It is reported only, deciding nothing.
- **L3 (curvature × repetition):** the product of two measures that each repeat at about 0.26 has no power, so nothing could kill it.
- **I3 (the cover done on the computer):** never computed, and it leaned on g.
- **kmin and the gap slack (card 1, M2):** only 22% of songs have kmin > 0. It is descriptive and is printed in the audit.
- **Time-reversal asymmetry of curvature:** split-half 0.20; the Geometer dropped it himself.
- **Chord surprise as its own confirmatory test:** it was found on these same songs, so a rerun here is not fresh evidence. It is held as a control instead.

## Power, plainly
Both tests are underpowered: about 0.29 for the bridge and 0.10 for curvature. These figures scale the within-artist standard error by each measure's leftover variance. Each script prints its real power before the estimate. A null clears nothing. A kill is the likeliest informative result. A pass would be worth checking on the hold-out.

My check scripts are scratch files and are not in the repo.

## Four more tests, frozen after the first two results (Jason's new rule)
Jason's new standing rule: if an idea is imagined and can be tested on the data at hand, test it tonight. So four ideas the brainstorm had put off are frozen now, each in its own folder with the bridge test's rows, token, wrap rule and `within()` model, holding `ch_rep`, chord surprise (`ch_ic_mean`), the size block, log clips and first year. **All four were written after the bridge and curvature outcomes were seen, so each is labelled "after seeing results": a pass is a lead needing confirmation on unused songs, never a finding.**

**Tonight now counts six tests, so each needs p < .05/6 = .0083 (two-sided), plus the same sign in both artist halves.** The threshold does not move if a test is stopped.

Each test first runs a gate on the notes alone: two clips of one song must agree at Spearman ≥ 0.20, and no |ρ| with a data-pack measure or the size block may exceed 0.7. A test that fails the gate is recorded "stopped" with no outcome joined. My own notes-only check (2,672 songs):

| Folder | Idea | Predicted β per SD | Clip-to-clip | Largest \|ρ\| | Gate (chair) | Power (chair) |
|---|---|---|---|---|---|---|
| `tonic_resistance/` | I2: is home the electrical hub? | −0.03 (lower H, more covers) | 0.247 | 0.08 | passes | 0.21 |
| `obtuse_statue/` | G3: min resistance curvature | −0.02 (more obtuse, more covers) | 0.154 | 0.08 | **fails** | 0.03 |
| `melody_transport/` | I1 revised: tune moves less than the chords | −0.03 (more negative, more covers) | 0.195 | 0.18 | **fails, narrowly** | 0.24 |
| `fifths_path/` | new: mean step on the fifths circle | −0.02 (smaller steps, more covers) | 0.356 | 0.22 | passes | 0.08 |

**Why these four.** I2 and G3 were the two resistance ideas ranked "later"; the Inventor had offered to run only the more stable one, and Jason's rule now says test both, with the gate deciding. I1 was ranked third, pending a stability recheck; the recheck is its gate. The fifths path answers `first_principles.md` §6: put the geometry in a fixed space that the song does not build, so a short song is a noisier reading rather than a different shape. Its direction (smaller steps, more covers) was chosen from chord surprise, since step size is about distance, not recurrence.

**What to expect.** Two of the four will probably stop at the gate. The two that run have power of 0.21 and 0.08. A kill (wrong sign, or weaker than 0.01 in the predicted direction) is the likeliest informative result. H and p_min overlap (ρ +0.51), which is printed. The gate's form for H and p_min (read on the residual after the size block) was fixed before I computed it, and no definition was changed after seeing the gate numbers.
