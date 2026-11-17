"""Songs 52 to 56 on the hook features, each section measured as a Hooktheory clip is (hooks_hooktheory.py) and placed as a
percentile of the Hooktheory clips of the same kind (chorus against choruses, verse against verses). Conventionality and the
uniqueness point are read against all Hooktheory songs; information content under a model trained on all clips."""
import json, pickle, sys, math, collections, gzip
import numpy as np
sys.path.insert(0, "/home/claude/zeneng-pipeline/studies/hooks"); sys.path.insert(0, "/home/claude/shape")
import hooks_hooktheory as HH
import surprise_hooktheory as SH
from surprise_our_songs import mel_tokens
SONGS = "/home/claude/zeneng-pipeline/songs/"
def kind(sec):
    s = sec.lower()
    return "chorus" if ("chorus" in s or "refrain" in s) else "verse" if "verse" in s else "bridge" if "bridge" in s else "other"
def sections_engine(folder, tpq):
    r = pickle.load(open(SONGS + folder + "/song_record.pkl", "rb")); out = collections.defaultdict(list)
    for e in sorted(r["lead"], key=lambda e: e["on"]): out[e["sec"]].append((e["on"] / tpq, (e["on"] + e["dur"]) / tpq, e["midi"]))
    return r["title"], out
def load():
    S = []
    m = json.load(open(SONGS + "p62/melody_varied.json"))["pick"]["notes"]; sec = collections.defaultdict(list)
    for n in sorted(m, key=lambda n: n["on"]): sec[n["sec"]].append((n["on"] / 12, (n["on"] + n["dur"]) / 12, n["p"]))
    S.append(dict(song="52 The Room Next Door", tonic=2, secs=sec))
    r = json.load(open(SONGS + "p63/song_record.json")); o = r["offsets"]; sec = collections.defaultdict(list)
    for n in sorted(r["voices"]["S"], key=lambda n: n["on"]):
        lab = "Verse A" if o["A_verse"] <= n["on"] < o["A_refrain"] else "Refrain A" if o["A_refrain"] <= n["on"] < o["B_verse"] else "Verse B" if o["B_verse"] <= n["on"] < o["B_refrain"] else "Refrain B" if n["on"] >= o["B_refrain"] else None
        if lab: sec[lab].append((n["on"] / 12, (n["on"] + n["dur"]) / 12, n["p"]))
    S.append(dict(song="53 Sung to Sleep", tonic=2, secs=sec))
    for folder, num, tonic, tpq in (("p64", 54, 7, 12), ("p65", 55, 9, 12), ("p66", 56, 4, 24)):
        t, sec = sections_engine(folder, tpq); S.append(dict(song=f"{num} {t}", tonic=tonic, secs=sec))
    return S
def main():
    clips = HH.load(); songs = sorted({c["song"] for c in clips}); sid = {s: i for i, s in enumerate(songs)}; NS = len(songs)
    for c in clips: c["tr"], c["tp"] = HH.tokens(c["notes"]); c["sid"] = sid[c["song"]]
    by_song = collections.defaultdict(set)
    for c in clips:
        for n in (3, 4, 5): by_song[c["sid"]].update(HH.ngrams(c["tr"], n))
    df = collections.Counter()
    for cells in by_song.values(): df.update(cells)
    MM = SH.VOM(84).fit([SH.tokens(c["raw"])[0] for c in clips])
    S = load(); rows = []
    for s in S:
        for lab, notes in s["secs"].items():
            if len(notes) < 12 or kind(lab) == "other": continue
            tr, tp = HH.tokens(notes); ps = [n[2] for n in notes]; nb = notes[-1][1] - notes[0][0]
            cells = [g for n in (3, 4, 5) for g in HH.ngrams(tr, n)]
            conv = float(np.mean([math.log2(max(df[g], 0.5) / NS) for g in cells]))
            ic, h = SH.score(MM, mel_tokens(ps, s["tonic"]))
            tc, tpos, tcov = HH.top_cell(tr, len(ps))
            rows.append(dict(song=s["song"], section=lab, kind=kind(lab), n=len(ps), density=len(ps) / nb, range=max(ps) - min(ps), mean_pitch=float(np.mean(ps)),
                             i_entropy=HH.entropy(tp), recurrence=HH.recurrence(tr), convention=conv, ic_mean=float(np.mean(ic)), top_cell_n=tc, top_cell_cover=tcov, tr=tr, tp=tp))
    # uniqueness point against the whole corpus
    for field, key in (("tr", "up_rhythm"), ("tp", "up_pitch")):
        for r in rows: r[key] = None
        for n in range(2, 17):
            present = set()
            for c in clips:
                for g in HH.ngrams(c[field], n): present.add(g)
            for r in rows:
                if r[key] is None and len(r[field]) >= n and tuple(r[field][:n]) not in present: r[key] = n + 1
    D = json.load(gzip.open("/home/claude/zeneng-pipeline/studies/hooks/hooks_clips.json.gz", "rt"))
    ref = {k: [x for x in D if x["section"] == k] for k in ("chorus", "verse", "bridge")}
    out = []
    for r in rows:
        R = ref[r["kind"]]; row = {k: v for k, v in r.items() if k not in ("tr", "tp")}
        for f in ("density", "range", "mean_pitch", "i_entropy", "recurrence", "convention", "ic_mean", "top_cell_cover", "up_rhythm"):
            v = np.array([x[f] for x in R if x[f] is not None], float)
            if r[f] is not None: row[f + "_pct"] = round(float(((v < r[f]).mean() + 0.5 * (v == r[f]).mean()) * 100), 1)
        out.append(row)
    json.dump(out, open("/home/claude/zeneng-pipeline/studies/hooks/hooks_our_songs.json", "w"), indent=1)
    for r in out:
        print("%-28s %-10s n%3d conv %5.1f pct  ic %5.1f pct  i_ent %5.1f pct  recur %5.1f pct  cell cover %5.1f pct  up %s  pitch %+.0f" % (
            r["song"][:28], r["section"], r["n"], r["convention_pct"], r["ic_mean_pct"], r["i_entropy_pct"], r["recurrence_pct"], r["top_cell_cover_pct"], r["up_rhythm"], r["mean_pitch"]))
if __name__ == "__main__": main()
