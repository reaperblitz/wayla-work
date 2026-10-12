import requests, re, json
H={"User-Agent":"Mozilla/5.0","Accept-Language":"en-US"}
pl=requests.get("https://www.youtube.com/playlist?list=UUAgk4f96GrNCEHC9mIPRJVg",headers=H,timeout=30).text
print("2oKOQ in playlist html?", "2oKOQdaThFA" in pl)
# check video page
v=requests.get("https://www.youtube.com/watch?v=2oKOQdaThFA",headers=H,timeout=30).text
m=re.search(r'"title"\s*:\s*"([^"]{5,150})"',v)
print("video page len",len(v),"title sample", (m.group(1)[:120] if m else "none"))
# shorts ids
sh=requests.get("https://www.youtube.com/@waylasciencelab357/shorts",headers=H,timeout=30).text
print("JH0PP in shorts?", "JH0PPafC7p0" in sh)
# check Hi guys duration on its watch page
m2=re.search(r'"lengthSeconds"\s*:\s*"(\d+)"',v)
print("lengthSeconds for 2oKO:", m2.group(1) if m2 else "not found")
w2=requests.get("https://www.youtube.com/watch?v=JH0PPafC7p0",headers=H,timeout=30).text
m3=re.search(r'"lengthSeconds"\s*:\s*"(\d+)"',w2)
print("lengthSeconds Hi guys:", m3.group(1) if m3 else "not found")
print("Hi guys isShorts in page?", "shorts" in w2[:100000].lower())
