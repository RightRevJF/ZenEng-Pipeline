"""Build the song record for 'Nothing On' from the frozen melody (melody_final.pkl: ranking #1, no hand edits). One female pop lead, a
backing echo, and a disco-funk band. Times in SIXTEENTHS (16 a bar of 4/4) at q = 116; F major signature, the loop never on F until the bridge.
  The three departures (the 8 Nov research: familiar frame, two or three moves):
    the withheld home chord -- verse Gm7-Am7, pre Bbmaj7-C, chorus Bbmaj7-Am7 / Gm7-C; F arrives only with the power in the bridge;
    the power cut -- at the end of each pre-chorus the band bends down (a tape stop) on 'breathe'/'are' and is silent for the chorus's
      first bar: she sings 'nothing on, nothing on' alone and the band slams back in on bar 2 with a crash; the bridge's last bar cuts
      the same way on 'hold my breath' into the last chorus;
    the off-beat hooks -- every 'nothing on' starts on the and of beat 1.
  drums      live-sounding kit. Verse: kick 1, the a of 2, 3; snare 2 and 4 with ghost notes; sixteenth hats. Pre: four on the floor,
             open hats on the off-beats, a snare build in the last bar to beat 3. Chorus and post: four on the floor, snare and handclaps
             on 2 and 4, sixteenth hats with the open hat on the off-beats, crash on the re-entry; bongos in the posts; a
             tambourine in eighths in chorus 2, in sixteenths in the last chorus. Bridge: out for two lines (the dark house), kick and hats return with line
             3, a snare roll up to the stop.
  bass       finger P-bass: the verse's syncopated root line; disco octaves from the pre-chorus; the bridge in whole notes then eighths.
  gtr        muted funk guitar ('chank'): off-beat eighths in the verses, the sixteenth pattern from the pre-chorus.
  riff       clean single-note guitar: the title cell with sixteenth fills (A4 G4 C5 | C5 A4 E4 ...) -- the intro, verse 2's gaps and the
             outro; the singer takes it over in the chorus (the research: an intro hook that returns in the vocal).
  keys       Rhodes: held chords in the verses and the bridge, syncopated stabs in the choruses; it alone stays for the last line.
  horns      brass section: two stabs (beat 4 and its and) in every chorus and post bar where the singer holds (a third, on
             the and of 2, in the last chorus); a swell in pre 2.
  hum        a low pad on F (the fridge's hum) under the bridge's first two lines -- the power coming back.
  bv         the backing echo '(nothing on)' before 'nothing on but you'; in the last chorus a third under every title line."""
import pickle, sys
sys.path[:0] = ["/home/claude/p31"]
import melody_p31 as M, lyric as L
c = pickle.load(open("/home/claude/p31/melody_final.pkl", "rb"))
R = pickle.load(open("/home/claude/p31/melody_result.pkl", "rb"))
QB = 116
bars = []
for i, b in enumerate(M.BARS):
    k = sum(1 for x in M.BARS[:i] if x["sec"] == b["sec"])
    bars.append(dict(sec=b["sec"], meter="4/4", chord=b["chord"], start=b["start"], len=b["len"], qbpm=QB, k=k, key="F major",
                     build=(b["sec"] == "Bridge" and k >= 4), instrumental=b["sec"] in ("Intro", "Outro")))
lead = []
for s in M.SINGS:
    for o, d, p, x, li in c[s]:
        lead.append(dict(on=o, dur=d, midi=p, syl=x, sec=s, line=li, role=M.SECS[s][li]["role"], meter="4/4", singer="her"))
lead.sort(key=lambda n: n["on"])
TOT = M.TOTAL; secs = TOT * 60 / QB / 4
plan = []
for sec, met, scale, lines, chs in M.FORM:
    b0 = next(i for i, b in enumerate(bars) if b["sec"] == sec); nb = sum(1 for b in bars if b["sec"] == sec)
    plan.append((sec, nb, b0, "4/4"))
ROOT = {"Gm7": 7, "Am7": 9, "Bbmaj7": 10, "C": 0, "F": 5, "Am": 9, "Bb": 10}
def at_or_above(pc, lo):
    p = lo
    while p % 12 != pc: p += 1
    return p
def tones(ch, lo, hi): return [p for p in range(lo, hi + 1) if p % 12 in M.CH[ch]]
D = dict(kick=36, snare=38, ghost=38, clap=39, hh=42, ohh=46, crash=49, tl=45, tm=47, th=50, tamb=54, bhi=60, blo=61)
drums, bass, gtr, riff, keys, horns, hum, bv = [], [], [], [], [], [], [], []
FULLS = ("Chorus 1", "Chorus 2", "Chorus 3", "Post 1", "Post 2", "Post 3")
def sec_bars(s): return [b for b in bars if b["sec"] == s]
def is_cut(b): return b["sec"].startswith("Chorus") and b["k"] == 0                      # the power cut: the chorus's first bar
def pre_end(b): return b["sec"].startswith("Pre") and b["k"] == 3                         # the tape stop: band out from beat 3
def bri_stop(b): return b["sec"] == "Bridge" and b["k"] == 7                               # one hit on 1, then out
def strip(b): return b["sec"] == "Post 3" and b["k"] >= 4                                  # the last line: Rhodes, bass, voice
CUTS = []
for bi, b in enumerate(bars):
    sec, ch, st, k = b["sec"], b["chord"], b["start"], b["k"]
    nsec = sum(1 for x in bars if x["sec"] == sec)
    last = sec == "Outro"
    if pre_end(b): CUTS.append(dict(kind="tape stop", start=st + 8, silent_from=st + 12, back=st + 32))
    if bri_stop(b): CUTS.append(dict(kind="stop", start=st, silent_from=st + 4, back=st + 32))
    if is_cut(b): continue                                                                   # silence: the voice alone
    lim = 12 if pre_end(b) else (4 if bri_stop(b) else 16)
    def keep(evs): return [dict(e, dur=min(e["dur"], lim - (e["on"] - st))) for e in evs if e["on"] - st < lim]
    r = at_or_above(ROOT[ch], 36)
    f5 = r + 7
    # ---- drums ----
    dr = []
    if sec == "Intro" and k < 2:
        dr += [dict(on=st + e, dur=1, p=[D["hh"]], vel=54 if e % 4 else 66, art="") for e in range(16)]
        if k == 1: dr += [dict(on=st + e, dur=1, p=[D["snare"]], vel=70 + 6 * j, art="") for j, e in enumerate((12, 13, 14, 15))]
    elif sec in ("Intro", "Verse 1", "Verse 2"):
        dr += [dict(on=st + e, dur=1, p=[D["kick"]], vel=96 if e != 7 else 82, art="") for e in (0, 7, 8)]
        dr += [dict(on=st + e, dur=1, p=[D["snare"]], vel=100, art="") for e in (4, 12)]
        dr += [dict(on=st + e, dur=1, p=[D["ghost"]], vel=38, art="ghost") for e in (7, 10, 15)]
        dr += [dict(on=st + e, dur=1, p=[D["hh"]], vel=(64 if e % 4 == 0 else (52 if e % 2 == 0 else 40)), art="") for e in range(16)]
    elif sec.startswith("Pre"):
        dr += [dict(on=st + e, dur=1, p=[D["kick"]], vel=98, art="") for e in (0, 4, 8, 12)]
        dr += [dict(on=st + e, dur=1, p=[D["snare"]], vel=100, art="") for e in (4, 12)]
        dr += [dict(on=st + e, dur=1, p=[D["ohh"] if e % 4 == 2 else D["hh"]], vel=66 if e % 4 == 2 else 50, art="") for e in range(0, 16, 2)]
        if k == 3: dr += [dict(on=st + e, dur=1, p=[D["snare"]], vel=66 + 3 * e, art="") for e in range(0, 12, 2)]
    elif sec == "Bridge":
        if k >= 4: dr += [dict(on=st + e, dur=1, p=[D["kick"]], vel=86 + 2 * k, art="") for e in (0, 4, 8, 12)]
        if k >= 4: dr += [dict(on=st + e, dur=1, p=[D["hh"]], vel=46 + 3 * k, art="") for e in range(0, 16, 2)]
        if k == 6: dr += [dict(on=st + e, dur=1, p=[D["snare"]], vel=60 + 3 * e, art="") for e in range(0, 16, 2)]
        if k == 7: dr += [dict(on=st, dur=1, p=[D["crash"]], vel=112, art=""), dict(on=st, dur=1, p=[D["kick"]], vel=110, art=""),
                          dict(on=st, dur=1, p=[D["snare"]], vel=108, art="")]
    elif sec in FULLS and not strip(b):
        big = sec == "Chorus 3" or sec == "Post 3"
        dr += [dict(on=st + e, dur=1, p=[D["kick"]], vel=104 + (4 if big else 0), art="") for e in (0, 4, 8, 12)]
        dr += [dict(on=st + e, dur=1, p=[D["snare"]], vel=108 + (4 if big else 0), art="") for e in (4, 12)]
        dr += [dict(on=st + e, dur=1, p=[D["clap"]], vel=100, art="") for e in (4, 12)]
        dr += [dict(on=st + e, dur=1, p=[D["ohh"] if e % 4 == 2 else D["hh"]], vel=(72 if e % 4 == 2 else (58 if e % 2 == 0 else 44)), art="") for e in range(16)]
        if k == 1 and sec.startswith("Chorus"): dr.append(dict(on=st, dur=1, p=[D["crash"]], vel=118, art=""))   # the re-entry
        if sec.startswith("Post"): dr += [dict(on=st + e, dur=1, p=[p], vel=62 if e % 4 else 72, art="") for e, p in ((2, D["bhi"]), (3, D["bhi"]), (6, D["blo"]), (10, D["bhi"]), (11, D["bhi"]), (14, D["blo"]))]
        if big: dr += [dict(on=st + e, dur=1, p=[D["tamb"]], vel=58 if e % 2 else 70, art="") for e in range(16)]
        elif sec in ("Chorus 2", "Post 2"): dr += [dict(on=st + e, dur=1, p=[D["tamb"]], vel=62, art="") for e in range(0, 16, 2)]
        if sec.startswith("Chorus") and k == nsec - 1: dr += [dict(on=st + e, dur=1, p=[D["snare"]], vel=84 + 4 * (e - 13), art="") for e in (13, 14, 15)]
    drums += keep(dr)
    # ---- bass ----
    bs = []
    if last: bs.append(dict(on=st, dur=16, p=[r], vel=84, art="ring")) if k == 0 else None
    elif strip(b): bs.append(dict(on=st, dur=16, p=[r], vel=80, art=""))
    elif sec == "Intro" and k < 2: pass
    elif sec in ("Intro", "Verse 1", "Verse 2"):
        bs += [dict(on=st + e, dur=d, p=[p], vel=v, art="") for e, d, p, v in ((0, 3, r, 98), (3, 1, r, 70), (6, 2, r + 12, 88), (8, 2, r, 92), (11, 1, r, 70), (12, 2, f5, 86), (14, 2, r + 10 if ch.endswith("7") else r + 12, 80))]
    elif sec == "Bridge":
        if k < 6: bs.append(dict(on=st, dur=16, p=[r], vel=78 + 2 * k, art="")) if k >= 2 else None
        else: bs += [dict(on=st + e, dur=2, p=[r if e % 4 == 0 else r + 12], vel=90, art="") for e in range(0, 16, 2)]
    else:   # pre, chorus, post: disco octaves with a sixteenth push
        bs += [dict(on=st + e, dur=d, p=[p], vel=v, art="") for e, d, p, v in ((0, 2, r, 100), (2, 2, r + 12, 86), (4, 2, r, 96), (6, 1, r + 12, 84), (7, 1, r, 74), (8, 2, r, 98), (10, 2, r + 12, 86), (12, 2, r, 96), (14, 2, r + 12, 86))]
    bass += keep(bs)
    # ---- the muted funk guitar ----
    tg = tones(ch, 62, 74)[-3:]
    gs = []
    if sec in ("Verse 1", "Verse 2", "Intro"): gs += [dict(on=st + e, dur=1, p=tg, vel=74, art="chank") for e in (2, 6, 10, 14)]
    elif sec.startswith("Pre") or (sec in FULLS and not strip(b)):
        gs += [dict(on=st + e, dur=1, p=tg, vel=(80 if e in (2, 6, 10, 14) else 58), art="chank") for e in (0, 2, 3, 6, 8, 10, 11, 14)]
    elif sec == "Bridge" and k >= 6: gs += [dict(on=st + e, dur=1, p=tg, vel=76, art="chank") for e in (2, 6, 10, 14)]
    gtr += keep(gs)
    # ---- Rhodes ----
    kt = tones(ch, 57, 70)[:4]
    ks = []
    if sec in ("Verse 1", "Verse 2") or (sec == "Intro" and k >= 2) or strip(b): ks.append(dict(on=st, dur=14 if not strip(b) else 16, p=kt, vel=62, art=""))
    elif sec == "Bridge": ks.append(dict(on=st, dur=16 if k < 7 else 4, p=kt, vel=58 + 2 * k, art=""))
    elif sec.startswith("Pre"): ks += [dict(on=st, dur=8, p=kt, vel=70, art=""), dict(on=st + 8, dur=8, p=kt, vel=66, art="")]
    elif sec in FULLS: ks += [dict(on=st + e, dur=d, p=kt, vel=72, art="") for e, d in ((0, 3), (6, 2), (10, 4))]
    elif last and k == 0: ks.append(dict(on=st, dur=16, p=tones(ch, 57, 72)[:5], vel=60, art="ring"))
    keys += keep(ks)
    # ---- the hum: the bridge's first two lines ----
    if sec == "Bridge" and k < 4: hum.append(dict(on=st, dur=16, p=[41, 48], vel=50 + 4 * k, art=""))
    # ---- horns: stabs where the singer holds (chorus and post bars); a swell in pre 2 ----
    if sec in FULLS and not strip(b):
        busy = any(st + 10 <= n["on"] < st + 16 for n in lead)
        if not busy: horns += [dict(on=st + e, dur=d, p=tones(ch, 62, 75)[-3:], vel=100, art="stab") for e, d in ((12, 1), (14, 2))]
        if sec in ("Chorus 3", "Post 3") and not any(st + 4 <= n["on"] < st + 10 for n in lead):      # the last chorus: a third stab on the and of 2
            horns.append(dict(on=st + 6, dur=1, p=tones(ch, 62, 75)[-3:], vel=96, art="stab"))
    if sec == "Pre 2" and k < 3: horns.append(dict(on=st, dur=16, p=tones(ch, 60, 72)[-3:], vel=60 + 10 * k, art="swell"))
# ---- the riff: the title cell with sixteenth fills; intro, verse 2's gaps, outro ----
RIFF = [(2, 2, 69), (5, 1, 67), (6, 3, 72), (10, 1, 72), (11, 1, 70), (12, 2, 69), (14, 1, 67),
        (18, 2, 72), (21, 1, 69), (22, 2, 64), (25, 1, 67), (26, 2, 69), (29, 1, 67), (30, 2, 64)]
def riff_at(at, vel=86, half=None):
    seg = RIFF if half is None else [x for x in RIFF if (x[0] < 16) == (half == 1)]
    off = 0 if half != 2 else -16
    return [dict(on=at + o + off, dur=d, p=[p], vel=vel - (8 if d == 1 else 0), art="", src="riff") for o, d, p in seg]
def sec_at(s): return next(b["start"] for b in bars if b["sec"] == s)
riff += riff_at(sec_at("Intro")) + riff_at(sec_at("Intro") + 32)
lines = {}
for n in lead: lines.setdefault((n["sec"], n["line"]), []).append(n)
for i in range(4):                                     # verse 2: the riff's second bar where the line leaves a bar's room
    ln = lines[("Verse 2", i)]; end = max(n["on"] + n["dur"] for n in ln); bar2 = M.SECS["Verse 2"][i]["at"] + 16
    nxt = lines.get(("Verse 2", i + 1)) or lines[("Pre 2", 0)]
    if end <= bar2 + 6 and min(n["on"] for n in nxt) >= bar2 + 16: riff += [e for e in riff_at(bar2, 74, half=2) if e["on"] >= end + 1]
o_ = sec_at("Outro"); riff += [dict(e, art="ring" if j == 6 else "") for j, e in enumerate(riff_at(o_, 70, half=1))]
# ---- the backing echo, and the last chorus's harmony (a third under every title line) ----
F_SCALE = sorted(p for p in range(48, 80) if p % 12 in M.DM)
def third_under(p):
    i = F_SCALE.index(p); return F_SCALE[i - 2]
for s in ("Post 1", "Post 2", "Post 3"):
    at = M.SECS[s][1]["at"]
    bv += [dict(on=at + o, dur=d, midi=p, syl=x, sec=s, line=1, singer="bv") for (o, d, p), x in zip(M.ECHO, M.SECS[s][0]["syl"][:3])]
for n in lead:
    if n["sec"] == "Chorus 3" and n["line"] in (0, 3):
        bv.append(dict(on=n["on"], dur=n["dur"], midi=third_under(n["midi"]), syl=n["syl"], sec=n["sec"], line=n["line"], singer="bv"))
bv.sort(key=lambda n: n["on"])
rec = dict(title=L.TITLE, nbars=len(bars), bars=bars, plan=plan, lead=lead, harm=bv, drums=drums, bass=bass, gtr=gtr, riff=riff, keys=keys, horns=horns,
           hum=hum, cuts=CUTS, total_slots=TOT, slot="sixteenth", seconds=secs, singers=dict(her=M.HER), singer_by_sec=L.SINGER,
           meas={k: (float(v) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()}, hand_edits=c["pick"]["edits"], pick=c["pick"]["rank"],
           fp=c["fp"], order_fp=R["order_fp"], survivors=R["survivors"], built=R["made"], attempts=R["tries"], deaths=dict(R["deaths"].most_common()),
           by_construction=R["by_construction"], qbpm={"4/4": QB}, slot_sec=60 / QB / 4, plans=c["plans"], cell_log=c["cell_log"], riff_cell=RIFF)
pickle.dump(rec, open("/home/claude/p31/song_record.pkl", "wb"))
print(rec["nbars"], "bars,", f"{secs:.0f} s ({int(secs//60)}:{int(round(secs%60)):02d});", len(lead), "sung;", len(bv), "bv;", len(drums), "drums;", len(bass), "bass;",
      len(gtr), "gtr;", len(riff), "riff;", len(keys), "keys;", len(horns), "horns;", len(hum), "hum;", len(CUTS), "cuts; fp", rec["fp"])
