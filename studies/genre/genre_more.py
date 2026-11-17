"""Follow-ups from the reading: Titon's register split of the third (via van der Bliek 2007), Day-O'Connell's 6 (falling to 5 or rising to 1),
Wagner's 'domesticated' blue notes (flat 3 or flat 7 as a chord tone), and where the leading tone goes. Major-key bars, CoCoPops Billboard."""
import json, os, collections, numpy as np
from genre_test import notes_of, deg, family, HERE
songs = json.load(open(os.path.join(HERE, "..", "tension", "cocopops_bars.json")))
reg = collections.Counter(); six = collections.defaultdict(collections.Counter); dom = collections.Counter(); lt = collections.defaultdict(collections.Counter)
for name, s in songs.items():
    ns = [n for n in notes_of(s) if not n["K"]["minor"]]
    if len(ns) < 40: continue
    fam = family(name); med = np.median([n["p"] for n in ns])
    for n in ns:
        d = deg(n); up = n["p"] >= med; nx = n["nxt"]
        if d in (3, 4): reg[("upper" if up else "lower", d)] += 1
        if d in (3, 10) and n["ch"] is not None: dom[(d, (n["p"] % 12) in n["ch"]["pcs"])] += 1
        if nx is None: continue
        st = nx - n["p"]; dn = (nx - n["K"]["tonic"]) % 12
        if d == 9:
            k = "down to 5" if st == -2 else "up to 1" if st == 3 and dn == 0 else "up to 7" if st == 2 else "repeat" if st == 0 else "other"
            six[fam][k] += 1; six["all"][k] += 1
        if d == 11:
            k = "up to 1" if st == 1 else "down to 6" if st == -2 else "repeat" if st == 0 else "other"
            lt[fam][k] += 1; lt["all"][k] += 1
pct = lambda c: {k: round(v / sum(c.values()), 3) for k, v in c.most_common()}
out = dict(
  third_by_register={r: round(reg[(r, 3)] / (reg[(r, 3)] + reg[(r, 4)]), 3) for r in ("lower", "upper")},
  third_counts={f"{r} {'flat 3' if d == 3 else '3'}": v for (r, d), v in reg.items()},
  six_next={f: pct(c) for f, c in six.items()}, six_n={f: sum(c.values()) for f, c in six.items()},
  flat3_as_chord_tone=round(dom[(3, True)] / (dom[(3, True)] + dom[(3, False)]), 3),
  flat7_as_chord_tone=round(dom[(10, True)] / (dom[(10, True)] + dom[(10, False)]), 3),
  leading_tone_next={f: pct(c) for f, c in lt.items()}, lt_n={f: sum(c.values()) for f, c in lt.items()})
json.dump(out, open(os.path.join(HERE, "genre_more_results.json"), "w"), indent=1); print(json.dumps(out, indent=1))
