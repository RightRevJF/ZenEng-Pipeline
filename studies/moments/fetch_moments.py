"""Moments people love: for a sample of the Hooktheory videos, the 100 most relevant top-level comments (one request each), reduced at
once to timestamps. Kept per timestamp: the video, the time in seconds, the comment's like count and keyword flags (chills, cry,
best part, this part, voice/high note, key change, bridge, drop/beat). No names, no comment text, nothing else is stored."""
import json, re, os, random, time, urllib.request, urllib.parse
KEY = open("/root/.secrets/youtube_key").read().strip(); OUT = "/home/claude/dl/shape/youtube"
TS = re.compile(r"(?<![\d:])(?:(\d{1,2}):)?(\d{1,2}):(\d{2})(?![\d:])")
FLAGS = {"chills": r"chill|goosebump|shiver|hair stand", "cry": r"\bcry|crying|tears|cried", "best": r"best part|favou?rite part|my part|the best",
         "this_part": r"this part|that part|this moment|this line", "voice": r"high note|that note|voice|vocal|falsetto|belt|range", "key_change": r"key change|modulat",
         "bridge": r"bridge", "drop": r"\bdrop\b|beat drop|the beat", "chorus": r"chorus|hook"}
def get(params):
    url = "https://www.googleapis.com/youtube/v3/commentThreads?" + urllib.parse.urlencode(dict(params, key=KEY))
    for a in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as r: return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (403, 404): return None                          # comments off, or quota
            time.sleep(2)
        except Exception: time.sleep(2)
    return None
if __name__ == "__main__":
    Y = json.load(open(f"{OUT}/hooktheory_youtube.json"))["videos"]
    pool = sorted(v for v, d in Y.items() if d["views"] and d["views"] >= 200000)
    random.seed(1115); sample = random.sample(pool, min(4000, len(pool)))
    done_path = f"{OUT}/moments.json"; M = json.load(open(done_path)) if os.path.exists(done_path) else {}
    calls = 0
    for i, vid in enumerate(sample):
        if vid in M: continue
        d = get(dict(part="snippet", videoId=vid, maxResults=100, order="relevance", textFormat="plainText")); calls += 1
        if d is None: M[vid] = None; continue
        out = []
        for it in d.get("items", []):
            s = it["snippet"]["topLevelComment"]["snippet"]; t = s.get("textOriginal") or ""
            for m in TS.finditer(t):
                sec = int(m.group(1) or 0) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
                if int(m.group(3)) >= 60: continue
                low = t.lower()
                out.append(dict(s=sec, likes=s.get("likeCount", 0), n_ts=len(TS.findall(t)), **{k: bool(re.search(p, low)) for k, p in FLAGS.items()}))
        M[vid] = out
        if i % 250 == 0:
            json.dump(M, open(done_path, "w")); print(i, "videos;", sum(len(v or []) for v in M.values()), "timestamps", flush=True)
    json.dump(M, open(done_path, "w"))
    print("videos", len(M), "with comments", sum(1 for v in M.values() if v is not None), "timestamps", sum(len(v or []) for v in M.values()), "calls", calls)
