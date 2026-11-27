"""Run 09, iiv_confirm09: run 08's frozen confirmation (first_principles section 5): the ii-V share on unseen songs. COUNTED.
Rules in PREDICTION.md. Run once, after the predictions commit is pushed:  python3 -I test.py   (from this folder)"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import common09 as C9      # the guard: harness09 reads the outcome only through C9.load_outcomes / C9.guard, AFTER printing power
import harness09 as H

K = 1; ALPHA = 0.05 / K
NJ = lambda s: s["genre"] != "jazz"
out = H.run_unseen(HERE, "IIV", H.STD, pred=0.05, alpha=ALPHA, K=K, counted=True, frozen_power=0.367, readings=[
    dict(label="non_jazz_frozen_reading", meas="IIV", extra=H.STD, pred=0.04, keep=NJ,
         note="run 08's frozen interpretive reading: genres other than jazz (biab, pop, wikifonia, other); if +0.04 lies outside its 95% range the finding is labelled 'jazz repertoire'"),
    dict(label="rb_biab_charts_only", meas="IIV", extra=H.STD, pred=0.035, source="rbb",
         note="R09-L1's counted form, merged here as an estimate: every column read from the song's real-book and BiaB charts only"),
    dict(label="name_matched_only", meas="IIV", extra=H.STD, pred=None, keep=lambda s: s["match"] == "name"),
    dict(label="chart_provenance_only", meas="IIV", extra=H.STD, pred=None, keep=lambda s: s["provenance"] == "chart"),
    dict(label="jazz_genre_only", meas="IIV", extra=H.STD, pred=None, keep=lambda s: s["genre"] == "jazz")])
r = out["readings"].get("non_jazz_frozen_reading", {})
if "b" in r:
    out["non_jazz_label"] = "jazz repertoire" if not r["prediction_inside_95"] else "not labelled (+0.04 inside the non-jazz range)"
    json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=1, default=float); print("non-jazz label:", out["non_jazz_label"])
