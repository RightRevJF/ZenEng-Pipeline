"""Test 3: the rhyme detector against CoCoPops's hand-marked rhymes. A line is a transcriber's line (a syllable written with a capital, as lines_cocopops.py);
by hand it is rhymed if its last word carries a rhyme mark; by the detector, if its end rhymes within four lines either side."""
import glob, re, json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import linefeat as LF
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."); tp = fp = fn = tn = 0; used = 0; unk = 0
for path in sorted(glob.glob(R + "/corpora/CoCoPops/Billboard/Data/*.hum")):
    sp = None; syls = []                                  # (text, rhyme mark?)
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        if not line or line[0] in "!=": continue
        t = line.split("\t")
        if line.startswith("**"): sp = t; continue
        if sp is None or line.startswith("*") or len(t) != len(sp): continue
        if "**silbe" not in sp or "**rhyme" not in sp: break
        si = sp.index("**silbe"); ri = sp.index("**rhyme")
        if t[si] not in (".", ""): syls.append([t[si], t[ri] not in (".", "")])
    if not syls: continue
    lines = []; cur = []; word = ""; mark = False                                # words with marks, cut into lines at a capital
    for s, m in syls:
        if not word and s[:1].isupper() and s not in ("I", "I'm", "I'll", "I've", "I'd") and cur: lines.append(cur); cur = []
        word += s.strip("-_~"); mark = mark or m
        if not s.endswith("-"): cur.append((word, mark)); word = ""; mark = False
    if cur: lines.append(cur)
    lines = [[(LF.words(w), m) for w, m in l] for l in lines]; lines = [[(w[0], m) for w, m in l if w and w[0] not in LF.VOCABLES] for l in lines]; lines = [l for l in lines if l]
    if len(lines) < 8: continue
    used += 1; ends = [l[-1][0] for l in lines]
    for i, l in enumerate(lines):
        d = LF.rhymed(ends, i)
        if d is None: unk += 1; continue
        g = l[-1][1]; tp += d > 0 and g; fp += d > 0 and not g; fn += d == 0 and g; tn += d == 0 and not g
p = tp / (tp + fp); r = tp / (tp + fn); out = dict(songs=used, lines=tp + fp + fn + tn, unknown_ends=unk, precision=round(p, 3), recall=round(r, 3), f1=round(2 * p * r / (p + r), 3), by_hand_rhymed=round((tp + fn) / (tp + fp + fn + tn), 3), by_detector=round((tp + fp) / (tp + fp + fn + tn), 3))
json.dump(out, open(os.path.dirname(os.path.abspath(__file__)) + "/rhyme_check.json", "w"), indent=1); print(out)
