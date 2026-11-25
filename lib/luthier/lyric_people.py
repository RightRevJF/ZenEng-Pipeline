"""lyric_people.py: who is in a lyric. Advice only: it prints readings and never stops a song.

Usage: python3 lib/luthier/lyric_people.py songs/pNN/lyricNN.json   (or a lyric .md with "## Section" headings)

From the lyric research of 25 November 2026 (studies/lyric_research; the round-two document): being moved goes with a bond
between people, and our lyrics are fuller of things and emptier of people than the hits. Nothing here has passed a test of
lasting value (within a writer, no word measure separates the acclaimed hit from the writer's others), so these are a
writer's notes beside a draft. The reference figures are medians per 100 words of 4,612 Billboard year-end hits, 1965 to 2015,
245 of them on a Rolling Stone 500 list (the round-two document's table)."""
import sys, re, json, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "studies", "lyric_research"))
from measures import EMOTION, YOU, I_, WE, VOCABLES, words

REF = {"I": (7.6, 8.4), "you": (4.5, 5.4), "I + you": (12.9, 14.2), "named feelings": (1.2, 1.5)}   # acclaimed hits, all hits
WE_SURE = WE - {"were", "well", "wed"}                                                                 # ambiguous once apostrophes go

def sections(path):
    if path.endswith(".json"): return [(n, list(ls)) for n, ls in json.load(open(path))["sections"]]
    out = []
    for l in open(path).read().split("\n"):
        if l.startswith("## "): out.append((l[3:].strip(), []))
        elif l.strip() and out and not l.startswith("#"): out[-1][1].append(l.strip())
    return out

def read(path):
    S = sections(path); lines = [(n, l) for n, ls in S for l in ls]; ws = [w for _, l in lines for w in words(l) if w not in VOCABLES]; n = max(1, len(ws))
    per = lambda s: round(100 * sum(w in s for w in ws) / n, 1)
    feel = [(i, n_, w) for i, (n_, l) in enumerate(lines) for w in words(l) if w in EMOTION]
    r = {"words": len(ws), "I": per(I_), "you": per(YOU), "we": per(WE_SURE), "named feelings": per(EMOTION)}; r["I + you"] = round(r["I"] + r["you"], 1)
    r["sections with no I, you or we"] = [n_ for n_, ls in S if ls and not any(w in I_ | YOU | WE_SURE for l in ls for w in words(l))]
    r["named feelings at"] = [{"section": n_, "word": w, "place": round((i + 1) / len(lines), 2)} for i, n_, w in feel]
    return r

def notes(r):
    out = []
    if r["I + you"] < 7.8: out.append(f"\"I\" plus \"you\" is {r['I + you']} in 100 words; acclaimed hits' median is 12.9 and about one in five is this low. Who is speaking, and to whom?")
    if r["you"] == 0: out.append("Nobody is addressed. A person, God, the dead or a place can be \"you\" somewhere in the song.")
    if r["named feelings"] == 0: out.append("No feeling is named. One plain feeling, stated late against the images, is allowed (acclaimed hits name about one in 100 words).")
    elif r["named feelings"] > 1.5: out.append(f"Feelings are named {r['named feelings']} times in 100 words, over the hits' median of 1.5. Showing is still the rule.")
    early = [x for x in r["named feelings at"] if x["place"] < 0.5]
    if early and r["named feelings"] <= 1.5: out.append("A feeling is named in the first half (" + ", ".join(f"\"{x['word']}\" in {x['section']}" for x in early[:3]) + "). Late is the place for it.")
    return out

if __name__ == "__main__":
    r = read(sys.argv[1])
    print(f"{r['words']} words. Per 100 words (acclaimed hits; all hits):")
    for k in ("I", "you", "I + you", "named feelings"): print(f"  {k}: {r[k]}  ({REF[k][0]}; {REF[k][1]})")
    print(f"  we: {r['we']}")
    if r["sections with no I, you or we"]: print("  sections with no I, you or we: " + ", ".join(r["sections with no I, you or we"]))
    for x in notes(r) or ["Nothing to note."]: print("- " + x)
    print("Advice only. None of these readings has passed a test of lasting value.")
