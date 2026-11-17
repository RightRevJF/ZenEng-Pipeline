"""research_p67.py: the research gates for song 57 (Parts 30 and 31), read on any build's notes. Used by pick_p67.py over the clean
survivors of the engine's run, before luthier_judge5's pick, and printed in the test report.
  R1 (H5)  the chorus above the verse: chorus 1's mean pitch over verse 1's (choruses are higher in 67% of songs, +1.5 semitones)
  R2 (H2)  the chorus repeats itself: chorus 1's cell recurrence at or above the 50th length-matched percentile of Hooktheory choruses,
           and above verse 1's percentile among verses
  R3 (H1)  typical cells: chorus 1's cells at or above the 60th length-matched percentile for typicality (mean log2 document frequency)
  R4 (H1)  interval variety and surprise per note at or below the 50th length-matched percentile
  R5 (P31) long notes (1.5 times the song's median length or more) on stressed syllables at least 75% of the time
  R6 (H3)  the title: its stressed syllables on a beat, held longer than the song's median note (report)
  R7 (H4)  the uniqueness point of chorus 1's opening, rhythm counted, at or under 8 notes (report)
Length-matched: Hooktheory clips of the same section kind with a note count within 25% of ours."""
import sys, json, math, gzip, collections, pickle, os
import numpy as np
sys.path[:0] = ["/home/claude/zeneng-pipeline/studies/hooks", "/home/claude/shape"]
import hooks_hooktheory as HH
import surprise_hooktheory as SH
from surprise_our_songs import mel_tokens
TONIC = 4; BEAT = 12
CACHE = "/home/claude/p67/research_cache.pkl"
class Ref:
    def __init__(self):
        if os.path.exists(CACHE):
            self.__dict__.update(pickle.load(open(CACHE, "rb"))); self.MM = SH.VOM(84).fit(self.mm_seqs); return
        clips = HH.load(); songs = sorted({c["song"] for c in clips}); sid = {s: i for i, s in enumerate(songs)}; self.NS = len(songs)
        by_song = collections.defaultdict(set); self.mm_seqs = []
        for c in clips:
            c["tr"], c["tp"] = HH.tokens(c["notes"])
            for n in (3, 4, 5): by_song[sid[c["song"]]].update(HH.ngrams(c["tr"], n))
            self.mm_seqs.append(SH.tokens(c["raw"])[0])
        self.df = collections.Counter()
        for cells in by_song.values(): self.df.update(cells)
        self.present = {n: set() for n in range(2, 13)}
        for c in clips:
            for n in range(2, 13): self.present[n].update(HH.ngrams(c["tr"], n))
        D = json.load(gzip.open("/home/claude/zeneng-pipeline/studies/hooks/hooks_clips.json.gz", "rt"))
        self.ref = {k: [dict(n=x["n"], recurrence=x["recurrence"], convention=x["convention"], i_entropy=x["i_entropy"], ic_mean=x["ic_mean"]) for x in D if x["section"] == k] for k in ("chorus", "verse")}
        self.MM = SH.VOM(84).fit(self.mm_seqs)
        pickle.dump(dict(NS=self.NS, df=self.df, present=self.present, ref=self.ref, mm_seqs=self.mm_seqs), open(CACHE, "wb"))
    def feats(self, notes):
        """notes: (on_beats, off_beats, midi) in order."""
        tr, tp = HH.tokens(notes); ps = [n[2] for n in notes]
        cells = [g for n in (3, 4, 5) for g in HH.ngrams(tr, n)]
        conv = float(np.mean([math.log2(max(self.df[g], 0.5) / self.NS) for g in cells])) if cells else None
        ic, _ = SH.score(self.MM, mel_tokens(ps, TONIC))
        up = next((n + 1 for n in range(2, 13) if len(tr) >= n and tuple(tr[:n]) not in self.present[n]), None)
        return dict(n=len(ps), recurrence=HH.recurrence(tr), convention=conv, i_entropy=HH.entropy(tp), ic_mean=float(np.mean(ic)), mean_pitch=float(np.mean(ps)), up_rhythm=up)
    def pct(self, kind, f, k):
        R = [x for x in self.ref[kind] if abs(x["n"] - f["n"]) <= 0.25 * f["n"] and x[k] is not None]
        v = np.array([x[k] for x in R], float); return round(float(((v < f[k]).mean() + 0.5 * (v == f[k]).mean()) * 100), 1)
def section_notes(notes, sec):
    """engine notes (dicts with on, dur, p, sec) -> (on_beats, off_beats, midi) for one section."""
    return [(n["on"] / BEAT, (n["on"] + n["dur"]) / BEAT, n["p"]) for n in sorted(notes, key=lambda n: n["on"]) if n["sec"] == sec]
def gates(R, notes, title_lines=()):
    c = section_notes(notes, "Chorus 1"); v = section_notes(notes, "Verse 1")
    fc, fv = R.feats(c), R.feats(v)
    pc = {k: R.pct("chorus", fc, k) for k in ("recurrence", "convention", "i_entropy", "ic_mean")}; pv = {k: R.pct("verse", fv, k) for k in ("recurrence",)}
    durs = sorted(n["dur"] for n in notes); med = float(np.median(durs)); longs = [n for n in notes if n["dur"] >= 1.5 * med]
    ls = sum(1 for n in longs if n["stress"]) / max(1, len(longs))
    tit = [n for n in notes if n["line"] in title_lines and n["stress"]]
    r = dict(R1_chorus_minus_verse=round(fc["mean_pitch"] - fv["mean_pitch"], 2), R2_recurrence_pct=pc["recurrence"], R2_verse_recurrence_pct=pv["recurrence"],
             R3_typical_pct=pc["convention"], R4_variety_pct=pc["i_entropy"], R4_surprise_pct=pc["ic_mean"], R5_long_on_stress=round(ls, 3),
             R6_title_on_beat=round(sum(1 for n in tit if n["on"] % BEAT == 0) / max(1, len(tit)), 3), R6_title_held=round(float(np.median([n["dur"] for n in tit])) / med, 2) if tit else None,
             R7_uniqueness_point=fc["up_rhythm"], chorus_notes=fc["n"])
    fails = []
    if r["R1_chorus_minus_verse"] <= 0: fails.append("R1")
    if not (r["R2_recurrence_pct"] >= 50 and r["R2_recurrence_pct"] > r["R2_verse_recurrence_pct"]): fails.append("R2")
    if r["R3_typical_pct"] < 60: fails.append("R3")
    if r["R4_variety_pct"] > 50 or r["R4_surprise_pct"] > 50: fails.append("R4")
    if r["R5_long_on_stress"] < 0.75: fails.append("R5")
    return r, fails
