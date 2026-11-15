"""The returning chorus varied (proposed fix 749.8, tried on song 52). Reads melody_final.json, writes melody_varied.json.

The rule, for a chorus that returns (not the first, not a line the final chorus draws fresh):
  - its first line and its hook stay exact, so the chorus is known at once and the hook is the same hook;
  - on each inner line copied from chorus 1, at most one note is lifted: a stressed note of a quarter or longer, or the line's last note;
  - it moves to the nearest chord tone above, within a minor third (within a fourth for a line's last note);
  - it stays at or under the section's cap (C#5 here), below the hook's peak; no run of four; no leap into or out of it past a fifth;
  - of the candidates, the longest is lifted (ties: the later).
The final chorus's copied lines take the second chorus's version, so each chorus sits a little higher than the one before."""
import json, copy, hashlib
import gen68 as G
H = "/home/claude/p62"
F = json.load(open(f"{H}/melody_final.json")); pick = copy.deepcopy(F["pick"])
CAP = G.REG["Chorus"][2]; HOOK_I = 4
def tones(t): return G.CHT[G.chord_at(t)]
def line(notes, sec, i): return [n for n in notes if n["sec"] == sec and n["line"] == i]
LOG = []
for i in range(1, HOOK_I):
    ln = line(pick["notes"], "Chorus 2", i); ps = [n["p"] for n in ln]; cands = []
    for k, n in enumerate(ln):
        final = k == len(ln) - 1
        if not (final or (n["stress"] and n["dur"] >= 12)): continue
        reach = 5 if final else 3
        up = next((q for q in range(n["p"] + 1, n["p"] + reach + 1) if q % 12 in tones(n["on"])), None)
        if up is None or up > CAP: continue
        trial = ps[:k] + [up] + ps[k + 1:]
        if not G.runs_ok(trial): continue
        if k > 0 and abs(up - ps[k - 1]) > 7: continue
        if k + 1 < len(ps) and abs(ps[k + 1] - up) > 7: continue
        cands.append((n["dur"], k, up))
    if not cands: LOG.append(dict(line=i, change=None)); continue
    d, k, up = max(cands)
    n = ln[k]; LOG.append(dict(line=i, syl=n["text"], on=n["on"], was=n["p"], now=up, dur=n["dur"]))
    n["p"] = up
for n in pick["notes"]:                                                   # the final chorus's copied lines take chorus 2's
    if n["sec"] == "Last Chorus" and n["line"] in (1,):
        src = [m for m in line(pick["notes"], "Chorus 2", n["line"]) if m["syl"] == n["syl"]][0]
        if src["p"] != n["p"]: LOG.append(dict(line=f"Last Chorus {n['line']}", syl=n["text"], on=n["on"], was=n["p"], now=src["p"], dur=n["dur"])); n["p"] = src["p"]
f = G.gates(pick); assert not f, f
pick["readings"] = G.readings(pick["notes"]); pick["charge"], pick["distance"] = G.charge(pick["readings"])
pick["fp_drawn"] = pick["fp"]; pick["fp"] = hashlib.sha1(json.dumps([(n["on"], n["p"]) for n in pick["notes"]]).encode()).hexdigest()[:12]
c1 = [n["p"] for n in pick["notes"] if n["sec"] == "Chorus 1"]; c2 = [n["p"] for n in pick["notes"] if n["sec"] == "Chorus 2"]
out = dict(F, pick=pick, variation=dict(rule=__doc__, log=LOG, chorus_notes=len(c2), changed=sum(a != b for a, b in zip(c1, c2))))
json.dump(out, open(f"{H}/melody_varied.json", "w"), default=float)
if __name__ == "__main__":
    for e in LOG: print(e)
    print("chorus 2 notes changed:", out["variation"]["changed"], "of", len(c2), "; charge", round(pick["charge"], 3), "was", round(F["pick"]["charge"], 3), "; fp", pick["fp"])
