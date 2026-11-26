"""Song 67 (A Door in the Coral): the mouth test, every line, as song 61's (mouth_p71.read: weak endings, density and friction at singing
speed, word-boundary clusters, the held vowel, rare words), plus the hook row (4-9 syllables). Provisional tempo for a song, tempo not yet chosen:
q = 70 (provisional, hazy indie), a line sung across six beats of its two bars, until the melody is drawn. Then the never-say list, and lib/luthier/lyric_people.py (advice only)."""
import sys, re, os, subprocess
sys.path[:0] = [os.path.dirname(os.path.abspath(__file__)), "/home/claude/carol", "/home/claude/zeneng-pipeline/songs/p71"]   # this song's intake first (song 61 has an intake.py too)
import mouth_p71 as M, intake, lyricsearch
M.QBPM, M.BEATS = 70, 6.0
lyricsearch.OVERRIDE.setdefault("tallboys", ["T AO1 L B OY2 Z"])     # not in the CMU lexicon: TALL-boys
lyricsearch.OVERRIDE.setdefault("paling", ["P EY1 L IH0 NG"])        # not in the CMU lexicon: PAY-ling
SAY = {"I-85": "I eighty five"}                                       # read as sung; the tokenizer drops digits
sec = None; prev = []; seen = set(); rows = []
for raw in open("lyric_locked.md"):
    l = raw.strip()
    if l.startswith("## "): sec = l[3:]; prev = []; continue
    if not l or l.startswith("#") or l.startswith("Words and") or l.startswith("Syllable plan"): continue
    for a, b in SAY.items(): l = l.replace(a, b)
    n, sps, fr, fl = M.read(l, tuple(prev)); prev.append(l)
    if (sec, l) in seen: continue
    seen.add((sec, l)); rows.append((sec, n, fl)); print(f"{sec:13} {n:2d} syl {sps:4.2f}/s fr {fr:5.2f} | {l}" + ("   <- " + "; ".join(fl) if fl else ""))
import statistics as S
print("lines", len(rows), "| syllables median", S.median(r[1] for r in rows), "| range", min(r[1] for r in rows), "-", max(r[1] for r in rows), "| flagged", sum(1 for r in rows if r[2]))
from lyricsearch import syllables
print(f"hook row: '{intake.TITLE}'", len(syllables(intake.TITLE)), "syllables (4-9 wanted)")
t = open("lyric_locked.md").read().lower(); hit = [w for w in intake.NEVER_SAY if re.search(r"\b" + w + r"\b", t)]
print("never-say words found:", hit or "none")
print("--- lyric_people.py (advice only) ---")
print(subprocess.run([sys.executable, "/home/claude/zeneng-pipeline/lib/luthier/lyric_people.py", "lyric_locked.md"], capture_output=True, text=True).stdout)
