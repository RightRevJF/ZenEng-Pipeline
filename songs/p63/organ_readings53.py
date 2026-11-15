"""The organ part measured against the Lieder accompaniment tables (tables/accompaniment_lieder.json, 3/4): per section, the right hand's
onsets a beat (both layers), the left hand's with the pedal (a pianist's left hand carries the bass), complementarity (the share of organ
onsets where the singers' tune has none) and the texture of each bar by the same rules as the tables (accomp_tables.texture)."""
import json, sys, collections
sys.path.insert(0, "/home/claude/atlas")
from accomp_tables import texture
BAR = 36
SECTIONS = [("introduction", 1, 8), ("verses 1-3", 9, 24), ("refrain", 25, 40), ("link", 41, 44), ("verse 4", 45, 60), ("final refrain", 61, 76), ("coda", 77, 80)]
def ons(V, names, b):
    out = collections.defaultdict(set)
    for n in names:
        for e in V.get(n, []):
            if (b - 1) * BAR <= e["on"] < b * BAR:
                out[e["on"] - (b - 1) * BAR] |= set(e["p"] if isinstance(e["p"], list) else [e["p"]])
    return sorted((o, sorted(p)) for o, p in out.items())
def read(path):
    V = json.load(open(path))["voices"]; res = {}
    for name, b0, b1 in SECTIONS + [("whole", 1, 80)]:
        rh_n = lh_n = pon = comp = 0; tex = collections.Counter(); nb = b1 - b0 + 1
        for b in range(b0, b1 + 1):
            rh = ons(V, ["org_rh", "org_rh_in"], b); lh = ons(V, ["org_lh", "org_ped"], b)
            vo = {o for o, _ in ons(V, ["S"], b)}
            rh_n += len(rh); lh_n += len(lh); po = {o for o, _ in rh} | {o for o, _ in lh}; pon += len(po); comp += len(po - vo)
            tex[texture(rh, lh, BAR, [0, 12, 24], "3/4")] += 1
        res[name] = dict(rh_a_beat=round(rh_n / nb / 3, 2), lh_ped_a_beat=round(lh_n / nb / 3, 2), complementarity=round(comp / max(1, pon), 2),
                         texture={k: round(v / nb, 2) for k, v in tex.most_common()})
    return res
if __name__ == "__main__":
    T = json.load(open("/home/claude/atlas/tables/accompaniment_lieder.json"))["by_metre"]["3/4"]
    print("Lieder 3/4: rh", [round(x, 2) for x in T["rh_onsets_a_beat"]], "lh", [round(x, 2) for x in T["lh_onsets_a_beat"]], "comp", [round(x, 2) for x in T["complementarity"]], T["texture_share"])
    for p in sys.argv[1:]:
        print(p)
        for k, v in read(p).items(): print(f"  {k:14s}", v)
