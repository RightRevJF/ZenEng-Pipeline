"""PREDICTION_pop_3_4.md and PREDICTION_234_235.md: a pop-style 3/4 record read, the pick and the living builds, K6 within sections.  python3 studies/other_metres/pop_read.py LYRIC.json NAME=DIR ... -> prints; OUT=file.json writes"""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [HERE, os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np, song_from_lyric as SL, metre_engine as M, atlas_build as AB, make_leadsheet_table as MK, chord_writer as C
BL = 36
def figs(notes, phr):
    """notes: dicts with on, dur, p, sec, stress, melisma; counted as the pop table counts"""
    s = sorted(notes, key=lambda x: x["on"]); ns = [[x["on"], x["dur"], x["p"]] for x in s]; r = AB.readings(ns, BL, [0, 12, 24], 12); st = [x for x in s if x["stress"] and x.get("melisma") != "second"]; p = [x["p"] for x in s]; wr = []; wf = []; by = collections.OrderedDict()
    for x in s: by.setdefault(x["sec"], []).append([x["on"], x["dur"], x["p"]])
    for v in by.values():
        if len(set(n[0] // BL for n in v)) >= 4: q = MK.structure(v, BL); wr.append(q["bars on a rhythm already sung"]); wf.append(q["bars on a figure already sung"])
    w = MK.structure(ns, BL)
    return dict(notes_a_bar=len(ns) / phr, onsets_on_a_beat=r["onsets on the beat"], first_beat_stress=float(np.mean([x["on"] % BL == 0 for x in st])), stress_off_the_beat=float(np.mean([x["on"] % 12 != 0 for x in st])), range=max(p) - min(p), pitches=len(set(p)), commonest=max(collections.Counter(p).values()) / len(p),
                rhythm_again_in_sections=float(np.median(wr)), figure_again_in_sections=float(np.median(wf)), rhythm_again_whole=w["bars on a rhythm already sung"], figure_again_whole=w["bars on a figure already sung"])
MARK = dict(notes_a_bar=(2.382, 3.847), onsets_on_a_beat=(0.508, None), first_beat_stress=(0.45, None), stress_off_the_beat=(None, 0.26), range=(12, None), pitches=(7, None), commonest=(None, 0.303), rhythm_again_in_sections=(0.349, 0.871), figure_again_in_sections=(None, 0.667))
def met(k, v): lo, hi = MARK[k]; return bool((lo is None or v >= lo) and (hi is None or v <= hi))
if __name__ == "__main__":
    L = json.load(open(sys.argv[1])); stem = os.path.basename(sys.argv[1]).replace(".json", ""); out = {}
    for a_ in sys.argv[2:]:
        name, d = a_.split("=", 1); R = json.load(open(os.path.join(d, stem + ".song.json"))); m = R["melody"]; j = R["judge7"]; sp = json.loads(json.dumps(R["spec"])); phr = sum(sum(v) for v in sp["slots"].values()); V = C.VOICES[L.get("voice", "tenor")]
        nn = [dict(on=n["on"], dur=n["dur"], p=n["midi"], sec=n["sec"], stress=n["stress"], melisma=n.get("melisma"), line=n["line"]) for n in m["notes"]]; pick = figs(nn, phr); made = m["made"] - sum(v for k, v in m["deaths"].items() if "780" in k or "cannot fit" in k)
        o = dict(made=m["made"], living=m["survivors"], pool=j.get("pass_the_gate"), deaths=m["deaths"], bars_of_sung_phrases=phr, sung_bars=sp.get("sung_bars"), shared_bars=sp.get("shared_bars"), title_room=sp.get("title_room"), registers=sp["registers"], range_choice=j.get("range_choice"), key=R["key"]["key"], lowest_highest=[min(n["p"] for n in nn), max(n["p"] for n in nn)], voice=list(V), inside_the_voice=bool(V[0] <= min(n["p"] for n in nn) and max(n["p"] for n in nn) <= V[1]),
                 leap_past_an_octave_in_a_line=bool(any(a["sec"] == b["sec"] and a["line"] == b["line"] and abs(b["p"] - a["p"]) > 12 for a, b in zip(sorted(nn, key=lambda x: x["on"]), sorted(nn, key=lambda x: x["on"])[1:]))), deaths_780_in_10=round(10 * sum(v for k, v in m["deaths"].items() if "780" in k) / m["made"], 2), deaths_840_in_10=round(10 * sum(v for k, v in m["deaths"].items() if k.startswith("840")) / max(1, made), 2), pick={k: round(v, 3) for k, v in pick.items()}, stress_table=(sp.get("stress_place") or {}).get("place"), seconds=[x for x in R.get("flags", []) if "seconds" in x])
        E = M.Engine(sp); E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(sp["scale"]), key="p", how=sp.get("how"), cap=None, share=None, clash=None, relocate=False)[0]; rng = random.Random(L.get("seed", 1)); rows = []
        for _ in range(600):
            c, err = E.build(rng)
            if err or E.gates(c): continue
            rows.append(figs(E.as_sung(c["notes"]), phr))
        if rows:
            o["living_read"] = len(rows); o["living_median"] = {k: round(float(np.median([r[k] for r in rows])), 3) for k in rows[0]}; o["living_quartiles"] = {k: [round(float(q), 3) for q in np.percentile([r[k] for r in rows], (25, 75))] for k in rows[0]}
            o["marks"] = {k: dict(pick=met(k, pick[k]), median=met(k, o["living_median"][k])) for k in MARK}; o["living_meeting_every_figure_mark_in_100"] = round(100 * float(np.mean([all(met(k, r[k]) for k in MARK) for r in rows])), 1)
        out[name] = o; print(name, json.dumps({k: v for k, v in o.items() if k not in ("sung_bars", "registers", "stress_table", "seconds", "shared_bars")}), flush=True)
    if os.environ.get("OUT"): json.dump(out, open(os.path.join(HERE, os.environ["OUT"]), "w"), indent=1)
