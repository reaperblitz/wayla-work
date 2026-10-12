import json, re
from collections import Counter
from datetime import date

videos = json.load(open("wayla_videos.json", encoding="utf-8"))
meta = json.load(open("wayla_raw.json", encoding="utf-8"))["meta"]

# --- refine categories (ASCII-safe, no em-dash) ---
def categorize(t):
    tl = (t or "").lower()
    has_attack = ("attack on all wayla" in tl) or ("atack on all wayla" in tl)
    is_react = tl.startswith("reacting")
    if is_react and has_attack:
        return "Reaction x Attack crossover"
    if is_react:
        return "Reaction / commentary"
    if has_attack:
        return "Attack on All Wayla - original series"
    if any(k in tl for k in ["99 nights", "capybara", "chess", "roblox"]):
        return "Gaming (Roblox / 99 Nights / chess)"
    if any(k in tl for k in ["backroom", "looping the rooms", "rooms"]):
        return "Backrooms / Rooms skits"
    if any(k in tl for k in ["birthday", "channel is", "i'm back", "im back", "hi guys"]):
        return "Vlog / channel updates"
    if any(k in tl for k in ["moonwalk", "michael", "billie jean", "michael deerson"]):
        return "Michael Jackson / moonwalk tributes"
    if any(k in tl for k in ["magic trick", "llamapie", "fall from the sky"]):
        return "Short skits / effects"
    if any(k in tl for k in ["meme", "funny", "frontman", "helpmemakethismakesense", "bluey"]):
        return "Memes / trends"
    return "Random / experimental shorts"

for v in videos:
    v["content_type"] = categorize(v["title"])
    # fix format: shorts tab membership already in is_short_id; Shorts can be up to 3 min
    # keep existing format but ensure Hi guys 3:01 stays Shorts (it is in shorts tab)
    # Unknown stays Unknown
    pass

with open("wayla_videos.json", "w", encoding="utf-8") as f:
    json.dump(videos, f, ensure_ascii=False, indent=1)

type_counts = Counter(v["content_type"] for v in videos)
format_counts = Counter(v["format"] for v in videos)
print(type_counts)
print(format_counts)
print(f"total {len(videos)}")

# sort videos: newest first as in playlist order (already newest first)
# compute top performers
def vn(s):
    return s or 0
top = sorted(videos, key=lambda x: x.get("views_num", 0), reverse=True)[:5]
print("TOP5:")
for t in top:
    print(t["views"], t["title"], t["id"])
