"""The living builds of a 3/4 record's fitted spec, read as the kept waltzes are counted.  python3 studies/other_metres/package_living.py NAME=DIR ... -> prints; OUT=file.json writes"""
import os, sys, json, random
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [HERE, os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np, song_from_lyric as SL, metre_engine as M, atlas_build as AB, leadsheet_waltz_figures as LW
def living(d, n=600):
    L = json.load(open(os.path.join(ROOT, "songs", "p63", "lyric53.json"))); R = json.load(open(os.path.join(d, "lyric53.song.json"))); sp = json.loads(json.dumps(R["spec"])); E = M.Engine(sp)
    E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(sp["scale"]), key="p", how=sp.get("how"), cap=None, share=None, clash=None, relocate=False)[0]; rng = random.Random(L.get("seed", 1)); rows = []; phr = sum(sum(v) for v in sp["slots"].values())
    for _ in range(n):
        c, err = E.build(rng)
        if err or E.gates(c): continue
        s = sorted(E.as_sung(c["notes"]), key=lambda x: x["on"]); ns = [[x["on"], x["dur"], x["p"]] for x in s]; f = LW.figs(ns); r = AB.readings(ns, 36, [0, 12, 24], 12); st = [x for x in s if x["stress"] and x.get("melisma") != "second"]
        rows.append(dict(notes_a_bar=len(ns) / phr, onsets_on_a_beat=r["onsets on the beat"], first_beat_stress=float(np.mean([x["on"] % 36 == 0 for x in st])), stress_off_the_beat=float(np.mean([x["on"] % 12 != 0 for x in st])), range=f["range"], pitches=f["distinct pitches"], commonest=f["commonest pitch, whole tune"], figure_again=f["bars on a figure already sung"], rhythm_again=f["bars on a rhythm already sung"]))
    a = {k: np.array([x[k] for x in rows]) for k in rows[0]}; o = dict(builds=n, living=len(rows), medians={k: round(float(np.median(v)), 3) for k, v in a.items()}, quartiles={k: [round(float(q), 3) for q in np.percentile(v, (25, 50, 75))] for k, v in a.items()})
    r3 = a["first_beat_stress"] >= 0.583; r4 = (a["range"] >= 13.75) & (a["pitches"] >= 9); r5 = a["commonest"] <= 0.275
    o["in_100"] = dict(R3_stress=round(100 * float(r3.mean()), 1), R4=round(100 * float(r4.mean()), 1), R5=round(100 * float(r5.mean()), 1), R4_and_R5=round(100 * float((r4 & r5).mean()), 1), R3_R4_R5=round(100 * float((r3 & r4 & r5).mean()), 1)); return o
if __name__ == "__main__":
    out = {}
    for a_ in sys.argv[1:]:
        name, d = a_.split("=", 1); out[name] = living(d); print(name, json.dumps(out[name]), flush=True)
    if os.environ.get("OUT"): json.dump(out, open(os.path.join(HERE, os.environ["OUT"]), "w"), indent=1)
