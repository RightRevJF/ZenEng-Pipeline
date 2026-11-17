"""Arrangement study, part 2b: the band by genre in the Lakh Pianoroll Dataset (LPD-5 cleansed: drums, piano, guitar, bass, strings,
24 steps a beat, 4/4). Per song, on a sixteenth grid (onsets are rising edges, so repeated strikes of one held pitch merge; a known
limit of the piano rolls): drums (commonest kick and snare bars, backbeat share, hat or ride subdivision, fills and crashes by place in
the 8-bar group), bass (notes a beat, the share on off-eighth sixteenths, by tempo), each chordal part (bars played, onsets a bar, notes
struck together, register, the commonest bar rhythm, share of strikes with a bass note), and parts playing by tenth of the song.
Writes lpd_band_rows.json (one row a song) for lpd_band_tables.py."""
import json, sys, collections, random, numpy as np, pypianoroll as P
from multiprocessing import Pool
GEN = json.load(open("lpd_genres.json"))
KICK = {35, 36}; SNARE = {37, 38, 39, 40}; HAT = {42, 44, 46}; RIDE = {51, 53, 59}; CRASH = {49, 52, 55, 57}; TOM = {41, 43, 45, 47, 48, 50}
def onsets(roll):
    a = roll > 0; on = a & ~np.vstack([np.zeros((1, a.shape[1]), bool), a[:-1]]); return on
def q16(t): return int(round(t / 6))
def song(f):
    try: m = P.load(f)
    except Exception: return None
    T = {t.name: t.pianoroll for t in m.tracks}; L = max((r.shape[0] for r in T.values()), default=0); nb = L // 96
    if nb < 16: return None
    tempo = float(np.median(m.tempo)) if len(m.tempo) else 120.0
    row = dict(f=f, genre=GEN[f]["genre"], tempo=tempo, bars=nb)
    def pad(r): return np.vstack([r, np.zeros((L - r.shape[0], 128), r.dtype)]) if 0 < r.shape[0] < L else r
    R = {k: pad(v) for k, v in T.items() if v.shape[0]}
    act = {k: np.array([R[k][b * 96:(b + 1) * 96].any() for b in range(nb)]) if k in R else np.zeros(nb, bool) for k in ("Drums", "Piano", "Guitar", "Bass", "Strings")}
    row["parts_by_tenth"] = [float(np.mean(sum(act[k][int(nb * i / 10):max(int(nb * i / 10) + 1, int(nb * (i + 1) / 10))] for k in act))) for i in range(10)]
    row["parts_max"] = int(max(sum(act[k][b] for k in act) for b in range(nb)))
    row["drums_enter_bar"] = int(np.argmax(act["Drums"])) if act["Drums"].any() else None
    if "Drums" in R and act["Drums"].mean() > 0.3:
        on = onsets(R["Drums"]); kb, sb, fills, crashes, hats16, hats8, bb = [], [], collections.Counter(), collections.Counter(), 0, 0, 0
        for b in range(nb):
            seg = on[b * 96:(b + 1) * 96]
            if not seg.any(): continue
            bb += 1
            k = tuple(sorted({q16(t) % 16 for t in np.nonzero(seg[:, list(KICK)].any(1))[0]})); s = tuple(sorted({q16(t) % 16 for t in np.nonzero(seg[:, list(SNARE)].any(1))[0]}))
            kb.append(k); sb.append(s)
            h = {q16(t) % 16 for t in np.nonzero(seg[:, list(HAT | RIDE)].any(1))[0]}
            if len(h) >= 12: hats16 += 1
            elif len(h) >= 6: hats8 += 1
            last = seg[72:]; tom = int(last[:, list(TOM)].any(1).sum()); sn = int(last[:, list(SNARE)].any(1).sum())
            if tom >= 2 or sn >= 3: fills[b % 8] += 1
            if seg[:6, list(CRASH)].any(): crashes[b % 8] += 1
        if bb >= 16:
            ck, cs = collections.Counter(kb).most_common(1)[0][0], collections.Counter(sb).most_common(1)[0][0]
            row["drums"] = dict(kick=list(ck), snare=list(cs), backbeat=float(np.mean([set(s) >= {4, 12} for s in sb])), hats16=hats16 / bb, hats8=hats8 / bb,
                                fill_rate=sum(fills.values()) / bb, fills_by_bar_of_8=[fills[i] for i in range(8)], crash_by_bar_of_8=[crashes[i] for i in range(8)],
                                distinct_kick_snare=len(set(zip(kb, sb))), commonest_share=collections.Counter(zip(kb, sb)).most_common(1)[0][1] / bb)
    bass_on = None
    if "Bass" in R and act["Bass"].mean() > 0.3:
        on = onsets(R["Bass"]); ts = np.nonzero(on.any(1))[0]; bass_on = set(q16(t) for t in ts)
        row["bass"] = dict(per_beat=len(ts) / (act["Bass"].sum() * 4), off8=float(np.mean([q16(t) % 2 == 1 for t in ts])) if len(ts) else 0.0,
                           median_pitch=float(np.median(np.nonzero(R["Bass"].any(0))[0])) if R["Bass"].any() else None)
    for k in ("Piano", "Guitar", "Strings"):
        if k not in R or act[k].mean() < 0.2: continue
        r = R[k]; on = onsets(r); ts = np.nonzero(on.any(1))[0]
        if len(ts) < 16: continue
        per = [int(on[t].sum()) for t in ts]; pitches = np.nonzero(on[ts])[1]
        bars_r = collections.Counter(tuple(sorted({q16(t) % 16 for t in ts if b * 96 <= t < (b + 1) * 96})) for b in range(nb) if act[k][b])
        row[k.lower()] = dict(bars_played=float(act[k].mean()), onsets_a_bar=len(ts) / act[k].sum(), together=float(np.mean(per)), low=float(np.percentile(pitches, 10)),
                              high=float(np.percentile(pitches, 90)), held=float((r[:nb * 96] > 0).any(1)[np.repeat(act[k], 96)].mean()),
                              commonest_rhythm=list(bars_r.most_common(1)[0][0]), with_bass=(float(np.mean([q16(t) in bass_on for t in ts])) if bass_on else None))
    return row
if __name__ == "__main__":
    rng = random.Random(56); files = sorted(GEN); byg = collections.defaultdict(list)
    for f in files: byg[GEN[f]["genre"]].append(f)
    pick = []
    for g, fs in byg.items(): rng.shuffle(fs); pick += fs[:1500]
    with Pool(2) as pool: rows = [r for r in pool.imap_unordered(song, pick, chunksize=20) if r]
    json.dump(rows, open("lpd_band_rows.json", "w"))
    print(len(pick), "picked;", len(rows), "read;", collections.Counter(r["genre"] for r in rows).most_common())
