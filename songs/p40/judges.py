"""ZenEng v108, fix 291 (252's refit): the content and order judges refitted on kept chart windows against the builds of songs 21-37
and song 38's rerun (Run B); the floor (254) and the kept percentiles from zeneng_v108_judges.json. The order measures' code is the
paper's (253), read from zeneng_v103_selector.json, measures unchanged."""
import json, numpy as np
_J = json.load(open("/home/claude/p40/tables/zeneng_v108_judges.json"))
CJ, OJ = _J["content_judge"], _J["order_judge"]
KEPT = _J["kept percentiles, held out (log-odds)"]; FLOOR = _J["floor (fix 254): reject a build whose combined score is under"]
exec(json.load(open("/home/claude/p40/tables/zeneng_v103_selector.json"))["judges, ready to use"]["order measures, code"], globals())
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
    out = []
    for m, fill, mu, sd, w in zip(CJ["measures"], CJ["fill_missing_with"], CJ["mean"], CJ["sd"], CJ["weight"]):
        v = content_f.get(m, np.nan)
        if v is None or not np.isfinite(v): v = fill
        out.append((m, round(w * (v - mu) / sd, 3)))
    return sorted(out, key=lambda x: x[1])[:k]
