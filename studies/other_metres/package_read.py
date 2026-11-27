"""PREDICTION_package_3_4.md: the package's records read as the kept waltzes are counted.  python3 studies/other_metres/package_read.py NAME=DIR ... -> package_3_4.json"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [HERE, os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas")]
import atlas_build as AB, leadsheet_waltz_figures as LW, chord_writer as C
if __name__ == "__main__":
    out = {}; LL = json.load(open(os.path.join(HERE, "like_length_3_4.json")))["percentiles_10_25_50_75_90"]
    for a in sys.argv[1:]:
        name, d = a.split("=", 1); R = json.load(open(os.path.join(d, "lyric53.song.json"))); m = R["melody"]; j = R["judge7"]; sp = R["spec"]; nn = sorted(m["notes"], key=lambda n: n["on"]); ns = [[n["on"], n["dur"], n["midi"]] for n in nn]; f = LW.figs(ns); r = AB.readings(ns, 36, [0, 12, 24], 12)
        phr = sum(sum(v) for v in sp["slots"].values()); st = [n for n in nn if n["stress"] and n.get("melisma") != "second"]; V = C.VOICES["mezzo"]; made = m["made"] - sum(v for k, v in m["deaths"].items() if "780" in k)
        out[name] = dict(made=m["made"], living=m["survivors"], pool=j.get("pass_the_gate"), deaths=m["deaths"], deaths_780=sum(v for k, v in m["deaths"].items() if "780" in k), deaths_840=sum(v for k, v in m["deaths"].items() if k.startswith("840")), bars_of_sung_phrases=phr, notes=len(ns), notes_a_bar_over_sung_phrases=round(len(ns) / phr, 3), onsets_on_a_beat=round(r["onsets on the beat"], 3),
                         stressed_on_first_beat=round(sum(n["on"] % 36 == 0 for n in st) / len(st), 3), range=f["range"], distinct_pitches=f["distinct pitches"], commonest_pitch=round(f["commonest pitch, whole tune"], 3), figure_again=round(f["bars on a figure already sung"], 3), rhythm_again=round(f["bars on a rhythm already sung"], 3), lowest_highest=[min(x[2] for x in ns), max(x[2] for x in ns)], inside_the_voice=bool(V[0] <= min(x[2] for x in ns) and max(x[2] for x in ns) <= V[1]),
                         leap_past_an_octave_in_a_line=bool(any(a_["sec"] == b_["sec"] and a_["line"] == b_["line"] and abs(b_["midi"] - a_["midi"]) > 12 for a_, b_ in zip(nn, nn[1:]))), key=R["key"]["key"], registers=sp["registers"], range_choice=j.get("range_choice"), sung_bars=sp.get("sung_bars"), title_room=sp.get("title_room"), stats={k: v for k, v in (m.get("stats") or {}).items() if "749." in k}, seconds=[x for x in R.get("flags", []) if "seconds" in x])
        print(name, json.dumps({k: v for k, v in out[name].items() if k not in ("sung_bars", "registers", "seconds", "deaths")}))
    out["like_length"] = LL; json.dump(out, open(os.path.join(HERE, "package_3_4.json"), "w"), indent=1)
