"""PREDICTION.md: every clash in a returning line, v50 fitted specs.  N=600 python3 read.py"""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import song_from_lyric as SL, metre_engine as M
out = {}; REST = collections.Counter()
for name, stem in (("55", "songs/p65/lyric55"), ("54", "songs/p64/lyric54"), ("58", "songs/p68/lyric58"), ("49", "songs/p59/lyric49"), ("50", "songs/p60/lyric50"), ("59", "songs/p69/lyric59")):
    L = json.load(open(os.path.join(ROOT, stem + ".json"))); spec = json.load(open(os.path.join(ROOT, stem + ".song.json")))["spec"]; DG = spec.get("degrees") or {}; blue = set(DG.get("blue", ())); E = M.Engine(spec)
    E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
    rng = random.Random(L.get("seed", 1)); C = collections.Counter(); nn = 0; nret = 0
    for _ in range(int(os.environ.get("N", "600"))):
        c, err = E.build(rng)
        if err or E.gates(c): continue
        raw = collections.defaultdict(list)
        for n in c["notes"]: raw[(n["sec"], n["line"])].append((n["on"], n["p"]))
        for v in raw.values(): v.sort()
        for n in E.as_sung(c["notes"]):
            nn += 1; k = (n["sec"], n["line"]); how = E.HOW.get(k, ["fresh"])
            if how[0] not in ("again", "copy"): continue
            nret += 1; ch = E.chord_at(n["on"])
            if (n["p"] - DG.get("tonic", 0)) % 12 in blue or n["dur"] < E.BEAT or n["p"] % 12 in ch or not ((n["p"] + 1) % 12 in ch or (n["p"] - 1) % 12 in ch): continue
            C["clashes in returning lines"] += 1; v = raw[k]; ons = [t for t, _ in v]; U = E.line_start(*k); Us = E.line_start(how[1], how[2]); rel = n["on"] - U
            same = set(E.chord_at(Us + rel)) == set(ch); dl = n["on"] in ons and (ons.index(n["on"]) == len(ons) - 1 or ons[ons.index(n["on"]) + 1] - n["on"] >= E.BEAT)
            mu, lo, hi = E.reg(*k); reach = any((n["p"] + d) % 12 in E.SCALE and (n["p"] + d) % 12 in ch and lo <= n["p"] + d <= hi for d in (-1, 1, -2, 2, -3, 3, -4, 4))
            if same: cause = "D the same chord as the source's"
            elif how[0] == "copy": cause = "A a copied line over another chord"
            elif not dl: cause = "C sung again, long only as sung"
            elif not reach: cause = "B sung again, long in the draw's sense, no chord tone in reach"
            else: cause = "E sung again, long in the draw's sense, a chord tone in reach (not foreseen)"
            C[cause] += 1; C["as sung: " + ("a melisma's second note" if n.get("melisma") == "second" else "a melisma's first note" if n.get("melisma") == "first" else "one note a syllable") + (", long in the draw's sense" if dl else ", long only as sung")] += 1; C[f"how: {how[0]}"] += 1; C["D by how: " + how[0]] += same
            if same: C["D, long in the draw's sense" if dl else "D, long only as sung"] += 1
    t = max(1, C["clashes in returning lines"]); out[name] = dict(notes=nn, notes_in_returning_lines=nret, per_100_notes=round(100 * C["clashes in returning lines"] / nn, 2), counts=dict(C), shares={k_: round(v_ / t, 3) for k_, v_ in sorted(C.items()) if (k_[0] in "ABCDE" and k_[1] == " ") or k_.startswith("as sung")})
    if name != "55": REST.update(C)
    print(name, json.dumps(out[name]), flush=True)
t = max(1, REST["clashes in returning lines"]); out["the other five together"] = {k_: round(v_ / t, 3) for k_, v_ in sorted(REST.items()) if (k_[0] in "ABCDE" and k_[1] == " ") or k_.startswith("as sung")}; print("other five", out["the other five together"])
json.dump(out, open(os.path.join(HERE, "read.json"), "w"), indent=1)
