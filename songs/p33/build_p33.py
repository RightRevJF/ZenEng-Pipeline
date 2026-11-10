"""Build the song record for 'Sadie' from the frozen melody (melody_final.pkl: #1 of the register gate's survivors by the composite, no
hand edits). A country-rock anthem: a male baritone lead (her father), a gang, and a band. Times in EIGHTHS (8 a bar of 4/4) at q = 124;
A major throughout. The designed moments:
  the riff (fix 22, motif from the title's words): the lead guitar plays the title cell's first bar -- SA E die C# SA E (pushed) die C#
             FEET A | POUND B -- then a low open-A chug with a lick (A C# E), bar by bar, following the chord (up a fourth on D, down a fourth on E); the
             intro, the riff break, the outro
  the answers (fixes 90 and 101): in verses 1 and 2 the lead guitar answers each line with its last notes an octave up, the figure
             FITTED TO THE ROOM the line leaves before the next pickup -- three notes when three eighths are free, two when two, none
             when fewer (fix 101, run as code here for the first time)
  the drop (fix 60, 76, 82, 87): bar 61 -- everyone hits E on beat 1 and stops; 'it's UP' alone; bars 62-64: nothing but a kick-drum
             heartbeat (lub-dub on beats 1 and 3), the voice silent; the chart prints N.C.; chorus 3 slams in with a crash
  the gang (fix 43): 'Sadie! Sadie!' in every chorus (unison and the octave below, the lead's notes); the whole last chorus;
             two 'Sadie!' shouts in the outro
  drums      verse: kick 1 and 3 (and the and of 3), snare 2 and 4, closed hats in eighths; pre: floor tom eighths, a snare fill into
             the chorus; chorus: four on the floor, snare 2 and 4, open hats on the off-beats, crash on bar 1; bridge: half time (kick 1,
             snare 3), rim clicks for four bars then the full kit building, a snare roll in its last bar; a tambourine on the
             off-beats in choruses 2 and 3, in eighths in chorus 4
  bass       eighths on the root (verses palm-muted feel, low); choruses root-fifth-octave eighths; bridge half notes; the drop one hit
  rhythm gtr palm-muted power chords in eighths (verses); open power chords in the choruses (a hit on 1, eighths after)
  acoustic   strummed eighths from chorus 1 (chorus, bridge, outro)
  organ      a pad in the pre-choruses, choruses and the bridge
Every instrument rests in bars 62-64; 9.12 reads the drop as designed silence (fix 87)."""
import pickle, sys
sys.path[:0] = ["/home/claude/p33"]
import melody_p33 as M, lyric as L
c = pickle.load(open("/home/claude/p33/melody_final.pkl", "rb"))
QB = 124
DROP0 = M.STARTS["Drop"][1]; DROP_BARS = {DROP0 + 8 * j for j in range(4)}
bars = []
for i, b in enumerate(M.BARS):
    k = sum(1 for x in M.BARS[:i] if x["sec"] == b["sec"])
    ch = "N.C." if (b["sec"] == "Drop" and k >= 1) else b["chord"]
    bars.append(dict(sec=b["sec"], meter="4/4", chord=ch, implied=b["chord"], start=b["start"], len=8, qbpm=QB, k=k, key="A major",
                     build=(b["sec"] == "Bridge" and k >= 4), instrumental=b["sec"] in ("Intro", "Riff", "Outro"),
                     silence=(b["sec"] == "Drop" and k >= 1)))
lead = []
for s in M.SINGS:
    for o, d, p, x, li in c[s]:
        lead.append(dict(on=o, dur=d, midi=p, syl=x, sec=s, line=li, role=M.SECS[s][li]["role"], meter="4/4", singer="him"))
lead.sort(key=lambda n: n["on"])
TOT = M.TOTAL; secs = TOT * 60 / QB / 2
plan = []
for sec, met, scale, lines, chs in M.FORM:
    b0 = next(i for i, b in enumerate(bars) if b["sec"] == sec); nb = sum(1 for b in bars if b["sec"] == sec)
    plan.append((sec, nb, b0, "4/4"))
ROOT = {"A": 9, "D": 2, "E": 4, "F#m": 6, "Bm": 11, "C#m": 1}
def at_or_above(pc, lo):
    p = lo
    while p % 12 != pc: p += 1
    return p
def tones(ch, lo, hi): return [p for p in range(lo, hi + 1) if p % 12 in M.CH[ch]]
D = dict(kick=36, snare=38, rim=37, hh=42, ohh=46, crash=49, ride=51, ftom=41, tamb=54)
drums, bass, rhy, ac, organ, riff, gang = [], [], [], [], [], [], []
CHOR = ("Chorus 1", "Chorus 2", "Chorus 3", "Chorus 4")
def dr(on, p, v, d=1): drums.append(dict(on=on, dur=d, p=[D[p]], vel=v))
for bi, b in enumerate(bars):
    sec, ch, st, k = b["sec"], b["implied"], b["start"], b["k"]
    r = at_or_above(ROOT[ch], 33)                                            # A1-G#2
    pc5 = (ROOT[ch] + 7) % 12; fifth = at_or_above(pc5, r + 1)
    last_of_sec = bi + 1 < len(bars) and bars[bi + 1]["sec"] != sec
    # ---- the drop ----
    if sec == "Drop":
        if k == 0:
            dr(st, "crash", 112, 8); dr(st, "kick", 112)
            bass.append(dict(on=st, dur=2, p=[r], vel=104)); rhy.append(dict(on=st, dur=2, p=[r + 12, r + 19, r + 24], vel=106))
            organ.append(dict(on=st, dur=2, p=tones(ch, 57, 69)[:3], vel=80))
        else:
            for e in (0, 1, 4, 5): dr(st + e, "kick", 70 if e in (0, 4) else 54)    # the heartbeat: lub-dub on 1 and 3
        continue
    intro_alone = sec == "Intro" and k < 4
    # ---- drums ----
    if not intro_alone:
        if sec in CHOR:
            for e in (0, 2, 4, 6): dr(st + e, "kick", 108)
            for e in (2, 6): dr(st + e, "snare", 110)
            for e in (1, 3, 5, 7): dr(st + e, "ohh", 78)
            if k == 0 or (sec == "Chorus 4" and k == 4): dr(st, "crash", 116, 8)
            if sec in ("Chorus 2", "Chorus 3"):
                for e in (1, 3, 5, 7): dr(st + e, "tamb", 96)                    # the lift: a tambourine on the off-beats from chorus 2
            if sec == "Chorus 4":
                for e in range(8): dr(st + e, "tamb", 98 if e % 2 else 104)
        elif sec.startswith("Pre"):
            for e in range(8): dr(st + e, "ftom", 84 if e % 2 == 0 else 70)
            for e in (2, 6): dr(st + e, "snare", 100)
            dr(st, "kick", 100)
            if last_of_sec:
                for e in (4, 5, 6, 7): dr(st + e, "snare", 96 + 4 * (e - 4))
        elif sec == "Bridge":
            dr(st, "kick", 96)
            if k < 4: dr(st + 4, "rim", 80)
            else:
                dr(st + 4, "snare", 98)
                for e in range(0, 8, 2): dr(st + e, "hh", 72)
            if last_of_sec:
                for e in range(8): dr(st + e, "snare", 80 + 4 * e)
        else:                                                                 # intro (bars 5-8), verses, riff break, outro
            for e in (0, 4, 5): dr(st + e, "kick", 100 if e != 5 else 84)
            for e in (2, 6): dr(st + e, "snare", 104)
            for e in range(8): dr(st + e, "hh", 76 if e % 2 == 0 else 62)
            if sec in ("Riff", "Outro") and k == 0: dr(st, "crash", 108, 8)
    # ---- bass ----
    if not intro_alone:
        if sec == "Bridge":
            bass += [dict(on=st + e, dur=4, p=[r], vel=90) for e in (0, 4)]
        elif sec in CHOR:
            fig = [r, r, fifth, r + 12, r, r, fifth, r + 12]
            bass += [dict(on=st + e, dur=1, p=[q], vel=100 - (0 if e % 2 == 0 else 8)) for e, q in enumerate(fig)]
        else:
            bass += [dict(on=st + e, dur=1, p=[r], vel=94 - (0 if e % 2 == 0 else 10)) for e in range(8)]
    # ---- rhythm guitar (power chords: root, fifth, octave) ----
    pw = [r + 12, r + 19, r + 24]
    if sec in ("Verse 1", "Verse 2") or (sec == "Intro" and k >= 4) or sec in ("Riff",):
        rhy += [dict(on=st + e, dur=1, p=pw, vel=86 - (0 if e % 2 == 0 else 10), art="palm") for e in range(8)]
    elif sec in CHOR or sec.startswith("Pre") or sec == "Outro":
        rhy.append(dict(on=st, dur=2, p=pw, vel=104, art="open")); rhy += [dict(on=st + e, dur=1, p=pw, vel=90, art="open") for e in range(2, 8)]
    elif sec == "Bridge":
        rhy.append(dict(on=st, dur=8, p=pw, vel=80 + (12 if k >= 4 else 0), art="ring"))
    # ---- acoustic (strummed eighths) ----
    if sec in CHOR or sec in ("Bridge", "Outro"):
        ac += [dict(on=st + e, dur=1, p=tones(ch, 52, 64), vel=74 - (0 if e % 2 == 0 else 10)) for e in range(8)]
    # ---- organ pad ----
    if sec in CHOR or sec.startswith("Pre") or sec == "Bridge":
        organ.append(dict(on=st, dur=8, p=tones(ch, 57, 69)[:3], vel=72 + (8 if sec == "Chorus 4" else 0), art="pad"))
# ---- the riff (fix 22): the title cell's first bar on the lead guitar, then the open-A chug with a lick ----
CELL = [(n["on"] - M.SECS["Chorus 1"][0]["at"], n["dur"], n["midi"]) for n in lead if n["sec"] == "Chorus 1" and n["line"] == 0][:6]
assert [p for _, _, p in CELL] == [64, 61, 64, 61, 57, 59], CELL
LICK = [(0, 1, 45), (1, 1, 45), (2, 1, 49), (3, 1, 45), (4, 1, 45), (5, 1, 52), (6, 2, 49)]
RIFF_BARS = []
TRANS = {"A": 0, "D": 5, "E": -5}                                            # the riff follows the chord: up a fourth on D, down a fourth on E
for bi, b in enumerate(bars):
    if b["sec"] in ("Intro", "Riff", "Outro") and bi + 1 < len(bars):
        fig = CELL if b["k"] % 2 == 0 else LICK
        tr_ = TRANS[b["implied"]]
        riff += [dict(on=b["start"] + o, dur=d, p=[p + tr_ + (12 if fig is CELL else 0)], vel=100, art="riff") for o, d, p in fig if o < 8]
        RIFF_BARS.append(bi + 1)
# chorus 4: the lead guitar doubles 'Sadie! Sadie!' an octave up with the crowd, and rings the chord tones under the rest of the line
for b in bars:
    if b["sec"] == "Chorus 4" and b["k"] in (0, 4):
        riff += [dict(on=b["start"] + o, dur=d, p=[p + 12], vel=104, art="riff") for o, d, p in CELL]
    elif b["sec"] == "Chorus 4":
        riff.append(dict(on=b["start"], dur=8, p=[tones(b["implied"], 64, 76)[-1]], vel=92, art="ring"))
# ---- the answers (fixes 90 and 101): verse lines answered by the lead guitar, the figure fitted to the room ----
ANSWERS = []
lines_ = {}
for n in lead: lines_.setdefault((n["sec"], n["line"]), []).append(n)
for (sec_, li), ns in sorted(lines_.items(), key=lambda kv: kv[1][0]["on"]):
    if sec_ not in ("Verse 1", "Verse 2"): continue
    t = ns[-1]["on"] + 1
    nxt = [x for x in lead if x["on"] > ns[-1]["on"] and (x["sec"], x["line"]) != (sec_, li)]
    stop = nxt[0]["on"] if nxt else t + 3
    room = stop - t
    m = 3 if room >= 3 else (2 if room >= 2 else 0)                           # 101: fitted to the room
    if m == 0: ANSWERS.append(dict(sec=sec_, line=li, on=t, figure=[], room=room)); continue
    figure = [x["midi"] + 12 for x in ns[-m:]]
    riff += [dict(on=t + j, dur=1, p=[q], vel=88, art="answer") for j, q in enumerate(figure)]
    ANSWERS.append(dict(sec=sec_, line=li, on=t, figure=figure, room=room))
riff.sort(key=lambda e: e["on"])
for a_, b_ in zip(riff, riff[1:]):
    if a_["on"] + a_["dur"] > b_["on"]: a_["dur"] = b_["on"] - a_["on"]
# ---- the gang (fix 43): 'Sadie! Sadie!' in every chorus (the lead's notes, unison and the octave below); all of chorus 4; the outro ----
GANG_LINES = []
for n in lead:
    whole = n["sec"] == "Chorus 4"
    sadie = n["sec"] in CHOR and n["line"] == 0 and n["syl"][0] == "sadie"
    if whole or sadie:
        gang.append(dict(on=n["on"], dur=n["dur"], p=[n["midi"] - 12, n["midi"]], vel=96 if sadie else 84, syl=n["syl"][0]))
OUT0 = M.STARTS["Outro"][1]
SH = [x for x in lead if x["sec"] == "Chorus 1" and x["line"] == 0][:4]
for j in (2, 6):                                                              # two 'Sadie! Sadie!' shouts in the outro, bars 3 and 7
    b0 = OUT0 + 8 * j
    gang += [dict(on=b0 + (x["on"] - SH[0]["on"]), dur=x["dur"], p=[x["midi"] - 12, x["midi"]], vel=100, syl="sadie") for x in SH]
gang.sort(key=lambda e: e["on"])
# the ending: everyone on A for the last bar, held
LASTB = bars[-1]["start"]
for lst in (drums, bass, rhy, ac, organ, riff):
    lst[:] = [e for e in lst if e["on"] < LASTB]
dr(LASTB, "crash", 116, 8); dr(LASTB, "kick", 112)
bass.append(dict(on=LASTB, dur=8, p=[33], vel=104)); rhy.append(dict(on=LASTB, dur=8, p=[45, 52, 57], vel=108, art="ring"))
ac.append(dict(on=LASTB, dur=8, p=tones("A", 52, 64), vel=80)); organ.append(dict(on=LASTB, dur=8, p=tones("A", 57, 69)[:3], vel=80, art="pad"))
riff.append(dict(on=LASTB, dur=8, p=[57], vel=100, art="ring"))
for lst in (riff, bass, rhy, ac, organ):
    lst.sort(key=lambda e: e["on"])
    for a_, b_ in zip(lst, lst[1:]):
        if a_["on"] + a_["dur"] > b_["on"]: a_["dur"] = b_["on"] - a_["on"]
_dd = {}
for e in drums:                                                               # one hit per drum per eighth (the louder kept)
    k_ = (e["on"], e["p"][0])
    if k_ not in _dd or e["vel"] > _dd[k_]["vel"]: _dd[k_] = e
drums = sorted(_dd.values(), key=lambda e: (e["on"], e["p"][0]))
SIL = sorted(DROP_BARS - {DROP0})
assert not [e for lst in (bass, rhy, ac, organ, riff, gang) for e in lst if any(s <= e["on"] < s + 8 for s in SIL)], "the drop: silence"
assert not [e for e in drums if any(s <= e["on"] < s + 8 for s in SIL) and e["p"] != [D["kick"]]], "the drop: the heartbeat only"
CUTS = [dict(kind="drop", bars=[DROP0 // 8 + 1 + j for j in range(4)], what="bar 61: everyone hits E on beat 1 and stops; bars 62-64: the kick's heartbeat only")]
R = c["search"]
rec = dict(title=L.TITLE, nbars=len(bars), bars=bars, plan=plan, lead=lead, harm=[], drums=drums, bass=bass, rhy=rhy, ac=ac, organ=organ,
           riff=riff, gang=gang, total_eighths=TOT, slot="eighth", seconds=secs, singers=dict(him=dict(lo=45, top=66)), singer_by_sec=L.SINGER,
           cuts=CUTS, drop_bars=[x // 8 + 1 for x in sorted(DROP_BARS)], answers=ANSWERS, riff_bars=RIFF_BARS,
           meas={k_: (float(v_) if isinstance(v_, (int, float)) else v_) for k_, v_ in c["meas"].items()}, hand_edits=c["hand"], from_fp=c["from"],
           fp=c["fp"], order_fp=R["order_fp"], survivors=R["survivors"], built=R["made"], attempts=R["tries"],
           deaths=dict(sorted(R["deaths"].items(), key=lambda kv: -kv[1])), by_construction=c["by_construction"], qbpm={"4/4": QB},
           plans=c["plans"], cell_log=c["cell_log"], rerun=R["rerun"], top20=R["top20"])
pickle.dump(rec, open("/home/claude/p33/song_record.pkl", "wb"))
print(rec["nbars"], "bars,", f"{secs:.0f} s ({int(secs//60)}:{int(round(secs%60)):02d});", len(lead), "sung;", {k: len(rec[k]) for k in ("drums", "bass", "rhy", "ac", "organ", "riff", "gang")},
      "answers", [(a["sec"][-1], a["line"], len(a["figure"]), a["room"]) for a in ANSWERS])
