import requests, re
H={"User-Agent":"Mozilla/5.0","Accept-Language":"en-US"}
pl=requests.get("https://www.youtube.com/playlist?list=UUAgk4f96GrNCEHC9mIPRJVg",headers=H,timeout=30).text
idx=pl.find("2oKOQdaThFA")
print("idx",idx)
ctx=pl[max(0,idx-3000):idx+3000]
print(ctx[:4000])
print("----")
# find surrounding lockup
lidx=pl.rfind('"lockupViewModel"',0,idx)
print("lockup before distance",idx-lidx)
print(pl[lidx:lidx+6000][:6000])
