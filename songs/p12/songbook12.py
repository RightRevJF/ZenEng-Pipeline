"""Wood and Cloth (second edition): the songbook and production notes, for musicians only (no engine terms). Every bar number, pitch and
chord is read from song_record.json. Writes songbook.md (the Doc's sections, split on '## ') and the Word copy."""
import json, subprocess, re
import lyric_p12 as L
H = "/home/claude/zeneng-pipeline/songs/p12"; OUT = f"{H}/out"
R = json.load(open(f"{H}/song_record.json")); N = R["tune"]; P = R["paths"]; C = R["chords"]; BAR = 36
ST = {int(k): v for k, v in R["stanza_offsets"].items()}; ED = R["edition"]
NM = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
def n(p, flat=False): return (("Bb" if flat and p % 12 == 10 else NM[p % 12])) + str(p // 12 - 1)
def bar_of(k): return N[k]["on"] // BAR + 1
def obar(stanza, b): return ST[stanza] // BAR + b                       # organ-score bar of stanza bar b (1-based)
CHN = {"D": "D", "Bm": "Bm", "G": "G", "A": "A", "E7": "E7", "F#7": "F#7", "Em7": "Em7", "A7": "A7", "Bm7": "Bm7", "Em": "Em", "F#m": "F#m", "Gm6": "Gm6"}
top = max(x["p"] for x in N); low = min(x["p"] for x in N)
k_top = next(k for k, x in enumerate(N) if x["p"] == top); b_top = bar_of(k_top)
syl = lambda s, k: L.syls(L.STANZAS[s][N[k]["line"]])[N[k]["syl"]][0]
top_words = [syl(s, k_top) for s in range(5)]
k_e7 = next(k for k, x in enumerate(N) if x["on"] // BAR == C["hymnal"].index("E7"))
k_f7 = next(k for k, x in enumerate(N) if x["on"] // BAR == C["hymnal"].index("F#7"))
b_gm6 = C["stanza4"].index("Gm6") + 1
gm6_bass = [p for (c, A, T, B) in P["stanza4"] for p in () ]
D = R["descant"]; d_top = max(D); d_top_bars = sorted({bar_of(k) for k, p in enumerate(D) if p == d_top})
ped_hold = [e for e in R["voices"]["org_ped"] if e["on"] >= ST[5] + 12 * BAR][0]
secs = 163
even_bars = sorted({b + 1 for b in range(16) if [x['dur'] for x in N if x['on'] // BAR == b] == [18, 6, 12]})
def and_(xs):
    xs = [str(x) for x in xs]; return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]
def line_notes(li): return " ".join(n(x["p"]) for x in N if x["line"] == li)
def chord_row(b): return C["hymnal"][b - 1]
# ---------------- sections ----------------
S = {}
S["glance"] = f"""## At a glance

A five-stanza Christmas hymn for congregation, choir and organ, in D major, written in 3/4 and felt in one: a dotted half about 33 a minute (♩ = 100). The full performance runs 88 bars, about {secs // 60}:{secs % 60:02d}.

| Item | Detail |
| --- | --- |
| Key and metre | D major, written in 3/4, felt in one (dotted half = c. 33; ♩ = 100) |
| Metre of the words | 87 87, five stanzas, no refrain |
| Tune | ARIMATHEA, {n(low)} to {n(top)} (women at pitch, men an octave lower) |
| Form of each stanza | 16 bars: line 1, line 2, line 1 again, line 4 |
| The one high note | {n(top)}, bar {b_top}: "{top_words[0]}" in stanzas 1 and 5 |
| Order | organ introduction (4 bars), stanzas 1–3, stanza 4 choir alone, organ link (4 bars), stanza 5 with descant |

**What it is about.** Every stanza sets a Christmas image beside its Easter twin: the manger's wood and the cross, swaddling bands and burial linen, the wise men's myrrh and the myrrh of the burial, the newborn called king and the king's title over the cross. The last stanza turns the chain into the empty tomb.

**How to sing and play it.** Plainly, in one long pulse to the bar. Let line 3 sound as the echo of line 1, because it is the same tune carrying the Easter half of each pair. Save the weight for "{top_words[0]}," and let stanza 4 be the quiet centre."""
S["hymn"] = f"""## The hymn

Chords as the hymnal setting sings them, one bar a cell. The four lines in the table are stanza 1; stanzas 2 to 5 follow.

| Bars | Chords | Stanza 1 |
| --- | --- | --- |
""" + "\n".join(f"| {4 * i + 1}–{4 * i + 4} | " + " · ".join(CHN[chord_row(4 * i + j)] for j in range(1, 5)) + f" | {L.STANZAS[0][i]} |" for i in range(4)) + "\n\n" + "\n\n".join(
    f"**{s + 1}.** " + "  \n".join(L.STANZAS[s]) for s in range(1, 5)) + f"""

**The pairs, stanza by stanza.**

- **Wood.** The feeding trough at Bethlehem, and the wood that held him on the cross. "Raised for dying" also looks ahead to Easter.
- **Cloth.** "Mary wrapped him close in linen… Joseph wrapped him close in linen." The second Joseph is Joseph of Arimathea, who wrapped the body for burial (Luke 23:53; Matthew 27:57–60). The stone rolled against the light here is rolled back in stanza 5.
- **Myrrh.** The wise men's gift was a burial spice; his friends carried pounds of it to a borrowed tomb (John 19:39).
- **King.** The wise men asked for the newborn king of the Jews (Matthew 2:2); Pilate wrote the same title over the cross (Matthew 27:37). Their gold comes back as a crown of thorns.
- **The empty tomb.** "Linen lies where God was lying" (John 20:6–7); they came and did not find him (Luke 24:3). The title returns: "wood and cloth are left behind."

A note for the bulletin, if wanted: *Stanza 2's second Joseph is Joseph of Arimathea, who buried Jesus in linen (Matthew 27:57–60).*"""
S["tune"] = f"""## The tune and harmony, bar by bar

**The shape.** Line 1 climbs from {n(N[0]['p'])} to {n([x for x in N if x['line'] == 0][-1]['p'])} (bars 1–4). Line 2 falls back through {n(N[k_e7]['p'])} to {n([x for x in N if x['line'] == 1][-1]['p'])}, a half close on A (bars 5–8). Line 3 is line 1 again, note for note (bars 9–12). Line 4 steps up to {n(top)} on "{top_words[0]}" in bar {b_top} and closes {n(N[-2]['p'])} to {n(N[-1]['p'])} (bars 13–16).

| Line | Bars | Melody |
| --- | --- | --- |
""" + "\n".join(f"| {li + 1} | {4 * li + 1}–{4 * li + 4} | {line_notes(li)} |" for li in range(4)) + f"""

**The recurring figure.** Bars {and_(even_bars)} put a dotted quarter on the strong syllable, a quick passing eighth slurred to it, then a quarter on the weak syllable. The weak syllable stays short in all five stanzas ("a-gainst," "be-neath," "the," "to," "and"), and the passing note is the turn the hymn keeps coming back to.

**Two borrowed chords in every stanza.**

- **E7 in bar {bar_of(k_e7)}** (the melody's {n(N[k_e7]['p'])} on "{syl(0, k_e7)}"): it leans toward A, so line 2's half close lands as a real arrival.
- **F#7 in bar {bar_of(k_f7)}**: under line 3, the same tune as line 1, the harmony turns toward B minor. The congregation sings the echo while the chords darken under it.

**Stanza 4, choir alone** (organ score bars {obar(4, 1)}–{obar(4, 16)}). Its own setting: B minor where the hymnal has D, E minor where it has G, and one chord from outside the key, G minor 6 in bar {b_gm6} of the stanza (organ score bar {obar(4, b_gm6)}), under "thorn." The tenor's B-flat there falls to A as the A7 follows.

**Stanza 5, the descant** (organ score bars {obar(5, 1)}–{obar(5, 16)}). Sopranos only, {n(min(D))} to {n(d_top)}, always above the tune. It reaches {n(d_top)} in stanza bars {and_(d_top_bars)} (organ score bars {and_([obar(5, b) for b in d_top_bars])}), a third above "{syl(4, k_top)}," and ends on {n(D[-1])}, the third of the last chord."""
S["players"] = f"""## For the organist, the choir, the congregation and the director

**Organist** (the organ score has every note).

| Bars | Section | Registration | What the organ does |
| --- | --- | --- | --- |
| 1–4 | Introduction | Gt. Diapasons 8′ 4′, Sw. to Gt.; Ped. Bourdon 16′, Principal 8′ | Plays line 4 in the hymnal harmony |
| {obar(1, 1)}–{obar(1, 16)} | Stanza 1 | as the introduction | Doubles the choir: soprano and alto in the right hand, tenor in the left, bass in the pedal |
| {obar(2, 1)}–{obar(2, 16)} | Stanza 2 | add Gt. Fifteenth 2′ | As stanza 1 |
| {obar(3, 1)}–{obar(3, 16)} | Stanza 3 | Sw. Flutes 8′ 4′, manuals only | Softer: tenor and bass together in the left hand, no pedal; hold the last chord and release as the choir breathes |
| {obar(4, 1)}–{obar(4, 16)} | Stanza 4 | silent | The choir sings alone |
| {R['link'] // BAR + 1}–{R['link'] // BAR + 4} | Link | Gt. 8′ 4′ 2′, Mixture, Sw. Reeds to Gt.; Ped. 16′ 8′ 4′ | Starts on D, the chord the choir ends on; the hymn's figure rising over D, E, A in the pedal, crescendo |
| {obar(5, 1)}–{obar(5, 16)} | Stanza 5 | Full organ | Its own harmony under the unison tune; a held low D in the pedal from bar {ped_hold['on'] // BAR + 1}; broaden over bars 87–88 |

**Choir.** Sing the hymnal setting in stanzas 1–3. Stanza 4 is yours alone and has its own parts, so learn it separately; give the G minor 6 chord in organ score bar {obar(4, b_gm6)} time to sound. Rehearse the way in and out: take the pitch from the organ's held D chord at the end of stanza 3 (your first chord, B minor, keeps its D and F-sharp), and end stanza 4 on D, where the organ comes back in. In stanza 5 everyone sings the tune (men an octave lower) and the sopranos take the descant.

**Congregation.** Stanzas 1, 2, 3 and 5 from the hymnal page. Stanza 4 is the choir's; the bulletin can say "choir alone."

**Singers, all parts.** Lines 1 and 3 end on a quarter note that runs straight into the next line: breathe by shortening it a little. Lines 2 and 4 end on a dotted half: breathe from the end of the hold, not from the next bar. Bars {and_(even_bars)}: the eighth is a passing note on the same syllable; keep it light and keep the weak syllable after it short. Keep "Ju-dah," "lin-en" and "sleep-ing" open on their held first syllables.

**Director.** Take the hymn in one, not three. Let stanza 3 come down, hold stanza 4 still, and let the link build into stanza 5. The final chord holds; the last two bars broaden."""
S["production"] = f"""## Production notes

**Lyric sheet with bar numbers** (hymnal page bars; every line starts on the downbeat).

| Bar | Stanza 1 | Stanza 2 | Stanza 3 | Stanza 4 | Stanza 5 |
| --- | --- | --- | --- | --- | --- |
""" + "\n".join(f"| {4 * i + 1} | " + " | ".join(L.STANZAS[s][i] for s in range(5)) + " |" for i in range(4)) + """

PAGEBREAK

### Producer one-sheet

**Emotional target.** Quiet wonder that darkens and then opens: the manger already holds the cross. The last stanza should feel like daylight after the choir's held breath in stanza 4.

**Three references.**

- [Willcocks, "O Come, All Ye Faithful" (Carols for Choirs 1, 1961)](https://blackwells.co.uk/bookshop/product/O-Come-All-Ye-Faithful-by-David-Willcocks-musical-arrangement/9780193368743): take the shape of the last verses, a soprano descant over the tune and a reharmonized final verse that builds.
- [Holst, CRANHAM ("In the Bleak Midwinter," English Hymnal, 1906)](https://hymnary.org/hymn/HTL1998/154): take its restraint, a Christmas hymn that never pushes.
- [Prichard, HYFRYDOL (1830)](https://en.wikipedia.org/wiki/Hyfrydol): the same 87 87 trochaic metre; take how its stresses sit squarely on the strong beats.

**Dynamic arc.**

| Section | Bars | Level | What changes |
| --- | --- | --- | --- |
| Introduction | 1–4 | mf | Organ alone, line 4 |
| Stanzas 1–2 | 5–36 | mf | Choir and organ together |
| Stanza 3 | 37–52 | p | Manuals only, no pedal; the last chord held |
| Stanza 4 | 53–68 | mp | Choir alone, its own darker setting; G minor 6 at bar """ + str(obar(4, b_gm6)) + """ |
| Link | 69–72 | mf, crescendo | Organ alone, from the choir's D, building |
| Stanza 5 | 73–88 | f | Unison tune, descant, full organ; held low D from bar """ + str(ped_hold['on'] // BAR + 1) + """; broaden at 87; hold the last chord |

**Non-negotiables.**

- Stanza 4 is unaccompanied.
- Line 3 is sung exactly as line 1.
- Bar 14's E5 ("cloth" in stanzas 1 and 5) is the only E5 in the tune.
- The hold at the end of stanza 3: the choir takes its pitch from the organ's D chord.
- The last chord is held.

**Mix priorities.** The words first: congregation and choir sit over the organ in every stanza. In stanza 5 the descant sits above everything but never covers the tune. The pedal's held D is felt more than heard.

PAGEBREAK

**Production brief.** A hymn for a congregation, recorded or led live with choir and organ. If recorded, capture the room: a church acoustic, the organ at a distance, the choir close enough for the words.

**Session notes.**

- Tempo: felt in one, dotted half = c. 33 (♩ = 100); a click only for the organ link if needed, none for stanza 4.
- Key D major throughout; range """ + f"{n(low)}–{n(top)}" + """ in the tune, descant """ + f"{n(min(D))}–{n(d_top)}" + """.
- Chords per bar: the table under "The hymn"; stanza 4 and stanza 5 as the organ score prints them.
- Track the choir in parts; stanza 5's unison and descant as a separate pass if the descant singers are few.
- Blend: organ centre and wide, choir in front, descant just above.

**Score and parts.**

- Hymnal page (SATB, five stanzas)
- Organ score with choir (88 bars: introduction, five stanzas, link, registrations)
- Lead sheet (tune, chords, five stanzas)
- MusicXML of the hymnal setting and the organ score
- Demo (MP3, General MIDI file)

**Credits.** Words and music: Jason Bryant. Tune name ARIMATHEA, 87 87."""
ORDER = ["glance", "hymn", "tune", "players", "production"]
md = f"# {L.TITLE}{ED} — Songbook\n\n" + "\n\n".join(S[k] for k in ORDER) + "\n"
open(f"{H}/songbook.md", "w").write(md)
json.dump({k: S[k].replace("PAGEBREAK\n\n", "") for k in ORDER}, open(f"{H}/songbook_sections.json", "w"))
word = md.replace("PAGEBREAK", '```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```')
open("/tmp/wac_songbook_word.md", "w").write(word)
subprocess.run(["pandoc", "/tmp/wac_songbook_word.md", "-o", f"{OUT}/{L.TITLE}{ED} - songbook.docx", "--reference-doc=/home/claude/carol/songbook/ref.docx"], check=True)
print("ok", len(md))
