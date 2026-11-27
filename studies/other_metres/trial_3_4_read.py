"""PREDICTION_trial_3_4.md: the two arms' records read.  python3 studies/other_metres/trial_3_4_read.py ESSEN_DIR WIKI_DIR -> trial_3_4.json"""
import os, sys, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier")]
import luthier_judge7 as J7, make_kept_commonest_pitch as CP
JE = J7.Judge7("3-4_sung"); JW = J7.Judge7("../../studies/other_metres/trial_tables/3-4_leadsheet_sung"); out = {}
for arm, d in (("Essen", sys.argv[1]), ("Wikifonia", sys.argv[2])):
    R = json.load(open(os.path.join(d, "lyric53.song.json"))); m = R["melody"]; j = R["judge7"]; ns = sorted(m["notes"], key=lambda n: n["on"]); rd = m["readings"]; by = collections.OrderedDict()
    for n in ns: by.setdefault((n["sec"], n["line"], n["text"], n["on"] if not n["text"] else None), n)
    first = [n for i, n in enumerate(ns) if n.get("melisma") != "second"]; st = [n for n in first if n["stress"]]; bar = 36
    out[arm] = dict(key=R["key"]["key"], made=m["made"], living=m["survivors"], deaths=m["deaths"], pool=j["pass_the_gate"], joint_gate=j["gate"], pick_distance_own_table=j["pick_distance"], distance_against_Essen=round(JE.distance(rd), 3), Essen_gate=round(JE.gate, 3), distance_against_Wikifonia=round(JW.distance(rd), 3), Wikifonia_gate=round(JW.gate, 3),
                    notes_a_bar=rd["notes a bar"], onsets_on_a_beat=round(rd["onsets on the beat"], 3), stressed_on_first_beat=round(sum(n["on"] % bar == 0 for n in st) / len(st), 3), stressed_syllables=len(st), words_fit=(j.get("pick_words_fit") or {}).get("all"),
                    commonest_pitch={part: round(CP.share([n["midi"] for n in ns if CP.kind(n["sec"]) == part]) or 0, 3) for part in ("Verse", "Chorus")}, range=rd["range"], lowest_highest=[min(n["midi"] for n in ns), max(n["midi"] for n in ns)],
                    leap_past_an_octave_in_a_line=bool(any(a["sec"] == b["sec"] and a["line"] == b["line"] and abs(b["midi"] - a["midi"]) > 12 for a, b in zip(ns, ns[1:]))), notes=len(ns), bars_sung=round(len(ns) / rd["notes a bar"]), readings={k: round(float(v), 3) for k, v in rd.items()})
    print(arm, json.dumps({k: v for k, v in out[arm].items() if k != "readings"}))
json.dump(out, open(os.path.join(HERE, "trial_3_4.json"), "w"), indent=1)
