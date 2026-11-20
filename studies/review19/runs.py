"""Where 926's deaths come from: for builds that die by the across-lines run gate, where is the long run?"""
# Review 19 (Luthier v32). Run from the repo root with PYTHONHASHSEED=0.
import sys, os, json, random, collections
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path.insert(0, os.path.join(ROOT, "lib", "luthier"))
import song_from_lyric as SL, metre_engine as M
def longest(ps):
    best = (0, 0); i = 0
    while i < len(ps):
        j = i
        while j + 1 < len(ps) and ps[j + 1] == ps[i]: j += 1
        if j - i + 1 > best[0]: best = (j - i + 1, i)
        i = j + 1
    return best
out = {}
for tag, lp in (("54", "songs/p64/lyric54.json"), ("55", "songs/p65/lyric55.json"), ("58", "songs/p68/lyric58.json")):
    R = json.load(open(os.path.join(ROOT, {"54": "songs/p64", "55": "songs/p65", "58": "songs/p68"}[tag], f"lyric{tag}.song.json"))); L = json.load(open(os.path.join(ROOT, lp))); spec = R["spec"]
    E = M.Engine(spec); E.as_sung = lambda ns_, L=L, spec=spec: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"))[0]
    rng = random.Random(7); C = collections.Counter(); runs = collections.Counter(); N = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    for _ in range(N):
        c, err = E.build(rng)
        if err: C["build failed"] += 1; continue
        g = E.gates(c)
        if not g or not g.startswith("926"): C["other or alive"] += 1; continue
        ns = sorted(c["notes"], key=lambda n: n["on"]); sung = sorted(E.as_sung(ns), key=lambda n: n["on"])
        raw = longest([n["p"] for n in ns]); L_, i = longest([n["p"] for n in sung]); runs[L_] += 1
        seg = sung[i:i + L_]; lines = {(n["sec"], n["line"]) for n in seg}
        if raw[0] <= E.RUN: C["made by a melisma"] += 1
        elif len(lines) == 1: C["inside one line"] += 1
        else:
            hw = [tuple(spec.get("how", {}).get(f"{s}:{l}", ["fresh"]))[0] for s, l in sorted(lines, key=lambda x: min(n["on"] for n in seg if (n["sec"], n["line"]) == x))]
            C["across lines: " + ("a copied or borrowed line in it" if any(h != "fresh" for h in hw) else "fresh lines only")] += 1
    out[tag] = dict(cap=E.RUN, counts=dict(C), dead_builds_longest_run=dict(sorted(runs.items())))
    print(tag, out[tag], flush=True)
json.dump(out, open(os.path.join(ROOT, "studies", "review19", "runs.json"), "w"), indent=1)
