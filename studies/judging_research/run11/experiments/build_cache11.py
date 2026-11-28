"""Build the run 11 notes-side cache (no outcome is read): per within-artist song (video id), the 13 baselines and every measure
from measures/*.py (each module defines KEYS and clip_measure(mel, a) -> dict). Song value = n_mel-weighted mean over clips with a
value; '<key>_c12' = (clip 1, clip 2) for the stability gate. Writes common11.CACHE."""
import os, sys, json, glob, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import common11 as C

def main(only=None):
    R = C.rows(verbose=True)
    mods = []
    for f in sorted(glob.glob(os.path.join(HERE, "measures", "*.py"))):
        name = os.path.basename(f)[:-3]
        if only and name not in only: continue
        s = importlib.util.spec_from_file_location(name, f); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
        mods.append(m); print("module", name, m.KEYS, flush=True)
    C.song_values(R, lambda mel, a: C.baseline(mel), C.BASE)
    for m in mods: C.song_values(R, m.clip_measure, m.KEYS)
    keys = list(C.BASE) + [k for m in mods for k in m.KEYS]
    out = {}
    for r in R:
        d = {}
        for k in keys:
            v = r.get(k); d[k] = None if v is None or not np.isfinite(v) else float(v)
            p = r.get(k + "_c12"); d[k + "_c12"] = None if p is None else [float(p[0]), float(p[1])]
        out[r["vid"]] = d
    json.dump(out, open(C.CACHE, "w"))
    print("cache", C.CACHE, len(out), "songs;", sum(1 for d in out.values() if d["ln_notes"] is not None), "with a melody value")

if __name__ == "__main__":
    main(sys.argv[1:] or None)
