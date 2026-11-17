"""Melodic rhythm by period, 1900 to the 2010s, in the Pop20c corpus (VanderStel and Temperley): the 100 note lists (1900-1999) and the
20 post-2000 transcriptions, which have no lyrics, turned into note lists by the corpus's own script (cli/scripts/process-duration.pl,
Temperley's). Rhythm only, so it can include the post-2000 songs: where onsets fall in the 4/4 bar, the last eighth of the bar,
anticipations (an onset on an offbeat eighth with the next beat left empty), and notes per bar. Songs on a sixteenth grid only."""
import os, re, glob, json, subprocess, collections, numpy as np
D = "/home/claude/data/pop20c/pop-corpus"; HERE = os.path.dirname(os.path.abspath(__file__))
YEAR = {l.split()[1]: int(l.split()[0]) for l in open(f"{D}/year_list.txt") if len(l.split()) >= 2}
def period(y): return "1900-1929" if y < 1930 else "1930-1954" if y < 1955 else "1955-1979" if y < 1980 else "1980-1999"
def onsets_of(lines):
    out = []
    for l in lines:
        p = l.split()
        if len(p) >= 3:
            try: out.append(float(p[0]))
            except ValueError: pass
    return out
songs = []
for f in sorted(glob.glob(f"{D}/transcriptions_notelist/*.txt")):
    n = os.path.basename(f)[:-4]
    if n in YEAR: songs.append((period(YEAR[n]), n, onsets_of(open(f))))
for f in sorted(glob.glob(f"{D}/post_2000/*.txt")):
    lines = subprocess.run(["perl", f"{D}/cli/scripts/process-duration.pl", "3", "0", f], capture_output=True, text=True).stdout.split("\n")
    songs.append(("2000-2019", os.path.basename(f)[:-4], onsets_of(lines)))
R = collections.defaultdict(collections.Counter); per_song = collections.defaultdict(list); used = collections.Counter()
for per, name, ons in songs:
    if len(ons) < 40: continue
    fr = [x - int(x) for x in ons]
    if np.mean([abs(x * 16 - round(x * 16)) < 1e-3 for x in fr]) < 0.98: continue
    used[per] += 1; grid = set(round(x * 16) for x in ons); c = collections.Counter()
    for x in ons:
        f16 = round((x - int(x)) * 16) % 16
        k = "beat 1" if f16 == 0 else "beat 3" if f16 == 8 else "beats 2 and 4" if f16 in (4, 12) else "offbeat eighths" if f16 in (2, 6, 10, 14) else "sixteenths"
        c[k] += 1
        if f16 == 14: c["last eighth"] += 1
        if f16 in (2, 6, 10, 14): c["anticipation"] += (round(x * 16) + 2) not in grid
    tot = len(ons); bars = int(max(ons)) - int(min(ons)) + 1
    for k in ("beat 1", "beat 3", "beats 2 and 4", "offbeat eighths", "sixteenths", "last eighth"): per_song[(per, k)].append(c[k] / tot)
    per_song[(per, "anticipations among offbeat eighths")].append(c["anticipation"] / max(1, c["offbeat eighths"]))
    per_song[(per, "notes per sung bar")].append(tot / len(set(int(x) for x in ons)))
out = {"songs": dict(used)}
for (per, k), v in sorted(per_song.items()):
    out.setdefault(k, {})[per] = round(float(np.median(v)), 3)
json.dump(out, open(os.path.join(HERE, "pop20c_rhythm_results.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
