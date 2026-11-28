"""Notes-side: are the 226 two-file songs near-duplicates? Re-run stability excluding pairs whose PCE_ALL and NPB agree to 1e-3.
Also outcome-free arithmetic from fit.json's r. Writes /home/claude/dl/run12/inventor_dup_check.json."""
import json, sys, numpy as np
from scipy.stats import spearmanr
from scipy.special import polygamma
from multiprocessing import Pool
sys.path.insert(0, "."); import inventor_rough_check as M
S = json.load(open("/home/claude/dl/run12/lakh_notes_side.json")); pairs = [s for s in S if len(s["md5s"]) >= 2]
with Pool(2) as P: res = P.map(M.job, pairs)
ok = [v for _, v in res if len(v) == 2 and v[0] and v[1]]
dup = [abs(a["PCE_ALL"] - b["PCE_ALL"]) < 1e-3 and abs(a["NPB"] - b["NPB"]) < 1e-3 for a, b in ok]
nd = [p for p, d in zip(ok, dup) if not d]
out = dict(pairs=len(ok), near_duplicates=int(sum(dup)))
for k in ["ROUGH", "ROUGH_BEAT", "NPB", "PCE_ALL", "PCE_SKY"]:
    out["stab_nodup_" + k] = round(float(spearmanr([a[k] for a, _ in nd], [b[k] for _, b in nd])[0]), 3)
r = 0.6628669583462676; tg = lambda x: float(polygamma(1, x))
out["var_log_eta_prior"] = tg(r)
out["attenuation_trigamma(r+N)/trigamma(r)"] = {N: round(tg(r + N) / tg(r), 4) for N in (0, 1, 2, 3, 5, 10, 30)}
out["R_from_shape_1/(R-1)=r"] = 1 + 1 / r; out["R_from_varlog_(R-1)^2=trigamma(r)"] = 1 + tg(r) ** 0.5
json.dump(out, open("/home/claude/dl/run12/inventor_dup_check.json", "w"), indent=1); print(json.dumps(out, indent=1))
