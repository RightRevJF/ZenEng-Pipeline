import json, sys, subprocess, collections
def lcs(a, b):
    L = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a)):
        for j in range(len(b)): L[i + 1][j + 1] = L[i][j] + 1 if a[i] == b[j] else max(L[i][j + 1], L[i + 1][j])
    return L[-1][-1]
def load(rev, path): return json.loads(subprocess.check_output(["git", "show", f"{rev}:{path}"]))
for path in sys.argv[2:]:
    for rev in sys.argv[1].split(","):
        R = load(rev, path); how = R["spec"].get("how", {}); N = collections.defaultdict(list)
        for n in R["melody"]["notes"]: N[(n["sec"], n["line"])].append(n)
        out = []
        for k, v in how.items():
            if not (isinstance(v, list) and v[0] == "again"): continue
            s, i = k.rsplit(":", 1); a = N[(s, int(i))]; b = N[(v[1], int(v[2]))]
            if not a or not b: continue
            pa = [n["midi"] for n in a]; pb = [n["midi"] for n in b]
            ra = [n["on"] - a[0]["on"] for n in a]; rb = [n["on"] - b[0]["on"] for n in b]
            out.append((len(pa) == len(pb), lcs(pa, pb) / len(pb), lcs(ra, rb) / len(rb), pa == pb and ra == rb))
        same = [o for o in out if o[0]]; diff = [o for o in out if not o[0]]
        f = lambda xs, k: round(sum(x[k] for x in xs) / max(1, len(xs)), 3)
        print(path.split("/")[-1], rev, "again lines", len(out), "| same count", len(same), "identical", sum(o[3] for o in same), "pitch kept", f(same, 1),
              "| other count", len(diff), "pitch kept", f(diff, 1), "rhythm kept", f(diff, 2))
