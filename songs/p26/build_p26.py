"""Build the song record for 'Five-Oh-One' from the frozen melody (melody_final.pkl: ranking #1, no hand edits). One male tenor and a
gang; a funk-pop band. Times in SIXTEENTHS (16 a bar of 4/4) at q = 112; Eb major to the lift, F major from chorus 3.
  drums      intro, choruses, hooks: kick on 1, the 'a' of 2 and 3; snare 2 and 4; sixteenth hats (open on the 'and' of 4);
             crash into each chorus. Verses: eighth hats, kick 1 and 3. Pre-choruses: sixteenth hats and a snare fill in the last bar.
             Breakdown: the kit drops out -- kick on 1 only; claps answer each CLAP. Lift: a sixteenth snare build over the two bars of C.
  bass       a sixteenth funk line: the root on 1, the root again on the 'a' of 1, the octave on the 'and' of 2, the root on 3, the
             fifth and octave pops, a chromatic approach into the next bar's root; the breakdown busier, the verses lighter.
  guitar     the sixteenth 'chicken scratch': muted ghosts on every sixteenth, the chord stabbed on each 'and' (top three notes).
  keys       electric piano: the chord held through each bar in the pre-choruses, choruses and hooks; out in the verses and breakdown.
  horns      stabs on 1 and the 'and' of 2 in the choruses; the hook's chant played with the voice in the hooks; the intro plays the
             chant alone (27.21's quote kind, v65 fix 21); the final hit on F.
  claps      2 and 4 in the hooks and the last choruses; three after each CLAP in the breakdown.
  gang       (hey!) and (go!) after each hook line; the title cell shouted with him in choruses 3 and 4; the lift's FIVE-OH-ONE is
             the gang's line in the voice part.
  the arc    the intro opens on guitar and horns alone (drums and bass from bar 3); the pre-choruses keep eighth hats until the fill;
             choruses 3 and 4 add open hats, a crash every two bars, held horn chords and the gang."""
import pickle, sys
sys.path[:0] = ["/home/claude/p26"]
import melody_p26 as M, lyric as L
c = pickle.load(open("/home/claude/p26/melody_final.pkl", "rb"))
R = pickle.load(open("/home/claude/p26/melody_result.pkl", "rb"))
QB = 112
FKEY = ("Chorus 3", "Chorus 4", "Hook 3", "Outro", "Ending")
bars = []
for i, b in enumerate(M.BARS):
    k = sum(1 for x in M.BARS[:i] if x["sec"] == b["sec"])
    bars.append(dict(sec=b["sec"], meter="4/4", chord=b["chord"], start=b["start"], len=b["len"], qbpm=QB, k=k,
                     key="F major" if b["sec"] in FKEY else "Eb major", build=b["sec"] in ("Pre 1", "Pre 2", "Lift"),
                     instrumental=b["sec"] in ("Intro", "Ending")))
lead = []
for s in M.SINGS:
    for o, d, p, x, li in c[s]:
        lead.append(dict(on=o, dur=d, midi=p, syl=x, sec=s, line=li, role=M.SECS[s][li]["role"], meter="4/4",
                         singer="gang" if (s, li) == ("Lift", 1) else "him"))
lead.sort(key=lambda n: n["on"])
TOT = M.TOTAL; secs = TOT * 60 / QB / 4
plan = []
for sec, met, scale, lines, chs in M.FORM:
    b0 = next(i for i, b in enumerate(bars) if b["sec"] == sec); nb = sum(1 for b in bars if b["sec"] == sec)
    plan.append((sec, nb, b0, "4/4"))
ROOT = {"Eb": 3, "Ab": 8, "Bb": 10, "Cm": 0, "Gm": 7, "C": 0, "F": 5, "Dm": 2}
def at_or_above(pc, lo):
    p = lo
    while p % 12 != pc: p += 1
    return p
def triad(ch, lo):
    out, p = [], lo
    while len(out) < 3:
        if p % 12 in M.CH[ch]: out.append(p)
        p += 1
    return out
FULL = ("Intro", "Chorus 1", "Chorus 2", "Chorus 3", "Chorus 4", "Hook 1", "Hook 2", "Hook 3", "Outro")
drums, bass, gtr, keys, horns, claps, gang = [], [], [], [], [], [], []
D = dict(kick=36, snare=38, hh=42, ohh=46, crash=49, clap=39, tom=45)
for bi, b in enumerate(bars):
    sec, ch, st, k = b["sec"], b["chord"], b["start"], b["k"]
    nsec = sum(1 for x in bars if x["sec"] == sec)
    last = sec == "Ending" and k == 1
    nxt = bars[bi + 1]["chord"] if bi + 1 < len(bars) else ch
    r = at_or_above(ROOT[ch], 28)                                  # bass root E1-D#2
    if sec == "Ending":
        if k == 0:
            hit = [at_or_above(5, 29), at_or_above(5, 41)]
            bass.append(dict(on=st, dur=8, p=hit, vel=100, art=""))
            drums += [dict(on=st, dur=1, p=[D["kick"], D["crash"]], vel=118, art="")]
            horns.append(dict(on=st, dur=6, p=triad("F", 65) + [77], vel=104, art=""))
            keys.append(dict(on=st, dur=12, p=triad("F", 53) + [65], vel=70, art=""))
            gtr.append(dict(on=st, dur=8, p=triad("F", 60), vel=90, art=""))
        continue
    # ---- drums ----
    if sec == "Intro" and k < 2:
        pass                                                         # the intro opens on the guitar and the horns' chant alone
    elif sec == "Breakdown":
        drums.append(dict(on=st, dur=1, p=[D["kick"]], vel=96, art=""))
    elif sec == "Lift":
        if k < 2: drums += [dict(on=st + e, dur=1, p=[D["hh"]], vel=60, art="") for e in range(0, 16, 2)] + [dict(on=st, dur=1, p=[D["kick"]], vel=96, art="")]
        else: drums += [dict(on=st + e, dur=1, p=[D["snare"]], vel=min(122, 64 + 2 * ((k - 2) * 16 + e)), art="") for e in range(16)]
    else:
        full = sec in FULL
        kick = [0, 7, 8] if full or sec.startswith("Pre") else [0, 8]
        drums += [dict(on=st + e, dur=1, p=[D["kick"]], vel=104 if e in (0, 8) else 92, art="") for e in kick]
        drums += [dict(on=st + e, dur=1, p=[D["snare"]], vel=108 if full else 96, art="") for e in (4, 12)]
        big = sec in ("Chorus 3", "Chorus 4")
        if full and sec != "Intro":
            drums += [dict(on=st + e, dur=1, p=[D["ohh"] if (e == 14 or (big and e % 4 == 2)) else D["hh"]], vel=(78 if e % 4 == 0 else 62) + 6, art="") for e in range(16)]
        else:
            drums += [dict(on=st + e, dur=1, p=[D["hh"]], vel=70 if e % 4 == 0 else 58, art="") for e in range(0, 16, 2)]
        if (k == 0 and sec.startswith("Chorus")) or (big and k % 2 == 0): drums.append(dict(on=st, dur=1, p=[D["crash"]], vel=112, art=""))
        if sec.startswith("Pre") and k == nsec - 1:
            drums = [d_ for d_ in drums if not (st + 8 <= d_["on"] < st + 16)]
            drums += [dict(on=st + e, dur=1, p=[D["snare"] if e % 2 == 0 else D["tom"]], vel=80 + 3 * (e - 8), art="") for e in range(8, 16)]
    # ---- claps ----
    if sec in ("Hook 1", "Hook 2", "Hook 3", "Chorus 3", "Chorus 4", "Outro"):
        claps += [dict(on=st + e, dur=1, p=[D["clap"]], vel=100, art="") for e in (4, 12)]
    # ---- bass ----
    o12 = r + 12; f5 = r + 7
    appr = at_or_above(ROOT[nxt], 28); appr = appr - 1 if appr - 1 != r else appr + 2
    if sec in ("Verse 1", "Verse 2"):
        pat = [(0, 3, r), (6, 1, o12), (8, 3, r), (14, 2, appr)]
    elif sec == "Breakdown":
        pat = [(0, 2, r), (3, 1, r), (6, 1, o12), (7, 1, r), (8, 2, r), (10, 1, f5), (11, 1, o12), (13, 1, f5), (14, 1, r), (15, 1, appr)]
    elif sec == "Lift" and k >= 2:
        pat = [(e, 1, r if e % 4 else o12) for e in range(0, 16, 2)]
    else:
        pat = [(0, 2, r), (3, 1, r), (6, 1, o12), (8, 2, r), (10, 1, f5), (11, 1, o12), (14, 2, appr)]
    if sec == "Intro" and k < 2: pat = []
    bass += [dict(on=st + e, dur=d, p=[p], vel=(100 if e in (0, 8) else 86) + (6 if sec in FULL else 0), art="") for e, d, p in pat]
    # ---- guitar: the scratch ----
    if sec not in ("Breakdown",) and not (sec == "Lift" and k >= 2):
        up = triad(ch, 60)
        for e in range(16):
            if e % 4 == 2: gtr.append(dict(on=st + e, dur=1, p=up, vel=92 if sec in FULL else 80, art="stab"))
            elif sec not in ("Verse 1",) or k >= 2: gtr.append(dict(on=st + e, dur=1, p=[up[0]], vel=34, art="ghost"))
    elif sec == "Lift":
        gtr.append(dict(on=st, dur=16, p=triad(ch, 60), vel=72, art="ring"))
    # ---- keys ----
    if sec.startswith(("Pre", "Chorus", "Hook", "Outro")) or sec == "Lift":
        keys.append(dict(on=st, dur=16, p=triad(ch, 53), vel=58 if sec.startswith("Pre") else 66, art=""))
    # ---- horns: stabs in the choruses ----
    if sec.startswith("Chorus"):
        hv = triad(ch, 63)
        horns += [dict(on=st, dur=2, p=hv, vel=100, art="stab"), dict(on=st + 6, dur=1, p=hv, vel=92, art="stab")]
        if sec in ("Chorus 3", "Chorus 4"):                       # the last choruses: the horns also hold the chord under the stabs
            horns.append(dict(on=st + 8, dur=8, p=triad(ch, 55), vel=78, art="pad"))
# ---- horns: the chant (the intro alone; with the voice in the hooks and the outro) ----
def chant(at, tr, hold=8):
    out = []
    for k_, ((o, d), p) in enumerate(zip(M.HOOK_RH, M.HOOK_P)):
        if k_ == len(M.HOOK_RH) - 1: d = hold
        out.append(dict(on=at + o, dur=d, p=[p + tr + 12], vel=100, art="", src="chant"))
    return out
intro_at = next(b["start"] for b in bars if b["sec"] == "Intro")
horns += chant(intro_at, 0) + chant(intro_at + 32, 0)
for sec, tr in (("Hook 1", 0), ("Hook 2", 0), ("Hook 3", 2)):
    for ln in M.SECS[sec]: horns += chant(ln["at"], tr)
horns += chant(M.SECS["Outro"][0]["at"], 2, hold=14)
# ---- gang: (hey!) and (go!) after each hook line; the breakdown's claps ----
for sec in ("Hook 1", "Hook 2", "Hook 3"):
    for ln, word in zip(M.SECS[sec], ("hey", "go")):
        tr = 2 if sec == "Hook 3" else 0
        gang.append(dict(on=ln["at"] + 26, dur=2, p=[67 + tr, 70 + tr], vel=110, art="", word=word))
for n in lead:                                                     # the last choruses: the gang shouts the title cell with him
    if n["sec"] in ("Chorus 3", "Chorus 4") and n["line"] in (0, 1, 3) and n["on"] - M.SECS[n["sec"]][n["line"]]["at"] < 6:
        gang.append(dict(on=n["on"], dur=n["dur"], p=[n["midi"] - 12, n["midi"]], vel=96, art="", word=n["syl"][0]))
for n in lead:
    if n["sec"] == "Breakdown" and n["syl"][0] == "clap":
        claps += [dict(on=n["on"] + 2 + 2 * j, dur=1, p=[D["clap"]], vel=112, art="") for j in range(3)]
horns.sort(key=lambda e: e["on"])
BIG = {i for i, b in enumerate(bars) if b["sec"] in ("Chorus 3", "Chorus 4", "Hook 3")}   # the key change plays harder: every part up
def bar_index(o): return next(i for i, b in enumerate(bars) if b["start"] <= o < b["start"] + b["len"])
for lst, up in ((drums, 8), (bass, 6), (horns, 8), (gtr, 6), (keys, 8), (claps, 6)):
    for e in lst:
        if bar_index(e["on"]) in BIG and e.get("art") != "ghost": e["vel"] = min(127, e["vel"] + up)
rec = dict(title=L.TITLE, nbars=len(bars), bars=bars, plan=plan, lead=lead, harm=[], drums=drums, bass=bass, gtr=gtr, keys=keys, horns=horns,
           claps=claps, gang=gang, total_slots=TOT, slot="sixteenth", seconds=secs, singers=dict(him=M.HIM), singer_by_sec=L.SINGER,
           meas={k: (float(v) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()}, hand_edits=c["hand"], from_fp=c["from"],
           fp=c["fp"], order_fp=R["order_fp"], survivors=R["survivors"], built=R["made"], attempts=R["tries"], deaths=dict(R["deaths"].most_common()),
           by_construction=R["by_construction"], qbpm={"4/4": QB}, slot_sec=60 / QB / 4, plans=c["plans"], cell_log=c["cell_log"])
pickle.dump(rec, open("/home/claude/p26/song_record.pkl", "wb"))
print(rec["nbars"], "bars,", f"{secs:.0f} s ({int(secs//60)}:{int(round(secs%60)):02d});", len(lead), "sung;", len(drums), "drums;", len(bass), "bass;",
      len(gtr), "guitar;", len(keys), "keys;", len(horns), "horns;", len(claps), "claps;", len(gang), "gang; fp", rec["fp"])
