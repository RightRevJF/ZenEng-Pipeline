"""Keeping Time (song 44): the song record from melody_final.pkl (the pick of record) -- mid-tempo dance-pop, q = 112, four on the floor,
straight; C minor verses, E-flat major chorus; 80 bars (Q5 A, Q7 A, Q9 A; Q16 A the design; Q17 C the lift).
  voice   the mezzo, every line.
  pulse   (Q5 A) a synth pulse that drifts: in dotted eighths against the kick in the intro, the verses and the outro (it meets the beat
          every three beats and slides off again); in the pre-chorus it moves to eighths on the last bar; locked in straight eighths in the
          choruses and post-choruses. Under 'Two clocks on the same wall' it alone plays the clocks' two pitches, tick and tock, in eighths.
  drums   kick on every beat from intro bar 5; hats in dotted eighths with the pulse in the verses, off-beat open hats once locked; claps on
          2 and 4 from the pre-chorus on; a snare build in each pre-chorus's last bar and the bridge's last two; out (all but the pulse) for
          the chorus's fifth bar ('Two clocks'), back with a crash on 'wall'; the bridge: no kick for six bars, atmosphere, the kick back
          for its last two bars (the writer's note to draft 3).
  bass    root and octave in eighths once locked; quarters in the verses; whole notes in the bridge.
  pad     the chord, held a bar; wider in the bridge.
  Verses thinner, the last chorus the fullest (9.12). The outro drifts again and ends on one E-flat chord, let ring."""
import pickle, sys
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p48", "/home/claude/p40"]
import melody_p44 as P
M = P.M
import pyphen
F = pickle.load(open("/home/claude/p48/melody_final.pkl", "rb")); c = F["pick"]
BAR = 48; NB = P.NBARS; QB = 112
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"every": ["ev", "ery"], "Nobody's": ["No", "bo", "dy's"], "into": ["in", "to"], "different": ["dif", "fer", "ent"], "someone": ["some", "one"],
        "isn't": ["is", "n't"], "along": ["a", "long"], "behind": ["be", "hind"], "falling": ["fall", "ing"], "keeping": ["keep", "ing"], "against": ["a", "gainst"],
        "vowel": ["vow", "el"], "never": ["nev", "er"], "strangers": ["stran", "gers"], "shouting": ["shout", "ing"], "after": ["af", "ter"], "before": ["be", "fore"],
        "started": ["start", "ed"], "enough": ["e", "nough"], "always": ["al", "ways"], "counting": ["count", "ing"], "leaving": ["leav", "ing"], "anymore": ["an", "y", "more"]}
def split_words(text, sy):
    out = []; ws = text.replace('"', "").split()
    for w in ws:
        n = len(P.syl(w)); core = w.rstrip(",.;:?")
        if n <= 1: out.append((w, False)); continue
        parts = HFIX.get(w) or HFIX.get(core) or _PY.inserted(core).split("-")
        tail = "" if w in HFIX else w[len(core):]
        if len(parts) > n: parts = parts[:n - 1] + ["".join(parts[n - 1:])]
        while len(parts) < n: parts.append("_")
        for j, p in enumerate(parts): out.append((p + (tail if j == n - 1 else ""), j < n - 1))
    assert len(out) == len(sy), (text, out, sy)
    return out
TEXT = {sec: [split_words(t, P.LINES[sec][i]) for i, (_, t) in enumerate(M.WORDS_OF[sec])] for sec in P.SUNG}
bars = []
for nm, kind, nb in P.FORM:
    for k in range(nb):
        b = P.BAR0[nm] + k
        bars.append(dict(sec=nm, kind=kind, k=k, n=nb, chord=P.CHORD[b], roman=M.ROMAN[P.CHORD[b]], start=b * BAR, len=BAR, qbpm=QB, key=("C minor" if kind in ("Intro", "Verse", "Pre") else "E-flat major"), stop=False))
lead = []
for n in c["notes"]:
    sec, i = n["line"].split(":"); i = int(i); t, hy = TEXT[sec][i][n["syl"]]
    lead.append(dict(on=n["on"], dur=n["dur"], midi=n["p"], sec=sec, line=i, syl=n["syl"], first=not n["slur"], text=t, hyph=hy,
                     stress=P.LINES[sec][i][n["syl"]][1], role=M.WORDS_OF[sec][i][0], singer="voice"))
ROOT = {k: v[0] for k, v in M.CH.items()}
def low_root(ch, lo=34): return lo + (ROOT[ch] - lo) % 12                               # B-flat 1 .. A2
def chord3(ch, lo):
    out, p = [], lo
    while len(out) < 3:
        if p % 12 in M.CH[ch][1]: out.append(p)
        p += 1
    return out
drums, bass, pad, pulse = [], [], [], []
def ev(lst, on, dur, p, vel, art="", **kw): lst.append(dict(on=on, dur=dur, p=p if isinstance(p, list) else [p], vel=vel, art=art, **kw))
DR = dict(kick=36, clap=39, snare=38, ohh=46, chh=42, crash=49)
CLK = sorted({n["p"] for n in c["notes"] if n["line"] == "Chorus 1:2"})               # the clocks' two pitches (Q16 A)
CLOCK_BAR = {P.BAR0[s_] + 4 for s_ in ("Chorus 1", "Chorus 2", "Last Chorus")}         # 'Two clocks on the same wall': the chorus's fifth bar
def drifting(kind, sec, k, n): return kind in ("Intro", "Verse", "Outro") or (kind == "Pre" and k < n - 1)
for b in bars:
    sec, kind, ch, st, k, n = b["sec"], b["kind"], b["chord"], b["start"], b["k"], b["n"]
    r = low_root(ch); bar_i = st // BAR
    last = kind == "Outro" and k == n - 1
    if last:
        ev(pad, st, BAR, chord3("Eb", 55) + [chord3("Eb", 55)[0] + 12], 60, "ring"); ev(bass, st, BAR, [r], 84, "ring"); ev(drums, st, 3, DR["kick"], 96); ev(drums, st, 3, DR["crash"], 90)
        ev(pulse, st, BAR, [chord3("Eb", 67)[0]], 60, "ring"); continue
    lift = 14 if sec == "Last Chorus" else 6 if kind == "Chorus" else 0 if kind == "Post" else -10 if kind == "Verse" else -4   # 9.12: verses thinner, the last chorus the top
    tones = sorted(chord3(ch, 63)); drift = drifting(kind, sec, k, n)
    # ---- the clocks' bar: the pulse alone, tick and tock ----
    if bar_i in CLOCK_BAR:
        for j in range(8): ev(pulse, st + 6 * j, 5, [CLK[1 - j % 2] + 12], 84 + (6 if j % 2 == 0 else 0), "tick")
        continue
    # ---- the pulse ----
    if drift: [ev(pulse, st + e, 5, [tones[(e // 9) % 3] + 12], 66 + lift // 2 + (10 if e % 12 == 0 else 0), "drift") for e in range(0, 48, 9)]
    elif kind == "Bridge" and k < 6: [ev(pulse, st + e, 10, [tones[(e // 12) % 3] + 12], 52, "air") for e in range(0, 48, 12)]
    else: [ev(pulse, st + 6 * j, 5, [tones[j % 3] + 12], 70 + lift // 2 + (8 if j % 2 == 0 else 0), "lock") for j in range(8)]
    # ---- drums ----
    kick = not (kind == "Intro" and k < 4) and not (kind == "Bridge" and k < 6)
    if kick: [ev(drums, st + e, 3, DR["kick"], (100 if e == 0 else 92) + min(lift, 8)) for e in (0, 12, 24, 36)]
    if kick and drift: [ev(drums, st + e, 3, DR["chh"], 60 + lift // 2) for e in range(0, 48, 9)]
    elif kick: [ev(drums, st + e, 3, DR["ohh"], 70 + lift) for e in (6, 18, 30, 42)]
    if kind in ("Pre", "Chorus", "Post") or (kind == "Bridge" and k >= 6): [ev(drums, st + e, 3, DR["clap"], 96 + min(lift, 10)) for e in (12, 36)]
    if kind == "Chorus" and not drift: [ev(drums, st + e, 3, DR["chh"], 58 + lift) for e in range(0, 48, 3) if e % 6 == 3 or sec == "Last Chorus"]   # the last chorus: every sixteenth
    if (kind == "Pre" and k == n - 1) or (kind == "Bridge" and k >= 6):
        [ev(drums, st + e, 3, DR["snare"], 54 + e // 2, "build") for e in range(0, 48, 6 if (kind == "Bridge" and k == 6) else 3)]
    if kind == "Chorus" and (k == 0 or k == 5): ev(drums, st, 3, DR["crash"], 100 + min(lift, 10))      # the chorus, and 'wall' after the clocks
    # ---- bass ----
    if kind == "Bridge" and k < 6: ev(bass, st, 46, [r + 12], 78, "whole")
    elif kind == "Intro" and k < 4: pass
    elif drift: [ev(bass, st + 12 * j, 10, [r], 86 + lift // 2, "quarter") for j in range(4)]
    else: [ev(bass, st + 6 * j, 5, [r + 12 if j % 2 else r], (92 if j % 2 == 0 else 84) + lift // 2, "pulse") for j in range(8)]
    # ---- pad ----
    if not (kind == "Intro" and k < 4): ev(pad, st, BAR, chord3(ch, 55) + ([chord3(ch, 55)[0] + 12] if kind in ("Chorus", "Bridge") else []), (50 if kind != "Bridge" else 60) + lift // 2, "pad")
def tidy(lst):
    lst.sort(key=lambda e: (e["on"], e["p"][0])); out = []
    for e in lst:
        if out and out[-1]["on"] == e["on"]: out[-1]["p"] = sorted(set(out[-1]["p"] + e["p"])); out[-1]["vel"] = max(out[-1]["vel"], e["vel"]); continue
        out.append(e)
    return out
drums = tidy(drums); bass = tidy(bass); pad = tidy(pad); pulse = tidy(pulse)
plan = [(nm, nb, P.BAR0[nm], "4/4") for nm, _, nb in P.FORM]
secs = NB * 4 * 60 / QB
rec = dict(title="Keeping Time", nbars=NB, bars=bars, plan=plan, lead=lead, drums=drums, bass=bass, pad=pad, pulse=pulse,
           slot="twelfth of a beat", bar=BAR, qbpm=QB, feel=P.FEEL, seconds=secs, tw_sec=60 / QB / 12, fp=c["fp"],
           order_fp=F["run"]["order_fp"], survivors=F["run"]["survivors"], built=F["run"]["made"], meas={k: (float(v) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()},
           judge={k: c["judge"][k] for k in ("combined", "content", "order")}, plans=c["meta"]["plans"], hand_edits=c["hand_edits"], picked_from=c["picked_from"],
           kinds={f"{a}:{b}": v for (a, b), v in c["meta"]["kinds"].items()}, rerun=F["run"]["rerun"], text=TEXT, lift=c["info"]["lift"], registers=c["meta"]["registers"],
           palettes=c["meta"]["palettes"], outside_target=c["meta"]["outside_target"], carriers=c["meta"]["carriers"],
           design=dict(gates=P.DESIGN_GATES, slots={s: P.slots_of(s) for s in P.SUNG}, clocks=CLK, clock_bars=sorted(CLOCK_BAR)))
pickle.dump(rec, open("/home/claude/p48/song_record.pkl", "wb"))
if __name__ == "__main__":
    print(NB, "bars,", f"{secs:.0f} s;", len(lead), "sung;", {k: len(v) for k, v in dict(drums=drums, bass=bass, pad=pad, pulse=pulse).items()})
    for sec in P.SUNG:
        for i, ws in enumerate(TEXT[sec]): print(sec, i, " ".join(t + ("-" if h else "") for t, h in ws))
