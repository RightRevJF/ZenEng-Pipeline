"""Tables from SymbTr (Turkish makam music, github.com/MTG/SymbTr, CC BY-NC-SA 4.0: non-commercial, share-alike) for additive metres.
Per usul (rhythmic cycle) and written metre: pieces, vocal pieces (notes carrying lyric syllables), the readings of atlas_build (on the
vocal line), onset weights by eighth-note position in the bar, and the beat grouping inferred from them: every chain of 2- and 3-unit groups that
fills the bar is scored by how far the onset weight at its group starts exceeds the weight inside its groups; the best is kept (a check against the usul tables of the literature, which the files lack).
Pitch: 53-comma index converted to the nearest equal-tempered semitone (Koma53 * 12 / 53). Writes tables/symbtr_usul.json."""
import glob, os, collections, json, re
import numpy as np
import atlas_build as AB
P = "/home/claude/atlas/src/SymbTr/txt"
LICENCE = "CC BY-NC-SA 4.0 (SymbTr): non-commercial use, share-alike"
LIT = {"aksak": (9, "2+2+2+3"), "türk aksağı": (5, "2+3"), "turk aksagi": (5, "2+3"), "devr-i hindi": (7, "3+2+2"), "devr-i turan": (7, "2+2+3"), "curcuna": (10, "3+2+2+3"),
       "aksak semai": (10, "3+2+2+3")}
def norm(s): return s.strip().lower().replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("ö", "o").replace("ç", "c").replace("â", "a").replace("î", "i")
def read(path):
    rows = [l.rstrip("\n").split("\t") for l in open(path, encoding="utf-8", errors="ignore")][1:]
    usul = None; num = den = None; notes = []; prev = 0.0; lyr = 0
    for r in rows:
        if len(r) < 13: continue
        kod, pay, payda, soz, off = r[1], r[6], r[7], r[11], r[12]
        try: off = float(off)
        except ValueError: continue
        if kod == "51":
            if usul is None: usul, num, den = soz, int(pay), int(payda)
            prev = off; continue
        if kod != "9": prev = off if kod not in ("53", "54", "55") else prev; continue
        try: k53 = int(r[4])
        except ValueError: k53 = -1
        dur_bar = off - prev
        if r[2] != "Es" and k53 >= 0:
            on = prev
            syl = soz if (soz not in (".", "") and not soz.isupper()) else ""
            if syl: lyr += 1
            notes.append((on, dur_bar, int(round(k53 * 12 / 53)), syl))
        prev = off
    return usul, num, den, notes, lyr
if __name__ == "__main__":
    G = collections.defaultdict(list)
    for f in sorted(glob.glob(P + "/*.txt")):
        u, n, d, ns, lyr = read(f)
        if not u or not n or len(ns) < 8: continue
        G[(norm(u), n, d)].append((f, ns, lyr))
    out = {"source": "SymbTr v2.4.3 (github.com/MTG/SymbTr)", "licence": LICENCE, "usul": {}}
    for (u, n, d), pieces in sorted(G.items(), key=lambda x: -len(x[1])):
        if len(pieces) < 8: continue
        barlen = int(n * 48 / d); unit = 48 // d                   # an eighth (or the denominator's note) in twelfths
        vocal = [p for p in pieces if p[2] >= 10]
        R = []; POS = collections.Counter(); BAR = collections.Counter()
        for f, ns, lyr in (vocal or pieces):
            ev = [[int(round(on * barlen)), max(1, int(round(du * barlen))), p] for on, du, p, s in ns]
            ev = [e for e in ev if e[0] >= 0]
            if len(ev) < 8: continue
            beats = list(range(0, barlen, unit))
            R.append(AB.readings(ev, barlen, beats, None))
            bars = collections.defaultdict(list)
            for on, du, p in ev: bars[on // barlen].append(on % barlen); POS[(on % barlen) // unit * unit if (on % barlen) % unit == 0 else -1] += 1
            for v in bars.values(): BAR[tuple(v)] += 1
        if not R: continue
        tot = sum(v for k, v in POS.items() if k >= 0)
        w = [POS.get(i * unit, 0) / tot for i in range(n)]
        def comps(k):
            if k == 0: return [[]]
            return [[g] + c for g in (2, 3) if g <= k for c in comps(k - g)]
        scored = []
        if d == 8 or n in (5, 7, 9, 10, 11, 13) and n <= 15:
            for c in comps(n):
                st = list(np.cumsum([0] + c[:-1]))
                inside = [i for i in range(n) if i not in st]
                if len(c) < 2 or not inside: continue
                scored.append((float(np.mean([w[i] for i in st[1:]]) - np.mean([w[i] for i in inside])), "+".join(map(str, c))))
        scored.sort(reverse=True)
        groups = scored[0][1].split("+") if scored else []
        Q = {k: [float(np.percentile([r[k] for r in R], q)) for q in (25, 50, 75)] for k in R[0]}
        out["usul"][f"{u} {n}/{d}"] = dict(usul=u, metre=f"{n}/{d}", pieces=len(pieces), vocal_pieces=len(vocal), tunes_read=len(R),
            onset_weight_by_unit={str(i + 1): round(x, 4) for i, x in enumerate(w)}, off_unit_onsets=round(POS.get(-1, 0) / (tot + POS.get(-1, 0)), 4),
            inferred_grouping="+".join(map(str, groups)) if groups else None, grouping_scores=[[g, round(x, 4)] for x, g in scored[:4]], literature_grouping=LIT.get(u, (None, None))[1] if LIT.get(u, (None,))[0] == n else None,
            readings_quartiles=Q, bar_rhythms=[[list(k), v] for k, v in BAR.most_common(12)], bars_total=sum(BAR.values()))
        o = out["usul"][f"{u} {n}/{d}"]
        if o["grouping_scores"]: print(f"{u} {n}/{d}: pieces {len(pieces)}, vocal {len(vocal)}; best {o['grouping_scores'][:3]}; literature {o['literature_grouping']}")
    json.dump(out, open("/home/claude/atlas/tables/symbtr_usul.json", "w"))
