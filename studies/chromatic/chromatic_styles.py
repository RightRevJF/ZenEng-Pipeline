"""How chromatic are hymns and art songs, against popular song? The same chord-level measures as chromatic_features.py,
computed from Roman-numeral analyses:
- When in Rome (Gotham et al., CC BY-SA 4.0), human analyses: Bach chorales (371), Goudimel psalms (41), OpenScore Lieder (about 170)
- OpenScore Lieder automatic analyses (AugmentedNet v1.9.1), 1,156 songs
Each chord is turned into pitch classes in its local key. A chord is chromatic if it leaves plain major (Ionian) or minor
(Aeolian plus the leading tone) of the local key; also reported against the piece's first key (which also counts modulations).
Kinds as before: applied dominant (major triad or dominant seventh outside the key whose next chord's root is a fifth below),
mixture (inside the parallel mode), other. 'Lives' = share of 8-bar windows with two or more chromatic chord changes.
Usage: python3 chromatic_styles.py OUT.json NAME=DIR_OR_GLOB ... ; writes per-piece records and prints a summary."""
import sys, glob, json, os, multiprocessing as mp
import numpy as np
IONIAN = {0, 2, 4, 5, 7, 9, 11}; AEOLIAN = {0, 2, 3, 5, 7, 8, 10}
def home(tonic, major): return {(tonic + p) % 12 for p in (IONIAN if major else AEOLIAN | {11})}
def piece(path):
    from music21 import converter, roman
    try: s = converter.parse(path, format="romanText")
    except Exception as e: return None
    rns = [r for r in s.recurse().getElementsByClass(roman.RomanNumeral) if r.quarterLength > 0]
    if len(rns) < 4: return None
    ev = []
    for r in rns:
        try:
            k = r.key; t = k.tonic.pitchClass; maj = k.mode == "major"; P = frozenset(p.pitchClass for p in r.pitches); root = r.root().pitchClass
        except Exception: continue
        m = r.measureNumber or 0
        if ev and ev[-1]["P"] == P and ev[-1]["t"] == t: ev[-1]["dur"] += float(r.quarterLength); continue
        ev.append(dict(P=P, root=root, t=t, maj=maj, dur=float(r.quarterLength), m=m))
    if len(ev) < 4: return None
    g_t, g_maj = ev[0]["t"], ev[0]["maj"]; T = sum(e["dur"] for e in ev)
    loc = [not e["P"] <= home(e["t"], e["maj"]) for e in ev]; glo = [not e["P"] <= home(g_t, g_maj) for e in ev]
    mix = sec = oth = 0
    for i, e in enumerate(ev):
        if not loc[i]: continue
        iv = {(p - e["root"]) % 12 for p in e["P"]}
        nxt = ev[i + 1]["root"] if i + 1 < len(ev) else None
        if iv in ({0, 4, 7}, {0, 4, 7, 10}) and nxt is not None and (nxt - e["root"]) % 12 == 5: sec += 1
        elif e["P"] <= home(e["t"], not e["maj"]) - ({(e["t"] + 11) % 12} if e["maj"] else set()): mix += 1
        else: oth += 1
    n = len(ev); win = {}
    for i, e in enumerate(ev): win.setdefault(e["m"] // 8, []).append(loc[i])
    keys = {(e["t"], e["maj"]) for e in ev}
    return dict(path=path, n_ev=n, chrom_local=sum(e["dur"] for e, c in zip(ev, loc) if c) / T, chrom_global=sum(e["dur"] for e, c in zip(ev, glo) if c) / T,
                mixture=mix / n, secdom=sec / n, other_chrom=oth / n, lives=float(np.mean([sum(w) >= 2 for w in win.values()])), local_keys=len(keys), major=1.0 if g_maj else 0.0)
if __name__ == "__main__":
    out = sys.argv[1]; R = {}
    for arg in sys.argv[2:]:
        name, pat = arg.split("=", 1)
        files = sorted(glob.glob(pat, recursive=True))
        with mp.Pool(max(2, os.cpu_count() - 1)) as pool: recs = [r for r in pool.map(piece, files, chunksize=4) if r]
        R[name] = recs; print(name, len(files), "files,", len(recs), "parsed", flush=True)
    json.dump(R, open(out, "w"), indent=0)
    for name, recs in R.items():
        print("== %s (%d)" % (name, len(recs)))
        for f in ("chrom_local", "chrom_global", "mixture", "secdom", "other_chrom", "lives"):
            x = np.array([r[f] for r in recs]); print("  %-13s median %.3f  p75 %.3f  p90 %.3f  mean %.3f" % (f, np.median(x), np.percentile(x, 75), np.percentile(x, 90), x.mean()))
