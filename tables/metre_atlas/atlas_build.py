"""Metre atlas for Luthier (749.4): kept tables per metre from music21's corpora. Sung tunes (the Essen folk-song collection) and
instrumental tunes (the Irish and Scottish dance collections: Ryan's Mammoth, O'Neill's 1850, Aird's Airs, miscFolk) are kept apart, since a
sung line and a fiddle line differ in density. Grid: twelfths of a quarter. Per metre: the bar's length, its beats, and the felt beat.

Per metre and source the tables hold: per-tune readings and their quartiles (the 14 the sketches use, plus readings in beat units, so
metres that differ only in notation can be compared: notes a beat, gaps of half a beat, of a third of a beat, of a beat or more), bar
rhythms by frequency, two-bar windows by note count, the interval shares, and onset weights by position in the bar (the metric profile).
Usage: python3 atlas_build.py METRE SOURCE [LIMIT]   (SOURCE: sung | instrumental). Writes tables/<metre>_<source>.json."""
import os, glob, json, collections, re, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
import music21
from music21 import converter
P = os.path.dirname(music21.__file__) + "/corpus"
# bar length (twelfths of a quarter), beats (felt), the beat's length, and the felt grouping
METRES = {
    "2/4": (24, [0, 12], 12, "simple duple"), "3/4": (36, [0, 12, 24], 12, "simple triple"), "4/4": (48, [0, 12, 24, 36], 12, "simple quadruple"),
    "2/2": (48, [0, 24], 24, "simple duple, half-note beat"), "3/2": (72, [0, 24, 48], 24, "simple triple, half-note beat"), "4/2": (96, [0, 24, 48, 72], 24, "simple quadruple, half-note beat"),
    "3/8": (18, [0], 18, "felt in one (a dotted-quarter beat), three eighths"), "6/8": (36, [0, 18], 18, "compound duple"), "9/8": (54, [0, 18, 36], 18, "compound triple"),
    "12/8": (72, [0, 18, 36, 54], 18, "compound quadruple"), "6/4": (72, [0, 36], 36, "compound duple, dotted-half beat"),
    "5/8": (30, [0, 12], None, "additive"), "5/4": (60, [0, 12, 24, 36, 48], 12, "simple quintuple"), "7/8": (42, [0, 12, 24], None, "additive"),
}
ALIAS = {"C": "4/4", "C|": "2/2"}
SOURCES = {"sung": ["essenFolksong"], "instrumental": ["ryansMammoth", "oneills1850", "airdsAirs", "miscFolk"]}
def tunes(want, source):
    out = []
    for d in SOURCES[source]:
        for f in sorted(glob.glob(P + f"/{d}/**/*.abc", recursive=True) + glob.glob(P + f"/{d}/*.abc")):
            txt = open(f, errors="ignore").read()
            for blk in re.split(r"\n(?=X:)", txt):
                m = re.search(r"\nM:\s*([^\n%]+)", "\n" + blk)
                if not m: continue
                mm = m.group(1).strip(); mm = ALIAS.get(mm, mm)
                if mm == want: out.append(blk.strip())
    seen = set(); uniq = []
    for b in out:
        k = re.sub(r"\s+", "", b.split("K:", 1)[-1])[:200]
        if k not in seen: seen.add(k); uniq.append(b)
    return uniq
def notes_of(abc, barlen):
    try: s = converter.parse(abc, format="abc")
    except Exception: return None
    p = s.parts[0] if hasattr(s, "parts") and s.parts else s
    ns = []
    try: fl = p.flatten()
    except Exception: return None
    for n in fl.notes:
        if n.isChord: n = n.notes[-1]
        if n.tie is not None and n.tie.type in ("stop", "continue"):
            if ns: ns[-1][1] += int(round(float(n.quarterLength) * 12))
            continue
        on = int(round(float(n.offset) * 12)); d = int(round(float(n.quarterLength) * 12))
        ns.append([on, d, n.pitch.midi])
    if len(ns) < 8: return None
    ms = list(p.getElementsByClass("Measure")) or list(p.recurse().getElementsByClass("Measure"))
    pick = 0
    if ms:
        fl = int(round(float(ms[0].duration.quarterLength) * 12))
        if 0 < fl < barlen: pick = barlen - fl
    for x in ns: x[0] += pick
    if any(x[0] % 3 for x in ns): return None
    return ns
def readings(ns, barlen, beats, beat):
    p = [x[2] for x in ns]; iv = np.diff(p)
    bars = collections.defaultdict(list)
    for on, d, q in ns: bars[on // barlen].append(on % barlen)
    pats = [tuple(v) for v in bars.values()]
    run = best = 1
    for a, b in zip(p, p[1:]): run = run + 1 if a == b else 1; best = max(best, run)
    gaps = np.diff([x[0] for x in ns]); bset = set(beats)
    r = {"repeated notes": float(np.mean(iv == 0)), "moves by step": float(np.mean((abs(iv) >= 1) & (abs(iv) <= 2))), "moves by leap": float(np.mean(abs(iv) >= 5)),
         "turns of direction": sum(1 for a, b in zip(iv, iv[1:]) if a * b < 0) / max(1, int(np.sum(iv != 0)) - 1), "range": int(max(p) - min(p)), "distinct pitches": len(set(p)),
         "longest run of one pitch": best, "distinct rhythms over bars": len(set(pats)) / len(pats), "notes a bar": len(ns) / len(pats),
         "onsets on the beat": float(np.mean([x[0] % barlen in bset for x in ns])), "onsets on the bar's first beat": float(np.mean([x[0] % barlen == 0 for x in ns])),
         "gaps of a sixteenth": float(np.mean(gaps == 3)), "gaps of an eighth": float(np.mean(gaps == 6)), "gaps of a quarter or more": float(np.mean(gaps >= 12))}
    if beat:
        r.update({"notes a beat": len(ns) / (len(pats) * len(beats)), "gaps of half a beat": float(np.mean(gaps * 2 == beat)), "gaps of a third of a beat": float(np.mean(gaps * 3 == beat)),
                  "gaps of a beat or more": float(np.mean(gaps >= beat)), "gaps under a third of a beat": float(np.mean(gaps * 3 < beat))})
    return r
def build(want, source, limit=None):
    barlen, beats, beat, kind = METRES[want]
    T = tunes(want, source); n_found = len(T); T = T[:limit] if limit else T
    R = []; BAR = collections.Counter(); WIN = collections.defaultdict(collections.Counter); IV = collections.Counter(); POS = collections.Counter(); DUR = collections.Counter()
    for abc in T:
        try: ns = notes_of(abc, barlen)
        except Exception: ns = None
        if not ns: continue
        R.append(readings(ns, barlen, beats, beat))
        bars = collections.defaultdict(list)
        for on, d, q in ns: bars[on // barlen].append((on % barlen, d, q)); DUR[d] += 1
        for b, v in bars.items():
            BAR[tuple(o for o, d, q in v)] += 1
            for o, d, q in v: POS[o] += 1
            if b + 1 in bars:
                w = tuple(o for o, d, q in v) + tuple(o + barlen for o, d, q in bars[b + 1]); WIN[len(w)][w] += 1
        for a, b in zip(ns, ns[1:]): IV[int(max(-12, min(12, b[2] - a[2])))] += 1
    if not R: return dict(metre=want, source=source, tunes=0, found=n_found)
    Q = {k: [float(np.percentile([r[k] for r in R], q)) for q in (25, 50, 75)] for k in R[0]}
    tot = sum(POS.values())
    return dict(metre=want, source=source, kind=kind, bar=barlen, beats=beats, beat=beat, found=n_found, tunes=len(R), readings_quartiles=Q,
                bar_rhythms=[[list(k), v] for k, v in BAR.most_common(40)], bars_total=sum(BAR.values()),
                two_bar_windows={str(n): [[list(k), v] for k, v in c.most_common(40)] for n, c in WIN.items()},
                intervals={str(k): v for k, v in sorted(IV.items())}, onset_weights={str(k): round(v / tot, 4) for k, v in sorted(POS.items())},
                durations={str(k): v for k, v in DUR.most_common(20)})
if __name__ == "__main__":
    want, source = sys.argv[1], sys.argv[2]; limit = int(sys.argv[3]) if len(sys.argv) > 3 else None
    out = build(want, source, limit)
    os.makedirs("/home/claude/atlas/tables", exist_ok=True)
    json.dump(out, open(f"/home/claude/atlas/tables/{want.replace('/', '-')}_{source}.json", "w"))
    print(want, source, "found", out.get("found"), "tunes", out.get("tunes"))
