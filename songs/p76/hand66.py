"""Song 66 (They Did the Right Thing): the writer's design notes (intake.py DESIGN_NOTES_FROM_THE_WRITER), laid on the engine's design run
(run_d/lyric66_d.song.json: v52, the tune held inside a tenor over an A3 tonic, design66.py). Writes lyric66_d.hand.song.json, which the
document scripts read. The engine's record is not touched. Every edit is listed in the record's "hand_edits".
  1. The chorus ends hold E4 (the key's fifth) at least two bars, and the bass begins a chromatic descent under it:
       chorus 1, 'gone' held two bars; the turn after it: E | E/D# | E7/D | Am/C (bass E, D#, D, C);
       chorus 2, 'gone' held two bars; the turn after it: E | E/D# (the bridge then sits on E).
  2. The bridge: voice, guitar and bass only, the lowest level of the song (no drums, no harmony voice).
  3. After the bridge: all stop, two beats, every instrument, no fill (the last two beats of the bridge's last bar).
  4. The final chorus: the full band back on the downbeat, nothing in the bar before; 'gone' held three bars over the bass E, D#, D, C#, C:
       five bars added after the final chorus (E | E/D# | E7/D | A/C# | C), so the tag starts after the descent, not under it.
  5. The tag: voice and guitar, fading; its last word held on E4, then the guitar alone; the song ends on A minor, no cadence.
"""
import json, os, sys, copy
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "..", "lib", "luthier"))
R = json.load(open(os.path.join(HERE, "run_d", "lyric66_d.song.json"))); BAR = R["bar"]; B = BAR // 4
assert R["key"]["key"] == "Am" and R["key"]["tonic_midi"] == 57
N = R["melody"]["notes"]; P = R["parts"]; EDITS = []
FORM = []; _b = 0
for sec, kind, nb in R["form"]: FORM.append([sec, kind, _b, _b + nb]); _b += nb
def start(sec): return next(f[2] for f in FORM if f[0] == sec)
def end(sec): return next(f[3] for f in FORM if f[0] == sec)
def last_word(sec):
    ns = sorted([n for n in N if n["sec"] == sec and n["text"]], key=lambda n: n["on"]); return ns[-1]
E4 = 64
# chords: name, roman, pitch classes (absolute), bass MIDI, guitar voicing
CH = {"E": ("V", [4, 8, 11], 40, [52, 56, 59]), "E/D#": ("V/♯4", [4, 8, 11], 39, [52, 56, 59]), "E7/D": ("V7/4", [4, 8, 11, 2], 38, [52, 56, 59]),
      "Am/C": ("i/♭3", [0, 4, 9], 36, [52, 57, 60]), "A/C#": ("I/3", [9, 1, 4], 37, [52, 57, 61]), "C": ("bIII", [0, 4, 7], 36, [55, 60, 64])}
for nm, (rn, pcs, _, _) in CH.items(): R["chord_tones"].setdefault(rn, pcs)
def set_bar(bi, name):
    """bar bi (absolute) gets the chord: its symbol in the record, the guitar's strums revoiced, the bass's notes moved to the designed bass note."""
    f = next(f for f in FORM if f[2] <= bi < f[3]); k = bi - f[2]; was = R["chords"][f[0]][k]
    rn, pcs, bass, voic = CH[name]; R["chords"][f[0]][k] = name; R["roman"][f[0]][k] = rn
    t0, t1 = bi * BAR, (bi + 1) * BAR
    for e in P["chords"]:
        if t0 <= e["on"] < t1: e["p"] = list(voic)
    for e in P["bass"]:
        if t0 <= e["on"] < t1: e["p"] = [bass]
    return dict(bar=bi + 1, was=was, now=name)
def hold(sec, bars_, why):
    n = last_word(sec); before = (n["text"], n["on"] / BAR + 1, n["dur"] / B, n["midi"])
    n["midi"] = E4; n["dur"] = bars_ * BAR
    EDITS.append(dict(what=why, word=n["text"], before=before, after=(n["text"], n["on"] / BAR + 1, n["dur"] / B, n["midi"]))); return n
# ---- 4 first (it moves everything after the final chorus): five bars after it
INS = 5; c3 = next(f for f in FORM if f[0] == "Chorus 3"); at = c3[3] * BAR; SH = INS * BAR
def shift(evs):
    for e in evs:
        if e["on"] >= at: e["on"] += SH
for k in ("chords", "bass", "drums", "harmony"): shift(P[k])
shift(N)
model = c3[3] - 2                                                     # the final chorus's next-to-last bar: its strums, bass and drums carry the added bars
for i in range(INS):
    for k in ("chords", "bass", "drums"):
        P[k] += [dict(e, on=e["on"] - model * BAR + (c3[3] + i) * BAR) for e in P[k] if model * BAR <= e["on"] < (model + 1) * BAR]
R["chords"]["Chorus 3"] += [None] * INS; R["roman"]["Chorus 3"] += [None] * INS
for f in R["form"]:
    if f[0] == "Chorus 3": f[2] += INS
FORM = []; _b = 0
for sec, kind, nb in R["form"]: FORM.append([sec, kind, _b, _b + nb]); _b += nb
CH_EDITS = [set_bar(c3[3] + i, nm) for i, nm in enumerate(["E", "E/D#", "E7/D", "A/C#", "C"])]
hold("Chorus 3", 3, "4: the final chorus's 'gone' on E4, held three bars, over the bass E, D#, D (then C#, C)")
EDITS.append(dict(what=f"4: five bars added after the final chorus (bars {c3[3] + 1} to {c3[3] + INS}), the descent's chords", chords=CH_EDITS))
# ---- 1: the first two choruses' ends
t2 = start("Turn 2"); EDITS.append(dict(what="1: the turn after chorus 1, the descent begun", chords=[set_bar(t2 + i, nm) for i, nm in enumerate(["E", "E/D#", "E7/D", "Am/C"])]))
hold("Chorus 1", 2, "1: chorus 1's 'gone' on E4, held two bars")
t3 = start("Turn 3"); EDITS.append(dict(what="1: the turn after chorus 2, the descent begun", chords=[set_bar(t3 + i, nm) for i, nm in enumerate(["E", "E/D#"])]))
hold("Chorus 2", 2, "1: chorus 2's 'gone' on E4, held two bars")
# ---- 5: the tag's last word held, then the guitar alone
tag_last = hold("Tag", 2, "5: the tag's last word on E4, held to the outro's first bar, then the guitar alone")
tag_last["dur"] = (start("Outro") + 1) * BAR - tag_last["on"]; EDITS[-1]["after"] = (tag_last["text"], tag_last["on"] / BAR + 1, tag_last["dur"] / B, tag_last["midi"])
# ---- 2, 3, 5: who plays where
br0, br1 = start("Bridge") * BAR, end("Bridge") * BAR; stop0 = br1 - 2 * B
tg0 = start("Tag") * BAR; held = [(n["on"], n["on"] + n["dur"]) for n in N if n.get("_held")]
HOLDS = [(n["on"], n["on"] + n["dur"]) for n in N if n["midi"] == E4 and n["dur"] >= 2 * BAR]
def drop(k, cond, why):
    before = len(P[k]); P[k] = [e for e in P[k] if not cond(e)]; return dict(part=k, removed=before - len(P[k]), why=why)
REMOVED = [drop("drums", lambda e: br0 <= e["on"] < br1, "2: the bridge has no drums"),
           drop("harmony", lambda e: br0 <= e["on"] < br1, "2: the bridge has no harmony voice"),
           drop("drums", lambda e: e["on"] >= tg0, "5: the tag and outro: voice and guitar"),
           drop("bass", lambda e: e["on"] >= tg0, "5: the tag and outro: voice and guitar"),
           drop("harmony", lambda e: e["on"] >= tg0, "5: the tag and outro: voice and guitar"),
           drop("harmony", lambda e: any(a <= e["on"] < b for a, b in HOLDS), "1, 4: the held E4 sung alone")]
for k in ("chords", "bass", "drums"):                                                    # 3: the stop
    for e in P[k]:
        if e["on"] < stop0 < e["on"] + e["dur"]: e["dur"] = stop0 - e["on"]
    REMOVED.append(drop(k, lambda e: stop0 <= e["on"] < br1, "3: all stop, the bridge's last two beats"))
N.sort(key=lambda n: n["on"])
for a, b in zip(N, N[1:]): assert a["on"] + a["dur"] <= b["on"], (a, b)
for k in P: P[k].sort(key=lambda e: e["on"])
# levels: the bridge the lowest of the song, the tag fading
R["levels"] = dict(R["levels"], **{"Bridge": 0.55, "Tag": 0.62, "Outro": 0.5})
import word_weight as WW_
fit = {k: round(v, 3) for k, v in WW_.fit([n for n in N if n.get("melisma") != "second"], BAR, B, parts=True).items()}
R["hand_edits"] = dict(note="the writer's design notes (hand66.py), logged in intake.py; the engine's record is run_d/lyric66_d.song.json", edits=EDITS, removed=REMOVED,
                       stop=dict(bar=end("Bridge"), beats="3 and 4"), holds=[(a / BAR + 1, (b - a) / B) for a, b in HOLDS] + [(tag_last["on"] / BAR + 1, tag_last["dur"] / B)],
                       words_fit_engine=R["judge7"]["pick_words_fit"], words_fit_after=fit)
json.dump(R, open(os.path.join(HERE, "lyric66_d.hand.song.json"), "w"), indent=1)
if __name__ == "__main__":
    for e in EDITS: print(e)
    for r in REMOVED: print(r)
    print("form:", R["form"]); print("words' fit: engine", R["judge7"]["pick_words_fit"], "after", fit)
