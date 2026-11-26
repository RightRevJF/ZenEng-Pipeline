"""The clean reading (PREDICTION.md, marks 1 to 6): each v50 record's fitted spec, the form off and on. N=1000 OUT=x.json python3 clean.py stem ..."""
import os, sys, json, random, collections, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas"), os.path.join(ROOT, "studies", "line_repeats"), os.path.join(ROOT, "studies", "ladder")]
import numpy as np, song_from_lyric as SL, metre_engine as M, make_kept_commonest_pitch as CP
from read import deg, repeat
from ladder import verse_figs
sys.path.insert(0, HERE); from bands_read import bands, joins
T7 = json.load(open(os.path.join(ROOT, "tables", "kept_line_repeat.json"))); T = T7["share"]; FORMS = {"the form": lambda: dict(T), "by the count": lambda: dict(T, by_count=T7["by_count"], true=False), "by the count, a true repeat": lambda: dict(T, by_count=T7["by_count"], true=True), "by the count, a true repeat, the chord tie": lambda: dict(T, by_count=T7["by_count"], true=True), "the three": lambda: dict(T, by_count=T7["by_count"], true=True)}; JM = json.load(open(os.path.join(ROOT, "tables", "kept_line_join.json")))["moves"]; TIE = json.load(open(os.path.join(ROOT, "tables", "kept_chord_tie.json")))["weights"]; RUN = [False] + os.environ.get("FORMS", "the form").split("|"); N = int(os.environ.get("N", "1000")); out = {}
for stem in sys.argv[1:]:
    L = json.load(open(stem + ".json")); rec = json.load(open(stem + ".song.json")); o = {}
    for form in RUN:
        spec = json.loads(json.dumps(rec["spec"])); scale = sorted(spec["scale"])
        if form: spec["borrow_kept"] = FORMS[form]()
        if form and ("chord tie" in form or form == "the three"): spec["chord_tie"] = TIE
        if form == "the three": spec["join_moves"] = JM
        E = M.Engine(spec); E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
        rng = random.Random(L.get("seed", 1)); sh = []; F = collections.defaultdict(list); fig = []; a = b = cl = nn = 0; same = tot = rep = lin = 0; DG = spec.get("degrees") or {}; blue = set(DG.get("blue", ())); bn = 0; psc = []; b816 = []; jn = []
        for _ in range(N):
            cc, err = E.build(rng)
            if err or E.gates(cc): continue
            s = sorted(E.as_sung(cc["notes"]), key=lambda n: n["on"]); ps = [n["p"] for n in s if CP.kind(n["sec"]) == "Verse"]; sh.append(collections.Counter(ps).most_common(1)[0][1] / len(ps)); rd_ = E.readings(cc["notes"]); fig.append(rd_["bars on a figure already sung"]); psc.append(rd_.get("pitch scaling", float("nan"))); bb_ = bands(np.array([n["p"] for n in s], float)); b816.append(bb_["8 to 16"]) if bb_ else None; ll_ = []; cu_ = None
            for n in s:
                if (n["sec"], n["line"]) != cu_: cu_ = (n["sec"], n["line"]); ll_.append((n["sec"], []))
                ll_[-1][1].append(n["p"])
            jn.append(float(np.mean(joins(ll_)[1])))
            by = collections.OrderedDict()
            for n in s:
                ch = E.chord_at(n["on"]); ct = n["p"] % 12 in ch; nn += 1
                if E.on_beat(n["on"]): a += ct; b += 1
                bl_ = (n["p"] - DG.get("tonic", 0)) % 12 in blue; bn += bl_
                if not bl_ and n["dur"] >= E.BEAT and not ct and ((n["p"] + 1) % 12 in ch or (n["p"] - 1) % 12 in ch): cl += 1
                if CP.kind(n["sec"]) == "Verse" and n.get("melisma") != "second": by.setdefault(n["sec"], collections.OrderedDict()).setdefault(n["line"], []).append(n["p"])
            for lines in by.values():
                ls = list(lines.values()); f = verse_figs(ls)
                if f:
                    for x, y in f.items(): F[x].append(y)
                dg = [[deg(p, 0, scale) for p in l] for l in ls]
                for i in range(1, len(dg)):
                    if len(dg[i]) < 4: continue
                    r = any(repeat(dg[j], dg[i]) is not None for j in (i - 2, i - 1) if j >= 0); lin += 1; rep += r
                    if not r and i >= 2 and len(dg[i - 2]) >= 4: tot += 1; same += abs(float(np.median(dg[i]) - np.median(dg[i - 2]))) < 1
        o[form or "v50"] = dict(living=len(sh), height_two_back=round(same / max(1, tot), 3), verse_lines_that_repeat=round(rep / max(1, lin), 3), between_lines=round(float(np.median(F["between lines"])), 2), first_notes_spread=round(float(np.median(F["spread of the lines' first notes"])), 2), within_lines=round(float(np.median(F["within lines"])), 2),
            commonest_pitch=round(st.median(sh), 3), over_the_ceiling_in_100=round(100 * sum(x > 0.44 for x in sh) / max(1, len(sh)), 1), bars_on_a_figure_already_sung=round(st.median(fig), 3), clashes_not_blue_per_100_notes=round(100 * cl / max(1, nn), 2), on_beat_chord_tones=round(a / max(1, b), 3), blue_notes_in_100=round(100 * bn / max(1, nn), 1), pitch_scaling=round(float(np.nanmedian(psc)), 3), slope_8_to_16=round(st.median(b816), 3), across_a_join=round(st.median(jn), 2))
        print(os.path.basename(stem), form or "v50", json.dumps(o[form or "v50"]), flush=True)
    out[os.path.basename(stem)] = o
json.dump(out, open(os.path.join(HERE, os.environ.get("OUT", "clean.json")), "w"), indent=1)
