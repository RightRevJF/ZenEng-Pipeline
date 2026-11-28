"""Folk replication: the tests, by PREDICTION.md. Joins clique_counts.json (outside the repo) to matches.json for the first
time, runs the 18 tests on the test half and their confirmations on the other, the same on exact-title matches only, and
writes result.json and RESULT.md from the figures it prints. One command:
python3 -I run.py /home/claude/dl/discogsvi/clique_counts.json"""
import sys, os, json, gzip, collections, math, datetime, subprocess
import numpy as np
from scipy import stats
import statsmodels.api as sm
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from match import MEASURES, ALPHA, RHO, K_TESTS, power, mde, pooled_groups, n_controls
SIGN = dict(pc_entropy=-1, surprise=-1, different_pitches=-1, time_on_tonic=1, five_note_share=1, six_note_share=1, leaps=-1, repeated_figures=1, plainness=1)
NAMES = dict(pc_entropy="Pitch-class entropy", surprise="Next note easy to foresee", different_pitches="Few different pitches", time_on_tonic="Time on the home note",
             five_note_share="Five-note scale", six_note_share="Six-note scale", leaps="Few leaps", repeated_figures="Short figures sung again", plainness="The gate's whole plainness")

def one_sided(stat_sign_ok_p2, sign_match):
    return stat_sign_ok_p2 / 2 if sign_match else 1 - stat_sign_ok_p2 / 2

def form_a(x, y, s):
    r, p2 = stats.spearmanr(x, y); return dict(r=float(r), p=float(one_sided(p2, np.sign(r) == s)), p_other=float(one_sided(p2, np.sign(r) == -s)), n=len(x))

def form_b(rows, m, s):
    met = pooled_groups([r["metre"] for r in rows], 5, "other"); col = pooled_groups([r["collection"] for r in rows], 5, "oneills")
    x = np.array([r[m] for r in rows], float); x = (x - x.mean()) / x.std()
    X = [x, np.array([r["ln_notes"] for r in rows]), np.array([r["range"] for r in rows], float)]
    for g, vals in (("m", met), ("c", col)):
        lv = sorted(set(vals))
        for v in lv[1:]: X.append(np.array([1.0 if q == v else 0.0 for q in vals]))
    X = sm.add_constant(np.column_stack(X)); y = np.log(np.array([r["n_sets"] for r in rows], float))
    f = sm.OLS(y, X).fit(cov_type="HC3"); b, se = float(f.params[1]), float(f.bse[1]); t = b / se; df = f.df_resid
    return dict(b=b, se=se, p=float(stats.t.sf(s * t, df)), p_other=float(stats.t.sf(-s * t, df)), n=len(rows))

def verdict(pw, t, c):
    if pw < 0.5: return "estimate"
    if t["p"] < ALPHA and c["p"] < 0.05: return "held"
    if t["p_other"] < ALPHA: return "missed, the other way"
    return "missed"

def run_set(rows, label):
    T = [r for r in rows if r["half"] == 0]; C = [r for r in rows if r["half"] == 1]
    pw = power(len(T), len(C), n_controls(T), n_controls(C))
    out = dict(label=label, n_test=len(T), n_confirm=len(C), power=pw, mde=dict(A=mde(len(T), len(C), n_controls(T), n_controls(C), "A"), B=mde(len(T), len(C), n_controls(T), n_controls(C), "B")), tests=[])
    for m in MEASURES:
        s = SIGN[m]
        for form in ("A", "B"):
            if form == "A":
                t = form_a([r[m] for r in T], [r["n_sets"] for r in T], s); c = form_a([r[m] for r in C], [r["n_sets"] for r in C], s)
                both = form_a([r[m] for r in rows], [r["n_sets"] for r in rows], s)
            else:
                t = form_b(T, m, s); c = form_b(C, m, s); both = form_b(rows, m, s)
            out["tests"].append(dict(measure=m, form=form, sign=s, power=pw[form], test=t, confirm=c, both=both, verdict=verdict(pw[form], t, c)))
    return out

def fmt_size(d, form): return ("%+.3f" % d["r"]) if form == "A" else ("%+.3f" % d["b"])

def main(counts_path):
    M = {r["id"]: r for r in json.load(gzip.open(os.path.join(HERE, "measures.json.gz"), "rt"))["rows"]}
    mt = json.load(open(os.path.join(HERE, "matches.json"))); counts = json.load(open(counts_path))
    rows = []
    for r in mt["rows"]:
        row = dict(M[r["id"]]); row.update(half=r["half"], step=r["step"], n_sets=int(counts[str(r["clique"])] if str(r["clique"]) in counts else counts[r["clique"]]))
        rows.append(row)
    rows = [r for r in rows if r["n_sets"] >= 1]
    exact = [r for r in rows if r["step"] == "exact"]
    res = dict(made=datetime.datetime.now().isoformat(timespec="seconds"), commit=subprocess.run(["git", "-C", HERE, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip(),
               k=K_TESTS, alpha=ALPHA, rho_for_power=RHO, outcome_summary=dict(median=float(np.median([r["n_sets"] for r in rows])), mean=float(np.mean([r["n_sets"] for r in rows])), max=int(max(r["n_sets"] for r in rows)), n=len(rows)),
               all=run_set(rows, "all matches"), exact=run_set(exact, "exact-title matches only"))
    json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1)
    L = []; P = lambda s="": (print(s), L.append(s))
    P("# Folk replication: result"); P()
    P("Printed by `python3 -I studies/folk_replication/run.py <clique_counts.json>` at %s (code at %s), which wrote this file and `result.json`. The rule: `PREDICTION.md`." % (res["made"], res["commit"])); P()
    o = res["outcome_summary"]; P("Matched tunes with an outcome: %d. Artists per tune: median %.0f, mean %.1f, most %d." % (o["n"], o["median"], o["mean"], o["max"])); P()
    P("K = %d tests; pass level .05 / %d = %.5f one-sided. Power is for a correlation of %.2f (test half at the pass level, times the confirm half at .05)." % (K_TESTS, K_TESTS, ALPHA, RHO)); P()
    for key in ("all", "exact"):
        S = res[key]
        P("## %s%s" % (S["label"][0].upper() + S["label"][1:], " (deciding)" if key == "all" else " (reported, deciding nothing)")); P()
        P("Test half %d tunes, confirm half %d. Power: form A %.3f, form B %.3f. Smallest correlation with power one half: A %.3f, B %.3f.%s" % (
            S["n_test"], S["n_confirm"], S["power"]["A"], S["power"]["B"], S["mde"]["A"], S["mde"]["B"], " **Power is under one half, so every test here is an estimate.**" if max(S["power"].values()) < 0.5 else "")); P()
        P("| Test | Form | Predicted | Test half: size, p | Confirm half: size, p | Both halves: size | Verdict |"); P("|---|---|---|---|---|---|---|")
        for t in S["tests"]:
            P("| %s | %s | %s | %s, %.4f | %s, %.3f | %s | %s |" % (NAMES[t["measure"]], "as is" if t["form"] == "A" else "held", "lower" if t["sign"] < 0 else "higher",
                                                             fmt_size(t["test"], t["form"]), t["test"]["p"], fmt_size(t["confirm"], t["form"]), t["confirm"]["p"], fmt_size(t["both"], t["form"]), t["verdict"]))
        P(); vc = collections.Counter(t["verdict"] for t in S["tests"]); P("Verdicts: " + ", ".join("%s %d" % kv for kv in sorted(vc.items()))); P()
        agree = sum(1 for t in S["tests"] if np.sign(t["both"]["r"] if t["form"] == "A" else t["both"]["b"]) == t["sign"])
        P("Tests whose both-halves size has the predicted sign: %d of %d." % (agree, len(S["tests"]))); P()
    P("Sizes: form A is Spearman's correlation with the number of artists; form B is the change in log(artists) per standard deviation of the measure, with log length, range, metre and collection held. p is one-sided, in the predicted direction.")
    open(os.path.join(HERE, "RESULT.md"), "w").write("\n".join(L) + "\n")

if __name__ == "__main__":
    main(sys.argv[1])
