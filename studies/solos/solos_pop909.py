"""Mid-song instrumental sections in POP909 (structure labels in human_label1.txt: lower-case letters other than i and o are instrumental
sections). Per song: whether one occurs between the first and last sung sections, its length in bars, place (fraction of bars) and the
section before it. Writes solos_pop909.json."""
import re, glob, json, collections, statistics as st
R = []; secs = []
for f in glob.glob("/home/claude/data/pop909/*/human_label1.txt"):
    p = re.findall(r"([A-Za-z])(\d+)", open(f).read().strip())
    if not p: continue
    tot = sum(int(n) for _, n in p); sung = [i for i, (k, n) in enumerate(p) if k.isupper()]
    if not sung: continue
    pos = 0; has = False
    for i, (k, n) in enumerate(p):
        if k.islower() and k not in "io" and sung[0] < i < sung[-1]:
            has = True; secs.append(dict(bars=int(n), frac=pos / tot, before=p[i - 1][0]))
        pos += int(n)
    R.append(has)
def q(v): v = sorted(v); return [v[int(.25 * (len(v) - 1))], st.median(v), v[int(.75 * (len(v) - 1))]]
out = dict(songs=len(R), with_mid_instrumental=round(100 * sum(R) / len(R)), sections=len(secs), bars=q([s["bars"] for s in secs]),
           place=[round(x, 2) for x in q([s["frac"] for s in secs])])
json.dump(out, open("solos_pop909.json", "w"), indent=1); print(out)
