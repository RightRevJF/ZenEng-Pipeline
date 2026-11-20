"""Where do Luthier's own songs sit on the page gate, against the kept pop tunes? Study only."""
import sys, json, zlib, collections, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
REPO = "/home/claude/rightrevjf/zeneng-pipeline/"; MAJ = np.array([6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88]); MIN = np.array([6.33,2.68,3.52,5.38,2.60,3.53,2.54,4.75,3.98,2.69,3.34,3.17])
def ent(v):
    c = np.array(list(collections.Counter(v).values()), float); q = c / c.sum(); return float(-(q * np.log2(q)).sum())
def ivs(p): return [int(np.clip(p[i] - p[i - 1], -12, 12)) for i in range(1, len(p))]
class Model:                      # pitch-interval model, context up to 4, interpolated back-off
    def __init__(self, seqs, K=4):
        self.K = K; self.c = [collections.Counter() for _ in range(K + 2)]
        for s in seqs:
            for i in range(len(s)):
                for k in range(0, K + 1):
                    if i - k >= 0: self.c[k + 1][tuple(s[i - k:i + 1])] += 1; 
                    if i - k >= 0: self.c[0][("ctx", k) + tuple(s[i - k:i])] += 1
    def ic(self, s, minus=None):
        out = []
        for i in range(len(s)):
            p = 1 / 25.0
            for k in range(0, self.K + 1):
                if i - k < 0: break
                n = self.c[k + 1][tuple(s[i - k:i + 1])]; N = self.c[0][("ctx", k) + tuple(s[i - k:i])]
                if minus is not None: n -= minus[k + 1][tuple(s[i - k:i + 1])]; N -= minus[0][("ctx", k) + tuple(s[i - k:i])]
                p = (n + 2.0 * p) / (N + 2.0)
            out.append(-np.log2(max(p, 1e-9)))
        return float(np.mean(out))
def own(s, K=4):
    c = [collections.Counter() for _ in range(K + 2)]
    for i in range(len(s)):
        for k in range(0, K + 1):
            if i - k >= 0: c[k + 1][tuple(s[i - k:i + 1])] += 1; c[0][("ctx", k) + tuple(s[i - k:i])] += 1
    return c
def parts(p, d):
    p = np.asarray(p, float); d = np.clip(np.asarray(d, float), .0625, 8); h = np.bincount(p.astype(int) % 12, d, 12); cm = [np.corrcoef(np.roll(MAJ, k), h)[0, 1] for k in range(12)]; cn = [np.corrcoef(np.roll(MIN, k), h)[0, 1] for k in range(12)]; minor = max(cn) > max(cm); ton = int(np.argmax(cn if minor else cm)); pc = (p.astype(int) - ton) % 12
    a = np.abs(np.diff(p)); s = ivs(p.astype(int)); g4 = [tuple(s[i:i + 4]) for i in range(len(s) - 3)]; six = [0, 3, 5, 7, 8, 10] if minor else [0, 2, 4, 5, 7, 9]; five = [0, 3, 5, 7, 10] if minor else [0, 2, 4, 7, 9]
    return dict(six_note_share=float(np.isin(pc, six).mean()), five_note_share=float(np.isin(pc, five).mean()), time_on_tonic=float((pc == 0).mean()), different_pitches=ent(p), different_intervals=ent(np.diff(p)), leaps=float((a > 4).mean()), range=float(p.max() - p.min()), repeated_notes=float((a == 0).mean()), repeated_figures=1 - len(set(g4)) / max(len(g4), 1))
PLAIN = dict(surprise=-1, six_note_share=1, five_note_share=1, time_on_tonic=1, different_pitches=-1, different_intervals=-1, leaps=-1, range=-1, repeated_notes=1, repeated_figures=1)
kept = set(json.load(open(REPO + "tables/kept_songs_4-4_pop.json"))); D = pd.read_csv("/home/claude/zeneng/corpus/cocopops_notes.csv.gz"); K = {}
for sname, g in D.groupby("song", sort=False):
    if str(sname) in kept:
        g = g.sort_values("abs_beat"); g = g[g.pitch == g.pitch]
        if len(g) >= 100: K[str(sname)] = (g.pitch.astype(int).tolist(), np.r_[np.diff(g.abs_beat.values), 1.0].tolist())
M = Model([ivs(p) for p, _ in K.values()]); rows = {}
for n, (p, d) in K.items(): r = parts(p, d); r["surprise"] = M.ic(ivs(p), minus=own(ivs(p))); rows[n] = r
KD = pd.DataFrame(rows).T.astype(float); L = {}
for tag, path in (("55 Your Yard Man", "songs/p65/lyric55.song.json"), ("54", "songs/p64/lyric54.song.json"), ("58", "songs/p68/lyric58.song.json"), ("52 (6/8)", "songs/p62/lyric52.song.json")):
    R = json.load(open(REPO + path)); ns = [n for n in R["melody"]["notes"] if n.get("midi") is not None]; p = [n["midi"] for n in ns]; on = np.array([n["on"] for n in ns]) / 12.0; d = np.r_[np.diff(on), 1.0]; r = parts(p, d); r["surprise"] = M.ic(ivs(p)); L[f'{tag} {R.get("title", "") if tag[:2] != "55" else ""}'.strip()] = r
LD = pd.DataFrame(L).T.astype(float)
z = lambda col, v: (v - KD[col].mean()) / KD[col].std(); KD["plainness"] = sum(PLAIN[c] * z(c, KD[c]) for c in PLAIN) / len(PLAIN); LD["plainness"] = sum(PLAIN[c] * z(c, LD[c]) for c in PLAIN) / len(PLAIN); PL = dict(PLAIN, plainness=1)
print(f"kept pop tunes: {len(KD)}\n"); print(f"{'part (plain side)':34}{'kept 10th':>10}{'kept mid':>10}{'kept 90th':>10}   " + "   ".join(f"{k[:14]:>14}" for k in LD.index)); out = {}
for c in ["plainness", "surprise", "six_note_share", "five_note_share", "time_on_tonic", "different_pitches", "different_intervals", "leaps", "range", "repeated_notes", "repeated_figures"]:
    q = np.percentile(KD[c], [10, 50, 90]); cells = []
    for k in LD.index:
        v = LD.loc[k, c]; pct = float((KD[c] < v).mean() * 100); plain_pct = pct if PL[c] > 0 else 100 - pct; flag = " LOW" if plain_pct < 10 else (" high" if plain_pct > 90 else ""); cells.append(f"{v:6.2f} ({plain_pct:3.0f}){flag:5}"); out.setdefault(k, {})[c] = dict(value=float(v), plain_percentile=round(plain_pct, 1))
    print(f"{c + (' (lower is plainer)' if PL[c] < 0 else ''):34}{q[0]:10.2f}{q[1]:10.2f}{q[2]:10.2f}   " + "   ".join(f"{x:>14}" for x in cells))
print("\n(in brackets: the share of kept tunes the song is plainer than; under 10 would fail a floor set at the kept 10th percentile)")
json.dump(dict(kept=KD.describe().to_dict(), songs=out), open("measure_results.json", "w"), indent=1)
