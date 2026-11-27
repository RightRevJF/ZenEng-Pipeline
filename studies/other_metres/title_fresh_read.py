"""PREDICTION_title_fresh.md: song 52's record read.  python3 studies/other_metres/title_fresh_read.py DIR -> title_fresh.json (the marks by package_6_8_read's own reading; the title lines and 818 counted here)"""
import os, sys, json, random, collections, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [HERE, os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import metre_engine as M
d = sys.argv[1]; keep = open(os.path.join(HERE, "package_6_8.json")).read(); subprocess.check_call([sys.executable, os.path.join(HERE, "package_6_8_read.py"), "fresh=" + d], stdout=subprocess.DEVNULL); out = json.load(open(os.path.join(HERE, "package_6_8.json"))); open(os.path.join(HERE, "package_6_8.json"), "w").write(keep)   # the earlier trial's file is put back as it was
R = json.load(open(os.path.join(d, "lyric52.song.json"))); sp = R["spec"]; E = M.Engine(sp); rng = random.Random(1); made = 0; d840 = 0; late840 = 0; on = collections.Counter(); how = collections.defaultdict(collections.Counter); other = 0; hooks = list(sp.get("hooks", ()))
for _ in range(1000):
    c, err = E.build(rng)
    if err: continue
    made += 1; g = E.gates(c) or ""; d840 += g.startswith("840"); ok = True
    for h in hooks:
        s_, i_ = h.rsplit(":", 1); U = E.line_start(s_, int(i_)); o = min(n["on"] - U for n in c["notes"] if n["sec"] == s_ and n["line"] == int(i_)); on[h] += o <= 0; ok = ok and o <= 0; how[h][E._made.get((s_, int(i_)), "?")] += 1
    late840 += g.startswith("840") and not ok; other += any(v == "818 again" for (s_, i_), v in E._made.items() if s_ == "Chorus 1" and f"{s_}:{i_}" not in hooks)
out["title lines"] = dict(builds_made=made, on_time_in_100={h: round(100 * on[h] / made, 1) for h in hooks}, how_made={h: dict(how[h]) for h in hooks}, deaths_on_840=d840, deaths_on_840_in_10=round(10 * d840 / made, 2), of_them_with_a_title_line_late=late840, chorus_builds_in_100_where_another_line_sings_an_earlier_one_again=round(100 * other / made, 1))
json.dump(out, open(os.path.join(HERE, "title_fresh.json"), "w"), indent=1); f = out["fresh"]; l = out["living builds"]
print(json.dumps({k: f[k] for k in ("made", "living", "pool", "deaths_780_in_10", "deaths_840_in_10", "notes_a_bar_over_sung_phrases", "onsets_on_the_beat", "onsets_on_the_first_beat", "inside_the_voice", "leap_past_an_octave_in_a_line")})); print(json.dumps({k: v for k, v in l.items() if k in ("made", "living", "medians", "not_made")})); print([k for k in l]); print(json.dumps(out["title lines"]))
