"""PREDICTION_package_6_8.md: song 52's records read, the chosen tune and the living builds.  python3 studies/other_metres/package_6_8_read.py NAME=DIR ... (the first is read in full) -> package_6_8.json"""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [HERE, os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np, song_from_lyric as SL, metre_engine as M, atlas_build as AB, chord_writer as C
def tune(R):
    m = R["melody"]; j = R["judge7"]; sp = R["spec"]; nn = sorted(m["notes"], key=lambda n: n["on"]); ns = [[n["on"], n["dur"], n["midi"]] for n in nn]; r = AB.readings(ns, 36, [0, 18], 18); phr = sum(sum(v) for v in sp["slots"].values()); st = [n for n in nn if n["stress"] and n.get("melisma") != "second"]; d = m["deaths"]
    d780 = sum(v for k, v in d.items() if "780" in k); d840 = sum(v for k, v in d.items() if k.startswith("840")); V = C.VOICES[json.load(open(os.path.join(ROOT, "songs", "p62", "lyric52.json"))).get("voice", "tenor")]
    return dict(made=m["made"], living=m["survivors"], pool=j.get("pass_the_gate"), deaths=d, deaths_780_in_10=round(10 * d780 / m["made"], 2), deaths_840_in_10=round(10 * d840 / max(1, m["made"] - d780), 2), bars_of_sung_phrases=phr, notes=len(ns), notes_a_bar_over_sung_phrases=round(len(ns) / phr, 3), onsets_on_the_beat=round(r["onsets on the beat"], 3), onsets_on_the_first_beat=round(r["onsets on the bar's first beat"], 3),
                stressed_on_a_beat=round(float(np.mean([n["on"] % 36 in (0, 18) for n in st])), 3), stressed_on_the_first_beat=round(float(np.mean([n["on"] % 36 == 0 for n in st])), 3), range=r["range"], distinct_pitches=r["distinct pitches"], lowest_highest=[min(x[2] for x in ns), max(x[2] for x in ns)], voice=list(V), inside_the_voice=bool(V[0] <= min(x[2] for x in ns) and max(x[2] for x in ns) <= V[1]),
                leap_past_an_octave_in_a_line=bool(any(a["sec"] == b["sec"] and a["line"] == b["line"] and abs(b["midi"] - a["midi"]) > 12 for a, b in zip(nn, nn[1:]))), pick_distance=j.get("pick_distance"), joint_gate=j.get("gate"), sung_bars=sp.get("sung_bars"), slots=sp["slots"], title_room=sp.get("title_room"), stats={k: v for k, v in (m.get("stats") or {}).items() if "749." in k}, seconds=[x for x in R.get("flags", []) if "seconds" in x])
if __name__ == "__main__":
    out = {}; L = json.load(open(os.path.join(ROOT, "songs", "p62", "lyric52.json")))
    for k, a in enumerate(sys.argv[1:]):
        name, d = a.split("=", 1); R = json.load(open(os.path.join(d, "lyric52.song.json"))); out[name] = tune(R); print(name, json.dumps({q: v for q, v in out[name].items() if q not in ("sung_bars", "slots", "seconds")}), flush=True)
        if k: continue
        sp = json.loads(json.dumps(R["spec"])); E = M.Engine(sp); E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(sp["scale"]), key="p", how=sp.get("how"), cap=None, share=None, clash=None, relocate=False)[0]; rng = random.Random(L.get("seed", 1)); rows = []; onb_all = []; errs = collections.Counter(); hk = collections.defaultdict(list)
        for _ in range(600):
            c, err = E.build(rng)
            if err: errs[str(err[0])] += 1; continue
            st = [n for n in c["notes"] if n["stress"]]; onb_all.append(float(np.mean([E.on_beat(n["on"]) for n in st])))
            for h in sp.get("hooks", ()):
                s_, i_ = h.rsplit(":", 1); hs = [n for n in st if n["sec"] == s_ and n["line"] == int(i_)]; hk[h].append(float(np.mean([E.on_beat(n["on"]) for n in hs])))
            if E.gates(c): continue
            s = sorted(E.as_sung(c["notes"]), key=lambda n: n["on"]); r = AB.readings([[n["on"], n["dur"], n["p"]] for n in s], 36, [0, 18], 18); s1 = [n for n in s if n["stress"] and n.get("melisma") != "second"]
            rows.append((len(s) / out[name]["bars_of_sung_phrases"], r["onsets on the beat"], r["onsets on the bar's first beat"], float(np.mean([n["on"] % 36 == 0 for n in s1])), r["range"], r["distinct pitches"]))
        a_ = np.array(rows); T = E.T; land = {}
        for h in sp.get("hooks", ()):
            s_, i_ = h.rsplit(":", 1); sy = E.LINES[s_][int(i_)]; land[h] = dict(syllables=len(sy), stressed=sum(1 for x in sy if x[1]), share_of_windows_landing_half_by_bars={b: round(SL._land(T, sy, b), 3) for b in (2, 3, 4)}, bars_given=E.SUNGB.get(id(sy)), under_half_in_builds=round(float(np.mean(np.array(hk[h]) < 0.5)), 3), stressed_on_a_beat_quartiles=[round(float(q), 3) for q in np.percentile(hk[h], (25, 50, 75))])
        out["living builds"] = dict(builds=600, made=len(onb_all), not_made=dict(errs), living=len(a_), medians=dict(notes_a_bar=round(float(np.median(a_[:, 0])), 3), onsets_on_the_beat=round(float(np.median(a_[:, 1])), 3), onsets_on_the_first_beat=round(float(np.median(a_[:, 2])), 3), stressed_on_the_first_beat=round(float(np.median(a_[:, 3])), 3), range=float(np.median(a_[:, 4])), distinct_pitches=float(np.median(a_[:, 5]))), stressed_on_a_beat_every_build_made_quartiles=[round(float(q), 3) for q in np.percentile(onb_all, (25, 50, 75))], title_lines=land)
        print(json.dumps(out["living builds"]), flush=True)
    json.dump(out, open(os.path.join(HERE, "package_6_8.json"), "w"), indent=1)
