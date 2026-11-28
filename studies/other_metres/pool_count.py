"""PREDICTION_counts_K5_pool.md: one run made by the planner's own routine under whatever switches the shell sets, the pool read from inside the engine's run as it ends (nothing replicated or changed), and the figure marks read on the living builds, the pool and the pick.  python3 studies/other_metres/pool_count.py LYRIC.json [SEED] -> prints JSON. A count."""
import os, sys, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE]
import numpy as np, pop_read as PR
SL = PR.SL; M = PR.M; AB = PR.AB; MK = PR.MK
def marks_for(table, by_section):
    T = json.load(open(os.path.join(M.ATLAS, "kept_readings.json"))).get(table)
    if T is None: T = json.load(open(os.path.join(M.ATLAS, table + ".rows.json")))
    X = np.array(T["rows"], float); q = lambda n, p: float(np.percentile(X[:, T["names"].index(n)], p))
    return dict(notes_a_bar=(q("notes a bar", 25), q("notes a bar", 75)), onsets_on_a_beat=(q("onsets on the beat", 25), None), range=(q("range", 25), None), pitches=(q("distinct pitches", 25), None), rhythm_again=(q("bars on a rhythm already sung", 10), q("bars on a rhythm already sung", 90)), figure_again=(None, q("bars on a figure already sung", 90)))
def figs(E, notes, phr, by_section):
    BL = E.BAR; s = sorted(notes, key=lambda x: x["on"]); ns = [[x["on"], x["dur"], x["p"]] for x in s]; r = AB.readings(ns, BL, list(range(0, BL, E.BEAT)), 12); p = [x["p"] for x in s]; st = [x for x in s if x["stress"] and x.get("melisma") != "second"]; w = MK.structure(ns, BL); wr = []; wf = []
    if by_section:
        by = collections.OrderedDict()
        for x in s: by.setdefault(x["sec"], []).append([x["on"], x["dur"], x["p"]])
        for v in by.values():
            if len(set(n[0] // BL for n in v)) >= 4: q = MK.structure(v, BL); wr.append(q["bars on a rhythm already sung"]); wf.append(q["bars on a figure already sung"])
    return dict(notes_a_bar=len(ns) / phr, onsets_on_a_beat=r["onsets on the beat"], range=max(p) - min(p), pitches=len(set(p)), rhythm_again=float(np.median(wr)) if by_section else w["bars on a rhythm already sung"], figure_again=float(np.median(wf)) if by_section else w["bars on a figure already sung"],
                commonest=max(collections.Counter(p).values()) / len(p), first_beat_stress=float(np.mean([x["on"] % BL == 0 for x in st])), stress_off_the_beat=float(np.mean([x["on"] % E.BEAT != 0 for x in st])))
def met(mk, k, v): lo, hi = mk[k]; return bool((lo is None or v >= lo) and (hi is None or v <= hi))
if __name__ == "__main__":
    L = json.load(open(sys.argv[1]))
    if len(sys.argv) > 2: L["seed"] = int(sys.argv[2])
    got = {}
    def prof(frame, event, arg):
        if event == "return" and frame.f_code.co_name == "run" and frame.f_code.co_filename.endswith("metre_engine.py") and "alive" in frame.f_locals:
            fl = frame.f_locals; got.update(E=fl["self"], alive=list(fl["alive"]), pool=list(fl.get("pool") or []), pick=fl.get("pick"))
    sys.setprofile(prof)
    try: rec = SL.write(L)
    finally: sys.setprofile(None)
    rec = rec[0] if isinstance(rec, tuple) else rec; E = got["E"]; sp = rec["spec"]; phr = sum(sum(v) for v in sp["slots"].values()); table = sp.get("table") or sp["metre"].replace("/", "-") + "_sung"; pop34 = sp["metre"] == "3/4"; six = marks_for(table, pop34)
    nine = dict(six, commonest=(None, 0.303), first_beat_stress=(0.45, None), stress_off_the_beat=(None, 0.26)) if pop34 else None
    sung = getattr(E, "as_sung", None) or (lambda x: x)
    for c in got["alive"]: c["_f"] = figs(E, sung(c["notes"]), phr, pop34)
    def desc(cs):
        o = dict(builds=len(cs), median={k: round(float(np.median([c["_f"][k] for c in cs])), 3) for k in cs[0]["_f"]}, meeting_in_100={k: round(100 * float(np.mean([met(six, k, c["_f"][k]) for c in cs])), 1) for k in six}, meeting_all_six_in_100=round(100 * float(np.mean([all(met(six, k, c["_f"][k]) for k in six) for c in cs])), 1))
        if nine: o["meeting_all_nine_in_100"] = round(100 * float(np.mean([all(met(nine, k, c["_f"][k]) for k in nine) for c in cs])), 1); o["meeting_K5_in_100"] = round(100 * float(np.mean([met(nine, "commonest", c["_f"]["commonest"]) for c in cs])), 1)
        return o
    j = rec.get("judge7") or {}; pk = got["pick"]; pool = got["pool"]
    print(json.dumps(dict(title=L.get("title"), metre=sp["metre"], table=table, seed=sp.get("seed"), key=rec["key"]["key"], registers=sp.get("registers"), range_choice=j.get("range_choice"), key_pick=rec.get("key_pick") or j.get("key_pick"), plan=sp.get("plan"), made=rec["melody"]["made"], deaths=rec["melody"]["deaths"], marks_six={k: [None if x is None else round(x, 3) for x in v] for k, v in six.items()},
                          living=desc(got["alive"]), pool=desc(pool) if pool else None, pool_in_the_record=j.get("pass_the_gate"), gates_passed=j.get("gates_passed"), how_the_pool_and_pick_are_made=j.get("pool"), pick=dict(fp=pk["fp"], fp_in_the_record=rec["melody"]["pick"], order_built_in_the_pool=(sorted(c["n"] for c in pool).index(pk["n"]) + 1) if pk in pool else None, figs={k: round(v, 3) for k, v in pk["_f"].items()}, lowest_highest=[min(n["p"] for n in pk["notes"]), max(n["p"] for n in pk["notes"])], meets_all_six=all(met(six, k, pk["_f"][k]) for k in six), meets_all_nine=all(met(nine, k, pk["_f"][k]) for k in nine) if nine else None)), indent=1))
