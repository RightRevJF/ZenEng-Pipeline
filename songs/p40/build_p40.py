"""Build the song record for 'Nothing Else on Earth' (song 40) from the shortlist pick (255; melody_main.pkl 'pick', no hand edits).
Times in twelfths of a beat (a bar is 48) at q = 116, D major, 110 bars. A riff-led rock band (the writer's Q5 A), light touch:
  lgtr     the riff (electric guitar, low): intro bars 1-8 (alone in bars 1-4), the outro's first three bars; the fills; the riff break.
  drums    enter at intro bar 5 (236: kept median bar 3, 2-6). Intro 5-8 and the verses: half time (the writer's B at Q19: Bonham
           style), kick on 1 and the 'and' of 2, snare on 3, eighth hats. Pre-choruses, choruses, bridge and riff break: the full beat,
           kick on 1 and 3 (and the 'and' of 3), snare on 2 and 4, eighths on the hats (the ride in the choruses and the break), a
           crash at each chorus's and the break's first bar and every 4 bars of the last chorus. A fill in each section's last bar.
           The outro: half time for three bars, then one hit (kick and crash), left to ring.
  bass     from the verse. 233: the root on beat 1 of every bar and at each change; a cell per section: in the verses the kick's
           half-time cell (R . . R | R . . approach); in the pre R R 5 approach in quarters; eighths R R 5 R R 8 5 approach in the
           choruses and the break; R 5 R approach in quarters in the bridge; roots in the outro.
  rgtr     power chords (root, fifth, octave), from the verse: let ring on beat 1 and the 'and' of 2 in the verses, quarters in the
           pre, open eighths in the choruses and the break, held in the bridge.
  keys     electric piano (237's chordal part, MIDI 55-74): half notes in the verses, quarters in the pre and choruses, an eighth-note
           arpeggio in the bridge.
  strings  a held pad from the pre-chorus on (three-note chords from MIDI 62), swelling in each pre-chorus, held through the choruses,
           the bridge and the break.
No backing vocals, no countermelody (Q18 A), no stop bars."""
import pickle, sys
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p40"]
import melody_p40 as P
M = P.M
import pyphen
import lyric_p40 as L
R = pickle.load(open("/home/claude/p40/melody_main.pkl", "rb")); c = R["pick"]
RF = pickle.load(open("/home/claude/p40/riff_p40.pkl", "rb"))
import riff_p40 as RV
BAR = 48; NB = P.NBARS; QB = 116
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"ivy": ["i", "vy"], "letters": ["let", "ters"], "every": ["ev", "ery"], "above": ["a", "bove"], "someone": ["some", "one"], "planted": ["plant", "ed"],
        "welcome,": ["wel", "come,"], "window": ["win", "dow"], "very": ["ver", "y"], "today.": ["to", "day."], "Nobody": ["No", "bod", "y"],
        "nobody": ["no", "bod", "y"], "honey": ["hon", "ey"], "pepper,": ["pep", "per,"], "oven": ["ov", "en"], "hungry": ["hun", "gry"],
        "bitter": ["bit", "ter"], "careful": ["care", "ful"], "pleasant": ["pleas", "ant"], "little": ["lit", "tle"], "reminds": ["re", "minds"],
        "gardens": ["gar", "dens"], "another": ["an", "oth", "er"], "table,": ["ta", "ble,"], "before.": ["be", "fore."], "bottle": ["bot", "tle"],
        "opened": ["o", "pened"], "instead": ["in", "stead"], "thistle": ["this", "tle"], "shadow": ["shad", "ow"], "winter,": ["win", "ter,"],
        "Every": ["Ev", "ery"], "Nothing": ["Noth", "ing"], "nothing": ["noth", "ing"]}
def split_words(text, sy):
    out = []; ws = text.replace(" —", "—").replace('"', "").split()
    for w in ws:
        n = len(P.syl(w.replace("-", " ").replace("—", "")))
        key = w; core = key.rstrip(",.;:—")
        if n <= 1: out.append((w, False)); continue
        parts = HFIX.get(key) or HFIX.get(core) or HFIX.get(core.lower()) or _PY.inserted(core).split("-")
        if len(parts) > n: parts = parts[:n - 1] + ["".join(parts[n - 1:])]
        while len(parts) < n: parts.append("_")
        tail = w[len(core):] if key not in HFIX else ""
        for j, p in enumerate(parts):
            t = p + (tail if j == n - 1 else "")
            if j == 0 and w[0].isupper(): t = t[0].upper() + t[1:]
            out.append((t, j < n - 1))
    assert len(out) == len(sy), (text, out, sy)
    return out
TEXT = {sec: [split_words(t, P.LINES[sec][i]) for i, (_, t) in enumerate(M.WORDS_OF[sec])] for sec in P.SUNG}
bars = []
for nm, kind, nb in P.FORM:
    for k in range(nb):
        b = P.BAR0[nm] + k
        bars.append(dict(sec=nm, kind=kind, k=k, n=nb, chord=P.CHORD[b], roman=M.ROMAN[P.CHORD[b]], start=b * BAR, len=BAR, qbpm=QB, key="D major", stop=False))
lead = []
for n in c["notes"]:
    sec, i = n["line"].split(":"); i = int(i)
    t, hy = TEXT[sec][i][n["syl"]]
    lead.append(dict(on=n["on"], dur=n["dur"], midi=n["p"], sec=sec, line=i, syl=n["syl"], first=not n["slur"], text=t, hyph=hy,
                     stress=P.LINES[sec][i][n["syl"]][1], role=M.WORDS_OF[sec][i][0]))
ROOT = {k: v[0] for k, v in M.CH.items()}
def root_bass(ch): return 36 + ROOT[ch] % 12                                  # C2 .. B2
def fifth(ch): return root_bass(ch) + 7
def power(ch, lo=45): r = lo + (ROOT[ch] - lo) % 12; return [r, r + 7, r + 12]
def chord3(ch, lo):
    out, p = [], lo
    while len(out) < 3:
        if p % 12 in M.CH[ch][1]: out.append(p)
        p += 1
    return out
D = dict(kick=36, snare=38, hh=42, ohh=46, crash=49, ride=51, tomh=48, tomm=45, toml=41)
drums, bass, rgtr, keys, strings, lgtr = [], [], [], [], [], []
def ev(lst, on, dur, p, vel, art=""): lst.append(dict(on=on, dur=dur, p=p if isinstance(p, list) else [p], vel=vel, art=art))
def approach(cur, nxt):
    """the bass's last note: a step or a fifth into the next root (233)."""
    a, b = root_bass(cur), root_bass(nxt)
    if a == b: return a + 7
    for d in (-2, 2, -1, 1):
        if (b + d) % 12 in M.SCALE | {0}: return b + d if abs(b + d - a) <= 7 else b + d - 12 if b + d - 12 >= 33 else b + d
    return b - 5 if b - 5 >= 33 else b + 7
for bi, b in enumerate(bars):
    sec, kind, ch, st, k, n = b["sec"], b["kind"], b["chord"], b["start"], b["k"], b["n"]
    nxt = bars[bi + 1]["chord"] if bi + 1 < NB else ch
    r = root_bass(ch); top = sec == "Last Chorus"; full = kind in ("Pre", "Chorus", "Bridge", "Solo")
    half = kind in ("Verse",) or (kind == "Intro" and k >= 4) or (kind == "Outro" and k < 3)
    if kind == "Outro" and k == 3:                                                  # the last hit, left to ring
        ev(drums, st, 3, [D["kick"], D["crash"]], 124); ev(bass, st, BAR, [r, r + 12], 110); ev(rgtr, st, BAR, power(ch), 108, "ring")
        ev(strings, st, BAR, chord3(ch, 62), 76, "ring"); ev(keys, st, BAR, chord3(ch, 55), 80, "ring")
        continue
    # ---- drums ----
    if kind == "Intro" and k < 4: pass
    elif half:
        for e in (0, 18): ev(drums, st + e, 3, D["kick"], 112 if e == 0 else 100)
        ev(drums, st + 24, 3, D["snare"], 116)
        [ev(drums, st + e, 3, D["hh"], 80 if e % 12 == 0 else 62) for e in range(0, 48, 6)]
        if kind == "Intro" and k == 4: ev(drums, st, 3, D["crash"], 116)
    else:
        kicks = (0, 24, 30) if kind in ("Pre", "Chorus", "Solo") else (0, 24)
        for e in kicks: ev(drums, st + e, 3, D["kick"], (112 if e == 0 else 102) + (4 if top else 0))
        for e in (12, 36): ev(drums, st + e, 3, D["snare"], 114 + (4 if top else 0))
        cym = D["ride"] if kind in ("Chorus", "Solo") else D["hh"]
        [ev(drums, st + e, 3, cym, (84 if e % 12 == 0 else 68) + (6 if top else 0)) for e in range(0, 48, 6)]
        if k == 0 and kind in ("Chorus", "Solo"): ev(drums, st, 3, D["crash"], 120)
        if top and k % 4 == 0 and k: ev(drums, st, 3, D["crash"], 114)
    last_of_sec = k == n - 1 and kind != "Outro"
    if last_of_sec and not (kind == "Intro" and k < 4):                            # 236: a fill in the section's last bar
        drums[:] = [d for d in drums if not (st + 24 <= d["on"] < st + 48 and d["p"][0] in (D["snare"], D["hh"], D["ride"], D["kick"]) and not (d["on"] == st + 24 and d["p"][0] == D["kick"]))]
        for j, e in enumerate(range(24, 48, 3)): ev(drums, st + e, 3, [D["snare"], D["tomh"], D["tomm"], D["toml"]][j // 2 % 4], 92 + j * 2)
    # ---- bass ----
    if kind == "Intro": pass                                                        # 238: the intro under half the fullest (the riff and the drums)
    elif kind == "Outro": ev(bass, st, 18, r, 100); ev(bass, st + 18, 6, r, 92); ev(bass, st + 24, 22, r, 96)
    elif kind == "Verse":
        for e, d, p in ((0, 17, r), (18, 5, r), (24, 17, r), (42, 5, approach(ch, nxt))): ev(bass, st + e, d, p, 100 if e in (0, 24) else 90)
    elif kind in ("Bridge", "Pre"):
        for e, p in ((0, r), (12, r if kind == "Pre" else fifth(ch)), (24, fifth(ch) if kind == "Pre" else r), (36, approach(ch, nxt))): ev(bass, st + e, 11, p, 98)
    else:
        cell = [r, r, fifth(ch), r, r, r + 12, fifth(ch), approach(ch, nxt)]
        for j, p in enumerate(cell): ev(bass, st + 6 * j, 5, p, (106 if j % 2 == 0 else 94) + (4 if top else 0))
    # ---- rhythm guitar ----
    if kind in ("Intro", "Outro"): pass
    elif kind == "Verse": ev(rgtr, st, 17, power(ch), 84, "ring"); ev(rgtr, st + 18, 29, power(ch), 78, "ring")
    elif kind == "Bridge": ev(rgtr, st, 46, power(ch), 86, "held")
    elif kind == "Pre":
        for e in range(0, 48, 12): ev(rgtr, st + e, 10, power(ch), 90, "open")
    else:
        for e in range(0, 48, 6): ev(rgtr, st + e, 5, power(ch), (98 if e % 12 == 0 else 86) + (6 if top else 0), "open")
    # ---- keys: electric piano ----
    if kind == "Verse":
        for e in (0, 24): ev(keys, st + e, 23, chord3(ch, 55), 70, "half")
    elif kind in ("Pre", "Chorus"):
        for e in range(0, 48, 12): ev(keys, st + e, 11, chord3(ch, 55), 72 + (6 if top else 0), "quarters")
    elif kind == "Bridge":
        tones = chord3(ch, 55) + [chord3(ch, 55)[0] + 12]
        for j, p in enumerate(tones + tones[-2:0:-1] + tones[:1] * 0): ev(keys, st + 6 * j, 6, p, 68 + (6 if j % 2 == 0 else 0), "arp")
    # ---- strings: the pad ----
    if kind == "Pre": ev(strings, st, 46, chord3(ch, 62), 58 + 8 * k, "swell")
    elif kind in ("Chorus", "Bridge", "Solo"): ev(strings, st, 46, chord3(ch, 62), 74 + (6 if top else 0), "pad")
# ---- the lead guitar: the riff, the fills, the riff break ----
RONS, RSTEPS = RF["pick"]["ons"], RF["pick"]["steps"]
for sl in RF["slots"]:
    pl = RV.place(RONS, RSTEPS, sl)
    for j, (t, p) in enumerate(pl):
        nx = pl[j + 1][0] if j + 1 < len(pl) else min(sl["end"], t + 12)
        ev(lgtr, t, max(3, nx - t), p, 100, "riff:" + sl["where"])
for f in RF["fills"]:
    for e in f["notes"]: ev(lgtr, e["on"], e["dur"], e["p"], 90, "fill:" + f["gap"]["after"])
for e in RF["solo"]: ev(lgtr, e["on"], e["dur"], e["p"], 96, "solo")
for lst in (drums, bass, rgtr, keys, strings, lgtr): lst.sort(key=lambda e: (e["on"], e["p"][0]))
plan = [(nm, nb, P.BAR0[nm], "4/4") for nm, _, nb in P.FORM]
secs = NB * 4 * 60 / QB
rec = dict(title=L.TITLE, nbars=NB, bars=bars, plan=plan, lead=lead, drums=drums, bass=bass, rgtr=rgtr, keys=keys, strings=strings, lgtr=lgtr,
           slot="twelfth of a beat", bar=BAR, qbpm=QB, seconds=secs, tw_sec=60 / QB / 12, fp=c["fp"], order_fp=R["order_fp"],
           survivors=R["survivors"], built=R["made"], deaths=dict(R["deaths"]), meas={k: (float(v) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()},
           judge={k: c["judge"][k] for k in ("combined", "content", "order")}, plans=c["meta"]["plans"], targets=c["meta"]["targets"], windows=c["meta"]["win"],
           registers=c["meta"]["registers"], lift=c["info"].get("lift"),
           kinds={f"{a}:{b}": v for (a, b), v in c["meta"]["kinds"].items()}, hand_edits=[], rerun=R["rerun"], text=TEXT, read=c["read"],
           stop_bars=[], summit=None, drums_design=P.__dict__.get("DRUMS", "half-time verses (Q19 B)"),
           riff=dict(RF["pick"], slots=[s_["where"] for s_ in RF["slots"]], drawn=RF["drawn"], passed=RF["passed"], seed=RF["seed"], solo_check=RF["solo_check"],
                     fills=len(RF["fills"]), gaps=len(RF["gaps"]), fill_stats=RF["fill_stats"]))
pickle.dump(rec, open("/home/claude/p40/song_record.pkl", "wb"))
print(NB, "bars,", f"{secs:.0f} s ({int(secs // 60)}:{int(round(secs % 60)):02d});", len(lead), "sung;", len(drums), "drums;", len(bass), "bass;",
      len(rgtr), "rhythm;", len(keys), "keys;", len(strings), "strings;", len(lgtr), "lead; fp", rec["fp"])
for sec in P.SUNG:
    for i, ws in enumerate(TEXT[sec]): print(sec, i, " ".join(t + ("-" if h else "") for t, h in ws))
