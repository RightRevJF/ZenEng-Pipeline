"""Build the song record for 'Fixed by Fall' (song 39) from the shortlist pick (255; melody_main.pkl 'pick', no hand edits).
Times in twelfths of a beat (a bar is 48) at q = 108, E major, 90 bars. Rock with a swagger (Q1, Q3, Q11, Q12):
  feel     the verses, bridge, solo, intro and outro a shuffle (eighths written straight, played swung: the demo puts the 'and' at
           two-thirds of the beat); the choruses straight, a rally march.
  drums    shuffle sections: kick on 1 and 3, snare on 2 and 4, hats in (swung) eighths; the choruses: kick on every beat, straight
           eighths on the ride (a tambourine joins in the last chorus), a marching
           snare figure (2 and 4 with a pickup on the 'and' of 4 and a roll into the next chorus bar), a crash on each chorus's first
           bar. A fill in the last bar of each section. One hit on the last bar.
  bass     from the verse. 233: the root on beat 1 of every bar and at each change; shuffle sections the boogie cell (root, root, fifth, fifth, sixth,
           sixth, fifth, root); the choruses straight driving eighths (root, fifth, octave); the bridge root-fifth half notes.
  rhythm   shuffle sections the boogie (root-fifth and root-sixth alternating in eighths); the choruses open strums in straight eighths;
           the bridge and the solo held power chords.
  piano    the chordal part (237): three-note chords between MIDI 51 and 71: the 'and's in the verses and outro, quarters in the
           choruses (a rally piano), held in the bridge; out for the solo.
  voice 2  the same singer on a second track (Q2): chorus 2 doubled in unison; in the last chorus the second candidate: line 2
           alone, lines 3-4 a third under, lines 5-9 in unison with voice 1.
  lead     the intro tune (intro, outro), the fills, the 8-bar solo."""
import pickle, sys
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p39"]
import melody_p39 as P
M = P.M
import pyphen
import lyric_p39 as L
R = pickle.load(open("/home/claude/p39/melody_main.pkl", "rb")); c = R["pick"]
RF = pickle.load(open("/home/claude/p39/riff_p39.pkl", "rb"))
import riff_p39 as RV
BAR = 48; NB = P.NBARS; QB = 108
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"Tuesday": ["Tues", "day"], "thousand": ["thou", "sand"], "Wednesday": ["Wednes", "day"], "other": ["oth", "er"], "donor's": ["do", "nor's"],
        "every": ["ev", "ery"], "shoulder,": ["shoul", "der,"], "minute": ["min", "ute"], "nine-thirty-one:": ["nine-", "thir", "ty-", "one:"],
        "before.": ["be", "fore."], "across": ["a", "cross"], "written": ["writ", "ten"], "studied": ["stud", "ied"], "government": ["gov", "ern", "ment"],
        "paychecks": ["pay", "checks"], "fundraiser's": ["fund", "rais", "er's"], "tonight.": ["to", "night."], "frosting": ["frost", "ing"],
        "lobby": ["lob", "by"], "above": ["a", "bove"]}
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
SWUNG = {nm for nm, kind, _ in P.FORM if kind != "Chorus"}
bars = []
for nm, kind, nb in P.FORM:
    for k in range(nb):
        b = P.BAR0[nm] + k
        bars.append(dict(sec=nm, kind=kind, k=k, n=nb, chord=P.CHORD[b], roman=M.ROMAN[P.CHORD[b]], start=b * BAR, len=BAR, qbpm=QB, key="E major",
                         stop=False, swing=nm in SWUNG))
lead = []
for n in c["notes"]:
    sec, i = n["line"].split(":"); i = int(i)
    t, hy = TEXT[sec][i][n["syl"]]
    lead.append(dict(on=n["on"], dur=n["dur"], midi=n["p"], sec=sec, line=i, syl=n["syl"], first=not n["slur"], text=t, hyph=hy,
                     stress=P.LINES[sec][i][n["syl"]][1], role=M.WORDS_OF[sec][i][0], voice=L.VOICES[i] if sec == "Last Chorus" else "one"))
ROOT = {k: v[0] for k, v in M.CH.items()}
def root_bass(ch): return 40 + (ROOT[ch] - 4) % 12                      # E2 .. D#3
def fifth(ch): return root_bass(ch) + 7
def sixth(ch): return root_bass(ch) + 9
def power(ch, lo=40): r = lo + (ROOT[ch] - lo) % 12; return [r, r + 7]
def triad(ch, lo):
    out, p = [], lo
    while len(out) < 3:
        if p % 12 in M.CH[ch][1]: out.append(p)
        p += 1
    return out
D = dict(kick=36, snare=38, hh=42, ohh=46, crash=49, ride=51, tomh=48, tomm=45, toml=41)
drums, bass, rgtr, piano, lgtr, voice2 = [], [], [], [], [], []
def ev(lst, on, dur, p, vel, art=""): lst.append(dict(on=on, dur=dur, p=p if isinstance(p, list) else [p], vel=vel, art=art))
for bi, b in enumerate(bars):
    sec, kind, ch, st, k, n = b["sec"], b["kind"], b["chord"], b["start"], b["k"], b["n"]
    r = root_bass(ch); march = kind == "Chorus"; top = sec == "Last Chorus"; last_bar = bi == NB - 1
    if last_bar:                                                                 # one hit
        ev(drums, st, 3, [D["kick"], D["crash"]], 122); ev(bass, st, 36, [r, r + 12], 108); ev(rgtr, st, 36, power(ch) + [power(ch)[0] + 12], 104, "ring")
        ev(piano, st, 36, triad(ch, 56), 84, "ring"); continue
    # ---- drums ----
    if march:
        for e in (0, 12, 24, 36): ev(drums, st + e, 3, D["kick"], 108 + (4 if top else 0))
        for e, v in ((12, 112), (36, 112), (42, 70), (45, 74)): ev(drums, st + e, 3, D["snare"], v + (4 if top else 0))
        [ev(drums, st + e, 3, D["ride"], 82 if e % 12 == 0 else 70) for e in range(0, 48, 6)]          # the march: straight eighths on the ride
        if top: [ev(drums, st + e, 3, 54, 72) for e in range(0, 48, 6)]                              # the last chorus: a tambourine too
        if k == 0: ev(drums, st, 3, D["crash"], 118)
        if top and k % 4 == 0 and k: ev(drums, st, 3, D["crash"], 112)
    else:
        for e in (0, 24): ev(drums, st + e, 3, D["kick"], 104)
        for e in (12, 36): ev(drums, st + e, 3, D["snare"], 106)
        [ev(drums, st + e, 3, D["hh"] if kind != "Solo" else D["ride"], 78 if e % 12 == 0 else 62) for e in range(0, 48, 6)]
        if kind == "Intro" and k == 0: ev(drums, st, 3, D["crash"], 112)
    if k == n - 1 and kind not in ("Outro",):                                   # 236: a fill in the section's last bar
        drums[:] = [d for d in drums if not (st + 24 <= d["on"] < st + 48 and not (d["on"] == st + 24 and d["p"][0] == D["kick"]))]
        for j, e in enumerate(range(24, 48, 3)): ev(drums, st + e, 3, [D["snare"], D["tomh"], D["tomm"], D["toml"]][j // 2 % 4], 92 + j * 2)
    # ---- bass ----
    if kind == "Intro": pass                                                     # 238: the bass waits for the verse
    elif kind == "Bridge": ev(bass, st, 22, r, 96); ev(bass, st + 24, 22, fifth(ch), 92)
    elif march:
        for j, p in enumerate([r, r, r, r, fifth(ch), fifth(ch), r + 12, fifth(ch)]): ev(bass, st + 6 * j, 5, p, (108 if j % 2 == 0 else 96) + (4 if top else 0))
    else:
        for j, p in enumerate([r, r, fifth(ch), fifth(ch), sixth(ch), sixth(ch), fifth(ch), r]): ev(bass, st + 6 * j, 5, p, 100 if j % 2 == 0 else 86)
    # ---- rhythm guitar ----
    if kind == "Bridge": ev(rgtr, st, 46, power(ch) + [power(ch)[0] + 12], 84, "held")
    elif march:
        for e in range(0, 48, 6): ev(rgtr, st + e, 5, power(ch) + [power(ch)[0] + 12], (96 if e % 12 == 0 else 84) + (6 if top else 0), "open")
    elif kind == "Solo":
        for e in (0, 24): ev(rgtr, st + e, 22, power(ch) + [power(ch)[0] + 12], 80, "held")              # the solo's guitar holds, under the lead
    else:
        rr = power(ch)[0]
        for j in range(8): ev(rgtr, st + 6 * j, 5, [rr, rr + (9 if j % 4 in (2, 3) else 7)], 86 if j % 2 == 0 else 74, "boogie")
    # ---- piano: the chordal part ----
    if kind == "Bridge": ev(piano, st, 46, triad(ch, 56), 70, "held")
    elif march:
        for e in (0, 12, 24, 36): ev(piano, st + e, 10, triad(ch, 56), 80 + (6 if top else 0), "stab")
    elif kind in ("Verse", "Outro"):
        for e in (6, 18, 30, 42): ev(piano, st + e, 5, triad(ch, 56), 66, "stab")
# ---- voice 2 in the last chorus ----
def third_under(p, at):
    ch = M.chord_at(at); return max(q for q in range(p - 5, p - 2) if q % 12 in M.SCALE and not M.clash(q, ch))
for x in lead:
    if x["sec"] == "Chorus 2": ev(voice2, x["on"], x["dur"], x["midi"], 80, "double:" + x["text"]); continue      # chorus 2 double-tracked
    if x["sec"] != "Last Chorus": continue
    v = L.VOICES[x["line"]]
    if v == "two": ev(voice2, x["on"], x["dur"], x["midi"], 90, "two:" + x["text"])
    elif v == "both, apart": ev(voice2, x["on"], x["dur"], third_under(x["midi"], x["on"]), 84, "third:" + x["text"])
    elif v == "unison": ev(voice2, x["on"], x["dur"], x["midi"], 86, "unison:" + x["text"])
# ---- the lead guitar ----
RONS, RSTEPS = RF["pick"]["ons"], RF["pick"]["steps"]
for sl in RF["slots"]:
    pl = RV.place(RONS, RSTEPS, sl)
    for j, (t, p) in enumerate(pl):
        nx = pl[j + 1][0] if j + 1 < len(pl) else min(sl["end"], t + 12)
        ev(lgtr, t, max(3, nx - t), p, 96, "tune:" + sl["where"])
for f in RF["fills"]:
    for e in f["notes"]: ev(lgtr, e["on"], e["dur"], e["p"], 90, "fill:" + f["gap"]["after"])
for e in RF["solo"]: ev(lgtr, e["on"], e["dur"], e["p"], 94, "solo")
for lst in (drums, bass, rgtr, piano, lgtr, voice2): lst.sort(key=lambda e: (e["on"], e["p"][0]))
plan = [(nm, nb, P.BAR0[nm], "4/4") for nm, _, nb in P.FORM]
secs = NB * 4 * 60 / QB
rec = dict(title=L.TITLE, nbars=NB, bars=bars, plan=plan, lead=lead, drums=drums, bass=bass, rgtr=rgtr, piano=piano, lgtr=lgtr, voice2=voice2,
           slot="twelfth of a beat", bar=BAR, qbpm=QB, seconds=secs, tw_sec=60 / QB / 12, fp=c["fp"], order_fp=R["order_fp"], swung=sorted(SWUNG),
           survivors=R["survivors"], built=R["made"], deaths=dict(R["deaths"]), meas={k: (float(v) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()},
           judge={k: c["judge"][k] for k in ("combined", "content", "order")}, plans=c["meta"]["plans"], targets=c["meta"]["targets"], windows=c["meta"]["win"],
           kinds={f"{a}:{b}": v for (a, b), v in c["meta"]["kinds"].items()}, hand_edits=[], rerun=R["rerun"], text=TEXT, read=c["read"], summit=P.SUMMIT,
           riff=dict(RF["pick"], slots=[s_["where"] for s_ in RF["slots"]], drawn=RF["drawn"], passed=RF["passed"], seed=RF["seed"], solo_check=RF["solo_check"],
                     fills=len(RF["fills"]), gaps=len(RF["gaps"]), fill_stats=RF["fill_stats"]))
pickle.dump(rec, open("/home/claude/p39/song_record.pkl", "wb"))
print(NB, "bars,", f"{secs:.0f} s ({int(secs // 60)}:{int(round(secs % 60)):02d});", len(lead), "sung;", len(drums), "drums;", len(bass), "bass;",
      len(rgtr), "rhythm;", len(piano), "piano;", len(voice2), "voice 2;", len(lgtr), "lead; fp", rec["fp"])
