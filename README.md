# ZenEng song pipeline

The working code behind Jason Bryant's ZenEng songs (songs 21–25, ZenEng v64 with the v65 fixes run as ports). The engine's rules live in the ZenEng spec; this repo holds the scripts that carry them out for one song at a time.

## Set up a new workspace

```
git clone <this repo> /home/claude/zeneng-pipeline
cd /home/claude/zeneng-pipeline && bash setup.sh
bash newsong.sh 26          # makes /home/claude/p26 from the template (the latest finished song)
```

`setup.sh` installs LilyPond, FluidSynth (with the FluidR3 GM soundfont), pandoc, ffmpeg and the Python packages, downloads the spaCy models and Playwright's Chromium, and links `lib/carol` and `lib/pop` to `/home/claude/carol` and `/home/claude/pop`, where the scripts expect them.

## What's here

| Path | What it is |
|---|---|
| `lib/carol/` | `lily.py` (LilyPond compile and MIDI readback), `measures.py` (melody measures), `lyricsearch.py` (syllables, stress, rhyme, frequency); `songbook/ref.docx` (the Word style for pandoc) |
| `lib/pop/` | `popsearch.py` (lexicon overrides), the pop calibration (`pop_calibration.json`, `pop_ppm.pkl`, `pop_intervals.pkl`) and the Brysbaert concreteness ratings |
| `template/` | Song 25's scripts: the starting point for the next song |
| `songs/p21`–`p24` | Earlier songs' scripts, for reference (duets and 7/8 in p22; a band, riff and push in p23; guitar with capo and TAB parts in p24) |

## One song, in order

| Step | Script | Output |
|---|---|---|
| Intake | `intake.py` | `LOG` (every question, the options, the writer's answer) and the song's constants |
| Writing room | `w1.py` | every line scored; deaths and the writer's locks |
| Lyric | `lyric.py` | the locked lyric, sections and roles |
| Melody search | `melody_pNN.py N` | `melody_result.pkl` (run with N about 500 inside a 590 s limit; never two at once) |
| Inspect and edit | by hand, logged | `melody_final.pkl` |
| Record | `build_pNN.py` | `song_record.pkl`: voice, accompaniment, every event the documents write |
| Demo | `demo_pNN.py` | MP3, General MIDI and GarageBand MIDI; stems (≥ +3 dB) and the 9.12 energy arc |
| Lead sheet | `engrave_pNN.py` | PDF, with MIDI readback per staff |
| Full score | `score_pNN.py` | PDF (piano-led songs), readback per staff |
| Parts | `parts_pNN.py` (see p22–p24) | the production parts PDF |
| Chart | `nashville_pNN.py` | Nashville PDF via Playwright |
| Quotable line | `q1020.py` | the three blind-pick slots |
| Songbook | `songbook.md` → pandoc with `ref.docx` | Word, plus a Doc; musicians only, production notes at the end |
| Test report | `test_report.md` → pandoc | Word; the engine's record and findings |
| Consistency | `consistency.py` | every document checked against the record |

Paths inside the scripts are absolute (`/home/claude/pNN`, `/home/claude/carol`, `/home/claude/pop`); `newsong.sh` rewrites the song number.
