"""Run 07: the notes side of the Lakh songs (no outcome is read here).

Builds, from the Lakh Pianoroll Dataset's LPD-5 cleansed set (Dong, Hsiao, Yang & Yang 2018; derived from Raffel's Lakh MIDI
Dataset; Zenodo record 5646574, CC BY 4.0), for every one of its 21,425 songs:
  - bar chroma: for each bar (96 time steps = 4 beats at the set's 24 steps per beat, counted from step 0: the cleansed set is
    4/4 only and starts at time 0, and its downbeat vector marks only step 0), a 12-vector, L1-normalised (a silent bar stays zero), = sum over the four pitched tracks (piano, guitar, bass,
    strings; drums left out) of velocity at each time step, folded to pitch class;
  - half-bar chords: each bar split into two equal halves; each half's chroma (L1-normalised) is scored against the 24 major and
    minor triad templates (sum of the chroma on the template's three pitch classes); the best template wins, ties to the lower
    index (roots C..B major = 0..11, then minor = 12..23); a half with no pitched note is "N" and is dropped;
  - tokens: the chord sequence with runs of the same chord collapsed (the pack's convention), as ints 0..23.
Names come from the Gold-Caps LMD-matched metadata (Jonason, Casini & Sturm 2023, Zenodo 10178563, CC BY 4.0), which repeats the
Million Song Dataset's artist_name, title, year, song_hotttnesss for each MSD track id. Billboard Hot 100 flags come from the Hit
Song Prediction dataset (Zangerle et al. 2019, Zenodo 3258042): msd_bb_matches.csv.

Writes (outside the repo): $LAKH/notes.json (one record per song) and $LAKH/chroma.npz (bar chroma, float16, keyed by track id).
Usage: python3 -I lakh_notes.py <dl_dir>
"""
import os, sys, json, csv, glob, numpy as np
from multiprocessing import Pool

DL = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/dl"
OUT = os.path.join(DL, "lakh"); os.makedirs(OUT, exist_ok=True)
TEMPL = np.zeros((24, 12))
for r in range(12):
    for s in (0, 4, 7): TEMPL[r, (r + s) % 12] = 1
    for s in (0, 3, 7): TEMPL[12 + r, (r + s) % 12] = 1


def load_roll(path):
    """sum of velocities over the four pitched tracks (1..4), as a (T, 12) chroma-per-step array, and the downbeat vector."""
    z = np.load(path, allow_pickle=False)
    db = z["downbeat"]; T = len(db); C = np.zeros((T, 12), np.float32)
    for k in (1, 2, 3, 4):
        shp = z[f"pianoroll_{k}_csc_shape"]
        if shp[0] == 0: continue
        ind, ptr, dat = z[f"pianoroll_{k}_csc_indices"], z[f"pianoroll_{k}_csc_indptr"], z[f"pianoroll_{k}_csc_data"].astype(np.float32)
        for p in range(128):                      # csc: column = pitch
            a, b = ptr[p], ptr[p + 1]
            if b > a: np.add.at(C[:, p % 12], ind[a:b], dat[a:b])
    return C, db


def song(path):
    tid = path.split(os.sep)[-2]
    C, db = load_roll(path)
    starts = list(range(0, len(db), 96)) + [len(db)]
    bars, chords = [], []
    for a, b in zip(starts, starts[1:]):
        if b <= a: continue
        v = C[a:b].sum(0); bars.append(v / v.sum() if v.sum() > 0 else v)
        m = (a + b) // 2
        for x, y in ((a, m), (m, b)):
            v = C[x:y].sum(0)
            if v.sum() <= 0: continue
            chords.append(int(np.argmax(TEMPL @ (v / v.sum()))))
    toks = [c for i, c in enumerate(chords) if i == 0 or c != chords[i - 1]]
    return tid, np.array(bars, np.float16), toks, len(chords)


def main():
    files = sorted(glob.glob(os.path.join(DL, "lpd", "x", "lpd_5", "lpd_5_cleansed", "*", "*", "*", "*", "*.npz")))
    assert len(files) == 21425, len(files)
    G = {x["track_id"]: x for x in json.load(open(os.path.join(DL, "gold", "g.json")))}
    BB = {r["msd_id"]: r for r in csv.DictReader(open(os.path.join(DL, "msd", "msd_bb_matches.csv")))}
    with Pool(2) as P: res = P.map(song, files, chunksize=50)
    notes, chroma = [], {}
    for f, (tid, bars, toks, nhalf) in zip(files, res):
        g = G[tid]; bb = BB.get(tid)
        notes.append(dict(tid=tid, md5=os.path.basename(f)[:-4], artist=g["artist_name"], title=g["title"],
                          year=int(g["year"] or 0), hot=(None if g["song_hotttnesss"] != g["song_hotttnesss"] else g["song_hotttnesss"]),
                          bb=bool(bb), bb_peak=(int(bb["peak"]) if bb else None), bb_weeks=(int(bb["weeks"]) if bb else None),
                          n_bars=int(len(bars)), n_half=nhalf, toks=toks))
        chroma[tid] = bars
    json.dump(notes, open(os.path.join(OUT, "notes.json"), "w"))
    np.savez_compressed(os.path.join(OUT, "chroma.npz"), **chroma)
    print(len(notes), "songs;", sum(1 for n in notes if len(n["toks"]) >= 4), "with 4+ chord runs")


if __name__ == "__main__":
    main()
