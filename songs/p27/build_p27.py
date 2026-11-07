"""Build the song record for 'Either Or' from the frozen melody (melody_final.pkl: ranking #1, no hand edits). One male tenor; angular art
rock. Times in EIGHTHS at q = 132: 5/4 bars (10 eighths, felt 3+2) in the verses, intro, break and build; 4/4 bars (8 eighths) in the
refrains and the outro. D Dorian (B natural) against F major (B flat).
  guitar 1   (clean, bright) the arpeggio figure in eighths, grouped 3+2: root-third-fifth, then fifth-third; in the refrains, the chord
             struck on 1 and 3 and left to ring (the upper voicing)
  guitar 2   (clean, darker; in from intro bar 3, out for verse 1) the answer: dyads on the offbeats of the 3-group and on beat 5 -- the two guitars interlock; in the break they
             hocket (guitar 1 on the even eighths, guitar 2 on the odd); in the refrains, the lower voicing in driving eighths
  bass       (fretless) the 5/4 line: root on 1 (dotted quarter), the root again, the fifth on 3, the octave on 4, an approach on 5; in
             the refrains, driving eighths with octave pops on the 'and' of 2 and 4
  organ      (church organ) the drone: F and C under every refrain; a swell through the build; D and A in the outro
  drums      5/4: kick on 1 and 4, snare on 3 and 5, eighth hats accented on 1 and 4 (the intro and verse 1: hats on 1 and 4 only); the refrains: kick 1 and 3, snare 2 and 4, ride,
             crash at the top; the break: toms on 1 and 4; the build: kick, then snare eighths rising, a fill into refrain 3
  the stop   after 'you can't keep SCORE' (the Bb4) the whole band stops: the last line is the voice alone. Then the outro: the organ's D-A
             drone and guitar 1's open D and A ringing -- the last chord a bare fifth, neither major nor minor."""
import pickle, sys
sys.path[:0] = ["/home/claude/p27"]
import melody_p27 as M, lyric as L
c = pickle.load(open("/home/claude/p27/melody_final.pkl", "rb"))
R = pickle.load(open("/home/claude/p27/melody_result.pkl", "rb"))
QB = 112 * 0 + 132
bars = []
for i, b in enumerate(M.BARS):
    k = sum(1 for x in M.BARS[:i] if x["sec"] == b["sec"])
    bars.append(dict(sec=b["sec"], meter=b["meter"], chord=b["chord"], start=b["start"], len=b["len"], qbpm=QB, k=k,
                     key="F major" if b["sec"].startswith("Refrain") else "D Dorian", build=b["sec"] == "Build",
                     instrumental=b["sec"] in ("Intro", "Break", "Build", "Outro")))
lead = []
for s in M.SINGS:
    for o, d, p, x, li in c[s]:
        lead.append(dict(on=o, dur=d, midi=p, syl=x, sec=s, line=li, role=M.SECS[s][li]["role"], meter=M.SECS[s][li]["meter"], singer="him"))
lead.sort(key=lambda n: n["on"])
TOT = M.TOTAL; secs = TOT * 60 / QB / 2
plan = []
for sec, met, scale, lines, chs in M.FORM:
    b0 = next(i for i, b in enumerate(bars) if b["sec"] == sec); nb = sum(1 for b in bars if b["sec"] == sec)
    plan.append((sec, nb, b0, met))
ROOT = {"Dm": 2, "G": 7, "F": 5, "Am": 9, "C": 0, "Bb": 10, "Gm": 7, "D5": 2, "Em": 4}
def at_or_above(pc, lo):
    p = lo
    while p % 12 != pc: p += 1
    return p
def voicing(ch, lo, n=3):
    out, p = [], lo
    while len(out) < n:
        if p % 12 in M.CH[ch]: out.append(p)
        p += 1
    return out
STOP_AT = None
r4 = next(b for b in bars if b["sec"] == "Refrain 4" and b["k"] == 6)["start"]   # refrain 4, bar 7: the band stops
g1, g2, bass, org, drums = [], [], [], [], []
D = dict(kick=36, snare=38, hh=42, ohh=46, ride=51, crash=49, tom=45, tomf=41)
for bi, b in enumerate(bars):
    sec, ch, st, k, ln = b["sec"], b["chord"], b["start"], b["k"], b["len"]
    if st >= r4 and sec == "Refrain 4": continue                         # the stop
    nxt = bars[bi + 1]["chord"] if bi + 1 < len(bars) else ch
    r = at_or_above(ROOT[ch], 38)                                          # bass root D2-C#3
    five = b["meter"] == "5/4"
    up = voicing(ch, 62); lo_ = voicing(ch, 52, 2)
    if sec == "Outro":
        if k == 0:
            org.append(dict(on=st, dur=32, p=[50, 57], vel=70, art="drone"))
            g1.append(dict(on=st, dur=32, p=[62, 69], vel=60, art="ring"))
            bass.append(dict(on=st, dur=32, p=[38], vel=64, art=""))
        continue
    # ---- guitars ----
    if five:
        if sec == "Break":
            for e in range(10):
                tgt = g1 if e % 2 == 0 else g2
                tgt.append(dict(on=st + e, dur=1, p=[up[(e // 2) % 3]] if e % 2 == 0 else lo_, vel=86 if e in (0, 6) else 74, art=""))
        elif sec == "Build":
            v = 60 + 4 * k
            g1 += [dict(on=st + e, dur=1, p=up, vel=min(110, v + (8 if e in (0, 6) else 0)), art="") for e in range(0, 10, 1 if k >= 4 else 2)]
        else:
            if not (sec == "Intro" and False):
                fig = [0, 1, 2, 0, 1, 2, 1, 0, 1, 2]
                g1 += [dict(on=st + e, dur=1, p=[up[fig[e]]], vel=(74 if e in (0, 6) else 62) - (6 if sec == "Intro" and k < 2 else 0), art="") for e in range(10)]
            if not (sec == "Intro" and k < 2) and sec != "Verse 1":       # verse 1: guitar 1 alone over bass and drums
                g2 += [dict(on=st + e, dur=1, p=lo_, vel=70, art="") for e in (1, 4, 8)]
    else:
        g1 += [dict(on=st, dur=4, p=voicing(ch, 60, 4), vel=92, art="ring"), dict(on=st + 4, dur=4, p=voicing(ch, 60, 4), vel=84, art="ring")]
        g2 += [dict(on=st + e, dur=1, p=voicing(ch, 48, 3), vel=88 if e % 4 == 0 else 78, art="") for e in range(8)]   # the refrain drives: eighths under the ringing chord
    # ---- bass ----
    if sec == "Intro" and k < 4: pass
    elif five:
        appr = at_or_above(ROOT[nxt], 38); appr = appr - 1 if appr - 1 != r else appr + 2
        if sec == "Build" and k < 2: bass.append(dict(on=st, dur=10, p=[r], vel=70, art=""))
        else: bass += [dict(on=st, dur=3, p=[r], vel=94, art=""), dict(on=st + 3, dur=1, p=[r], vel=80, art=""), dict(on=st + 4, dur=2, p=[r + 7], vel=84, art=""),
                       dict(on=st + 6, dur=2, p=[r + 12], vel=90, art=""), dict(on=st + 8, dur=2, p=[appr], vel=82, art="")]
    else:
        bass += [dict(on=st + e, dur=1, p=[r + (12 if e in (3, 7) else 0)], vel=96 if e % 4 == 0 else 84, art="") for e in range(8)]
    # ---- organ ----
    if sec.startswith("Refrain"):
        if k == 0: org.append(dict(on=st, dur=64 if sec != "Refrain 4" else 48, p=[41, 48], vel=72, art="drone"))
    elif sec == "Build":
        org.append(dict(on=st, dur=10, p=voicing(ch, 50, 3), vel=40 + 6 * k, art="swell"))
    # ---- drums ----
    if sec == "Intro" and k < 4: continue
    if five:
        if sec == "Build":
            if k < 2: drums += [dict(on=st + e, dur=1, p=[D["hh"]], vel=56 + 2 * e, art="") for e in range(0, 10, 2)] + [dict(on=st, dur=1, p=[D["kick"]], vel=90, art="")]
            elif k < 6: drums += [dict(on=st + e, dur=1, p=[D["kick"]] if e in (0, 6) else [D["snare"]], vel=70 + 5 * k, art="") for e in (0, 4, 6, 8)] + \
                                 [dict(on=st + e, dur=1, p=[D["hh"]], vel=64, art="") for e in range(0, 10, 2)]
            else: drums += [dict(on=st + e, dur=1, p=[D["snare"]] if e % 3 else [D["tom"]], vel=min(124, 80 + 4 * e + 6 * (k - 6)), art="") for e in range(10)]
        else:
            drums += [dict(on=st + e, dur=1, p=[D["kick"]], vel=100, art="") for e in (0, 6)]
            drums += [dict(on=st + e, dur=1, p=[D["snare"]], vel=96, art="") for e in (4, 8)]
            drums += [dict(on=st + e, dur=1, p=[D["hh"]], vel=76 if e in (0, 6) else 58, art="") for e in ((0, 6) if sec in ("Verse 1", "Intro") else range(0, 10, 2))]
            if sec == "Break": drums += [dict(on=st + e, dur=1, p=[D["tomf"]], vel=96, art="") for e in (0, 6)]
    else:
        drums += [dict(on=st + e, dur=1, p=[D["kick"]], vel=104, art="") for e in (0, 4)]
        drums += [dict(on=st + e, dur=1, p=[D["snare"]], vel=100, art="") for e in (2, 6)]
        drums += [dict(on=st + e, dur=1, p=[D["ride"]], vel=78 if e % 2 == 0 else 66, art="") for e in range(8)]
        if k == 0: drums.append(dict(on=st, dur=1, p=[D["crash"]], vel=112, art=""))
        if sec == "Refrain 4" and k == 5: drums.append(dict(on=st, dur=1, p=[D["crash"]], vel=118, art=""))
rec = dict(title=L.TITLE, nbars=len(bars), bars=bars, plan=plan, lead=lead, harm=[], g1=g1, g2=g2, bass=bass, organ=org, drums=drums,
           total_eighths=TOT, slot="eighth", seconds=secs, singers=dict(him=M.HIM), singer_by_sec=L.SINGER, stop_at=r4,
           meas={k_: (float(v) if isinstance(v, (int, float)) else v) for k_, v in c["meas"].items()}, hand_edits=c["hand"], from_fp=c["from"],
           fp=c["fp"], order_fp=R["order_fp"], survivors=R["survivors"], built=R["made"], attempts=R["tries"], deaths=dict(R["deaths"].most_common()),
           by_construction=R["by_construction"], qbpm={"5/4": QB, "4/4": QB}, slot_sec=60 / QB / 2, plans=c["plans"], cell_log=c["cell_log"])
pickle.dump(rec, open("/home/claude/p27/song_record.pkl", "wb"))
print(rec["nbars"], "bars,", f"{secs:.0f} s ({int(secs//60)}:{int(round(secs%60)):02d});", len(lead), "sung;", len(g1), "gtr1;", len(g2), "gtr2;", len(bass), "bass;",
      len(org), "organ;", len(drums), "drums; fp", rec["fp"])
