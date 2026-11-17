"""Intro and outro lengths in bars in POP909 (Wang et al. 2020), from human_label1.txt (Dai, Zhang and Dannenberg's structure labels:
i intro, o outro, capitals sung sections, lower-case instrumental ones, each with its length in bars). Writes edges_pop909.json."""
import re, glob, json, collections, statistics as st
R = []
for f in glob.glob("/home/claude/data/pop909/*/human_label1.txt"):
    s = open(f).read().strip(); parts = re.findall(r"([A-Za-z])(\d+)", s)
    if not parts: continue
    intro = parts[0][1] if parts[0][0] == "i" else "0"
    outro = parts[-1][1] if parts[-1][0] == "o" else "0"
    # instrumental tail: lower-case sections at the end (o counted)
    tail = 0
    for k, n in reversed(parts):
        if k.islower(): tail += int(n)
        else: break
    last_sung = next((k for k, n in reversed(parts) if k.isupper()), None)
    R.append(dict(intro=int(intro), outro=int(outro), tail=tail, last_sung=last_sung, total=sum(int(n) for _, n in parts)))
def q(v):
    v = sorted(v); n = len(v); return [v[int(.25 * (n - 1))], st.median(v), v[int(.75 * (n - 1))]]
out = dict(songs=len(R), intro_share=round(100 * sum(r["intro"] > 0 for r in R) / len(R)), intro_bars=q([r["intro"] for r in R if r["intro"]]),
           outro_share=round(100 * sum(r["outro"] > 0 for r in R) / len(R)), outro_bars=q([r["outro"] for r in R if r["outro"]]),
           ends_sung=round(100 * sum(r["tail"] == 0 for r in R) / len(R)), instrumental_tail_bars=q([r["tail"] for r in R if r["tail"]]),
           last_sung=dict(collections.Counter(r["last_sung"] for r in R).most_common(4)))
json.dump(out, open("edges_pop909.json", "w"), indent=1); print(out)
