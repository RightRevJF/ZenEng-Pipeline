"""read_l7.py: Luthier v7's tests (730-739) on a song's runs. Usage: python3 read_l7.py 48|49 [v6]  ->  read/read_l7_<song>.json
- 730: the pick (luthier_judge5), its most-repeating window's place (0.552-0.934), eligible builds, builds within 0.02 of the least charge; what
  728's rule (every window under the kept 75th for its density, by the reader's windows, among builds eligible under 715) would have picked.
- 731: drawn lines' entries (two-bar slots) by the stress of the first syllable, against 20 / 42 / 38 and 43 / 10 / 47; 714's by cell, printed.
- 732: bars (3+ notes) on a figure some kept song sings (56% within 15), the rate; 651's share (49%, middle half 35-62%).
- 733: builds with each window under the kept 75th for its density (three in four), every window; the longest run of one pitch (kept 4 to 7).
- 734: the per-note reading (89% within 3; 73% within 5); the power's rounds with their standard errors.
- 735: drawn lines under 6.5 notes a bar against the build's capped palette, sixteenth / eighth / quarter (within 10); bits saved a gap by the
  judge's reader (0.13 to 0.36); the build's gaps from the kept mean palette (0.19 or more).
- 736: deaths for want of a placement (under 20 a thousand), and where. 737: bars sung in a kept song, every complete build (81% within 8).
- 738: drawn lines of 6.5 notes a bar and over against the kept lines' pooled shares for the cell (within 10).
- 739: the nineteen readings for the pick and the median clean build beside the kept middle halves."""
import sys, io, contextlib, json, pickle, collections, os
import numpy as np
SONG = sys.argv[1] if len(sys.argv) > 1 else "48"; V6 = len(sys.argv) > 2 and sys.argv[2] == "v6"
H = "/home/claude/p58" if SONG == "48" else "/home/claude/p61"
sys.argv = ["x", "10", "main"]; sys.path.insert(0, H); sys.path.insert(0, "/home/claude/p58")
with contextlib.redirect_stdout(io.StringIO()):
    E = __import__("melody_l7_p58" if SONG == "48" else "melody_l7_p61")
import luthier_judge4 as J4, luthier_judge5 as J5, read739 as R9
BAR = E.BAR
T7 = json.load(open(f"{H}/tables/luthier_v7_tables.json"))
KW = T7[[k for k in T7 if k.startswith("730: kept windows")][0]]; BANDN = ["under 3.5", "3.5 to 4.5", "4.5 to 5.5", "5.5 and over"]
K9 = T7[[k for k in T7 if k.startswith("739: what")][0]]
KB710 = set(tuple(o_) for rows_ in json.load(open(f"{H}/tables/luthier_v6_kept_bars.json"))["rhythms"].values() for o_, c_, s_ in rows_)
CELL2 = (lambda S: dict(S["600: cells below 5.5, two-bar slots"], **S["600: cells at 5.5 and over, two-bar slots"]))(json.load(open(f"{H}/tables/zeneng_v137_span.json")))
DRAWN = ("fresh", "fresh (361 unit return)", "sung again"); KM = np.array(E.MEANPAL606[0])
TAG = "l6" if V6 else "l7"
RUNS = {f"{SONG} {m}": f"{H}/run{TAG}/melody_{TAG}_p{int(SONG) + 10}_{m}.pkl" for m in ("main", "ctl")}
def ntup(b): return [(o, p, s) for o, d, p, s, l, st, sy in b["notes"]]
out = {}
for lab, path in RUNS.items():
    D = pickle.load(open(path, "rb")); A = D["all"]; r = {}; alive = {a[0] for a in D["all_alive"]}
    clean = [b for b in A if b["fp"] in alive and not (isinstance(b.get("info"), dict) and b["info"].get("soft"))]
    r["runs"] = dict(made=D["made"], survivors=D["survivors"], order=D["order_fp"], pick=D["pick"]["fp"], clean=len(clean), deaths=dict(D["deaths"].most_common(8)))
    # 730
    pk, RR = J5.pick([(b["fp"], ntup(b)) for b in clean]); RD = dict(RR); el = [i for i, x in RD.items() if x["eligible for the pick"]]
    ls = min(RD[i]["charge"] for i in el); near = [i for i in el if RD[i]["charge"] <= ls + 0.02]
    def under75(x): return all(rep < KW[BANDN[J5._band(d)]]["25th, 50th, 75th, 90th"][2] for _, d, rep, _ in x["windows: label, notes a bar, repeats, place"])
    e728 = [i for i, x in RD.items() if x["eligible under 715"] and under75(x)]
    p728 = None
    if e728:
        l2 = min(RD[i]["charge"] for i in e728); p728 = min([i for i in e728 if RD[i]["charge"] <= l2 + 0.02], key=lambda i: RD[i]["distance from the kept medians"])
    chs = sorted(x["charge"] for x in RD.values()); pls = sorted(x["place among kept songs"] for x in RD.values())
    r["730: the pick (luthier_judge5); engine's pick; window place (0.552-0.934); eligible under 715 / 730 of clean; within 0.02; charge, place, distance; median build charge, place"] = dict(
        pick=pk, engine_pick=D["pick"]["fp"], window=round(RD[pk]["most-repeating window, place for its density"], 3), windows=RD[pk]["windows: label, notes a bar, repeats, place"],
        eligible715=sum(x["eligible under 715"] for x in RD.values()), eligible730=len(el), clean=len(clean), within_002=len(near),
        pick_charge=round(RD[pk]["charge"], 4), pick_place=round(RD[pk]["place among kept songs"], 3), pick_distance=round(RD[pk]["distance from the kept medians"], 3),
        median_charge=round(float(np.median(chs)), 4), median_place=round(float(np.median(pls)), 3),
        most_charged=collections.Counter(k for x in RD.values() for k in x["charges"]).most_common(6))
    r["730: 728's rule (every window under the kept 75th, among builds eligible under 715): builds; its pick"] = [len(e728), p728]
    r["730: share of clean builds whose most-repeating window lies over / under the kept middle half"] = [round(float(np.mean([x["most-repeating window, place for its density"] > 0.934 for x in RD.values()])), 3),
                                                                                                      round(float(np.mean([x["most-repeating window, place for its density"] < 0.552 for x in RD.values()])), 3)]
    # 731, 714 / 653
    ES = {1: [0, 0, 0], 0: [0, 0, 0]}; EC = collections.defaultdict(lambda: [0, 0, 0])
    for b in A:
        byl = collections.defaultdict(list)
        for o, d, p, s_, l, st, sy in b["notes"]: byl[l].append(o)
        for l, v in byl.items():
            s_, i_ = l.split(":"); i_ = int(i_); kd = b["kinds"].get((s_, i_))
            if E.slot_len(s_, i_) != 2 or kd not in DRAWN: continue
            e_ = min(v) - E.line_start(s_, i_); k = 0 if e_ < 0 else 1 if e_ == 0 else 2
            ES[1 if E.LINES[s_][i_][0][1] else 0][k] += 1; EC[E.cell600(len(v) / 2)][k] += 1
    r["731: entries before / on / after by the first syllable's stress (lines; shares; kept)"] = {("stressed" if s_ else "unstressed"): [sum(v), [round(x / max(1, sum(v)), 3) for x in v], [0.198, 0.419, 0.383] if s_ else [0.426, 0.102, 0.472]] for s_, v in ES.items()}
    r["714 (printed): entries by cell (build; kept; lines)"] = {c: [[round(x / max(1, sum(v)), 3) for x in v], E.KS653[c]["entry before the bar line / on it / after it"] if c in E.KS653 else None, sum(v)] for c, v in sorted(EC.items()) if sum(v) > 30}
    # 732, 733, 734, 735, 737, 738 on every complete build
    F7 = []; F6 = []; RN = []; WU = []; WA = collections.defaultdict(list); E6 = []; BS = []; DI = []; B710 = []; PAL = collections.defaultdict(lambda: [0, 0, 0]); DEN = collections.defaultdict(lambda: [0, 0, 0])
    for b in A:
        nd = [dict(on=o, p=p, sec=s_, line=l) for o, d, p, s_, l, st, sy in b["notes"]]; F7.append(E.read717(nd)); f6 = E.read651(nd)
        if f6 is not None: F6.append(f6)
        E6.append(E.read650(nd)); s9 = R9.song(ntup(b)); RN.append(R9.read(s9)[3])
        W = J5.windows(s9); u = [rep < KW[BANDN[J5._band(d)]]["25th, 50th, 75th, 90th"][2] for _, d, rep in W]; WU.append(all(u))
        for j, x in enumerate(u): WA[j].append(x)
        t = np.array(sorted(o for o, *_ in ntup(b))); g = np.searchsorted(J4.GB, np.clip(np.diff(t), 1, 96)); DI.append(0.5 * float(np.abs(np.bincount(g, minlength=9) / len(g) - KM).sum()))
        by = collections.defaultdict(set)
        for o in t: by[o // BAR].add(o % BAR)
        B710.append(float(np.mean([tuple(sorted(v)) in KB710 for v in by.values()])))
        rr = E.read735(dict(notes=nd, meta=b["meta"]))
        if rr:
            for k in range(3): PAL[k][0] += rr[0][k]; PAL[k][1] += rr[1][k]
            PAL["n"][0] += rr[2]
        byl = collections.defaultdict(list)
        for n in nd: byl[n["line"]].append(n["on"])
        for l, v in byl.items():
            s_, i_ = l.split(":"); i_ = int(i_); kd = b["kinds"].get((s_, i_))
            if E.slot_len(s_, i_) != 2 or kd not in DRAWN or len(v) / 2 < 6.5: continue
            v.sort(); c = E.cell600(len(v) / 2); gg = np.diff(v)
            for k, gv in enumerate((3, 6, 12)): DEN[(c, k)][0] += int(np.sum(gg == gv)); DEN[(c, k)][1] += len(gg)
    for b in clean[:400]: BS.append(RD[b["fp"]]["components"]["bits saved a gap"])
    f7 = [x for x in F7 if np.isfinite(x)]; ea = [x for x, _ in E6 if np.isfinite(x)]; eb = [y for _, y in E6 if np.isfinite(y)]
    r["732: bars (3+ notes) on a figure some kept song sings (mean); rate; 651's share (mean; kept 0.488, 0.349-0.617)"] = [round(float(np.mean(f7)), 3), D["rerun"].get("r717"), round(float(np.mean(F6)), 3)]
    r["733: builds with every window under the kept 75th; by window in order (share under; three in four asked); longest run of one pitch (25th, 50th, 75th; kept 4-7)"] = [
        round(float(np.mean(WU)), 3), [round(float(np.mean(v)), 3) for j, v in sorted(WA.items())], [float(x) for x in np.percentile(RN, [25, 50, 75])]]
    r["734: per-note reading (easier of a pair; than every neighbour); kept 0.89, 0.727"] = [round(float(np.mean(ea)), 3), round(float(np.mean(eb)), 3)]
    r["734: the power's rounds"] = [D["rerun"].get("pow734"), D["rerun"].get("stop734"), D["rerun"].get("pow650")]
    n_ = PAL["n"][0] or 1
    r["735: drawn lines under 6.5 notes a bar against the build's capped palette (sixteenth, eighth, quarter: sung, palette); the power; its rounds"] = [[[round(PAL[k][0] / n_, 3), round(PAL[k][1] / n_, 3)] for k in range(3)], D["rerun"].get("q735"), D["rerun"].get("hist735")]
    r["735: bits saved a gap, the judge's reader (25th, 50th, 75th; kept 0.13-0.36); gaps from the kept mean palette (25th, 50th, 75th; 0.19 or more)"] = [[round(float(x), 3) for x in np.percentile(BS, [25, 50, 75])], [round(float(x), 3) for x in np.percentile(DI, [25, 50, 75])]]
    r["736: deaths for want of a placement, a thousand builds; where"] = [round(1000 * D["deaths"].get("rhythm: no placement", 0) / max(1, D["made"]), 1), dict(collections.Counter(c.get("where") for c in D["every"] if c["cause"] == "rhythm: no placement").most_common(4))]
    r["737: bars sung in a kept song, every complete build (81% within 8)"] = round(float(np.mean(B710)), 3)
    r["738: drawn lines of 6.5 notes a bar and over against the kept lines' pooled shares for the cell (sung, kept, gaps)"] = {f"{c} | {['sixteenth', 'eighth', 'quarter'][k]}": [round(v[0] / max(1, v[1]), 3), CELL2[c]["gap values, shares"][['sixteenth', 'eighth', 'quarter'][k]], v[1]] for (c, k), v in sorted(DEN.items()) if v[1] > 50}
    # 739
    X = np.array([R9.read(R9.song(ntup(b))) for b in clean], float); xp = np.array(R9.read(R9.song(ntup(next(b for b in A if b["fp"] == D["pick"]["fp"])))), float)
    r["739: the nineteen readings (the pick; the median clean build; kept 25th, 50th, 75th; the pick outside?)"] = {nm: [round(float(xp[j]), 3), round(float(np.nanmedian(X[:, j])), 3), K9[nm]["kept 25th, 50th, 75th (raw)"],
        ("over" if xp[j] > K9[nm]["kept 25th, 50th, 75th (raw)"][2] else "under" if xp[j] < K9[nm]["kept 25th, 50th, 75th (raw)"][0] else "")] for j, nm in enumerate(R9.NAMES)}
    r["survivors"] = D["survivors"]
    out[lab] = r
os.makedirs(f"{H}/read", exist_ok=True)
json.dump(out, open(f"{H}/read/read_{TAG}_{SONG}.json", "w"), indent=1, default=str)
for lab, r in out.items():
    print("==", lab, r["runs"])
    for k, v in r.items():
        if k != "runs": print("  ", k, json.dumps(v, default=str)[:900])
