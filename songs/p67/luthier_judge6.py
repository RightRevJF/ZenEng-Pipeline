"""Luthier v8 stage 1, fix 752: a stopgap on the pick until the judge is rebuilt (stage 7). Needs luthier_judge5.py, luthier_judge4.py and
luthier_judge4_data.json beside it. The charge, the place among kept songs and the tie by distance are 715's; the window test is 730's.
A build is eligible for the pick when it is eligible under 730 and:
  no two notes share an onset (751);
  its longest run of one pitch is at or under the kept songs' 90th percentile (10 notes);
  its moves by step (1 or 2 semitones) and by leap (5 semitones or more) lie in the kept songs' middle halves;
  the share of its notes lying in runs of four or more of one pitch is at or under RUNS_CEILING.
RUNS_CEILING is the writer's setting, not a reading of kept songs: the kept median (about 12% of notes). Kept songs themselves reach 22% at
their 75th percentile, and the picks the writer set aside for chanting (songs 49, 51) lay inside the kept middle half. Call
pick(builds, runs="kept") to use the kept 75th instead. If no build passes, the pick falls back to 730's and the result says so.
score(notes) and pick(builds) take what luthier_judge4 takes: notes as (onset in twelfths of a beat from the song's first bar line, pitch, section label)."""
import numpy as np
import luthier_judge5 as J5
J = J5.J
def _runs(p):
    n = len(p); inrun = 0; r = 1; best = 1
    for i in range(1, n + 1):
        if i < n and p[i] == p[i - 1]: r += 1
        else:
            if r >= 4: inrun += r
            best = max(best, r); r = 1
    return inrun / max(1, n), best
def _motion(p): iv = np.abs(np.diff(p)); return float(np.mean((iv >= 1) & (iv <= 2))), float(np.mean(iv >= 5))
_K = np.array([list(_runs(list(s["p"]))) + list(_motion(s["p"])) for s in J._KEPT])
RUNS_MEDIAN, RUNS_75 = (float(x) for x in np.percentile(_K[:, 0], (50, 75))); LONGEST_90 = float(np.percentile(_K[:, 1], 90))
STEPS = tuple(float(x) for x in np.percentile(_K[:, 2], (25, 75))); LEAPS = tuple(float(x) for x in np.percentile(_K[:, 3], (25, 75)))
def score(notes, runs="writer"):
    r = J5.score(notes); ns = sorted(notes, key=lambda n: n[0]); t = [int(n[0]) for n in ns]; p = [int(n[1]) for n in ns]
    share, longest = _runs(p); st, lp = _motion(np.array(p)); ceil = RUNS_MEDIAN if runs == "writer" else RUNS_75
    tests = {"no two notes on one onset (751)": all(b > a for a, b in zip(t, t[1:])), "longest run of one pitch at or under the kept 90th": longest <= LONGEST_90,
             "steps in the kept middle half": STEPS[0] <= st <= STEPS[1], "leaps in the kept middle half": LEAPS[0] <= lp <= LEAPS[1],
             "notes in runs of four or more at or under the ceiling": share <= ceil}
    r["752: readings"] = {"notes in runs of four or more of one pitch": share, "longest run of one pitch": longest, "moves by step": st, "moves by leap": lp, "runs ceiling": ceil, "the ceiling is": "the writer's setting (kept median)" if runs == "writer" else "the kept 75th"}
    r["752: tests"] = tests; r["eligible under 730"] = r["eligible for the pick"]; r["eligible for the pick"] = bool(r["eligible under 730"] and all(tests.values())); return r
def pick(builds, runs="writer"):
    """builds: list of (id, notes). Returns (id of the pick, list of (id, result)). A result's 'eligible for the pick' is 752's."""
    R = [(i, score(n, runs)) for i, n in builds]; el = [(i, r) for i, r in R if r["eligible for the pick"]]; fell = False
    if not el: el = [(i, r) for i, r in R if r["eligible under 730"] and r["752: tests"]["no two notes on one onset (751)"]]; fell = True
    if not el: return None, R
    least = min(r["charge"] for _, r in el); near = [(i, r) for i, r in el if r["charge"] <= least + 0.02]; pk = min(near, key=lambda x: x[1]["distance from the kept medians"])[0]
    dict(R)[pk]["752: the pick fell back to 730's eligibility"] = fell; return pk, R
