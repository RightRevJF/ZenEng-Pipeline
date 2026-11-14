"""Writes songbook.md for 'The Small Things' (song 50) from song_record.pkl: every bar number, pitch and chord read from the record. A
musicians' document: no engine terms. Then the Word copy (pandoc, the songbook reference doc)."""
import pickle, collections, subprocess, bisect
import importlib.util as _u
R = pickle.load(open("/home/claude/p60/song_record.pkl", "rb"))
PN = ["C", "C♯", "D", "E♭", "E", "F", "F♯", "G", "G♯", "A", "B♭", "B"]
def nm(p): return f"{PN[p % 12]}{p // 12 - 1}"
def cn(c): return c.replace("#", "♯")
BARS = R["bars"]; BST = [b["start"] for b in BARS]
def barno(t): return bisect.bisect_right(BST, t)
by = collections.OrderedDict()
for n in R["lead"]: by.setdefault((n["sec"], n["line"]), []).append(n)
B0 = {}; NBS = {}
for i, b in enumerate(BARS): B0.setdefault(b["sec"], i); NBS[b["sec"]] = b["n"]
SLOT = R["design"]["slots"]
_s = _u.spec_from_file_location("lyr", "/home/claude/p60/lyric_p60.py"); L = _u.module_from_spec(_s); _s.loader.exec_module(L)
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
def sec_chords(s): return " ".join(cn(BARS[b]["chord"]) if BARS[b]["chord"] == BARS[b]["chord2"] else f"{cn(BARS[b]['chord'])}–{cn(BARS[b]['chord2'])}" for b in range(B0[s], B0[s] + NBS[s]))
def rng_(k):
    ps = [p for e in R["parts"][k] for p in e["p"]]; return f"{nm(min(ps))}–{nm(max(ps))}"
def med(xs): xs = sorted(xs); return xs[len(xs) // 2]
ps = [n["midi"] for n in R["lead"]]; vlo, vhi = nm(min(ps)), nm(max(ps))
def table(s):
    rows = ["| Bars | Chords | Line |", "|---|---|---|"]
    for i, w in enumerate(WORDS[s]):
        b0, b1 = line_bars(s, i); rows.append(f"| {b0 + 1}–{b1} | {chords_of(b0, b1)} | {w} |")
    return "\n".join(rows)
mm, ss = int(R["seconds"] // 60), int(round(R["seconds"] % 60))
hk, hw = v("Chorus 1", 6), v("Chorus 1", 7); b3 = v("Bridge", 3)
vps = [n["midi"] for j in range(8) for n in v("Verse 1", j)]; cps = [n["midi"] for j in range(6) for n in v("Chorus 1", j)]
bps = [n["midi"] for j in range(3) for n in v("Bridge", j)]
small = next(n for n in hk if n["text"].startswith("small")); will = hw[-1]
def runs(ns):
    """the longest run of one pitch in a line: (length, the pitch)"""
    best, r, q = (1, ns[0]["midi"]), 1, ns[0]["midi"]
    for a, b in zip(ns, ns[1:]):
        r = r + 1 if b["midi"] == a["midi"] else 1
        if r > best[0]: best = (r, b["midi"])
    return best
o = []; A = o.append
A('---\ntitle: "The Small Things"\nsubtitle: "Songbook and production notes"\nauthor: "Words and music: Jason Bryant"\n---\n')
A("# At a glance\n")
A("**What it's about.** A late afternoon on the couch. The light lies across the floor, Sammie takes his post by the sliding glass door, a bumblebee bounces past, and Maggie hits the glass with both paws. There's no moral to it, the song says, and then it finds one anyway: somebody else is watching this too, and laughing, and God likes the small things. The bridge says it plainly: nobody sent me here; I just sat down on a Tuesday, and the holy showed up clear.\n")
A(f"**How it goes.** Gentle acoustic folk, ♩ = {R['qbpm']} with a slow swing, D major, for a baritone. A fingerpicked acoustic guitar carries the whole song; a soft piano, an acoustic bass and light brushes come and go around it. The hook, \"I think God likes the small things,\" climbs to the song's top note on \"small\" and holds it; \"I think He always will\" steps back down and lands home. The bridge drops to the guitar alone, stops for one beat, and rises into \"the holy showed up clear.\" The last line of the song slows to a stop.\n")
A(f"**Form ({R['nbars']} bars, about {mm}:{ss:02d}).** Every sung line takes two bars. Swing the eighths: long-short, gently.\n")
A("| Section | Bars | Chords |\n|---|---|---|")
for s, nb, st, mets, mv in R["plan"]:
    ch = {"Chorus 2": "as chorus 1", "Verse 2": "as verse 1", "Last Chorus": "as chorus 1"}.get(s) or sec_chords(s)
    A(f"| {s} | {span(s)} | {ch} |")
A(f"\n**The singer.** A baritone, {vlo} to {vhi}. The verses sit low (around {nm(med(vps))}); the choruses lift about {med(cps) - med(vps)} semitones (around {nm(med(cps))}); the top, {vhi}, is the hook's held \"small.\"\n")
A("# Section by section\n")
A("Pitches are where the voice sounds. Bar numbers count from the first bar of the intro.\n")
A(f"## Intro (bars {span('Intro')})\n\nThe acoustic guitar alone, fingerpicked and swung: the thumb on the root and fifth, the fingers between. In bars 3–4 the piano plays the hook's tune an octave up, softly, before anyone has sung it.\n")
A(f"## Verse 1 (bars {span('Verse 1')})\n"); A(table("Verse 1"))
_v0 = v("Verse 1", 0); _e0 = _v0[0]["on"] - BST[line_bars("Verse 1", 0)[0]]
ENT0 = "a beat before the bar line, as a pickup" if _e0 < 0 else ("on the downbeat" if _e0 == 0 else "just after the downbeat")
_r = max(((runs(v("Verse 1", j)), j) for j in range(8)), key=lambda x: x[0][0])
A(f"\nPlain and unhurried, {nm(min(vps))} to {nm(max(vps))}. \"Late afternoon\" begins on {nm(_v0[0]['midi'])} {ENT0}. The verse stays close to home, often repeating a note the way speech does (\"{WORDS['Verse 1'][_r[1]]}\" holds {nm(_r[0][1])} for {_r[0][0]} syllables), so the story sounds told rather than sung. The second half of the verse (from bar {line_bars('Verse 1', 4)[0] + 1}) takes the first half's tunes again over the same chords; the acoustic bass enters there. \"and doesn't even slow down\" ends on {nm(v('Verse 1', 7)[-1]['midi'])}, not home: the chorus answers it.\n")
A(f"## Chorus 1 (bars {span('Chorus 1')})\n"); A(table("Chorus 1"))
_c0 = v("Chorus 1", 0)
A(f"\nThe chorus lifts. \"And I think somebody's watching this\" starts on {nm(_c0[0]['midi'])} and rises to {nm(_c0[-1]['midi'])} at its end. The hook (bars {line_bars('Chorus 1', 6)[0] + 1}–{line_bars('Chorus 1', 7)[1]}): \"I think God likes the small things\" climbs {', '.join(nm(n['midi']) for n in hk)}, reaching {nm(small['midi'])} on \"small\" on the downbeat of bar {barno(small['on'])} and holding it; \"I think He always will\" steps down {', '.join(nm(n['midi']) for n in hw)} and lands home on {nm(will['midi'])} over D in bar {barno(will['on'])}. Harmony joins on those two lines in every chorus.\n")
A(f"## Verse 2 (bars {span('Verse 2')})\n"); A(table("Verse 2"))
A("\nThe verse tunes again, fitted to new words. The piano answers softly at the end of every other bar.\n")
A(f"## Chorus 2 (bars {span('Chorus 2')})\n\nAs chorus 1, the brushes moving from the rim to the snare.\n")
A(f"## Bridge (bars {span('Bridge')})\n"); A(table("Bridge"))
L3 = BST[line_bars("Bridge", 3)[0]]
A(f"\nThe drop: the guitar alone, low and quiet. The first three lines stay between {nm(min(bps))} and {nm(max(bps))}. On the first beat of bar {line_bars('Bridge', 3)[0] + 1} everything stops for one beat. Then \"and the holy showed up clear\" rises {', '.join(nm(n['midi']) for n in b3)} and holds \"clear\" on {nm(b3[-1]['midi'])} over A, open, into the last chorus.\n")
A(f"## Last chorus (bars {span('Last Chorus')})\n"); A(table("Last Chorus"))
A(f"\nThe fullest the song gets: guitar, piano, bass, brushes on the snare, and harmony on every line. The last line, \"I think He always will,\" slows down beat by beat (a ritardando) and lands on {nm(will['midi'])} at the end.\n")
A(f"## Outro (bars {span('Outro')})\n\nThe guitar picking, softer each bar; in bars {B0['Outro'] + 2}–{B0['Outro'] + 3} the piano echoes \"I think He always will\" an octave up; the last bar a D chord, let ring.\n")
A("# For each player\n")
A(f"**Voice.** A baritone, {vlo} to {vhi}. Sing the verses like you're telling the person next to you on the couch what the cats just did: no push, a smile in it. Open up a little at the chorus, and lean on the held \"small\"; then let \"I think He always will\" come home easily. In the bridge come right down, nearly speaking, take the one beat of silence, and let \"the holy showed up clear\" rise on its own. Take your time on the last line.\n")
A(f"**Harmony vocals.** Two parts, one above and one below, on the hook in every chorus and on every line of the last chorus (high {nm(min(n['midi'] for n in R['harm_hi']))}–{nm(max(n['midi'] for n in R['harm_hi']))}, low {nm(min(n['midi'] for n in R['harm_lo']))}–{nm(max(n['midi'] for n in R['harm_lo']))}). Blend under the lead.\n")
A(f"**Acoustic guitar** ({rng_('guitar')}). Steel-string, fingerpicked all the way through (thumb on the root and fifth on the beats, fingers on the upper chord notes between), with the eighths swung. A little fuller in the choruses. Alone in the bridge; stop for the one beat of silence at the start of bar {line_bars('Bridge', 3)[0] + 1}.\n")
A(f"**Piano** ({rng_('piano')}). The hook's tune in the intro; soft answers at the end of every other bar in verse 2; half-note chords in the choruses; out in the bridge; the hook's last line in the outro.\n")
A(f"**Acoustic bass** ({rng_('bass')}). In halfway through verse 1; root on every chord change, walking lightly between; out in the bridge; back for the last chorus; a last low D in the outro.\n")
A("**Drums.** Brushes only.\n\n- *Intro, verse 1, verse 2, bridge, outro:* out.\n- *Chorus 1:* brushes: kick soft on 1 and 3, rim on 2 and 4, ride in quarters.\n- *Chorus 2:* brushes, snare on 2 and 4, ride in eighths (swung).\n- *Last chorus:* as chorus 2, a touch more; follow the singer through the slowing last line.\n")
A("# Arrangement\n")
A("The song is an afternoon you don't want to end. The guitar never stops picking, so the whole song feels like one long, easy moment. Each chorus adds a little: piano, bass, brushes, and harmony on the hook. The bridge takes everything away except the guitar, then takes that away too for one beat, so \"the holy showed up clear\" arrives in real quiet. The last chorus is the fullest, and its last line slows down like the light going.\n")
A("# Production notes\n")
A("## Lyric sheet with bar numbers\n")
A("| Bar | Line |\n|---|---|")
for (s, i), ns in by.items():
    if s in ("Chorus 2", "Last Chorus"):
        if i == 0: A(f"| {span(s)} | (chorus{', the last line slowing' if s == 'Last Chorus' else ''}) |")
        continue
    b_ = line_bars(s, i)[0] + 1; f_ = barno(ns[0]['on'])
    A(f"| {b_}{f' (pickup in {f_})' if f_ < b_ else ''} | {WORDS[s][i]} |")
A('\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n')
A("## Producer one-sheet\n")
A("**The emotional target.** Contentment and quiet wonder. Nothing happens, and that is the point: a man notices an ordinary afternoon and suspects God is enjoying it too. Warm, a little funny, never preachy.\n")
A("**The three references.**\n")
A("- **Cat Stevens, \"Morning Has Broken\"** (*Teaser and the Firecat*, 1971): Eleanor Farjeon's hymn of praise for an ordinary morning, with Rick Wakeman's piano. Take the wonder at plain things and the piano's gentleness.\n- **Simon & Garfunkel, \"The 59th Street Bridge Song (Feelin' Groovy)\"** (*Parsley, Sage, Rosemary and Thyme*, 1966): \"Slow down, you move too fast.\" Take the unhurried delight and the light touch.\n- **Iron & Wine, \"Naked as We Came\"** (*Our Endless Numbered Days*, 2004): a short, intimate acoustic song in close harmony. Take the closeness of the voice and the harmony on the hook.\n")
A("**The dynamic arc.**\n")
A("| Section | Bars | Level | What changes |\n|---|---|---|---|")
for lab, s1, lv, wh in (("Intro", "Intro", "p", "guitar alone; the hook's tune on piano"), ("Verse 1", "Verse 1", "p → mp", "guitar and voice; bass in halfway"),
                        ("Chorus 1", "Chorus 1", "mp+", "piano, bass, brushes on the rim; harmony on the hook"), ("Verse 2", "Verse 2", "mp", "guitar, bass, piano answers"),
                        ("Chorus 2", "Chorus 2", "mf", "brushes on the snare"), ("Bridge", "Bridge", "pp → silence → p", "guitar alone; one beat of silence"),
                        ("Last chorus", "Last Chorus", "mf", "the fullest; harmony on every line; the last line slows"), ("Outro", "Outro", "p", "guitar and the piano's echo, fading")):
    A(f"| {lab} | {span(s1)} | {lv} | {wh} |")
A(f"\n**The non-negotiables.** The held {nm(small['midi'])} on \"small.\" \"I think He always will\" landing home on {nm(will['midi'])}. The one beat of silence before \"and the holy showed up clear,\" held open on {nm(b3[-1]['midi'])}. The swing, gentle throughout. The last line slowing to a stop. Nothing louder than mf.\n")
A("**The mix priorities.** The voice close and warm, every word clear. The guitar's picking at the centre of everything, slightly left; the piano right and soft. Brushes as texture, never a beat you notice. In the bridge's silent beat, let the room be silent.\n")
A('\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n')
A("## Production brief\n")
A("*The song.* A gentle folk song about watching two cats and a bumblebee on a lazy afternoon, and suspecting that God likes the small things too.\n")
A("*References* (checked by search):\n")
A("- **Cat Stevens, \"Morning Has Broken.\"** From *Teaser and the Firecat* (1971); words by Eleanor Farjeon (a hymn first published in 1931) set to the traditional tune \"Bunessan\"; piano by Rick Wakeman; recorded March 1971 at Morgan Studios, London; 3:20.\n- **Simon & Garfunkel, \"The 59th Street Bridge Song (Feelin' Groovy).\"** From *Parsley, Sage, Rosemary and Thyme* (Columbia, 1966); recorded August 16, 1966; 1:43; Joe Morello (drums) and Eugene Wright (double bass) of the Dave Brubeck Quartet play on it.\n- **Iron & Wine, \"Naked as We Came.\"** From *Our Endless Numbered Days* (Sub Pop, March 23, 2004), produced by Brian Deck; 2:32.\n")
A("*Non-negotiables.* As on the one-sheet.\n")
A("## Session notes\n")
_f7 = [(s_, i_) for (s_, i_), ns_ in by.items() if any(n_['midi'] % 12 == 0 for n_ in ns_)]
_f7s = sorted({s_ for s_, _ in _f7}, key=lambda x_: list(B0).index(x_))
F7 = ("The flat seventh (C natural) appears as a passing note in the voice in " + (" and ".join(", ".join(("the " if x_ == "Bridge" else "") + x_.lower() for x_ in _f7s).rsplit(", ", 1)) if len(_f7s) > 1 else ("the " if _f7s[0] == "Bridge" else "") + _f7s[0].lower()) + " (bars " + ", ".join(str(b_) for b_ in sorted({barno(n_['on']) for k_ in _f7 for n_ in by[k_] if n_['midi'] % 12 == 0})) + ").") if _f7 else "No note outside the scale in the voice."
A(f"- **Tempo and click.** ♩ = {R['qbpm']} throughout, 4/4, swung eighths (a triplet feel); the click in quarters. The last line of the song slows (ritardando): follow the singer, no click.\n- **Key.** D major. {F7}\n- **Chords per bar.** As in the section tables; most bars hold one chord, some two (two beats each).\n- **Range.** Voice {vlo}–{vhi}; harmony as above.\n- **Tracking.** Guitar and a guide vocal to the click first; then bass and piano; then brushes; the lead vocal; the harmonies with the finished lead in the headphones.\n- **Blend and panning.** Voice centre; guitar slightly left, piano right; bass and kick centre; harmonies slightly left and right.\n- **The silent beat.** The first beat of bar {line_bars('Bridge', 3)[0] + 1}: every track silent; cut reverb tails before it.\n")
A("## Score and parts\n")
A("- Lead sheet: voice, words and chord symbols (PDF).\n- Full score: every part on one set of systems (PDF).\n- Parts: harmony vocals (high, low), acoustic guitar, piano, acoustic bass and drums (PDF).\n- Number chart (PDF).\n- MusicXML: the lead sheet and the full score (.musicxml and .mxl).\n- Demo: MP3 and a General MIDI file.\n")
open("/home/claude/p60/songbook.md", "w").write("\n".join(o) + "\n")
subprocess.run(["pandoc", "/home/claude/p60/songbook.md", "--reference-doc=/home/claude/carol/songbook/ref.docx", "-o", "/home/claude/p60/out/The Small Things - songbook.docx"], check=True)
print("ok")
