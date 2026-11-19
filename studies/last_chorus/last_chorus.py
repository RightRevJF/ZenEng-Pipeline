"""749.75: how kept songs lift the last chorus, when not by accompaniment density (POP909 says no). Two kept sources, last chorus against the first.
CoCoPops Billboard (corpora/cocopops_notes.csv.gz, voice; built by lib/luthier/cocopops_parse.py): a chorus instance is a run of sung notes labelled chorus.
  key (a modulation up), the sung line's mean and top pitch, notes, length in beats, and for the ~100 .varms songs the recording's loudness (rms) and the
  listeners' arousal at the sung notes.
McGill Billboard (studies/harmony/billboard_sections.json, 739 songs): the last chorus's bars against the first's, and how often a song ends on two
  choruses or more in a row. python3 studies/last_chorus/last_chorus.py -> last_chorus.json"""
import json, os, collections
import numpy as np, pandas as pd
from scipy.stats import wilcoxon, binomtest
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
d = pd.read_csv(os.path.join(ROOT, "corpora", "cocopops_notes.csv.gz"), low_memory=False); d = d[(d.dur > 0) & (d.lead == "voice")]
rows = []
for s, g in d.groupby("song", sort=False):
    g = g.sort_values("abs_beat").reset_index(drop=True); lab = g.section.astype(str).str.lower().values; inst = []; cur = None
    for i, l in enumerate(lab):
        if l == "chorus":
            if cur is None or i != cur[-1] + 1: cur = [i]; inst.append(cur)
            else: cur.append(i)
    inst = [x for x in inst if len(x) >= 8]
    if len(inst) < 2: continue
    a, z = g.iloc[inst[0]], g.iloc[inst[-1]]
    f = lambda x, c: float(x[c].astype(float).mean()) if x[c].notna().any() else np.nan
    kd = (int(z.key_pc.iloc[0]) - int(a.key_pc.iloc[0])) % 12 if a.key_pc.notna().all() and z.key_pc.notna().all() else None
    rows.append(dict(song=s, n_chorus=len(inst), key_up=kd, mean_p=f(z, "pitch") - f(a, "pitch"), top_p=float(z.pitch.max() - a.pitch.max()),
                     notes=len(z) - len(a), beats=float((z.abs_beat.iloc[-1] + z.dur.iloc[-1] - z.abs_beat.iloc[0]) - (a.abs_beat.iloc[-1] + a.dur.iloc[-1] - a.abs_beat.iloc[0])),
                     rms=f(z, "rms") - f(a, "rms") if a.rms.notna().any() and z.rms.notna().any() else np.nan,
                     arousal=f(z, "arousal") - f(a, "arousal") if a.arousal.notna().any() and z.arousal.notna().any() else np.nan))
R = pd.DataFrame(rows)
def summ(col):
    x = R[col].dropna(); x = x[np.isfinite(x)]
    if len(x) < 5: return None
    nz = x[x != 0]
    return dict(n=int(len(x)), median=round(float(x.median()), 2), quartiles=[round(float(q), 2) for q in x.quantile([0.25, 0.75])], share_up=round(float((x > 0).mean()), 3),
                share_down=round(float((x < 0).mean()), 3), wilcoxon_p=round(float(wilcoxon(nz).pvalue), 4) if len(nz) >= 5 else None)
out = dict(cocopops=dict(songs=int(len(R)), modulation=dict(songs_with_key_change=int((R.key_up.dropna() != 0).sum()), up_1_or_2=int(R.key_up.isin([1, 2]).sum()), of=int(R.key_up.notna().sum()),
                         key_changes=dict(collections.Counter(int(k) for k in R.key_up.dropna() if k != 0))),
                         **{c: summ(c) for c in ("mean_p", "top_p", "notes", "beats", "rms", "arousal")}))
M = json.load(open(os.path.join(ROOT, "studies", "harmony", "billboard_sections.json"))); mc = []; ends = []
for s in M:
    secs = [x for x in s["sections"] if x.get("label")]; ch = [x for x in secs if "chorus" in x["label"].lower()]
    if len(ch) >= 2: mc.append(len(ch[-1]["bars"]) - len(ch[0]["bars"]))
    labs = [x["label"].lower() for x in secs if x["label"].lower() not in ("silence", "end", "fadeout", "outro", "coda", "fade out")]
    if any("chorus" in l for l in labs):
        k = 0
        for l in reversed(labs):
            if "chorus" in l: k += 1
            else: break
        ends.append(k)
mc = np.array(mc); ends = np.array(ends)
out["mcgill"] = dict(songs_two_choruses=int(len(mc)), last_minus_first_bars=dict(median=float(np.median(mc)), quartiles=[float(q) for q in np.quantile(mc, (0.25, 0.75))], share_longer=round(float((mc > 0).mean()), 3),
                     share_shorter=round(float((mc < 0).mean()), 3), sign_p=round(float(binomtest(int((mc > 0).sum()), int((mc != 0).sum())).pvalue), 5)),
                     songs_with_a_chorus=int(len(ends)), end_on_two_or_more_choruses_in_a_row=round(float((ends >= 2).mean()), 3), end_on_a_chorus=round(float((ends >= 1).mean()), 3))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "last_chorus.json"), "w"), indent=1); print(json.dumps(out, indent=1))
