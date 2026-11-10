"""Build the song record for 'Stay Tuned' (song 38) from the shortlist pick (255; melody_main.pkl 'pick', no hand edits).
Times in twelfths of a beat (a bar is 48) at q = 132, A major, 114 bars. A Who-style rock band (the writer's Q1, Q3, Q11, Q12):
  keys     the pulse: a one-bar eighth-note figure on the chord (root, fifth, octave, fifth, root, fifth, octave, third), alone in
           intro bars 1-4, then under the verses, pre-choruses, choruses, solo and breakdown; out in the bridge. It is the set's hum.
  drums    enter at intro bar 5 (236: kept median bar 3, 2-6). Verses, pre-choruses and the bridge: a rock beat, kick on 1 and 3 (and the
           'and' of 3 in the pre), snare on 2 and 4, eighth hats. Choruses and the solo: four on the floor (the writer's B), snare 2
           and 4, the ride in eighths, a crash at each chorus's first bar and every 4 bars of the last chorus. The breakdown: kick on 1
           and 3 and the hats only for 4 bars, then the snare in eighths building. A fill in the last bar of each section (10 fills).
           Two bars of nothing under 'Turn it off.' Then one hit (kick and crash) on the outro's first beat, left to ring.
  intro    bars 1-4 the pulse alone; bars 5-8 the drums and the lead guitar's tune join it (238: under half the fullest).
  bass     from the verse. 233: the root on beat 1 of every bar and at each change; a cell per section, held: eighths R R 5 R R 8 5 (approach) in the
           verses, pre and choruses; R 5 R (approach) in quarters in the bridge; half notes in the breakdown's first 4 bars.
  rhythm   power chords (root, fifth, octave), from the verse: palm-muted eighths in the verses, quarters in the pre, open eighths in the choruses and
           the solo, held in the bridge.
  organ    the chordal part (237): three-note chords between MIDI 51 and 71: held from beat 1 in the pre and the bridge, quarters in
           the choruses; the last chorus adds the countermelody above the voice (the writer's B at Q11).
  bvox     chorus 2: a gang vocal an octave under on the chant lines; the last chorus adds a third under on them (each chorus bigger).
  lead     the intro tune (intro bars 5-8, breakdown bars 5-8), the fills, the 8-bar solo."""
import pickle, sys
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p38"]
import melody_p38 as P
M = P.M
import pyphen
import lyric_p38 as L
R = pickle.load(open("/home/claude/p38/melody_main.pkl", "rb")); c = R["pick"]
RF = pickle.load(open("/home/claude/p38/riff_p38.pkl", "rb"))
import riff_p38 as RV
BAR = 48; NB = P.NBARS; QB = 132
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"powders": ["pow", "ders"], "camera": ["cam", "er", "a"], "every": ["ev", "ery"], "tonight.": ["to", "night."], "selling": ["sell", "ing"],
        "paying": ["pay", "ing"], "after": ["af", "ter"], "shouting": ["shout", "ing"], "laughing": ["laugh", "ing"], "downstairs": ["down", "stairs"],
        "billionaire": ["bil", "lion", "aire"], "Danny": ["Dan", "ny"], "other": ["oth", "er"], "ratings,": ["rat", "ings,"], "dial.": ["di", "al."]}
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
        b = P.BAR0[nm] + k; stop = b in P.STOP_BARS
        bars.append(dict(sec=nm, kind=kind, k=k, n=nb, chord="N.C." if stop else P.CHORD[b], roman="" if stop else M.ROMAN[P.CHORD[b]],
                         start=b * BAR, len=BAR, qbpm=QB, key="A major", stop=stop))
lead = []
for n in c["notes"]:
    sec, i = n["line"].split(":"); i = int(i)
    t, hy = TEXT[sec][i][n["syl"]]
    lead.append(dict(on=n["on"], dur=n["dur"], midi=n["p"], sec=sec, line=i, syl=n["syl"], first=not n["slur"], text=t, hyph=hy,
                     stress=P.LINES[sec][i][n["syl"]][1], role=M.WORDS_OF[sec][i][0]))
ROOT = {k: v[0] for k, v in M.CH.items()}
def root_bass(ch): return 40 + (ROOT[ch] - 4) % 12                      # E2 .. D#3
def fifth(ch): return root_bass(ch) + 7
def power(ch, lo=45): r = lo + (ROOT[ch] - lo) % 12; return [r, r + 7, r + 12]
def triad(ch, lo):
    out, p = [], lo
    while len(out) < 3:
        if p % 12 in M.CH[ch][1]: out.append(p)
        p += 1
    return out
D = dict(kick=36, snare=38, hh=42, ohh=46, crash=49, ride=51, tomh=48, tomm=45, toml=41)
drums, bass, rgtr, organ, lgtr, keys, bvox = [], [], [], [], [], [], []
def ev(lst, on, dur, p, vel, art=""): lst.append(dict(on=on, dur=dur, p=p if isinstance(p, list) else [p], vel=vel, art=art))
def approach(cur, nxt):
    """the bass's last eighth: a step or a fifth into the next root (233)."""
    a, b = root_bass(cur), root_bass(nxt)
    if a == b: return a + 7
    for d in (-2, 2, -1, 1):
        if (b + d) % 12 in M.SCALE | {7}: return b + d if abs(b + d - a) <= 7 else b + d - 12 if b + d - 12 >= 40 else b + d
    return b - 5 if b - 5 >= 40 else b + 7
for bi, b in enumerate(bars):
    sec, kind, ch, st, k, n = b["sec"], b["kind"], b["chord"], b["start"], b["k"], b["n"]
    if b["stop"]: continue                                                       # 'Turn it off.': the voice alone
    nxt = bars[bi + 1]["chord"] if bi + 1 < NB and not bars[bi + 1]["stop"] else ch
    if nxt == "N.C.": nxt = ch
    r = root_bass(ch); top = sec == "Last Chorus"; four = kind in ("Chorus", "Solo")
    if kind == "Outro":
        if k == 0:                                                               # the last hit, left to ring
            ev(drums, st, 3, [D["kick"], D["crash"]], 124); ev(bass, st, 4 * BAR, [r, r + 12], 110); ev(rgtr, st, 6 * BAR, power(ch), 108, "ring")
            ev(organ, st, 8 * BAR, triad(ch, 57), 80, "ring")
        continue
    # ---- keys: the pulse ----
    if kind != "Bridge":
        rk = 57 + (ROOT[ch] - 57) % 12; third = min(p for p in range(rk, rk + 12) if p % 12 in M.CH[ch][1] and p != rk and (p - rk) % 12 in (3, 4))
        pat = [rk, rk + 7, rk + 12, rk + 7, rk, rk + 7, rk + 12, third]
        for j, p in enumerate(pat): ev(keys, st + 6 * j, 5, p, (72 if j % 2 == 0 else 62) + (6 if four else 0) + (4 if top else 0), "pulse")
    # ---- drums ----
    intro_quiet = kind == "Intro" and k < 4
    if intro_quiet: pass
    elif kind == "Breakdown" and k < 4:
        for e in (0, 24): ev(drums, st + e, 3, D["kick"], 92)
        [ev(drums, st + e, 3, D["hh"], 56 if e % 12 else 64) for e in range(0, 48, 6)]
    elif kind == "Breakdown":
        for e in (0, 24): ev(drums, st + e, 3, D["kick"], 100)
        [ev(drums, st + e, 3, D["snare"], 60 + (k - 4) * 12 + e // 4) for e in range(0, 48, 6)]
        [ev(drums, st + e, 3, D["hh"], 70) for e in range(0, 48, 12)]
    else:
        kicks = (0, 12, 24, 36) if four else ((0, 24, 30) if kind == "Pre" else (0, 24))
        for e in kicks: ev(drums, st + e, 3, D["kick"], (112 if e == 0 else 104) + (4 if top else 0))
        for e in (12, 36): ev(drums, st + e, 3, D["snare"], (116 if four else 104) + (4 if top else 0))
        cym = D["ride"] if four else D["hh"]
        [ev(drums, st + e, 3, cym, (84 if e % 12 == 0 else 68) + (6 if top else 0)) for e in range(0, 48, 6)]
        if k == 0 and kind in ("Chorus", "Solo"): ev(drums, st, 3, D["crash"], 120)
        if kind == "Intro" and k == 4: ev(drums, st, 3, D["crash"], 116)
        if top and k % 4 == 0 and k: ev(drums, st, 3, D["crash"], 114)
    last_of_sec = k == n - 1 or (sec == "Last Chorus" and k == 15)
    if last_of_sec and not intro_quiet and kind not in ("Outro",):          # 236: a fill in the section's last bar
        drums[:] = [d for d in drums if not (st + 24 <= d["on"] < st + 48 and d["p"][0] in (D["snare"], D["hh"], D["ride"], D["kick"]) and not (d["on"] == st + 24 and d["p"][0] == D["kick"]))]
        for j, e in enumerate(range(24, 48, 3)): ev(drums, st + e, 3, [D["snare"], D["tomh"], D["tomm"], D["toml"]][j // 2 % 4], 92 + j * 2)
    # ---- bass ----
    if kind == "Intro": pass                                                      # 238: the intro under half the fullest (pulse, drums, the tune)
    elif kind == "Bridge":
        for e, p in ((0, r), (12, fifth(ch)), (24, r), (36, approach(ch, nxt))): ev(bass, st + e, 11, p, 98)
    elif kind == "Breakdown" and k < 4: ev(bass, st, 22, r, 90); ev(bass, st + 24, 22, r, 86)
    else:
        cell = [r, r, fifth(ch), r, r, r + 12, fifth(ch), approach(ch, nxt)]
        for j, p in enumerate(cell): ev(bass, st + 6 * j, 5, p, (106 if j % 2 == 0 else 94) + (4 if top else 0))
    # ---- rhythm guitar ----
    if kind == "Intro": pass
    elif kind == "Bridge": ev(rgtr, st, 46, power(ch), 86, "held")
    elif kind in ("Verse", "Intro", "Breakdown"):
        for e in range(0, 48, 6): ev(rgtr, st + e, 4, power(ch), (82 if e % 12 == 0 else 72) - (10 if kind == "Breakdown" and k < 4 else 0), "mute")
    elif kind == "Pre":
        for e in range(0, 48, 12): ev(rgtr, st + e, 10, power(ch), 92, "open")
    else:
        for e in range(0, 48, 6): ev(rgtr, st + e, 5, power(ch), (98 if e % 12 == 0 else 86) + (6 if top else 0), "open")
    # ---- organ: the chordal part ----
    if kind in ("Pre", "Bridge"): ev(organ, st, 46, triad(ch, 57), 70, "pad")
    elif kind == "Chorus":
        for e in range(0, 48, 12): ev(organ, st + e, 11, triad(ch, 57), 72 + (6 if top else 0), "stab")
    elif kind == "Solo": ev(organ, st, 46, triad(ch, 57), 70, "pad")
# ---- backing vocals on the chant lines: chorus 2 an octave under; the last chorus also a third under ----
def third_under(p, at):
    ch = M.chord_at(at); return max(q for q in range(p - 5, p - 2) if q % 12 in (M.SCALE | {7}) and not M.clash(q, ch))
for x in lead:
    if x["sec"] in ("Chorus 2", "Last Chorus") and x["line"] in (0, 1, 4):
        ev(bvox, x["on"], x["dur"], x["midi"] - 12, 84, "gang:" + x["text"])
        if x["sec"] == "Last Chorus": ev(bvox, x["on"], x["dur"], third_under(x["midi"], x["on"]), 78, "third:" + x["text"])
# ---- the lead guitar: the intro tune, the fills, the solo; the countermelody (organ) ----
RONS, RSTEPS = RF["pick"]["ons"], RF["pick"]["steps"]
for sl in RF["slots"]:
    pl = RV.place(RONS, RSTEPS, sl)
    for j, (t, p) in enumerate(pl):
        nx = pl[j + 1][0] if j + 1 < len(pl) else min(sl["end"], t + 12)
        ev(lgtr, t, max(3, nx - t), p, 96, "tune:" + sl["where"])
for f in RF["fills"]:
    for e in f["notes"]: ev(lgtr, e["on"], e["dur"], e["p"], 90, "fill:" + f["gap"]["after"])
for e in RF["solo"]: ev(lgtr, e["on"], e["dur"], e["p"], 94, "solo")
counter = [dict(on=e["on"], dur=e["dur"], p=[e["p"]], vel=74, art="counter") for e in RF["counter"]]
for lst in (drums, bass, rgtr, organ, lgtr, keys, bvox, counter): lst.sort(key=lambda e: (e["on"], e["p"][0]))
plan = [(nm, nb, P.BAR0[nm], "4/4") for nm, _, nb in P.FORM]
secs = NB * 4 * 60 / QB
rec = dict(title=L.TITLE, nbars=NB, bars=bars, plan=plan, lead=lead, drums=drums, bass=bass, rgtr=rgtr, organ=organ, lgtr=lgtr, keys=keys, bvox=bvox,
           counter=counter, slot="twelfth of a beat", bar=BAR, qbpm=QB, seconds=secs, tw_sec=60 / QB / 12, fp=c["fp"], order_fp=R["order_fp"],
           survivors=R["survivors"], built=R["made"], deaths=dict(R["deaths"]), meas={k: (float(v) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()},
           judge={k: c["judge"][k] for k in ("combined", "content", "order")}, plans=c["meta"]["plans"], targets=c["meta"]["targets"], windows=c["meta"]["win"],
           kinds={f"{a}:{b}": v for (a, b), v in c["meta"]["kinds"].items()}, hand_edits=[], rerun=R["rerun"], text=TEXT, read=c["read"],
           stop_bars=sorted(P.STOP_BARS), summit=P.SUMMIT,
           riff=dict(RF["pick"], slots=[s_["where"] for s_ in RF["slots"]], drawn=RF["drawn"], passed=RF["passed"], seed=RF["seed"], solo_check=RF["solo_check"],
                     fills=len(RF["fills"]), gaps=len(RF["gaps"]), fill_stats=RF["fill_stats"], counter_check=RF["counter_check"]))
pickle.dump(rec, open("/home/claude/p38/song_record.pkl", "wb"))
print(NB, "bars,", f"{secs:.0f} s ({int(secs // 60)}:{int(round(secs % 60)):02d});", len(lead), "sung;", len(drums), "drums;", len(bass), "bass;",
      len(rgtr), "rhythm;", len(organ), "organ;", len(keys), "keys;", len(bvox), "bvox;", len(lgtr), "lead;", len(counter), "counter; fp", rec["fp"])
