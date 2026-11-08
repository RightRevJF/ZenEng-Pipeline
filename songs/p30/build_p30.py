"""Build the song record for 'She Left the Light On' from the frozen melody (melody_final.pkl: ranking #1, no hand edits). One male
country voice and a five-piece country band. Times in SIXTEENTHS (16 a bar of 4/4) at q = 84; D major, G minor borrowed under THUMB.
  acoustic   strummed steel-string from bar 1 (open shapes): the verses' light pattern (down on 1 and 3, up on the 'and' of 2 and 4)
             in verse 1; the full pattern (D . D U . U D U) from chorus 1; the bridge picks the chord in eighths; the drop (chorus 3's
             first two bars) one strum, let ring; the last bar one strum, let ring (on G -- the song ends open).
  lick       the clean electric's hook: the title cell up an octave (A4 D5 B4 D5) answered by a falling line; the intro, both post-
             choruses and the outro play it (the research: an intro guitar hook that returns in the vocal).
  steel      pedal steel: swells under verse 1 and the bridge; from verse 2 it answers the singer where a line leaves room (falling
             chord tones from the top); it holds B-flat over the G minor; in the drop it swells alone under 'now you're the one out late'.
  bass       verse 1: the root on 1 and 3; from chorus 1 the two-beat (root on 1, fifth on 3) with an eighth walk into each chord change;
             the bridge in whole notes; out in the drop; the last bar held.
  organ      the last chorus only, from the flip: the chord held a bar at a time, under everything (with a tambourine on the eighths).
  drums      intro bars 3-4 and verse 1: kick 1 and 3, cross-stick 2 and 4, soft eighth hats; choruses: kick 1, the 'and' of 2 and 3,
             snare 2 and 4, eighth hats (open on the 'and' of 4), crash at the top; verse 2 as the choruses without the open hat; the
             bridge: kick on 1 and a tom swell in its last bar; the drop silent until a fill into the flip; the flip: crash, the full kit."""
import pickle, sys
sys.path[:0] = ["/home/claude/p30"]
import melody_p30 as M, lyric as L
c = pickle.load(open("/home/claude/p30/melody_final.pkl", "rb"))
R = pickle.load(open("/home/claude/p30/melody_result.pkl", "rb"))
QB = 84
bars = []
for i, b in enumerate(M.BARS):
    k = sum(1 for x in M.BARS[:i] if x["sec"] == b["sec"])
    bars.append(dict(sec=b["sec"], meter="4/4", chord=b["chord"], start=b["start"], len=b["len"], qbpm=QB, k=k, key="D major",
                     build=(b["sec"] == "Bridge" and k == 5), instrumental=b["sec"] in ("Intro", "Post 1", "Post 2", "Outro")))
lead = []
for s in M.SINGS:
    for o, d, p, x, li in c[s]:
        lead.append(dict(on=o, dur=d, midi=p, syl=x, sec=s, line=li, role=M.SECS[s][li]["role"], meter="4/4", singer="him"))
lead.sort(key=lambda n: n["on"])
TOT = M.TOTAL; secs = TOT * 60 / QB / 4
plan = []
for sec, met, scale, lines, chs in M.FORM:
    b0 = next(i for i, b in enumerate(bars) if b["sec"] == sec); nb = sum(1 for b in bars if b["sec"] == sec)
    plan.append((sec, nb, b0, "4/4"))
ROOT = {"D": 2, "G": 7, "A": 9, "Bm": 11, "Em": 4, "Gm": 7}
SHAPE = {"D": [50, 57, 62, 66], "G": [43, 47, 50, 55, 59, 67], "A": [45, 52, 57, 61, 64], "Bm": [47, 54, 59, 62, 66],
         "Gm": [43, 50, 55, 58, 62, 67], "Em": [40, 47, 52, 55, 59, 64]}
def at_or_above(pc, lo):
    p = lo
    while p % 12 != pc: p += 1
    return p
def tones(ch, lo, hi): return [p for p in range(lo, hi + 1) if p % 12 in M.CH[ch]]
D = dict(kick=36, snare=38, xstick=37, hh=42, ohh=46, crash=49, tl=45, tm=47, th=50)
drums, bass, ac, lick, steel, organ = [], [], [], [], [], []
FULLS = ("Chorus 1", "Chorus 2", "Chorus 3")
def is_drop(b): return b["sec"] == "Chorus 3" and b["k"] < 2
for bi, b in enumerate(bars):
    sec, ch, st, k = b["sec"], b["chord"], b["start"], b["k"]
    nsec = sum(1 for x in bars if x["sec"] == sec)
    nxt = bars[bi + 1]["chord"] if bi + 1 < len(bars) else ch
    last = bi == len(bars) - 1
    sh = SHAPE[ch]
    # ---- acoustic ----
    if last or is_drop(b) and k == 0:
        ac.append(dict(on=st, dur=16 if not is_drop(b) else 32, p=sh, vel=74 if is_drop(b) else 80, art="ring"))
    elif is_drop(b): pass
    elif sec == "Bridge":
        arp = [sh[0], sh[2], sh[-2], sh[-1], sh[-2], sh[2], sh[1], sh[2]]
        ac += [dict(on=st + 2 * j, dur=2, p=[p], vel=66, art="pick") for j, p in enumerate(arp)]
    else:
        pat = [(0, "D"), (6, "U"), (8, "D"), (14, "U")] if sec in ("Verse 1", "Intro") else [(0, "D"), (4, "D"), (6, "U"), (10, "U"), (12, "D"), (14, "U")]
        for j, (e, dn) in enumerate(pat):
            e2 = pat[j + 1][0] if j + 1 < len(pat) else 16
            ac.append(dict(on=st + e, dur=e2 - e, p=sh if dn == "D" else sh[-3:], vel=(78 if dn == "D" else 64) + (6 if sec in FULLS else 0), art="strum"))
    # ---- bass ----
    r = at_or_above(ROOT[ch], 38)                                    # D2-C#3
    f5 = r + 7 if r + 7 <= 52 else r - 5
    if last: bass.append(dict(on=st, dur=16, p=[r], vel=88, art=""))
    elif is_drop(b) or (sec == "Intro" and k < 2): pass
    elif sec in ("Verse 1", "Intro"): bass += [dict(on=st, dur=8, p=[r], vel=84, art=""), dict(on=st + 8, dur=8, p=[r if sec == "Intro" else f5], vel=78, art="")]
    elif sec == "Bridge": bass.append(dict(on=st, dur=16, p=[r], vel=82, art=""))
    else:
        nr = at_or_above(ROOT[nxt], 38)
        pat = [(0, 6, r), (8, 4, f5)]
        if nxt != ch:                                                 # an eighth walk into the change
            step = 1 if nr > r else -1
            w1 = nr - 2 * step if abs(nr - r) > 2 else (r + f5) // 2
            pat += [(12, 2, w1), (14, 2, nr - step)]
        else: pat += [(12, 2, f5 + (2 if f5 + 2 <= 52 else -2)), (14, 2, r + 12 if r + 12 <= 52 else r)]
        bass += [dict(on=st + e, dur=d, p=[p], vel=(92 if e in (0, 8) else 80) + (4 if sec in FULLS else 0), art="") for e, d, p in pat]
    # ---- drums ----
    if (sec == "Intro" and k < 2) or (is_drop(b) and k == 0) or last: pass
    elif is_drop(b):                                                   # the fill into the flip: toms on the last beat and a half
        drums += [dict(on=st + e, dur=1, p=[t], vel=72 + 6 * j, art="") for j, (e, t) in enumerate([(10, D["th"]), (12, D["tm"]), (13, D["tm"]), (14, D["tl"]), (15, D["tl"])])]
    elif sec in ("Intro", "Verse 1"):
        drums += [dict(on=st + e, dur=1, p=[D["kick"]], vel=84, art="") for e in (0, 8)]
        drums += [dict(on=st + e, dur=1, p=[D["xstick"]], vel=70, art="") for e in (4, 12)]
        drums += [dict(on=st + e, dur=1, p=[D["hh"]], vel=48 if e % 4 else 56, art="") for e in range(0, 16, 2)]
    elif sec == "Bridge":
        drums.append(dict(on=st, dur=1, p=[D["kick"]], vel=76, art=""))
        if k == nsec - 1: drums += [dict(on=st + 8 + e, dur=1, p=[D["tl"]], vel=56 + 5 * e, art="") for e in range(8)]
    else:
        full = sec in FULLS; big = sec == "Chorus 3"
        drums += [dict(on=st + e, dur=1, p=[D["kick"]], vel=(98 if e in (0, 8) else 86) + (4 if big else 0), art="") for e in ((0, 6, 8) if full or sec.startswith("Post") else (0, 8))]
        drums += [dict(on=st + e, dur=1, p=[D["snare"]], vel=(104 if full else 94) + (4 if big else 0), art="") for e in (4, 12)]
        drums += [dict(on=st + e, dur=1, p=[D["ohh"] if (full and e == 14) else D["hh"]], vel=(70 if e % 4 == 0 else 58) + (6 if full else 0), art="") for e in range(0, 16, 2)]
        if k == 0 and full or (big and k == 2): drums.append(dict(on=st, dur=1, p=[D["crash"]], vel=110, art=""))
        if sec in ("Chorus 1", "Chorus 2") and k == nsec - 1:              # a snare pickup into the post-chorus
            drums += [dict(on=st + e, dur=1, p=[D["snare"]], vel=78 + 6 * (e - 13), art="") for e in (13, 14, 15)]
    # ---- the last chorus lifts: organ under it and a tambourine on the eighths (from the flip) ----
    if sec == "Chorus 3" and k >= 2 and not last:
        organ.append(dict(on=st, dur=16, p=tones(ch, 55, 67)[:3], vel=62, art=""))
        drums += [dict(on=st + e, dur=1, p=[54], vel=60 if e % 4 else 70, art="") for e in range(0, 16, 2)]
    # ---- steel: swells under verse 1 and the bridge (a bar's chord tone, high) ----
    if sec in ("Verse 1", "Bridge") and not last:
        top = [p for p in tones(ch, 64, 76)]
        p = 70 if ch == "Gm" else top[len(top) // 2]
        steel.append(dict(on=st + 2, dur=14, p=[p], vel=56 if sec == "Verse 1" else 62, art="swell"))
    if is_drop(b) and k == 0:
        steel.append(dict(on=st, dur=32, p=[69, 73], vel=64, art="swell"))
# ---- steel answers: where the singer leaves room, from verse 2 (falling chord tones from the top) ----
lines = {}
for n in lead: lines.setdefault((n["sec"], n["line"]), []).append(n)
keys_ = list(lines)
def bar_of(o): return next(b for b in bars if b["start"] <= o < b["start"] + b["len"])
for a, nb_ in zip(keys_, keys_[1:] + [None]):
    if a[0] not in ("Verse 2", "Chorus 1", "Chorus 2", "Chorus 3") or a == ("Chorus 3", 0): continue
    end = max(n["on"] + n["dur"] for n in lines[a]) if a[0] == "Verse 2" or lines[a][-1]["dur"] < 8 else lines[a][-1]["on"] + 4
    nxt_on = min(n["on"] for n in lines[nb_]) if nb_ else end + 24
    if a[0] == "Chorus 3" and a[1] == 4: nxt_on = end + 16
    t = end + 1
    room = nxt_on - 2 - t
    if room < 6: continue
    ch = bar_of(t)["chord"]; tt = sorted(tones(ch, 66, 79), reverse=True)[:3]
    for j, p in enumerate(tt):
        d = 4 if j < 2 else min(8, nxt_on - 2 - (t + 8))
        if d < 2 or t + d > nxt_on - 2: break
        steel.append(dict(on=t, dur=d, p=[p], vel=70, art="slide" if j == 0 else "")); t += d
# ---- the lick ----
LICK = [(2, 2, 69), (4, 6, 74), (10, 2, 71), (12, 4, 74), (16, 6, 71), (22, 2, 69), (24, 4, 67), (28, 4, 66),
        (34, 2, 69), (36, 6, 74), (42, 2, 71), (44, 4, 74), (48, 4, 73), (52, 2, 71), (54, 2, 69), (56, 8, 64)]
def lick_at(at, part, last=False):
    seg = [(o, d, p) for o, d, p in LICK if (o < 32) == (part == 1)]
    off = 0 if part == 1 else -32
    out = [dict(on=at + o + off, dur=d, p=[p], vel=86, art="", src="lick") for o, d, p in seg]
    if last: out = out[:-2] + [dict(on=at + 24, dur=8, p=[71], vel=80, art="ring", src="lick")]   # the end: B4 held over G -- open
    return out
def sec_at(s): return next(b["start"] for b in bars if b["sec"] == s)
lick += lick_at(sec_at("Intro"), 1) + lick_at(sec_at("Intro") + 32, 2)
for s in ("Post 1", "Post 2"): lick += lick_at(sec_at(s), 2)
o_ = sec_at("Outro"); lick += lick_at(o_, 1) + lick_at(o_ + 32, 1, last=True)
rec = dict(title=L.TITLE, nbars=len(bars), bars=bars, plan=plan, lead=lead, harm=[], drums=drums, bass=bass, ac=ac, lick=lick, steel=steel, organ=organ,
           total_slots=TOT, slot="sixteenth", seconds=secs, singers=dict(him=M.HIM), singer_by_sec=L.SINGER,
           meas={k: (float(v) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()}, hand_edits=c["pick"]["edits"], pick=c["pick"]["rank"],
           fp=c["fp"], order_fp=R["order_fp"], survivors=R["survivors"], built=R["made"], attempts=R["tries"], deaths=dict(R["deaths"].most_common()),
           by_construction=R["by_construction"], qbpm={"4/4": QB}, slot_sec=60 / QB / 4, plans=c["plans"], cell_log=c["cell_log"])
pickle.dump(rec, open("/home/claude/p30/song_record.pkl", "wb"))
print(rec["nbars"], "bars,", f"{secs:.0f} s ({int(secs//60)}:{int(round(secs%60)):02d});", len(lead), "sung;", len(drums), "drums;", len(bass), "bass;",
      len(ac), "acoustic;", len(lick), "lick;", len(steel), "steel;", len(organ), "organ; fp", rec["fp"])
