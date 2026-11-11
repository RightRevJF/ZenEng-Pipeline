"""The Water Used to Sing (song 41): the song record from melody_final.pkl (the pick of record, no hand edits) and riff_p41.pkl.
Swung shuffle at q = 96 (written straight, played swung), G major, 104 bars. Americana rock (Q5 A): acoustic and electric guitars,
organ, bass, drums with brushes in the verses and sticks from the first chorus (Q19 A: the kit follows the sound).
  voice     the baritone, every line (sounding G2-E4 row; written an octave up on a treble-8 clef).
  acoustic  shuffle eighths on the chord from bar 1; half-note strokes in the bridge (the dry valley); one chord to ring at the end.
  electric  the lick (intro, outro bars 1-7); chord chops on 2 and 4 in the choruses, the break and verse 3 from its fifth bar;
            the fills in the choruses' gaps; the break's solo ('the gate').
  organ     held chords from verse 2 on (pre-choruses swell); a low open fifth in the bridge; the last chorus's countermelody above the
            voice (Q18 B, design) with the chords held low beneath it.
  bass      in at intro bar 5: root and fifth in half notes (verses, pre-choruses); the boogie (R 3 5 6, minor R b3 5 b7) in the choruses,
            the break, verse 3 from bar 5 and the outro; whole notes in the bridge.
  drums     brushes (intro from bar 5, verses 1-2, pre-choruses, bridge, verse 3 bars 1-4): kick 1 and 3, a tap on 2 and 4, the swirl on
            every beat. Sticks (choruses, break, verse 3 from bar 5, last chorus, outro): kick 1, 3 and the swung 'and' of 4, snare 2 and 4,
            hi-hat eighths (ride in the last chorus), crash at each section's start. A fill in the last bar of each section (Q19 A)."""
import pickle, sys
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p41"]
import melody_p41 as P
M = P.M
import pyphen
F = pickle.load(open("/home/claude/p41/melody_final.pkl", "rb")); c = F["pick"]
RF = pickle.load(open("/home/claude/p41/riff_p41.pkl", "rb"))
BAR = 48; NB = P.NBARS; QB = 96
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"hurry,": ["hur", "ry,"], "county": ["coun", "ty"], "every": ["ev", "ery"], "April,": ["A", "pril,"], "supper": ["sup", "per"], "after": ["af", "ter"],
        "reason,": ["rea", "son,"], "water": ["wa", "ter"], "The": ["The"], "under": ["un", "der"], "window,": ["win", "dow,"], "only": ["on", "ly"],
        "August,": ["Au", "gust,"], "forty": ["for", "ty"], "patient": ["pa", "tient"], "river": ["riv", "er"], "sheepdog": ["sheep", "dog"],
        "ribbon,": ["rib", "bon,"], "quiet": ["qui", "et"], "Below": ["Be", "low"], "willows": ["wil", "lows"], "paper,": ["pa", "per,"],
        "matchsticks,": ["match", "sticks,"], "over": ["o", "ver"], "Daddy,": ["Dad", "dy,"], "didn't": ["did", "n't"], "answer.": ["an", "swer."],
        "against": ["a", "gainst"], "valley": ["val", "ley"], "shouting,": ["shout", "ing,"], "water's": ["wa", "ter's"], "singing": ["sing", "ing"],
        "crooked": ["crook", "ed"], "cellar,": ["cel", "lar,"], "living": ["liv", "ing"], "doesn't": ["does", "n't"], "river's": ["riv", "er's"]}
def split_words(text, sy):
    out = []; ws = text.replace('"', "").split()
    for w in ws:
        n = len(P.syl(w))
        core = w.rstrip(",.;:?")
        if n <= 1: out.append((w, False)); continue
        parts = HFIX.get(w) or HFIX.get(core) or _PY.inserted(core).split("-")
        tail = "" if w in HFIX else w[len(core):]
        if len(parts) > n: parts = parts[:n - 1] + ["".join(parts[n - 1:])]
        while len(parts) < n: parts.append("_")
        for j, p in enumerate(parts): out.append((p + (tail if j == n - 1 else ""), j < n - 1))
    assert len(out) == len(sy), (text, out, sy)
    return out
TEXT = {sec: [split_words(t, P.LINES[sec][i]) for i, (_, t) in enumerate(M.WORDS_OF[sec])] for sec in P.SUNG}
_b4 = TEXT["Bridge"][4]; _j = [t for t, _ in _b4].index("Dad"); _b4[_j] = ("“Dad", True); _b4[-1] = (_b4[-1][0] + "”", False)   # the girl's words in quotes
STICKS0 = P.BAR0["Verse 3"] + 4                                                       # 'then the whole lake leaned against the gate'
def kit_of(b, kind):
    if kind in ("Chorus", "Break", "Outro"): return "sticks"
    if kind == "Verse" and b >= STICKS0 and b < P.BAR0["Last Chorus"]: return "sticks"
    return "brushes"
bars = []
for nm, kind, nb in P.FORM:
    for k in range(nb):
        b = P.BAR0[nm] + k
        bars.append(dict(sec=nm, kind=kind, k=k, n=nb, chord=P.CHORD[b], roman=M.ROMAN[P.CHORD[b]], start=b * BAR, len=BAR, qbpm=QB, key="G major",
                         kit=kit_of(b, kind), stop=False))
lead = []
for n in c["notes"]:
    sec, i = n["line"].split(":"); i = int(i); t, hy = TEXT[sec][i][n["syl"]]
    lead.append(dict(on=n["on"], dur=n["dur"], midi=n["p"], sec=sec, line=i, syl=n["syl"], first=not n["slur"], text=t, hyph=hy,
                     stress=P.LINES[sec][i][n["syl"]][1], role=M.WORDS_OF[sec][i][0], singer="voice"))
tagn = lead[-1]; tagn["dur"] = max(tagn["dur"], P.BAR0["Outro"] * BAR + BAR - tagn["on"])   # 'It sings.' held into the outro's first bar (the writer's note)
ROOT = {k: v[0] for k, v in M.CH.items()}
MINOR = {"Em", "Am"}
def root_bass(ch): return 28 + (ROOT[ch] - 28) % 12                                   # E1 .. D#2
def chord3(ch, lo):
    out, p = [], lo
    while len(out) < 3:
        if p % 12 in M.CH[ch][1]: out.append(p)
        p += 1
    return out
OPEN = {"G": [43, 47, 50, 55, 59, 67], "C": [48, 52, 55, 60, 64], "D": [50, 57, 62, 66], "Em": [40, 47, 52, 55, 59, 64], "Am": [45, 52, 57, 60, 64], "F": [41, 48, 53, 57, 60, 65]}
CHOP = {"G": [55, 59, 62], "C": [55, 60, 64], "D": [57, 62, 66], "Em": [55, 59, 64], "Am": [57, 60, 64], "F": [57, 60, 65]}
DR = dict(kick=36, snare=38, hh=42, ohh=46, crash=49, ride=51, tomh=50, tomm=47, toml=43, tap=38, swirl=40)
drums, bass, acou, egtr, organ, counter = [], [], [], [], [], []
def ev(lst, on, dur, p, vel, art="", **kw): lst.append(dict(on=on, dur=dur, p=p if isinstance(p, list) else [p], vel=vel, art=art, **kw))
BOOGIE_MAJ, BOOGIE_MIN = (0, 4, 7, 9), (0, 3, 7, 10)
LOUD = {"Verse 1": 0, "Pre 1": 2, "Chorus 1": 6, "Verse 2": 2, "Pre 2": 4, "Chorus 2": 9, "Bridge": -6, "Break": 10, "Verse 3": 6, "Last Chorus": 14, "Intro": 0, "Outro": 8}
for bi, b in enumerate(bars):
    sec, kind, ch, st, k, n, kit = b["sec"], b["kind"], b["chord"], b["start"], b["k"], b["n"], b["kit"]
    r = root_bass(ch); L = LOUD[sec]; last_bar = k == n - 1
    v3_band = sec == "Verse 3" and bi >= STICKS0
    band = kind in ("Chorus", "Break", "Outro") or v3_band
    if kind == "Outro" and last_bar:                                                  # one G chord, left to ring
        ev(acou, st, BAR, OPEN["G"], 96, "ring"); ev(egtr, st, BAR, [55, 59, 62, 67], 90, "ring"); ev(organ, st, BAR, [55, 59, 62, 67], 72, "ring")
        ev(bass, st, BAR, [31], 98, "ring"); ev(drums, st, 6, [DR["crash"], DR["kick"]], 112, kit="sticks")
        continue
    # ---- acoustic: shuffle eighths; the bridge in half notes ----
    if kind == "Bridge": [ev(acou, st + e, 22, OPEN[ch], 70, "stroke") for e in (0, 24)]
    else:
        for j, e in enumerate(range(0, BAR, 6)):
            down = j % 2 == 0; ev(acou, st + e, 6, OPEN[ch] if down else OPEN[ch][-3:], (82 if down else 66) + L // 2, "strum")
    # ---- electric: chops on 2 and 4 where the band plays (the lick, fills and break below) ----
    if band and kind not in ("Break", "Outro"): [ev(egtr, st + e, 5, CHOP[ch], 80 + L // 2, "chop") for e in (12, 36)]
    if kind == "Break": [ev(egtr, st + e, 5, [p - 12 for p in CHOP[ch]], 76, "chop") for e in (12, 36)]
    # ---- organ ----
    if kind == "Pre" and sec == "Pre 2" or (kind == "Pre" and sec == "Pre 1" and k >= 2): ev(organ, st, 46, chord3(ch, 55), 54 + 6 * k, "swell")
    elif kind == "Bridge": ev(organ, st, 46, [40, 47] if k < 8 else [45, 52] if ch == "Am" else [38, 45], 52, "held")
    elif sec == "Last Chorus": ev(organ, st, 46, chord3(ch, 48), 64, "held")
    elif sec in ("Verse 2", "Verse 3") or kind in ("Chorus", "Break", "Outro"): ev(organ, st, 46, chord3(ch, 55), (56 if kind == "Verse" else 66) + L // 2, "held")
    # ---- bass ----
    if kind == "Intro" and k < 4: pass
    elif kind == "Bridge": ev(bass, st, 46, r, 80)
    elif band or kind == "Outro":
        cell = BOOGIE_MIN if ch in MINOR else BOOGIE_MAJ
        for j, x in enumerate(cell): ev(bass, st + 12 * j, 11, r + x, (100 if j % 2 == 0 else 90) + L // 2)
    else: ev(bass, st, 23, r, 90 + L // 2); ev(bass, st + 24, 23, r + 7, 84 + L // 2)
    # ---- drums ----
    if kind == "Intro" and k < 4: continue
    if kit == "brushes":
        for e in (0, 24): ev(drums, st + e, 3, DR["kick"], 72 + L, kit=kit)
        for e in (12, 36): ev(drums, st + e, 3, DR["tap"], 74 + L, kit=kit)
        if kind != "Bridge" or k % 2 == 0: [ev(drums, st + e, 12, DR["swirl"], 50 + L, kit=kit) for e in (0, 12, 24, 36)]
        if last_bar and kind != "Bridge": [ev(drums, st + e, 3, DR["tap"], 62 + 4 * j + L, "fill", kit=kit) for j, e in enumerate((30, 36, 42, 45))]
    else:
        top = sec == "Last Chorus"
        if k == 0 or (bi == STICKS0): ev(drums, st, 3, DR["crash"], 112, kit=kit)
        if top and k % 4 == 0 and k: ev(drums, st, 3, DR["crash"], 106, kit=kit)
        for e in (0, 24, 42): ev(drums, st + e, 3, DR["kick"], (106 if e == 0 else 96) + L // 2, kit=kit)
        if not last_bar or kind == "Outro":
            for e in (12, 36): ev(drums, st + e, 3, DR["snare"], 108 + L // 2, kit=kit)
        else:                                                                              # the fill into the next section
            ev(drums, st + 12, 3, DR["snare"], 108, kit=kit)
            for j, e in enumerate((24, 30, 36, 42)): ev(drums, st + e, 3, [DR["snare"], DR["tomh"], DR["tomm"], DR["toml"]][j], 92 + 5 * j, "fill", kit=kit)
        cym = DR["ride"] if top else DR["hh"]
        for e in range(0, BAR, 6):
            if last_bar and e >= 24 and kind != "Outro": continue
            ev(drums, st + e, 3, cym, (84 if e % 12 == 0 else 66) + L // 3, kit=kit)
# ---- the lick, the fills, the break, the countermelody ----
for e in RF["lick"]: ev(egtr, e["on"], 6, e["p"], 92 if e["where"] == "intro" else 88, "lick:" + e["where"])
for f in RF["fills"]:
    for e in f["notes"]: ev(egtr, e["on"], e["dur"], e["p"], 88, "fill:" + f["gap"]["after"])
for e in RF["solo"]: ev(egtr, e["on"], e["dur"], e["p"], 90, "solo")
for e in RF["counter"]: ev(counter, e["on"], e["dur"], e["p"], 74, "counter")
for lst in (drums, bass, acou, egtr, organ, counter): lst.sort(key=lambda e: (e["on"], e["p"][0]))
plan = [(nm, nb, P.BAR0[nm], "4/4") for nm, _, nb in P.FORM]
secs = NB * 4 * 60 / QB
rec = dict(title="The Water Used to Sing", nbars=NB, bars=bars, plan=plan, lead=lead, harm=[], drums=drums, bass=bass, acou=acou, egtr=egtr, organ=organ, counter=counter,
           slot="twelfth of a beat", bar=BAR, qbpm=QB, feel="swung eighths (shuffle): written straight, played 2:1", seconds=secs, tw_sec=60 / QB / 12, fp=c["fp"],
           order_fp=F["run"]["order_fp"], survivors=F["run"]["survivors"], built=F["run"]["made"], meas={k: (float(v) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()},
           judge={k: c["judge"][k] for k in ("combined", "content", "order")}, plans=c["meta"]["plans"], hand_edits=c["hand_edits"], picked_from=c["picked_from"],
           kinds={f"{a}:{b}": v for (a, b), v in c["meta"]["kinds"].items()}, rerun=F["run"]["rerun"], text=TEXT, lift=c["info"]["lift"],
           design=dict(gates=P.DESIGN_GATES, slots={s: P.slots_of(s) for s in P.SUNG}, two_bar=P.DESIGNED_TWO_BAR, one_bar=P.DESIGNED_ONE_BAR,
                       counter="last chorus only, organ above the voice (Q18 B)", sticks_from=STICKS0),
           riff=dict(RF["pick"], drawn=RF["drawn"], passed=RF["passed"], seed=RF["seed"], solo_check=RF["solo_check"], fills=len(RF["fills"]), gaps=len(RF["gaps"]),
                     fill_stats=RF["fill_stats"], counter_check=RF["counter_check"]))
pickle.dump(rec, open("/home/claude/p41/song_record.pkl", "wb"))
if __name__ == "__main__":
    print(NB, "bars,", f"{secs:.0f} s;", len(lead), "sung;", {k: len(v) for k, v in dict(drums=drums, bass=bass, acou=acou, egtr=egtr, organ=organ, counter=counter).items()})
    for sec in P.SUNG:
        for i, ws in enumerate(TEXT[sec]): print(sec, i, " ".join(t + ("-" if h else "") for t, h in ws))
