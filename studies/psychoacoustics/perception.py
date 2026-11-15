"""Perception checks for a song record (timeline of voices, ticks = twelfths of a quarter, MIDI pitches; chords as lists):
  1 roughness   Sethares' (1993) Plomp-Levelt roughness of every sounding set, notes given 6 harmonics at amplitude 0.88^n; per
                slice and per bar. Register-aware low-interval check: an adjacent pair below the traditional low-interval limit
                for its size (an arranger's rule of thumb; the model only ranks these, it has not been tested against listeners).
  2 masking     at each onset of the top sung line: accompaniment above it (top-voice salience lost), and accompaniment a second or less
                from it (well inside its critical band; a third below is ordinary harmony, a unison or octave a doubling); sustained accompaniment in the octave below.
  3 streaming   per line: share of moves of a step or less (pitch proximity), leaps over a fifth; choir crossings; inner organ
                notes fused with the tune (unison against it, or in parallel perfect intervals with it).
  4 phrases     the sung line's phrases in seconds (split at rests of a beat or more), against the 8-second memory limit.
Usage: python3 perception.py record.json [record2.json ...]"""
import json, sys, math, collections
import numpy as np
LOW_LIMIT = {1: 52, 2: 51, 3: 48, 4: 46, 5: 46, 6: 47, 7: 34, 8: 41, 9: 41, 10: 41, 11: 41}   # lowest note of the pair: E3, Eb3, C3, Bb2, Bb2, B2, Bb1, F2...
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
def erb(f): return 24.7 * (4.37 * f / 1000 + 1)
def sethares(f1, f2, a1, a2):
    s = 0.24 / (0.0207 * min(f1, f2) + 18.96); d = abs(f2 - f1)
    return a1 * a2 * (math.exp(-3.5 * s * d) - math.exp(-5.75 * s * d))
def roughness(pitches, nh=6):
    parts = [(hz(p) * n, 0.88 ** (n - 1)) for p in pitches for n in range(1, nh + 1)]
    r = 0.0
    for i in range(len(parts)):
        for j in range(i + 1, len(parts)): r += sethares(parts[i][0], parts[j][0], parts[i][1], parts[j][1])
    return r
def ps(e): return e["p"] if isinstance(e["p"], list) else [e["p"]]
def sounding(V, names, t):
    out = []
    for n in names:
        for e in V.get(n, []):
            if e["on"] <= t < e["on"] + e["dur"]: out += [(q, n, e) for q in ps(e)]
    return out
CHOIR = ["S", "A", "T", "B", "Desc"]; ORG = ["org_rh", "org_rh_in", "org_lh", "org_ped"]
def check(rec, qpm=None):
    V = rec["voices"]; qpm = qpm or rec.get("qpm", 88); sec_per_tick = 60.0 / qpm / 12; BAR = 36
    onsets = sorted({e["on"] for v in CHOIR + ORG for e in V.get(v, [])})
    # 1 roughness and low intervals
    rough, low_viol = [], []
    for t in onsets:
        S = sorted({q for q, _, _ in sounding(V, CHOIR + ORG, t)})
        if len(S) < 2: continue
        rough.append((t, roughness(S) / max(1, len(S) - 1)))
        org = sorted({q for q, _, _ in sounding(V, ORG, t)})
        for a, b in zip(org, org[1:]):
            iv = b - a
            if 0 < iv < 12 and a < LOW_LIMIT[iv]: low_viol.append((t // BAR + 1, a, b))
    R = np.array([r for _, r in rough])
    # 2 masking of the top sung line
    top_line = []
    for v in ("S", "Desc"):
        for e in V.get(v, []): top_line.append((e["on"], max(ps(e)), v))
    top_line = sorted({t: (t, p, v) for t, p, v in sorted(top_line, key=lambda x: (x[0], x[1]))}.values())
    above = within = sustained_below = 0; n_top = 0
    for t, p, v in top_line:
        acc = [(q, n, e) for q, n, e in sounding(V, ORG, t)]
        if not acc: continue
        n_top += 1; f = hz(p)
        if any(q > p for q, _, _ in acc): above += 1
        if any(q != p and (q - p) % 12 != 0 and abs(q - p) <= 2 for q, _, _ in acc): within += 1          # a second from the tune: inside its critical band, and not a chord's third
        if any(p - 12 <= q < p and e["on"] < t and e["on"] + e["dur"] > t + 12 for q, _, e in acc): sustained_below += 1
    # 3 streaming
    def line_stats(v, pick=max):
        ev = sorted(V.get(v, []), key=lambda e: e["on"]); seq = [pick(ps(e)) for e in ev]
        mv = [abs(b - a) for a, b in zip(seq, seq[1:]) if b != a or True]
        return dict(notes=len(seq), steps=float(np.mean([m <= 2 for m in mv])) if mv else None, leaps_over_fifth=float(np.mean([m > 7 for m in mv])) if mv else None)
    lines = {v: line_stats(v) for v in CHOIR + ["org_rh", "org_rh_in"] if V.get(v)}
    crossings = 0
    for t in sorted({e["on"] for v in ("S", "A", "T", "B") for e in V[v]}):
        cur = {v: [q for q, _, _ in sounding(V, [v], t)] for v in ("S", "A", "T", "B")}
        if all(cur.values()):
            s, a, tt, b = (max(cur["S"]), max(cur["A"]), max(cur["T"]), max(cur["B"]))
            if not (s >= a >= tt >= b): crossings += 1
    fused = 0; inner_n = 0
    for e in V.get("org_rh_in", []):
        tune = [q for q, _, _ in sounding(V, ["S"], e["on"])]
        if not tune: continue
        inner_n += 1
        if max(ps(e)) == max(tune): fused += 1
    # 4 phrases in seconds (top sung line, split at rests of a beat or more)
    S_ev = sorted(V["S"], key=lambda e: e["on"]); phrases = []; start = S_ev[0]["on"]
    for a, b in zip(S_ev, S_ev[1:]):
        if b["on"] - (a["on"] + a["dur"]) >= 12: phrases.append((a["on"] + a["dur"] - start) * sec_per_tick); start = b["on"]
    phrases.append((S_ev[-1]["on"] + S_ev[-1]["dur"] - start) * sec_per_tick)
    by_line = collections.OrderedDict()
    for e in S_ev:
        key = (e.get("part"), e.get("line"), e["on"] // (16 * BAR)) if e.get("line") is not None else None
        if key is None: continue
        by_line.setdefault(key, []).append(e)
    line_s = [((L[-1]["on"] + L[-1]["dur"]) - L[0]["on"]) * sec_per_tick for L in by_line.values()]
    return dict(roughness_mean=float(R.mean()), roughness_p90=float(np.percentile(R, 90)), roughest_bars=[int(t // BAR + 1) for t, r in sorted(rough, key=lambda x: -x[1])[:5]],
                low_interval_violations=len(low_viol), low_interval_examples=low_viol[:6],
                top_line_onsets=n_top, accomp_above_share=above / max(1, n_top), accomp_within_second_share=within / max(1, n_top), sustained_below_share=sustained_below / max(1, n_top),
                lines=lines, choir_crossings=crossings, inner_fused_with_tune_share=fused / max(1, inner_n),
                phrases_s=[round(x, 1) for x in phrases], phrases_over_8s=int(sum(x > 8 for x in phrases)), phrase_median_s=float(np.median(phrases)),
                lyric_line_s_median=float(np.median(line_s)) if line_s else None, lyric_lines_over_8s=int(sum(x > 8 for x in line_s)), lyric_lines=len(line_s))
if __name__ == "__main__":
    for p in sys.argv[1:]:
        r = check(json.load(open(p)))
        print(p)
        for k in ("roughness_mean", "roughness_p90", "roughest_bars", "low_interval_violations", "low_interval_examples", "accomp_above_share", "accomp_within_second_share",
                  "sustained_below_share", "choir_crossings", "inner_fused_with_tune_share", "phrases_over_8s", "phrase_median_s", "lyric_line_s_median", "lyric_lines_over_8s", "lyric_lines"):
            v = r[k]; print("   %-28s %s" % (k, round(v, 3) if isinstance(v, float) else v))
        print("   lines", {k: (v["steps"] and round(v["steps"], 2), v["leaps_over_fifth"] and round(v["leaps_over_fifth"], 2)) for k, v in r["lines"].items()})
