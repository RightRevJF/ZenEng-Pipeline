"""749.84 follow-up: the kept counts behind 876 (a one-bar silence, per eight bars) and 877 (silences of two bars or more, per song), on the parse given
($LUTHIER_COCOPOPS_NOTES or corpora/cocopops_notes.csv.gz). A silence is the time from a sung note's end (clipped at the next onset) to the next onset, inside the sung span."""
import os, sys, json, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib", "luthier")); import kept_corpus as KC
one, two, n = [], [], 0
for k in KC.kept_songs():
    on = k["t"] / 12.0; end = np.minimum(on + k["dur"] / 12.0, np.r_[on[1:], 1e9]); gap = on[1:] - end[:-1]; bars = (end[-1] - on[0]) / 4.0
    one.append(8 * np.sum((gap >= 4) & (gap < 8)) / bars); two.append(int(np.sum(gap >= 8))); n += 1
print(json.dumps(dict(parse=KC.notes_path(), songs=n, one_bar_silences_per_8_bars_mean=round(float(np.mean(one)), 3), one_bar_silences_per_8_bars_median=round(float(np.median(one)), 3),
                      two_bar_silences_a_song_quartiles=[float(x) for x in np.percentile(two, (25, 50, 75))])))
