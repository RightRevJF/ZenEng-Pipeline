"""Song 62: the songbook and production notes (for musicians: no engine terms), every bar, pitch and chord read from out/<label>/record.json.
  python3 songbook62.py "first edition" -> songbook.md (with page breaks for Word), songbook_doc.md (for the Doc), out/<label>/<title> (<label>) - songbook.docx"""
import json, sys, re, subprocess, collections
LABEL = sys.argv[1]; D = f"out/{LABEL}"; R = json.load(open(f"{D}/record.json")); B = R["bar"]; BT = B // 4
NM = ["C", "D♭", "D", "E♭", "E", "F", "G♭", "G", "A♭", "A", "B♭", "B"]; nm = lambda m: NM[m % 12] + str(m // 12 - 1)
chn = lambda c: c.replace("b", "♭") if len(c) > 1 and c[1] == "b" else c
mel = sorted(R["melody"], key=lambda n: n["on"]); bar = lambda t: t // B + 1
start = {}; o = 0
for n, k, b in R["form"]: start[n] = (o // B + 1, b, k); o += b * B
NB = o // B; SECS = round(o / BT * 60 / R["bpm"])
L = collections.defaultdict(list)
for n in mel: L[(n["sec"], n["line"])].append(n)
lyric = {}; sec = None
for raw in open("lyric_locked.md"):
    l = raw.strip()
    if l.startswith("## "): sec = l[3:]; lyric[sec] = []; continue
    if l and sec and not l.startswith("#"): lyric[sec].append(l)
SECNAME = {"Verse 1": "Verse 1", "Chorus 1": "Refrain", "Verse 2": "Verse 2", "Chorus 2": "Refrain", "Bridge": "Bridge", "Verse 3": "Verse 3", "Chorus 3": "Last refrain"}
LYRSEC = {"Verse 1": "Verse 1", "Chorus 1": "Refrain", "Verse 2": "Verse 2", "Chorus 2": "Refrain", "Bridge": "Bridge", "Verse 3": "Verse 3", "Chorus 3": "Last refrain"}
SHOW = {"Intro": "Intro", "Turn 1": "Turn", "Turn 2": "Turn", "Outro": "Outro"} | SECNAME
top = max(n["midi"] for n in mel); low = min(n["midi"] for n in mel)
tops = sorted({(bar(n["on"]), n["text"]) for n in mel if n["midi"] == top})
key = R["key"]["key"].replace("b", "♭"); bass = sorted(R["parts"]["bass"], key=lambda e: e["on"])
def bass_at(b_): x = [e for e in bass if e["on"] == (b_ - 1) * B]; return x[0]["p"] if x else None
def chord_bar(b_):
    for n, (s, nb, k) in start.items():
        if s <= b_ < s + nb: return R["chords"][n][b_ - s], k
def slash(b_):
    c, k = chord_bar(b_); first = c.split()[0]; bp = bass_at(b_)
    if R.get("design") and k == "verse" and bp is not None and NM[bp % 12].replace("♭", "b") != re.match(r"[A-G]b?", first).group(0) and len(c.split()) == 1:
        return chn(first) + "/" + NM[bp % 12]
    return " ".join(chn(x) for x in c.split())
def line_info(sec, i):
    ns = L[(sec, i)]; s, nb, k = start[sec]; slot = s + 2 * i; f = ns[0]
    pick = bar(f["on"]) < slot
    stressed = [n for n in ns if n["stress"]]; hi = max(ns, key=lambda n: n["midi"])
    return dict(slot=slot, pickup=bar(f["on"]) if pick else None, first=nm(f["midi"]), last=nm(ns[-1]["midi"]), lastbar=bar(ns[-1]["on"]), high=(nm(hi["midi"]), hi["text"], bar(hi["on"])), chords=[slash(b_) for b_ in (slot, slot + 1)])
bridge_iv = [b_ for b_ in range(start["Bridge"][0], start["Bridge"][0] + start["Bridge"][1]) if "m" in chord_bar(b_)[0] and chord_bar(b_)[0].startswith(("Abm", "Gbm", "Fm", "Bbm", "Dbm"))]
ivbars = [b_ for b_ in range(start["Bridge"][0], start["Bridge"][0] + 8) if chord_bar(b_)[0] in ("Abm",)]
close = [n for n in L[("Chorus 3", 3)] if n["text"] == "today"][-1]
cello0 = bar(min(e["on"] for e in R["parts"]["cello"])); vln0 = bar(min(e["on"] for e in R["parts"]["violin1"]))
out = []; w = out.append
PB = '\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n'
w(f"# {R['title']} ({LABEL})\n\nWords and music: Jason Bryant\n")
w("## At a glance\n")
w(f"- **Key and feel:** {key} major, 4/4, ♩ = {R['bpm']}, gently, with space. About {SECS // 60}:{SECS % 60:02d}, {NB} bars.")
w(f"- **Voice:** tenor, {nm(low)} to {nm(top)}. The verses sit low and close; the refrain lifts; the bridge is the most open singing, up to G4.")
w("- **Form:** " + ", ".join(f"{SHOW[n]} ({s}–{s + nb - 1})" for n, (s, nb, k) in start.items()) + ".")
w("- **What it is about:** a narrator watches a preacher who has words for every grieving family and almost none for his own son. A friend's unanswered text, a mother who keeps her boy's shoes by the door. Then the father begins to forget, and one cold Saturday he asks his son which game he would like to see. The last line is the first time the song comes all the way home.")
w(f"- **How to play it:** bare and patient. In the verses the voice has only the piano's left hand under it, a bass line that walks down one step a bar, so the harmony keeps moving without ever looping. The refrains open into the piano's chords. The cello comes in at the bridge (bar {cello0}); the whole quartet only in the last refrain (bar {vln0}), and even then the violins answer the voice in its rests rather than play over it.\n")
w("## Section by section\n")
for n, (s, nb, k) in start.items():
    w(f"### {SHOW[n]} (bars {s}–{s + nb - 1})\n")
    if k in ("intro", "solo", "outro"):
        w("| Bar | " + " | ".join(str(b_) for b_ in range(s, s + nb)) + " |\n|---|" + "---|" * nb + "\n| Chord | " + " | ".join(slash(b_) for b_ in range(s, s + nb)) + " |\n")
        if k == "outro": w(f"The piano and first violin play the tune of the last line once more, unsung, from bar {s}, and the piano holds {key} to the end.\n")
        if k == "solo": w("Piano alone, a breath between the refrain and the next verse.\n")
        if k == "intro": w("Piano alone.\n")
        continue
    lines = lyric[LYRSEC[n]] if n != "Chorus 2" else lyric["Refrain"]
    w("| Bars | Chords | Line | Melody |\n|---|---|---|---|")
    for i, txt in enumerate(lines):
        if (n, i) not in L: continue
        x = line_info(n, i); pk = f" (pickup in {x['pickup']})" if x["pickup"] else ""
        w(f"| {x['slot']}–{x['slot'] + 1}{pk} | {x['chords'][0]} · {x['chords'][1]} | {txt} | from {x['first']} to {x['last']}; highest {x['high'][0]} on “{x['high'][1]}” |")
    w("")
    if n == "Verse 1": w(f"The bass walks {', '.join(NM[bass_at(b_) % 12] for b_ in range(s, s + 8))} under the first half, and the second half bends: bar {s + 13} is G minor, not E♭, and the verse ends on C minor (bar {s + 15}), so the refrain arrives from the relative minor.\n")
    if n == "Verse 3": w(f"As verse 1, but its last bar (bar {s + 15}) is B♭: the only verse that leans straight into the refrain's home chord.\n")
    if n == "Bridge": w(f"Bars {ivbars[0]}–{ivbars[-1]} are A♭ minor, the one chord in the song from outside the key, under “for now”. Hold it; do not resolve it. Verse 3 resolves it.\n")
    if n == "Chorus 3": w(f"The last two bars turn: A♭ to B♭, then {key}. “Today” lands on {nm(close['midi'])} over {key} in bar {bar(close['on'])}, the song's first full close.\n")
w("## For each player\n")
vr = [n["midi"] for n in mel if n["sec"].startswith("Verse")]; vmed = sorted(vr)[len(vr) // 2]
w(f"- **Singer:** tell it, don't sell it. The verses run {nm(min(vr))} to {nm(max(vr))} and sit mostly around {nm(vmed)}; keep them conversational. The refrain's notes are longer than the verses' (sing through them). After “good sermon, Dad” (bar {line_info('Verse 1', 6)['lastbar']}) let the silence sit before “And his father nodded”. The highest note, {nm(top)}, falls on “got” in “got a nod across the nave” (bars {', '.join(str(b_) for b_, _ in tops)}). The bridge is the most open singing; “for now” is held and left hanging. The last line is the only one that comes all the way home: land “today” softly.")
w("- **Piano:** the left hand is the song's spine. In the verses it walks down a step a bar; play it legato, the second note of each bar (beat 4) a little lighter. The right hand stays out of the verses and comes in with the refrains; keep it under the voice. In the outro the right hand plays the last line's tune.")
w(f"- **Cello:** from the bridge (bar {cello0}), one long note a bar on the bass line; through verse 3 and the last refrain. Warm, never pushed.")
w(f"- **Violins and viola:** the last refrain only (from bar {vln0}). The viola holds a low fifth under the voice; the violins answer each sung line in its rest with the line's last notes an octave up, then play the last line's tune with the piano in the outro.\n")
w("## The arrangement\n")
w("| Section | Bars | Level | What changes |\n|---|---|---|---|")
arc = [("Intro", "pp", "piano"), ("Verse 1", "p", "voice over the walking bass"), ("Chorus 1", "mp", "the piano's chords come in"), ("Turn 1", "p", "piano"), ("Verse 2", "p", "as verse 1"), ("Chorus 2", "mp", "as the first refrain"), ("Turn 2", "p", "piano"), ("Bridge", "mf", "the cello enters; the voice at its most open; the held A♭ minor"), ("Verse 3", "p", "pulled back again; the cello stays"), ("Chorus 3", "mf", "the quartet: viola under, violins answering in the rests"), ("Outro", "p to pp", "piano and first violin play the last line's tune; hold E♭")]
for n, lv, ch in arc:
    s, nb, k = start[n]; w(f"| {SHOW[n]} | {s}–{s + nb - 1} | {lv} | {ch} |")
w("")
w("## Production notes\n")
w("### Lyric sheet (bars)\n")
for n in ("Verse 1", "Chorus 1", "Verse 2", "Chorus 2", "Bridge", "Verse 3", "Chorus 3"):
    lines = lyric[LYRSEC[n]] if n != "Chorus 2" else lyric["Refrain"]; w(f"**{SHOW[n]}**\n")
    for i, txt in enumerate(lines):
        if (n, i) in L: x = line_info(n, i); w(f"{x['slot']}{' (pickup in ' + str(x['pickup']) + ')' if x['pickup'] else ''}  {txt}  ")
    w("")
w(PB)
w("### Producer one-sheet\n")
w("**Emotional target.** A quiet, steady telling that never pleads, so the small details do the hurting. The last line should feel like a door opening, not a swell.\n")
w("**References.**\n")
w("- Sufjan Stevens, “So You Are Tired” (Javelin, 2023): take the piano and strings, and how little they need to do.")
w("- Sufjan Stevens, “Will Anybody Ever Love Me?” (Javelin, 2023): take the way the strings swell only when the song has earned it.")
w("- Lizzy McAlpine, Older (2024): take the understated arrangements that open into fuller textures without losing fragility.\n")
w("**Dynamic arc.**\n")
w("| Section | Bars | Level | What changes |\n|---|---|---|---|")
for n, lv, ch in arc:
    s, nb, k = start[n]; w(f"| {SHOW[n]} | {s}–{s + nb - 1} | {lv} | {ch} |")
w(f"\nSilences: a full beat after “good sermon, Dad” (bar {line_info('Verse 1', 6)['lastbar']}). Anchor: “today” on {key} (bar {bar(close['on'])}).\n")
w("**Non-negotiables.**\n")
w("- The verse bass walks; never loop it.")
w("- No drums.")
w("- Strings hold back until the bridge (cello) and the last refrain (quartet).")
w(f"- A♭ minor under “for now” (bars {ivbars[0]}–{ivbars[-1]}), unresolved.")
w(f"- The last line lands on {key}, softly.\n")
w("**Mix priorities.** The voice in front and dry enough to hear every word; the piano's left hand clear under it; the strings behind the voice and never over it while it sings; the outro's violin may come forward when the voice is gone.\n")
w(PB)
w("### Production brief\n")
w(f"A chamber-pop ballad for tenor, piano and string quartet in {key} major at ♩ = {R['bpm']}, about {SECS // 60}:{SECS % 60:02d}. References as on the one-sheet. Non-negotiables as on the one-sheet.\n")
w("### Session notes\n")
w(f"- **Tempo and click:** ♩ = {R['bpm']}, 4/4, a steady click; no tempo change.")
w(f"- **Key:** {key} major. **Range:** {nm(low)} to {nm(top)} (tenor).")
w("- **Chords per bar:** as in “Section by section” and on the lead sheet; the verses' slash chords are the walking bass.")
w("- **Tracking:** piano first, to the click (both hands); voice; then cello, viola and violins, which can be tracked together.")
w("- **Blend and panning:** piano wide; voice centre; violins left, viola and cello right of centre, as a quartet would sit.\n")
w("### Score and parts\n")
w(f"- Full score (voice, string quartet, piano), lead sheet (voice, chords, words), parts (piano with the voice cued, violin I, violin II, viola, cello): {R['title']} ({LABEL}).")
w("- Demo (MP3, General MIDI): a sketch for the notes, not the sound.\n")
w(f"*{R['title']} ({LABEL}) · Words and music: Jason Bryant*")
text = "\n".join(out); open("songbook.md", "w").write(text)
open("songbook_doc.md", "w").write(re.sub(r"\n```\{=openxml\}\n.*?\n```\n", "\n", text, flags=re.S))
subprocess.run(["pandoc", "songbook.md", "-o", f"{D}/{R['title']} ({LABEL}) - songbook.docx", "--reference-doc=/home/claude/carol/songbook/ref.docx"], check=True)
print("songbook:", len(text.split()), "words")
