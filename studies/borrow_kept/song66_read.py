"""PREDICTION_song66.md: the two records, and 1,000 builds of each record's fitted spec.  python3 song66_read.py"""
import os, sys, json, random, collections, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas"), os.path.join(ROOT, "studies", "line_repeats"), os.path.join(ROOT, "studies", "ladder"), HERE]
import numpy as np, song_from_lyric as SL, metre_engine as M, make_kept_commonest_pitch as CP, page_gate as PG
from read import deg, repeat
from ladder import verse_figs
from bands_read import joins
L = json.load(open(os.path.join(ROOT, "songs", "p76", "lyric66.json"))); T = PG.table(); out = {}
for lab in ("v50", "pair"):
    r = json.load(open(os.path.join(HERE, f"lyric66.{lab}.song.json"))); j = r["judge7"]; m = r["melody"]; pm = [x["midi"] for x in m["notes"]]; stt = m["stats"] if isinstance(m["stats"], dict) else {}
    o = dict(record=dict(living=m["survivors"], pool=j["range_choice"]["builds_in_the_pool"] if j.get("range_choice") else None, words_fit_builds_middle=j["words_gate"]["the_builds_median_fit"], chosen_range=max(pm) - min(pm), floor=(j.get("range_choice") or {}).get("floor"), peak_planted=stt.get("950: the peak planted in a chorus line"), key=r["key"]["key"], deaths=m["deaths"], switches=dict(borrow_kept="borrow_kept" in r["spec"], chord_tie="chord_tie" in r["spec"], join_moves="join_moves" in r["spec"]), blue_song=(r["spec"].get("degrees") or {}).get("blue_song")))
    spec = r["spec"]; scale = sorted(spec["scale"]); DG = spec.get("degrees") or {}; blue = set(DG.get("blue", ())); E = M.Engine(spec)
    E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
    rng = random.Random(L.get("seed", 1)); ps_ = []; fg = []; sh = []; su = []; bls = []; jn = []; a = b = cl = bn = nn = rep = lin = 0
    for _ in range(1000):
        c, err = E.build(rng)
        if err or E.gates(c): continue
        rd = E.readings(c["notes"]); ps_.append(rd.get("pitch scaling", float("nan"))); fg.append(rd["bars on a figure already sung"])
        s = sorted(E.as_sung(c["notes"]), key=lambda x: x["on"]); on_ = [x["on"] for x in s]; su.append(PG.read([x["p"] for x in s], [(b_ - a_) / float(E.BEAT) for a_, b_ in zip(on_, on_[1:])] + [1.0], T)["surprise"])
        vp = [x["p"] for x in s if CP.kind(x["sec"]) == "Verse"]; sh.append(collections.Counter(vp).most_common(1)[0][1] / len(vp)); by = collections.OrderedDict(); ll = []; cu = None
        for x in s:
            ch = E.chord_at(x["on"]); ct = x["p"] % 12 in ch; nn += 1; bl = (x["p"] - DG.get("tonic", 0)) % 12 in blue; bn += bl
            if E.on_beat(x["on"]): a += ct; b += 1
            if not bl and x["dur"] >= E.BEAT and not ct and ((x["p"] + 1) % 12 in ch or (x["p"] - 1) % 12 in ch): cl += 1
            if CP.kind(x["sec"]) == "Verse" and x.get("melisma") != "second": by.setdefault(x["sec"], collections.OrderedDict()).setdefault(x["line"], []).append(x["p"])
            if (x["sec"], x["line"]) != cu: cu = (x["sec"], x["line"]); ll.append((x["sec"], []))
            ll[-1][1].append(x["p"])
        jn.append(float(np.mean(joins(ll)[1])))
        for lines in by.values():
            ls = list(lines.values()); f_ = verse_figs(ls)
            if f_: bls.append(f_["between lines"])
            dg = [[deg(q, 0, scale) for q in l] for l in ls]
            for i in range(1, len(dg)):
                if len(dg[i]) >= 4: lin += 1; rep += any(repeat(dg[j_], dg[i]) is not None for j_ in (i - 2, i - 1) if j_ >= 0)
    n = len(sh); o["builds"] = dict(living=n, verses_over_the_ceiling_in_100=round(100 * sum(x > 0.44 for x in sh) / n, 1), commonest_pitch=round(st.median(sh), 3), true_verse_repeats=round(rep / max(1, lin), 3), clashes_not_blue_per_100_notes=round(100 * cl / nn, 2), blue_notes_in_100=round(100 * bn / nn, 2),
        surprise=round(st.median(su), 3), pitch_scaling=round(float(np.nanmedian(ps_)), 3), pitch_scaling_25_75=[round(float(x), 3) for x in np.nanpercentile(ps_, (25, 75))], on_beat_chord_tones=round(a / b, 3), between_lines=round(float(np.median(bls)), 2), figure=round(st.median(fg), 3), across_a_join=round(st.median(jn), 2))
    out[lab] = o; print(lab, json.dumps(o), flush=True)
out["kept"] = dict(surprise_middle=T["percentiles_10_25_50_75_90"]["surprise"][2], pitch_scaling_10_50_90=[0.667, 0.905, 1.107])
json.dump(out, open(os.path.join(HERE, "song66.json"), "w"), indent=1)
