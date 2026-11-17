"""The hook study on the Hooktheory clips (CC BY-NC-SA, via Sheet Sage): what a chorus does that its own verse does not, on the
features that predicted how fast listeners recognised song sections in the Hooked! game (Van Balen et al. 2015; Burgoyne et al.
2013) and how they identify melodies (Schulkind et al. 2003; Dalla Bella et al. 2003).

Per clip (a user's transcription of one labelled section, joined to its section name in Hooktheory_Raw):
  density      notes per beat
  range        highest minus lowest note, semitones; mean pitch (MIDI)
  i_entropy    Shannon entropy of the interval distribution, bits (lower = more repetitive; FANTASTIC i.entropy)
  recurrence   share of the clip's 3- to 5-note cells (interval + rhythm ratio) heard more than once in the clip
               (Van Balen's song-based recurrence; FANTASTIC 1 - productivity)
  convention   mean log2 share of other songs that contain each of the clip's cells (FANTASTIC mtcf.mean.log.DF, corpus-based,
               the clip's own song left out)
  ic_mean      mean information content of the melody under a variable-order model trained on other songs (5 folds by song)
  top_cell     the clip's most frequent 4-note cell: times it returns, where it first starts (share of the clip), share of notes
               it covers
  up_rhythm    uniqueness point: notes from the first sung note until the opening (intervals with rhythm) occurs in no other song
  up_pitch     the same with intervals only
  opens_down   whether the first note falls on a downbeat
Writes hooks_clips.json.gz (one row per clip, derived numbers only) and hooks_hooktheory_results.json."""
import gzip, json, math, sys, collections
import numpy as np
sys.path.insert(0, "/home/claude/shape")
import surprise_hooktheory as SH
H = "/home/claude/chrisdonahue/sheetsage-data/hooktheory/"
OUT = "/home/claude/zeneng-pipeline/studies/hooks/"
def norm_section(s):
    s = (s or "").lower().strip()
    for k in ("pre-chorus and chorus", "intro and verse", "verse and pre-chorus", "chorus lead-out"):
        if s == k: return k
    for k in ("pre-chorus", "chorus", "verse", "intro", "bridge", "outro", "instrumental", "solo"):
        if s.startswith(k): return k
    return "other"
def rclass(prev, cur):
    if prev <= 0 or cur <= 0: return 1
    r = math.log2(cur / prev)
    return 0 if r < -0.4 else 2 if r > 0.4 else 1
def tokens(notes):
    """notes: list of (onset_beats, offset_beats, midi). Token k (k >= 1) = (interval from note k-1 clipped to +-12, IOI ratio class)."""
    ioi = [notes[i + 1][0] - notes[i][0] for i in range(len(notes) - 1)] + [notes[-1][1] - notes[-1][0]]
    t_r, t_p = [], []
    for k in range(1, len(notes)):
        iv = max(-12, min(12, notes[k][2] - notes[k - 1][2])); rc = rclass(ioi[k - 1], ioi[k])
        t_r.append((iv + 12) * 3 + rc); t_p.append(iv + 12)
    return t_r, t_p
def ngrams(t, n): return [tuple(t[i:i + n]) for i in range(len(t) - n + 1)]
def entropy(xs):
    c = collections.Counter(xs); n = sum(c.values()); return -sum(v / n * math.log2(v / n) for v in c.values()) if n else 0.0
def recurrence(t):
    vals = []
    for n in (3, 4, 5):
        g = ngrams(t, n)
        if not g: continue
        c = collections.Counter(g); vals.append(sum(v for v in c.values() if v > 1) / len(g))
    return float(np.mean(vals)) if vals else 0.0
def top_cell(t, nnotes):
    g = ngrams(t, 3)  # 3 tokens = 4 notes
    if not g: return 0, None, 0.0
    c = collections.Counter(g); cell, cnt = c.most_common(1)[0]
    # non-overlapping occurrences
    occ = []; i = 0
    while i < len(g):
        if g[i] == cell: occ.append(i); i += 3
        else: i += 1
    cover = len(occ) * 4 / nnotes
    return len(occ), occ[0] / max(1, len(g)), min(1.0, cover)
def load():
    R = json.load(gzip.open(H + "Hooktheory_Raw.json.gz")); D = json.load(gzip.open(H + "Hooktheory.json.gz"))
    sec = {r["hash"]: (r.get("json_api") or {}).get("section") for r in R.values()}
    clips = []
    for k, d in D.items():
        a = d["annotations"]; mel = sorted(a.get("melody") or [], key=lambda n: n["onset"])
        if len(mel) < 16: continue
        meters = a.get("meters") or [{"beats_per_bar": 4}]
        bpb = meters[0].get("beats_per_bar", 4)
        notes = [(n["onset"], n["offset"], 12 * n["octave"] + n["pitch_class"] + 48) for n in mel]
        song = d["hooktheory"]["artist"] + "/" + d["hooktheory"]["song"]
        clips.append(dict(k=k, song=song, section=norm_section(sec.get(d["hooktheory"]["id"])), raw=d, notes=notes, bpb=bpb, nb=a.get("num_beats") or (notes[-1][1] - notes[0][0])))
    return clips
def main():
    clips = load(); print(len(clips), "clips with 16+ notes", flush=True)
    songs = sorted({c["song"] for c in clips}); sid = {s: i for i, s in enumerate(songs)}; NS = len(songs)
    for c in clips: c["tr"], c["tp"] = tokens(c["notes"]); c["sid"] = sid[c["song"]]
    # document frequency of cells by song (3..5 tokens)
    df = collections.Counter()
    for s in range(NS): pass
    by_song = collections.defaultdict(set)
    for c in clips:
        for n in (3, 4, 5): by_song[c["sid"]].update(ngrams(c["tr"], n))
    for s, cells in by_song.items(): df.update(cells)
    print("cells", len(df), flush=True)
    # uniqueness points: for each n, the set of songs containing each n-gram (stop tracking past 2)
    def up(field, maxn=16):
        res = {c["k"]: None for c in clips}
        pending = {c["k"] for c in clips}
        cmap = {c["k"]: c for c in clips}
        for n in range(2, maxn + 1):
            owner = {}
            for c in clips:
                for g in set(ngrams(c[field], n)):
                    o = owner.get(g)
                    if o is None: owner[g] = c["sid"]
                    elif o != c["sid"]: owner[g] = -1
            done = []
            for k in pending:
                c = cmap[k]
                if len(c[field]) < n: done.append(k); continue
                if owner.get(tuple(c[field][:n])) != -1: res[k] = n + 1; done.append(k)  # n intervals = n+1 notes
            for k in done: pending.discard(k)
            print(field, "n", n, "still shared", len(pending), flush=True)
            if not pending: break
        return res
    UPR = up("tr"); UPP = up("tp")
    # information content, cross-fitted by song
    rng = np.random.default_rng(11); fold = rng.integers(0, 5, NS)
    IC = {}
    toks = {c["k"]: SH.tokens(c["raw"])[0] for c in clips}
    for f in range(5):
        mm = SH.VOM(84).fit([toks[c["k"]] for c in clips if fold[c["sid"]] != f])
        for c in clips:
            if fold[c["sid"]] == f:
                ic, h = SH.score(mm, toks[c["k"]]); IC[c["k"]] = (float(np.mean(ic)), float(np.mean(h)))
        print("IC fold", f, flush=True)
    rows = []
    for c in clips:
        ps = [n[2] for n in c["notes"]]; nb = max(1e-6, c["nb"])
        cells = [g for n in (3, 4, 5) for g in ngrams(c["tr"], n)]
        conv = float(np.mean([math.log2(max(df[g] - 1, 0.5) / NS) for g in cells])) if cells else None
        tc, tpos, tcov = top_cell(c["tr"], len(ps))
        first = c["notes"][0][0]
        rows.append(dict(k=c["k"], song=c["song"], section=c["section"], n=len(ps), beats=round(nb, 2), density=len(ps) / nb, range=max(ps) - min(ps),
                         mean_pitch=float(np.mean(ps)), i_entropy=entropy(c["tp"]), recurrence=recurrence(c["tr"]), convention=conv,
                         ic_mean=IC[c["k"]][0], h_mean=IC[c["k"]][1], top_cell_n=tc, top_cell_pos=tpos, top_cell_cover=tcov,
                         up_rhythm=UPR[c["k"]], up_pitch=UPP[c["k"]], opens_down=int(abs((first % c["bpb"])) < 1e-6)))
    json.dump(rows, gzip.open(OUT + "hooks_clips.json.gz", "wt"))
    print("rows", len(rows))
if __name__ == "__main__": main()
