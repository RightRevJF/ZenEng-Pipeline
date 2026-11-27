"""Run 09, iiv_dres08: R09-L2's lead on SEEN songs (all run 08 songs; outcomes opened in run 08): the ii-V share holding resolved
dominants per bar (DRES). A LEAD: not in K, passes nothing, kills nothing. Rules in PREDICTION.md. Run once:  python3 -I test.py"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import common09 as C9      # the guard: harness09 reads the outcome only through C9.load_outcomes / C9.guard, AFTER printing power
import harness09 as H

COLS = ["IIV", "DRES"] + H.SEEN_STD
def classify(res, rd):
    bi, bd = res["IIV"], res["DRES"]; alone = rd["IIV_alone_same_songs"]["IIV"]["b"]
    ii = bi["b"] >= 0.06 and bd["range95"][0] <= 0 <= bd["range95"][1]
    resol = bd["b"] > 0 and bd["p"] < 0.05 and bi["b"] <= alone / 2
    return dict(ii_carries=bool(ii), resolution_carries=bool(resol), IIV_alone=alone,
                reading="the ii carries it (writer's-signature reading)" if ii else "the resolution carries it" if resol else "neither rule met")
H.run_seen(HERE, H.dres_rows, COLS, {"IIV": 0.035, "DRES": 0.04}, classify=classify, within_reading=True, readings=[
    dict(label="IIV_alone_same_songs", cols=["IIV"] + H.SEEN_STD, report=["IIV"]),
    dict(label="DRES_alone_same_songs", cols=["DRES"] + H.SEEN_STD, report=["DRES"]),
    dict(label="IIV_holding_TR", cols=["IIV", "TR"] + H.SEEN_STD, report=["IIV", "TR"], keep=lambda r: r.get("TR") is not None)])
