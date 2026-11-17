"""Solos and instrumental sections in the McGill Billboard annotations (salami_chords.txt via ChoCo; 739 distinct songs 1958-91).
Instrumental section kinds: solo, instrumental, interlude, theme, instrumental break (not intro or outro). For each: length in seconds
and bars, place in the song (fraction of length at its start, and the section before and after), its material (section letter shared
with a verse, chorus, bridge or other sung section, or its own), and its lead instrument. Per song: whether it has a solo, any
mid-song instrumental section, and the share of the song with no lead voice. Writes solos_results.json."""
import os, re, csv, json, collections, statistics as st
SRC = "/home/claude/data/choco/smashub-choco-f7dd3ee/partitions/billboard/raw"
year = {r["id"].zfill(4): int(r["chart_date"][:4]) for r in csv.DictReader(open(f"{SRC}/billboard-2.0-index.csv")) if r["title"]}
INSTR = re.compile(r"\((guitar|piano|synthesizer|saxophone|organ|strings|trumpet|harmonica|flute|bass|drums|horns|brass|violin|electric piano|clavinet|steel|banjo|fiddle|vocal|voice|keyboard|trombone|clarinet|mandolin)", re.I)
INST_KINDS = ("solo", "instrumental", "interlude", "theme", "main theme", "instrumental break", "secondary theme")
def bars_of(s):
    n = s.count("|")
    if n == 0: return 0
    n -= 1; m = re.search(r"\|\s*x(\d+)", s); return n * int(m.group(1)) if m else n
def per(y): return "1958-64" if y < 1965 else "1965-69" if y < 1970 else "1970-74" if y < 1975 else "1975-79" if y < 1980 else "1980-84" if y < 1985 else "1985-91"
songs = []; secs_all = []; seen = set()
for sid in sorted(os.listdir(f"{SRC}/original")):
    if sid not in year: continue
    L = open(f"{SRC}/original/{sid}/salami_chords.txt").read().splitlines()
    head = {l[1:].split(":", 1)[0].strip(): l.split(":", 1)[1].strip() for l in L if l.startswith("#") and ":" in l}
    key = (head.get("title", "").lower(), head.get("artist", "").lower())
    if key in seen: continue
    seen.add(key)
    ev = []
    for l in L:
        if "\t" in l and not l.startswith("#"):
            t, c = l.split("\t", 1); ev.append((float(t), c))
    music = [(t, c) for t, c in ev if not re.match(r"\s*(silence|end|Z\b)", c)]
    if not music: continue
    start = music[0][0]; tail = [t for t, c in ev if re.match(r"\s*(silence|end)", c) and t > music[-1][0]]
    stop = min(tail) if tail else ev[-1][0]; T = stop - start
    # sections
    secs = []; voice_on = False; voiced = 0.0; prev_t = None
    for i, (t, c) in enumerate(music):
        m = re.match(r"\s*([A-Z]'*)\s*,\s*([a-z][a-z \-]*?)\s*,", c)
        if m: secs.append(dict(t=t, let=m.group(1), lab=m.group(2).strip(), lines=[]))
        elif re.match(r"\s*fadeout", c): secs.append(dict(t=t, let="", lab="fadeout", lines=[]))
        if secs: secs[-1]["lines"].append(c)
        # voice time: lines between "(voice" and "voice)"
        nxt = music[i + 1][0] if i + 1 < len(music) else stop
        if "(voice" in c: voice_on = True
        if voice_on: voiced += nxt - t
        if "voice)" in c: voice_on = False
    for j, s in enumerate(secs): s["end"] = secs[j + 1]["t"] if j + 1 < len(secs) else stop
    sung_lets = collections.defaultdict(set)
    for s in secs:
        if s["lab"] in ("verse", "chorus", "bridge", "pre-chorus", "prechorus", "refrain"): sung_lets[s["let"]].add(s["lab"])
    y = year[sid]; has_solo = False; has_inst = False
    for j, s in enumerate(secs):
        if s["lab"] not in INST_KINDS: continue
        if j == 0 or j == len(secs) - 1: continue           # not intro or outro positions
        has_inst = True; has_solo |= s["lab"] == "solo"
        mat = sung_lets.get(s["let"]); mat = ("chorus" if "chorus" in mat else "verse" if "verse" in mat else "bridge" if "bridge" in mat else sorted(mat)[0]) if mat else "its own"
        inst = None
        for c in s["lines"]:
            mm = INSTR.search(c)
            if mm: inst = mm.group(1).lower(); break
        if inst in ("trumpet", "horns", "brass", "trombone", "saxophone", "clarinet"): inst = "horns or sax"
        if inst in ("electric piano", "clavinet", "keyboard"): inst = "piano or keys"
        if inst == "piano": inst = "piano or keys"
        secs_all.append(dict(year=y, kind=s["lab"], secs=round(s["end"] - s["t"], 1), bars=sum(bars_of(c) for c in s["lines"]), frac=round((s["t"] - start) / T, 3),
                             before=secs[j - 1]["lab"], after=secs[j + 1]["lab"], material=mat, inst=inst or "none marked"))
    songs.append(dict(id=sid, year=y, length=round(T, 1), solo=has_solo, inst=has_inst, voiced_share=round(voiced / T, 3) if T else None))
def q(v):
    v = sorted(v); n = len(v)
    return [round(v[int(.25 * (n - 1))], 2), round(st.median(v), 2), round(v[int(.75 * (n - 1))], 2)] if n else None
out = {"songs": {}, "sections": {}}
for g in ["1958-64", "1965-69", "1970-74", "1975-79", "1980-84", "1985-91", "all"]:
    S = [s for s in songs if g == "all" or per(s["year"]) == g]
    X = [x for x in secs_all if g == "all" or per(x["year"]) == g]
    sol = [x for x in X if x["kind"] == "solo"]
    out["songs"][g] = dict(songs=len(S), with_solo=round(100 * sum(s["solo"] for s in S) / len(S)), with_mid_instrumental=round(100 * sum(s["inst"] for s in S) / len(S)),
                           voiced_share=q([s["voiced_share"] for s in S if s["voiced_share"] is not None]))
    out["sections"][g] = dict(n=len(X), solos=len(sol), solo_secs=q([x["secs"] for x in sol]), solo_bars=q([x["bars"] for x in sol if x["bars"]]),
                              other_secs=q([x["secs"] for x in X if x["kind"] != "solo"]), other_bars=q([x["bars"] for x in X if x["kind"] != "solo" and x["bars"]]),
                              solo_place=q([x["frac"] for x in sol]),
                              solo_material={k: round(100 * v / max(len(sol), 1)) for k, v in collections.Counter(x["material"] for x in sol).most_common(5)},
                              solo_before={k: round(100 * v / max(len(sol), 1)) for k, v in collections.Counter(x["before"] for x in sol).most_common(5)},
                              solo_after={k: round(100 * v / max(len(sol), 1)) for k, v in collections.Counter(x["after"] for x in sol).most_common(5)},
                              solo_inst={k: round(100 * v / max(len(sol), 1)) for k, v in collections.Counter(x["inst"] for x in sol).most_common(6)})
# solo lead by period, compact
json.dump(dict(out, per_song=songs, per_section=secs_all), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "solos_results.json"), "w"), indent=0)
for k in ("songs", "sections"):
    for g, v in out[k].items(): print(k, g, json.dumps(v))
