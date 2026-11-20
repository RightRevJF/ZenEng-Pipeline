"""Hold-out (song 59): how far every living build's median goes from the kept median toward its aimed song's reading, per check, for songs 55, 54, 58 (studies/review19/aimpool.json, v34) and 59 (aimpool59.json).
share closed = (builds - kept median) / (aim - kept median); 1 is on the aim, 0 is the kept middle, below 0 the wrong way. Gap = |builds - aim| over the kept middle half's width."""
import os, json, sys, numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path[:0] = [os.path.join(ROOT, "studies", "soundness"), os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas")]; sys.argv = sys.argv[:1]
import soundness as S
K = S.kept_rows(); W = {}
A = json.load(open(os.path.join(ROOT, "studies", "review19", "aimpool.json"))); A.update(json.load(open(os.path.join(ROOT, "studies", "holdout59", "aimpool59.json"))))
out = {}
for s, v in A.items():
    rows = {}
    for k, c in v["checks"].items():
        q = np.percentile([r[k] for r in K.values() if r.get(k) is not None], (25, 75)); w = float(q[1] - q[0]); d = c["aim"] - c["kept_median"]
        rows[k] = dict(aim=c["aim"], builds=c["builds_median"], kept=c["kept_median"], share_closed=round((c["builds_median"] - c["kept_median"]) / d, 2) if abs(d) > 0.1 * w else None, gap_in_kept_widths=round(abs(c["builds_median"] - c["aim"]) / w, 2))
    out[s] = dict(aims_at=v["aims_at"], checks=rows, median_gap=round(float(np.median([r["gap_in_kept_widths"] for r in rows.values()])), 2),
                  median_share_closed=round(float(np.median([r["share_closed"] for r in rows.values() if r["share_closed"] is not None])), 2))
    print(s, v["aims_at"], "median gap", out[s]["median_gap"], "median share closed", out[s]["median_share_closed"]); [print(f"   {k:32s} aim {r['aim']:<6} builds {r['builds']:<6} kept {r['kept']:<6} closed {r['share_closed']}  gap {r['gap_in_kept_widths']}") for k, r in rows.items()]
json.dump(out, open(os.path.join(ROOT, "studies", "holdout59", "aim_table.json"), "w"), indent=1)
