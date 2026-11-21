"""945 (Window 197): a check of the lyric's room, run when a lyric is locked and before any music is written.
A kept song's voice is busy for a stretch and sparse or silent for a stretch, and that is what gives its rhythm a long memory (studies/rhythm_memory).
A lyric that fills every bar, with verse and chorus lines of one length, cannot be given that by any setting. This says so while the words can still change.
    python3 lib/luthier/lyric_room.py songs/pNN/lyricNN.json [tunes=40]
It lays the song out as the engine will and draws quick tunes; no pick is made, nothing is written but lyricNN.room.json beside the lyric."""
import os, sys, json, random, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); TABLE = os.path.join(HERE, "..", "..", "tables", "kept_rhythm_room.json")
def read(ons, bar=48):
    """onsets in twelfths of a quarter -> room, contrast, rhythm scaling"""
    import scaling as SC
    ons = sorted(int(t) for t in ons); t0 = ons[0] // bar; nb = ons[-1] // bar - t0 + 1; cnt = np.zeros(nb)
    for t in ons: cnt[t // bar - t0] += 1
    w = [cnt[i:i + 4].mean() for i in range(0, nb - 3, 4)]; g0 = ons[0] // 3; grid = np.zeros(ons[-1] // 3 - g0 + 1); grid[[t // 3 - g0 for t in ons]] = 1; a = SC.dfa(grid)
    return dict(room=float(np.mean(cnt == 0)), contrast=float(np.std(w) / np.mean(w)) if len(w) >= 3 and np.mean(w) > 0 else float("nan"), rhythm_scaling=a["alpha"] if a else float("nan"))
def check(L, tunes=40):
    sys.path.insert(0, HERE); import song_from_lyric as SL, metre_engine as M
    class Got(Exception): pass
    cap = {}
    def capture(self, N, seed):
        rng = random.Random(f"room {seed}"); rows = []; tries = 0
        while len(rows) < tunes and tries < 12 * tunes:
            c, err = self.build(rng); tries += 1
            if err or self.gates(c): continue
            rows.append(read([n["on"] for n in self.as_sung(c["notes"])], self.BAR))
        cap.update(rows=rows, tries=tries, spec=self.S, bar=self.BAR); raise Got()
    old = M.Engine.run; M.Engine.run = capture
    try: SL.write(L, 1000, 12)
    except Got: pass
    finally: M.Engine.run = old
    if not cap.get("rows"): return dict(error="no tune could be drawn for this lyric", tries=cap.get("tries"))
    T = json.load(open(TABLE))["percentiles_10_25_50_75_90"]; med = {c: round(float(np.nanmedian([r[c] for r in cap["rows"]])), 3) for c in ("room", "contrast", "rhythm_scaling")}
    place = {c: ("under the kept 25th" if med[c] < T[c][1] else "over the kept 75th" if med[c] > T[c][3] else "in the kept middle half") for c in med}
    spec = cap["spec"]; sung = spec["sung"]; ln = lambda kind: [len(l) for n, k, ls in sung if k == kind for l in ls]; v, c = ln("Verse"), ln("Chorus"); form = spec["form"]; bars = sum(len(b) for _, b in form); secs = round(bars * 4 * 60.0 / L["bpm"])
    sung_bars = sum(len(b) for n, b in form if any(n == s[0] for s in sung)); words = []
    if place["room"] == "under the kept 25th":
        words.append(f"The words leave little room. About {round(100 * med['room'])} bars in a hundred have nothing sung; kept songs leave {round(100 * T['room'][1])} to {round(100 * T['room'][3])}. The song runs {secs} seconds over {bars} bars, and {sung_bars} of those bars belong to sung sections. Fewer lines, or a verse less, would leave room for the voice to rest.")
    if place["contrast"] == "under the kept 25th":
        words.append(f"The singing is one busyness all through. The verse's lines run {np.mean(v):.1f} syllables and the chorus's {np.mean(c):.1f}" + (" (close to the same)" if c and v and abs(np.mean(v) - np.mean(c)) < 0.25 * max(np.mean(v), np.mean(c)) else "") + ". Kept songs change: a wordy verse against a chorus of few, held words, or the reverse. Lines of clearly different length in verse and chorus would give the tune that change.") if v and c else None
    if not words: words.append("The words leave room and the sections differ in how busy they are, as kept songs do.")
    return dict(title=L["title"], tunes_read=len(cap["rows"]), tries=cap["tries"], readings=med, kept_25th_middle_75th={k: [T[k][1], T[k][2], T[k][3]] for k in med}, place=place, seconds=secs, bars=bars, bars_in_sung_sections=sung_bars,
                syllables_a_line=dict(verse=round(float(np.mean(v)), 1) if v else None, chorus=round(float(np.mean(c)), 1) if c else None), in_plain_words=[w for w in words if w])
def stamp():
    """953 (749.132): the engine and the tables that made a room file, so a file that no longer matches its engine can be seen. Hashes of the files' contents, not a commit
    (a commit is not known until the file is in it): every .py in lib/luthier, every .json under tables. A rerun on the same engine gives the same file byte for byte."""
    import hashlib, glob
    def h(paths):
        s = hashlib.sha1()
        for q in sorted(paths): s.update(os.path.basename(q).encode()); s.update(open(q, "rb").read())
        return s.hexdigest()[:12]
    root = os.path.join(HERE, "..", ".."); return dict(engine=h(glob.glob(os.path.join(HERE, "*.py"))), tables=h(glob.glob(os.path.join(root, "tables", "**", "*.json"), recursive=True)), note="953: sha1 of every .py in lib/luthier and of every .json under tables; lib/luthier/lyric_room.py --check lists room files that no longer match")
if __name__ == "__main__":
    if sys.argv[1] == "--check":
        import glob; now = stamp(); bad = [q for q in sorted(glob.glob(os.path.join(HERE, "..", "..", "songs", "*", "*.room.json"))) if {k: v for k, v in (json.load(open(q)).get("made_by") or {}).items() if k != "note"} != {k: v for k, v in now.items() if k != "note"}]
        print("every room file is this engine's" if not bad else "room files not made by this engine (rerun them):\n  " + "\n  ".join(os.path.relpath(q) for q in bad)); sys.exit(1 if bad else 0)
    L = json.load(open(sys.argv[1])); R = check(L, int(sys.argv[2]) if len(sys.argv) > 2 else 40); R["made_by"] = stamp(); json.dump(R, open(sys.argv[1].replace(".json", ".room.json"), "w"), indent=1)
    if "error" in R: print(R["error"]); sys.exit(1)
    print(f"{R['title']}: the lyric's room ({R['tunes_read']} quick tunes)")
    for k, nm in (("room", "bars with nothing sung"), ("contrast", "change in how busy the singing is"), ("rhythm_scaling", "rhythm scaling")): print(f"  {nm:36} {R['readings'][k]:<6} kept {R['kept_25th_middle_75th'][k]}   {R['place'][k]}")
    for w in R["in_plain_words"]: print("  " + w)
