"""Breath readings for Luthier records: real breaths (gap of 3 beats or more), the dominant breath period and whether it is locked to 1, 2 or 4 bars.
python3 luthier_breath.py record.song.json [...]"""
import sys, os, json, numpy as np
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here); import breath_lib as BL
def defs(fn):
    src = open(os.path.join(here, fn)).read(); g = {"__file__": os.path.join(here, fn)}; exec(src.split("\nrows = []")[0], g); return g
R_ = defs("breath_return.py"); S_ = defs("breath_spectrum.py")
for fn in sys.argv[1:]:
    ns, L_ = BL.read_record_timed(fn); R = json.load(open(fn)); spq = 60.0 / R["bpm"]
    E = R_["events"](ns, spq); r = S_["readings"]([a for a, _, _ in ns], spq)
    lock = any(abs(r["dom_beats"] - k) < 0.6 for k in (4, 8, 16))
    print(fn.split("songs/")[-1], R["bpm"], "bpm", round(L_ / 60, 2), "min | real breaths", len(E), f"({len(E) / (L_ / 60):.1f}/min)",
          "| breath every", round(r["dom_beats"], 1), "beats =", round(r["dom_s"], 2), "s | locked", lock)
