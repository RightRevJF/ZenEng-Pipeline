"""Run 09, gap_writer08: R09-L1's lead on SEEN songs (run 08 songs; their outcomes were opened in run 08). The ii-V read upstream
(Real Book / BiaB charts) and the iReal-minus-upstream gap, entered together. A LEAD: not in K, passes nothing, kills nothing.
Rules in PREDICTION.md. Run once:  python3 -I test.py"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import common09 as C9      # the guard: harness09 reads the outcome only through C9.load_outcomes / C9.guard, AFTER printing power
import harness09 as H

COLS = ["IIV_up", "GAP"] + H.GAP_CTRL + ["ln_n_ireal"]
def classify(res, rd):
    bu, bg = res["IIV_up"], res["GAP"]
    song_x = not (bu["range95"][0] <= 0.045 <= bu["range95"][1])
    writer_x = bu["range95"][0] > 0.01 or bg["range95"][1] < 0.03
    lab = ("song story (writer story excluded)" if writer_x and not song_x else "writer story (song story excluded)" if song_x and not writer_x
           else "neither story excluded" if not song_x and not writer_x else "both stories excluded")
    return dict(song_story_excluded=bool(song_x), writer_story_excluded=bool(writer_x), reading=lab)
H.run_seen(HERE, H.gap_rows, COLS, {"IIV_up": 0.045, "GAP": 0.0}, classify=classify, power_betas={"IIV_up": 0.045, "GAP": 0.03}, readings=[
    dict(label="without_ln_n_ireal", cols=["IIV_up", "GAP"] + H.GAP_CTRL, report=["IIV_up", "GAP"]),
    dict(label="IIV_up_alone", cols=["IIV_up"] + H.GAP_CTRL[:5], report=["IIV_up"]),
    dict(label="IIV_ireal_alone_same_songs", cols=["IIV_ireal"] + H.GAP_CTRL[5:], report=["IIV_ireal"])])
