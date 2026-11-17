"""Melody by genre: scale degrees, five-note scales, blue notes and the melodic-harmonic divorce in CoCoPops Billboard (214 songs with
melody, CC BY-NC 4.0; derived counts only), read from ../tension/cocopops_bars.json (made by ../tension/parse_cocopops.py).

Each sung onset gets: its degree above the bar's tonic (**harm key), the chord sounding at its onset (**harte), its section label, its decade,
and the next sung pitch. Families are a hand tagging by artist (FAMILY below), not a corpus field: soul/R&B/funk, country, and all others.

Measures, major-key bars unless stated:
  degree shares (onsets); per-song pentatonic fit (major pent 1 2 3 5 6, minor pent 1 b3 4 5 b7 on the tonic, the union);
  flat 3 and flat 7 rates and the chord under flat 3; where flat 3 goes next;
  the fix-200 case: a note outside the key's scale a semitone from a tone of the sounding chord and not itself a chord tone;
  the tri() case: a note a tritone from the sounding chord's root; non-chord tones and unresolved ones (next note not within 2 semitones),
  verse against chorus; 'minor melody over major harmony' songs (more flat 3 than 3 in major-key bars)."""
import json, sys, os, re, collections, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tension"))
from tension_features import parse_harte, key_info
HERE = os.path.dirname(os.path.abspath(__file__))
SOUL = """AlGreen AnitaBaker Commodores CorneliusBrothersAndSisterRose DavidRuffinAndJimmyRuffin DinahWashington EarthWindAndFire EdwinStarr
FatsDomino FontellaBass JamesBrown LaVernBaker KoolAndTheGang MarvinGaye OtisRedding RickJames StephanieMills TheMeters TheMiracles
TheRighteousBrothers JimmyReed TheRobertCrayBand TheShirelles TheRonettes TheChiffons TheCrystals""".split()
COUNTRY = """AnneMurray HankSnow JerryJeffWalker JohnDenver JohnnyCash JohnnyHorton JuiceNewton NittyGrittyDirtBand OakRidgeBoys RogerMiller
TheKendalls TheEverlyBrothers LindaRonstadt""".split()
def family(name):
    a = name.split("_")[0]
    return "soul" if a in SOUL else "country" if a in COUNTRY else "other"
MAJ = {0, 2, 4, 5, 7, 9, 11}; MINS = {0, 2, 3, 5, 7, 8, 10}
MPENT = {0, 2, 4, 7, 9}; mPENT = {0, 3, 5, 7, 10}; UNION = MPENT | mPENT
SEC = lambda l: "verse" if l and l.startswith(("Verse", ">Verse", "Preverse")) else "chorus" if l and l.startswith(("Chorus", "Refrain")) else "other"
def notes_of(song):
    """Sung onsets with key, chord at onset, section; ties merged into the note before."""
    out = []; ch = None
    for b in song["bars"]:
        K = key_info(b["key"]); spans = []; pos = 0.0
        for c in b["chords"]:
            q = c["q"] or 0.0; pc = parse_harte(c["harte"]); spans.append((pos, pos + q, pc)); pos += q
        pos = 0.0
        for n in b["notes"]:
            if n["p"] is not None and n["on"] and K:
                cur = ch
                for s0, s1, pc in spans:
                    if s0 <= pos + 1e-6 and pc is not None: cur = pc
                    if s0 > pos + 1e-6: break
                out.append(dict(p=n["p"], q=n["q"], K=K, ch=cur, sec=SEC(b["label"])))
            elif n["p"] is not None and out and not n["on"]: out[-1]["q"] += n["q"]
            pos += n["q"]
        if spans and spans[-1][2] is not None: ch = spans[-1][2]
    for i, n in enumerate(out): n["nxt"] = out[i + 1]["p"] if i + 1 < len(out) else None
    return out
def deg(n): return (n["p"] - n["K"]["tonic"]) % 12
def analyse(songs):
    R = dict(); G = collections.defaultdict(lambda: collections.Counter())
    per_song = []
    for name, s in songs.items():
        ns = notes_of(s)
        if len(ns) < 40: continue
        fam = family(name); yr = int(re.search(r"(\d{4})$", name).group(1)); dec = f"{(yr // 10) * 10}s"
        maj = [n for n in ns if not n["K"]["minor"]]
        if len(maj) < 0.6 * len(ns):
            per_song.append(dict(name=name, fam=fam, dec=dec, mode="minor", n=len(ns))); continue
        c = collections.Counter(deg(n) for n in maj); tot = sum(c.values())
        ps = dict(name=name, fam=fam, dec=dec, mode="major", n=tot,
                  mpent=sum(c[d] for d in MPENT) / tot, mpent_min=sum(c[d] for d in mPENT) / tot, union=sum(c[d] for d in UNION) / tot,
                  majscale=sum(c[d] for d in MAJ) / tot, b3=c[3] / tot, n3=c[4] / tot, b7=c[10] / tot, n7=c[11] / tot)
        # the fix-200 case and the tri() case
        f200 = tri = nct = nct_unres = 0; sec_c = collections.Counter(); b3ch = collections.Counter(); b3next = collections.Counter()
        f200_res = 0
        for n in maj:
            d = deg(n); ch = n["ch"]
            for key in (("all", fam), ("dec", dec), ("sec", n["sec"]), ("secfam", n["sec"] + "|" + fam)):
                G[key][d] += 1
            if ch is None: continue
            pc = n["p"] % 12; tones = set(ch["pcs"])
            is_ct = pc in tones
            if not is_ct:
                nct += 1; sec_c[n["sec"] + "_nct"] += 1
                if n["nxt"] is None or abs(n["nxt"] - n["p"]) > 2: nct_unres += 1; sec_c[n["sec"] + "_unres"] += 1
            sec_c[n["sec"]] += 1
            if d not in MAJ and not is_ct and any(((pc - t) % 12) in (1, 11) for t in tones):
                f200 += 1
                if n["nxt"] is not None and abs(n["nxt"] - n["p"]) <= 2: f200_res += 1
            if (pc - ch["root"]) % 12 == 6 and not is_ct: tri += 1
            if d == 3:
                rel = (ch["root"] - n["K"]["tonic"]) % 12
                lab = {0: "I", 5: "IV", 7: "V", 10: "bVII", 9: "vi", 2: "ii", 3: "bIII"}.get(rel, "other")
                if rel == 0 and ((n["K"]["tonic"] + 4) % 12) in tones: lab = "I (major third sounding)"
                b3ch[lab] += 1
                if n["nxt"] is not None:
                    dn = (n["nxt"] - n["K"]["tonic"]) % 12; step = n["nxt"] - n["p"]
                    b3next["down to 1 or 2" if step in (-1, -2, -3) and dn in (0, 2) else "up to 3" if step == 1 else
                           "up to 4 or 5" if step in (2, 4) else "repeat" if step == 0 else "leap"] += 1
        ps.update(f200=f200 / tot, f200_res=(f200_res / f200 if f200 else None), tri=tri / tot, nct=nct / tot, nct_unres=nct_unres / tot,
                  verse_nct=sec_c["verse_nct"] / max(1, sec_c["verse"]), chorus_nct=sec_c["chorus_nct"] / max(1, sec_c["chorus"]),
                  verse_unres=sec_c["verse_unres"] / max(1, sec_c["verse"]), chorus_unres=sec_c["chorus_unres"] / max(1, sec_c["chorus"]),
                  nverse=sec_c["verse"], nchorus=sec_c["chorus"], b3ch=dict(b3ch), b3next=dict(b3next))
        per_song.append(ps)
    return per_song, G
def share(c):
    t = sum(c.values()); return {d: round(c[d] / t, 4) for d in range(12)} if t else {}
def summarise(per_song, G):
    M = [p for p in per_song if p["mode"] == "major"]
    out = dict(songs=len(per_song), major=len(M), minor=len(per_song) - len(M),
               family_n=dict(collections.Counter(p["fam"] for p in M)))
    def med(xs): xs = [x for x in xs if x is not None]; return round(float(np.median(xs)), 4) if xs else None
    def mean(xs): xs = [x for x in xs if x is not None]; return round(float(np.mean(xs)), 4) if xs else None
    def q90(xs): xs = [x for x in xs if x is not None]; return round(float(np.percentile(xs, 90)), 4) if xs else None
    fams = {}
    for f in ("all", "soul", "country", "other"):
        S = M if f == "all" else [p for p in M if p["fam"] == f]
        fams[f] = dict(n=len(S),
            pent_fit_median=med([max(p["mpent"], p["mpent_min"]) for p in S]),
            share_songs_pent90=round(np.mean([max(p["mpent"], p["mpent_min"]) >= 0.9 for p in S]), 3),
            share_songs_union95=round(np.mean([p["union"] >= 0.95 for p in S]), 3),
            share_songs_majscale95=round(np.mean([p["majscale"] >= 0.95 for p in S]), 3),
            b3_mean=mean([p["b3"] for p in S]), b3_songs=round(np.mean([p["b3"] > 0.01 for p in S]), 3),
            b7_mean=mean([p["b7"] for p in S]), n7_mean=mean([p["n7"] for p in S]),
            b7_over_n7_songs=round(np.mean([p["b7"] > p["n7"] for p in S]), 3),
            minor_over_major_songs=round(np.mean([p["b3"] > p["n3"] for p in S]), 3),
            f200_per1000_mean=round(1000 * mean([p["f200"] for p in S]), 2), f200_songs=round(np.mean([p["f200"] > 0 for p in S]), 3),
            f200_per1000_q90=round(1000 * q90([p["f200"] for p in S]), 2), f200_resolved_by_step=mean([p["f200_res"] for p in S]),
            tri_per1000_mean=round(1000 * mean([p["tri"] for p in S]), 2), tri_songs=round(np.mean([p["tri"] > 0 for p in S]), 3),
            nct_mean=mean([p["nct"] for p in S]), nct_unres_mean=mean([p["nct_unres"] for p in S]))
    out["families"] = fams
    V = [p for p in M if p["nverse"] >= 30 and p["nchorus"] >= 30]
    out["verse_vs_chorus"] = dict(n=len(V), verse_nct=mean([p["verse_nct"] for p in V]), chorus_nct=mean([p["chorus_nct"] for p in V]),
        verse_unres=mean([p["verse_unres"] for p in V]), chorus_unres=mean([p["chorus_unres"] for p in V]),
        songs_verse_more_unres=round(np.mean([p["verse_unres"] > p["chorus_unres"] for p in V]), 3))
    b3c = collections.Counter(); b3n = collections.Counter()
    for p in M: b3c.update(p["b3ch"]); b3n.update(p["b3next"])
    out["b3_chord"] = {k: round(v / sum(b3c.values()), 3) for k, v in b3c.most_common()}; out["b3_n"] = sum(b3c.values())
    out["b3_next"] = {k: round(v / sum(b3n.values()), 3) for k, v in b3n.most_common()}
    out["degree_share"] = {"/".join(k): share(c) for k, c in G.items() if sum(c.values()) > 500}
    out["decades"] = {d: dict(n=len(S), b3_mean=mean([p["b3"] for p in S]), b7_mean=mean([p["b7"] for p in S]),
                              pent90=round(np.mean([max(p["mpent"], p["mpent_min"]) >= 0.9 for p in S]), 3),
                              f200_per1000=round(1000 * mean([p["f200"] for p in S]), 2))
                      for d in sorted({p["dec"] for p in M}) for S in [[p for p in M if p["dec"] == d]]}
    return out
def engine_song(xml):
    """Songs 54 and 55 lead sheets: the same measures, from MusicXML (melody and chord symbols)."""
    from music21 import converter, harmony, note
    sc = converter.parse(xml); part = sc.parts[0]
    k = sc.analyze("key") if not list(sc.recurse().getElementsByClass("KeySignature")) else None
    ks = list(sc.recurse().getElementsByClass("KeySignature"))[0].asKey("major") if k is None else k
    tonic = ks.tonic.pitchClass
    evs = sorted([(e.getOffsetInHierarchy(sc), e) for e in sc.recurse() if isinstance(e, (harmony.ChordSymbol, note.Note))], key=lambda x: x[0])
    ch = None; ns = []
    for off, e in evs:
        if isinstance(e, harmony.ChordSymbol): ch = {p.pitchClass for p in e.pitches}; root = e.root().pitchClass; chd = (ch, root); continue
        if e.tie is not None and e.tie.type in ("stop", "continue"): continue
        ns.append((e.pitch.midi, chd if ch else None))
    c = collections.Counter((p - tonic) % 12 for p, _ in ns); tot = sum(c.values())
    f200 = sum(1 for p, cd in ns if cd and ((p - tonic) % 12) not in MAJ and p % 12 not in cd[0] and any(((p % 12 - t) % 12) in (1, 11) for t in cd[0]))
    nct = sum(1 for p, cd in ns if cd and p % 12 not in cd[0])
    return dict(n=tot, key=str(ks), pent_fit=round(max(sum(c[d] for d in MPENT), sum(c[d] for d in mPENT)) / tot, 3),
                majscale=round(sum(c[d] for d in MAJ) / tot, 3), b3=round(c[3] / tot, 4), b7=round(c[10] / tot, 4), n7=round(c[11] / tot, 4),
                f200=f200, nct=round(nct / tot, 3), degree_share=share(c))
if __name__ == "__main__":
    songs = json.load(open(os.path.join(HERE, "..", "tension", "cocopops_bars.json")))
    per_song, G = analyse(songs)
    out = summarise(per_song, G)
    F = collections.Counter(); T = collections.Counter()
    for name, s in songs.items():
        for n in notes_of(s):
            if n["K"]["minor"] or n["ch"] is None: continue
            d = deg(n); pc = n["p"] % 12; t = set(n["ch"]["pcs"]); r = (n["ch"]["root"] - n["K"]["tonic"]) % 12
            if d not in MAJ and pc not in t and any(((pc - x) % 12) in (1, 11) for x in t): F[d] += 1
            if (pc - n["ch"]["root"]) % 12 == 6 and pc not in t: T[f"degree {d} over chord root {r}"] += 1
    out["f200_by_degree"] = {f"degree {k}": v for k, v in F.most_common()}
    out["tri_by_case"] = dict(T.most_common(10))
    out["engine"] = {}
    for lab, path in (("song 54", "/home/claude/p64/out/The Man Mama Prayed I'd Be - lead sheet.musicxml"),
                      ("song 55", "/home/claude/p65/out/Your Yard Man - lead sheet.musicxml")):
        try: out["engine"][lab] = engine_song(path)
        except Exception as ex: out["engine"][lab] = dict(error=str(ex))
    json.dump(out, open(os.path.join(HERE, "genre_results.json"), "w"), indent=1)
    json.dump(per_song, open(os.path.join(HERE, "genre_per_song.json"), "w"))
    print(json.dumps({k: v for k, v in out.items() if k != "degree_share"}, indent=1))
    for k in ("all/soul", "all/country", "all/other", "sec/verse", "sec/chorus"):
        if k in out["degree_share"]: print(k, {d: round(100 * x, 1) for d, x in out["degree_share"][k].items()})
