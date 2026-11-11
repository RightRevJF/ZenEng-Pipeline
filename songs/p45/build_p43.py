"""Blue Movie (song 43): the song record from melody_final.pkl (the pick of record) -- up-tempo dance-pop, q = 118, four on the floor,
straight, A minor, 80 bars (Q8 C, Q9 A, Q16 A; 'Houdini' the lead reference, Q17 A).
  voice   the tenor, every line.
  drums   kick on every beat from intro bar 5; off-beat open hats; claps on 2 and 4 from the pre-chorus on (verse 2 has them too);
          sixteenth closed hats in the choruses and post-choruses; a snare build in each pre-chorus's last bar and the bridge's last two;
          out for the bridge (bars 1-6) and for the last post-chorus, where only the kick returns on its last two bars.
  bass    synth bass in eighths, root and octave; the bridge in whole notes; the last post-chorus held.
  pad     the chord, held a bar, through everything but the intro's first four bars; it flickers (production note).
  pluck   (Q16 A) the 'blue movie' figure: the intro (bars 1-8), an octave above the voice in each post-chorus, under the whole last
          chorus, the outro. Verses thinner, the last chorus the fullest (9.12).
  The outro ends on one A minor chord, let ring."""
import pickle, sys
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p45", "/home/claude/p40"]
import melody_p43 as P
M = P.M
import pyphen
F = pickle.load(open("/home/claude/p45/melody_final.pkl", "rb")); c = F["pick"]
BAR = 48; NB = P.NBARS; QB = 118
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"picture,": ["pic", "ture,"], "every": ["ev", "ery"], "pleather": ["pleath", "er"], "sweating,": ["sweat", "ing,"], "speakers": ["speak", "ers"],
        "nobody": ["no", "bo", "dy"], "movie,": ["mo", "vie,"], "movie": ["mo", "vie"], "Somebody": ["Some", "bo", "dy"], "shoulder,": ["shoul", "der,"],
        "credits": ["cred", "its"], "empty": ["emp", "ty"], "socket": ["sock", "et"], "starring": ["star", "ring"], "only": ["on", "ly"], "isn't": ["is", "n't"],
        "after": ["af", "ter"], "any": ["an", "y"], "rules": ["rules"], "behind": ["be", "hind"], "beneath": ["be", "neath"], "evidence": ["ev", "i", "dence"], "crossing": ["cross", "ing"]}
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
bars = []
for nm, kind, nb in P.FORM:
    for k in range(nb):
        b = P.BAR0[nm] + k
        bars.append(dict(sec=nm, kind=kind, k=k, n=nb, chord=P.CHORD[b], roman=M.ROMAN[P.CHORD[b]], start=b * BAR, len=BAR, qbpm=QB, key="A minor", stop=False))
lead = []
for n in c["notes"]:
    sec, i = n["line"].split(":"); i = int(i); t, hy = TEXT[sec][i][n["syl"]]
    lead.append(dict(on=n["on"], dur=n["dur"], midi=n["p"], sec=sec, line=i, syl=n["syl"], first=not n["slur"], text=t, hyph=hy,
                     stress=P.LINES[sec][i][n["syl"]][1], role=M.WORDS_OF[sec][i][0], singer="voice"))
ROOT = {k: v[0] for k, v in M.CH.items()}
def low_root(ch, lo=33): return lo + (ROOT[ch] - lo) % 12                               # A1 .. G#2
def chord3(ch, lo):
    out, p = [], lo
    while len(out) < 3:
        if p % 12 in M.CH[ch][1]: out.append(p)
        p += 1
    return out
drums, bass, pad, pluck = [], [], [], []
def ev(lst, on, dur, p, vel, art="", **kw): lst.append(dict(on=on, dur=dur, p=p if isinstance(p, list) else [p], vel=vel, art=art, **kw))
DR = dict(kick=36, clap=39, snare=38, ohh=46, chh=42, crash=49)
FIGL = [n for n in c["notes"] if n["line"] == "Chorus 1:2"]; FU = P.line_start("Chorus 1", 2)
FIG = [(n["on"] - FU, n["p"]) for n in FIGL]                                              # the 'blue movie' figure: six notes over two bars
for b in bars:
    sec, kind, ch, st, k, n = b["sec"], b["kind"], b["chord"], b["start"], b["k"], b["n"]
    r = low_root(ch)
    last = kind == "Outro" and k == n - 1
    if last:
        ev(pad, st, BAR, chord3("Am", 57), 60, "ring"); ev(bass, st, BAR, [33], 84, "ring"); ev(drums, st, 3, DR["kick"], 96); ev(drums, st, 3, DR["crash"], 90); continue
    full = kind in ("Chorus", "Post") and sec != "Post 3"
    lift = 14 if sec == "Last Chorus" else 6 if kind == "Chorus" else -6 if kind == "Post" else -10 if kind == "Verse" else 0   # 9.12: verses thinner, the last chorus the top
    # ---- drums ----
    kick = not (kind == "Intro" and k < 4) and kind != "Bridge" and not (sec == "Post 3" and k < 2)
    if kind == "Bridge" and k >= 6: kick = True
    if kick: [ev(drums, st + e, 3, DR["kick"], (100 if e == 0 else 92) + min(lift, 8)) for e in (0, 12, 24, 36)]
    if kick and sec != "Post 3": [ev(drums, st + e, 3, DR["ohh"], 70 + lift) for e in (6, 18, 30, 42)]
    if (kind in ("Pre", "Chorus", "Post") or sec == "Verse 2") and sec != "Post 3": [ev(drums, st + e, 3, DR["clap"], 96 + min(lift, 10)) for e in (12, 36)]
    if full and kind == "Chorus": [ev(drums, st + e, 3, DR["chh"], 58 + lift) for e in range(0, 48, 3) if e % 6 == 3]
    if (kind == "Pre" and k == n - 1) or (kind == "Bridge" and k >= 6):
        [ev(drums, st + e, 3, DR["snare"], 60 + e, "build") for e in range(0, 48, 6 if (kind == "Bridge" and k == 6) else 3)]
    if kind in ("Chorus",) and (k == 0 or (sec == "Last Chorus" and k == 4)): ev(drums, st, 3, DR["crash"], 100 + min(lift, 10))
    # ---- bass ----
    if kind == "Bridge" and k < 6: ev(bass, st, 46, [r + 12], 80, "whole")
    elif sec == "Post 3": ev(bass, st, 46, [r + 12], 76, "whole")
    elif not (kind == "Intro" and k < 4):
        for j in range(8): ev(bass, st + 6 * j, 5, [r + 12 if j % 2 else r], (92 if j % 2 == 0 else 84) + lift // 2, "pulse")
    # ---- pad ----
    if not (kind == "Intro" and k < 4): ev(pad, st, BAR, chord3(ch, 57) + ([chord3(ch, 57)[0] + 12] if kind == "Chorus" else []), (50 if kind != "Bridge" else 58) + lift // 2, "pad")
    # ---- the pluck: the figure ----
    if kind in ("Intro", "Outro") or (kind == "Post" and sec != "Post 3") or sec == "Last Chorus":       # the last chorus: the figure under it all
        half = k % 2                                                                       # the figure's two bars, in turn
        for (t, p) in FIG:
            if half * BAR <= t < (half + 1) * BAR: ev(pluck, st + t - half * BAR, 6, [p + 12], 74 if kind != "Post" else 62 if sec != "Last Chorus" else 70, "pluck")
def tidy(lst):
    lst.sort(key=lambda e: (e["on"], e["p"][0])); out = []
    for e in lst:
        if out and out[-1]["on"] == e["on"]: out[-1]["p"] = sorted(set(out[-1]["p"] + e["p"])); out[-1]["vel"] = max(out[-1]["vel"], e["vel"]); continue
        out.append(e)
    return out
drums = tidy(drums); bass = tidy(bass); pad = tidy(pad); pluck = tidy(pluck)
plan = [(nm, nb, P.BAR0[nm], "4/4") for nm, _, nb in P.FORM]
secs = NB * 4 * 60 / QB
rec = dict(title="Blue Movie", nbars=NB, bars=bars, plan=plan, lead=lead, drums=drums, bass=bass, pad=pad, pluck=pluck,
           slot="twelfth of a beat", bar=BAR, qbpm=QB, feel=P.FEEL, seconds=secs, tw_sec=60 / QB / 12, fp=c["fp"],
           order_fp=F["run"]["order_fp"], survivors=F["run"]["survivors"], built=F["run"]["made"], meas={k: (float(v) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()},
           judge={k: c["judge"][k] for k in ("combined", "content", "order")}, plans=c["meta"]["plans"], hand_edits=c["hand_edits"], picked_from=c["picked_from"],
           kinds={f"{a}:{b}": v for (a, b), v in c["meta"]["kinds"].items()}, rerun=F["run"]["rerun"], text=TEXT, lift=c["info"]["lift"], registers=c["meta"]["registers"],
           palettes=c["meta"]["palettes"], outside_target=c["meta"]["outside_target"], carriers=c["meta"]["carriers"],
           design=dict(gates=P.DESIGN_GATES, slots={s: P.slots_of(s) for s in P.SUNG}, figure=FIG))
pickle.dump(rec, open("/home/claude/p45/song_record.pkl", "wb"))
if __name__ == "__main__":
    print(NB, "bars,", f"{secs:.0f} s;", len(lead), "sung;", {k: len(v) for k, v in dict(drums=drums, bass=bass, pad=pad, pluck=pluck).items()})
    for sec in P.SUNG:
        for i, ws in enumerate(TEXT[sec]): print(sec, i, " ".join(t + ("-" if h else "") for t, h in ws))
