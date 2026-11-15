"""Every eighth of the song: the pitches sounding in the choir and the organ; counts semitone clashes (a minor second or major seventh
between any two pitch classes) and, between the organ's top and its pedal, parallel fifths and octaves from one onset to the next."""
import json, sys, collections
BAR = 36
def sounding(V, names, t):
    out = []
    for n in names:
        for e in V.get(n, []):
            if e["on"] <= t < e["on"] + e["dur"]: out += e["p"] if isinstance(e["p"], list) else [e["p"]]
    return out
def run(path):
    V = json.load(open(path))["voices"]; clashes = collections.Counter(); where = []
    names = ["S", "A", "T", "B", "Desc", "org_rh", "org_rh_in", "org_lh", "org_ped"]
    for t in range(0, 80 * BAR, 6):
        ps = sounding(V, names, t); pc = {p % 12 for p in ps}
        bad = [(a, (a + 1) % 12) for a in pc if (a + 1) % 12 in pc]
        if bad:
            b = t // BAR + 1; clashes[b] += 1; where.append((b, (t % BAR) / 12 + 1, sorted(ps)))
    # parallels: organ top (highest of rh layers) against the pedal at successive organ onsets
    ons = sorted({e["on"] for n in ("org_rh", "org_rh_in", "org_ped") for e in V.get(n, [])})
    par = []
    for a, b in zip(ons, ons[1:]):
        ta, tb = sounding(V, ["org_rh", "org_rh_in"], a), sounding(V, ["org_rh", "org_rh_in"], b)
        pa, pb = sounding(V, ["org_ped"], a), sounding(V, ["org_ped"], b)
        if not (ta and tb and pa and pb): continue
        x0, x1, y0, y1 = max(ta), max(tb), pa[0], pb[0]
        i0, i1 = (x0 - y0) % 12, (x1 - y1) % 12
        if i0 == i1 and i0 in (0, 7) and x0 != x1 and y0 != y1: par.append((b // BAR + 1, i0))
    return clashes, where, par
if __name__ == "__main__":
    for p in sys.argv[1:]:
        c, w, par = run(p)
        print(p, "eighths with a semitone clash:", sum(c.values()), "outer parallels:", par)
        if "-v" in sys.argv: print(w[:60])
