"""Harmony study, part 2: what follows what, by section kind and mode, in 739 McGill Billboard songs (1958-1991), from
billboard_sections.json. Writes billboard_tables.json: per section kind and mode, the chord vocabulary (share of beats), first and last
chords, changes a bar, bars, distinct chords, the loop period, the bigram and trigram transitions between changes; the joins between
sections; the out-of-key chords; a section's return (does the second verse keep the first's chords); by decade."""
import json, collections, statistics as st
S = json.load(open("billboard_sections.json"))
KIND = {"verse": "verse", "chorus": "chorus", "refrain": "chorus", "bridge": "bridge", "pre-chorus": "pre", "prechorus": "pre", "intro": "intro", "outro": "outro",
        "fadeout": "outro", "coda": "outro"}
def beats(sec):
    out = []
    for b in sec["bars"]:
        n = len(b["rn"]); per = 4 // n if n in (1, 2, 4) else None
        if per is None: out += [x for x in b["rn"]]; continue
        for x in b["rn"]: out += [x] * per
    return out
def changes(bts):
    ch = []
    for x in bts:
        if x is None: continue
        if ch and ch[-1][0] == x: ch[-1][1] += 1
        else: ch.append([x, 1])
    return ch
def bar_tokens(sec): return [tuple(x for x in b["rn"] if x) for b in sec["bars"]]
def period(bt):
    n = len(bt)
    for p in (1, 2, 4, 8):
        if n >= 2 * p and sum(bt[i] == bt[i + p] for i in range(n - p)) >= 0.9 * (n - p): return p
    return None
IN = {"major": {"I", "ii", "iii", "IV", "V", "vi", "viio"}, "minor": {"i", "iio", "bIII", "iv", "v", "bVI", "bVII", "V"}}
R = collections.defaultdict(lambda: collections.defaultdict(list))
VOC = collections.defaultdict(collections.Counter); BIG = collections.defaultdict(collections.Counter); TRI = collections.defaultdict(collections.Counter)
FIRST = collections.defaultdict(collections.Counter); LAST = collections.defaultdict(collections.Counter); JOIN = collections.defaultdict(collections.Counter)
OUT = collections.defaultdict(collections.Counter); RET = collections.defaultdict(list); DEC = collections.defaultdict(lambda: collections.defaultdict(list))
for so in S:
    mode = so["mode"]; dec = (so["date"] or "0000")[:3] + "0s"; prev = None; firsts = {}
    for s in so["sections"]:
        k = KIND.get(s["label"]); bts = beats(s); ch = changes(bts)
        if k and ch:
            key = (k, mode); seq = [c for c, _ in ch]
            for x in bts:
                if x: VOC[key][x] += 1
            FIRST[key][seq[0]] += 1; LAST[key][seq[-1]] += 1
            for a, b in zip(seq, seq[1:]): BIG[key][(a, b)] += 1
            for a, b, c in zip(seq, seq[1:], seq[2:]): TRI[key][(a, b, c)] += 1
            nb = len(s["bars"]); bt = bar_tokens(s)
            R[key]["bars"].append(nb); R[key]["changes_a_bar"].append(len(ch) / max(1, nb)); R[key]["distinct"].append(len(set(seq)))
            R[key]["period"].append(period(bt) or 0); R[key]["tonic_share"].append(sum(1 for x in bts if x in ("I", "i")) / max(1, sum(1 for x in bts if x)))
            R[key]["out_share"].append(sum(1 for x in bts if x and x.rstrip("57sus+") not in IN[mode] and x not in IN[mode]) / max(1, sum(1 for x in bts if x)))
            for x in set(seq):
                if x not in IN[mode]: OUT[key][x] += 1
            DEC[(k, dec)]["changes_a_bar"].append(len(ch) / max(1, nb)); DEC[(k, dec)]["distinct"].append(len(set(seq)))
            if k in firsts: RET[k].append(bt == firsts[k])
            else: firsts[k] = bt
            if prev: JOIN[(prev[0], k)][(prev[1], seq[0])] += 1
            prev = (k, seq[-1])
        elif ch: prev = (s["label"], [c for c, _ in ch][-1])
def q(v): v = sorted(v); return [round(v[int(p * (len(v) - 1))], 3) for p in (0.25, 0.5, 0.75)] if v else None
def top(c, n=12): t = sum(c.values()); return [[(" ".join(k) if isinstance(k, tuple) else k), round(v / t, 3)] for k, v in c.most_common(n)]
out = {"about": "McGill Billboard (Burgoyne, Wild and Fujinaga 2011), 739 unique songs charting 1958-1991, raw salami_chords via ChoCo v1.0.0 (Zenodo 7706751). Roman numerals on the annotated tonic; lower case minor; 'o' diminished. Changes = consecutive distinct chords. Quartiles 25/50/75.",
       "by_section": {}}
for key in sorted(R):
    k, mode = key; r = R[key]; n = len(r["bars"])
    if n < 20: continue
    out["by_section"][f"{k} ({mode})"] = dict(n=n, bars=q(r["bars"]), changes_a_bar=q(r["changes_a_bar"]), distinct=q(r["distinct"]), tonic_share=q(r["tonic_share"]),
        out_of_key_share=q(r["out_share"]), loop_period={str(p): round(c / n, 3) for p, c in sorted(collections.Counter(r["period"]).items())},
        vocabulary=top(VOC[key], 14), first=top(FIRST[key], 8), last=top(LAST[key], 8), bigrams=top(BIG[key], 20), trigrams=top(TRI[key], 15),
        out_of_key_sections=[[c, round(v / n, 3)] for c, v in OUT[key].most_common(10)])
out["joins"] = {f"{a} -> {b}": dict(n=sum(c.values()), top=top(c, 8)) for (a, b), c in JOIN.items() if sum(c.values()) >= 40 and a in KIND.values()}
out["returns_keep_chords"] = {k: dict(n=len(v), share=round(sum(v) / len(v), 3)) for k, v in RET.items() if len(v) >= 20}
out["by_decade"] = {f"{k} {d}": dict(n=len(v["changes_a_bar"]), changes_a_bar=q(v["changes_a_bar"]), distinct=q(v["distinct"])) for (k, d), v in sorted(DEC.items()) if len(v["distinct"]) >= 30 and k in ("verse", "chorus")}
json.dump(out, open("billboard_tables.json", "w"), indent=1, ensure_ascii=False)
for k, v in out["by_section"].items():
    print(f"\n== {k} n={v['n']} bars {v['bars']} chg/bar {v['changes_a_bar']} distinct {v['distinct']} tonic {v['tonic_share']} out {v['out_of_key_share']} loop {v['loop_period']}")
    print("  vocab", v["vocabulary"][:10]); print("  first", v["first"][:5], " last", v["last"][:5]); print("  bigrams", v["bigrams"][:10]); print("  out-of-key", v["out_of_key_sections"][:6])
print("\njoins", {k: (v["n"], v["top"][:4]) for k, v in out["joins"].items()})
print("returns", out["returns_keep_chords"]); print("decades", {k: v["changes_a_bar"] for k, v in out["by_decade"].items()})
