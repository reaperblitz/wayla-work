import re, json, html as ihtml, requests
from datetime import date

CHANNEL_HANDLE = "@waylasciencelab357"
CHANNEL_ID = "UCAgk4f96GrNCEHC9mIPRJVg"
UPLOADS = "UU" + CHANNEL_ID[2:]
HEADERS = {"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.9"}

def fetch(url):
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.text

print("Fetching playlist...")
pl_html = fetch(f"https://www.youtube.com/playlist?list={UPLOADS}")
print("Fetching channel...")
ch_html = fetch(f"https://www.youtube.com/{CHANNEL_HANDLE}")
print("Fetching shorts tab...")
sh_html = fetch(f"https://www.youtube.com/{CHANNEL_HANDLE}/shorts")

def parse_playlist_videos(pl_html):
    parts = pl_html.split('"lockupViewModel"')
    videos = []
    for chunk_raw in parts[1:]:
        chunk = chunk_raw[:40000]
        idm = re.search(r'"contentId"\s*:\s*"([A-Za-z0-9_-]{11})"', chunk)
        if not idm:
            continue
        vid = idm.group(1)
        tm = re.search(r'"title"\s*:\s*\{\s*"content"\s*:\s*"((?:[^"\\]|\\.)+?)"', chunk)
        title = tm.group(1) if tm else ""
        try:
            title = json.loads(f'"{title}"')
        except:
            pass
        dm = re.search(r'"thumbnailBadgeViewModel"\s*:\s*\{\s*"text"\s*:\s*"([^"]+)"', chunk)
        dur = dm.group(1) if dm else ""
        # views / age
        views, age = "", ""
        for mm in re.finditer(r'"text"\s*:\s*\{\s*"content"\s*:\s*"([^"]{1,60})"\s*\}\s*,\s*"accessibilityLabel"\s*:\s*"([^"]{1,120})"', chunk):
            label = mm.group(2).lower()
            if "view" in label:
                views = mm.group(1)
            if any(k in label for k in ["ago","hour","day","week","month","year","minute","second"]):
                age = mm.group(1)
        videos.append({"id": vid, "title": title, "duration": dur, "views": views, "age": age,
                       "url": f"https://www.youtube.com/watch?v={vid}"})
    # de-dupe preserve order
    seen, out = set(), []
    for v in videos:
        if v["id"] not in seen:
            seen.add(v["id"]); out.append(v)
    return out

def parse_shorts_ids(sh_html):
    ids = []
    for chunk_raw in sh_html.split("shortsLockupViewModel")[1:]:
        m = re.search(r'"videoId"\s*:\s*"([A-Za-z0-9_-]{11})"', chunk_raw[:6000])
        if m and m.group(1) not in ids:
            ids.append(m.group(1))
    return set(ids)

def parse_channel_meta(ch_html):
    meta = {}
    m = re.search(r'"pageTitle"\s*:\s*"([^"]+)"', ch_html)
    meta["name"] = m.group(1) if m else "Wayla Science Lab"
    # subscribers + video count from header metadata
    # e.g. "content":"61 subscribers" and "content":"54 videos"
    subs = re.search(r'"content"\s*:\s*"([\d.,KMB]+ subscribers)"', ch_html)
    meta["subs"] = subs.group(1) if subs else ""
    vc = re.search(r'"content"\s*:\s*"(\d+ videos)"', ch_html)
    meta["video_count_label"] = vc.group(1) if vc else ""
    # description preview
    dm = re.search(r'"descriptionPreviewViewModel".{0,500}?"content"\s*:\s*"([^"]{0,500})"', ch_html, re.S)
    meta["desc_short"] = dm.group(1) if dm else "entertainment"
    # channelId
    meta["channel_id"] = CHANNEL_ID
    meta["handle"] = CHANNEL_HANDLE
    meta["url"] = f"https://www.youtube.com/{CHANNEL_HANDLE}"
    return meta

videos = parse_playlist_videos(pl_html)
shorts_ids = parse_shorts_ids(sh_html)
meta = parse_channel_meta(ch_html)
print(f"videos={len(videos)} shorts_tab={len(shorts_ids)} meta={meta}")

# save raw json for audit
with open("wayla_raw.json","w",encoding="utf-8") as f:
    json.dump({"meta":meta,"videos":videos,"shorts_ids":sorted(shorts_ids)},f,ensure_ascii=False,indent=1)

def dur_to_sec(d):
    if not d: return 0
    # can be "15:49", "0:16", "1:02:03", "SHORTS" etc
    d=d.strip()
    if not re.match(r'^[\d:]+$',d): return 0
    p=[int(x) for x in d.split(":")]
    s=0
    for x in p: s=s*60+x
    return s

for v in videos:
    v["secs"]=dur_to_sec(v["duration"])
    v["is_short_id"]=v["id"] in shorts_ids
    v["format"]="Shorts" if (v["is_short_id"] or (0 < v["secs"] <= 60)) else ("Long-form" if v["secs"]>60 else "Unknown/Private")

def views_to_num(s):
    if not s: return 0
    s=s.strip().replace(",","")
    m=re.match(r'([\d.]+)([KMB]?)',s)
    if not m: return 0
    n=float(m.group(1)); suf=m.group(2)
    return int(n*{"":1,"K":1000,"M":1000000,"B":1000000000}[suf])

for v in videos:
    v["views_num"]=views_to_num(v["views"])

# content-type categorization (rule-based, transparent)
def categorize(t):
    tl=t.lower()
    if "attack on all wayla" in tl or "attack on all wayla" in tl.replace("atack","attack"):
        return "Attack on All Wayla — original series"
    if tl.startswith("attack on all wayla") or "attack on all wayla" in tl or "atack on all wayla" in tl:
        return "Attack on All Wayla — original series"
    if tl.startswith("reacting"):
        return "Reaction / commentary (friends + own series)"
    if any(k in tl for k in ["99 nights","capybara","chess","roblox"]):
        return "Gaming (Roblox / chess / 99 Nights)"
    if any(k in tl for k in ["backroom","looping the rooms","rooms"]):
        return "Backrooms / Rooms skits"
    if any(k in tl for k in ["birthday","channel is","i'm back","im back","hi guys"]):
        return "Vlog / channel updates (birthday, anniversary, comeback)"
    if any(k in tl for k in ["moonwalk","michael","billie jean","michael deerson"]):
        return "Michael Jackson / moonwalk tributes"
    if any(k in tl for k in ["magic trick","llamapie","fall from the sky"]):
        return "Short skits / effects"
    if any(k in tl for k in ["meme","funny","frontman","helpmemakethismakesense","bluey"]):
        return "Memes / trends"
    return "Random / experimental shorts (early era)"

for v in videos:
    v["content_type"]=categorize(v["title"])

from collections import Counter
type_counts=Counter(v["content_type"] for v in videos)
format_counts=Counter(v["format"] for v in videos)
print(type_counts, format_counts)

# Save enriched
with open("wayla_videos.json","w",encoding="utf-8") as f:
    json.dump(videos,f,ensure_ascii=False,indent=1)
print("saved json")
