"""A 6/8 record read against the marks S1 to S7 and U1 to U4, for any lyric.  python3 studies/other_metres/read_6_8_lyric.py LYRIC.json RECORD.song.json -> prints one JSON object
The bars of sung phrases are the sung bars: a rest bar ahead of a title line (749.232 changed) is not counted."""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [HERE, os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np, song_from_lyric as SL, metre_engine as M, atlas_build as AB, chord_writer as C
def read(lyric, record, n_living=600, n_title=1000):
    L = json.load(open(lyric)); R = json.load(open(record)); sp = R["spec"]; out = {}
    if "melody" not in R: return dict(record="no build survived", deaths=R.get("deaths"))
    rest = sp.get("title_entry_rest") or {}; phr = sum(sum(v) for v in sp["slots"].values()) - sum(b - a for a, b in rest.values()) if rest else sum(sum(v) for v in sp["slots"].values())
    m = R["melody"]; j = R["judge7"]; nn = sorted(m["notes"], key=lambda n: n["on"]); ns = [[n["on"], n["dur"], n["midi"]] for n in nn]; r = AB.readings(ns, 36, [0, 18], 18); st = [n for n in nn if n["stress"] and n.get("melisma") != "second"]; d = m["deaths"]; d780 = sum(v for k, v in d.items() if "780" in k); d840 = sum(v for k, v in d.items() if k.startswith("840")); V = C.VOICES[L.get("voice", "tenor")]
    out["pick"] = dict(made=m["made"], living=m["survivors"], pool=j.get("pass_the_gate"), deaths_780_in_10=round(10 * d780 / m["made"], 2), deaths_840_in_10=round(10 * d840 / max(1, m["made"] - d780), 2), bars_of_sung_phrases=phr, notes_a_bar=round(len(ns) / phr, 3), onsets_on_the_beat=round(r["onsets on the beat"], 3), onsets_on_the_first_beat=round(r["onsets on the bar's first beat"], 3), stressed_on_the_first_beat=round(float(np.mean([n["on"] % 36 == 0 for n in st])), 3), range=r["range"], inside_the_voice=bool(V[0] <= min(x[2] for x in ns) and max(x[2] for x in ns) <= V[1]), leap_past_an_octave_in_a_line=bool(any(a["sec"] == b["sec"] and a["line"] == b["line"] and abs(b["midi"] - a["midi"]) > 12 for a, b in zip(nn, nn[1:]))))
    out["plan"] = dict(sung_bars=sp.get("sung_bars"), slots=sp["slots"], title_lines=sp.get("hooks"), lines_ahead_of_title_lines=sp.get("title_entry"), rest_form=rest, title_room=sp.get("title_room"))
    E = M.Engine(json.loads(json.dumps(sp))); E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(sp["scale"]), key="p", how=sp.get("how"), cap=None, share=None, clash=None, relocate=False)[0]; rng = random.Random(L.get("seed", 1)); rows = []; onb = []; errs = collections.Counter(); made = 0
    for _ in range(n_living):
        c, err = E.build(rng)
        if err: errs[f"{err[0]} ({err[1]}:{err[2]})"] += 1; continue
        made += 1; s0 = [n for n in c["notes"] if n["stress"]]; onb.append(float(np.mean([E.on_beat(n["on"]) for n in s0])))
        if E.gates(c): continue
        s = sorted(E.as_sung(c["notes"]), key=lambda n: n["on"]); r = AB.readings([[n["on"], n["dur"], n["p"]] for n in s], 36, [0, 18], 18); s1 = [n for n in s if n["stress"] and n.get("melisma") != "second"]; rows.append((len(s) / phr, r["onsets on the beat"], r["onsets on the bar's first beat"], float(np.mean([n["on"] % 36 == 0 for n in s1])), r["range"]))
    a = np.array(rows); med = lambda k: round(float(np.median(a[:, k])), 3)
    out["living"] = dict(builds=n_living, made=made, never_made=dict(errs), living=len(a), notes_a_bar=med(0), onsets_on_the_beat=med(1), onsets_on_the_first_beat=med(2), stressed_on_the_first_beat=med(3), range=med(4), stressed_on_a_beat_every_build_made_median=round(float(np.median(onb)), 3)) if len(a) else dict(builds=n_living, made=made, never_made=dict(errs), living=0)
    E = M.Engine(json.loads(json.dumps(sp))); rng = random.Random(1); made = 0; d840 = 0; on = collections.Counter(); gap = collections.defaultdict(list); hooks = list(sp.get("hooks", ()))
    for _ in range(n_title):
        c, err = E.build(rng)
        if err: continue
        made += 1; d840 += (E.gates(c) or "").startswith("840"); flat = sorted(c["notes"], key=lambda n: n["on"])
        for h in hooks:
            s_, i_ = h.rsplit(":", 1); mine = [n for n in flat if n["sec"] == s_ and n["line"] == int(i_)]; o = mine[0]["on"]; on[h] += o - E.line_start(s_, int(i_)) <= 0; before = [n for n in flat if n["on"] < o]
            if before: gap[h].append((o - (before[-1]["on"] + before[-1]["dur"])) / 6.0)
    out["title lines"] = dict(builds_made=made, on_time_in_100={h: round(100 * on[h] / max(1, made), 1) for h in hooks}, silence_before_in_eighths_median={h: round(float(np.median(gap[h])), 2) for h in hooks if gap[h]}, deaths_on_840_in_10=round(10 * d840 / max(1, made), 2))
    return out
if __name__ == "__main__": print(json.dumps(read(sys.argv[1], sys.argv[2])))
