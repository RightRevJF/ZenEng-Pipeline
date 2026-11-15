"""The kept tables for a compound-metre Luthier sketch, built from the Essen folk-song collection (music21's corpus): every tune in 6/8, and
every tune in 4/4 for comparison. Grid: twelfths of a quarter (an eighth = 6, a 6/8 bar = 36, a dotted-quarter beat = 18; a 4/4 bar = 48).
Writes tables/essen_meter_tables.json: bar rhythms by notes a bar, two-bar windows by notes, the interval and repeat shares, per-tune readings
(their quartiles), and the positions of onsets in the bar. Run once."""
import os, glob, json, collections, re, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
import music21
from music21 import converter, meter
P = os.path.dirname(music21.__file__) + "/corpus/essenFolksong"
def tunes(want):
    out = []
    for f in sorted(glob.glob(P + "/*.abc")):
        txt = open(f, errors="ignore").read()
        for blk in re.split(r"\n(?=X:)", txt):
            m = re.search(r"\nM:\s*([^\n]+)", "\n" + blk)
            if m and m.group(1).strip() == want: out.append(blk.strip())
    return out
def notes_of(abc, barlen):
    try: s = converter.parse(abc, format="abc")
    except Exception: return None
    p = s.parts[0] if hasattr(s, "parts") and s.parts else s
    ns = []
    for n in p.recurse().notes:
        if n.isChord: n = n.notes[-1]
        if n.tie is not None and n.tie.type in ("stop", "continue"):
            if ns: ns[-1][1] += int(round(float(n.quarterLength) * 12))
            continue
        on = int(round(float(n.getOffsetInHierarchy(p)) * 12)); d = int(round(float(n.quarterLength) * 12))
        ns.append([on, d, n.pitch.midi])
    if len(ns) < 8: return None
    ms = list(p.getElementsByClass("Measure")) or list(p.recurse().getElementsByClass("Measure"))
    pick = 0
    if ms:
        first = ms[0]; fl = int(round(float(first.duration.quarterLength) * 12))
        if 0 < fl < barlen: pick = barlen - fl                                      # a pickup bar: shift so bar lines fall on multiples of the bar
    for x in ns: x[0] += pick
    if any(x[0] % 3 for x in ns): return None                                       # the sixteenth grid only (no triplets in 6/8)
    return ns
def readings(ns, barlen, beat):
    p = [x[2] for x in ns]; iv = np.diff(p); mv = len(iv)
    bars = collections.defaultdict(list)
    for on, d, q in ns: bars[on // barlen].append(on % barlen)
    pats = [tuple(v) for v in bars.values()]
    run = best = 1
    for a, b in zip(p, p[1:]):
        run = run + 1 if a == b else 1; best = max(best, run)
    turns = sum(1 for a, b in zip(iv, iv[1:]) if a * b < 0)
    gaps = np.diff([x[0] for x in ns])
    return {"repeated notes": float(np.mean(iv == 0)), "moves by step": float(np.mean((abs(iv) >= 1) & (abs(iv) <= 2))), "moves by leap": float(np.mean(abs(iv) >= 5)),
            "turns of direction": turns / max(1, int(np.sum(iv != 0)) - 1), "range": int(max(p) - min(p)), "distinct pitches": len(set(p)),
            "longest run of one pitch": best, "distinct rhythms over bars": len(set(pats)) / len(pats), "notes a bar": len(ns) / len(pats),
            "onsets on the beat": float(np.mean([x[0] % beat == 0 for x in ns])), "onsets on the bar's first beat": float(np.mean([x[0] % barlen == 0 for x in ns])),
            "gaps of a sixteenth": float(np.mean(gaps == 3)), "gaps of an eighth": float(np.mean(gaps == 6)), "gaps of a quarter or more": float(np.mean(gaps >= 12))}
def build(want, barlen, beat, limit=None):
    T = tunes(want)[:limit]; R = []; BAR = collections.Counter(); WIN = collections.defaultdict(collections.Counter); IV = collections.Counter(); POS = collections.Counter()
    for abc in T:
        ns = notes_of(abc, barlen)
        if not ns: continue
        R.append(readings(ns, barlen, beat))
        bars = collections.defaultdict(list)
        for on, d, q in ns: bars[on // barlen].append((on % barlen, d, q))
        for b, v in bars.items():
            BAR[tuple(o for o, d, q in v)] += 1
            for o, d, q in v: POS[o] += 1
            if b + 1 in bars:                                                       # two-bar windows from a bar line: a sung line's slot
                w = tuple(o for o, d, q in v) + tuple(o + barlen for o, d, q in bars[b + 1])
                WIN[len(w)][w] += 1
        for a, b in zip(ns, ns[1:]): IV[int(max(-12, min(12, b[2] - a[2])))] += 1
    Q = {k: [float(np.percentile([r[k] for r in R], q)) for q in (25, 50, 75)] for k in R[0]}
    return dict(metre=want, bar=barlen, beat=beat, tunes=len(R), readings_quartiles=Q,
                bar_rhythms=[[list(k), v] for k, v in BAR.most_common()], two_bar_windows={str(n): [[list(k), v] for k, v in c.most_common(60)] for n, c in WIN.items()},
                intervals={str(k): v for k, v in sorted(IV.items())}, onset_positions={str(k): v for k, v in sorted(POS.items())})
if __name__ == "__main__":
    os.makedirs("/home/claude/p62/tables", exist_ok=True)
    out = {"6/8": build("6/8", 36, 18), "4/4": build("4/4", 48, 12, limit=924)}
    json.dump(out, open("/home/claude/p62/tables/essen_meter_tables.json", "w"))
    for k, v in out.items():
        print(k, v["tunes"], "tunes;", {a: [round(x, 3) for x in b] for a, b in v["readings_quartiles"].items()})
        print("  top bars", v["bar_rhythms"][:8])
