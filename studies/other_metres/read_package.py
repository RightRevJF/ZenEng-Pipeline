"""A 6/8 package record read whole: the marks' figures (read_6_8_lyric.py), the lyric's "again" drawn fresh (712), the switches the record carries, whether the judge ran, the share of lines beginning after their bar line, and what is met and missed.
python3 studies/other_metres/read_package.py LYRIC.json RECORD.song.json LIMIT_712|none -> prints one JSON object"""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [HERE, os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import metre_engine as M, read_6_8_lyric as RL
KEYS = ("table", "title_entry_pickup", "title_840", "again_inside", "again_refit", "title_fresh", "title_nowait", "copy_join", "section_density", "title_room", "kept_rests", "kept_rests_rate", "no_pickup_windows", "again_runs", "title_pull", "shared_bars", "stress_place", "title_entry", "title_entry_rest")
def late(record, n=400):
    R = json.load(open(record)); E = M.Engine(R["spec"]); rng = random.Random(1); lt = tot = 0
    for _ in range(n):
        c, err = E.build(rng)
        if err or E.gates(c): continue
        by = collections.defaultdict(list)
        for x in c["notes"]: by[(x["sec"], x["line"])].append(x["on"])
        for (s_, i_), ons in by.items(): tot += 1; lt += min(ons) - E.line_start(s_, i_) > 0
    return round(lt / max(1, tot), 3)
def read(lyric, record, lim):
    d = RL.read(lyric, record); R = json.load(open(record)); sp = R["spec"]; d["switches"] = {k: (bool(sp.get(k)) if k == "stress_place" else sp.get(k)) for k in KEYS}; d["judge_ran"] = "pass_the_gate" in (R.get("judge7") or {}); d["shared_bars"] = sp.get("shared_bars")
    if "pick" not in d: d["missed"] = ["no build survived"]; return d
    s = R["melody"].get("stats") or {}; d["again_drawn_fresh_712"] = sum(v for q, v in s.items() if q.startswith("712")); d["limit_712"] = lim; d["lines_beginning_after_their_bar_line"] = late(record); p, l = d["pick"], d["living"]
    m = [("living and pool", p["living"] >= 30 and (p["pool"] or 0) >= 10), ("notes a bar", 3.6 <= p["notes_a_bar"] <= 4.33 and 3.6 <= l["notes_a_bar"] <= 4.33), ("onsets on the beat", min(p["onsets_on_the_beat"], l["onsets_on_the_beat"]) >= 0.389), ("onsets on the first beat", min(p["onsets_on_the_first_beat"], l["onsets_on_the_first_beat"]) >= 0.211), ("731", l["stressed_on_a_beat_every_build_made_median"] >= 0.4), ("780 and 840", p["deaths_780_in_10"] < 1 and p["deaths_840_in_10"] < 1), ("voice and leap", p["inside_the_voice"] and not p["leap_past_an_octave_in_a_line"]), ("title lines on time", min(d["title lines"]["on_time_in_100"].values()) >= 75), ("the silence before a title line", max(d["title lines"]["silence_before_in_eighths_median"].values()) <= 3), ("the judge ran", d["judge_ran"])]
    if lim is not None: m.append(("712", d["again_drawn_fresh_712"] <= lim))
    d["missed"] = [k for k, v in m if not v]; return d
def line(d):
    if "pick" not in d: return "no build survived"
    p, l = d["pick"], d["living"]; return f"living {p['living']}; pool {p['pool']} | notes a bar {p['notes_a_bar']}; {l['notes_a_bar']} | on the beat {p['onsets_on_the_beat']}; {l['onsets_on_the_beat']} | first beat {p['onsets_on_the_first_beat']}; {l['onsets_on_the_first_beat']} | 731 {l['stressed_on_a_beat_every_build_made_median']} | 840 {p['deaths_840_in_10']} | title {min(d['title lines']['on_time_in_100'].values())} | silence {max(d['title lines']['silence_before_in_eighths_median'].values())} | 712 {d['again_drawn_fresh_712']} (limit {d['limit_712']}) | never made {sum(l['never_made'].values())} | late lines {d['lines_beginning_after_their_bar_line']} | MISSED: {d['missed'] or 'nothing'}"
if __name__ == "__main__":
    d = read(sys.argv[1], sys.argv[2], None if sys.argv[3] == "none" else float(sys.argv[3])); print(json.dumps(d))
