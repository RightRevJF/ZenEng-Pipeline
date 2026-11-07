"""The band for 'What Holds' -- one set of rules, read by the demo (which humanizes it) and by the parts (which write it out), so the
two always agree. Times in eighths. Driving rock built on tension: every chord change is pushed -- the bass and the rhythm guitar play
the next chord on the 'and' of 4 and tie it over the bar line (Q tempo/feel A).
  Intro    riff guitar alone for four bars; then drums, bass doubling the roots, guitar stabs.
  Verses   coiled: tight kick and backbeat, closed hats; bass and palm-muted root-fifth guitar locked on 1, the 'and' of 2, 3 and 4;
           organ low.
  Choruses released: crash, ride, kick on 1, the 'and' of 2 and 3; open power chords and bass in straight eighths; organ up.
  Riff     the riff guitar over the full band.
  Bridge   the pressure builds over eight bars (kick quarters; then the backbeat; then snare on every beat; then snare eighths), the bass a
           pedal then eighths, the guitar eighths rising, all of it ramping 0.7 -> 1.05.
  Chorus 3 stripped: the band drops out; a clean guitar rings one chord a bar, the organ soft; a snare build in the last bar.
  Chorus 4 everything; crash and china on STAND (A4, over D), crash on HOLDS (G); a tom fill into the outro.
  Outro    the riff over the full band; the last bar one hit on E minor, let ring."""
import pickle, collections
REC = pickle.load(open("/home/claude/p23/song_record.pkl", "rb"))
BARS = REC["bars"]; NB = len(BARS)
ROOT = {"Em": 4, "C": 0, "D": 2, "G": 7, "Am": 9}
TONES = {"Em": [4, 7, 11], "C": [0, 4, 7], "D": [2, 6, 9], "G": [7, 11, 2], "Am": [9, 0, 4]}
DRUM_MIDI = dict(bd=36, sn=38, hh=42, hho=46, cymr=51, cymc=49, cymch=52, tomh=50, tommh=48, tomml=47, toml=45, tomfl=43)
def voicing(ch, lo=52, n=4):
    out, p = [], lo
    while len(out) < n:
        if p % 12 in TONES[ch]: out.append(p)
        p += 1
    return out
def broot(ch): return 28 + ((ROOT[ch] - 28) % 12)
def sec_info(bi):
    sec = BARS[bi]["sec"]; idx = [x for x in range(NB) if BARS[x]["sec"] == sec]
    return sec, bi - idx[0], len(idx)
def events():
    E = collections.defaultdict(list); D = collections.defaultdict(dict)
    def add(inst, on, dur, ps, vel, art=""): E[inst].append(dict(on=on, dur=dur, p=list(ps), vel=vel, art=art))
    def dr(on, name, vel): D[on][name] = max(vel, D[on].get(name, 0))
    pushed = set()                                             # bars whose downbeat is already sounding (a push tied over)
    for bi, b in enumerate(BARS):
        sec, k, n = sec_info(bi); ch = b["chord"]; st = b["start"]; r = broot(ch)
        nxt = BARS[bi + 1] if bi + 1 < NB else None
        nsec = nxt["sec"] if nxt else None
        change = nxt is not None and nxt["chord"] != ch and nsec == sec
        verse = sec.startswith("Verse"); cho = sec in ("Chorus 1", "Chorus 2", "Chorus 4")
        band = (sec == "Intro" and k >= 4) or sec in ("Riff", "Outro")
        last_outro = sec == "Outro" and k == n - 1
        g = 0.7 + 0.35 * k / max(1, n - 1) if sec == "Bridge" else 1.0
        pw = [r + 12, r + 19, r + 24]
        if last_outro:
            add("bass", st, 8, [r], 90); add("gtr", st, 8, pw, 100, "ring"); add("keys", st, 8, voicing(ch, 52, 4), 70); dr(st, "cymc", 110); dr(st, "bd", 100)
            continue
        # ---- keys (organ, from the chord symbols) ----
        if verse: add("keys", st, 8, voicing(ch, 52, 3), 46)
        elif cho: add("keys", st, 8, voicing(ch, 55, 4), 62)
        elif sec == "Bridge": add("keys", st, 8, voicing(ch, 55, 4), int(58 * g))
        elif sec == "Chorus 3": add("keys", st, 8, voicing(ch, 55, 3), 40)
        # ---- bass ----
        if verse:
            for e in (0, 3, 4, 6): add("bass", st + e, 1, [r], 84 if e == 0 else 72, "mute")
            if change: add("bass", st + 7, 1, [broot(nxt["chord"])], 80, "push")
        elif band:
            for e in range(8 if not change else 7): add("bass", st + e, 1, [r], 84 if e == 0 else 70)
            if change: add("bass", st + 7, 1, [broot(nxt["chord"])], 80, "push")
        elif cho:
            for e in range(0 if bi not in pushed else 3, 7): add("bass", st + e, 1, [r], 90 if e == 0 else 78)
            if change: add("bass", st + 7, 4, [broot(nxt["chord"])], 88, "push"); pushed.add(bi + 1)
            else: add("bass", st + 7, 1, [r], 76)
        elif sec == "Bridge":
            if k < 4:
                for e in (0, 2, 4, 6): add("bass", st + e, 2, [r], int(80 * g))
            else:
                for e in range(8): add("bass", st + e, 1, [r], int(84 * g))
        # ---- guitar ----
        if verse:
            for e in (0, 3, 4, 6): add("gtr", st + e, 1, [r + 12, r + 19], 54, "mute")
            if change: add("gtr", st + 7, 1, [broot(nxt["chord"]) + 12, broot(nxt["chord"]) + 19], 62, "push")
        elif cho:
            for e in range(0 if bi not in pushed else 3, 7): add("gtr", st + e, 1, pw, 92 if e == 0 else 84)
            if change: add("gtr", st + 7, 4, [broot(nxt["chord"]) + 12, broot(nxt["chord"]) + 19, broot(nxt["chord"]) + 24], 94, "push")
            else: add("gtr", st + 7, 1, pw, 84)
        elif band and not (sec == "Intro" and k < 4):
            if sec == "Intro":
                add("gtr", st, 3, pw, 84, "ring")
                if change: add("gtr", st + 7, 1, [broot(nxt["chord"]) + 12, broot(nxt["chord"]) + 19], 84, "push")
            else:
                for e in range(8 if not change else 7): add("gtr", st + e, 1, [r + 12, r + 19], 80)
                if change: add("gtr", st + 7, 1, [broot(nxt["chord"]) + 12, broot(nxt["chord"]) + 19], 88, "push")
        elif sec == "Bridge":
            for e in range(8): add("gtr", st + e, 1, [r + 12, r + 19] if k < 6 else pw, int(70 * g))
        elif sec == "Chorus 3":
            add("cgtr", st, 8, voicing(ch, 52, 5), 58, "ring")
        # ---- drums ----
        if verse:
            dr(st, "bd", 84); dr(st + 3, "bd", 70); dr(st + 2, "sn", 82); dr(st + 6, "sn", 84)
            for e in range(8): dr(st + e, "hh", 44 if e % 2 == 0 else 32)
        elif cho:
            for e in (0, 3, 4): dr(st + e, "bd", 92 if e != 3 else 78)
            dr(st + 2, "sn", 96); dr(st + 6, "sn", 98)
            for e in range(8): dr(st + e, "cymr", 52 if e % 2 == 0 else 38)
            if k == 0: dr(st, "cymc", 108)
            if sec == "Chorus 4":
                line4 = k - 6                                   # bars 7-10 are the turn (C D G G)
                if line4 == 1: dr(st, "cymc", 112); dr(st, "cymch", 100)
                if line4 == 2: dr(st, "cymc", 112)
                if line4 == 3:
                    for i, t in enumerate(["tomh", "tommh", "tomml", "toml"]): dr(st + 4 + i, t, 96)
        elif band and not (sec == "Intro" and k < 4):
            dr(st, "bd", 90); dr(st + 3, "bd", 76); dr(st + 4, "bd", 84); dr(st + 2, "sn", 92); dr(st + 6, "sn", 94)
            for e in range(8): dr(st + e, "hho" if sec != "Intro" and e % 2 == 0 else "hh", 50 if e % 2 == 0 else 36)
            if k == 0 and sec != "Intro": dr(st, "cymc", 104)
        elif sec == "Bridge":
            q = k // 2
            for e in (0, 2, 4, 6): dr(st + e, "bd", int(84 * g))
            if q == 0:
                for e in range(8): dr(st + e, "tomfl", int((50 if e % 2 == 0 else 38) * g))
            if q == 1: dr(st + 2, "sn", int(88 * g)); dr(st + 6, "sn", int(90 * g)); [dr(st + e, "hh", int(44 * g)) for e in range(8)]
            if q == 2: [dr(st + e, "sn", int(86 * g)) for e in (0, 2, 4, 6)]; [dr(st + e, "hh", int(46 * g)) for e in range(8)]
            if q == 3: [dr(st + e, "sn", int((70 + 4 * e) * g)) for e in range(8)]
        elif sec == "Chorus 3":
            if k == n - 1: [dr(st + e, "sn", 50 + 7 * e) for e in range(8)]
    for inst in E: E[inst].sort(key=lambda x: x["on"])
    return E, D
if __name__ == "__main__":
    E, D = events()
    for k, v in E.items(): print(k, len(v))
    print("drum hits", sum(len(v) for v in D.values()))
