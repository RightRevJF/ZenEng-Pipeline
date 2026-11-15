"""Sung to Sleep: the song-wide intensity curve as sung (749.17), in performed order: introduction, three times verse and refrain
(registration building each time), the link, verse 4, the final refrain, the coda. Per bar, from the record: the top of the singers'
line (sopranos or descant), whether the choir sings, how many parts sound, the organ's onsets, and the dynamic level with the
registration step. Each standardised and averaged; smoothed with the shape study's cosine filter. Reports where the high point
falls and whether each return rises above the one before."""
import json, sys
import numpy as np
sys.path.insert(0, "/home/claude/shape")
import shape_lib as SL
H = "/home/claude/p63"; BAR = 36
DYN = {0: 1, 276: 2, 864: 1, 1440: 3, 2160: 4, 2160 + 420: 1, 2736: 0}            # p, mp, p, mf, f, p (last line, 'hush'), pp (coda)
REG_STEP = [0.0, 0.5, 1.0]                                                       # verses and refrains 1, 2, 3: the registration builds
def bar_values(V, b):
    a, z = (b - 1) * BAR, b * BAR
    sound = lambda v: [e for e in V.get(v, []) if e["on"] < z and e["on"] + e["dur"] > a]
    ps = [e["p"] for v in ("S", "Desc") for e in sound(v)]
    top = max(ps) if ps else np.nan
    sing = 1.0 if sound("S") else 0.0
    parts = len({v for v in ("S", "A", "T", "B", "Desc") if sound(v)})
    org = sum(1 for v in ("org_rh", "org_rh_in", "org_lh", "org_ped") for e in V.get(v, []) if a <= e["on"] < z)
    dyn = DYN[max(k for k in DYN if k <= a)]
    return [top, sing, parts, org, dyn]
def performed(rec):
    V = rec["voices"]; rows = []; labels = []
    def add(b0, b1, lab, step=0.0):
        for b in range(b0, b1 + 1):
            r = bar_values(V, b); r[4] += step; rows.append(r); labels.append(lab)
    add(1, 8, "introduction")
    for i in range(3): add(9, 24, f"verse {i + 1}", REG_STEP[i]); add(25, 40, f"refrain {i + 1}", REG_STEP[i])
    add(41, 44, "link"); add(45, 60, "verse 4", 1.0); add(61, 76, "final refrain", 1.0); add(77, 80, "coda")
    return np.array(rows, float), labels
def curve(rec):
    X, labels = performed(rec)
    X[:, 0] = np.where(np.isnan(X[:, 0]), np.nanmean(X[:, 0]), X[:, 0])
    Z = (X - X.mean(0)) / np.where(X.std(0) > 0, X.std(0), 1); c = Z.mean(1)
    sm = SL.dct_smooth(c, 10); peak = int(np.argmax(sm)) / (len(sm) - 1)
    sec = {}
    for lab, v in zip(labels, c): sec.setdefault(lab, []).append(v)
    means = {k: float(np.mean(v)) for k, v in sec.items()}
    return dict(bars=len(c), raw=[float(x) for x in c], smooth=[float(x) for x in sm], peak_pos=peak, section_means=means,
                refrains_rise=means["refrain 1"] <= means["refrain 2"] <= means["refrain 3"] <= means["final refrain"],
                verses_rise=means["verse 1"] <= means["verse 2"] <= means["verse 3"] <= means["verse 4"])
if __name__ == "__main__":
    for p in sys.argv[1:] or [f"{H}/song_record.json"]:
        r = curve(json.load(open(p)))
        print(p, "performed bars", r["bars"], "high point at %.2f" % r["peak_pos"], "refrains rise", r["refrains_rise"], "verses rise", r["verses_rise"])
        print("  ", {k: round(v, 2) for k, v in r["section_means"].items()})
