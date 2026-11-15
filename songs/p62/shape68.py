"""The song shaped as a whole (proposed fix 749.10, tried on song 52, third edition). Reads melody_varied.json, writes melody_shaped.json.

Before, every register came from the section's kind (verse, chorus, bridge), never from its place in the song: four verses at one height,
the last chorus no higher than the first, the song's top note in bar 21 of 84. The plan here sets a target for each section by its place:
  - verses 1 and 2 as drawn (the tune learned); verse 3 (the turn: the first night's sleep) three quarters of a semitone higher on average; verse 4
    (the resolve) about one and three quarters higher, its cap a step above the verse's (B4);
  - choruses 1 and 2 as they are (chorus 2 already lifted, 749.8); the last chorus's lines above chorus 2's on average, cap C#5;
  - the bridge stays the hush;
  - the song's top moves late: in the last chorus the first 'door' sings E5, a step over the D5 of choruses 1 and 2, once.
How a section reaches its target: whole lines move up one step of the scale, so each tune keeps its shape (the latest line first, each
line at most once), until the section's mean meets its target. Rhythm unchanged. After the shift, a stressed, long or on-the-beat note that
is not in its chord moves to the nearest chord tone; a note over the cap comes down to the highest chord tone under it; over B-flat no F#,
C# or B; the voice stays in the scale; no run of four; a note that would leap past a fifth from its neighbour takes the nearer fit."""
import json, copy, hashlib, collections
import numpy as np
import gen68 as G
H = "/home/claude/p62"
F = json.load(open(f"{H}/melody_varied.json")); pick = copy.deepcopy(F["pick"])
def sec_notes(ns, s): return [n for n in ns if n["sec"] == s]
def mean(ns, s, lines=None): v = [n["p"] for n in sec_notes(ns, s) if lines is None or n["line"] in lines]; return sum(v) / len(v)
BASE_V = mean(pick["notes"], "Verse 1"); BASE_C2 = mean(pick["notes"], "Chorus 2", (0, 1, 2, 3))
TARGET = {"Verse 3": (BASE_V + 0.75, 69, None), "Verse 4": (BASE_V + 1.75, 71, None), "Last Chorus": (BASE_C2 + 1.0, 73, (0, 1, 2, 3))}
LOG = []
def tones(t): return G.CHT[G.chord_at(t)]
SC = sorted(q for q in range(48, 84) if q % 12 in G.SCALE)
def step_up(p, k=1):
    if p not in SC: return p
    return SC[min(len(SC) - 1, SC.index(p) + k)]
def shift_line(ns, sec, li, cap):
    ln = [n for n in ns if n["sec"] == sec and n["line"] == li]; old = [n["p"] for n in ln]; new = []
    for k, n in enumerate(ln):
        ct = tones(n["on"]) & G.SCALE; bad = {6, 1, 11} if G.chord_at(n["on"]) == "Bbmaj7" else set()
        strong = n["stress"] or n["dur"] >= 12 or n["on"] % G.BEAT == 0
        ok = (ct if strong else G.SCALE) - bad
        q = step_up(n["p"])
        if q % 12 not in ok or q > cap:
            fits = [x for x in range(n["p"] - 2, cap + 1) if x % 12 in ok]
            q = min(fits, key=lambda x: (abs(x - step_up(n["p"])), -x)) if fits else n["p"]
        if new and abs(q - new[-1]) > 7:
            fits = [x for x in range(new[-1] - 7, min(cap, new[-1] + 7) + 1) if x % 12 in ok]
            q = min(fits, key=lambda x: abs(x - q)) if fits else n["p"]
        new.append(q)
    for _ in range(8):                                                                 # a run of four: the weakest note of it takes the next fit
        r = next((k for k in range(len(new) - 3) if new[k] == new[k + 1] == new[k + 2] == new[k + 3]), None)
        if r is None: break
        j = min(range(r, r + 4), key=lambda j: (ln[j]["stress"], ln[j]["dur"], ln[j]["on"] % G.BEAT == 0))
        n = ln[j]; ct = tones(n["on"]) & G.SCALE; bad = {6, 1, 11} if G.chord_at(n["on"]) == "Bbmaj7" else set()
        fits = [x for x in range(new[j] - 3, min(cap, new[j] + 3) + 1) if x % 12 in (G.SCALE - bad) and x != new[j]]
        if not fits: break
        new[j] = min(fits, key=lambda x: (abs(x - step_up(old[j])), x > new[j]))
    if not G.runs_ok(new): return False
    for n, q, o in zip(ln, new, old):
        n["p"] = q
    LOG.append(dict(sec=sec, line=li, was=old, now=new, changed=sum(a != b for a, b in zip(old, new)))); return True
for sec, (tgt, cap, lines) in TARGET.items():
    order = sorted({n["line"] for n in pick["notes"] if n["sec"] == sec and (lines is None or n["line"] in lines)}, reverse=True)
    for li in order:
        if mean(pick["notes"], sec, lines) >= tgt: break
        shift_line(pick["notes"], sec, li, cap)
for n in pick["notes"]:                                                                          # the song's top, late: the last chorus's first 'door' on E5
    if n["sec"] == "Last Chorus" and n["line"] == 4 and n["p"] == 74:
        LOG.append(dict(sec="Last Chorus", line=4, was=[74], now=[76], changed=1, note="door")); n["p"] = 76
def gates3(c):
    """gen68.gates with the third edition's one change: the top is E5, sung once, on the last chorus's first 'door'; D5 still only on 'door'."""
    f = []
    top = [n for n in c["notes"] if n["p"] >= 75]
    if not (len(top) == 1 and top[0]["p"] == 76 and top[0]["sec"] == "Last Chorus" and top[0]["line"] == 4): f.append("design: E5 once, on the last chorus's first 'door'")
    if any(n["p"] == 74 and not ((n["sec"], n["line"]) in G.DSPEC and G.DSPEC[(n["sec"], n["line"])] is G.DOOR) for n in c["notes"]): f.append("design: D5 only on 'door'")
    c2 = copy.deepcopy(c)
    for n in c2["notes"]:
        if n["p"] == 76: n["p"] = 74
    f += G.gates(c2)
    return f
f = gates3(pick); assert not f, f
pick["readings"] = G.readings(pick["notes"]); pick["charge"], pick["distance"] = G.charge(pick["readings"])
pick["fp"] = hashlib.sha1(json.dumps([(n["on"], n["p"]) for n in pick["notes"]]).encode()).hexdigest()[:12]
def shape_readings(ns, nbars=G.NBARS):
    """song-level readings: each section's mean pitch, the verses' rise, the last chorus against the first, where the top falls."""
    secs = list(dict.fromkeys(n["sec"] for n in ns)); m = {s: mean(ns, s) for s in secs}
    top = max(n["p"] for n in ns); first_top = min(n["on"] for n in ns if n["p"] == top) // G.BAR + 1
    vs = [m[s] for s in secs if s.startswith("Verse")]
    return {"section means": {s: round(v, 2) for s, v in m.items()}, "verse 4 over verse 1 (semitones)": round(vs[-1] - vs[0], 2),
            "the verses rise in order": all(b >= a - 0.05 for a, b in zip(vs, vs[1:])),
            "last chorus over chorus 1, lines before the hook (semitones)": round(mean(ns, "Last Chorus", (0, 1, 2, 3)) - mean(ns, "Chorus 1", (0, 1, 2, 3)), 2),
            "top note": top, "bar of the top note's first sounding": first_top, "share of the song before it": round((first_top - 1) / nbars, 2)}
before = shape_readings(F["pick"]["notes"]); after = shape_readings(pick["notes"])
json.dump(dict(F, pick=pick, shape=dict(rule=__doc__, targets={k: v[0] for k, v in TARGET.items()}, log=LOG, before=before, after=after)), open(f"{H}/melody_shaped.json", "w"), default=float)
if __name__ == "__main__":
    for e in LOG: print(e)
    print("before", before); print("after ", after)
    print("charge", round(pick["charge"], 3), "was", round(F["pick"]["charge"], 3), "fp", pick["fp"], "lifts", len(LOG))
    for k, v in pick["readings"].items():
        a, mm, z = G.Q[k]; print(f"  {k}: {round(v, 3)} (kept {round(a, 3)}, {round(mm, 3)}, {round(z, 3)}){' *' if not (a <= v <= z) else ''}")
