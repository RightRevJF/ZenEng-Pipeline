"""The builds' figures from records' fitted specs: v50 records and a directory of trial records. N=300 OUT=x.json python3 whole_builds.py DIR"""
import os, sys, json, random, collections, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas"), os.path.join(ROOT, "studies", "line_repeats"), os.path.join(ROOT, "studies", "ladder")]
import numpy as np, song_from_lyric as SL, metre_engine as M, make_kept_commonest_pitch as CP
from read import deg, repeat
from ladder import verse_figs
out = {}
for n, p in (("55", "songs/p65/lyric55"), ("54", "songs/p64/lyric54"), ("58", "songs/p68/lyric58"), ("49", "songs/p59/lyric49"), ("50", "songs/p60/lyric50"), ("59", "songs/p69/lyric59")):
    L = json.load(open(os.path.join(ROOT, p + ".json"))); o = {}
    for lab, f in (("v50", os.path.join(ROOT, p + ".song.json")), ("form", os.path.join(sys.argv[1], f"lyric{n}.song.json"))):
        spec = json.load(open(f))["spec"]; scale = sorted(spec["scale"]); DG = spec.get("degrees") or {}; blue = set(DG.get("blue", ())); E = M.Engine(spec)
        E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
        rng = random.Random(L.get("seed", 1)); ps_ = []; rs = []; fg = []; sh = []; F = collections.defaultdict(list); a = b = cl = bn = nn = rep = lin = 0
        for _ in range(int(os.environ.get("N", "300"))):
            c, err = E.build(rng)
            if err or E.gates(c): continue
            r = E.readings(c["notes"]); ps_.append(r["pitch scaling"]); rs.append(r["rhythm scaling"]); fg.append(r["bars on a figure already sung"])
            s = sorted(E.as_sung(c["notes"]), key=lambda x: x["on"]); vp = [x["p"] for x in s if CP.kind(x["sec"]) == "Verse"]; sh.append(collections.Counter(vp).most_common(1)[0][1] / len(vp)); by = collections.OrderedDict()
            for x in s:
                ch = E.chord_at(x["on"]); ct = x["p"] % 12 in ch; nn += 1; bl = (x["p"] - DG.get("tonic", 0)) % 12 in blue; bn += bl
                if E.on_beat(x["on"]): a += ct; b += 1
                if not bl and x["dur"] >= E.BEAT and not ct and ((x["p"] + 1) % 12 in ch or (x["p"] - 1) % 12 in ch): cl += 1
                if CP.kind(x["sec"]) == "Verse" and x.get("melisma") != "second": by.setdefault(x["sec"], collections.OrderedDict()).setdefault(x["line"], []).append(x["p"])
            for lines in by.values():
                ls = list(lines.values()); f_ = verse_figs(ls)
                if f_: F["between lines"].append(f_["between lines"])
                dg = [[deg(q, 0, scale) for q in l] for l in ls]
                for i in range(1, len(dg)):
                    if len(dg[i]) >= 4: lin += 1; rep += any(repeat(dg[j], dg[i]) is not None for j in (i - 2, i - 1) if j >= 0)
        o[lab] = dict(builds=len(ps_), pitch_scaling=round(st.median(ps_), 3), rhythm_scaling=round(st.median(rs), 3), figure=round(st.median(fg), 3), over_the_ceiling_in_100=round(100 * sum(x > 0.44 for x in sh) / len(sh), 1), commonest_pitch=round(st.median(sh), 3), clashes_not_blue_per_100_notes=round(100 * cl / nn, 2), blue_notes_in_100=round(100 * bn / nn, 1), on_beat_chord_tones=round(a / b, 3), between_lines=round(float(np.median(F["between lines"])), 2), true_verse_repeats=round(rep / max(1, lin), 3))
    out[n] = o; print(n, json.dumps(o), flush=True)
json.dump(out, open(os.path.join(HERE, os.environ.get("OUT", "whole_builds.json")), "w"), indent=1)
