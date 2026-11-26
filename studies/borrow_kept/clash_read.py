"""PREDICTION_clash.md: where clashes arise, v50 and the pair (form 2 with the chord tie).  N=600 python3 clash_read.py"""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import song_from_lyric as SL, metre_engine as M
T7 = json.load(open(os.path.join(ROOT, "tables", "kept_line_repeat.json"))); TIE = json.load(open(os.path.join(ROOT, "tables", "kept_chord_tie.json")))["weights"]; N = int(os.environ.get("N", "600")); out = {}
for name, stem in (("55", "songs/p65/lyric55"), ("49", "songs/p59/lyric49"), ("54", "songs/p64/lyric54"), ("58", "songs/p68/lyric58"), ("50", "songs/p60/lyric50"), ("59", "songs/p69/lyric59")):
    L = json.load(open(os.path.join(ROOT, stem + ".json"))); rec = json.load(open(os.path.join(ROOT, stem + ".song.json"))); o = {}
    for form in ("v50", "the pair"):
        spec = json.loads(json.dumps(rec["spec"]))
        if form == "the pair": spec["borrow_kept"] = dict(T7["share"], by_count=T7["by_count"], true=True); spec["chord_tie"] = TIE
        E = M.Engine(spec); E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
        last = {}; a0, j0 = E.again, E.join
        def again(rng, src, src_st0, sy, U, sec, i, tmin, slot, a0=a0, E=E, last=last):
            r = a0(rng, src, src_st0, sy, U, sec, i, tmin, slot)
            if E.HOW.get((sec, i), ["fresh"])[0] == "fresh": last.clear(); last.update(r=r, key=(sec, i))
            return r
        def join(r, lines, k, sec, i, j0=j0, E=E, last=last):
            r2 = j0(r, lines, k, sec, i)
            if last and r is last.get("r") and r2 is not None: E._b.add(last["key"])
            return r2
        DG = spec.get("degrees") or {}; E.again, E.join = again, join; rng = random.Random(L.get("seed", 1)); C = collections.Counter(); nn = 0; nl = collections.Counter()
        for _ in range(N):
            E._b = set(); c, err = E.build(rng)
            if err or E.gates(c): continue
            raw = collections.defaultdict(list)
            for n in c["notes"]: raw[(n["sec"], n["line"])].append(n["on"])
            for v in raw.values(): v.sort()
            for n in E.as_sung(c["notes"]):
                k = (n["sec"], n["line"]); how = E.HOW.get(k, ["fresh"])[0]; src = "a line borrowed by 818" if k in E._b else "a fresh line" if how == "fresh" else "a line sung again or copied by the plan" if how in ("again", "copy") else "other (" + how + ")"
                nn += 1; nl[src] += 1; ch = E.chord_at(n["on"]); bl = (n["p"] - DG.get("tonic", 0)) % 12 in set(DG.get("blue", ())); nl["blue notes"] += bl; nl["long notes"] += n["dur"] >= E.BEAT; nl["long blue notes"] += bl and n["dur"] >= E.BEAT
                if n["dur"] >= E.BEAT and n["p"] % 12 not in ch and ((n["p"] + 1) % 12 in ch or (n["p"] - 1) % 12 in ch):
                    v = raw[k]; dl = n["on"] in v and (v.index(n["on"]) == len(v) - 1 or v[v.index(n["on"]) + 1] - n["on"] >= E.BEAT)
                    C["a blue note (846 allows it)" if bl else "not a blue note"] += 1; C[src] += 1; C[src + (" | long in the draw's sense" if dl else " | long only as sung")] += 1; C["on the beat" if E.on_beat(n["on"]) else "off the beat"] += 1
        o[form] = dict(notes=nn, clashes_per_100_notes=round(100 * sum(v for k, v in C.items() if "|" not in k and "beat" not in k and "blue" not in k) / nn, 2), by_source_per_100_notes={k: round(100 * v / nn, 3) for k, v in sorted(C.items())}, share_of_notes_by_source={k: round(v / nn, 3) for k, v in nl.items()}, kept_degree_weights_of_the_blue_notes={k: DG["weights"].get(E.KIND.get("Verse 1", "all"), DG["weights"]["all"]).get(str(k)) if isinstance(DG.get("weights", {}).get("all"), dict) else None for k in DG.get("blue", ())})
        print(name, form, json.dumps(o[form]), flush=True)
    out[name] = o
json.dump(out, open(os.path.join(HERE, "clash_read.json"), "w"), indent=1)
