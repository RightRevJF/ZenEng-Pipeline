"""The same readings on the engine's delivered songs 54 and 55 (lead-sheet MusicXML from songs/p64 and p65 out/, not in the repo):
section roles from rehearsal marks, chords from the chord symbols, the sung line, Lerdahl distance from the tonic, the dominant before each
chorus, the tonic and the melodic lift at chorus bar 1, and where the smoothed harmonic-tension curve peaks."""
import json, sys, numpy as np, music21 as m21
sys.path.insert(0, ".")
from tension_features import parse_harte, key_info, tonic_chord, delta
SONGS = {"54 The Man Mama Prayed I'd Be": ("/home/claude/p64/out/The Man Mama Prayed I'd Be - lead sheet.musicxml"),
         "55 Your Yard Man": ("/home/claude/p65/out/Your Yard Man - lead sheet.musicxml")}
def role(l):
    l = (l or "").lower()
    if "pre" in l and "chorus" in l: return "pre-chorus"
    for r in ("chorus", "verse", "bridge", "intro", "outro", "tag", "turnaround", "instrumental", "solo"):
        if r in l: return r
    return "other"
QMAP = {"major": "maj", "minor": "min", "dominant-seventh": "7", "major-seventh": "maj7", "minor-seventh": "min7", "diminished": "dim",
        "augmented": "aug", "suspended-fourth": "sus4", "suspended-second": "sus2", "half-diminished-seventh": "hdim7", "major-sixth": "maj6", "dominant-ninth": "9"}
out = {}
for name, path in SONGS.items():
    sc = m21.converter.parse(path); part = sc.parts[0]
    ks = sc.flatten().getElementsByClass(m21.key.KeySignature)
    k = sc.analyze("key") if not ks else ks[0].asKey("major")
    K = key_info(k.tonic.name.replace("-", "-") if k.mode == "major" else k.tonic.name.lower())
    T = tonic_chord(K); label = None; rows = []
    for meas in part.getElementsByClass(m21.stream.Measure):
        for rm in meas.getElementsByClass(m21.expressions.RehearsalMark): label = rm.content
        for te in meas.getElementsByClass(m21.expressions.TextExpression):
            if any(w in te.content.lower() for w in ("verse", "chorus", "bridge", "intro", "tag", "outro")): label = te.content
        chs = []
        for h in meas.getElementsByClass(m21.harmony.ChordSymbol):
            q = QMAP.get(h.chordKind, "maj"); ch = parse_harte(f"{h.root().name.replace('-', 'b')}:{q}")
            if ch: chs.append(ch)
        notes = [n for n in meas.notes if not isinstance(n, m21.harmony.ChordSymbol) and n.isNote]
        rows.append(dict(bar=meas.number, role=role(label), tps=float(np.mean([delta(T, c, K) for c in chs])) if chs else None,
                         dom=int(any((c["root"] - K["tonic"]) % 12 == 7 for c in chs)), ton=int(any((c["root"] - K["tonic"]) % 12 == 0 for c in chs)),
                         pitch=float(np.mean([n.pitch.midi for n in notes])) if notes else None))
    # carry chords across empty-symbol bars
    last = None
    for r in rows:
        if r["tps"] is None: r["tps"] = last
        else: last = r["tps"]
    Z = lambda key: (lambda v: (v - np.nanmean(v)) / (np.nanstd(v) or 1))(np.array([r[key] if r[key] is not None else np.nan for r in rows], float))
    zt, zp = Z("tps"), Z("pitch")
    by = {}
    for rl in ("intro", "verse", "pre-chorus", "chorus", "bridge", "tag", "turnaround"):
        idx = [i for i, r in enumerate(rows) if r["role"] == rl]
        if idx: by[rl] = dict(tps=round(float(np.nanmean(zt[idx])), 2), pitch=round(float(np.nanmean(zp[idx])), 2), bars=len(idx))
    starts = [i for i in range(1, len(rows)) if rows[i]["role"] == "chorus" and rows[i - 1]["role"] != "chorus"]
    appr = dict(dominant_last_bar_before=round(float(np.mean([rows[i - 1]["dom"] for i in starts])), 2) if starts else None,
                tonic_chorus_bar1=round(float(np.mean([rows[i]["ton"] for i in starts])), 2) if starts else None,
                pitch_z_chorus_bar1=round(float(np.nanmean([zp[i] for i in starts])), 2) if starts else None, choruses=len(starts))
    v = np.where(np.isnan(zt), 0, zt); sm = np.empty_like(v); acc = v[0]
    for i in range(len(v)): acc = 0.9 * acc + 0.1 * v[i]; sm[i] = acc
    lo = int(0.1 * len(sm)); pk = (lo + int(np.argmax(sm[lo:]))) / len(sm)
    out[name] = dict(key=f"{k.tonic.name} {k.mode}", bars=len(rows), by_role=by, approach=appr, harmonic_peak_position=round(pk, 2))
    print(name, json.dumps(out[name]))
json.dump(out, open("engine_songs_results.json", "w"), indent=1)
