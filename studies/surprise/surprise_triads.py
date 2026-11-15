"""Sensitivity: chords reduced to triads (major, minor, diminished, augmented, suspended) in both the corpus and our songs, since
Hooktheory transcribers often simplify colour chords (add9, maj7, 9ths) that our songs write out."""
import json, gzip, sys
import numpy as np
sys.path.insert(0, "/home/claude/shape")
import surprise_hooktheory as SH, surprise_our_songs as OS
TRI = {0: 0, 1: 1, 2: 2, 3: 3, 4: 0, 5: 0, 6: 1, 7: 7, 8: 8}
def tri(t): return (t // 9) * 9 + TRI[t % 9]
D = json.load(gzip.open(SH.SRC)); seqs = []
for c in D.values():
    mm, cc = SH.tokens(c)
    if len(mm) >= 12 and len(cc) >= 4: seqs.append(OS.dedupe([tri(x) for x in cc]))
rng = np.random.default_rng(9); idx = rng.permutation(len(seqs)); test = set(idx[:3000].tolist())
CMt = SH.VOM(108).fit([s for i, s in enumerate(seqs) if i not in test])
ref = np.array([np.mean(SH.score(CMt, seqs[i])[0]) for i in sorted(test)])
CM = SH.VOM(108).fit(seqs)
print("held-out corpus median %.2f bits; share of 'other' chords in the corpus %.3f" % (np.median(ref), np.mean([x % 9 == 8 for s in seqs for x in s])))
import re, pickle
def tri_sym(sym, tonic):
    m = re.match(r"([A-G])([#b]?)(.*)", sym.split("/")[0]); root = (OS.PC[m.group(1)] + (1 if m.group(2) == "#" else -1 if m.group(2) == "b" else 0)) % 12; q = m.group(3)
    k = 2 if q.startswith("dim") else 3 if (q.startswith("aug") or q.startswith("+")) else 7 if q.startswith("sus") else 1 if (q.startswith("m") and not q.startswith("maj")) else 0
    return ((root - tonic) % 12) * 9 + k
SYMS = {}
for d in ("p42", "p45", "p48", "p49"):
    r = pickle.load(open(f"{OS.SONGS}/{d}/song_record.pkl", "rb")); SYMS[d] = [b["chord"] for b in r["bars"] if b.get("chord")]
SYMS["p62"] = json.load(open(f"{OS.SONGS}/p62/melody_final.json"))["chords"]
sys.path.insert(0, f"{OS.SONGS}/p63"); import gen34 as G; SYMS["p63"] = G.VERSE_CH + G.REFRAIN_CH
for s in OS.load_songs():
    ct = OS.dedupe([tri_sym(c, s["tonic"]) for c in SYMS[s["folder"]]]); ic = float(np.mean(SH.score(CM, ct)[0]))
    print("%-45s chords (triads) %.2f bits (%2.0fth pct); 'other' share in the original %.2f" % (s["title"][:45], ic, (ref < ic).mean() * 100, np.mean([x % 9 == 8 for x in s["chords"]])))
