"""Build the song record for 'Dance Anyway' from the frozen pick (melody_main.pkl, ranking #1, no hand edits).
Times in twelfths of a beat (a bar is 48) at q = 118, E-flat major throughout. A four-on-the-floor disco-pop band:
  drums   kick on every beat from bar 3; clap with the snare on 2 and 4; hats in eighths in the verses, sixteenths with the open hat on
          every 'and' in the choruses; a crash into each chorus; a snare build in the last bar of each pre-chorus and the bridge's last two.
          The bridge: the kick on 1 and 3 only, no hats, until its build.
  bass    disco octaves: root on the beat, the octave on each 'and' (verses: root and octave in quarters, lighter); the bridge in whole
          notes; the outro's last bar one hit.
  keys    electric piano stabs on the 'and' of 2 and 4 (verses), on every 'and' (choruses); held chords in the bridge.
  guitar  muted sixteenths with the chord on the 'and' of each beat, from verse 2 and in every chorus.
  pad     a held synth pad from the first pre-chorus; the last chorus voiced an octave higher.
  synth   the hook ('so I dance anyway') played in the intro's last two bars and the outro, an octave over the voice."""
import pickle, sys, re
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p36", "/home/claude/carol", "/home/claude/pop"]
import melody_p36 as M
import engine_p36 as _E
import pyphen, os
V2 = os.environ.get("V2") == "1"
if V2:                                            # version 2: lyric draft 5, the v2 bridge and the synth answer riff
    import lyric_v2 as L
    R2 = pickle.load(open("/home/claude/p36/melody_v2.pkl", "rb")); c = R2["pick"]
    M.LINES = R2["lines2"]; M.WORDS_OF = dict(L.SECTIONS)
    R = dict(order_fp=R2["order"], survivors=R2["survivors"], made=R2["built"], deaths=R2["deaths"], rerun=R2["rerun"])
else:
    import lyric as L
    R = pickle.load(open("/home/claude/p36/melody_main.pkl", "rb")); c = R["alive"][0]
BAR = M.BAR; NB = M.NBARS; QB = 118
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"a.m.,": ["a.", "m.,"], "microwave's": ["mi", "cro", "wave's"], "radio": ["ra", "di", "o"], "somewhere": ["some", "where"], "anyway,": ["an", "y", "way,"],
        "anyway.": ["an", "y", "way."], "anyway": ["an", "y", "way"], "july;": ["Ju", "ly;"], "july,": ["Ju", "ly,"], "july": ["Ju", "ly"], "july's,": ["Ju", "ly's,"],
        "every": ["ev", "ery"], "blinking": ["blink", "ing"], "dishes": ["dish", "es"], "counting": ["count", "ing"], "singing": ["sing", "ing"],
        "louder": ["loud", "er"], "before": ["be", "fore"], "only": ["on", "ly"], "watching": ["watch", "ing"], "keeping": ["keep", "ing"],
        "counter,": ["coun", "ter,"], "counter": ["coun", "ter"], "morning": ["morn", "ing"], "forgot": ["for", "got"], "again": ["a", "gain"],
        "freezer": ["freez", "er"], "dripping": ["drip", "ping"], "puddle": ["pud", "dle"], "neighbors'": ["neigh", "bors'"], "didn't": ["did", "n't"],
        "o'clock": ["o'", "clock"], "forever": ["for", "ev", "er"], "face-down": ["face", "down"]}
def split_words(text, sy):
    """the printed syllables of a line, matched one to one with the stress reading's syllables."""
    out = []
    ws = text.replace(" —", "—").split()
    for w in ws:
        n = len(M.syl(w.replace("-", " ").replace("—", "")))
        key = w.lower(); core = key.rstrip(",.;:—")
        if n <= 1: out.append((w, False)); continue
        parts = HFIX.get(key) or HFIX.get(core) or _PY.inserted(core).split("-")
        if len(parts) > n: parts = parts[:n - 1] + ["".join(parts[n - 1:])]
        while len(parts) < n: parts.append("_")
        tail = w[len(core):] if not (key in HFIX) else ""
        for j, p in enumerate(parts):
            t = p + (tail if j == n - 1 else "")
            if j == 0 and w[0].isupper(): t = t[0].upper() + t[1:]
            out.append((t, j < n - 1))
    assert len(out) == len(sy), (text, out, sy)
    return out
TEXT = {sec: [split_words(t, M.LINES[sec][i]) for i, (_, t) in enumerate(M.WORDS_OF[sec])] for sec in M.SUNG}

bars = []
for nm, kind, nb in M.FORM:
    for k in range(nb):
        b = M.BAR0[nm] + k
        bars.append(dict(sec=nm, kind=kind, k=k, n=nb, chord=M.CHORD[b], roman=M.ROMAN[M.CHORD[b]], start=b * BAR, len=BAR, qbpm=QB, key="E♭ major"))
lead = []
for n in c["notes"]:
    sec, i = n["line"].split(":"); i = int(i)
    t, hy = TEXT[sec][i][n["syl"]]
    lead.append(dict(on=n["on"], dur=n["dur"], midi=n["p"], sec=sec, line=i, syl=n["syl"], first=not n["slur"], text=t, hyph=hy,
                     stress=M.LINES[sec][i][n["syl"]][1], role=M.WORDS_OF[sec][i][0]))
ROOT = {k: v[0] for k, v in M.CH.items()}
def root_bass(ch): return 39 + (ROOT[ch] - 3) % 12          # E-flat 2 .. D3
def triad(ch, lo):
    out, p = [], lo
    while len(out) < 3:
        if p % 12 in M.CH[ch][1]: out.append(p)
        p += 1
    return out
D = dict(kick=36, snare=38, clap=39, hh=42, ohh=46, crash=49, tom=45, ride=51)
drums, bass, keys, gtr, pad, synth = [], [], [], [], [], []
def ev(lst, on, dur, p, vel, art=""): lst.append(dict(on=on, dur=dur, p=p if isinstance(p, list) else [p], vel=vel, art=art))
for bi, b in enumerate(bars):
    sec, kind, ch, st, k, n = b["sec"], b["kind"], b["chord"], b["start"], b["k"], b["n"]
    last_song_bar = bi == NB - 1
    full = kind == "Chorus" or (kind == "Outro" and not last_song_bar)
    big = sec == "Last Chorus"
    r = root_bass(ch)
    if last_song_bar:                                                    # the end: one hit on E-flat
        ev(drums, st, 3, [D["kick"], D["crash"]], 118); ev(bass, st, 36, [r, r + 12], 104)
        ev(keys, st, 36, triad(ch, 55) + [67], 92); ev(pad, st, 48, triad(ch, 63), 70); ev(gtr, st, 36, triad(ch, 60), 90)
        continue
    # ---- drums ----
    if kind == "Intro" and k < 2: pass
    elif kind == "Bridge" and k < 6:
        ev(drums, st, 3, D["kick"], 92); ev(drums, st + 24, 3, D["kick"], 86)
        if k >= 4: [ev(drums, st + e, 3, D["hh"], 54) for e in range(0, 48, 12)]
    elif kind == "Bridge":
        [ev(drums, st + e, 3, D["kick"], 100) for e in range(0, 48, 12)]
        [ev(drums, st + e, 3, D["snare"], min(120, 70 + (k - 6) * 24 + e // 2)) for e in range(0, 48, 6 if k == 6 else 3)]
    else:
        [ev(drums, st + e, 3, D["kick"], 108 if e == 0 else 100) for e in range(0, 48, 12)]
        for e in (12, 36): ev(drums, st + e, 3, [D["snare"], D["clap"]], 112 if full else 100)
        if full:
            for e in range(0, 48, 3):
                ev(drums, st + e, 3, D["ohh"] if e % 12 == 6 else D["hh"], (80 if e % 12 == 0 else 66 if e % 6 == 0 else 54) + (6 if big else 0))
        else:
            [ev(drums, st + e, 3, D["hh"], 72 if e % 12 == 0 else 60) for e in range(0, 48, 6)]
        if k == 0 and kind == "Chorus": ev(drums, st, 3, D["crash"], 116)
        if big and k % 4 == 0 and k: ev(drums, st, 3, D["crash"], 110)
        if kind == "Pre" and k == n - 1:
            drums[:] = [d for d in drums if not (st + 24 <= d["on"] < st + 48 and d["p"][0] in (D["snare"], D["hh"], D["ohh"]))]
            [ev(drums, st + e, 3, D["snare"], 84 + e) for e in range(24, 48, 3)]
    # ---- bass: disco octaves ----
    if kind == "Intro" and k < 2: pass
    elif kind == "Bridge" and k < 6: ev(bass, st, 46, r, 92)
    elif kind in ("Verse",) or (kind == "Bridge"):
        for e in range(0, 48, 12): ev(bass, st + e, 6, r, 96); ev(bass, st + e + 6, 5, r + 12, 82)
    else:
        for e in range(0, 48, 6): ev(bass, st + e, 5, r if e % 12 == 0 else r + 12, (104 if e % 12 == 0 else 90) + (4 if big else 0))
    # ---- keys: electric piano stabs ----
    up = triad(ch, 60)
    if kind == "Bridge" and k < 6: ev(keys, st, 46, triad(ch, 55) + [triad(ch, 67)[0]], 70, "held")
    elif kind == "Verse" or kind == "Intro":
        for e in (18, 42): ev(keys, st + e, 5, up, 86, "stab")
        if kind == "Intro" and k < 2: ev(keys, st, 5, up, 90, "stab")
    else:
        for e in (6, 18, 30, 42): ev(keys, st + e, 5, up, 92 if full else 84, "stab")
    # ---- guitar: muted sixteenths, the chord on each 'and' ----
    if (full or sec == "Verse 2" or kind == "Pre") and not (kind == "Bridge" and k < 6):
        g = triad(ch, 64)
        for e in range(0, 48, 3):
            if e % 12 == 6: ev(gtr, st + e, 3, g, 88 if full else 78, "chord")
            else: ev(gtr, st + e, 3, [g[0]], 36, "ghost")
    # ---- pad ----
    if kind in ("Pre", "Chorus", "Bridge", "Outro") and sec != "Pre 1" or (sec == "Pre 1"):
        lo = 67 if big else 55
        ev(pad, st, 47, triad(ch, lo), 60 if kind != "Bridge" else 66, "pad")
# ---- the synth hook: the intro's last two bars and the outro ----
hook = [n for n in c["notes"] if n["line"] == "Chorus 1:0"]
h0 = M.BAR0["Chorus 1"] * BAR
def put_hook(at_bar):
    for j, n in enumerate(hook):
        d = n["dur"] if j < len(hook) - 1 else 24
        ev(synth, at_bar * BAR + (n["on"] - h0), d, n["p"] + 12, 88, "hook")
if not V2:
    put_hook(2); put_hook(M.BAR0["Outro"] + 1)
else:                                             # 205: the riff answers each chorus line in its hold; four times in the intro, three in the outro
    import melody_v2_p36 as V
    _, rons, rsteps = R2["riff"][:3]
    def put_riff(bar):
        ch = M.CHORD[bar]; ps = V.riff_pitches(rsteps, ch)
        for j, (t, p) in enumerate(zip(rons, ps)):
            nxt = rons[j + 1] if j + 1 < len(rons) else 24
            ev(synth, bar * BAR + 24 + t, max(3, nxt - t), p, 90, "riff")
    for bar in range(0, 4): put_riff(bar)
    for sl in R2["riff_slots"]: put_riff(sl["bar"])
    for bar in range(M.BAR0["Outro"], M.BAR0["Outro"] + 3): put_riff(bar)
synth = [s for s in synth if s["on"] < (NB - 1) * BAR]
for lst in (drums, bass, keys, gtr, pad, synth): lst.sort(key=lambda e: (e["on"], e["p"][0]))
plan = [(nm, nb, M.BAR0[nm], "4/4") for nm, _, nb in M.FORM]
secs = NB * 4 * 60 / QB
rec = dict(title=L.TITLE, nbars=NB, bars=bars, plan=plan, lead=lead, drums=drums, bass=bass, keys=keys, gtr=gtr, pad=pad, synth=synth,
           slot="twelfth of a beat", bar=BAR, qbpm=QB, seconds=secs, tw_sec=60 / QB / 12, fp=c["fp"], order_fp=R["order_fp"], survivors=R["survivors"],
           built=R["made"], deaths=dict(R["deaths"]), meas={k: (float(v) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()},
           plans=c["meta"]["plans"], shifts={f"{a} {b + 1}": v for (a, b), v in c["meta"]["shifts"].items()}, hand_edits=[], rerun=R["rerun"], text=TEXT)
rec["version"] = 2 if V2 else 1
pickle.dump(rec, open("/home/claude/p36/song_record_v2.pkl" if V2 else "/home/claude/p36/song_record.pkl", "wb"))
print(NB, "bars,", f"{secs:.0f} s ({int(secs // 60)}:{int(round(secs % 60)):02d});", len(lead), "sung;", len(drums), "drums;", len(bass), "bass;",
      len(keys), "keys;", len(gtr), "guitar;", len(pad), "pad;", len(synth), "synth; fp", rec["fp"])
