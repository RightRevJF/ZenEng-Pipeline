"""How a line sung again stands against its source's rhythm: on living builds, for each line made "again" or "818 again", sorted by how its syllable count stands against its source's notes, the share whose onsets (from the line's own start) are exactly the source's, the share that keep every source onset but the ones the count forces (one more: the source's onsets and one added; one fewer: the source's less one), and the rest. python3 studies/other_metres/count_again_rhythm.py LYRIC.json RECORD.song.json [BUILDS] -> prints JSON. A count; no note is changed."""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE]
import count_after_251 as CA
if __name__ == "__main__":
    L = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2])); E, sp = CA.engine(L, R); seen = {}; inner = E.again
    def wrapped(rng, src, src_st0, sy, U, sec, i, tmin, slot): seen[(sec, i)] = ([t for t, _ in src], len(sy) - len(src)); return inner(rng, src, src_st0, sy, U, sec, i, tmin, slot)
    E.again = wrapped; rng = random.Random(L.get("seed", 1)); G = collections.defaultdict(collections.Counter); n = 0
    for _ in range(int(sys.argv[3]) if len(sys.argv) > 3 else 400):
        seen.clear(); c, err = E.build(rng)
        if err or E.gates(c): continue
        n += 1; by = collections.defaultdict(list)
        for x in c["notes"]: by[(x["sec"], x["line"])].append(x["on"])
        for k, ons in by.items():
            made = E._made.get(k)
            if made not in ("again", "818 again") or k not in seen: continue
            so, d = seen[k]; U = E.line_start(*k); o = [t - U for t in sorted(ons)]; a, b = set(so), set(o)
            how = "exactly the source's rhythm" if o == so else "every source onset kept, only the count's notes added" if (d > 0 and a <= b and len(b - a) == d) else "the source's onsets less only the count's notes" if (d < 0 and b <= a and len(a - b) == -d) else "the same onsets moved together (a shift)" if (len(o) == len(so) and len(set(x - y for x, y in zip(o, so))) == 1) else "other"
            sort = "the same count" if d == 0 else "one more syllable" if d == 1 else "one fewer" if d == -1 else "two or three apart" if abs(d) <= 3 else "more than three apart"
            for g in ("all", made + ": " + sort, "both: " + sort): G[g][how] += 1
    print(json.dumps(dict(living_builds=n, rows={g: dict(lines=sum(v.values()), **{h: round(x / sum(v.values()), 3) for h, x in v.most_common()}) for g, v in sorted(G.items())}), indent=1))
