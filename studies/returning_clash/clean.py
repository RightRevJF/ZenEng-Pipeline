"""PREDICTION_forms.md, the clean reading: each v52 record's fitted spec; v52, form 1 alone (the copy), form 2 alone (the melisma's second note).  N=1000 OUT=x.json python3 clean.py stem ..."""
import os, sys, json, random, collections, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np, song_from_lyric as SL, metre_engine as M, page_gate as PG
T = PG.table(); out = {}; N = int(os.environ.get("N", "1000")); DIR = os.environ.get("DIR")
for stem in sys.argv[1:]:
    L = json.load(open(stem + ".json")); o = {}
    for form in ("v52", "form 1", "form 2") if not DIR else ("v52", os.environ["LABEL"]):
        rec = json.load(open(stem + ".song.json" if form == "v52" else os.path.join(DIR, os.path.basename(stem) + ".song.json") if DIR else stem + ".song.json")); spec = json.loads(json.dumps(rec["spec"]))
        if not DIR and form == "form 1": spec["copy_clash"] = True
        if not DIR and form == "form 2": spec["melisma_clear"] = True
        DG = spec.get("degrees") or {}; blue = set(DG.get("blue", ())); E = M.Engine(spec)
        E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"), clash=SL.melisma_clash(E, 0) if spec.get("melisma_clear") else None)[0]
        rng = random.Random(L.get("seed", 1)); C = collections.Counter(); fig = []; psc = []; su = []; nn = 0; living = 0
        for _ in range(N):
            c, err = E.build(rng)
            if err or E.gates(c): continue
            living += 1; rd = E.readings(c["notes"]); fig.append(rd["bars on a figure already sung"]); psc.append(rd.get("pitch scaling", float("nan")))
            s = sorted(E.as_sung(c["notes"]), key=lambda x: x["on"]); on_ = [x["on"] for x in s]; su.append(PG.read([x["p"] for x in s], [(b_ - a_) / float(E.BEAT) for a_, b_ in zip(on_, on_[1:])] + [1.0], T)["surprise"])
            for i, n in enumerate(s):
                nn += 1; k = (n["sec"], n["line"]); how = E.HOW.get(k, ["fresh"]); ch = E.chord_at(n["on"])
                if n.get("melisma") == "first":
                    C["melismas"] += 1; nx = s[i + 2] if i + 2 < len(s) else None; C["melismas at a line's end"] += nx is None or (nx["sec"], nx["line"]) != k
                if n.get("melisma") != "second": C["syllables"] += 1
                if (n["p"] - DG.get("tonic", 0)) % 12 in blue or n["dur"] < E.BEAT or n["p"] % 12 in ch or not ((n["p"] + 1) % 12 in ch or (n["p"] - 1) % 12 in ch): continue
                C["clashes"] += 1
                if n.get("melisma") == "second": C["on a melisma's second note"] += 1
                elif how[0] == "copy" and set(E.chord_at(E.line_start(how[1], how[2]) + n["on"] - E.line_start(*k))) != set(ch): C["in a copied line over another chord"] += 1
        o[form] = dict(living=living, clashes_per_100=round(100 * C["clashes"] / nn, 3), copy_over_another_chord_per_100=round(100 * C["in a copied line over another chord"] / nn, 3), melisma_second_per_100=round(100 * C["on a melisma's second note"] / nn, 3), figure=round(st.median(fig), 3), pitch_scaling=round(float(np.nanmedian(psc)), 3), surprise=round(st.median(su), 3), melismas_in_100_syllables=round(100 * C["melismas"] / C["syllables"], 2), melismas_at_a_line_end_share=round(C["melismas at a line's end"] / max(1, C["melismas"]), 3), moved=E.stats.get("749.223: a copied line's long note moved off a clash under another chord", 0))
        print(os.path.basename(stem), form, json.dumps(o[form]), flush=True)
    out[os.path.basename(stem)] = o
json.dump(out, open(os.path.join(HERE, os.environ.get("OUT", "clean.json")), "w"), indent=1)
