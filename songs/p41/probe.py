import pickle, sys, collections, numpy as np
F_ = sys.argv[1] if len(sys.argv) > 1 else "melody_v109_p40_main_t.pkl"; sys.argv = ["x", "1", "main"]; sys.path.insert(0, "/home/claude/p41")
import melody_v109_p40 as P, judges as J
D = pickle.load(open(F_, "rb"))
sd_c, sd_v, share, four5 = [], [], [], []
for b in D["all"]:
    if b["read"]["c"]: sd_c.append(b["read"]["c"]["notes_per_bar_sd"])
    if b["read"]["v"]: sd_v.append(b["read"]["v"]["notes_per_bar_sd"])
    lines = collections.defaultdict(list)
    for n in b["notes"]: lines[n[4]].append(n)
    for ln, ns in lines.items():
        if len(ns) >= 9:
            c = collections.Counter(x[0] // 48 for x in ns); m = max(c.values()) / len(ns); share.append(m); four5.append(m >= 0.8)
print("chorus sd", np.percentile(sd_c, [5, 50, 95]).round(2), "verse sd", np.percentile(sd_v, [5, 50, 95]).round(2), "share>2.91", np.mean(np.array(sd_c) > 2.91))
print("long lines: fullest share median", round(float(np.median(share)), 3), "4/5 in one bar", round(float(np.mean(four5)), 3), len(share))
jc = [b["judge"]["combined"] for b in D["all"]]; print("under floor", np.mean(np.array(jc) < J.FLOOR), "judge median", np.median(jc))
ga = collections.defaultdict(list)
for b in D["all"][:300]:
    for w in ("v", "c"):
        if b["read"][w]:
            for m, x in J.give_away(b["read"][w], k=46): ga[m].append(x)
print(sorted(((m, round(float(np.mean(v)), 3)) for m, v in ga.items()), key=lambda x: x[1])[:6])
