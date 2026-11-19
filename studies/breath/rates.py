"""Real breaths a minute (gap of 3 beats or more) in the human sets, for comparison with Luthier records. python3 rates.py"""
import os, sys, re, glob, csv, numpy as np, mido
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here); import breath_lib as BL
src = open(os.path.join(here, "breath_return.py")).read(); g = {"__file__": here + "/breath_return.py"}; exec(src.split("\nrows = []")[0], g); events = g["events"]
C = "/home/claude/data/cocopops/CoCoPops"; B = "/home/claude/data/bimmuda/BiMMuDa"; out = {}
for grp, pat in (("RS", "RollingStone/Data/*.hum"), ("BB", "Billboard/Data/*.hum")):
    for fn in sorted(glob.glob(os.path.join(C, pat))):
        got = BL.read_hum_timed(fn)
        if not got: continue
        ns, L_ = got; q = np.array([a for a, _, _ in ns]); s = np.array([b for _, b, _ in ns]); dq = np.diff(q)
        span = (s[-1] - s[0]) / 60
        pk = re.search(r"!!!BillboardPeak:\s*(\d+)", open(fn, errors="ignore").read())
        key = grp if grp == "RS" else ("TOP10" if pk and int(pk.group(1)) <= 10 else "LOW" if pk and int(pk.group(1)) > 20 else "MID")
        out.setdefault(key, []).append((len(events(ns, 1.0)) / span, span))
for m in csv.DictReader(open(B + "/metadata/bimmuda_per_song_metadata.csv")):
    if m["Time Signature 1"] != "4/4" or m["Time Signature 2"] or m["BPM 2"]: continue
    try: bpm = float(m["BPM 1"])
    except ValueError: continue
    pos = m["Position"].strip(); mm = re.match(r"(\d+)(\w*)", pos)
    fn = f"{B}/bimmuda_dataset/{m['Year']}/{pos}/{m['Year']}_{int(mm.group(1)):02d}{mm.group(2)}_full.mid"
    if not os.path.exists(fn): continue
    mf = mido.MidiFile(fn); t = 0; ns = []
    for msg in mido.merge_tracks(mf.tracks):
        t += msg.time
        if msg.type == "note_on" and msg.velocity > 0: ns.append((t / mf.ticks_per_beat, t / mf.ticks_per_beat * 60 / bpm, msg.note))
    if len(ns) < 40: continue
    span = (ns[-1][1] - ns[0][1]) / 60; out.setdefault("BIM", []).append((len(events(ns, 1.0)) / span, span))
for k, v in out.items():
    r = np.array(v); print(k, len(v), "breaths/min quartiles", np.quantile(r[:, 0], (0.1, 0.25, 0.5, 0.75, 0.9)).round(1), "sung span min median", round(float(np.median(r[:, 1])), 2), "90th", round(float(np.quantile(r[:, 1], 0.9)), 2))
