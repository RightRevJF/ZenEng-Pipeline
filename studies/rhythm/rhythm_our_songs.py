"""The rhythm layer for our songs: descriptors and rhythm surprise (model trained on all Hooktheory clips), placed against the
Hooktheory distribution. Ticks are twelfths of a quarter; beats are quarters (song 52's 6/8 bar read as three quarters)."""
import json, pickle, gzip, sys
import numpy as np
sys.path.insert(0, "/home/claude/shape")
import surprise_hooktheory as SH, surprise_rhythm as RR
SONGS = "/home/claude/zeneng-pipeline/songs"
def clip(notes, bpb):
    mel = [dict(onset=n["on"] / 12, offset=(n["on"] + n["dur"]) / 12) for n in sorted(notes, key=lambda n: n["on"])]
    t0 = int(mel[0]["onset"] // bpb) * bpb
    for m in mel: m["onset"] -= t0; m["offset"] -= t0
    return {"annotations": {"meters": [{"beats_per_bar": bpb, "beat_unit": 4}], "melody": mel, "num_beats": int(np.ceil(mel[-1]["offset"]))}}
def songs():
    S = []
    for d in ("p42", "p45", "p48", "p49"):
        r = pickle.load(open(f"{SONGS}/{d}/song_record.pkl", "rb")); S.append((r["title"], clip(r["lead"], 4)))
    sh = json.load(open(f"{SONGS}/p62/melody_shaped.json")); notes = (sh.get("pick", sh) if isinstance(sh, dict) else {}).get("notes") or json.load(open(f"{SONGS}/p62/melody_final.json"))["pick"]["notes"]
    S.append(("The Room Next Door (song 52)", clip(notes, 3)))
    m = json.load(open(f"{SONGS}/p63/melody_final_v2.json"))["pick"]["tune"]
    S.append(("Sung to Sleep (song 53, verse)", clip([n for ln in m["verse"] for n in ln], 3)))
    S.append(("Sung to Sleep (song 53, refrain)", clip([dict(n, on=n["on"]) for ln in m["refrain"] for n in ln], 3)))
    return S
if __name__ == "__main__":
    D = json.load(gzip.open(SH.SRC)); seqs = [r["toks"] for r in (RR.analyse(c) for c in D.values()) if r]
    mdl = SH.VOM(256).fit(seqs); ref = json.load(open("/home/claude/shape/hooktheory_rhythm.json"))
    F = ["rhy_ic_mean", "sync_per_note", "rest_share", "phrase_mean", "phrase_on_downbeat", "density", "length_variety"]
    R = {f: np.array([r[f] for r in ref]) for f in F}; out = []
    for title, c in songs():
        a = RR.analyse(c)
        if not a: print(title, "skipped"); continue
        a["rhy_ic_mean"] = float(np.mean(SH.score(mdl, a["toks"])[0]))
        row = dict(title=title, **{f: a[f] for f in F}, **{f + "_pct": float((R[f] < a[f]).mean() * 100) for f in F}); out.append(row)
        print("%-34s rhythm surprise %.2f (%2.0f%%) sync %.2f (%2.0f%%) rests %.2f (%2.0f%%) phrase %.1f beats (%2.0f%%) downbeat starts %.2f (%2.0f%%) density %.2f (%2.0f%%) variety %.2f (%2.0f%%)" % (
            title[:34], *[x for f in F for x in (row[f], row[f + "_pct"])]))
    json.dump(dict(songs=out, medians={f: float(np.median(R[f])) for f in F}), open("/home/claude/shape/rhythm_our_songs.json", "w"), indent=1)
    print("medians", {f: round(float(np.median(R[f])), 2) for f in F})
