"""Where our songs sit against the popular corpus: the Hooktheory surprise model (trained on all 21,998 clips) scores the melody
and chords of the songs whose records are on disk, and places each against the distribution of the cross-fitted Hooktheory clips.
Lower surprise went with more views (study_surprise_views.py), so the percentile says how conventional each song's notes are."""
import json, pickle, re, sys, gzip
import numpy as np
sys.path.insert(0, "/home/claude/shape")
import surprise_hooktheory as SH
SONGS = "/home/claude/zeneng-pipeline/songs"
PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def chord_token(sym, tonic):
    m = re.match(r"([A-G])([#b]?)(.*)", sym.split("/")[0])
    root = (PC[m.group(1)] + (1 if m.group(2) == "#" else -1 if m.group(2) == "b" else 0)) % 12; q = m.group(3)
    if q.startswith("maj7") or q.startswith("maj9") or q.startswith("M7"): iv = (4, 3, 4) + ((3,) if "9" in q else ())
    elif q.startswith("m7") or q.startswith("min7") or q.startswith("m9"): iv = (3, 4, 3) + ((4,) if "9" in q else ())
    elif q.startswith("dim"): iv = (3, 3)
    elif q.startswith("aug") or q.startswith("+"): iv = (4, 4)
    elif q.startswith("sus4") or q.startswith("sus"): iv = (5, 2) + ((3,) if "7" in q else ())
    elif q.startswith("m") and not q.startswith("maj"): iv = (3, 4)
    elif q.startswith("7") or q.startswith("9"): iv = (4, 3, 3) + ((4,) if q.startswith("9") else ())
    elif "add9" in q: iv = (2, 2, 3)
    else: iv = (4, 3)
    return ((root - tonic) % 12) * 9 + SH.qual(iv)
def mel_tokens(pitches, tonic):
    out = []; prev = None
    for p in pitches:
        out.append(((p - tonic) % 12) * 7 + (SH.ib(p - prev) if prev is not None else 3)); prev = p
    return out
def dedupe(t): return [x for i, x in enumerate(t) if i == 0 or t[i - 1] != x]
def load_songs():
    S = []
    for d, label in (("p42", None), ("p45", None), ("p48", None), ("p49", None)):
        r = pickle.load(open(f"{SONGS}/{d}/song_record.pkl", "rb"))
        key = r["bars"][0]["key"].split()[0]; tonic = (PC[key[0]] + (1 if "#" in key else -1 if "b" in key or "-" in key else 0)) % 12
        lead = sorted([e for e in r["lead"] if e.get("singer", "voice") == "voice" or True], key=lambda e: e["on"])
        S.append(dict(folder=d, title=r["title"], tonic=tonic, mel=[e["midi"] for e in lead], chords=dedupe([chord_token(b["chord"], tonic) for b in r["bars"] if b.get("chord")])))
    m = json.load(open(f"{SONGS}/p62/melody_shaped.json")) if False else None
    m52 = json.load(open(f"{SONGS}/p62/melody_final.json")); shaped = json.load(open(f"{SONGS}/p62/melody_shaped.json"))
    notes = shaped.get("pick", shaped).get("notes") if isinstance(shaped, dict) else shaped
    if notes is None: notes = m52["pick"]["notes"]
    S.append(dict(folder="p62", title="The Room Next Door (song 52, third edition)", tonic=2, mel=[n["p"] if "p" in n else n["midi"] for n in sorted(notes, key=lambda n: n["on"])],
                  chords=dedupe([chord_token(c, 2) for c in m52["chords"]])))
    m53 = json.load(open(f"{SONGS}/p63/melody_final_v2.json")); T = m53["pick"]["tune"]
    sys.path.insert(0, f"{SONGS}/p63"); import gen34 as G
    mel = [n["p"] for sec in ("verse", "refrain") for ln in T[sec] for n in ln]
    S.append(dict(folder="p63", title="Sung to Sleep (song 53)", tonic=2, mel=mel, chords=dedupe([chord_token(c, 2) for c in G.VERSE_CH + G.REFRAIN_CH])))
    return S
if __name__ == "__main__":
    D = json.load(gzip.open(SH.SRC)); seqs_m, seqs_c = [], []
    for c in D.values():
        mm, cc = SH.tokens(c)
        if len(mm) >= 12 and len(cc) >= 4: seqs_m.append(mm); seqs_c.append(cc)
    MM = SH.VOM(84).fit(seqs_m); CM = SH.VOM(108).fit(seqs_c)
    ref = json.load(open("/home/claude/shape/hooktheory_surprise.json"))
    R = {k: np.array([o[k] for o in ref]) for k in ("mel_ic_mean", "ch_ic_mean", "mel_h_mean", "ch_h_mean", "mel_cheung", "ch_cheung")}
    # event-level constants for the Cheung term: a 2,000-clip held-out check (fold-free approximation: clips scored by the full model)
    out = []
    for s in load_songs():
        mt = mel_tokens(s["mel"], s["tonic"]); ct = s["chords"]
        mi, mh = SH.score(MM, mt); ci, chh = SH.score(CM, ct)
        row = dict(title=s["title"], folder=s["folder"], n_mel=len(mt), n_ch=len(ct), mel_ic_mean=float(np.mean(mi)), ch_ic_mean=float(np.mean(ci)), mel_h_mean=float(np.mean(mh)), ch_h_mean=float(np.mean(chh)))
        for k in ("mel_ic_mean", "ch_ic_mean", "mel_h_mean", "ch_h_mean"): row[k + "_pct"] = float((R[k] < row[k]).mean() * 100)
        out.append(row)
    json.dump(dict(songs=out, reference=dict(n=len(ref), mel_ic_median=float(np.median(R["mel_ic_mean"])), ch_ic_median=float(np.median(R["ch_ic_mean"])))), open("/home/claude/shape/surprise_our_songs.json", "w"), indent=1)
    print("Hooktheory medians: melody %.2f bits, chords %.2f bits" % (np.median(R["mel_ic_mean"]), np.median(R["ch_ic_mean"])))
    for r in out: print("%-45s melody %.2f bits (%2.0fth pct), chords %.2f bits (%2.0fth pct), %d notes, %d chord changes" % (r["title"][:45], r["mel_ic_mean"], r["mel_ic_mean_pct"], r["ch_ic_mean"], r["ch_ic_mean_pct"], r["n_mel"], r["n_ch"]))
