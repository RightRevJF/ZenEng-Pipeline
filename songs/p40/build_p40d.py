"""Nothing Else on Earth, made for real: the song record from melody_final_d.pkl (the design run's pick by ear, with the hand edits it
logs) and riff_p40d.pkl. 4/4 at q = 116, D major, 110 bars. After The Battle of Evermore (the writer's Q23-Q27): mandolin and acoustic
guitar carry the verses; the band arrives at the chorus ('Evermore, then the storm', Q24 B).
  Voices    Lark (mezzo) sings the verses, the pre-choruses and the bridge. Briar (an older man, high and worn) sings the choruses:
            chorus 1 alone; chorus 2 with Lark's harmony a third above; the last chorus both, except 'she sat down hungry...',
            which Lark sings alone; the tag both.
  mandolin  the riff (intro, verse bars 1-8, the riff break's edges, the outro); strummed eighths on the chord elsewhere.
  acoustic  strummed eighths, open chords, from intro bar 5 to the end (down, down-up pattern by velocity).
  perc      verses and intro bar 5 on: floor tom on 1 and 3 (soft), tambourine on 2 and 4; the pre-choruses add the tom on every beat.
  drums     the band's sections (choruses, riff break, last chorus): kick 1, 3 and the 'and' of 3, snare 2 and 4, ride eighths, a crash
            at each section's start and every four bars of the last chorus; a fill in the bar before each chorus and the break.
  bass      enters at the pre-chorus (roots in half notes); eighths in the choruses and the break; whole notes in the bridge.
  rgtr      electric, open power chords in eighths in the choruses and the break.
  strings   swell in each pre-chorus; held through the choruses and the bridge; the last chorus an octave higher on top.
  lgtr      electric lead: the chorus fills and the riff break's solo.
  Chorus 2 adds the tambourine on 2 and 4, the last chorus tambourine eighths; the break's electric guitar plays quarters under the solo.
  The outro: the mandolin riff alone for three bars, then one D chord on everything that plays, left to ring."""
import pickle, sys
sys.argv = ["x", "1", "design"]; sys.path[:0] = ["/home/claude/p40"]
import melody_p40d as P
M = P.M
import build_p40 as B0_                                                        # the hyphenation and the text (song 40's lyric)
F = pickle.load(open("/home/claude/p40/melody_final_d.pkl", "rb")); c = F["pick"]
RF = pickle.load(open("/home/claude/p40/riff_p40d.pkl", "rb"))
BAR = 48; NB = P.NBARS; QB = 116; TEXT = B0_.TEXT
bars = []
for nm, kind, nb in P.FORM:
    for k in range(nb):
        b = P.BAR0[nm] + k
        bars.append(dict(sec=nm, kind=kind, k=k, n=nb, chord=P.CHORD[b], roman=M.ROMAN[P.CHORD[b]], start=b * BAR, len=BAR, qbpm=QB, key="D major", stop=False))
def singer(sec, i):
    if sec in ("Chorus 1", "Chorus 2"): return "Briar"
    if sec == "Last Chorus": return "Lark" if i == 6 else "Briar"
    return "Lark"
lead = []
for n in c["notes"]:
    sec, i = n["line"].split(":"); i = int(i); t, hy = TEXT[sec][i][n["syl"]]
    lead.append(dict(on=n["on"], dur=n["dur"], midi=n["p"], sec=sec, line=i, syl=n["syl"], first=not n["slur"], text=t, hyph=hy,
                     stress=P.LINES[sec][i][n["syl"]][1], role=M.WORDS_OF[sec][i][0], singer=singer(sec, i)))
SC = sorted(p for p in range(48, 90) if p % 12 in M.SCALE)
def harm_note(p, t):
    """Lark's harmony: a third above in D major, a chord tone where one is a third away; at most D5."""
    ch = M.chord_at(t); up = [q for q in SC if 3 <= q - p <= 4]
    tones = [q for q in up if q % 12 in M.CH[ch][1]]
    q = (tones or up)[0]
    return q if q <= 74 else p                                                        # over D5: the unison (never above her row)
harm = []
for x in lead:
    if (x["sec"] == "Chorus 2" or x["sec"] == "Last Chorus") and x["singer"] == "Briar":
        harm.append(dict(on=x["on"], dur=x["dur"], midi=harm_note(x["midi"], x["on"]), sec=x["sec"], line=x["line"], syl=x["syl"], first=x["first"], text=x["text"], hyph=x["hyph"]))
ROOT = {k: v[0] for k, v in M.CH.items()}
def root_bass(ch): return 36 + ROOT[ch] % 12
def fifth(ch): return root_bass(ch) + 7
def power(ch, lo=45): r = lo + (ROOT[ch] - lo) % 12; return [r, r + 7, r + 12]
def chord3(ch, lo):
    out, p = [], lo
    while len(out) < 3:
        if p % 12 in M.CH[ch][1]: out.append(p)
        p += 1
    return out
OPEN = {"D": [50, 57, 62, 66], "C": [48, 52, 55, 60, 64], "G": [43, 47, 50, 55, 59, 67], "A": [45, 52, 57, 61, 64], "Bm": [47, 54, 59, 62, 66], "Em": [40, 47, 52, 55, 59, 64]}
MANDO = {"D": [62, 69, 74, 78], "C": [60, 67, 72, 76], "G": [55, 62, 71, 74], "A": [57, 64, 69, 73], "Bm": [59, 66, 71, 74], "Em": [55, 64, 71, 76]}
D = dict(kick=36, snare=38, hh=42, crash=49, ride=51, tomh=48, tomm=45, toml=41, tamb=54)
drums, perc, bass, rgtr, strings, lgtr, mando, acou = [], [], [], [], [], [], [], []
def ev(lst, on, dur, p, vel, art=""): lst.append(dict(on=on, dur=dur, p=p if isinstance(p, list) else [p], vel=vel, art=art))
def approach(cur, nxt):
    a, b = root_bass(cur), root_bass(nxt)
    if a == b: return a + 7
    for d in (-2, 2, -1, 1):
        if (b + d) % 12 in M.SCALE | {0}: return b + d if abs(b + d - a) <= 7 else b + d - 12 if b + d - 12 >= 33 else b + d
    return b - 5 if b - 5 >= 33 else b + 7
BAND = ("Chorus", "Solo")
riff_bars = {b for _, b in RF["bars"]}
for bi, b in enumerate(bars):
    sec, kind, ch, st, k, n = b["sec"], b["kind"], b["chord"], b["start"], b["k"], b["n"]
    nxt = bars[bi + 1]["chord"] if bi + 1 < NB else ch; nkind = bars[bi + 1]["kind"] if bi + 1 < NB else None
    r = root_bass(ch); top = sec == "Last Chorus"; band = kind in BAND
    lift = {"Chorus 2": 4, "Last Chorus": 10, "Riff break": -12}.get(sec, 0)                     # each chorus bigger; the break under the last chorus
    if kind == "Outro" and k == 3:                                                  # one D chord, left to ring
        ev(mando, st, BAR, MANDO[ch], 92, "ring"); ev(acou, st, BAR, OPEN[ch], 96, "ring"); ev(strings, st, BAR, chord3(ch, 62), 70, "ring")
        ev(bass, st, BAR, [r], 96, "ring"); ev(perc, st, 6, [D["toml"]], 84)
        continue
    # ---- mandolin: the riff in its bars; strummed eighths elsewhere ----
    if bi not in riff_bars and kind != "Intro":
        for j, e in enumerate(range(0, BAR, 6)): ev(mando, st + e, 6, MANDO[ch][:3] if j % 2 else MANDO[ch], (80 if j % 2 == 0 else 66) + (8 if band else 0), "strum")
    # ---- acoustic guitar: from intro bar 5 ----
    if not (kind == "Intro" and k < 4):
        for j, e in enumerate(range(0, BAR, 6)):
            down = j in (0, 2, 3, 5, 6); ev(acou, st + e, 6, OPEN[ch] if down else OPEN[ch][-3:], (84 if j % 2 == 0 else 70) + (6 if band else 0) - (0 if down else 6), "strum")
    # ---- percussion (the folk sections) and drums (the band's) ----
    if band:
        kicks = (0, 24, 30)
        for e in kicks: ev(drums, st + e, 3, D["kick"], (110 if e == 0 else 100) + lift)
        for e in (12, 36): ev(drums, st + e, 3, D["snare"], 112 + lift)
        [ev(drums, st + e, 3, D["ride"], (80 if e % 12 == 0 else 64) + lift) for e in range(0, 48, 6)]
        if k == 0: ev(drums, st, 3, D["crash"], 120)
        if top and k % 4 == 0 and k: ev(drums, st, 3, D["crash"], 114)
        if sec == "Chorus 2": [ev(perc, st + e, 3, D["tamb"], 84) for e in (12, 36)]                  # each chorus a little bigger
        if top: [ev(perc, st + e, 3, D["tamb"], 90 if e % 12 == 0 else 80) for e in range(0, 48, 6)]
    elif not (kind == "Intro" and k < 4) and kind != "Outro":
        toms = (0, 12, 24, 36) if kind == "Pre" else (0, 24)
        for e in toms: ev(perc, st + e, 6, D["toml"], (84 if kind == "Pre" else 74) + (4 * k if kind == "Pre" else 0))
        for e in (12, 36): ev(perc, st + e, 3, D["tamb"], 58 if kind != "Bridge" else 50)
    elif kind == "Outro":
        for e in (0, 24): ev(perc, st + e, 6, D["toml"], 70)
    if nkind in BAND and kind not in BAND:                                         # the storm arrives: a fill into the chorus or the break
        ev(drums, st + 24, 3, D["crash"], 70)
        for j, e in enumerate(range(24, 48, 3)): ev(drums, st + e, 3, [D["snare"], D["tomh"], D["tomm"], D["toml"]][j // 2 % 4], 88 + j * 3)
    # ---- bass ----
    if kind in ("Pre",):
        ev(bass, st, 23, r, 92); ev(bass, st + 24, 23, r if k % 2 == 0 else approach(ch, nxt), 88)
    elif kind == "Bridge": ev(bass, st, 46, r, 88)
    elif band:
        cell = [r, r, fifth(ch), r, r, r + 12, fifth(ch), approach(ch, nxt)]
        for j, p in enumerate(cell): ev(bass, st + 6 * j, 5, p, (104 if j % 2 == 0 else 92) + lift)
    # ---- electric rhythm guitar ----
    if band:
        if kind == "Solo": [ev(rgtr, st + e, 10, power(ch), 88, "open") for e in range(0, 48, 12)]          # the break leaves room for the solo
        else: [ev(rgtr, st + e, 5, power(ch), (96 if e % 12 == 0 else 84) + (6 if top else 0), "open") for e in range(0, 48, 6)]
    # ---- strings ----
    if kind == "Pre": ev(strings, st, 46, chord3(ch, 62), 56 + 8 * k, "swell")
    elif kind in ("Chorus", "Bridge", "Solo"):
        voic = chord3(ch, 62) + ([chord3(ch, 74)[0]] if top else [])
        ev(strings, st, 46, voic, (72 if kind != "Bridge" else 64) + (6 if top else 0), "pad")
# ---- the mandolin riff ----
for e in RF["mandolin"]:
    vel = 92 if e["where"] in ("intro", "outro") else 76 if e["where"] == "riff break" else 70           # under Lark: back
    mando.append(dict(on=e["on"], dur=e["dur"], p=e["p"], vel=vel + (8 if e["top"] else 0), art="riff:" + e["where"]))
for f in RF["fills"]:
    for e in f["notes"]: ev(lgtr, e["on"], e["dur"], e["p"], 90, "fill:" + f["gap"]["after"])
for e in RF["solo"]: ev(lgtr, e["on"], e["dur"], e["p"], 88, "solo")
for lst in (drums, perc, bass, rgtr, strings, lgtr, mando, acou): lst.sort(key=lambda e: (e["on"], e["p"][0]))
plan = [(nm, nb, P.BAR0[nm], "4/4") for nm, _, nb in P.FORM]
secs = NB * 4 * 60 / QB
rec = dict(title="Nothing Else on Earth", nbars=NB, bars=bars, plan=plan, lead=lead, harm=harm, drums=drums, perc=perc, bass=bass, rgtr=rgtr, strings=strings,
           lgtr=lgtr, mando=mando, acou=acou, slot="twelfth of a beat", bar=BAR, qbpm=QB, seconds=secs, tw_sec=60 / QB / 12, fp=c["fp"],
           order_fp=F["run"]["order_fp"], survivors=F["run"]["survivors"], built=F["run"]["made"], meas={k: (float(v) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()},
           judge={k: c["judge"][k] for k in ("combined", "content", "order")}, plans=c["meta"]["plans"], hand_edits=c["hand_edits"], picked_from=c["picked_from"],
           rerun=F["run"]["rerun"], text=TEXT, lift=c["info"]["lift"], design=dict(hook_top=P.HOOK_TOP, hook_end=P.HOOK_END, gates=P.DESIGN_GATES),
           riff=dict(RF["pick"], drawn=RF["drawn"], passed=RF["passed"], seed=RF["seed"], solo_check=RF["solo_check"], fills=len(RF["fills"]), gaps=len(RF["gaps"]), fill_stats=RF["fill_stats"]))
pickle.dump(rec, open("/home/claude/p40/song_record_d.pkl", "wb"))
print(NB, "bars,", f"{secs:.0f} s;", len(lead), "sung (", sum(x["singer"] == "Lark" for x in lead), "Lark,", sum(x["singer"] == "Briar" for x in lead), "Briar ),", len(harm), "harmony;",
      {k: len(v) for k, v in dict(drums=drums, perc=perc, bass=bass, rgtr=rgtr, strings=strings, lgtr=lgtr, mando=mando, acou=acou).items()})
print("harmony range", min(h["midi"] for h in harm), max(h["midi"] for h in harm))
