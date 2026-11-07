"""Build the song record for 'Tinted Glass' from the frozen melody (melody_final.pkl). A duet that never sings together: him (baritone)
and her (his chorus tune an octave up). Slow-burn soul in 6/8 at dotted-q = 54: times in EIGHTHS (a bar = 6, beats on 0 and 3).
Eb major throughout, no key change.
  electric piano  the heart of it: in the verses, a low chord on 1 held, then the triplet climb (chord tones on eighths 4-6); in each
                  four-bar verse or bridge line the voice is done by bar 3, and the piano ANSWERS in bar 4 (a falling line of eighths);
                  in the choruses, chords on 1 and 4, pushed: the second chord an eighth early on the last bar of each line
  bass            warm, fingered: root on 1 (dotted quarter), fifth on 4, an approach on the last eighth into a new chord; in from verse 1
  organ           drawbar, quiet: held chords under the choruses and the bridge, from verse 4 under the verses too; fuller in the last choruses
  drums           brushes: hats on the eighths (1 and 4 leaning), side-stick on 4 in the verses; the choruses: kick 1, snare 4, ride;
                  verse 1 and the intro without drums; the bridge only hats and a soft kick (the quiet that frightens); the last choruses
                  the fullest, with no key change -- the song refuses its own lift
  outro           the electric piano alone: Ab, Bb, Eb, Eb, the last chord left to ring"""
import pickle, sys
sys.path[:0] = ["/home/claude/p28"]
import melody_p28 as M, lyric as L, intake as I
c = pickle.load(open("/home/claude/p28/melody_final.pkl", "rb"))
R = pickle.load(open("/home/claude/p28/melody_result.pkl", "rb"))
DQ = 54                                                   # dotted quarters a minute; MIDI tempo in quarters is 81 (v65 fix 33)
bars = []
for i, b in enumerate(M.BARS):
    k = sum(1 for x in M.BARS[:i] if x["sec"] == b["sec"])
    bars.append(dict(sec=b["sec"], meter="6/8", chord=b["chord"], start=b["start"], len=6, qbpm=81, k=k, key="Eb major",
                     instrumental=b["sec"] in ("Intro", "Outro")))
lead = []
for s in M.SINGS:
    for o, d, p, x, li in c[s]:
        ln = M.SECS[s][li]
        lead.append(dict(on=o, dur=d, midi=p, syl=x, sec=s, line=li, role=ln["role"], meter="6/8", singer=ln["singer"]))
lead.sort(key=lambda n: n["on"])
TOT = M.TOTAL; secs = TOT * 60 / DQ / 3
plan = []
for sec, met, scale, lines, chs in M.FORM:
    b0 = next(i for i, b in enumerate(bars) if b["sec"] == sec); nb = sum(1 for b in bars if b["sec"] == sec)
    plan.append((sec, nb, b0, "6/8"))
ROOT = {"Eb": 3, "Ab": 8, "Bb": 10, "Cm": 0, "Fm": 5, "Gm": 7}
FIFTH = {k: (v + 7) % 12 for k, v in ROOT.items()}
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
def scale_down(top, n):
    out, p = [], top
    while len(out) < n:
        if p % 12 in M.EB: out.append(p)
        p -= 1
    return out
keys, bass, org, drums = [], [], [], []
D = dict(kick=36, snare=38, stick=37, hh=42, ride=51, crash=49)
LAST = ("Chorus 3", "Chorus 4")
for bi, b in enumerate(bars):
    sec, ch, st, k = b["sec"], b["chord"], b["start"], b["k"]
    nxt = bars[bi + 1]["chord"] if bi + 1 < len(bars) else ch
    chorus = sec.startswith("Chorus"); line_bar = k % 4                  # four-bar lines in the verses and the bridge
    lift = 8 if sec in LAST else 0
    r = at_or_above(ROOT[ch], 39)                                         # bass root Eb2-D3
    lh = voicing(ch, 48, 3); rh = voicing(ch, 60, 3)
    # ---- electric piano ----
    if sec == "Outro":
        keys.append(dict(on=st, dur=6 if k < 3 else 6, p=lh + rh, vel=58 - 4 * k, art="ring"))
    elif chorus:
        push = (k % 2 == 1)                                              # the line's second bar: the second chord pushed an eighth early
        keys += [dict(on=st, dur=3 if not push else 2, p=lh + rh, vel=78 + lift, art=""),
                 dict(on=st + (2 if push else 3), dur=4 if push else 3, p=lh + rh, vel=74 + lift, art="")]
        keys += [dict(on=st + e, dur=1, p=[rh[-1] + 12 if e == 4 else rh[1]], vel=52 + lift, art="") for e in (1, 4, 5)]
    elif (sec.startswith("Verse") or sec == "Bridge") and line_bar == 3:   # the answer: the voice is done; a falling line of eighths
        top = voicing(ch, 67, 1)[0]
        keys.append(dict(on=st, dur=6, p=lh, vel=62, art=""))
        keys += [dict(on=st + e, dur=1, p=[q], vel=70 - 2 * e, art="answer") for e, q in enumerate(scale_down(top, 6))]
    else:
        quiet = sec == "Intro" or sec in ("Verse 5", "Verse 6")
        keys.append(dict(on=st, dur=3, p=lh, vel=(60 if quiet else 66), art=""))
        keys += [dict(on=st + 3 + e, dur=1 if e < 2 else 3 - e, p=[rh[e]], vel=(54 if quiet else 60) + 2 * e, art="") for e in range(3)]
    # ---- bass ----
    if sec not in ("Intro", "Outro"):
        bv = 78 + lift
        appr = at_or_above(ROOT[nxt], 39); appr = appr - 1 if nxt != ch else None
        if sec == "Bridge":
            bass.append(dict(on=st, dur=6, p=[r], vel=70, art=""))
        else:
            bass += [dict(on=st, dur=3, p=[r], vel=bv, art=""), dict(on=st + 3, dur=2 if appr else 3, p=[at_or_above(FIFTH[ch], r)], vel=bv - 8, art="")]
            if appr and appr != r: bass.append(dict(on=st + 5, dur=1, p=[appr], vel=bv - 12, art=""))
    # ---- organ ----
    if (chorus or sec == "Bridge" or sec in ("Verse 4", "Verse 5", "Verse 6")) and (k % 2 == 0):
        ov = 52 if sec.startswith("Verse") else (58 if sec == "Bridge" else 62 + lift)
        org.append(dict(on=st, dur=12, p=voicing(ch, 55, 3 if sec not in LAST else 4), vel=ov, art="pad"))
    # ---- drums (brushes) ----
    if sec in ("Intro", "Verse 1", "Outro"): continue
    if sec == "Bridge":
        drums += [dict(on=st + e, dur=1, p=[D["hh"]], vel=44 if e % 3 else 52, art="") for e in range(6)]
        drums.append(dict(on=st, dur=1, p=[D["kick"]], vel=60, art=""))
        continue
    if chorus:
        drums += [dict(on=st, dur=1, p=[D["kick"]], vel=92 + lift, art=""), dict(on=st + 3, dur=1, p=[D["snare"]], vel=84 + lift, art="")]
        drums += [dict(on=st + e, dur=1, p=[D["ride"]], vel=(68 if e % 3 == 0 else 54) + lift, art="") for e in range(6)]
        if k == 0: drums.append(dict(on=st, dur=1, p=[D["crash"]], vel=96 + lift, art=""))
        if k == 7 and sec != "Chorus 4": drums.append(dict(on=st + 5, dur=1, p=[D["snare"]], vel=72, art=""))
    else:
        soft = sec in ("Verse 5", "Verse 6")
        drums += [dict(on=st + e, dur=1, p=[D["hh"]], vel=(58 if e % 3 == 0 else 42) - (6 if soft else 0), art="") for e in range(6)]
        drums.append(dict(on=st + 3, dur=1, p=[D["stick"]], vel=64 - (8 if soft else 0), art=""))
        if not soft: drums.append(dict(on=st, dur=1, p=[D["kick"]], vel=70, art=""))
rec = dict(title=L.SECTIONS and I.TITLE, nbars=len(bars), bars=bars, plan=plan, lead=lead, harm=[], keys=keys, bass=bass, organ=org, drums=drums,
           total_eighths=TOT, slot="eighth", seconds=secs, singers=dict(him=M.HIM, her=M.HER), singer_by_sec=L.SINGER, stop_at=None,
           meas={k_: (float(v) if isinstance(v, (int, float)) else v) for k_, v in c["meas"].items()}, hand_edits=c["hand"], from_fp=c["from"],
           fp=c["fp"], order_fp=R["order_fp"], survivors=R["survivors"], built=R["made"], attempts=R["tries"], deaths=dict(R["deaths"].most_common()),
           by_construction=R["by_construction"], qbpm={"6/8": 81}, slot_sec=60 / DQ / 3, plans=c["plans"], cell_log=c["cell_log"])
pickle.dump(rec, open("/home/claude/p28/song_record.pkl", "wb"))
print(rec["nbars"], "bars,", f"{secs:.0f} s ({int(secs//60)}:{int(round(secs%60)):02d});", len(lead), "sung;", len(keys), "keys;", len(bass), "bass;",
      len(org), "organ;", len(drums), "drums; fp", rec["fp"])
