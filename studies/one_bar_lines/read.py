"""PREDICTION.md: lines of 6 to 8 syllables sung in one bar, kept against the builds.  python3 read.py kept | N=600 python3 read.py builds DIR"""
import os, sys, json, random, collections, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np
BAR = 48; BEAT = 12
def line_figs(ons, lens, tiers):
    """ons: onsets (twelfths of a quarter), lens: note lengths, tiers: 2 = weighty"""
    w = [k for k, t in enumerate(tiers) if t == 2]; r = [k for k, t in enumerate(tiers) if t != 2]
    o = {"a spread of lengths": float(np.std(lens) / np.mean(lens)), "start": "on the first beat" if ons[0] % BAR == 0 else "before it" if ons[0] % BAR > BAR / 2 else "after it", "n_weighty": len(w)}
    if w and r: o["c weighty length over the rest"] = float(np.mean([lens[k] for k in w]) / np.mean([lens[k] for k in r]))
    if w: o["b weighty on a beat"] = sum(ons[k] % BEAT == 0 for k in w); o["d weighty a sixteenth or less"] = sum(lens[k] <= 3 for k in w)
    return o
def summary(rows):
    q = lambda v: [round(float(x), 3) for x in np.percentile(v, (25, 50, 75))]; nw = sum(x["n_weighty"] for x in rows)
    return dict(lines=len(rows), a_spread_of_lengths=q([x["a spread of lengths"] for x in rows]), c_weighty_length_over_the_rest=q([x["c weighty length over the rest"] for x in rows if "c weighty length over the rest" in x]),
                b_weighty_on_a_beat=round(sum(x.get("b weighty on a beat", 0) for x in rows) / max(1, nw), 3), d_weighty_a_sixteenth_or_less=round(sum(x.get("d weighty a sixteenth or less", 0) for x in rows) / max(1, nw), 3), start={k: round(v / len(rows), 3) for k, v in collections.Counter(x["start"] for x in rows).items()}, commonest_length_patterns=[(list(k), v) for k, v in collections.Counter(tuple(x["lens"]) for x in rows).most_common(5)])
if __name__ != "__main__": pass
elif sys.argv[1] == "kept":
    import kept_corpus as KC, make_kept_word_weight as MW
    out = {}; R = collections.defaultdict(list)
    for k in KC.kept_songs():
        tr = MW.tiers(k["words"]); tr = tr[0] if isinstance(tr, tuple) else tr; idx = collections.OrderedDict()
        for i, (l, s) in enumerate(zip(k["lines"], k["sec"])): idx.setdefault((str(s), l, sum(1 for j in range(i) if k["lines"][j] > l)), []).append(i)
        cur = None; groups = []
        for i, (l, s) in enumerate(zip(k["lines"], k["sec"])):
            if (str(s), l) != cur: cur = (str(s), l); groups.append([])
            groups[-1].append(i)
        for g in groups:
            if not 6 <= len(g) <= 8: continue
            ons = [int(k["t"][i]) for i in g]
            if ons[-1] - ons[0] >= BAR or any(b <= a for a, b in zip(ons, ons[1:])): continue
            lens = [b - a for a, b in zip(ons, ons[1:])] + [int(k["dur"][g[-1]])]; f = line_figs(ons, lens, [tr[i] for i in g]); f["lens"] = lens
            for key in ("all", str(len(g))) + (("verse",) if str(k["sec"][g[0]]).lstrip(">") == "verse" else ()): R[key].append(f)
    out = {key: summary(v) for key, v in R.items()}; json.dump(out, open(os.path.join(HERE, "kept.json"), "w"), indent=1); print(json.dumps(out, indent=1))
else:
    import song_from_lyric as SL, metre_engine as M, word_weight as W
    out = {}
    for n, p in (("49", "songs/p59/lyric49"), ("54", "songs/p64/lyric54")):
        L = json.load(open(os.path.join(ROOT, p + ".json"))); spec = json.load(open(os.path.join(sys.argv[2], f"lyric{n}.song.json")))["spec"]; E = M.Engine(spec)
        E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
        one = [(s, i) for (s, i) in E.KEYS if E.SLOTS[s][i] == 1 and 6 <= len(E.LINES[s][i]) <= 8 and E.KIND.get(s) == "Verse"]; rng = random.Random(L.get("seed", 1)); rows = []; stats = collections.Counter()
        for _ in range(int(os.environ.get("N", "600"))):
            c, err = E.build(rng)
            if err or E.gates(c): continue
            by = collections.defaultdict(list)
            for x in c["notes"]: by[(x["sec"], x["line"])].append(x)
            for k in one:
                v = sorted(by[k], key=lambda x: x["on"]); ons = [x["on"] for x in v]; lens = [b - a for a, b in zip(ons, ons[1:])] + [v[-1]["dur"]]; f = line_figs(ons, lens, W.tier(E.LINES[k[0]][k[1]])); f["lens"] = lens; rows.append(f)
        out[n] = dict(one_bar_lines=[f"{s}:{i + 1}" for s, i in one], verse_closer=spec.get("verse_closer"), how={f"{s}:{i + 1}": E.HOW.get((s, i), ["fresh"])[0] for s, i in one}, **summary(rows), stats={k: v for k, v in E.stats.items() if k[:3] in ("653", "760", "870")}); print(n, json.dumps(out[n]), flush=True)
    json.dump(out, open(os.path.join(HERE, "builds.json"), "w"), indent=1)
