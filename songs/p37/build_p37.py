"""Build the song record for 'Windows Down' (song 37) from the pick (melody_main.pkl, first by the rank of record, no hand edits).
Times in twelfths of a beat (a bar is 48) at q = 122, A major throughout, 112 bars. A heartland rock band:
  drums    straight eighths on the hat (the ride in the choruses, the solo and the last chorus), kick on 1 and 3 with the 'and' of 3,
           snare on 2 and 4; the intro's first four bars the guitar alone; a tom fill into each chorus; the bridge half-time (kick on 1,
           snare on 3) for six bars, then a snare build; a crash every four bars in the last chorus; one hit on bar 112.
  bass     driving eighths on the root from bar 5 (the verses), the octave on the 'and' of 4 in the choruses; the bridge in half notes
           until its build.
  rhythm   power chords (root, fifth, octave) in palm-muted eighths in the verses, open eighths in the choruses, the solo and the outro,
           held chords in the bridge; from bar 5.
  organ    held chords in the pre-choruses, choruses, bridge, the solo's second half and the outro; the last chorus voiced higher, with
           the open hat on every 'and' and a pickup on the snare, so it is the top of the song.
  lead     the instrumental hook (209): intro bars 1-8, the holds after chorus lines, outro bars 105-111; the 16-bar solo."""
import pickle, sys, os
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p37"]
import melody_p37 as P
M = P.M
import pyphen
import lyric_p37 as L
R = pickle.load(open("/home/claude/p37/melody_main.pkl", "rb")); c = R["alive"][0]
RF = pickle.load(open("/home/claude/p37/riff_p37.pkl", "rb"))
import riff_p37 as RV
BAR = 48; NB = P.NBARS; QB = 122
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"minutes": ["min", "utes"], "always": ["al", "ways"], "someday;": ["some", "day;"], "picture": ["pic", "ture"], "locker": ["lock", "er"],
        "away.": ["a", "way."], "shadow's": ["shad", "ow's"], "under": ["un", "der"], "doesn't": ["does", "n't"], "windows": ["win", "dows"], "Windows": ["Win", "dows"],
        "heater": ["heat", "er"], "number": ["num", "ber"], "Number": ["Num", "ber"], "quiet,": ["qui", "et,"], "quiet": ["qui", "et"], "hollering": ["hol", "ler", "ing"],
        "didn't": ["did", "n't"], "nineteen": ["nine", "teen"], "twenty-six": ["twen", "ty", "six"], "almost": ["al", "most"], "little": ["lit", "tle"]}
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
        bars.append(dict(sec=nm, kind=kind, k=k, n=nb, chord=P.CHORD[b], roman=M.ROMAN[P.CHORD[b]], start=b * BAR, len=BAR, qbpm=QB, key="A major"))
lead = []
for n in c["notes"]:
    sec, i = n["line"].split(":"); i = int(i)
    t, hy = TEXT[sec][i][n["syl"]]
    lead.append(dict(on=n["on"], dur=n["dur"], midi=n["p"], sec=sec, line=i, syl=n["syl"], first=not n["slur"], text=t, hyph=hy,
                     stress=P.LINES[sec][i][n["syl"]][1], role=M.WORDS_OF[sec][i][0]))
ROOT = {k: v[0] for k, v in M.CH.items()}
def root_bass(ch): return 40 + (ROOT[ch] - 4) % 12             # E2 .. D#3
def power(ch, lo=45): r = lo + (ROOT[ch] - lo) % 12; return [r, r + 7, r + 12]
def triad(ch, lo):
    out, p = [], lo
    while len(out) < 3:
        if p % 12 in M.CH[ch][1]: out.append(p)
        p += 1
    return out
D = dict(kick=36, snare=38, hh=42, ohh=46, crash=49, ride=51, tomh=48, tomm=45, toml=41)
drums, bass, rgtr, organ, lgtr = [], [], [], [], []
def ev(lst, on, dur, p, vel, art=""): lst.append(dict(on=on, dur=dur, p=p if isinstance(p, list) else [p], vel=vel, art=art))
for bi, b in enumerate(bars):
    sec, kind, ch, st, k, n = b["sec"], b["kind"], b["chord"], b["start"], b["k"], b["n"]
    last_song_bar = bi == NB - 1; r = root_bass(ch)
    big = kind in ("Chorus", "Solo") or (kind == "Outro" and not last_song_bar); top = sec == "Last Chorus"
    if last_song_bar:
        ev(drums, st, 3, [D["kick"], D["crash"]], 120); ev(bass, st, 36, [r, r + 12], 106); ev(rgtr, st, 36, power(ch), 100); ev(organ, st, 48, triad(ch, 57), 76)
        continue
    # ---- drums ----
    if kind == "Intro" and k < 4: pass
    elif kind == "Bridge" and k < n - 2:
        ev(drums, st, 3, D["kick"], 96); ev(drums, st + 24, 3, D["snare"], 100)
        [ev(drums, st + e, 3, D["hh"], 58) for e in range(0, 48, 12)]
    elif kind == "Bridge":
        [ev(drums, st + e, 3, D["kick"], 100) for e in range(0, 48, 12)]
        [ev(drums, st + e, 3, D["snare"], min(122, 74 + (k - n + 2) * 24 + e // 2)) for e in range(0, 48, 6 if k == n - 2 else 3)]
    else:
        for e in (0, 24, 30): ev(drums, st + e, 3, D["kick"], 110 if e == 0 else 100)
        for e in (12, 36): ev(drums, st + e, 3, D["snare"], 114 if big else 104)
        cym = D["ride"] if big and not (kind == "Solo" and k < 8) else D["hh"]          # the solo builds: hats for 8 bars, then the ride
        [ev(drums, st + e, 3, cym, (82 if e % 12 == 0 else 66) + (6 if top else 0)) for e in range(0, 48, 6)]
        if k == 0 and kind in ("Chorus", "Solo"): ev(drums, st, 3, D["crash"], 118)
        if top and k % 4 == 0 and k: ev(drums, st, 3, D["crash"], 112)
        if top: [ev(drums, st + e, 3, D["ohh"], 70) for e in range(6, 48, 12)]                 # the last chorus: the open hat on every 'and'
        if top: [ev(drums, st + e, 3, D["snare"], 70) for e in (42, 45)]
        if kind == "Intro" and k == 4: ev(drums, st, 3, D["crash"], 114)
        if kind == "Pre" and k == n - 1:                                          # a tom fill into the chorus
            drums[:] = [d for d in drums if not (st + 24 <= d["on"] < st + 48 and d["p"][0] in (D["snare"], D["hh"], D["ride"]))]
            for j, e in enumerate(range(24, 48, 3)): ev(drums, st + e, 3, [D["tomh"], D["tomm"], D["toml"]][j // 3 % 3], 92 + j * 2)
    # ---- bass: driving eighths ----
    if kind == "Intro" and k < 4: pass
    elif kind == "Bridge" and k < n - 2: ev(bass, st, 22, r, 94); ev(bass, st + 24, 22, r, 90)
    else:
        for e in range(0, 48, 6):
            p = r + 12 if (big and e == 42) else r
            ev(bass, st + e, 5, p, (104 if e % 12 == 0 else 92) + (4 if top else 0))
    # ---- rhythm guitar: power chords ----
    if kind == "Intro" and k < 4: pass
    elif kind == "Bridge" and k < n - 2: ev(rgtr, st, 46, power(ch), 84, "held")
    elif kind == "Verse" or (kind == "Intro"):
        for e in range(0, 48, 6): ev(rgtr, st + e, 4, power(ch), 80 if e % 12 == 0 else 70, "mute")
    else:
        lift = -12 if (kind == "Solo" and k < 8) else (6 if top else 0)
        for e in range(0, 48, 6): ev(rgtr, st + e, 5, power(ch), (96 if e % 12 == 0 else 84) + lift, "open")
    # ---- organ ----
    if kind in ("Pre", "Chorus", "Bridge", "Outro") or (kind == "Solo" and k >= 8):           # the organ enters the solo halfway
        ev(organ, st, 47, triad(ch, 64 if top else 57), 66 if kind != "Bridge" else 72, "pad")
# ---- the lead guitar: the hook in its slots, the solo ----
RONS, RSTEPS = RF["pick"]["ons"], RF["pick"]["steps"]
for sl in RF["slots"]:
    pl = RV.place(RONS, RSTEPS, sl)
    for j, (t, p) in enumerate(pl):
        nxt = pl[j + 1][0] if j + 1 < len(pl) else min(sl["end"], t + 12)
        ev(lgtr, t, max(3, nxt - t), p, 96, "hook:" + sl["where"])
for e in RF["solo"]: ev(lgtr, e["on"], e["dur"], e["p"], 92, "solo")
lgtr = [s for s in lgtr if s["on"] < (NB - 1) * BAR]
for lst in (drums, bass, rgtr, organ, lgtr): lst.sort(key=lambda e: (e["on"], e["p"][0]))
plan = [(nm, nb, P.BAR0[nm], "4/4") for nm, _, nb in P.FORM]
secs = NB * 4 * 60 / QB
rec = dict(title=L.TITLE, nbars=NB, bars=bars, plan=plan, lead=lead, drums=drums, bass=bass, rgtr=rgtr, organ=organ, lgtr=lgtr,
           slot="twelfth of a beat", bar=BAR, qbpm=QB, seconds=secs, tw_sec=60 / QB / 12, fp=c["fp"], order_fp=R["order_fp"], survivors=R["survivors"],
           built=R["made"], deaths=dict(R["deaths"]), meas={k: (float(v) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()},
           plans=c["meta"]["plans"], targets=c["meta"]["targets"], hand_edits=[], rerun=R["rerun"], text=TEXT, read=c["read"],
           riff=dict(RF["pick"], slots=[s_["where"] for s_ in RF["slots"]], drawn=RF["drawn"], passed=RF["passed"], seed=RF["seed"], solo_check=RF["solo_check"]))
pickle.dump(rec, open("/home/claude/p37/song_record.pkl", "wb"))
print(NB, "bars,", f"{secs:.0f} s ({int(secs // 60)}:{int(round(secs % 60)):02d});", len(lead), "sung;", len(drums), "drums;", len(bass), "bass;",
      len(rgtr), "rhythm;", len(organ), "organ;", len(lgtr), "lead; fp", rec["fp"])
