"""The rhythm layer: for every Hooktheory clip with a melody, (1) rhythm surprise and uncertainty from the same kind of model as the
pitch layer (orders 0 to 3, five folds by video), on a rhythm token per note = position in the bar on a sixteenth grid, length class,
and whether a rest of half a beat or more came before; (2) descriptors:
  syncopation   per note, Longuet-Higgins & Lee style: a note on a weaker position held across a stronger one adds the difference in
                metrical weight (4/4: bar 0, half-bar -1, beats -2, eighths -3, sixteenths -4; 3/4 and 6/4 on their own beat grid)
  rest share    share of the clip's beats with no melody sounding; long rests = rests of a beat or more, per bar
  phrases       melody spans between rests of a beat or more: mean length in beats, their spread (CV), share starting on a downbeat
  density       notes per beat; length variety = entropy of the length classes
Writes hooktheory_rhythm.json (per clip) and, for clips timed to their video, per-note rhythm IC into clip_rhythm_events.json."""
import gzip, json, math, collections, sys
import numpy as np
sys.path.insert(0, "/home/claude/shape")
import surprise_hooktheory as SH
LCLS = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 99]
def lcls(d): return next(i for i, b in enumerate(LCLS) if d <= b + 1e-6)
def weights(bpb):
    n = int(round(bpb * 4)); w = []
    for p in range(n):
        if p == 0: w.append(0)
        elif bpb == 4 and p == 8: w.append(-1)
        elif bpb == 6 and p == 12: w.append(-1)
        elif p % 4 == 0: w.append(-2)
        elif p % 2 == 0: w.append(-3)
        else: w.append(-4)
    return w
def analyse(c):
    a = c["annotations"]; m0 = a["meters"][0] if a.get("meters") else {"beats_per_bar": 4, "beat_unit": 4}
    bpb = m0["beats_per_bar"] if m0["beat_unit"] == 4 else m0["beats_per_bar"] / 2
    if bpb not in (2, 3, 4, 6): return None
    W = weights(bpb); n16 = len(W); mel = sorted(a.get("melody") or [], key=lambda n: n["onset"])
    if len(mel) < 12: return None
    toks, sync, lens = [], [], []; prev_off = None
    for n in mel:
        on, off = n["onset"], n["offset"]; d = max(0.0625, off - on); p = int(round(on * 4)) % n16
        rest = prev_off is not None and on - prev_off >= 0.5
        toks.append(min(p, 15) * 16 + lcls(d) * 2 + int(rest)); lens.append(lcls(d))
        s16, e16 = int(round(on * 4)), int(round(off * 4)); best = W[p]
        for q in range(s16 + 1, e16):
            best = max(best, W[q % n16])
        sync.append(best - W[p]); prev_off = off
    nb = a["num_beats"]; covered = np.zeros(int(math.ceil(nb * 4)) + 1, bool)
    for n in mel: covered[int(round(n["onset"] * 4)):int(round(n["offset"] * 4))] = True
    span = covered[:int(nb * 4)] if nb > 0 else covered
    phrases, start = [], mel[0]
    for x, y in zip(mel, mel[1:]):
        if y["onset"] - x["offset"] >= 1.0: phrases.append((start["onset"], x["offset"])); start = y
    phrases.append((start["onset"], mel[-1]["offset"])); pl = np.array([e - s for s, e in phrases])
    long_rests = sum(1 for x, y in zip(mel, mel[1:]) if y["onset"] - x["offset"] >= 1.0)
    lc = np.bincount(lens, minlength=len(LCLS)) / len(lens); ent = float(-(lc[lc > 0] * np.log2(lc[lc > 0])).sum())
    return dict(toks=toks, sync_per_note=float(np.mean(sync)), sync_share=float(np.mean(np.array(sync) > 0)), rest_share=float(1 - span.mean()) if len(span) else 0.0,
                long_rests_per_bar=long_rests / max(1, nb / bpb), phrase_mean=float(pl.mean()), phrase_cv=float(pl.std() / pl.mean()) if pl.mean() > 0 else 0.0,
                phrase_on_downbeat=float(np.mean([int(round(s * 4)) % n16 == 0 for s, _ in phrases])), density=len(mel) / max(1, nb), length_variety=ent, bpb=bpb,
                onsets=[n["onset"] for n in mel])
if __name__ == "__main__":
    D = json.load(gzip.open(SH.SRC)); rows = []
    for k, c in D.items():
        yt = c.get("youtube") or {}
        if not yt.get("id"): continue
        r = analyse(c)
        if r: r.update(k=k, vid=yt["id"]); rows.append(r)
    vids = sorted({r["vid"] for r in rows}); rng = np.random.default_rng(5); fold = {v: int(rng.integers(5)) for v in vids}
    ev = {}
    for f in range(5):
        tr = [r for r in rows if fold[r["vid"]] != f]; te = [r for r in rows if fold[r["vid"]] == f]
        mdl = SH.VOM(256).fit([r["toks"] for r in tr])
        for r in te:
            ic, h = SH.score(mdl, r["toks"]); r["rhy_ic"] = ic; r["rhy_h"] = h
        print("fold", f, flush=True)
    IC = np.concatenate([r["rhy_ic"] for r in rows]); H = np.concatenate([r["rhy_h"] for r in rows]); mi, si, mh, sh = IC.mean(), IC.std(), H.mean(), H.std()
    out = []
    for r in rows:
        ic, h = np.array(r.pop("rhy_ic")), np.array(r.pop("rhy_h")); ons = r.pop("onsets"); r.pop("toks")
        ev[r["k"]] = [(o, round(float(i), 3), round(float(x), 3)) for o, i, x in zip(ons, ic, h)]
        r.update(rhy_ic_mean=float(ic.mean()), rhy_h_mean=float(h.mean()), rhy_cheung=float(-np.mean(((ic - mi) / si) * ((h - mh) / sh))))
        out.append(r)
    json.dump(out, open("/home/claude/shape/hooktheory_rhythm.json", "w")); json.dump(ev, open("/home/claude/shape/clip_rhythm_events.json", "w"))
    print(len(out), "clips; rhythm IC mean %.2f bits, H mean %.2f" % (np.mean([r["rhy_ic_mean"] for r in out]), np.mean([r["rhy_h_mean"] for r in out])))
    for f in ("sync_per_note", "sync_share", "rest_share", "long_rests_per_bar", "phrase_mean", "phrase_cv", "phrase_on_downbeat", "density", "length_variety"):
        v = np.array([r[f] for r in out]); print("  %-20s median %.3f  IQR %.3f-%.3f" % (f, np.median(v), np.percentile(v, 25), np.percentile(v, 75)))
