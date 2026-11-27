# Luthier list for v53 (since v52)

26 November 2026. v52 (fix 965, the loop gate with a chance as what `loop_less` means) is merged into main (5dd5ba8). Next finding 749.223; next fix 966.

## Songs

| Song | Folder | Path | Status |
|---|---|---|---|
| 66, They Did the Right Thing | p76 | engine (v52) with a design gate; the writer's design notes by hand | first edition delivered; consistency 62 of 62 |

## Items

### 749.219 A writer's key cannot be asked for
**Problem.** The engine draws the tune against a written tonic and chooses the key afterwards by range. On song 66 its own run put the tonic at the bottom of the tune (D minor for a tenor). The writer asked for A minor.
**Evidence.** A design gate (`songs/p76/design66.py`) kept only tunes inside a tenor over an A3 tonic: 962 of 4,000 builds died at it, 86 lived, and the joint gate passed 9 (the standard asks 10).
**Fix.** A lyric `key` setting that places the draw's register against that tonic before drawing, so an asked key costs no builds.
**Check.** Song 66 with `key: Am` and no design gate: living builds no fewer than 0.9 of the engine's own run (276 in 1,000), pool 10 or more, the melody inside a tenor.

### 749.220 The pitch ceiling reads verses only
**Problem.** 956 holds a verse's commonest pitch to 0.44. Other sections are never read.
**Evidence.** Song 66: the verses are under it, but the pre-choruses put D4 on 20 of 38 notes in their first eight bars and the bridge E4 on 21 of 39 (0.54).
**Fix.** Read 956 on every sung section and report it; decide by kind (a bridge or pre-chorus may sit on one note on purpose) whether it holds.
**Check.** The reading on the six seen songs and song 66, by section kind, against kept songs' sections.

### 749.221 Arrangement the writer designs has no lever
**Problem.** A held note of set length at a section's end, a bass line under it, an instrument's entry and exit by section, a stop, an added stretch of bars: none can be asked for.
**Evidence.** Every one of song 66's five design notes was laid by hand (`songs/p76/hand66.py`), including five bars added after the final chorus.
**Fix.** A design file the engine reads, naming these by section, so the record carries them and the checks read them.
**Check.** Song 66's design notes written as such a file reproduce `lyric66_d.hand.song.json`'s parts and holds.

### 749.222 The harmony voice sits over the lead
**Problem.** The harmony voice can sing above the lead and very low.
**Evidence.** Song 66: twice (“Still”, bars 36 and 102) the engine's harmony note was G4 over the lead's B3; its range reaches A2.
**Fix.** The harmony a third to a sixth under the lead, never over it, inside a stated range for its voice.
**Check.** On the six seen songs and song 66: no harmony note over the lead; range inside the stated voice.

## Settled on the thread (26 November, evening)

- **749.212 (returning lines that clash), read:** nothing named by the rule. Two causes, described: a copied line over another chord (song 55's fault), and the melisma's second note, which turned out to be the larger half of the engine's clashes in five songs of six.
- **749.223 (form 1, the copy):** 833's clash rule on a copied line's long notes where the chord differs from the source's. Met every mark, clean and whole, alone and with 749.225. **Fix 966.**
- **749.224 (form 2):** missed the whole engine's soundness clause through a changed pick in song 55. Recorded as missed; replaced by 749.225.
- **749.225 (form 2b):** the melisma's second note cleared after the pick (the step above, or one note). Met all five of its marks and the pair's. **Fix 967.**
- **Sealed song 64 ("Go On Ahead"):** run once on the pair. All nine marks held. It tested 967 (clashes 0.545 to 0); its plan gave 966 nothing to do. Song 64 is spent. 966 goes in on the seen songs' evidence, by the rule written first, with a standing watch on new songs. Song 65 is the last unreserved sealed song.

- **v53 merged** into main (3ea86c0): fixes 966 and 967, defaults for 4/4; engine records run again; delivered editions untouched; the paper `reports/Luthier_v53.docx` (Window 210, Module 27.134, Table HV). With both switches off, songs 54 and 55 are byte for byte v52; `--check` passes. For v54: fixes from 968, findings from 749.226.

## Carried, open

- 749.171, 749.144, 749.147, 749.148 to 749.152 (hymns), 749.163.
- The `loop_less` on/off description on the six seen songs (asked with v52).
