"""Luthier v20, stage 7 (Module 27.101; fixes 858-864): the judge, rebuilt as a gate and a pick, with a standing bench.

What the bench showed of the old judge (715's charge, 730's window, 752's tests): it answers damage (a kept song with a tenth of its notes re-pitched is charged
more nine times in ten) and it has no relation to how a kept song fared (Spearman with weeks on the chart -0.01, with peak 0.09). So it is a judge of likeness,
and its last step, 'nearest the kept medians', asked for the most average song, which no kept song is: a kept song lies inside the middle half on twenty
readings at once about once in a million.

860  THE GATE. A candidate's readings are read together against the kept songs' own, one song a row (tables/metre_atlas/kept_readings.json): the distance from the
     kept centre in the kept songs' own spread and correlations (Mahalanobis, the covariance shrunk three-tenths toward the identity). A candidate passes if it
     is no further out than nine kept songs in ten are, each kept song read with itself left out. Readings the lyric sets (density, gap classes, range) are left out.
861  THE PICK. Among those that pass, not the nearest the centre: the one whose distance is nearest the kept songs' own median distance, the place a kept song
     usually stands. If none passes, the least distance, and the record says so.
862  The pick is never graded by the reading that chose it: the record prints the old charge beside it, and the 4/4 judge's place where that judge can read it.
     python3 lib/luthier/luthier_judge7.py           # prints the gate's figures for each kept table
Nothing here says a pick is great. The bench (lib/luthier/judge_bench.py) is the standing test of any reading that claims to."""
import json, os, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROWS = os.path.join(HERE, "..", "..", "tables", "metre_atlas", "kept_readings.json")
LYRIC_SET = ("notes a bar", "notes a beat", "gaps of a sixteenth", "gaps of an eighth", "gaps of a quarter or more", "gaps of half a beat", "gaps of a third of a beat", "gaps of a beat or more",
             "gaps under a third of a beat", "range", "distinct pitches")
class Judge7:
    def __init__(self, table, shrink=0.3, gate=0.90):
        T = json.load(open(ROWS)).get(table)
        if T is None: raise KeyError(table)
        self.table = table; names = [n for n in T["names"] if n not in LYRIC_SET]; idx = [T["names"].index(n) for n in names]; X = np.array(T["rows"], float)[:, idx]
        keep = X.std(0) > 1e-9; self.names = [n for n, k in zip(names, keep) if k]; X = X[:, keep]; self.n = len(X)
        self.mu = X.mean(0); self.sd = X.std(0); Z = (X - self.mu) / self.sd; S = np.cov(Z.T); self.Si = np.linalg.inv((1 - shrink) * S + shrink * np.eye(len(self.names)))
        loo = []
        for i in range(self.n):                                                              # each kept song against the others
            R = np.delete(X, i, 0); mu, sd = R.mean(0), R.std(0); Zr = (R - mu) / sd; Si = np.linalg.inv((1 - shrink) * np.cov(Zr.T) + shrink * np.eye(len(self.names))); z = (X[i] - mu) / sd; loo.append(float(np.sqrt(z @ Si @ z)))
        self.loo = np.array(loo); self.gate = float(np.quantile(self.loo, gate)); self.usual = float(np.median(self.loo)); self.band = [float(x) for x in np.quantile(self.loo, (0.25, 0.75))]
    def distance(self, readings):
        z = (np.array([float(readings[n]) for n in self.names]) - self.mu) / self.sd; return float(np.sqrt(z @ self.Si @ z))
    def pick(self, cands):
        """cands: [(id, readings)]. Returns (id, report)."""
        D = [(i, self.distance(r)) for i, r in cands]; ok = [(i, d) for i, d in D if d <= self.gate]
        rep = dict(table=self.table, kept_songs=self.n, readings=self.names, gate=round(self.gate, 3), a_kept_songs_usual_distance=round(self.usual, 3), kept_middle_half=[round(x, 3) for x in self.band], candidates=len(D), pass_the_gate=len(ok),
                   candidates_distance_quartiles=[round(float(x), 3) for x in np.quantile([d for _, d in D], (0.25, 0.5, 0.75))] if D else None)
        if ok: i, d = min(ok, key=lambda x: (abs(x[1] - self.usual), str(x[0]))); rep["the pick fell back to the least distance"] = False
        elif D: i, d = min(D, key=lambda x: (x[1], str(x[0]))); rep["the pick fell back to the least distance"] = True
        else: return None, rep
        rep["pick_distance"] = round(d, 3); rep["distances"] = {str(a): round(b, 3) for a, b in D}; return i, rep
if __name__ == "__main__":
    for t in json.load(open(ROWS)):
        J = Judge7(t); print(f"{t}: {J.n} kept songs, {len(J.names)} readings read together; the gate {J.gate:.2f} (nine kept songs in ten, each left out in turn); a kept song's usual distance {J.usual:.2f}, middle half {J.band[0]:.2f} to {J.band[1]:.2f}")
