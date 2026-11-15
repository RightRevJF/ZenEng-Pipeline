"""The Room Next Door (song 52): the song record from melody_final.json (the 6/8 sketch's pick) and the writer's chords. An intimate folk
ballad in 6/8, D major, dotted quarter = 54 (quarter = 81), for an alto; 84 bars (the sound, A; the key, A; the form, A).
  Intro (4): the fingerpicked acoustic guitar alone (six eighths a bar: the bass note on 1, the fifth on 4, the chord between).
  Verse 1: guitar and voice.   Chorus 1: piano and bass come in; harmony on the hook.   Verse 2: piano answers at the line ends.
  Chorus 2: the cello joins with long notes.   Interlude (4): the cello sings the hook's tune.   Verse 3: guitar, bass, the cello held.
  Bridge: a hush; the guitar and bass out, soft piano and cello alone.   Verse 4: the guitar back.
  Final chorus: the fullest; harmony on every line; the second 'there's a door in the wall' comes home and holds into the outro.
  Outro (4): guitar and cello, the last Dadd9 ringing.
The bass is written here, not by the 4/4 routine (bass_v134 reads 48-tick bars): the root on the bar's first beat, the fifth or the next
chord's approach on its second."""
import json, pickle, collections
import pyphen
H = "/home/claude/p62"
F = json.load(open(f"{H}/melody_shaped.json")); c = F["pick"]                           # chorus 2 varied (749.8) and the song shaped (shape68.py, 749.10)                           # the pick with chorus 2 varied (vary68.py, 749.8)
import importlib.util as _u
_s = _u.spec_from_file_location("lyr", f"{H}/lyric_p62.py"); L = _u.module_from_spec(_s); _s.loader.exec_module(L)
import gen68 as G
BAR, BEAT = 36, 18; NB = G.NBARS; QB = 81                                                   # quarter = 81: the dotted quarter at 54
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"Forty": ["For", "ty"], "every": ["ev", "ery"], "little": ["lit", "tle"], "weren't": ["were", "n't"], "coming": ["com", "ing"], "sunlight": ["sun", "light"],
        "never": ["nev", "er"], "lying": ["ly", "ing"], "open": ["o", "pen"], "Margaret": ["Mar", "ga", "ret"], "worry": ["wor", "ry"], "daughters": ["daugh", "ters"],
        "hello": ["hel", "lo"], "plaster": ["plas", "ter"], "morning": ["morn", "ing"], "early": ["ear", "ly"], "kettle": ["ket", "tle"], "Mama": ["Ma", "ma"],
        "going": ["go", "ing"], "opens": ["o", "pens"], "after": ["af", "ter"], "There's": ["There's"], "there's": ["there's"], "you're": ["you're"], "tired": ["ti", "red"]}
def split_words(text, n_sy):
    out = []; ws = text.split()
    for w in ws:
        core = w.rstrip(",.;:?"); tail = w[len(core):]
        parts = HFIX.get(core) or _PY.inserted(core).split("-")
        out.append((core, tail, parts))
    toks = []
    for core, tail, parts in out:
        for j, p in enumerate(parts): toks.append([p + (tail if j == len(parts) - 1 else ""), j < len(parts) - 1])
    return toks
TEXT = {}
for sec, ls in L.SECTIONS:
    TEXT[sec] = []
    for i, (_, t) in enumerate(ls):
        n = len(G.SY[sec][i]); tk = split_words(t, n)
        while len(tk) > n:                                                               # merge where the syllable count says fewer
            j = next(k for k in range(len(tk) - 1) if tk[k][1]); tk[j] = [tk[j][0] + tk[j + 1][0], tk[j + 1][1]]; del tk[j + 1]
        while len(tk) < n:                                                               # split the longest word where it says more
            j = max(range(len(tk)), key=lambda k: len(tk[k][0])); w = tk[j][0]; h = len(w) // 2; tk[j:j + 1] = [[w[:h], True], [w[h:], tk[j][1]]]
        TEXT[sec].append([tuple(x) for x in tk])
CHORD = G.CHORD
bars = []
for nm, nb in G.FORM:
    for k in range(nb):
        b = G.BAR0[nm] + k
        bars.append(dict(sec=nm, kind=nm.split()[0], k=k, n=nb, b=b, meter="6/8", start=b * BAR, len=BAR, chord=CHORD[b], chord2=CHORD[b], qbpm=QB, key="D major", movement=nm, stop=False))
lead = []
for n in c["notes"]:
    sec, i = n["sec"], n["line"]; tx, hy = TEXT[sec][i][n["syl"]]
    lead.append(dict(on=n["on"], dur=n["dur"], midi=n["p"], sec=sec, line=i, syl=n["syl"], first=True, text=tx, hyph=hy, stress=n["stress"], role=L.SECTIONS[[s for s, _ in L.SECTIONS].index(sec)][1][i][0], singer="voice"))
TONES = {"Dadd9": {2, 6, 9, 4}, "Gmaj7": {7, 11, 2, 6}, "Dadd9/F#": {2, 6, 9, 4}, "Asus4": {9, 2, 4}, "D/F#": {2, 6, 9}, "Em9": {4, 7, 11, 2, 6}, "Bm7": {11, 2, 6, 9},
         "A": {9, 1, 4}, "Gadd9": {7, 11, 2, 9}, "F#m7": {6, 9, 1, 4}, "Cadd9": {0, 4, 7, 2}, "G/B": {7, 11, 2}, "A7sus4": {9, 2, 4, 7}, "Bbmaj7": {10, 2, 5, 9}}
ROOT = {"Dadd9": 2, "Gmaj7": 7, "Dadd9/F#": 6, "Asus4": 9, "D/F#": 6, "Em9": 4, "Bm7": 11, "A": 9, "Gadd9": 7, "F#m7": 6, "Cadd9": 0, "G/B": 11, "A7sus4": 9, "Bbmaj7": 10}
CROOT = {"Dadd9/F#": 2, "D/F#": 2, "G/B": 7}                                                # the chord's own root, where the bass takes another note
SCALE = {2, 4, 6, 7, 9, 11, 1}
def tones(ch): return TONES[ch]
def voicing(ch, lo, n):
    out, p = [], lo
    while len(out) < n:
        if p % 12 in tones(ch): out.append(p)
        p += 1
    return out
def up_to(p, pcs, k=1):
    q = p
    for _ in range(k):
        q += 1
        while q % 12 not in pcs: q += 1
    return q
def down_to(p, pcs, k=1):
    q = p
    for _ in range(k):
        q -= 1
        while q % 12 not in pcs: q -= 1
    return q
def chord_at_rec(t): return CHORD[min(NB - 1, t // BAR)]
# ---- harmony: on the hook in every chorus; every line of the final chorus; written as lines (harm68.py, 749.9) ----
import harm68
HSPAN = [n for n in lead if n["role"] == "hook" or n["sec"] == "Last Chorus"]
_hp = harm68.high(HSPAN, lambda t: tones(chord_at_rec(t)))
harm_hi = [dict(n, midi=p, singer="harmony high") for n, p in zip(HSPAN, _hp)]
harm_lo = [dict(n, singer="harmony low", stress=False, first=True, hyph=False, role="ooh") for n in harm68.low(HSPAN, lambda t: tones(chord_at_rec(t)))]
parts = collections.defaultdict(list)
def ev(part, on, dur, p, vel, art=""): parts[part].append(dict(on=on, dur=dur, p=p if isinstance(p, list) else [p], vel=int(max(1, min(127, vel))), art=art))
def pick6(st, ch, vel):
    """the fingerpicked guitar in 6/8: the bass on 1 and 4, the chord's upper notes on the eighths between."""
    r = 40 + (ROOT[ch] - 40) % 12; f5 = r + 7 if r + 7 <= 52 else r - 5; up = voicing(ch, 55, 3)
    for e, p in ((0, r), (6, up[0]), (12, up[1]), (18, f5), (24, up[2]), (30, up[1])):
        ev("guitar", st + e, 6 if e % 18 else 12, p, vel + (6 if e % 18 == 0 else -4))
def piano_beats(st, ch, vel): ev("piano", st, 18, voicing(ch, 55, 3), vel); ev("piano", st + 18, 18, voicing(ch, 55, 3), vel - 6)
def piano_hold(st, ch, vel): ev("piano", st, 36, voicing(ch, 50, 4), vel)
def cello(st, p, dur, vel): ev("cello", st, dur, p, vel)
def bass(st, ch, nxt, vel):
    r = 33 + (ROOT[ch] - 33) % 12; ev("bass", st, 18, r, vel)
    tgt = 33 + (ROOT[nxt] - 33) % 12; a = tgt - 2 if abs(tgt - 2 - r) <= 7 and (tgt - 2) % 12 in SCALE else r + 7 if r + 7 <= 52 else r - 5
    ev("bass", st + 18, 18, a, vel - 6)
DOORT = [(t, p - 12, d) for t, p, d in G.DOOR]
for x in bars:
    sec, st, k, nb, ch = x["sec"], x["start"], x["k"], x["n"], x["chord"]
    nxt = CHORD[min(NB - 1, x["b"] + 1)]; last = k == nb - 1
    if sec == "Intro": pick6(st, ch, 54)
    elif sec == "Verse 1": pick6(st, ch, 56)
    elif sec == "Chorus 1":
        pick6(st, ch, 60); piano_beats(st, ch, 44); bass(st, ch, nxt, 56)
    elif sec == "Verse 2":
        pick6(st, ch, 58); bass(st, ch, nxt, 52)
        if k % 2 == 1: ev("piano", st + 24, 12, voicing(ch, 69, 1), 42)                          # the piano's answer at the line's end
    elif sec == "Chorus 2":
        pick6(st, ch, 62); piano_beats(st, ch, 48); bass(st, ch, nxt, 58); cello(st, 38 + (ROOT[ch] - 38) % 12 + 12, 36, 50)
    elif sec == "Interlude":
        pick6(st, ch, 56); bass(st, ch, nxt, 52)
        if k == 0:
            for t, p, d in DOORT: ev("cello", st + t, d if t + d <= 72 else 72 - t, p, 60)
        if k == 2: cello(st, 50, 72, 54)
    elif sec == "Verse 3":
        pick6(st, ch, 58); bass(st, ch, nxt, 54)
        if k % 2 == 0: cello(st, 38 + (ROOT[ch] - 38) % 12 + 12, 72, 46)
    elif sec == "Bridge":
        piano_hold(st, ch, 40 + (4 if k >= 6 else 0)); cello(st, 38 + (ROOT[ch] - 38) % 12 + 12, 36, 44 + 2 * k)
    elif sec == "Verse 4":
        pick6(st, ch, 60); bass(st, ch, nxt, 56); ev("piano", st, 36, voicing(ch, 62, 3), 38)
    elif sec == "Last Chorus":
        pick6(st, ch, 64); piano_beats(st, ch, 52); bass(st, ch, nxt, 60)
        cello(st, 38 + (ROOT[ch] - 38) % 12 + 12 + (7 if k % 2 else 0), 36, 56)
        if k == nb - 1: ev("piano", st, 36, voicing(ch, 50, 5), 50)
    elif sec == "Outro":
        if k < 3: pick6(st, ch, 54 - 4 * k); cello(st, 38 + (ROOT[ch] - 38) % 12 + 12, 36, 48 - 3 * k)
        else: ev("guitar", st, 36, voicing("Dadd9", 50, 5), 54); cello(st, 38, 36, 44); ev("bass", st, 36, 38, 50); ev("piano", st, 36, voicing("Dadd9", 62, 3), 40)
def tidy(lst):
    lst.sort(key=lambda e: (e["on"], e["p"][0])); out = []
    for e in lst:
        if out and out[-1]["on"] == e["on"] and out[-1]["art"] == e["art"]: out[-1]["p"] = sorted(set(out[-1]["p"] + e["p"])); out[-1]["vel"] = max(out[-1]["vel"], e["vel"]); continue
        out.append(e)
    for j in range(len(out) - 1):
        if out[j]["on"] + out[j]["dur"] > out[j + 1]["on"]: out[j]["dur"] = out[j + 1]["on"] - out[j]["on"]
    return out
PARTS = {k: tidy(v) for k, v in parts.items()}
plan = [(nm, nb, G.BAR0[nm] * BAR, ["6/8"] * nb, nm) for nm, nb in G.FORM]
secs = NB * BAR / 12 * 60 / QB
rec = dict(title=L.TITLE, file_title=L.TITLE + " (third edition)", edition="third edition", nbars=NB, bars=bars, chords2=[h for ch in CHORD for h in (ch, ch)], plan=plan, lead=lead, harm_hi=harm_hi, harm_lo=harm_lo,
           parts=PARTS, slot="twelfth of a quarter; a 6/8 bar of 36", qbpm=QB, dotted=54, seconds=secs, tw_sec=60 / QB / 12, end=NB * BAR, meters={},
           fp=c["fp"], survivors=F["survivors"], built=F["made"], readings=c["readings"], charge=c["charge"], distance=c["distance"], plans=c["plans"], text=TEXT,
           design=dict(door=G.DOOR, home=G.HOME, there=G.THERE, registers=G.REG), seed=F["seed"], hand_edits=[])
pickle.dump(rec, open(f"{H}/song_record.pkl", "wb"))
if __name__ == "__main__":
    print(NB, "bars,", f"{secs:.0f} s;", len(lead), "sung;", {k: len(v) for k, v in PARTS.items()}, "harmony", len(harm_hi))
    for sec in TEXT:
        for i, ws in enumerate(TEXT[sec]): print(sec, i, " ".join(t + ("-" if h else "") for t, h in ws))
