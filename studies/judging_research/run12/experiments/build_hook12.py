"""Run 12: notes-side Hooktheory cache for this pass's clip measures (deterministic; reads NO outcome).
Usage: python3 build_hook12.py  -> /home/claude/dl/run12/hook_measures12.json
Per within-artist song (video id; run 04's 9,588 rows via common11): the keys of measures/m_geometer.py (G_C, G_E5, G_REST, G_S5, G_PI)
and measures/m_listener.py (PI1C, PIC, PIC_REL), song value = n_mel-weighted mean over clips (common11.song_values), '<key>_c12' =
(clip 1, clip 2). Run 11's measures (REP = pc_entropy, the 13 baselines) are read from run 11's frozen cache, not rebuilt here."""
import os, sys, json, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "run11", "experiments")))
import numpy as np
import common11 as C

OUT = os.environ.get("HOOK12_CACHE", "/home/claude/dl/run12/hook_measures12.json")

def main():
    R = C.rows(verbose=True); keys = []
    for name in ("m_geometer", "m_listener"):
        f = os.path.join(HERE, "measures", name + ".py")
        s = importlib.util.spec_from_file_location(name, f); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
        C.song_values(R, m.clip_measure, m.KEYS); keys += m.KEYS; print("module", name, m.KEYS, flush=True)
    out = {}
    for r in R:
        d = {}
        for k in keys:
            v = r.get(k); d[k] = None if v is None or not np.isfinite(v) else float(v)
            p = r.get(k + "_c12"); d[k + "_c12"] = None if p is None else [float(p[0]), float(p[1])]
        out[r["vid"]] = d
    json.dump(out, open(OUT, "w")); print("cache", OUT, len(out))

if __name__ == "__main__":
    main()
