"""Line ends of Luthier records against tables/kept_line_ends.json: the last syllable's held length by weight (with its melisma), the rest to the next line,
lines run on (under a beat of rest), and on a word's weak syllable, how often it outlasts the stressed one. python3 studies/kept_checks/line_ends_engine.py rec.song.json ..."""
import sys, json, collections, numpy as np
sys.path.insert(0, "lib/luthier"); import word_weight as WW
for f in sys.argv[1:]:
    R = json.load(open(f)); L = collections.OrderedDict()
    for n in sorted(R["melody"]["notes"], key=lambda n: n["on"]): L.setdefault((n["sec"], n["line"]), []).append(n)
    keys = list(L); by = collections.defaultdict(list); rests = []; wl = []
    for a, b in zip(keys, keys[1:]):
        ns = L[a]; syl = [n for n in ns if n["text"]]; tr = WW.tier([(n["text"], n["stress"]) for n in syl]); last = syl[-1]
        held = sum(n["dur"] for n in ns[ns.index(last):]); by[tr[-1]].append(held); rests.append(L[b][0]["on"] - (ns[-1]["on"] + ns[-1]["dur"]))
        if tr[-1] == 1 and len(syl) > 1:
            j = len(syl) - 1
            while j > 0 and syl[j - 1]["text"] == last["text"] and tr[j] != 2: j -= 1
            if tr[j] == 2 and syl[j]["text"] == last["text"]:
                i = ns.index(syl[j]); hs = sum(n["dur"] for n in ns[i:ns.index(syl[j + 1])]); wl.append(held > hs)
    rests = np.array(rests)
    out = {["function", "weak", "stressed"][t]: dict(n=len(v), eighth_or_less=round(float(np.mean([x <= 6 for x in v])), 2), half_or_more=round(float(np.mean([x >= 24 for x in v])), 2)) for t, v in sorted(by.items())}
    print(f.split("/")[-1], out, "| run on (rest under a beat)", round(float(np.mean(rests < 12)), 2), "| rest median", float(np.median(rests)), "| weak outlasts stressed", f"{sum(wl)}/{len(wl)}")
