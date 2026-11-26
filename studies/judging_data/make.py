"""studies/judging_data: the covers study's inputs, for the nightly judging research to read. python3 studies/judging_data/make.py
Needs, on the maintainer's machine: the Sheet Sage data (git clone https://github.com/chrisdonahue/sheetsage-data into /home/claude/chrisdonahue) or the one file https://raw.githubusercontent.com/chrisdonahue/sheetsage-data/main/hooktheory/Hooktheory.json.gz (sha256 917b7cd58f5f4e07d6c36acf7bfad958c99ee05472dab3555399141094698e0c),
and /home/claude/shape/{hooktheory_surprise,hooktheory_rhythm,hooktheory_covers_discogs}.json as rebuilt by the scripts named in README.md."""
import os, json, gzip
HERE = os.path.dirname(os.path.abspath(__file__)); SH = "/home/claude/shape"
COV = json.load(open(f"{SH}/hooktheory_covers_discogs.json")); D = json.load(gzip.open("/home/claude/chrisdonahue/sheetsage-data/hooktheory/Hooktheory.json.gz")); clips = {}
for k, c in D.items():
    vid = (c.get("youtube") or {}).get("id")
    if vid in COV:
        a = c["annotations"]; clips[k] = dict(video=vid, artist=c["hooktheory"]["artist"], song=c["hooktheory"]["song"], num_beats=a.get("num_beats"), meters=a.get("meters"), keys=a.get("keys"), melody=a.get("melody"), harmony=a.get("harmony"))
def gz(name, obj):
    with gzip.GzipFile(os.path.join(HERE, name), "wb", mtime=0) as f: f.write(json.dumps(obj, separators=(",", ":"), sort_keys=True).encode())
gz("hooktheory_clips.json.gz", dict(credit="Hooktheory TheoryTab annotations as released with Sheet Sage (Donahue, Thickstun & Liang, ISMIR 2022; github.com/chrisdonahue/sheetsage-data), CC BY-NC-SA 3.0. Reduced to the clips of the songs matched to a Discogs-VI group; per clip: the YouTube video id, the Hooktheory artist and song slugs, metre, key, melody and harmony as released. No audio, no alignment.", clips=clips))
gz("hooktheory_surprise.json.gz", json.load(open(f"{SH}/hooktheory_surprise.json"))); gz("hooktheory_rhythm.json.gz", json.load(open(f"{SH}/hooktheory_rhythm.json")))
json.dump(COV, open(os.path.join(HERE, "hooktheory_covers_discogs.json"), "w"), sort_keys=True, separators=(",", ":"))
print(len(clips), "clips of", len({c["video"] for c in clips.values()}), "songs;", len(COV), "songs with a Discogs-VI group")
