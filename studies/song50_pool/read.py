"""749.195 and 749.196 on the builds: each v50 record's fitted spec, a thousand builds.  python3 studies/song50_pool/read.py -> builds.json"""
import os, sys, json, random, collections, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas")]
import song_from_lyric as SL, metre_engine as M, make_kept_commonest_pitch as CP
out = {}
for name, stem in (("50", "songs/p60/lyric50"), ("55", "songs/p65/lyric55"), ("54", "songs/p64/lyric54"), ("58", "songs/p68/lyric58"), ("49", "songs/p59/lyric49")):
    L = json.load(open(os.path.join(ROOT, stem + ".json"))); rec = json.load(open(os.path.join(ROOT, stem + ".song.json"))); spec = json.loads(json.dumps(rec["spec"])); spec["count_the_tail"] = True; E = M.Engine(spec)
    E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
    cei = spec["pitch_ceiling"]; R = spec["registers"]; rng = random.Random(L.get("seed", 1)); sh = collections.defaultdict(list); where = collections.Counter(); over = collections.Counter(); nb = 0
    for _ in range(1000):
        c, err = E.build(rng)
        if err or E.gates(c): continue
        nb += 1; s = sorted(E.as_sung(c["notes"]), key=lambda n: n["on"]); by = collections.defaultdict(list)
        for n in s: by[CP.kind(n["sec"])].append(n["p"])
        for k, ps in by.items():
            if k not in cei: continue
            p0, cnt = collections.Counter(ps).most_common(1)[0]; sh[k].append(cnt / len(ps)); over[k] += cnt / len(ps) > cei[k]
            lo, hi = min(ps), max(ps); where[(k, "the bottom third" if p0 - lo <= (hi - lo) / 3 else "the top third" if hi - p0 <= (hi - lo) / 3 else "the middle")] += 1
    q = lambda v: [round(x, 3) for x in (sorted(v)[int(.25 * (len(v) - 1))], st.median(v), sorted(v)[int(.75 * (len(v) - 1))])]
    out[name] = dict(living=nb, ceilings=cei, registers={k: R[k] for k in ("Verse", "Chorus") if k in R}, voice=L.get("voice"), asked_range=(spec["target"].get("peak") or {}).get("range"), commonest_pitch_share_quartiles={k: q(v) for k, v in sh.items()}, builds_over_the_ceiling={k: round(over[k] / nb, 3) for k in sh},
                     the_commonest_pitch_sits={k: {w: round(c / nb, 3) for (kk, w), c in where.items() if kk == k} for k in sh}, notes_weighed=getattr(E, "_tail_n", 0), sides_with_pitches_past_the_octave_and_no_octave=getattr(E, "_tail_no_octave", 0),
                     per_1000_notes=round(1000 * getattr(E, "_tail_no_octave", 0) / max(1, getattr(E, "_tail_n", 0)), 2))
    print(name, json.dumps(out[name]), flush=True)
json.dump(out, open(os.path.join(HERE, "builds.json"), "w"), indent=1)
