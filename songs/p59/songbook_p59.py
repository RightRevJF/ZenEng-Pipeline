"""Writes songbook.md for 'The World Is Asking' (song 49) from song_record.pkl: every bar number, pitch and chord read from the record. A
musicians' document: no engine terms. Then the Word copy (pandoc, the songbook reference doc)."""
import pickle, collections, subprocess, bisect
import importlib.util as _u
R = pickle.load(open("/home/claude/p59/song_record.pkl", "rb"))
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
_s = _u.spec_from_file_location("lyr", "/home/claude/p59/lyric_p59.py"); L = _u.module_from_spec(_s); _s.loader.exec_module(L)
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
hk, h7, lc7 = v("Chorus 1", 0), v("Chorus 1", 6), v("Last Chorus", 7)
b4, b5 = v("Bridge", 4), v("Bridge", 5)
vps = [n["midi"] for j in range(8) for n in v("Verse 1", j)]; cps = [n["midi"] for j in (1, 2, 3, 4, 5, 7) for n in v("Chorus 1", j)]
bps = [n["midi"] for j in range(4) for n in v("Bridge", j)]
o = []; A = o.append
A('---\ntitle: "The World Is Asking"\nsubtitle: "Songbook and production notes"\nauthor: "Words and music: Jason Bryant"\n---\n')
A("# At a glance\n")
A("**What it's about.** A man grew up in a house with a door painted shut, taught to trust only what he could touch, and to call any knock in the night the wind. The chorus turns: the world is asking, in the smallest hum, in the stutter of a heart, in the first light of everything. Three strangers working far apart found the same small circle coming round. The bridge answers without proof: a door left open a crack, and a prayer to whoever is asking. \"Here I am. Speak, I'm listening.\"\n")
A(f"**How it goes.** Indie folk, ♩ = {R['qbpm']}, G major, for a baritone. A fingerpicked acoustic guitar carries the verses; the choruses open into strummed guitar, piano, strings and brushes. The hook, \"The world is asking,\" climbs and hangs on D, the fifth, a question left open. The bridge drops low and close, falls silent for a bar, and asks to be spoken to. Only the last chorus's last line comes home to G.\n")
A(f"**Form ({R['nbars']} bars, about {mm}:{ss:02d}).** Every sung line takes two bars.\n")
A("| Section | Bars | Chords |\n|---|---|---|")
for s, nb, st, mets, mv in R["plan"]:
    ch = {"Chorus 2": "as chorus 1", "Verse 2": "as verse 1"}.get(s) or sec_chords(s)
    A(f"| {s} | {span(s)} | {ch} |")
A(f"\n**The singer.** A baritone, {vlo} to {vhi}. The verses sit low (around {nm(med(vps))}); the choruses lift about {med(cps) - med(vps)} semitones (around {nm(med(cps))}); the top, {vhi}, is the hook's held \"asking.\"\n")
A("# Section by section\n")
A("Pitches are where the voice sounds. Bar numbers count from the first bar of the intro.\n")
A(f"## Intro (bars {span('Intro')})\n\nThe acoustic guitar alone, fingerpicked: the thumb on the root and fifth, the fingers between. In bars 3–4 the piano plays the hook's figure an octave up, softly, before anyone has sung it.\n")
A(f"## Verse 1 (bars {span('Verse 1')})\n"); A(table("Verse 1"))
A(f"\nPlain and close, {nm(min(vps))} to {nm(max(vps))}. \"There's a door\" begins on {nm(v('Verse 1', 0)[0]['midi'])} just after the downbeat and settles on G for \"house.\" The second half of the verse (from bar {line_bars('Verse 1', 4)[0] + 1}) sings the first half's shapes again over the same chords; the acoustic bass enters there. \"I told myself it was the wind\" ends on {nm(v('Verse 1', 7)[-1]['midi'])}, not home: the chorus answers it.\n")
A(f"## Chorus 1 (bars {span('Chorus 1')})\n"); A(table("Chorus 1"))
A(f"\nThe chorus lifts and opens. The hook, \"But the world is asking\" (bars {line_bars('Chorus 1', 0)[0] + 1}–{line_bars('Chorus 1', 0)[1]}): {', '.join(nm(n['midi']) for n in hk)}, climbing to {nm(hk[-1]['midi'])} on \"ask-\" and holding \"-ing\" there into the D chord, unresolved. Line 7, \"The world is asking\" (bars {line_bars('Chorus 1', 6)[0] + 1}–{line_bars('Chorus 1', 6)[1]}), is the same figure without \"But.\" \"Will I let the question in\" ends on {nm(v('Chorus 1', 7)[-1]['midi'])} over D: the question stays open.\n")
A(f"## Verse 2 (bars {span('Verse 2')})\n"); A(table("Verse 2"))
A("\nThe verse tune again, fitted to new words: the three strangers and the circle. The piano answers at the end of each bar; brushes on the rim.\n")
A(f"## Chorus 2 (bars {span('Chorus 2')})\n\nAs chorus 1, the strings higher, brushes on the snare.\n")
A(f"## Bridge (bars {span('Bridge')})\n"); A(table("Bridge"))
A(f"\nThe drop. Piano alone, low and close; the first four lines stay between {nm(min(bps))} and {nm(max(bps))}. Bar {line_bars('Bridge', 4)[0] + 1} is silent: everyone out. \"Here I am\" ({', '.join(nm(n['midi']) for n in b4)}) comes in bar {barno(b4[0]['on'])}. \"Speak, I'm listening\" ({', '.join(nm(n['midi']) for n in b5)}) holds \"-ing\" on {nm(b5[-1]['midi'])} over D, open, into the last chorus.\n")
A(f"## Last chorus (bars {span('Last Chorus')})\n"); A(table("Last Chorus"))
A(f"\nEverything open: guitar strumming eighths, the strings high, the kit with sticks, harmony on every line. \"And I won't call it the wind\" answers the first verse. \"Here I am, here I am\" climbs like the hook, {', '.join(nm(n['midi']) for n in v('Last Chorus', 6))}. The last line, \"Speak, I'm listening\" ({', '.join(nm(n['midi']) for n in lc7)}), comes down and lands on G over G: the first time the song comes home.\n")
A(f"## Outro (bars {span('Outro')})\n\nThe guitar picking over held strings, softer each bar; the last bar a G chord, let ring.\n")
A("# For each player\n")
A(f"**Voice.** A baritone, {vlo} to {vhi}. Sing the verses as if telling one person a family story: no push. Open up at the chorus, and lean on the held \"asking\"; it should feel unfinished. In the bridge come right down to almost speaking. \"Speak, I'm listening\" twice: the first held open on D, the second, the song's last, landing on G.\n")
A(f"**Harmony vocals.** Two parts, one above and one below, on the hooks in every chorus and on every line of the last chorus (high {nm(min(n['midi'] for n in R['harm_hi']))}–{nm(max(n['midi'] for n in R['harm_hi']))}, low {nm(min(n['midi'] for n in R['harm_lo']))}–{nm(max(n['midi'] for n in R['harm_lo']))}). Blend under the lead.\n")
A(f"**Acoustic guitar** ({rng_('guitar')}). Steel-string, fingerpicked in the intro, verses and outro (thumb on the root and fifth on the beats, fingers on the upper chord notes between). Strum quarters in the first two choruses and eighths in the last; out in the bridge.\n")
A(f"**Piano** ({rng_('piano')}). The hook's figure in the intro; answers at the end of each bar in verse 2; half-note chords in the choruses; alone in the bridge, low and close, and silent in its ninth bar.\n")
A(f"**Strings** ({rng_('strings')}). Low pads in chorus 1, higher in chorus 2; in softly from the bridge's fifth bar, swelling into the last chorus; open and high in the last chorus; held under the outro.\n")
A(f"**Acoustic bass** ({rng_('bass')}). In halfway through verse 1; root on every chord change, walking lightly between; out in the bridge; back for the last chorus; a last low G in the outro.\n")
A("**Drums.**\n\n- *Verse 1, intro, outro:* out.\n- *Chorus 1:* brushes: kick soft on 1 and 3, rim on 2 and 4, ride in quarters; a soft crash on 1.\n- *Verse 2:* brushes on the rim.\n- *Chorus 2:* brushes, snare on 2 and 4, ride in eighths.\n- *Bridge:* out; a ride swell in its last two beats into the last chorus.\n- *Last chorus:* sticks: kick on 1, the and of 2, and 3; snare on 2 and 4; ride in eighths; crash on 1.\n")
A("# Arrangement\n")
A("The song is a door opening a little at a time. The verses keep to the guitar and the voice so the story stays close. Each chorus adds a layer, and the hook never resolves. The bridge takes almost everything away, then takes away the rest for a bar, so \"Here I am\" is sung into real silence. The last chorus is the first time the whole band plays, and its last note is the first time the melody comes home.\n")
A("# Production notes\n")
A("## Lyric sheet with bar numbers\n")
A("| Bar | Line |\n|---|---|")
for (s, i), ns in by.items():
    if s == "Chorus 2":
        if i == 0: A(f"| {span('Chorus 2')} | (chorus) |")
        continue
    A(f"| {barno(ns[0]['on'])} | {WORDS[s][i]} |")
A('\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n')
A("## Producer one-sheet\n")
A("**The emotional target.** Honest wonder, not certainty. The verses are a quiet confession; the chorus is a question asked out loud; the bridge is a prayer without proof; the last line is an answer of trust, not a victory.\n")
A("**The three references.**\n")
A("- **Gregory Alan Isakov, \"The Stable Song\"** (*That Sea, the Gambler*, 2007): fingerpicked guitar and a low, close voice; later reworked with the Colorado Symphony. Take the picking and the intimacy of the verse.\n- **Josh Garrels, \"Farther Along\"** (*Love & War & The Sea in Between*, 2011): folk with a hopeful, spiritual pulse and acoustic and orchestral colour. Take the chorus's warmth and lift.\n- **Sufjan Stevens, \"Mystery of Love\"** (*Call Me by Your Name* soundtrack, 2017): a spare acoustic ballad. Take the restraint and the space around the voice in the bridge.\n")
A("**The dynamic arc.**\n")
A("| Section | Bars | Level | What changes |\n|---|---|---|---|")
for lab, s1, lv, wh in (("Intro", "Intro", "p", "guitar alone; the hook's figure on piano"), ("Verse 1", "Verse 1", "p → mp", "guitar and voice; bass in halfway"),
                        ("Chorus 1", "Chorus 1", "mf", "strum, piano, low strings, brushes"), ("Verse 2", "Verse 2", "mp", "piano answers, brushes on the rim"),
                        ("Chorus 2", "Chorus 2", "mf+", "strings higher, snare"), ("Bridge", "Bridge", "pp → silence → mp", "piano alone; a bar of silence; strings swell"),
                        ("Last chorus", "Last Chorus", "f", "everything open; sticks; harmony on every line"), ("Outro", "Outro", "p", "guitar and held strings, fading")):
    A(f"| {lab} | {span(s1)} | {lv} | {wh} |")
A(f"\n**The non-negotiables.** The held, unresolved \"asking\" on {nm(hk[-1]['midi'])}. The bar of silence before \"Here I am.\" \"Speak, I'm listening\" held open on {nm(b5[-1]['midi'])} in the bridge and landing on G at the very end. Nothing louder than the last chorus.\n")
A("**The mix priorities.** The voice close and dry enough to hear every word of the verses. The guitar's picking clear (left of centre), the piano right. Strings as air, never a wall, until the last chorus. In the bridge's silent bar, no reverb tail should fill the gap.\n")
A('\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n')
A("## Production brief\n")
A("*The song.* A folk song about a man raised to believe the world was silent who begins to hear it asking a question, and answers with a prayer rather than a proof.\n")
A("*References* (checked by search):\n")
A("- **Gregory Alan Isakov, \"The Stable Song.\"** Track 2 of *That Sea, the Gambler* (self-released, 2007), 6:00; later on *Gregory Alan Isakov with the Colorado Symphony* (2016).\n- **Josh Garrels, \"Farther Along.\"** From *Love & War & The Sea in Between* (Small Voice Records, 2011), Christianity Today's album of the year for 2011.\n- **Sufjan Stevens, \"Mystery of Love.\"** From the *Call Me by Your Name* soundtrack (2017), produced by Thomas Bartlett; an acoustic ballad, 4:08; nominated for the Academy Award for Best Original Song.\n")
A("*Non-negotiables.* As on the one-sheet.\n")
A("## Session notes\n")
A(f"- **Tempo and click.** ♩ = {R['qbpm']} throughout, 4/4; the click in quarters.\n- **Key.** G major. The flat seventh (F) appears as a passing note in the bridge.\n- **Chords per bar.** As in the section tables; most bars hold one chord, some two (two beats each).\n- **Range.** Voice {vlo}–{vhi}; harmony as above.\n- **Tracking.** Guitar and a guide vocal to the click first; then bass, piano and strings; then drums (brushes; sticks for the last chorus); the lead vocal; the harmonies with the finished lead in the headphones.\n- **Blend and panning.** Voice centre; guitar left of centre, piano right; strings wide; bass and kick centre; harmonies slightly left and right.\n- **The silent bar.** Bar {line_bars('Bridge', 4)[0] + 1}, the bridge's ninth: every track silent; cut reverb tails before it.\n")
A("## Score and parts\n")
A("- Lead sheet: voice, words and chord symbols (PDF).\n- Full score: every part on one set of systems (PDF).\n- Parts: harmony vocals (high, low), acoustic guitar, piano, strings, acoustic bass and drums (PDF).\n- Number chart (PDF).\n- MusicXML: the lead sheet and the full score (.musicxml and .mxl).\n- Demo: MP3 and a General MIDI file.\n")
open("/home/claude/p59/songbook.md", "w").write("\n".join(o) + "\n")
subprocess.run(["pandoc", "/home/claude/p59/songbook.md", "--reference-doc=/home/claude/carol/songbook/ref.docx", "-o", "/home/claude/p59/out/The World Is Asking - songbook.docx"], check=True)
print("ok")
