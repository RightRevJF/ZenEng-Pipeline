"""The rosary and hexameter reach 0.1 Hz the same way: two halves alternate (priest and people; listen and recite), each half one ordinary breath,
the pair one slow 10-second cycle (Bernardi 2001; Cysarz 2004: a shallow breath listening, a deeper one reciting, 6.4 cycles a minute).
Does a sung melody's sing-and-breathe pattern carry that two-level alternation, a slow cycle at twice the period of the breath?
Signal: 1 while the voice sings, 0 in a breath (an onset gap of 1.5 beats or more; the note before it sounds for one beat). Onsets only, the same rule
for every corpus. Readings, in beats (tempo-free): power at the 16-beat period (the four-bar unit) against the 8-beat period (two bars), and the share of
power at periods of 12 to 20 beats; in seconds: the share of power at 0.07 to 0.14 Hz. python3 breath_spectrum.py -> breath_spectrum.json"""
import os, sys, re, glob, csv, json
import numpy as np, mido
from scipy.signal import periodogram
from scipy.stats import mannwhitneyu
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import breath_lib as BL
C = "/home/claude/data/cocopops/CoCoPops"; B = "/home/claude/data/bimmuda/BiMMuDa"
def signal(onsets_q, dt=0.25, gap=1.5):
    on = np.array(sorted(set(onsets_q))) - min(onsets_q); n = int(on[-1] / dt) + 8; s = np.zeros(n)
    for a, b in zip(on, list(on[1:]) + [on[-1] + 1]):
        end = b if b - a < gap else a + 1.0; s[int(a / dt):int(end / dt)] = 1
    return s
def readings(onsets_q, spq):
    s = signal(onsets_q); s = s - s.mean()
    if len(s) < 64 * 4: return None
    f, P = periodogram(s, fs=4.0, window="hann")             # f in cycles per beat
    band = lambda lo, hi: P[(f >= lo) & (f <= hi)].sum()
    tot = band(1 / 64, 1.0)
    at = lambda per: P[np.argmin(abs(f - 1 / per))] + P[np.argmin(abs(f - 1 / per)) + 1] + P[np.argmin(abs(f - 1 / per)) - 1]
    fs = f / spq                                                # cycles per second
    w = (f >= 1 / 32) & (f <= 1 / 3); dom = 1 / f[w][np.argmax(P[w])]
    return dict(dom_beats=float(dom), dom_s=float(dom * spq), four_over_two=float(np.log((at(16) + 1e-9) / (at(8) + 1e-9))), slow_share_beats=float(band(1 / 20, 1 / 12) / tot),
                mayer_share=float(P[(fs >= 0.07) & (fs <= 0.14)].sum() / tot), spq=spq)
def main():
  pass
rows = []
for grp, pat in (("RS", "RollingStone/Data/*.hum"), ("BB", "Billboard/Data/*.hum")):
    for fn in sorted(glob.glob(os.path.join(C, pat))):
        got = BL.read_hum_timed(fn)
        if not got: continue
        ns, L_ = got; q = np.array([a for a, _, _ in ns]); s = np.array([b for _, b, _ in ns])
        spq = float(np.median(np.diff(s)[np.diff(q) > 0] / np.diff(q)[np.diff(q) > 0]))
        meta = {x.group(1): x.group(2) for x in (re.match(r"!!!([^:]+):\s*(.*)", l) for l in open(fn, errors="ignore")) if x}
        if not meta.get("M", "4/4").startswith(("4/4", "2/4", "2/2")) and "*M3/4" in open(fn, errors="ignore").read(): continue
        pk = re.match(r"\d+", meta.get("BillboardPeak", "")); r = readings(list(q), spq)
        if r: r.update(group=grp, file=os.path.basename(fn), peak=int(pk.group(0)) if pk else None); rows.append(r)
for m in csv.DictReader(open(B + "/metadata/bimmuda_per_song_metadata.csv")):
    if m["Time Signature 1"] != "4/4" or m["Time Signature 2"] or m["BPM 2"]: continue
    try: bpm = float(m["BPM 1"])
    except ValueError: continue
    pos = m["Position"].strip(); mm = re.match(r"(\d+)(\w*)", pos)
    fn = f"{B}/bimmuda_dataset/{m['Year']}/{pos}/{m['Year']}_{int(mm.group(1)):02d}{mm.group(2)}_full.mid"
    if not os.path.exists(fn): continue
    mf = mido.MidiFile(fn); t = 0; on = []
    for msg in mido.merge_tracks(mf.tracks):
        t += msg.time
        if msg.type == "note_on" and msg.velocity > 0: on.append(t / mf.ticks_per_beat)
    if len(on) < 40: continue
    r = readings(on, 60.0 / bpm)
    if r: r.update(group="BIM", file=os.path.basename(fn), year=int(m["Year"])); rows.append(r)
for fn in sorted(glob.glob("/home/claude/zeneng-pipeline/songs/p*/lyric*.song.json")):
    ns, L_ = BL.read_record_timed(fn); q = [a for a, _, _ in ns]; R = json.load(open(fn))
    spq = 60.0 / R["bpm"]; r = readings(q, spq)
    if r: r.update(group="LUTHIER", file=fn.split("songs/")[1]); rows.append(r)
def auc(a, b):
    if not a or not b: return None
    u = mannwhitneyu(a, b); return [round(float(u.statistic / (len(a) * len(b))), 3), round(float(u.pvalue), 4), len(a), len(b)]
G = dict(BIM=[r for r in rows if r["group"] == "BIM"], RS=[r for r in rows if r["group"] == "RS"],
         TOP10=[r for r in rows if r["group"] == "BB" and r["peak"] and r["peak"] <= 10], LOW=[r for r in rows if r["group"] == "BB" and r["peak"] and r["peak"] > 20],
         LUTHIER=[r for r in rows if r["group"] == "LUTHIER"])
res = {}
for k in ("four_over_two", "slow_share_beats", "mayer_share", "dom_beats", "dom_s"):
    res[k] = dict(medians={g: round(float(np.median([r[k] for r in v])), 3) for g, v in G.items() if v},
                  BIM_over_LOW=auc([r[k] for r in G["BIM"]], [r[k] for r in G["LOW"]]), TOP10_over_LOW=auc([r[k] for r in G["TOP10"]], [r[k] for r in G["LOW"]]),
                  RS_over_LOW=auc([r[k] for r in G["RS"]], [r[k] for r in G["LOW"]]))
near5 = lambda x: -abs(np.log(x / 4.8))
res["dom_near_4p8s"] = dict(BIM_over_LOW=auc([near5(r["dom_s"]) for r in G["BIM"]], [near5(r["dom_s"]) for r in G["LOW"]]), TOP10_over_LOW=auc([near5(r["dom_s"]) for r in G["TOP10"]], [near5(r["dom_s"]) for r in G["LOW"]]), RS_over_LOW=auc([near5(r["dom_s"]) for r in G["RS"]], [near5(r["dom_s"]) for r in G["LOW"]]))
res["dom_beats_counts"] = {g: dict(__import__("collections").Counter(round(r["dom_beats"]) for r in v).most_common(5)) for g, v in G.items()}
res["luthier"] = [(r["file"], round(r["four_over_two"], 2), round(r["slow_share_beats"], 3), round(r["mayer_share"], 3)) for r in G["LUTHIER"]]
json.dump(dict(res=res, rows=rows), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "breath_spectrum.json"), "w"), indent=1); print(json.dumps(res, indent=1))
