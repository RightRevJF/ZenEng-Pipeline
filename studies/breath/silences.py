"""Breaths read from durations, not onsets: silences of a beat or more between a sung note's end and the next onset, per 100 beats of the sung span, and the
median silence in beats. Human songs: CoCoPops Billboard (corpora/cocopops_notes.csv.gz, voice, ties merged). Luthier: the records given.
python3 studies/breath/silences.py record.song.json ..."""
import sys, json, numpy as np, pandas as pd
def read(on, end):
    gaps = [b - a for a, b in zip(end[:-1], on[1:])]; span = on[-1] - on[0]
    big = [g for g in gaps if g >= 1.0]; return 100.0 * len(big) / span, (float(np.median(big)) if big else 0.0)
d = pd.read_csv("corpora/cocopops_notes.csv.gz", low_memory=False); d = d[(d.dur > 0) & (d.lead == "voice")]
H = []
for s, g in d.groupby("song"):
    g = g.sort_values("abs_beat"); on = g.abs_beat.values; end = on + g.dur.values
    if len(g) >= 100: H.append(read(on, end))
H = np.array(H); print(f"CoCoPops Billboard ({len(H)} songs): silences of a beat or more per 100 beats, quartiles {np.quantile(H[:, 0], (0.25, 0.5, 0.75)).round(1)}; median silence (beats) quartiles {np.quantile(H[:, 1], (0.25, 0.5, 0.75)).round(2)}")
for f in sys.argv[1:]:
    R = json.load(open(f)); ns = sorted(R["melody"]["notes"], key=lambda n: n["on"]); on = np.array([n["on"] for n in ns]) / 12.0; end = on + np.array([n["dur"] for n in ns]) / 12.0
    a, b = read(on, end); print(f"{f}: {a:.1f} per 100 beats; median silence {b:.2f} beats")
