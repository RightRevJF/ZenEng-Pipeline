"""Song 61 (This Side of the Door): the mouth test, every line (Luthier v7: Principle 4, 'the mouth test is non-negotiable'; the lyric skeleton,
'mouth test every line'; the hook row, 4-9 syllables at singing speed). Its measured parts, as the spec gives them:
  weak line endings (Window 32, Module 28 filter; the song-27 exemptions);
  density and friction at singing speed (Window 36, Table M: 2.481 syllables a second, p95 4.762, ceiling 6.4; friction p95 9.43);
  word-boundary consonant clusters (Window 39, 10.7: 4 or more reported, 5 or more named a tongue-twister);
  the held note's vowel (10.7: held notes want open vowels; close and reduced vowels flagged);
  rare words (lemma Zipf under 2.75).
The tempo and spans are provisional (q = 80, a line sung across six beats of its two bars) until the melody is drawn; the density
reading is then repeated on the pick's own onsets."""
import re, sys
sys.path[:0] = ["/home/claude/carol"]
from lyricsearch import words, phones, syllables, zipf, FUNCTION, WEAK_END, OVERRIDE, rhyme_kind
OVERRIDE.setdefault("yellowed", ["Y EH1 L OW0 D"])   # not in CMUdict
QBPM, BEATS = 80, 6.0    # provisional: an acoustic ballad, a line sung across six beats of its two bars
PLO = set("P B T D K G".split()); FRI = set("F V TH DH S Z SH ZH HH CH JH".split()); SON = set("M N NG L R W Y".split())
CLOSE = {"IY", "IH", "UW", "UH", "ER"}; REDUCED = {"AH0", "IH0", "ER0", "UH0"}
EXEMPT_END = {"up", "out", "down", "on", "in", "off", "here", "there", "now", "again", "home"}   # the song-27 port
AUXEND = {"do", "does", "did", "is", "was", "are", "were", "has", "have", "had", "can", "could", "will", "would"}   # v52 (Table K)
DEM = {"this", "that", "these", "those"}   # F-b
def cons(w):
    return [re.sub(r"\d", "", p) for p in phones(w).split() if not p[-1].isdigit()]
def edges(w):
    ps = phones(w).split(); i = next(k for k, p in enumerate(ps) if p[-1].isdigit()); j = max(k for k, p in enumerate(ps) if p[-1].isdigit())
    return ps[:i], ps[j + 1:]
def load(ws):
    c = [p for w in ws for p in cons(w)]; n = sum(len([p for p in phones(w).split() if p[-1].isdigit()]) for w in ws)
    return sum(1.0 if p in PLO else 0.7 if p in FRI else 0.4 for p in c) / max(1, n)
def read(line, prev=()):
    ws = words(line); syl = syllables(line); n = len(syl)
    sps = n / (BEATS * 60 / QBPM); fr = sps * (1 + load(ws))
    clusters = []
    for a, b in zip(ws, ws[1:]):
        k = len(edges(a)[1]) + len(edges(b)[0])
        if k >= 4: clusters.append((f"{a} {b}", k))
    last = ws[-1]; flags = []
    rhymed = len(syllables(last)) == 1 and any(rhyme_kind(last, words(q)[-1]) >= 0.8 for q in prev[-2:])   # a stressed monosyllable in a rhyme slot
    if last in WEAK_END and last not in EXEMPT_END | AUXEND | DEM and not rhymed: flags.append(f"weak ending '{last}'")
    hv = syl[-1][1]; v = re.sub(r"\d", "", hv)
    if hv in REDUCED: flags.append(f"held vowel reduced ({hv} in '{syl[-1][0]}')")
    elif v in CLOSE: flags.append(f"held vowel close ({v} in '{syl[-1][0]}')")
    rare = [w for w in ws if w not in FUNCTION and zipf(w) < 2.75]
    if rare: flags.append("rare: " + ", ".join(rare))
    if sps > 4.762: flags.append(f"dense {sps:.2f}/s (p95 4.76)")
    if fr > 9.43: flags.append(f"friction {fr:.2f} (p95 9.43)")
    for c, k in clusters: flags.append(f"cluster {k} at '{c}'" + (" (tongue-twister)" if k >= 5 else ""))
    return n, sps, fr, flags
if __name__ == "__main__":
    sec = None; rows = []; prev = []
    for raw in open(sys.argv[1] if len(sys.argv) > 1 else "lyric_locked.md"):
        l = raw.strip()
        if l.startswith("## "): sec = l[3:]; prev = []; continue
        if not l or l.startswith("#"): continue
        if re.fullmatch(r"(Verse|Chorus|Bridge|Outro|Tag|Pre-chorus|Intro|Last Chorus)( \d+)?( \(.*\))?", l): sec = l; prev = []; continue
        if l.startswith("Words and"): continue
        n, sps, fr, fl = read(l, tuple(prev)); rows.append((sec, l, n, sps, fr, fl)); prev.append(l)
    seen = set()
    for sec, l, n, sps, fr, fl in rows:
        if (sec, l) in seen: continue
        seen.add((sec, l)); print(f"{sec:8} {n:2d} syl {sps:4.2f}/s fr {fr:5.2f} | {l}" + ("   <- " + "; ".join(fl) if fl else ""))
    import statistics as S
    print("lines", len(seen), "| syllables median", S.median(r[2] for r in rows), "| flagged", sum(1 for r in {(a, b): f for a, b, *_, f in rows}.values() if r))
