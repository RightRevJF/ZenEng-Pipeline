"""523: songs 40-46's regression runs against their orders of record (v131)."""
import json, re
REC = {"40": (("d508b254a8f4", 796), ("04342d35cd1d", 885)), "42": (("9fd23492dad3", 801), ("529bf7a1c186", 820)),
       "43": (("af58ce3be702", 882), ("a095303f51b7", 904)), "44": (("2f43a0bc93d6", 776), ("7d4dd7b83e26", 755)),
       "45": None, "46": (("120253ea25cb", 773), ("635084318e00", 860))}
old = {(r["song"], r["run"]): r for r in json.load(open("/home/claude/p56/regress/regression.json"))["rows"]}
REC["45"] = tuple((old[("45", m)]["record"], old[("45", m)]["record_survivors"]) for m in ("main", "ctl"))
rows = []
for s, recs in REC.items():
    for m, (r, n) in zip(("main", "ctl"), recs):
        t = open(f"/home/claude/p57/regress/run{s}_{m}.txt").read(); g = re.search(r"survivors (\d+) \([\d.]+%\), order (\w+)", t)
        rows.append(dict(song=s, run=m, record=r, record_survivors=n, rerun=g.group(2) if g else None, rerun_survivors=int(g.group(1)) if g else None,
                         same=bool(g) and g.group(2) == r and int(g.group(1)) == n))
v = "Every closed song reproduces its order of record, main and control." if all(x["same"] for x in rows) else "**Not every closed song reproduces: " + ", ".join(f"{x['song']} {x['run']}" for x in rows if not x["same"]) + ".**"
json.dump(dict(rows=rows, verdict=v), open("/home/claude/p57/regress/regression.json", "w"), indent=1)
print(v)
