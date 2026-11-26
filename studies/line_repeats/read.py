"""How a line repeats an earlier line (PREDICTION.md).  python3 read.py kept | python3 read.py builds"""
import os, sys, json, random, collections, math
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np
def deg(p, tonic, scale):
    """a pitch as a step of the scale (seven to the octave); a note off the scale takes the scale note under it"""
    d = (p - tonic) % 12; o = (p - tonic) // 12
    while d not in scale: d -= 1
    return 7 * o + scale.index(d)
def repeat(a, b):
    """does b (later) repeat a? returns the height in scale steps, or None"""
    m = min(len(a), len(b))
    if m < 4: return None
    ia = [a[k + 1] - a[k] for k in range(m - 1)]; ib = [b[k + 1] - b[k] for k in range(m - 1)]
    if sum(x == y for x, y in zip(ia, ib)) < math.ceil(0.8 * (m - 1)): return None
    return int(np.median([b[k] - a[k] for k in range(m)]))
def part(lines):
    """lines: lists of scale steps in order. For each line from the second: (repeats i-1 or i-2?, its height), (repeats any earlier?, the height of the nearest)"""
    out = []
    for i in range(1, len(lines)):
        if len(lines[i]) < 4: continue
        near = next((h for j in (i - 2, i - 1) if j >= 0 for h in [repeat(lines[j], lines[i])] if h is not None), None)
        anyh = next((h for j in range(i - 1, -1, -1) for h in [repeat(lines[j], lines[i])] if h is not None), None)
        out.append((near, anyh))
    return out
def summary(rows_by_song):
    allr = [r for v in rows_by_song.values() for r in v]; n = max(1, len(allr)); near = [r[0] for r in allr if r[0] is not None]; anyh = [r[1] for r in allr if r[1] is not None]
    bs = [sum(r[0] is not None for r in v) / len(v) for v in rows_by_song.values() if len(v) >= 6]
    hist = collections.Counter(max(-4, min(4, h)) for h in near)
    return dict(lines=len(allr), repeat_the_line_before_or_two_before=round(len(near) / n, 3), repeat_any_earlier_line=round(len(anyh) / n, 3), by_song_10_25_50_75_90=[round(float(x), 3) for x in np.percentile(bs, (10, 25, 50, 75, 90))] if len(bs) >= 5 else None,
                of_those_at_the_same_pitch=round(sum(h == 0 for h in near) / max(1, len(near)), 3), at_another_height=round(sum(h != 0 for h in near) / max(1, len(near)), 3), heights_in_scale_steps={str(k): round(v / max(1, len(near)), 3) for k, v in sorted(hist.items())},
                any_earlier_at_another_height=round(sum(h != 0 for h in anyh) / max(1, len(anyh)), 3))
MAJ = [0, 2, 4, 5, 7, 9, 11]; MIN = [0, 2, 3, 5, 7, 8, 10]
if __name__ != "__main__": pass
elif sys.argv[1] == "kept":
    import kept_corpus as KC
    d = KC.table(); key = {str(s): (int(g.key_pc.iloc[0]), MIN if str(g["mode"].iloc[0]) == "minor" else MAJ) for s, g in d.groupby("song", sort=False)}; R = {"verse": collections.defaultdict(list), "chorus": collections.defaultdict(list)}
    for k in KC.kept_songs():
        if k["song"] not in key: continue
        tonic, scale = key[k["song"]]; cur = None; lines = collections.OrderedDict()
        def flush():
            if cur in R and len(lines) >= 2: R[cur][k["song"]] += part(list(lines.values()))
        for i, (l, s) in enumerate(zip(k["lines"], k["sec"])):
            if str(s) != cur: flush(); cur = str(s); lines = collections.OrderedDict()
            lines.setdefault(l, []).append(deg(int(k["p"][i]), tonic, scale))
        flush()
    out = {p: summary(v) for p, v in R.items()}; json.dump(out, open(os.path.join(HERE, "kept.json"), "w"), indent=1); print(json.dumps(out, indent=1))
else:
    import song_from_lyric as SL, metre_engine as M, make_kept_commonest_pitch as CP
    out = {}
    for name, stem in (("55", "songs/p65/lyric55"), ("54", "songs/p64/lyric54"), ("58", "songs/p68/lyric58"), ("49", "songs/p59/lyric49"), ("50", "songs/p60/lyric50"), ("59", "songs/p69/lyric59")):
        L = json.load(open(os.path.join(ROOT, stem + ".json"))); spec = json.load(open(os.path.join(ROOT, stem + ".song.json")))["spec"]; E = M.Engine(spec); scale = sorted(spec["scale"])
        E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
        rng = random.Random(L.get("seed", 1)); R = {"Verse": collections.defaultdict(list), "Chorus": collections.defaultdict(list)}; nb = 0
        for _ in range(300):
            c, err = E.build(rng)
            if err or E.gates(c): continue
            nb += 1; by = collections.OrderedDict()
            for n in sorted(E.as_sung(c["notes"]), key=lambda n: n["on"]):
                if n.get("melisma") == "second": continue
                by.setdefault(n["sec"], collections.OrderedDict()).setdefault(n["line"], []).append(deg(n["p"], 0, scale))
            for sec, lines in by.items():
                kd = CP.kind(sec)
                if kd in R and len(lines) >= 2: R[kd][nb] += part(list(lines.values()))
        out[name] = {p: summary(v) for p, v in R.items()}; print(name, json.dumps({p: {k: v[k] for k in ("repeat_the_line_before_or_two_before", "repeat_any_earlier_line", "of_those_at_the_same_pitch", "at_another_height", "heights_in_scale_steps")} for p, v in out[name].items()}), flush=True)
    json.dump(out, open(os.path.join(HERE, "builds.json"), "w"), indent=1)
