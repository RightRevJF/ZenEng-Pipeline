"""523: songs 40-45's regression runs against their orders of record (v129, songs/p55 part1)."""
import json, pickle, re, os
REC = {"40": ("d508b254a8f4", "04342d35cd1d"), "42": ("9fd23492dad3", "529bf7a1c186"), "43": ("af58ce3be702", "a095303f51b7"),
       "44": ("2f43a0bc93d6", "7d4dd7b83e26"), "45": ("6dc6710923f0", "9a1c46f67b24")}
rows = []
for s, (rm, rc) in REC.items():
    for m, r in (("main", rm), ("ctl", rc)):
        P0 = pickle.load(open(f"/home/claude/p55/part1/melody_v129_p{s}_{m}.pkl", "rb")); assert P0["order_fp"] == r
        t = open(f"/home/claude/p56/regress/run{s}_{m}.txt").read(); g = re.search(r"survivors (\d+) \([\d.]+%\), order (\w+)", t)
        rows.append(dict(song=s, run=m, record=r, record_survivors=P0["survivors"], rerun=g.group(2), rerun_survivors=int(g.group(1)), same=g.group(2) == r and int(g.group(1)) == P0["survivors"]))
v = "Every closed song reproduces its order of record, main and control." if all(x["same"] for x in rows) else "**Not every closed song reproduces: " + ", ".join(f"{x['song']} {x['run']}" for x in rows if not x["same"]) + ".**"
json.dump(dict(rows=rows, verdict=v), open("/home/claude/p56/regress/regression.json", "w"), indent=1)
print(v)
