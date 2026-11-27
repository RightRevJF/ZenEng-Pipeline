"""PREDICTION_song64.md: the two records, and 1,000 builds of each record's fitted spec read as sung.  python3 song64_read.py"""
import os, sys, json, random, collections, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np, song_from_lyric as SL, metre_engine as M, page_gate as PG
L = json.load(open(os.path.join(ROOT, "songs", "p74", "lyric64.json"))); T = PG.table(); out = {}; CK = "sung notes a beat long or more a semitone from a chord tone"
for lab in ("v52", "pair"):
    r = json.load(open(os.path.join(HERE, f"lyric64.{lab}.song.json"))); j = r["judge7"]; m = r["melody"]; pm = [x["midi"] for x in m["notes"]]; spec = r["spec"]; E = M.Engine(spec); tm = r["key"]["tonic_midi"]; DG = spec.get("degrees") or {}; blue = set(DG.get("blue", ()))
    def clash(t, pc, dur): ch = E.chord_at(t); return dur >= E.BEAT and pc not in ch and ((pc + 1) % 12 in ch or (pc - 1) % 12 in ch)
    o = dict(record=dict(living=m["survivors"], pool=j["range_choice"]["builds_in_the_pool"], words_fit_builds_middle=j["words_gate"]["the_builds_median_fit"], chosen_range=max(pm) - min(pm), floor=j["range_choice"]["floor"], long_clash_count=r["checks"].get(CK), on_a_melisma_second_note=sum(1 for x in m["notes"] if x.get("melisma") == "second" and clash(x["on"], (x["midi"] - tm) % 12, x["dur"])), key=r["key"]["key"], chord_draft=r["chord_pick"]["draft"], pick=m["pick"], deaths=m["deaths"], blue_song=DG.get("blue_song"), copies=sum(1 for v in (spec.get("how") or {}).values() if v[0] == "copy"), again=sum(1 for v in (spec.get("how") or {}).values() if v[0] == "again"), switches=dict(copy_clash=spec.get("copy_clash"), melisma_clear=spec.get("melisma_clear")), moved=(m["stats"] if isinstance(m["stats"], dict) else {}).get("749.223: a copied line's long note moved off a clash under another chord")))
    E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"), clash=SL.melisma_clash(E, 0) if spec.get("melisma_clear") else None, relocate=spec.get("melisma_clear") != "after")[0]
    rng = random.Random(L.get("seed", 1)); C = collections.Counter(); fig = []; psc = []; su = []; nn = 0; living = 0
    for _ in range(1000):
        c, err = E.build(rng)
        if err or E.gates(c): continue
        living += 1; rd = E.readings(c["notes"]); fig.append(rd["bars on a figure already sung"]); psc.append(rd.get("pitch scaling", float("nan")))
        s = sorted(E.as_sung(c["notes"]), key=lambda x: x["on"]); on_ = [x["on"] for x in s]; su.append(PG.read([x["p"] for x in s], [(b_ - a_) / float(E.BEAT) for a_, b_ in zip(on_, on_[1:])] + [1.0], T)["surprise"])
        for n in s:
            nn += 1; k = (n["sec"], n["line"]); how = E.HOW.get(k, ["fresh"])
            if n.get("melisma") == "first": C["melismas"] += 1
            if n.get("melisma") != "second": C["syllables"] += 1
            if (n["p"] - DG.get("tonic", 0)) % 12 in blue or not clash(n["on"], n["p"] % 12, n["dur"]): continue
            C["clashes"] += 1
            if n.get("melisma") == "second": C["second"] += 1
            elif how[0] == "copy" and set(E.chord_at(E.line_start(how[1], how[2]) + n["on"] - E.line_start(*k))) != set(E.chord_at(n["on"])): C["copy"] += 1
    o["builds"] = dict(living=living, clashes_per_100=round(100 * C["clashes"] / nn, 3), copy_over_another_chord_per_100=round(100 * C["copy"] / nn, 3), melisma_second_per_100=round(100 * C["second"] / nn, 3), figure=round(st.median(fig), 3), pitch_scaling=round(float(np.nanmedian(psc)), 3), surprise=round(st.median(su), 3), melismas_in_100_syllables=round(100 * C["melismas"] / C["syllables"], 2))
    out[lab] = o; print(lab, json.dumps(o), flush=True)
json.dump(out, open(os.path.join(HERE, "song64.json"), "w"), indent=1)
