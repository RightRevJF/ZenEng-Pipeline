"""Lyric craft measures for Luthier v8. Reads lyrics, keeps only derived numbers (no lyric text is written).

Sources (all as sung, with repeats):
  RS    CoCoPops Rolling Stone files that carry syllables (80 songs from Rolling Stone's 500 Greatest Songs, chosen by artists and critics)
  BB    CoCoPops Billboard complete transcriptions (a random sample of Hot 100 songs, 1958-1991), minus songs also in RS
  OURS  songs 52, 54, 55, 56 from their records (sung order); song 53 from its locked lyric, stanzas as written
Lines: one rule for every source (segment()): a gap of half a beat, a word held two beats, or a section change.

Per lyric: words, lines, words per line; MATTR-50 (lexical variety); repeated-line share; mean Zipf of content words and the share
under Zipf 3 (wordfreq); you, I, we and he/she/they per word; mean concreteness of content words (Brysbaert et al. 2014); past-tense
share of verbs, time words, place words, proper nouns and numbers per 100 words (the features Bamman et al. 2025 found behind
narrativity), combined into a narrativity index (mean of z-scores); VADER valence per line, the ending (last fifth minus the rest) and a
sad-ending flag (Rosch and Rauch 2025); absolutes per line (always, never, forever ...); rhyme density (a line
end rhyming with one of the three lines before it, CMU dictionary); title count."""
import glob, json, os, re, sys, math, pickle, collections
import numpy as np
from wordfreq import zipf_frequency
import pronouncing, spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sys.path.insert(0, "/home/claude/zeneng-pipeline/studies/hooks")
import hooks_titles as HT
NLP = spacy.load("en_core_web_sm", disable=["ner", "parser"])
VADER = SentimentIntensityAnalyzer()
CONC = {}
for i, l in enumerate(open("/home/claude/data/norms/concreteness.txt")):
    if i == 0: continue
    f = l.rstrip("\n").split("\t")
    if f[1] == "0": CONC[f[0].lower()] = float(f[2])
STOP = set("a an the and or but so if of to in on at by for with from up down out over into onto off as is are was were be been being am do does did have has had i me my mine you your yours we us our he him his she her they them their it its this that these those what who whom which there here not no yes oh ooh ah yeah la na hey baby just can could will would shall should may might must".split())
TIME = set("tonight today yesterday tomorrow morning evening night nights day days week weeks year years summer winter spring fall autumn sunday monday tuesday wednesday thursday friday saturday hour hours minute minutes midnight noon dawn sunrise sunset ago later before after then when while until since o'clock clock time times".split())
PLACE = set("town city street streets road roads highway downtown house home room kitchen bedroom door window porch yard church school bar club car truck train bus station hall hotel motel river lake ocean sea beach shore field farm hill mountain valley country state corner store park bridge floor wall table bed stairs garden alley avenue boulevard parking lot".split())
ABS = set("always never forever everything nothing everyone nobody everybody all none every".split())
def norm(w): return re.sub(r"[^a-z0-9']", "", w.lower().replace("’", "'"))
def mattr(ws, k=50):
    if len(ws) < k: return len(set(ws)) / max(1, len(ws))
    return float(np.mean([len(set(ws[i:i + k])) / k for i in range(0, len(ws) - k + 1)]))
def rhyme_part(w):
    p = pronouncing.phones_for_word(w)
    return pronouncing.rhyming_part(p[0]) if p else None
def features(lines, title=None):
    """lines: list of strings (as sung)."""
    lines = [l for l in (x.strip() for x in lines) if l]
    toks = [[norm(w) for w in l.split() if norm(w)] for l in lines]; toks = [t for t in toks if t]
    words = [w for t in toks for w in t]; n = len(words)
    if n < 40: return None
    content = [w for w in words if w not in STOP and len(w) > 2]
    z = [zipf_frequency(w, "en") for w in content]
    conc = [CONC[w] for w in content if w in CONC]
    text = " ".join(" ".join(t) for t in toks)
    doc = NLP(text)
    verbs = [t for t in doc if t.pos_ in ("VERB", "AUX") and t.tag_.startswith("VB")]
    past = sum(1 for t in verbs if t.tag_ in ("VBD", "VBN")) / max(1, len(verbs))
    propn = sum(1 for t in doc if t.pos_ == "PROPN") / n * 100
    nums = sum(1 for t in doc if t.like_num) / n * 100
    line_keys = [" ".join(t) for t in toks]; cnt = collections.Counter(line_keys)
    vals = [VADER.polarity_scores(" ".join(t))["compound"] for t in toks]
    k = max(1, len(vals) // 5); end = float(np.mean(vals[-k:])); rest = float(np.mean(vals[:-k])) if len(vals) > k else end
    ends = [rhyme_part(t[-1]) for t in toks]; rh = 0; tot = 0
    for i, e in enumerate(ends):
        if i == 0 or e is None: continue
        tot += 1; rh += int(any(ends[j] == e and toks[j][-1] != toks[i][-1] for j in range(max(0, i - 3), i)))
    title_n = None
    if title:
        tw = [norm(w) for w in title.split() if norm(w)]
        title_n = sum(1 for i in range(len(words) - len(tw) + 1) if words[i:i + len(tw)] == tw)
    return dict(words=n, lines=len(toks), words_per_line=n / len(toks), mattr=mattr(words), repeated_lines=sum(1 for l in line_keys if cnt[l] > 1) / len(line_keys),
                zipf=float(np.mean(z)) if z else None, rare=float(np.mean([v < 3 for v in z])) if z else None,
                you=sum(w in ("you", "your", "yours", "you're", "you'll", "you've", "you'd", "ya") for w in words) / n,
                i=sum(w in ("i", "me", "my", "mine", "i'm", "i'll", "i've", "i'd", "myself") for w in words) / n,
                we=sum(w in ("we", "us", "our", "we're", "we'll", "ours") for w in words) / n,
                third=sum(w in ("he", "she", "him", "her", "his", "they", "them", "their", "he's", "she's", "they're") for w in words) / n,
                conc=float(np.mean(conc)) if conc else None, past=past, time=sum(w in TIME for w in words) / n * 100, place=sum(w in PLACE for w in words) / n * 100,
                propn=propn, nums=nums, valence=float(np.mean(vals)), valence_sd=float(np.std(vals)), ending=end - rest, sad_end=int(end < rest),
                absolutes=sum(w in ABS for w in words) / len(toks),
                rhyme=rh / max(1, tot), title_n=title_n)
def hum_lines(fn):
    words, ts, end = HT.parse(fn)
    if not words: return []
    return segment([dict(text=w["text"], on=w["on"], end=w["on"] + sum(d for _, d in w["notes"]), sec=w["sec"]) for w in words])
def rs_lines(fn):
    """Rolling Stone files use a time base (*tb32: one row = a 32nd note) and kern tokens without durations; sections as *>Verse."""
    head = None; tb = 32; beat = 0.0; label = None; events = []
    for L in open(fn, errors="ignore").read().split("\n"):
        if not L or L.startswith("!"): continue
        f = L.split("\t")
        if L.startswith("**"): head = f; ki = f.index("**kern"); si = f.index("**silbe"); continue
        if head is None: continue
        if L.startswith("*"):
            m = re.match(r"\*tb(\d+)", f[ki])
            if m: tb = int(m.group(1))
            for x in f:
                if x.startswith("*>") and not x.startswith(("*>Letter", "*>Label>")) and len(x) > 2 and not x[2:3].isdigit(): label = x[2:]
                if x.startswith("*>Label>"): label = x[8:]
            continue
        if L.startswith("="): continue
        k = f[ki]; s_ = f[si] if si < len(f) else "."
        if k != ".":
            is_rest = "r" in k
            events.append(dict(on=beat, rest=is_rest, syl=None if is_rest or s_ in (".", "_") else s_, sec=label))
        beat += 4.0 / tb
    events.append(dict(on=beat, rest=True, syl=None, sec=label))
    words = []
    for i, e in enumerate(events[:-1]):
        nxt = events[i + 1]["on"]
        if e["rest"]:
            continue
        if e["syl"] is None:
            if words: words[-1]["end"] = nxt
            continue
        sy = e["syl"]
        if sy.startswith("-") and words:
            words[-1]["text"] += sy.strip("-"); words[-1]["raw"] = sy; words[-1]["end"] = nxt
        else:
            words.append(dict(text=sy.strip("-"), raw=sy, on=e["on"], end=nxt, sec=e["sec"]))
    return segment(words)
def segment(words):
    """One rule for every source: a new line after a gap of half a beat or more, after a word held two beats or more, or at a section
    change. Punctuation is ignored because the Rolling Stone files carry none."""
    lines = [[]]
    for j, w in enumerate(words):
        if j > 0:
            pv = words[j - 1]
            if w["on"] - pv["end"] >= 0.5 or pv["end"] - pv["on"] >= 2.0 or w["sec"] != pv["sec"]: lines.append([])
        lines[-1].append(w["text"])
    return [" ".join(l) for l in lines if l]
def rs_files():
    out = []
    for fn in sorted(glob.glob("/home/claude/data/cocopops/CoCoPops/RollingStone/Data/*.hum")):
        head = open(fn, errors="ignore").read(3000)
        if "**silbe" not in head: continue
        m = re.search(r"!!!OTL: (.*)", head); y = re.search(r"!!!RRD: (\d{4})", head); r = re.search(r"Rank: (\d+)", head)
        out.append(dict(fn=fn, title=m.group(1).strip() if m else None, year=int(y.group(1)) if y else None, rank=int(r.group(1)) if r else None))
    return out
def main():
    rows = []
    rs = rs_files(); rs_keys = {re.sub(r"[^a-z]", "", os.path.basename(x["fn"]).split("_")[1].lower()) for x in rs}
    for x in rs:
        f = features(rs_lines(x["fn"]), x["title"])
        if f: rows.append(dict(group="RS", song=os.path.basename(x["fn"])[:-4], year=x["year"], rank=x["rank"], **f))
    for fn in sorted(glob.glob(HT.SRC + "*.hum")):
        base = os.path.basename(fn)[:-4]; parts = base.split("_")
        key = re.sub(r"[^a-z]", "", parts[1].lower()) if len(parts) >= 3 else ""
        if key in rs_keys: continue
        title = " ".join(HT.split_title(fn)); year = int(parts[-1]) if parts[-1].isdigit() else None
        f = features(hum_lines(fn), title)
        if f: rows.append(dict(group="BB", song=base, year=year, **f))
    json.dump(rows, open("/home/claude/zeneng-pipeline/studies/lyrics/lyrics_rows.json", "w"))
    print(collections.Counter(r["group"] for r in rows))
if __name__ == "__main__": main()
