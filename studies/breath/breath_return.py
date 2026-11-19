"""Test A: the breath and the return. Prediction (749.19, written before this test): great songs thin the melody for a beat or two before their best
moment and re-enter on a less expected note, at about 0.55 to 0.65 of the song.
Events: an onset gap of 3 beats or more (a note of about a beat, then a rest of about two), the re-entry note after it.
Entry surprise, two ways, each within the song: how rare the entry's pitch class is in the song (-log2 p), and the leap from the note before the breath.
Each is ranked among the song's own re-entries; the song's 'return' is its re-entry with the highest mean rank.
Readings: position of the return (0 to 1 of the sung span, in seconds); whether it falls in 0.55 to 0.65; the share of the song's re-entries that are
fresh (top third on both) inside 0.5 to 0.7, against the share expected from the count of re-entries there; breath depth (gap in seconds) at the return.
Second reading carried over: breath locked to the 1, 2 or 4-bar grid (breath_spectrum.json). python3 breath_return.py -> breath_return.json"""
import os, sys, re, glob, csv, json
import numpy as np, mido
from scipy.stats import mannwhitneyu, fisher_exact, binomtest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import breath_lib as BL
C = "/home/claude/data/cocopops/CoCoPops"; B = "/home/claude/data/bimmuda/BiMMuDa"
def events(notes, spq, gap_beats=3.0):
    """notes: (quarters, seconds, midi) sorted. Returns list of dicts per re-entry."""
    notes = sorted(notes); q = np.array([a for a, _, _ in notes]); s = np.array([b for _, b, _ in notes]); p = np.array([c for _, _, c in notes])
    pc = p % 12; freq = np.bincount(pc, minlength=12) / len(pc); rare = -np.log2(freq[pc] + 1e-9)
    t0, t1 = s[0], s[-1]; out = []
    for i in range(1, len(q)):
        if q[i] - q[i - 1] >= gap_beats and t1 > t0:
            out.append(dict(pos=float((s[i] - t0) / (t1 - t0)), rare=float(rare[i]), leap=float(abs(p[i] - p[i - 1])), gap_s=float(s[i] - s[i - 1]),
                            up=float(p[i] - np.median(p))))
    return out
def song(notes, spq):
    E = events(notes, spq)
    if len(E) < 5: return None
    r1 = np.argsort(np.argsort([e["rare"] for e in E])) / (len(E) - 1); r2 = np.argsort(np.argsort([e["leap"] for e in E])) / (len(E) - 1)
    m = (r1 + r2) / 2; k = int(np.argmax(m)); ret = E[k]
    fresh = [(a >= 2 / 3 and b >= 2 / 3) for a, b in zip(r1, r2)]; inwin = [0.5 <= e["pos"] <= 0.7 for e in E]
    return dict(n_events=len(E), return_pos=ret["pos"], return_in_window=bool(0.55 <= ret["pos"] <= 0.65), return_gap_s=ret["gap_s"], return_up=ret["up"],
                fresh_in_win=int(sum(f and w for f, w in zip(fresh, inwin))), fresh=int(sum(fresh)), win=int(sum(inwin)),
                deepest_pos=E[int(np.argmax([e["gap_s"] for e in E]))]["pos"])
rows = []
for grp, pat in (("RS", "RollingStone/Data/*.hum"), ("BB", "Billboard/Data/*.hum")):
    for fn in sorted(glob.glob(os.path.join(C, pat))):
        got = BL.read_hum_timed(fn)
        if not got: continue
        ns, L_ = got; q = np.array([a for a, _, _ in ns]); s = np.array([b for _, b, _ in ns]); dq = np.diff(q)
        spq = float(np.median(np.diff(s)[dq > 0] / dq[dq > 0]))
        meta = {x.group(1): x.group(2) for x in (re.match(r"!!!([^:]+):\s*(.*)", l) for l in open(fn, errors="ignore")) if x}
        pk = re.match(r"\d+", meta.get("BillboardPeak", "")); r = song(ns, spq)
        if r: r.update(group=grp, file=os.path.basename(fn), peak=int(pk.group(0)) if pk else None); rows.append(r)
for m in csv.DictReader(open(B + "/metadata/bimmuda_per_song_metadata.csv")):
    if m["Time Signature 1"] != "4/4" or m["Time Signature 2"] or m["BPM 2"]: continue
    try: bpm = float(m["BPM 1"])
    except ValueError: continue
    pos = m["Position"].strip(); mm = re.match(r"(\d+)(\w*)", pos)
    fn = f"{B}/bimmuda_dataset/{m['Year']}/{pos}/{m['Year']}_{int(mm.group(1)):02d}{mm.group(2)}_full.mid"
    if not os.path.exists(fn): continue
    mf = mido.MidiFile(fn); t = 0; ns = []; spq = 60.0 / bpm
    for msg in mido.merge_tracks(mf.tracks):
        t += msg.time
        if msg.type == "note_on" and msg.velocity > 0: ns.append((t / mf.ticks_per_beat, t / mf.ticks_per_beat * spq, msg.note))
    if len(ns) < 40: continue
    r = song(ns, spq)
    if r: r.update(group="BIM", file=os.path.basename(fn), year=int(m["Year"])); rows.append(r)
for fn in sorted(glob.glob("/home/claude/zeneng-pipeline/songs/p*/lyric*.song.json")):
    ns, L_ = BL.read_record_timed(fn); R = json.load(open(fn)); r = song(ns, 60.0 / R["bpm"])
    rec = dict(group="LUTHIER", file=fn.split("songs/")[1], n_events=len(events(ns, 60.0 / R["bpm"])))
    if r: rec.update(r)
    rows.append(rec)
G = dict(BIM=[r for r in rows if r["group"] == "BIM"], RS=[r for r in rows if r["group"] == "RS"],
         TOP10=[r for r in rows if r["group"] == "BB" and r.get("peak") and r["peak"] <= 10], LOW=[r for r in rows if r["group"] == "BB" and r.get("peak") and r["peak"] > 20])
def auc(a, b): u = mannwhitneyu(a, b); return [round(float(u.statistic / (len(a) * len(b))), 3), round(float(u.pvalue), 4)]
res = {}
for g, v in G.items():
    fiw = sum(r["fresh_in_win"] for r in v); exp = sum(r["fresh"] * r["win"] / r["n_events"] for r in v)
    hist = np.histogram([r["return_pos"] for r in v], bins=10, range=(0, 1))[0]
    res[g] = dict(n=len(v), events_median=float(np.median([r["n_events"] for r in v])), return_in_055_065=round(float(np.mean([r["return_in_window"] for r in v])), 3),
                  return_in_055_065_vs_chance=round(float(binomtest(sum(r["return_in_window"] for r in v), len(v), 0.10).pvalue), 4),
                  fresh_in_0507_obs_over_exp=round(float(fiw / max(exp, 1e-9)), 3), return_pos_deciles=hist.tolist(),
                  return_gap_s_median=round(float(np.median([r["return_gap_s"] for r in v])), 2), deepest_in_0507=round(float(np.mean([0.5 <= r["deepest_pos"] <= 0.7 for r in v])), 3))
for g in ("BIM", "RS", "TOP10"):
    a = sum(r["return_in_window"] for r in G[g]); c = sum(r["return_in_window"] for r in G["LOW"])
    res[g + "_vs_LOW"] = dict(window_fisher=[round(float(x), 4) for x in fisher_exact([[a, len(G[g]) - a], [c, len(G["LOW"]) - c]])],
                             events_auc=auc([r["n_events"] for r in G[g]], [r["n_events"] for r in G["LOW"]]),
                             gap_auc=auc([r["return_gap_s"] for r in G[g]], [r["return_gap_s"] for r in G["LOW"]]))
res["LUTHIER"] = [{k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()} for r in rows if r["group"] == "LUTHIER"]
json.dump(dict(res=res, rows=rows), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "breath_return.json"), "w"), indent=1); print(json.dumps(res, indent=1))
