"""Song 63 (We Saved You a Plate): the mouth test, every line, as song 61's (mouth_p71.read: weak endings, density and friction at singing
speed, word-boundary clusters, the held vowel, rare words), plus the hook row (4-9 syllables). Provisional tempo for a chamber-pop ballad:
q = 120, a line sung across six beats of its two bars, until the melody is drawn."""
import sys, re
sys.path[:0] = ["/home/claude/carol", "/home/claude/zeneng-pipeline/songs/p71"]
import mouth_p71 as M
M.QBPM, M.BEATS = 120, 6.0
sec = None; prev = []; seen = set(); rows = []
for raw in open("lyric_locked.md"):
    l = raw.strip()
    if l.startswith("## "): sec = l[3:]; prev = []; continue
    if not l or l.startswith("#") or l.startswith("Words and"): continue
    n, sps, fr, fl = M.read(l, tuple(prev)); prev.append(l)
    if (sec, l) in seen: continue
    seen.add((sec, l)); rows.append((sec, n, fl)); print(f"{sec:12} {n:2d} syl {sps:4.2f}/s fr {fr:5.2f} | {l}" + ("   <- " + "; ".join(fl) if fl else ""))
import statistics as S
print("lines", len(rows), "| syllables median", S.median(r[1] for r in rows), "| range", min(r[1] for r in rows), "-", max(r[1] for r in rows), "| flagged", sum(1 for r in rows if r[2]))
from lyricsearch import syllables
print("hook row: 'We saved you a plate'", len(syllables("We saved you a plate")), "syllables (4-9 wanted)")   # was measuring song 62's title by mistake (fixed 25 Nov)
