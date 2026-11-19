import sys, os, json, gzip, pickle, hashlib, re, collections, warnings, numpy as np, pandas as pd; warnings.filterwarnings("ignore")
sys.path[:0] = ["/home/claude/zeneng/corpus/v26", "/home/claude/zeneng/corpus/v25"]
os.chdir("/home/claude/zeneng/corpus/v26"); import build as Bd; os.chdir("/home/claude/arena")
from scipy.stats import rankdata
H = lambda a: int(hashlib.md5(str(a).encode()).hexdigest(), 16) % 2
G = pickle.load(open("/home/claude/zeneng/corpus/v23/graded.pkl", "rb")); byid = {(s["src"], s["id"]): s for s in G}
s1, s2, s3 = pickle.load(open("/home/claude/zeneng/corpus/v31/s_sets.pkl", "rb")); L = {}
for ln in open("/home/claude/corpus/parsed_lakh.jsonl"):
    r = json.loads(ln); L[r["id"]] = r
HT = json.load(gzip.open("/home/claude/corpus_new/sheetsage-data/hooktheory/Hooktheory.json.gz")); htby = collections.defaultdict(list)
for k, v in HT.items():
    if "MELODY" in v["tags"] and "HARMONY" in v["tags"]: htby[f'{v["hooktheory"]["artist"]}/{v["hooktheory"]["song"]}'].append(v["annotations"])
songs = []
def add(r, st, clips, extra=None):
    d = dict(set=st, title=r.title, artist=r.artist, year=int(r.year), peak=float(r.peak) if r.peak == r.peak and r.peak is not None else None, G=float(r.G), love=float(r.love), cover_rank=float(r.cover_rank), clips=[[(float(t), int(p)) for t, p in c] for c in clips]); d.update(extra or {}); songs.append(d)
for r in s1.itertuples(): add(r, 1, [c for c in byid[(r.src, r.id)]["clips"] if len(c) >= 8], dict(source=r.src, hooktheory=htby.get(r.id) if r.src == "HT" else None))
for r in s2.itertuples():
    t, p, tr, lines = Bd.read(Bd.D + "syllable_level_npy_39/" + r.file); a = np.load(Bd.D + "syllable_level_npy_39/" + r.file, allow_pickle=True, encoding="latin1"); add(r, 2, [list(zip(t, p))], dict(source="lyrics-melody MIDI", syllables=[str(x) for x in a[0][2]], durations=[float(n[1]) for n in a[0][1]]))
for r in s3.itertuples():
    ns = sorted({(float(n["off"]), int(n["p"])) for s in L[r.id]["melody"]["sections"] for n in s["notes"] if "off" in n}); add(r, 3, [ns], dict(source="Lakh MIDI (voice track guessed)", tempo=L[r.id].get("tempo"), midi_path="/home/claude/corpus/lakh-midi/clean_midi/" + r.id))
for st in (1, 2, 3):
    v = [s for s in songs if s["set"] == st]; rk = rankdata([s["G"] for s in v]) / len(v)
    for s, x in zip(v, rk): s["G_rank"] = float(x)
op = [s for s in songs if H(s["artist"]) == 0]; lk = [s for s in songs if H(s["artist"]) == 1]; pickle.dump(op, open("tunes_open.pkl", "wb")); pickle.dump(lk, open("/home/claude/arena_locked/tunes_locked.pkl", "wb"))
# sound stores
M = pd.read_pickle("/home/claude/zeneng/corpus/v36/sound2_meta.pkl").assign(store="mcgill_whole_recordings"); D2 = pd.read_pickle("/home/claude/zeneng/corpus/v37/second.pkl").assign(store="msd_previews"); S = pd.concat([M, D2], ignore_index=True).drop(columns=["h"], errors="ignore"); S["half"] = [H(a) for a in S.a]
S[S.half == 0].to_pickle("sound_open.pkl"); S[S.half == 1].to_pickle("/home/claude/arena_locked/sound_locked.pkl")
# every Hot 100 song with Spotify's readings and the yardstick (titles, artists, no notes)
exec(open("/home/claude/zeneng/corpus/v34/sound.py").read().split("def part")[0]); d["half"] = [H(a) for a in d.a]; keep = ["title", "performer", "t", "a", "year", "peak", "weeks", "spotify_genre", "love", "cover_rank", "G", "half"] + F
keep = [c for c in keep if c in d.columns]; d[d.half == 0][keep].to_pickle("hot100_open.pkl"); d[d.half == 1][keep].to_pickle("/home/claude/arena_locked/hot100_locked.pkl")
print("tunes open/locked", len(op), len(lk), "| sound", int((S.half == 0).sum()), int((S.half == 1).sum()), "| hot100", int((d.half == 0).sum()), int((d.half == 1).sum()))
