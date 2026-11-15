"""Writes songbook.md for 'A Wire Pulled Tight' (song 51) from song_record.pkl: every bar number, pitch, chord and tempo read from the record.
A musicians' document: no engine terms. Then the Word copy (pandoc, the songbook reference doc)."""
import pickle, collections, subprocess, bisect, itertools
import importlib.util as _u
H = "/home/claude/p61"
R = pickle.load(open(f"{H}/song_record.pkl", "rb"))
PN = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]
def nm(p): return f"{PN[p % 12]}{p // 12 - 1}"
CNAME = {"Dadd9": "Dadd9", "C#dim7": "C♯dim7"}
def cn(c): return CNAME.get(c, c.replace("#", "♯"))
BARS = R["bars"]; BST = [b["start"] for b in BARS]
def barno(t): return bisect.bisect_right(BST, t)
by = collections.OrderedDict()
for n in R["lead"]: by.setdefault((n["sec"], n["line"]), []).append(n)
B0 = {}; NBS = {}
for i, b in enumerate(BARS): B0.setdefault(b["sec"], i); NBS[b["sec"]] = b["n"]
SLOT = R["design"]["slots"]; T = R["tempo"]
_s = _u.spec_from_file_location("lyr", f"{H}/lyric_p61.py"); L = _u.module_from_spec(_s); _s.loader.exec_module(L)
WORDS = {s: [t for _, t in ls] for s, ls in L.SECTIONS}
def line_bars(s, i): b0 = B0[s] + sum(SLOT[s][:i]); return b0, b0 + SLOT[s][i]
def chords_of(b0, b1):
    out = []
    for b in range(b0, b1):
        for c in (BARS[b]["chord"], BARS[b]["chord2"]):
            if not out or out[-1] != c: out.append(c)
    return " ".join(cn(c) for c in out)
def v(s, i): return by[(s, i)]
def span(s): return f"{B0[s] + 1}–{B0[s] + NBS[s]}"
def sec_chords(s):
    out = []
    for c, g in itertools.groupby(BARS[b]["chord"] for b in range(B0[s], B0[s] + NBS[s])):
        k = len(list(g)); out.append(cn(c) + (f" ×{k}" if k > 1 else ""))
    return ", ".join(out)
def tq(s):
    a, z = T[s]; return f"♩ = {a} (felt {a // 2})" if a == z else f"♩ = {a} → {z} (felt {a // 2} → {z // 2})"
def rng_(k):
    ps = [p for e in R["parts"][k] for p in e["p"]]; return f"{nm(min(ps))}–{nm(max(ps))}"
def med(xs): xs = sorted(xs); return xs[len(xs) // 2]
def near(x):
    SC = {9, 11, 1, 2, 4, 6, 8}; r = round(x)
    if r % 12 in SC: return nm(r)
    lo = max(q for q in range(r - 2, r + 1) if q % 12 in SC); hi = min(q for q in range(r, r + 3) if q % 12 in SC); return f"{nm(lo)} to {nm(hi)}"
def KIND_C(n): return n["sec"].startswith("Chorus") or n["sec"] == "Last Chorus"
def notes(ns): return ", ".join(nm(n["midi"]) for n in ns)
ps = [n["midi"] for n in R["lead"]]; vlo, vhi = nm(min(ps)), nm(max(ps))
def table(s, only=None):
    rows = ["| Bars | Chords | Line |", "|---|---|---|"]
    for i, w in enumerate(WORDS[s]):
        if only is not None and i not in only: continue
        b0, b1 = line_bars(s, i); rows.append(f"| {b0 + 1}–{b1} | {chords_of(b0, b1)} | {w} |")
    return "\n".join(rows)
mm, ss = int(R["seconds"] // 60), int(round(R["seconds"] % 60))
vps = [n["midi"] for j in range(4) for n in v("Verse 1", j)]; cps = [n["midi"] for j in range(7) for n in v("Chorus 1", j)]
hk = v("Chorus 1", 7); hl = v("Last Chorus", 7); bd = v("Bridge", 6); tg = v("Tag", 1)
b1ps = [n["midi"] for j in range(4) for n in v("Bridge", j)]
d4 = next(n for n in bd if n["midi"] == 62)
A0 = B0["Approach"]; LC0 = B0["Last Chorus"]
hold = hk[-1]; holdl = hl[-1]
def bars_of(n): return f"{barno(n['on'])}–{barno(n['on'] + n['dur'] - 1)}"
g_nat = sorted({barno(n["on"]) for n in R["lead"] if n["midi"] % 12 == 7})
o = []; A = o.append
A('---\ntitle: "A Wire Pulled Tight"\nsubtitle: "Songbook and production notes"\nauthor: "Words and music: Jason Bryant"\n---\n')
A("# At a glance\n")
A("**What it's about.** Time, felt four ways. A chair in a waiting room where the clock forgets how to move; a laugh at a table while the afternoon slips by; a stadium roar where the clock makes no sound; a fever that breaks at three in the morning. Under all of it runs one wire, every hour strung from the cradle to the stone. The bridge puts the clock down: none of it was lost, none of it was wasted. The song ends where it began, in the same chair, but the weight inside it is a grace now.\n")
A(f"**How it goes.** Slow-build alternative rock in A major, for a baritone. It is written at double tempo with a half-time feel: the snare lands on beat 3 of every written bar, and every tempo you feel is half the one on the page. It starts at {tq('Verse 1')} with one fingerpicked acoustic guitar and grows section by section (bass, then brushes, then the full kit, overdriven guitars and organ) while the tempo climbs to {tq('Bridge')} at the bridge. After the bridge, a bar of silence, four slow bars of guitar, and a final chorus at {tq('Last Chorus')}, slower and steadier than before. The tag, at {tq('Tag')}, is slower than the opening.\n")
A(f"**The hook.** \"time is breaking through\" ends every chorus. In the first three it lands on {nm(hold['midi'])} and holds, still waiting. Only in the final chorus does it climb to {nm(holdl['midi'])}, the song's top note, sung nowhere else. The harmony waits the same way: a full A major chord never sounds on a downbeat until that last \"through.\"\n")
A(f"**Form ({R['nbars']} bars, about {mm}:{ss:02d}).** Verse lines take four bars (two as felt); every other line takes two.\n")
A("| Section | Bars | Tempo | Chords |\n|---|---|---|---|")
for s, nb, st, mets, mv in R["plan"]:
    A(f"| {s} | {span(s)} | {tq(s)} | {sec_chords(s)} |")
_va = [n["midi"] for n in R["lead"] if n["sec"].startswith("Verse")]; _ca = [n["midi"] for n in R["lead"] if KIND_C(n) and n["line"] < 7]
_lift = round(2 * (sum(_ca) / len(_ca) - sum(_va) / len(_va))) / 2
A(f"\n**The singer.** A baritone, {vlo} to {vhi}. The verses sit low (around {near(sum(_va) / len(_va))} on average); the choruses sit about {_lift:g} semitones higher (around {near(sum(_ca) / len(_ca))}). The top before the final chorus is {nm(hold['midi'])}; the bridge reaches {nm(d4['midi'])} once; {vhi} comes only at the very end.\n")
A("# Section by section\n")
A("Pitches are where the voice sounds. Bar numbers count from the first bar of the intro; tempos are as written (felt in brackets).\n")
A(f"## Intro (bars {span('Intro')}, {tq('Intro')})\n\nThe acoustic guitar alone, fingerpicked: the thumb on the root and fifth, the fingers on the upper chord notes between, in written eighths.\n")
A(f"## Verse 1 (bars {span('Verse 1')}, {tq('Verse 1')})\n"); A(table("Verse 1"))
_v0 = v("Verse 1", 0)
A(f"\nVoice and acoustic guitar only, {nm(min(vps))} to {nm(max(vps))}. Each line is sung over about two of its four written bars; the guitar fills the rest. \"There's a chair in the waiting room\" starts on {nm(_v0[0]['midi'])} on the downbeat of bar {barno(_v0[0]['on'])}, close to speech; \"a second stretched thin like a wire pulled tight\" (sung from bar {barno(v('Verse 1', 2)[0]['on'])}) is the title line.\n")
A(f"## Pre-chorus 1 (bars {span('Pre 1')}, {tq('Pre 1')})\n"); A(table("Pre 1"))
_p = [n['midi'] for j in range(2) for n in v('Pre 1', j)]
A(f"\nThe bass comes in on held roots and a clean electric guitar swells; the tempo pushes forward into the chorus. The bass line climbs B, C♯, D, E under the voice ({nm(min(_p))}–{nm(max(_p))}).\n")
A(f"## Chorus 1 (bars {span('Chorus 1')}, {tq('Chorus 1')})\n"); A(table("Chorus 1"))
_c0 = v("Chorus 1", 0)
A(f"\nThe kit comes in, light: kick, cross-stick on beat 3, hat. The chorus opens on D, not A, and its bass walks down D, C♯, B. \"Every hour is a wire\" starts on {nm(_c0[0]['midi'])}. The hook (bars {line_bars('Chorus 1', 7)[0] + 1}–{line_bars('Chorus 1', 7)[1]}): \"time is breaking through\" climbs {notes(hk)}; \"through\" lands on {nm(hold['midi'])} on the downbeat of bar {barno(hold['on'])} over Dmaj7 and holds through bar {barno(hold['on'] + hold['dur'] - 1)}. Harmony joins on that line in every chorus.\n")
A(f"## Verse 2 (bars {span('Verse 2')}, {tq('Verse 2')})\n"); A(table("Verse 2"))
A("\nVerse 1's tunes, fitted to new words. Brushes come in; the overdriven guitar plays quiet palm-muted quarters.\n")
A(f"## Pre-chorus 2 (bars {span('Pre 2')}, {tq('Pre 2')})\n"); A(table("Pre 2"))
A("\nStrummed now; a snare roll in the last half-bar.\n")
A(f"## Chorus 2 (bars {span('Chorus 2')}, {tq('Chorus 2')})\n\nAs chorus 1, with new words on lines 5 and 6:\n"); A(table("Chorus 2", only=(4, 5)))
def _diffbars(sec):
    out = []
    for k in range(NBS["Chorus 1"]):
        a_ = [(n["on"] - BST[B0["Chorus 1"] + k], n["midi"], n["dur"]) for n in R["lead"] if B0["Chorus 1"] + k == barno(n["on"]) - 1]
        b_ = [(n["on"] - BST[B0[sec] + k], n["midi"], n["dur"]) for n in R["lead"] if B0[sec] + k == barno(n["on"]) - 1]
        if a_ != b_: out.append(B0[sec] + k + 1)
    return out
def _bl(xs): return ", ".join(str(x) for x in xs[:-1]) + (" and " if len(xs) > 1 else "") + str(xs[-1])
A(f"\nThe new words are fitted to chorus 1's tune, so a few notes and rhythms shift where they fall (bars {_bl(_diffbars('Chorus 2'))}); every other bar is sung exactly as in chorus 1. The same holds in chorus 3 (bars {_bl(_diffbars('Chorus 3'))}).\n")
A("\nThe full kit, snare on 3; the overdriven guitar opens up; clean arpeggios and the organ on top.\n")
A(f"## Verse 3 (bars {span('Verse 3')}, {tq('Verse 3')})\n"); A(table("Verse 3"))
A("\nThe full kit; the overdriven guitar palm-muted in eighths.\n")
A(f"## Pre-chorus 3 (bars {span('Pre 3')}, {tq('Pre 3')})\n"); A(table("Pre 3"))
A(f"\nThe last chord is C♯dim7 (bar {B0['Pre 3'] + 4}), outside the key, pulling hard toward the chorus's D; a fill over it.\n")
A(f"## Chorus 3 (bars {span('Chorus 3')}, {tq('Chorus 3')})\n\nAs chorus 1, with new words on lines 5 and 6:\n"); A(table("Chorus 3", only=(4, 5)))
A("\nThe most so far: the ride in eighths, crashes on each line's downbeat, the overdriven guitar in eighths. Harmony on the first four lines and the hook.\n")
A(f"## Verse 4 (bars {span('Verse 4')}, {tq('Verse 4')})\n"); A(table("Verse 4"))
A("\nDriving: hats in eighths, the guitars pushing, the organ under it. There is no pre-chorus or chorus after this verse; it goes straight into the bridge.\n")
A(f"## Bridge (bars {span('Bridge')}, {tq('Bridge')})\n"); A(table("Bridge"))
A(f"\nTwice through D F♯/A♯ Bm G. The first pass (bars {B0['Bridge'] + 1}–{B0['Bridge'] + 8}) strips back to the acoustic guitar and the kick, low and plain ({nm(min(b1ps))}–{nm(max(b1ps))}): sing \"and I put the clock down\" straight. The second pass builds (kit, strumming, organ, then the overdriven guitar from bar {B0['Bridge'] + 13}) and the melody presses up: \"none of it was ever lost\" climbs {notes(bd)}, touching {nm(d4['midi'])} over Bm in bar {barno(d4['on'])}. A fill, and a full stop.\n")
A(f"## Approach (bars {span('Approach')}, {tq('Approach')})\n\nBar {A0 + 1}: silence, everyone (two felt beats). Bars {A0 + 2}–{A0 + 8}: the acoustic guitar alone, G for five bars and Asus2 for two, slowing. Don't fill it.\n")
A(f"## Final chorus (bars {span('Last Chorus')}, {tq('Last Chorus')})\n\nAs chorus 1, with new words on lines 5 and 6:\n"); A(table("Last Chorus", only=(4, 5, 6, 7)))
A(f"\nThe full band, steady: big but not louder than the bridge. Over the G, \"and somewhere in the stillness\" takes G3 where the other choruses sing F♯3. At the G (bars {LC0 + 13}–{LC0 + 15}) everything thins to the voice, the acoustic guitar and the organ. Then \"time is breaking through\" climbs {notes(hl)}: \"through\" lands on {nm(holdl['midi'])} over Asus4 in bar {barno(holdl['on'])} with the band back in, and the Asus4 releases to A in bar {LC0 + 18}, a crash and the first full A chord on a downbeat in the song. Hold {nm(holdl['midi'])} through bar {barno(holdl['on'] + holdl['dur'] - 1)} and let the chord ring. Harmony on every line.\n")
A(f"## Tag (bars {span('Tag')}, {tq('Tag')})\n"); A(table("Tag"))
A(f"\nThe acoustic guitar alone. The opening line comes back exactly as verse 1 sang it; then \"and the weight inside it is a grace\" settles to {nm(tg[-1]['midi'])} on \"grace\" over A (bar {barno(tg[-1]['on'])}). The last A rings and decays. No fade.\n")
A("# For each player\n")
A(f"**Voice.** A baritone, {vlo} to {vhi}. The verses are testimony: plain, close, unhurried, telling it, not selling it. Lean into the choruses but keep the held {nm(hold['midi'])} on \"through\" open and unresolved; it is supposed to feel like waiting. In the bridge come right down, then let the second pass rise to {nm(d4['midi'])}. Save everything for the final chorus's {vhi}; it is the one time the song reaches it.\n")
A(f"**Harmony vocals.** Two parts, one above and one below: on the hook in every chorus, the first four lines of chorus 3, and every line of the final chorus (high {nm(min(n['midi'] for n in R['harm_hi']))}–{nm(max(n['midi'] for n in R['harm_hi']))}, low {nm(min(n['midi'] for n in R['harm_lo']))}–{nm(max(n['midi'] for n in R['harm_lo']))}). Blend under the lead.\n")
A(f"**Acoustic guitar** ({rng_('acoustic')}). Steel-string. Fingerpicked in the intro, verse 1, pre-chorus 1, verse 2 and the bridge's first pass; strummed from pre-chorus 2 on; picked again in the approach and the tag. Alone in the intro, verse 1, the approach and the tag.\n")
A(f"**Electric guitar, clean** ({rng_('electric')}). Swells in pre-chorus 1; a held chord in chorus 1; eighth-note arpeggios in choruses 2 and 3, the bridge (from bar {B0['Bridge'] + 5}) and the final chorus.\n")
A(f"**Electric guitar, overdriven** ({rng_('drive')}). Root, fifth and octave. Palm-muted quarters in verse 2 and pre-chorus 2; open chords in chorus 2; palm-muted eighths in verse 3; eighths in chorus 3; in verse 4, two bars palm-muted, two bars open, in turn; in at bar {B0['Bridge'] + 13} of the bridge; out at the final chorus's G, back on the Asus4.\n")
A(f"**Organ** ({rng_('organ')}). A pad in every chorus, pre-chorus 3, verse 4 and the bridge's second pass; stays with the voice at the final chorus's G.\n")
A(f"**Bass** ({rng_('bass')}). Held roots in pre-chorus 1; a line from chorus 1 on; held roots in the bridge's first pass from bar {B0['Bridge'] + 3}, the line again from bar {B0['Bridge'] + 9}; out at the final chorus's G; a low A under the release.\n")
A("**Drums.** Half-time throughout: the snare (or cross-stick) on beat 3 of each written bar.\n\n- *Intro, verse 1, pre-chorus 1, approach, tag:* out.\n- *Chorus 1:* light: kick, cross-stick, hat in quarters.\n- *Verse 2, pre-chorus 2:* brushes; a snare roll into chorus 2.\n- *Chorus 2, verse 3, pre-chorus 3:* full kit; a fill at the end of pre-chorus 3.\n- *Chorus 3:* the ride in eighths; crash on each line's downbeat.\n- *Verse 4:* driving, hats in eighths.\n- *Bridge:* kick alone for eight bars, then the kit building to a fill and a full stop.\n- *Final chorus:* full, steady; out at the G; back with a crash on the Asus4 and another on the A.\n")
A("# Arrangement\n")
A("The tempo is the story. The song starts at a waiting-room pulse and speeds up through every verse and chorus, the band filling in as it goes: one guitar, then bass, brushes, the kit, overdrive and organ. The bridge is the peak and then the break: a bar of silence and four bars of one guitar, slowing, like lying still after a fever. The final chorus comes back slower than the choruses before it, full but steady, and saves the song's top note and its first full A chord for the last \"through.\" The tag is the opening image again, slower than ever, on one guitar.\n")
A("# Production notes\n")
A("## Lyric sheet with bar numbers\n")
A("| Bar | Line |\n|---|---|")
for (s, i), ns in by.items():
    if s in ("Chorus 2", "Chorus 3", "Last Chorus") and i not in (4, 5):
        if i == 0: A(f"| {span(s)} | (chorus; new lines 5–6 below) |")
        continue
    b_ = line_bars(s, i)[0] + 1; f_ = barno(ns[0]['on'])
    A(f"| {b_}{f' (pickup in {f_})' if f_ < b_ else ''} | {WORDS[s][i]} |")
A('\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n')
A("## Producer one-sheet\n")
A("**The emotional target.** Testimony, not celebration. Someone who has waited, drifted, been carried away and been broken open, telling you that none of it was wasted. The build should feel earned and the ending should feel changed: the same chair, a different weight.\n")
A("**The three references.**\n")
A("- **Coldplay, \"Fix You\"** (*X&Y*, 2005): an organ-led ballad that builds into full alternative rock in its second half. Take the shape of the build and the organ's role.\n- **Snow Patrol, \"Run\"** (*Final Straw*, 2003; single 2004): a slow guitar ballad that grows into an anthem. Take the patience of the climb and the big, steady last chorus.\n- **Band of Horses, \"The Funeral\"** (*Everything All the Time*, 2006): quiet verses that break open into a loud, ringing chorus. Take the quiet-to-loud dynamics and the ringing guitars.\n")
A("**The dynamic arc.**\n")
A("| Section | Bars | Level | What changes |\n|---|---|---|---|")
for lab, s1, lv, wh in (("Intro, verse 1", "Verse 1", "pp", "one acoustic guitar and the voice"), ("Pre-chorus 1", "Pre 1", "p → mp", "bass in; clean guitar swells; speeding up"),
                        ("Chorus 1", "Chorus 1", "mp", "the kit in, light; organ; harmony on the hook"), ("Verse 2, pre-chorus 2", "Verse 2", "mp → mf", "brushes; muted overdrive; a roll"),
                        ("Chorus 2", "Chorus 2", "mf", "full kit; open overdrive"), ("Verse 3, pre-chorus 3", "Verse 3", "mf → f", "full kit; C♯dim7 and a fill"),
                        ("Chorus 3", "Chorus 3", "f", "the most so far; crashes"), ("Verse 4", "Verse 4", "f", "driving"),
                        ("Bridge", "Bridge", "p → ff", "stripped to guitar and kick, then the build to a full stop"), ("Approach", "Approach", "silence → pp", "a bar of silence; one guitar, slowing"),
                        ("Final chorus", "Last Chorus", "f, steady", "thins at the G; the band back on Asus4; the release to A"), ("Tag", "Tag", "pp", "one guitar; the last A decays")):
    sp_ = {"Verse 1": f"1–{B0['Verse 1'] + NBS['Verse 1']}", "Verse 2": f"{B0['Verse 2'] + 1}–{B0['Pre 2'] + NBS['Pre 2']}", "Verse 3": f"{B0['Verse 3'] + 1}–{B0['Pre 3'] + NBS['Pre 3']}"}.get(s1, span(s1))
    A(f"| {lab} | {sp_} | {lv} | {wh} |")
A(f"\n**The non-negotiables.** The tempo plan as written, no click track that fights it. The held {nm(hold['midi'])} on \"through\" in choruses 1–3, unresolved over Dmaj7. The bar of silence after the bridge, and the four bars of one guitar after it. {vhi} sung only once, on the final \"through,\" over Asus4 releasing to A. No full A chord on a downbeat before that moment. The tag slower than the opening.\n")
A("**The mix priorities.** The voice forward and close in the verses, every word clear. The acoustic guitar at the centre of the first half; the overdriven guitar wide but under the voice in the second. The organ as glue, never a lead. In the silent bar, true silence: no reverb tails.\n")
A('\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n')
A("## Production brief\n")
A("*The song.* A slow-build alternative rock song about four kinds of time, a wire running under all of them, and the moment it breaks through.\n")
A("*References* (checked by search):\n")
A("- **Coldplay, \"Fix You.\"** From *X&Y* (Parlophone, 2005), written by all four members; built around an organ with piano and guitar in its first half and full alternative rock (electric guitar, bass, drums) in its second; released as the album's second single on 5 September 2005; number 4 in the UK.\n- **Snow Patrol, \"Run.\"** From *Final Straw* (2003), produced by Jacknife Lee; written by Gary Lightbody, Iain Archer, Mark McClelland, Nathan Connolly and Jonny Quinn; released as a single in early 2004; number 5 in the UK; the album version runs 5:56.\n- **Band of Horses, \"The Funeral.\"** From *Everything All the Time* (Sub Pop, March 21, 2006), produced by Phil Ek; released as a single in the US on May 21, 2006; 5:21.\n")
A("*Non-negotiables.* As on the one-sheet.\n")
A("## Session notes\n")
A("- **Tempo and click.** Written at double tempo with a half-time feel; if you use a click, program the tempo map, section by section:\n")
A("| Section | Written tempo | Felt |\n|---|---|---|")
for s, nb, st, mets, mv in R["plan"]:
    a, z = T[s]; A(f"| {s} | ♩ = {a}" + (f" → {z} (gradual)" if a != z else "") + f" | {a // 2}" + (f" → {z // 2}" if a != z else "") + " |")
A(f"\n- **Key.** A major. The voice stays in the scale except G natural over the G chord (bars {', '.join(str(b) for b in g_nat)}).\n- **Chords per bar.** As in the section tables: one chord to a bar, one written bar is half a felt bar.\n- **Range.** Voice {vlo}–{vhi}; harmony as above.\n- **Tracking.** Acoustic guitar and a guide vocal to the tempo map first; bass and drums; the electric guitars and organ; the lead vocal; harmonies with the finished lead in the headphones.\n- **Blend and panning.** Voice centre; acoustic slightly left; clean electric right, overdriven left; organ wide right; bass and kick centre; harmonies slightly left and right.\n- **The silent bar.** Bar {A0 + 1}: every track silent; cut reverb tails before it.\n- **The holds.** \"through\" holds four and a half bars in choruses 1–3 and {round(holdl['dur'] / 48, 1):g} bars in the final chorus.\n")
A("## Score and parts\n")
A("- Lead sheet: voice, words, chord symbols and the tempo at each section (PDF).\n- Full score: every part on one set of systems (PDF).\n- Parts: harmony vocals (high, low), acoustic guitar, clean electric guitar, overdriven electric guitar, organ, bass and drums (PDF).\n- Number chart (PDF).\n- MusicXML: the lead sheet and the full score (.musicxml and .mxl).\n- Demo: MP3 and a General MIDI file.\n")
open(f"{H}/songbook.md", "w").write("\n".join(o) + "\n")
subprocess.run(["pandoc", f"{H}/songbook.md", "--reference-doc=/home/claude/carol/songbook/ref.docx", "-o", f"{H}/out/{R['file_title']} - songbook.docx"], check=True)
print("ok", len("\n".join(o)))
