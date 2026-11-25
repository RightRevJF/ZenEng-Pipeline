"""The line that carries the top, in kept songs and in the builds (PREDICTION.md).  python3 studies/the_peak_line/read.py -> reading.json"""
import os, sys, json, random, collections, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); Lb = os.path.join(ROOT, "lib", "luthier"); sys.path[:0] = [Lb, os.path.join(Lb, "..", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import kept_corpus as KC, song_from_lyric as SL, metre_engine as M
def measure(lines, part_of):
    """lines: {key: [pitches]} in order; part_of: key -> part. The line that first holds the top."""
    top = max(max(v) for v in lines.values()); key = next((k for k, v in lines.items() if len(v) >= 3 and top in v), None)
    if key is None: return None
    v = lines[key]; j = v.index(top); others = [st.median(w) for k, w in lines.items() if k != key and part_of(k) == part_of(key) and len(w) >= 3]
    d = None if j == 0 else top - v[j - 1]
    return dict(reach=top - st.median(v), lift=(st.median(v) - st.median(others)) if others else None, approach="first note" if d is None else "repeat" if d == 0 else "step" if d <= 2 else "skip" if d <= 7 else "leap" if d <= 12 else "past an octave", part=str(part_of(key)).lower())
def summary(rows):
    q = lambda v: [round(float(x), 1) for x in (sorted(v)[int(0.25 * (len(v) - 1))], st.median(v), sorted(v)[int(0.75 * (len(v) - 1))])]; lf = [r["lift"] for r in rows if r["lift"] is not None]; n = len(rows)
    return dict(n=n, reach_quartiles=q([r["reach"] for r in rows]), lift_quartiles=q(lf), approach={k: round(c / n, 3) for k, c in collections.Counter(r["approach"] for r in rows).most_common()}, part={k: round(c / n, 3) for k, c in collections.Counter(r["part"] for r in rows).most_common()})
out = {}; rows = []
for k in KC.kept_songs():
    lines = collections.OrderedDict(); part = {}
    for i, l in enumerate(k["lines"]): lines.setdefault(l, []).append(int(k["p"][i])); part.setdefault(l, str(k["sec"][i]))
    r = measure(lines, lambda key: part[key])
    if r: rows.append(r)
out["kept"] = summary(rows); print("kept", json.dumps(out["kept"]), flush=True)
for stem in ("songs/p65/lyric55", "songs/p64/lyric54", "songs/p68/lyric58", "songs/p59/lyric49"):
    L = json.load(open(os.path.join(ROOT, stem + ".json"))); rec = json.load(open(os.path.join(ROOT, stem + ".song.json"))); spec = json.loads(json.dumps(rec["spec"])); spec["no_leap_past_an_octave"] = False; E = M.Engine(spec)
    E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
    R = spec["registers"]; P = int(min(min(R[x][1] for x in ("Verse", "Chorus")) + round(spec["target"]["peak"]["range"]), max(R[x][2] for x in ("Verse", "Chorus", "Bridge") if x in R)))
    while P % 12 not in E.SCALE: P -= 1
    rng = random.Random(L.get("seed", 1)); rows = []
    for _ in range(1000):
        E._peaked = False; c, err = E.build(rng)
        if err or E.gates(c) or not getattr(E, "_peaked", False): continue
        s = sorted(E.as_sung(c["notes"]), key=lambda n: n["on"]); lines = collections.OrderedDict()
        for n in s: lines.setdefault((n["sec"], n["line"]), []).append(n["p"])
        r = measure(lines, lambda key: E.KIND.get(key[0]))
        if r: rows.append(r)
    o = summary(rows); o["the_plant"] = dict(peak=P, chorus_register_centre_floor_top=R["Chorus"], peak_less_the_chorus_centre=P - R["Chorus"][0]); out[os.path.basename(stem)] = o; print(os.path.basename(stem), json.dumps(o), flush=True)
json.dump(out, open(os.path.join(HERE, "reading.json"), "w"), indent=1)
