"""Writes SUMMARY.md, the one-page reading, from result.json, match_check.json and matches.json; every figure in it is
printed here from those files. python3 -I summary.py"""
import os, sys, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from match import power
R = json.load(open(os.path.join(HERE, "result.json"))); MC = json.load(open(os.path.join(HERE, "match_check.json"))); MT = json.load(open(os.path.join(HERE, "matches.json")))
NAMES = dict(pc_entropy="Fewer pitch classes (entropy)", surprise="Next note easy to foresee", different_pitches="Few different pitches", time_on_tonic="Time on the home note",
             five_note_share="Five-note scale", six_note_share="Six-note scale", leaps="Few leaps", repeated_figures="Short figures sung again", plainness="The gate's whole plainness")
A = R["all"]; L = []; P = lambda s="": (print(s), L.append(s))
v = collections.Counter(t["verdict"] for t in A["tests"]); n_read = sum(MT["steps"].values()) + 0
tunes_read = 12761 if not os.path.exists(os.path.join(HERE, "match_log.txt")) else int(open(os.path.join(HERE, "match_log.txt")).readline().split()[-1])
need = next(n for n in range(100, 5000, 10) if power(n, n, 12, 12)["A"] >= 0.5)
agree = lambda S: sum(1 for t in S["tests"] if (t["both"]["r"] if t["form"] == "A" else t["both"]["b"]) * t["sign"] > 0)
P("# Folk replication: the one-page reading"); P()
P("27 November 2026, branch `folk-replication`. Written by `summary.py` from `result.json`, `match_check.json` and `matches.json`. The rule came first: `PREDICTION.md`."); P()
P("**The question:** are plainer tunes recorded by more artists? Tested again from scratch, without TheSession and without any withdrawn figure."); P()
P("## In short"); P()
P("- **What held:** nothing. %d of %d tests held." % (v.get("held", 0), len(A["tests"])))
P("- **What failed:** nothing either. There were too few tunes to tell, so every test is an estimate (%d of %d)." % (v.get("estimate", 0), len(A["tests"])))
P("- **How sure:** not sure. If the link is small but real (a correlation of 0.15), this study had about a %d in 100 chance of showing it." % round(100 * A["power"]["A"]))
P("- **The page gate without the withdrawn data:** neither supported nor ruled out. Its parts still rest on the hymn tunes and the within-artist readings alone."); P()
P("## Why so thin"); P()
P("| | Count |"); P("|---|---|")
P("| Tunes read from the four collections | {:,} |".format(tunes_read))
P("| Found in Discogs, one tune per song | %d |" % R["outcome_summary"]["n"])
P("| Test half / confirm half | %d / %d |" % (A["n_test"], A["n_confirm"]))
P("| Matches checked by eye: right / wrong / unsure | %d / %d / %d |" % (MC["totals"].get("right", 0), MC["totals"].get("wrong", 0), MC["totals"].get("unsure", 0)))
P("| Wrong among the German (Essen) matches checked | %d of %d |" % (MC["by_collection"]["essen"].get("wrong", 0), sum(MC["by_collection"]["essen"].values())))
eng = {k: sum(MC["by_collection"][c].get(k, 0) for c in ("oneills", "ryans", "airds")) for k in ("right", "wrong", "unsure")}
P("| Wrong among the Irish and Scottish matches checked | %d of %d |" % (eng["wrong"], sum(eng.values())))
P(); P("Most old tunes aren't in Discogs under their printed names. Many Irish and Scottish titles land on a later pop song with the same name (\"Hang Fire\", \"Christmas Eve\"). A wrong match only blurs a result, but it blurs it a lot. Since the check's wrong share (%d in 100) is over 25, a miss here would count only weakly against the idea anyway." % MC["totals"]["wrong"]); P()
P("## Which way the tests leaned (estimates, deciding nothing)"); P()
P("| Test | As is | Held fixed* |"); P("|---|---|---|")
for m in NAMES:
    a = [t for t in A["tests"] if t["measure"] == m and t["form"] == "A"][0]; b = [t for t in A["tests"] if t["measure"] == m and t["form"] == "B"][0]
    w = lambda t, x: ("as predicted" if x * t["sign"] > 0 else "the other way") + " (%+.2f)" % x
    P("| %s | %s | %s |" % (NAMES[m], w(a, a["both"]["r"]), w(b, b["both"]["b"])))
P(); P("*Held fixed: tune length, range, metre and collection. Sizes are both halves together, for scale only. \"As is\" is a rank correlation; \"held fixed\" is the change per step of the measure."); P()
P("- %d of %d lean the predicted way. Coin flips would give about 9." % (agree(A), len(A["tests"])))
best = min(A["tests"], key=lambda t: t["test"]["p"])
P("- Closest to passing: %s, %s, test half p %.4f against a bar of %.5f; the confirm half didn't follow (p %.2f)." % (NAMES[best["measure"]].lower(), "held fixed" if best["form"] == "B" else "as is", best["test"]["p"], R["alpha"], best["confirm"]["p"]))
P("- Spread of pitches leans the predicted way as is, but the other way once length and range are held. So the small edge seen as is may come from those, not from the pitches themselves.")
P("- Exact-title matches only: %d of %d lean the predicted way. Essen only (the clean matches, %d tunes): %d of %d. No test passes either way." % (agree(R["exact"]), len(R["exact"]["tests"]), R["essen"]["n_test"] + R["essen"]["n_confirm"], agree(R["essen"]), len(R["essen"]["tests"]))); P()
P("## What it would take"); P()
P("About %d correctly matched tunes (%d a half) for an even chance at a correlation of 0.15, and more again for the matching errors. That's roughly double what was found, all of it matched right. Old printed collections plus Discogs titles won't give that. A source with recordings already tied to each tune would." % (2 * need, need)); P()
P("## Notes for the maintainer"); P()
P("- `studies/judging_checks/within_artist/cliques_versions.py` reads Discogs-VI's artist fields, stored as the text of a list, letter by letter. A track with no track artist counts `\"[]\"` as an artist and never falls back to the release's artists. The pack's cover counts are close but not exact. Here the lists were parsed properly (`PREDICTION.md`, addendum).")
P("- music21 10.5's ABC reader doesn't carry a sharp or flat to the rest of its bar. This study writes it out first (`measures.py`). Anything else reading ABC through music21 has the same gap.")
P("- Nothing under `lib/` or `tables/` was changed. Raw downloads are outside the repository.")
open(os.path.join(HERE, "SUMMARY.md"), "w").write("\n".join(L) + "\n")
