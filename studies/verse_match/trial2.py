"""The borrows fitted to the aimed song, with the words held: second trial outside the engine. See PREDICTION2.md. python3 studies/verse_match/trial2.py -> trial2.json (PYTHONHASHSEED=0)"""
import sys, os, json, random, numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas"), os.path.join(ROOT, "studies", "soundness")]
import song_from_lyric as SL, metre_engine as M, soundness as S
FIG, RHY, FIT = "bars on a figure already sung", "bars on a rhythm already sung", "the words' fit, whole"; GRID = ((0.0, 0.0), (0.8, 0.0), (1.0, 0.0), (0.5, 0.5), (0.0, 1.0))
KR = json.load(open(os.path.join(ROOT, "tables", "metre_atlas", "kept_readings.json")))["4-4_pop_sung"]; Wd = {c: float(np.subtract(*np.percentile([r[KR["names"].index(c)] for r in KR["rows"]], (75, 25)))) for c in (FIG, RHY)}
def row(ns): return S.record_row(dict(melody=dict(notes=[dict(n, midi=n["p"]) for n in sorted(ns, key=lambda n: n["on"])]), checks={"the chorus's median over the verse's, semitones": 0, "rest share inside sung sections": 0}))
def run(spec, L, tg, f, r, tries, seed):
    s2 = json.loads(json.dumps(spec)); s2["borrow"] = dict(figure=f, rhythm=r); E = M.Engine(s2); rng = random.Random(seed); rows = []
    for _ in range(tries):
        c, err = E.build(rng)
        if err or E.gates(c): continue
        x = row(SL.melisma_notes(c["notes"], L, set(spec["scale"]), key="p", how=spec.get("how"), cap=tg.get("run"), share=tg.get("melisma_share"))[0]); rows.append({k: x[k] for k in (FIG, RHY, FIT, "rhythm scaling")})
    return dict(builds=len(rows), **{k: round(float(np.median([x[k] for x in rows])), 3) for k in rows[0]}) if rows else dict(builds=0)
out = {}
for tag, p in (("55", "songs/p65/lyric55"), ("54", "songs/p64/lyric54"), ("58", "songs/p68/lyric58"), ("59", "songs/p69/lyric59")):
    spec = json.load(open(os.path.join(ROOT, p + ".song.json")))["spec"]; L = json.load(open(os.path.join(ROOT, p + ".json"))); tg = spec["target"]; aim = dict(zip(KR["names"], KR["rows"][tg["kept_song_row"]]))
    gap = lambda d: round(sum(abs(d[c] - aim[c]) / Wd[c] for c in (FIG, RHY)), 3)
    fits = {g: run(spec, L, tg, g[0], g[1], 80, f"second fit {tag}") for g in GRID}; best = min((g for g in GRID if fits[g]["builds"] >= 8 and fits[g][FIT] >= fits[(0.8, 0.0)][FIT] - 0.03), key=lambda g: gap(fits[g]))
    a = run(spec, L, tg, 0.8, 0.0, 150, 44); b = a if best == (0.8, 0.0) else run(spec, L, tg, best[0], best[1], 150, 44)
    out[tag] = dict(aims_at=tg["kept_song"], aim={c: round(float(aim[c]), 3) for c in (FIG, RHY)}, fit={f"figure {g[0]}, rhythm {g[1]}": dict(fits[g], gap=gap(fits[g])) for g in GRID}, chosen=dict(figure=best[0], rhythm=best[1]),
                    the_engines_setting=dict(a, gap=gap(a)), the_fitted_setting=dict(b, gap=gap(b)), gap_change=round(gap(b) - gap(a), 3), words_fit_change=round(b[FIT] - a[FIT], 3), builds_share=round(b["builds"] / max(a["builds"], 1), 2))
    print(tag, json.dumps({k: v for k, v in out[tag].items() if k != "fit"}), flush=True)
T3 = ("55", "54", "58"); c1 = sum(out[t]["gap_change"] < 0 for t in T3) >= 2 and all(out[t]["gap_change"] <= 0.05 for t in T3); c2 = all(out[t]["words_fit_change"] >= -0.03 for t in T3); c3 = all(out[t]["builds_share"] >= 0.8 for t in T3)
h = out["59"]["chosen"]["figure"] + out["59"]["chosen"]["rhythm"] < 0.8 and out["59"]["gap_change"] < 0
out["checks"] = {"1 nearer the aim": bool(c1), "2 the words hold": bool(c2), "3 builds survive": bool(c3), "passes on the practice songs": bool(c1 and c2 and c3), "the hold-out's prediction holds": bool(h), "built": bool(c1 and c2 and c3 and h)}; print(out["checks"])
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "trial2.json"), "w"), indent=1)
