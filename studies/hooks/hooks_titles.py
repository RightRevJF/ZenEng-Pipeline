"""Where the title goes (lines are read from punctuation, rests of 3/4 beat or more and section changes): CoCoPops Billboard (214 hits 1958-1991, lead melody with sung syllables, section labels, timestamps).
For every song the title is read from the file name and found in the sung words (apostrophes and punctuation dropped). Per song:
how many times the title is sung, in which sections, where in its line (first or last words) and in its section (first or last
line), when it is first heard (seconds and share of the song), whether it starts on beat 1, how long its notes are held against
the song's median note, and whether it carries the chorus's highest note. Only derived counts are written; no lyrics are kept."""
import glob, json, re, os, statistics as st
import numpy as np
SRC = "/home/claude/data/cocopops/CoCoPops-Billboard/Humdrum/CompleteTranscriptions/"
OUT = "/home/claude/zeneng-pipeline/studies/hooks/"
KERN = re.compile(r"^([\[\(]*)(\d+)(\.*)([a-gA-Gr]+)?([#\-n]*)")
def pitch(tok):
    m = re.search(r"([a-gA-G]+)([#\-]*)", tok)
    if not m: return None
    letters, acc = m.group(1), m.group(2)
    base = {"c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11}[letters[0].lower()]
    octave = 4 + (len(letters) - 1) if letters[0].islower() else 3 - (len(letters) - 1)
    return 12 * (octave + 1) + base + acc.count("#") - acc.count("-")
def dur(tok):
    m = re.search(r"(\d+)(\.*)", tok)
    if not m: return 0.0
    n = int(m.group(1)); d = 4.0 / n if n else 8.0
    return d * (1.5 if len(m.group(2)) == 1 else 1.75 if len(m.group(2)) == 2 else 1.0)
def split_title(fn):
    parts = os.path.basename(fn)[:-4].split("_"); t = parts[1] if len(parts) >= 3 else parts[-1]
    t = re.sub(r"([a-z])([A-Z])", r"\1 \2", t); t = re.sub(r"([A-Za-z])(\d)", r"\1 \2", t)
    return [w.lower() for w in t.split()]
def norm(w): return re.sub(r"[^a-z0-9]", "", w.lower())
def parse(fn):
    lines = open(fn, encoding="utf-8", errors="ignore").read().split("\n")
    head = None; label = None; beat = 0.0; bar_start = 0.0; words = []; cur = None; newline_pending = True; ts = []
    for L in lines:
        if not L or L.startswith("!"): continue
        f = L.split("\t")
        if L.startswith("**"): head = f; ki = f.index("**kern"); si = f.index("**silbe"); pi = f.index("**phrase") if "**phrase" in f else None; ti = f.index("**timestamp") if "**timestamp" in f else None; continue
        if head is None: continue
        if L.startswith("*"):
            for x in f:
                if x.startswith("*>Label>"): label = x.replace("*>Label>", "").lstrip(">"); newline_pending = True
            continue
        if L.startswith("="): bar_start = beat; continue
        if ti is not None and f[ti] not in (".", ""):
            try: ts.append((beat, float(f[ti])))
            except ValueError: pass
        if pi is not None and f[pi] == "newline": newline_pending = True
        k = f[ki]
        if k == ".": continue
        k0 = k.split(" ")[0]; d = dur(k0); p = None if "r" in re.sub(r"[^a-gA-Gr]", "", k0) else pitch(k0)
        s = f[si]
        if p is not None and s not in (".", "_") and "]" not in k0 and "_" not in k0:
            starts_word = not s.startswith("-")
            if starts_word or cur is None:
                if cur: words.append(cur)
                cur = dict(text=s.strip("-"), raw=s, on=beat, pos=beat - bar_start, notes=[(p, d)], sec=label, newline=newline_pending)
                newline_pending = False
            else:
                cur["text"] += s.strip("-"); cur["raw"] = s; cur["notes"].append((p, d))
        elif p is not None and cur is not None:
            cur["notes"].append((p, d))  # melisma or tie continues the current word
        beat += d
    if cur: words.append(cur)
    return words, ts, beat
def interp(ts, b):
    if not ts: return None
    xs, ys = zip(*ts); return float(np.interp(b, xs, ys))
def main():
    rows = []
    for fn in sorted(glob.glob(SRC + "*.hum")):
        try: words, ts, end = parse(fn)
        except Exception as e: print("skip", fn, e); continue
        if len(words) < 20: continue
        title = [norm(w) for w in split_title(fn)]; title = [w for w in title if w]
        W = [norm(w["text"]) for w in words]
        # lines: index of line per word
        # lyric lines: a new line after terminal punctuation, after a gap of 3/4 beat or more, or at a new section
        line = []; li = 0
        for j, w in enumerate(words):
            if j > 0:
                pv = words[j - 1]; gap = w["on"] - (pv["on"] + sum(d for _, d in pv["notes"]))
                if pv["raw"].rstrip("-")[-1:] in ".,?!;:" or gap >= 0.75 or w["sec"] != pv["sec"]: li += 1
            line.append(li)
        hits = []
        n = len(title)
        for i in range(len(W) - n + 1):
            if W[i:i + n] == title: hits.append(i)
        if not hits and n >= 3:  # allow the first two-thirds of a long title
            m = max(2, (2 * n) // 3)
            for i in range(len(W) - m + 1):
                if W[i:i + m] == title[:m]: hits.append(i)
            n = m if hits else n
        allnotes = [d for w in words for _, d in w["notes"]]; med = st.median(allnotes)
        song_len = interp(ts, end) or None
        sec_of = [w["sec"] or "None" for w in words]
        chorus_max = {}
        for w in words:
            if (w["sec"] or "").startswith(("Chorus", "Refrain")):
                chorus_max.setdefault(w["sec"], 0); chorus_max[w["sec"]] = max(chorus_max[w["sec"]], max(p for p, _ in w["notes"]))
        occ = []
        for i in hits:
            ws = words[i:i + n]; L = line[i]
            line_idx = [j for j in range(len(words)) if line[j] == L]
            sec_lines = sorted({line[j] for j in range(len(words)) if sec_of[j] == sec_of[i] and abs(j - i) < 200})
            # section run: contiguous words with the same label around i
            a = i
            while a > 0 and sec_of[a - 1] == sec_of[i]: a -= 1
            b = i
            while b < len(words) - 1 and sec_of[b + 1] == sec_of[i]: b += 1
            run_lines = sorted({line[j] for j in range(a, b + 1)})
            tnotes = [d for w in ws for _, d in w["notes"]]; tp = max(p for w in ws for p, _ in w["notes"])
            sec_max = max(p for j in range(a, b + 1) for p, _ in words[j]["notes"])
            occ.append(dict(section=(sec_of[i].rstrip("0123456789").strip() or "None"), at_line_start=int(i == line_idx[0]), at_line_end=int(i + n - 1 == line_idx[-1]),
                            first_line=int(L == run_lines[0]), last_line=int(L == run_lines[-1]), n_lines_in_section=len(run_lines),
                            beat1=int(abs(words[i]["pos"]) < 1e-6), on_beat=int(abs(words[i]["pos"] - round(words[i]["pos"])) < 1e-6),
                            held_ratio=float(np.mean(tnotes) / med), longest_ratio=float(max(tnotes) / med), carries_section_top=int(tp >= sec_max),
                            t=interp(ts, words[i]["on"]), beat=words[i]["on"]))
        # chorus by chorus: each contiguous run of words labelled Chorus or Refrain
        runs = []; j = 0
        while j < len(words):
            if (sec_of[j] or "").startswith(("Chorus", "Refrain")):
                a = j
                while j + 1 < len(words) and sec_of[j + 1] == sec_of[a]: j += 1
                runs.append((a, j))
            j += 1
        chor = []
        for a, b in runs:
            ls = sorted({line[x] for x in range(a, b + 1)}); inrun = [i for i in hits if a <= i <= b]
            tl = {line[i] for i in inrun}
            chor.append(dict(n_lines=len(ls), n_title=len(inrun), first_line=int(ls[0] in tl), last_line=int(ls[-1] in tl), lines_with_title=len(tl),
                             first_word=int(bool(inrun) and inrun[0] == a)))
        first = occ[0] if occ else None
        rows.append(dict(song=os.path.basename(fn)[:-4], title_words=len(title), matched=len(occ) > 0, matched_words=n, n_sung=len(occ),
                         first_time=first["t"] if first else None, first_share=(first["t"] / song_len if first and song_len and first["t"] is not None else None),
                         song_seconds=song_len, occ=occ, choruses=chor, has_chorus=any(s.startswith(("Chorus", "Refrain")) for s in sec_of)))
    json.dump(rows, open(OUT + "hooks_titles_rows.json", "w"))
    M = [r for r in rows if r["matched"]]; C = [o for r in M for o in r["occ"]]
    def share(xs): return round(100 * float(np.mean(xs)), 1) if xs else None
    chor = [o for o in C if o["section"] in ("Chorus", "Refrain")]
    res = dict(songs=len(rows), title_found=len(M), title_found_pct=share([r["matched"] for r in rows]),
               times_sung=dict(median=float(np.median([r["n_sung"] for r in M])), p25=float(np.percentile([r["n_sung"] for r in M], 25)), p75=float(np.percentile([r["n_sung"] for r in M], 75))),
               by_section={s: share([o["section"] == s for o in C]) for s in sorted({o["section"] for o in C})},
               songs_with_title_in_chorus=share([any(o["section"] in ("Chorus", "Refrain") for o in r["occ"]) for r in M if r["has_chorus"]]),
               songs_with_chorus=sum(r["has_chorus"] for r in M),
               chorus=dict(n=len(chor), first_line=share([o["first_line"] for o in chor]), last_line=share([o["last_line"] for o in chor]),
                           line_start=share([o["at_line_start"] for o in chor]), line_end=share([o["at_line_end"] for o in chor]),
                           beat1=share([o["beat1"] for o in chor]), on_beat=share([o["on_beat"] for o in chor]),
                           held_ratio_median=float(np.median([o["held_ratio"] for o in chor])), longest_ratio_median=float(np.median([o["longest_ratio"] for o in chor])),
                           carries_top=share([o["carries_section_top"] for o in chor])),
               first_time=dict(median=float(np.median([r["first_time"] for r in M if r["first_time"] is not None])), p25=float(np.percentile([r["first_time"] for r in M if r["first_time"] is not None], 25)), p75=float(np.percentile([r["first_time"] for r in M if r["first_time"] is not None], 75))),
               first_share=dict(median=float(np.median([r["first_share"] for r in M if r["first_share"]])), p25=float(np.percentile([r["first_share"] for r in M if r["first_share"]], 25)), p75=float(np.percentile([r["first_share"] for r in M if r["first_share"]], 75))),
               title_in_first_line_of_song=share([r["occ"][0]["beat"] <= min(o["beat"] for o in r["occ"]) and r["occ"][0]["section"] not in ("Chorus", "Refrain") for r in M]))
    # per chorus section: times the title is sung inside one chorus
    per = []
    for r in M:
        cs = {}
        for o in r["occ"]:
            if o["section"] in ("Chorus", "Refrain"): cs.setdefault(round(o["beat"] // 64), 0)
        # count by chorus runs: group occurrences within 32 beats of each other
        b = sorted(o["beat"] for o in r["occ"] if o["section"] in ("Chorus", "Refrain")); g = []
        for x in b:
            if g and x - g[-1][-1] <= 24: g[-1].append(x)
            else: g.append([x])
        per += [len(x) for x in g]
    CH = [c for r in M for c in r["choruses"] if c["n_lines"] >= 2]
    res["choruses"] = dict(n=len(CH), songs=len({r["song"] for r in M if r["choruses"]}), with_title=share([c["n_title"] > 0 for c in CH]),
        title_times_median=float(np.median([c["n_title"] for c in CH])), title_times_p75=float(np.percentile([c["n_title"] for c in CH], 75)),
        lines_median=float(np.median([c["n_lines"] for c in CH])), share_of_lines_with_title=round(100 * float(np.median([c["lines_with_title"] / c["n_lines"] for c in CH])), 1),
        first_line=share([c["first_line"] for c in CH]), last_line=share([c["last_line"] for c in CH]), first_and_last=share([c["first_line"] and c["last_line"] for c in CH]),
        first_or_last=share([c["first_line"] or c["last_line"] for c in CH]), first_word=share([c["first_word"] for c in CH]),
        chance_first_line=round(100 * float(np.mean([c["lines_with_title"] / c["n_lines"] for c in CH])), 1))
    res["per_chorus_old"] = dict(n=len(per), median=float(np.median(per)) if per else None, share_once=share([x == 1 for x in per]), share_2=share([x == 2 for x in per]), share_3plus=share([x >= 3 for x in per]))
    json.dump(res, open(OUT + "hooks_titles_results.json", "w"), indent=1); print(json.dumps(res, indent=1))
if __name__ == "__main__": main()
