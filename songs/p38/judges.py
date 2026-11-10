"""ZenEng v103, 27.47 (fixes 252-255): the content judge, the order reading, the combined score, the floor and the shortlist.
Weights and code from zeneng_v103_selector.json ('judges, ready to use'); a window is 8 bars, N = [(onset beats, dur beats, pitch, chord set)]."""
import json, numpy as np
_J = json.load(open("/home/claude/p38/tables/zeneng_v103_selector.json"))["judges, ready to use"]
CJ = _J["content_judge (fitted on kept chart windows against the builds of songs 21-37; for song 38)"]
OJ = _J["order_judge (fitted on kept chart windows against their own bar-shuffles)"]
KEPT = _J["kept percentiles, held out (log-odds)"]; FLOOR = -0.059
assert abs(_J["floor (fix 254): reject a build whose combined score is under"] - FLOOR) < 1e-9
exec(_J["order measures, code"], globals())                      # bars_of(N), measures(B): the paper's code (253)
def _lo(J, f):
    z = []
    for m, fill, mu, sd in zip(J["measures"], J["fill_missing_with"], J["mean"], J["sd"]):
        v = f.get(m, np.nan) if f else np.nan
        if v is None or not np.isfinite(v): v = fill
        z.append((v - mu) / sd)
    return float(J["intercept"] + np.dot(J["weight"], z))
def order_feats(N):
    m = measures(bars_of([(n[0], n[1], n[2]) for n in N]))
    return None if m is None else {k: m[k] for k in OJ["measures"]}
def score_window(content_f, N):
    of = order_feats(N); c = _lo(CJ, content_f); o = _lo(OJ, of or {})
    return dict(content=c, order=o, combined=(c + o) / 2, order_measures=of)
def give_away(content_f, k=5):
    """the measures that most give a build away: weight x z, most negative first (252)."""
    out = []
    for m, fill, mu, sd, w in zip(CJ["measures"], CJ["fill_missing_with"], CJ["mean"], CJ["sd"], CJ["weight"]):
        v = content_f.get(m, np.nan)
        if v is None or not np.isfinite(v): v = fill
        out.append((m, round(w * (v - mu) / sd, 3)))
    return sorted(out, key=lambda x: x[1])[:k]
