"""Chromatic harmony on the Hooktheory clips (CC BY-NC-SA via Sheet Sage): how much of each clip's harmony lies outside its key,
and of what kind. Writes hooktheory_chromatic.json, one record per clip (same keys as hooktheory_surprise.json).

A chord is a pitch-class set (root plus its intervals). Two homes are used:
- the labelled mode (a Mixolydian song's bVII is at home), and
- plain major/minor: Ionian for modes with a major third, Aeolian plus the leading tone for modes with a minor third
  (so V and vii in minor are at home, and a Mixolydian bVII counts as borrowed).
Measures per clip, by chord time (beats) unless said otherwise:
- chrom: share of chord time outside the labelled mode
- chrom_mm: share of chord time outside plain major/minor
- mixture: share of chord events outside plain major/minor but inside the parallel mode (iv, bVI, bVII, bIII in major; IV, major II in minor via Dorian is NOT counted)
- secdom: share of chord events that are an applied dominant: a major triad or dominant seventh outside plain major/minor whose next chord's root is a fourth above (a fifth below)
- other_chrom: share of chord events outside plain major/minor that are neither of the above
- n_chrom_ev: number of chord events outside plain major/minor; distinct_chrom: number of distinct such chords
- lives: 1 if the clip (a section) has two or more chord events outside plain major/minor"""
import gzip, json
SRC = "/home/claude/chrisdonahue/sheetsage-data/hooktheory/Hooktheory.json.gz"
IONIAN = [0, 2, 4, 5, 7, 9, 11]; AEOLIAN = [0, 2, 3, 5, 7, 8, 10]
def scale(sdi):
    s = [0]
    for x in sdi: s.append(s[-1] + x)
    return set(p % 12 for p in s)
def pcs(c, tonic):
    r = (c["root_pitch_class"] - tonic) % 12; out = {r}; acc = r
    for iv in c["root_position_intervals"]: acc += iv; out.add(acc % 12)
    return r, out
def clip_features(clip):
    a = clip["annotations"]; ks = a.get("keys") or []; H = sorted(a.get("harmony") or [], key=lambda c: c["onset"])
    if not ks or len(H) < 2: return None
    k = ks[0]; tonic = k["tonic_pitch_class"]; mode = scale(k["scale_degree_intervals"])
    major = 4 in mode
    home = set(IONIAN) if major else set(AEOLIAN) | {11}
    par = set(AEOLIAN) if major else set(IONIAN)
    ev = []
    for c in H:
        r, P = pcs(c, tonic); key = (r, tuple(c["root_position_intervals"]))
        if ev and ev[-1]["key"] == key: ev[-1]["dur"] += c["offset"] - c["onset"]; continue
        ev.append(dict(key=key, r=r, P=P, iv=tuple(c["root_position_intervals"]), dur=c["offset"] - c["onset"]))
    T = sum(e["dur"] for e in ev) or 1.0; n = len(ev)
    chrom = sum(e["dur"] for e in ev if not e["P"] <= mode) / T
    chrom_mm = sum(e["dur"] for e in ev if not e["P"] <= home) / T
    mix = sec = oth = 0; ch_keys = set(); n_ch = 0
    for i, e in enumerate(ev):
        if e["P"] <= home: continue
        n_ch += 1; ch_keys.add(e["key"])
        nxt = ev[i + 1]["r"] if i + 1 < n else None
        if e["iv"] in ((4, 3), (4, 3, 3)) and nxt is not None and (nxt - e["r"]) % 12 == 5: sec += 1
        elif e["P"] <= par: mix += 1
        else: oth += 1
    return dict(chrom=chrom, chrom_mm=chrom_mm, mixture=mix / n, secdom=sec / n, other_chrom=oth / n, n_chrom_ev=n_ch,
                distinct_chrom=len(ch_keys), lives=1.0 if n_ch >= 2 else 0.0, n_ev=n, major=1.0 if major else 0.0, labelled_mode_mm=1.0 if mode in (set(IONIAN), set(AEOLIAN)) else 0.0, nkeys=len(ks))
if __name__ == "__main__":
    D = json.load(gzip.open(SRC)); out = {}
    for kk, c in D.items():
        f = clip_features(c)
        if f: out[kk] = f
    json.dump(out, open("/home/claude/shape/hooktheory_chromatic.json", "w"))
    import numpy as np
    A = list(out.values()); print(len(A), "clips")
    for f in ("chrom", "chrom_mm", "mixture", "secdom", "other_chrom", "lives"):
        x = np.array([a[f] for a in A]); print("%-12s mean %.3f  median %.3f  share>0 %.2f" % (f, x.mean(), np.median(x), (x > 0).mean()))
