"""YouTube Data API v3 (key in /root/.secrets/youtube_key, never written elsewhere): for each Hooktheory video, its views, likes,
comments, upload date, duration and channel; then each channel's subscribers and video count. 50 ids a request (1 quota unit each).
Raw statistics stay in /home/claude/dl/shape/youtube (not the repository; YouTube's terms limit keeping them)."""
import json, os, time, urllib.request, urllib.parse
KEY = open("/root/.secrets/youtube_key").read().strip()
OUT = "/home/claude/dl/shape/youtube"; os.makedirs(OUT, exist_ok=True)
def get(endpoint, params):
    params = dict(params, key=KEY); url = f"https://www.googleapis.com/youtube/v3/{endpoint}?" + urllib.parse.urlencode(params)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=30) as r: return json.load(r)
        except Exception as e:
            err = e; time.sleep(2 * (attempt + 1))
    raise err
if __name__ == "__main__":
    clips = json.load(open("/home/claude/shape/hooktheory_surprise.json"))
    vids = sorted({c["vid"] for c in clips}); V = {}
    for i in range(0, len(vids), 50):
        d = get("videos", dict(part="statistics,snippet,contentDetails", id=",".join(vids[i:i + 50]), maxResults=50))
        for it in d.get("items", []):
            s = it.get("statistics", {}); sn = it.get("snippet", {})
            V[it["id"]] = dict(views=int(s["viewCount"]) if "viewCount" in s else None, likes=int(s["likeCount"]) if "likeCount" in s else None,
                               comments=int(s["commentCount"]) if "commentCount" in s else None, published=sn.get("publishedAt"), channel=sn.get("channelId"),
                               channel_title=sn.get("channelTitle"), duration=it.get("contentDetails", {}).get("duration"), category=sn.get("categoryId"))
        if i % 2000 == 0: print("videos", i, len(V), flush=True)
    chans = sorted({v["channel"] for v in V.values() if v["channel"]}); C = {}
    for i in range(0, len(chans), 50):
        d = get("channels", dict(part="statistics", id=",".join(chans[i:i + 50]), maxResults=50))
        for it in d.get("items", []):
            s = it.get("statistics", {})
            C[it["id"]] = dict(subscribers=int(s["subscriberCount"]) if s.get("subscriberCount") and not s.get("hiddenSubscriberCount") else None, videos=int(s.get("videoCount", 0)))
    json.dump(dict(videos=V, channels=C, fetched=time.strftime("%Y-%m-%d")), open(f"{OUT}/hooktheory_youtube.json", "w"))
    print("asked", len(vids), "found", len(V), "with views", sum(1 for v in V.values() if v["views"] is not None), "channels", len(C))
