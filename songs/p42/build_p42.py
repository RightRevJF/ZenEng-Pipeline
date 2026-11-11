"""Nothing Important (song 42): the song record from melody_final.pkl (the pick of record, no hand edits) and riff_p42.pkl.
A piano ballad, straight eighths at q = 76, B-flat major, 68 bars (Q5 A). The piano part is complete on its own (Q7: one player at the
piano can perform the whole song with the singer and nothing else); the cello and the band only add colour.
  voice    the alto, every line.
  piano    intro: the right-hand figure over a left hand in half notes. Verses 1-2: broken chords in eighths, right hand under the voice
           (from B-flat 3), left hand root and fifth in half notes. Choruses: the right hand's broken chords a step higher, the left hand
           in quarters (root, fifth, octave, fifth). Bridge: half-note chords over whole notes. Verse 3 (the silence): bars 1-4 one chord
           a bar, held; bars 5-8 the verse's broken chords return. Last chorus: block chords on the beat over left-hand eighths; bars
           11-12 ('I'll call you back') one chord a bar, alone. Outro: the figure for three bars; one B-flat chord, let ring.
  cello    (Q14 A) holds in verse 2 and chorus 2 (and verse 3 from bar 5); the countermelody in the bridge and the last chorus.
  band     the last chorus only (Q5 A), bars 1-10: bass (root, then root and fifth), drums (brushes bars 1-6, sticks 7-10), clean guitar
           arpeggios; out at bar 11, so 'I'll call you back' falls quietly on the piano (Q11 note 4)."""
import pickle, sys
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p42", "/home/claude/p40"]
import melody_p42 as P
M = P.M
import pyphen
F = pickle.load(open("/home/claude/p42/melody_final.pkl", "rb")); c = F["pick"]
RF = pickle.load(open("/home/claude/p42/riff_p42.pkl", "rb"))
BAR = 48; NB = P.NBARS; QB = 76
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"kitchen": ["kitch", "en"], "message": ["mes", "sage"], "blinker,": ["blink", "er,"], "tapping": ["tap", "ping"], "always": ["al", "ways"],
        "before": ["be", "fore"], "hello:": ["hel", "lo:"], "nothing": ["noth", "ing"], "Nothing": ["Noth", "ing"], "important,": ["im", "por", "tant,"],
        "important.": ["im", "por", "tant."], "Seventh": ["Sev", "enth"], "wanted": ["want", "ed"], "October": ["Oc", "to", "ber"], "battery": ["bat", "ter", "y"],
        "counter": ["coun", "ter"], "didn't": ["did", "n't"], "radio;": ["ra", "di", "o;"], "morning": ["morn", "ing"], "wouldn't": ["would", "n't"],
        "away.": ["a", "way."], "There's": ["There's"]}
def split_words(text, sy):
    out = []; ws = text.replace('"', "").split()
    for w in ws:
        n = len(P.syl(w)); core = w.rstrip(",.;:?")
        if n <= 1: out.append((w, False)); continue
        parts = HFIX.get(w) or HFIX.get(core) or _PY.inserted(core).split("-")
        tail = "" if w in HFIX else w[len(core):]
        if len(parts) > n: parts = parts[:n - 1] + ["".join(parts[n - 1:])]
        while len(parts) < n: parts.append("_")
        for j, p in enumerate(parts): out.append((p + (tail if j == n - 1 else ""), j < n - 1))
    assert len(out) == len(sy), (text, out, sy)
    return out
TEXT = {sec: [split_words(t, P.LINES[sec][i]) for i, (_, t) in enumerate(M.WORDS_OF[sec])] for sec in P.SUNG}
for i_ in (2, 3):                                                                       # the counter's words in quotes
    ws = TEXT["Verse 2"][i_]
    for j, (t, h) in enumerate(ws):
        if t in ("Noth", "There's"): ws[j] = ("“" + t, h)
        if t in ("save,", "it,"): ws[j] = (t + "”", h)
LC0 = P.BAR0["Last Chorus"]
def kit_of(b):
    if not (LC0 <= b < LC0 + 10): return None
    return "brushes" if b < LC0 + 6 else "sticks"
bars = []
for nm, kind, nb in P.FORM:
    for k in range(nb):
        b = P.BAR0[nm] + k
        bars.append(dict(sec=nm, kind=kind, k=k, n=nb, chord=P.CHORD[b], roman=M.ROMAN[P.CHORD[b]], start=b * BAR, len=BAR, qbpm=QB, key="B-flat major",
                         kit=kit_of(b), stop=False))
lead = []
for n in c["notes"]:
    sec, i = n["line"].split(":"); i = int(i); t, hy = TEXT[sec][i][n["syl"]]
    lead.append(dict(on=n["on"], dur=n["dur"], midi=n["p"], sec=sec, line=i, syl=n["syl"], first=not n["slur"], text=t, hyph=hy,
                     stress=P.LINES[sec][i][n["syl"]][1], role=M.WORDS_OF[sec][i][0], singer="voice"))
tag = lead[-1]; tag["dur"] = max(tag["dur"], (LC0 + 12) * BAR - tag["on"])               # 'back' held to the end of the last chorus
ROOT = {k: v[0] for k, v in M.CH.items()}
def low_root(ch, lo=34): return lo + (ROOT[ch] - lo) % 12                               # B-flat 1 .. A2
def chord3(ch, lo):
    out, p = [], lo
    while len(out) < 3:
        if p % 12 in M.CH[ch][1]: out.append(p)
        p += 1
    return out
rh, lh, cello, bass, drums, gtr = [], [], [], [], [], []
def ev(lst, on, dur, p, vel, art="", **kw): lst.append(dict(on=on, dur=dur, p=p if isinstance(p, list) else [p], vel=vel, art=art, **kw))
DR = dict(kick=36, snare=38, hh=42, ride=51, crash=49, tap=38, swirl=40)
V3S = P.BAR0["Verse 3"]
for bi, b in enumerate(bars):
    sec, kind, ch, st, k, n = b["sec"], b["kind"], b["chord"], b["start"], b["k"], b["n"]
    r = low_root(ch); r2 = r + 12
    if kind == "Outro" and k == n - 1:                                                   # one B-flat chord, let ring
        ev(rh, st, BAR, chord3("Bb", 62) + [74], 64, "ring"); ev(lh, st, BAR, [34, 41, 46], 66, "ring"); ev(cello, st, BAR, [46], 52, "ring"); continue
    # ---- the piano's left hand ----
    if kind in ("Intro", "Outro", "Verse") and not (sec == "Verse 3" and k < 4):
        ev(lh, st, 24, [r, r2] if kind != "Verse" else [r2], 62, "half"); ev(lh, st + 24, 24, [r2 + 7], 56, "half")
    elif sec == "Verse 3": ev(lh, st, BAR, [r, r2], 52, "whole")
    elif kind == "Bridge": ev(lh, st, BAR, [r2, r2 + 7], 56, "whole")
    elif sec == "Last Chorus" and k >= 10: ev(lh, st, BAR, [r, r2], 54, "whole")
    elif sec == "Last Chorus": [ev(lh, st + 6 * j, 6, [r2 if j % 2 == 0 else r2 + 12], 70 if j % 2 == 0 else 62, "eighth") for j in range(8)]
    else: [ev(lh, st + 12 * j, 12, [x], 64 if j == 0 else 58, "quarter") for j, x in enumerate((r2, r2 + 7, r2 + 12, r2 + 7))]
    # ---- the piano's right hand ----
    if kind in ("Intro", "Outro"):
        ev(rh, st, 6, chord3(ch, 58), 58, "under")                                     # a soft chord under the figure's first beat
    elif sec == "Verse 3" and k < 4: ev(rh, st, BAR, chord3(ch, 58), 50, "whole")
    elif kind == "Verse":
        cv = chord3(ch, 58); pat = [cv[0], cv[1], cv[2], cv[1]] * 2
        for j, p in enumerate(pat): ev(rh, st + 6 * j, 6, [p], 56 if j % 4 == 0 else 48, "broken")
    elif kind == "Bridge": ev(rh, st, 24, chord3(ch, 58), 52, "half"); ev(rh, st + 24, 24, chord3(ch, 58), 48, "half")
    elif sec == "Last Chorus" and k >= 10: ev(rh, st, BAR, chord3(ch, 58), 48, "whole")
    elif sec == "Last Chorus": [ev(rh, st + 12 * j, 12, chord3(ch, 60) + ([chord3(ch, 60)[0] + 12] if j == 0 else []), 70 if j == 0 else 62, "block") for j in range(4)]
    else:
        cv = chord3(ch, 60); pat = [cv[0], cv[1], cv[2], cv[1]] * 2
        for j, p in enumerate(pat): ev(rh, st + 6 * j, 6, [p], 62 if j % 4 == 0 else 52, "broken")
    # ---- cello ----
    if sec in ("Verse 2", "Chorus 2") or (sec == "Verse 3" and k >= 4):
        ev(cello, st, 46, [r2 + (12 if r2 < 43 else 0)], 54 + (6 if kind == "Chorus" else 0), "held")
    # ---- the band: the last chorus, bars 1-10 ----
    kit = b["kit"]
    if kit:
        if k < 6: ev(bass, st, 46, [r + (12 if r < 36 else 0)], 82, "whole")
        else: ev(bass, st, 22, [r + (12 if r < 36 else 0)], 88, "half"); ev(bass, st + 24, 22, [r + 7 + (12 if r < 36 else 0)], 82, "half")
        cv = chord3(ch, 55)
        for j, p in enumerate([cv[0], cv[2], cv[1] + 12, cv[2]] * 2): ev(gtr, st + 6 * j, 6, [p], 60 if j % 4 == 0 else 52, "arp")
        if kit == "brushes":
            ev(drums, st, 3, DR["kick"], 60, kit=kit); ev(drums, st + 24, 3, DR["kick"], 56, kit=kit)
            [ev(drums, st + e, 3, DR["tap"], 58, kit=kit) for e in (12, 36)]; [ev(drums, st + e, 12, DR["swirl"], 42, kit=kit) for e in (0, 12, 24, 36)]
        else:
            if k == 6: ev(drums, st, 3, DR["crash"], 96, kit=kit)
            [ev(drums, st + e, 3, DR["kick"], 90 if e == 0 else 80, kit=kit) for e in (0, 24, 30)]; [ev(drums, st + e, 3, DR["snare"], 92, kit=kit) for e in (12, 36)]
            [ev(drums, st + e, 3, DR["ride"], 70 if e % 12 == 0 else 58, kit=kit) for e in range(0, 48, 6)]
            if k == 9: [ev(drums, st + e, 3, DR["snare"], 70 - 6 * j, "fill", kit=kit) for j, e in enumerate((36, 39, 42, 45))]
# ---- the intro and outro figure (the right hand), the cello's countermelody ----
for e in RF["lick"]: ev(rh, e["on"], 0, [e["p"]], 66 if e["where"] == "intro" else 60, "figure:" + e["where"])
for e in RF["counter"]: ev(cello, e["on"], e["dur"], [e["p"]], 58, "counter")
def tidy(lst):                                                                           # one hand plays one line: durations to the next onset
    lst.sort(key=lambda e: (e["on"], e["p"][0])); out = []
    for e in lst:
        if out and out[-1]["on"] == e["on"]: out[-1]["p"] = sorted(set(out[-1]["p"] + e["p"])); out[-1]["vel"] = max(out[-1]["vel"], e["vel"]); out[-1]["art"] = e["art"] if e["art"].startswith("figure") else out[-1]["art"]; continue
        out.append(e)
    for j, e in enumerate(out):
        nx = out[j + 1]["on"] if j + 1 < len(out) else NB * BAR
        if e["dur"] == 0 or e["on"] + e["dur"] > nx: e["dur"] = nx - e["on"]
    return out
rh = tidy(rh); lh = tidy(lh); cello = tidy(cello)
for lst in (bass, drums, gtr): lst.sort(key=lambda e: (e["on"], e["p"][0]))
plan = [(nm, nb, P.BAR0[nm], "4/4") for nm, _, nb in P.FORM]
secs = NB * 4 * 60 / QB
rec = dict(title="Nothing Important", nbars=NB, bars=bars, plan=plan, lead=lead, harm=[], piano_rh=rh, piano_lh=lh, cello=cello, bass=bass, drums=drums, gtr=gtr,
           slot="twelfth of a beat", bar=BAR, qbpm=QB, feel="straight eighths", seconds=secs, tw_sec=60 / QB / 12, fp=c["fp"],
           order_fp=F["run"]["order_fp"], survivors=F["run"]["survivors"], built=F["run"]["made"], meas={k: (float(v) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()},
           judge={k: c["judge"][k] for k in ("combined", "content", "order")}, plans=c["meta"]["plans"], hand_edits=c["hand_edits"], picked_from=c["picked_from"],
           kinds={f"{a}:{b}": v for (a, b), v in c["meta"]["kinds"].items()}, rerun=F["run"]["rerun"], text=TEXT, lift=c["info"]["lift"], registers=c["meta"]["registers"],
           design=dict(gates=P.DESIGN_GATES, slots={s: P.slots_of(s) for s in P.SUNG}, counter="cello: holds in verse 2 and chorus 2; countermelody in the bridge and last chorus (Q14 A)"),
           riff=dict(RF["pick"], drawn=RF["drawn"], passed=RF["passed"], seed=RF["seed"], counter_check=RF["counter_check"], r319=RF["r319"]))
pickle.dump(rec, open("/home/claude/p42/song_record.pkl", "wb"))
if __name__ == "__main__":
    print(NB, "bars,", f"{secs:.0f} s;", len(lead), "sung;", {k: len(v) for k, v in dict(rh=rh, lh=lh, cello=cello, bass=bass, drums=drums, gtr=gtr).items()})
    for sec in P.SUNG:
        for i, ws in enumerate(TEXT[sec]): print(sec, i, " ".join(t + ("-" if h else "") for t, h in ws))
