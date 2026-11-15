"""Moments people love. (A) Where in a song listeners' timestamps fall (share of the video's length), overall and by what the comment
names. (B) Inside the Hooktheory clips, which are timed beat by beat to the video: what the music is doing in the four beats from a
timestamp, against every other four-beat window of the same clip (within-clip standard scores, so each song is its own control),
with a lag check from 8 beats before to 8 after."""
import json, re, collections
import numpy as np
Y = json.load(open("/home/claude/dl/shape/youtube/hooktheory_youtube.json"))["videos"]
M = json.load(open("/home/claude/dl/shape/youtube/moments.json")); E = json.load(open("/home/claude/shape/clip_events.json"))
def dur_s(iso):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or ""); return sum(int(x or 0) * k for x, k in zip(m.groups(), (3600, 60, 1))) if m else None
FL = ["chills", "cry", "best", "this_part", "voice", "key_change", "bridge", "drop", "chorus"]
# unique moments per video (timestamps within 2 s merged)
moments = []
for vid, lst in M.items():
    if not lst: continue
    d = dur_s(Y.get(vid, {}).get("duration"))
    if not d or d < 60: continue
    seen = []
    for t in sorted(lst, key=lambda x: x["s"]):
        if t["s"] <= 2 or t["s"] >= d: continue
        if t["n_ts"] > 3: continue                                     # lists of many times (track listings, lyrics timings)
        if seen and t["s"] - seen[-1]["s"] <= 2:
            for k in FL: seen[-1][k] = seen[-1][k] or t[k]
            seen[-1]["n"] += 1; continue
        seen.append(dict(t, n=1, vid=vid, rel=t["s"] / d))
    moments += seen
res = {}
rel = np.array([m["rel"] for m in moments]); bins = np.linspace(0, 1, 11)
res["A"] = dict(moments=len(moments), videos=len({m["vid"] for m in moments}), deciles=[float(x) for x in np.histogram(rel, bins)[0] / len(rel)],
                median_rel=float(np.median(rel)), share_last_third=float(np.mean(rel >= 2 / 3)), share_middle=float(np.mean((rel >= 1 / 3) & (rel < 2 / 3))),
                by_flag={k: dict(n=int(sum(m[k] for m in moments)), median_rel=float(np.median([m["rel"] for m in moments if m[k]])) if any(m[k] for m in moments) else None) for k in FL})
print("A:", res["A"]["moments"], "moments in", res["A"]["videos"], "videos; median at %.2f; last third %.2f" % (res["A"]["median_rel"], res["A"]["share_last_third"]))
print("   deciles", [round(x, 3) for x in res["A"]["deciles"]])
for k, v in res["A"]["by_flag"].items(): print("   %-10s n %5d  median %.2f" % (k, v["n"], v["median_rel"] or -1))
# (B) inside clips
by_vid = collections.defaultdict(list)
for k, c in E.items(): by_vid[c["vid"]].append(c)
def window_feats(c, b0, W=4):
    mel = [x for x in c["mel"] if b0 <= x[0] < b0 + W]; ch = [x for x in c["ch"] if b0 <= x[0] < b0 + W]
    allp = [x[2] for x in c["mel"]]; prev_end = max([x[1] for x in c["mel"] if x[1] <= b0 + 0.01] or [-99])
    first_on = min([x[0] for x in mel] or [None]) if mel else None
    return dict(top=(max(x[2] for x in mel) - np.mean(allp)) if mel else np.nan, onsets=len(mel), mel_ic=max([x[3] for x in mel] or [np.nan]),
                ch_change=float(len(ch) > 0), ch_ic=max([x[1] for x in ch] or [np.nan]), entry=float(bool(mel) and first_on is not None and first_on - prev_end >= 2),
                silence=float(not mel), mel_h_at_peak=(max(mel, key=lambda x: x[3])[4] if mel else np.nan))
F = ["top", "onsets", "mel_ic", "ch_change", "ch_ic", "entry", "silence", "mel_h_at_peak"]
lags = list(range(-8, 9, 2)); Z = {L: collections.defaultdict(list) for L in lags}; hits = 0; hits_flag = collections.Counter()
for m in moments:
    for c in by_vid.get(m["vid"], []):
        t, b = c["times"], c["beats"]
        if not (t[0] <= m["s"] <= t[-1]): continue
        beat = float(np.interp(m["s"], t, b)); nb = int(c["nb"])
        if nb < 16: continue
        hits += 1
        for k in FL:
            if m[k]: hits_flag[k] += 1
        grid = {s: window_feats(c, s) for s in range(0, max(1, nb - 3))}
        for L in lags:
            b0 = int(round(beat)) + L
            if b0 not in grid: continue
            others = [grid[s] for s in grid if abs(s - b0) >= 4]
            for f in F:
                vals = np.array([o[f] for o in others], float); vals = vals[np.isfinite(vals)]
                x = grid[b0][f]
                if not np.isfinite(x) or len(vals) < 4 or vals.std() < 1e-6: continue
                Z[L][f].append(float(np.clip((x - vals.mean()) / vals.std(), -5, 5)))
        break
def ci(a):
    a = np.array(a); bs = [np.mean(np.random.default_rng(i).choice(a, len(a))) for i in range(300)]
    return float(np.mean(a)), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)), len(a)
res["B"] = dict(moments_in_clips=hits, by_flag=dict(hits_flag), lags={str(L): {f: ci(Z[L][f]) for f in F if len(Z[L][f]) > 20} for L in lags})
print("B:", hits, "moments inside aligned clips")
for L in lags:
    print("  lag %+d beats:" % L, {f: "%+.2f [%+.2f,%+.2f]" % v[:3] for f, v in res["B"]["lags"][str(L)].items()})
json.dump(res, open("/home/claude/shape/moments_results.json", "w"), indent=1)
