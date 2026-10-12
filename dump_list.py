import json
v=json.load(open('wayla_videos.json',encoding='utf-8'))
for x in v:
    print(f"{x['duration']:>6} | {x['format']:9} | {x['views']:>6} | {x['age']:>8} | {x['title'][:90]} | {x['id']}")
print("---- by type ----")
from collections import Counter
print(Counter(x['content_type'] for x in v))
