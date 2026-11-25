"""Readings after the result (RESULT.md): features again on first-sung lines only (writes /home/claude/lyr_dl/covers_feat_first.csv). Then readings.py."""
import sys, runpy, numpy as np
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import linefeat as LF
from measures import YOU, I_, VOCABLES, words
_f = LF.features
def features(stanzas):
    r = _f(stanzas)
    if r is None: return None
    lines = [l for s in stanzas for l in s if words(l)]; seen = set(); first = []
    for l in lines:
        k = " ".join(words(l))
        if k not in seen: first.append(l); seen.add(k)
    r["syl_line_first"] = float(np.mean([LF.syl(l) for l in first]))
    ws = [w for l in first for w in words(l) if w not in VOCABLES]
    r["iyou_first"] = 100 * sum(w in YOU or w in I_ for w in ws) / max(1, len(ws)); r["you_lines_first"] = float(np.mean([any(w in YOU for w in words(l)) for l in first]))
    return r
LF.features = features
src = open(__import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)), "build.py")).read().replace("covers_feat.csv", "covers_feat_first.csv")
exec(compile(src, "build_first", "exec"))   # run from the repo root: python3 studies/covers_lines/first_lines.py
