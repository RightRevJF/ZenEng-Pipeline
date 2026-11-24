# Run 04: first principles

24 November 2026. Recommendations; nothing is dropped without Jason.

## 1. Bedrock
**Facts.**
- On the new outcome (is the song in Discogs-VI at all; 9,588 songs, 23% in), songs whose chords repeat more were *more* likely in: +1.19 points per SD (p .018; halves and conditional logit agree). Not counted: the bar was .01. Among versioned songs, more repetition still means fewer covers (−0.042).
- The rest came out near zero; the torus tests (power 0.08) say only "not large".
- From the scripts: a song is "in" when its title and its artist sit in a Discogs-VI group with two different sets of performer names. "Artist" and "Artist, Guest" are two sets, so a song can be "in" with nobody else recording it.

**Assumptions.** That "in" means another artist took it up; that a clip stands for the song.

## 2. Question every requirement
- **Yardstick (love + covers).** Tonight's outcome was neither. Flag: count only versions sharing no name with the original's.
- **Notes only** (Jason). Kept, though only recording findings have repeated on a second store.
- **Hits only.** A data habit: "never versioned" means among transcribed songs.
- **Within artist.** Keep. Gap: era inside a career; later songs carry more guest credits.
- **Power habit.** Two near-blind tests on seen songs raised every bar from .0167 to .01. Flag: don't count tests under power 0.2 on seen songs. The 0.5 floor is Jason's.
- **Chord surprise as its own claim.** Killed twice; keep it as a control.
- **J1 in 749.159.** Its support is covers among songs already versioned. If tonight's sign is real, looping less could cost a song its chance of being taken up at all. Flag: keep it a reading until section 5 runs; drawing the writer back to the kept rate is still justified.

## 3. Delete (recommended)
- Chords that move, predicted negative on being in at all: wrong sign.
- Chord surprise there: −0.10.
- Distance from the habitual information rate: −0.16, halves split.
- P/L/R share and mean torus step: +0.0065.
- Thirds axis, both readings: +0.006.
- Torus winding and signed area: undefined (whole steps are exact half-turns).
- Geometry on run 03's seen songs, as a family: five kills.

## 4. Simplify
Chord repetition, within artist, on one versions file read two ways: did anyone outside the original artist release it, and how many did. Perhaps loops are taken up more often, by fewer people; or tonight's sign is credit noise.

## 5. Speed the loop: a sixth test tonight, after seeing results
**Code.** `move_extensive/test.py`, outcome changed only: same 9,588 rows and columns (z `ch_rep`, z `ch_ic_mean`, chord-count bins, clip dummies, ln beats, title flags), artist demeaning, CR1 by artist, md5 halves, conditional logit.

**Outcome.** For a song whose `vid` is in `hooktheory_covers_discogs.json`: its sets are the first elements of `discogs_versions_matched.json["cliques"][clique]["versions"]`. a = `re.sub(r"[^a-z0-9]", "", slug.lower().replace("&", "and"))` on the first clip's `artist` (match rule; no unquoting). Own sets contain a; O = every name in an own set. A foreign set is non-empty and shares no name with O. y_foreign = 100 if a foreign set exists, else 0 (0 for unmatched songs); y_self = y − y_foreign. Matched songs with no own set, or a clique missing from the versions file: print, drop from every model; over 25, stop ("not run"). Print y_foreign, y_self and dropped counts, then SE and power, before any β.

**Prediction (two-part story).** β(`ch_rep`) on y_foreign = **+0.9 points per SD**: most of +1.19, shrunk for a first look. The artefact story says under +0.3, the rest on y_self.

**Rules** (p < .05/6 = .0083, two-sided, z 2.638):
- **Pass, a lead needing fresh songs:** β > 0, p < .0083, positive in both halves, conditional logit positive and converged. The artefact story dies.
- **Kill:** β < +0.3. The sign was the original artist's own credit variants; drop "loops get versioned more", and later tests on being versioned use y_foreign.
- **Unsettled:** anything else.

**Power.** Expected SE ≤ 0.50: power about 0.20 at +0.9. The kill line decides: it fires 12% of the time if +0.9 is true, 73% if zero.

**Reported, deciding nothing.** β on y_self, with β_foreign + β_self = β(y) checked to 1e−9; foreign as "a not in the set"; sets naming "karaoke" or "tribute" removed; `ch_ic_mean` on y_foreign.

**Postscript (added after the sixth test ran; the rule above is unchanged).** It came out *unsettled*. Of 2,224 matched songs, only 94 have nothing but the original artist's own credit variants. β(`ch_rep`) on y_foreign was +1.00 points per SD (SE 0.49, p .044; halves +0.45 and +1.43; conditional logit +0.132, p .025). That is above the kill line, so the artefact story did not explain the sign, but it is short of p < .0083. It is a weak lead on seen songs, designed after seeing them.

## 6. The obstacle and the way through
**Obstacle.** Every outcome is a by-product of a credit database, and its noise is as large as the notes signal (about 0.04 SD). Every song on disk is seen.

**Way through (speculation).** Outcomes the original artist cannot produce, covers weighted by the coverer's independence (karaoke out, later covers in). If loops draw cover factories, the audience channel is leaking into covers. Fresh songs: the re-match, y_foreign by default.
