import json, re
from fpdf import FPDF, XPos, YPos
from collections import Counter
from datetime import date

videos = json.load(open("wayla_videos.json", encoding="utf-8"))
meta = json.load(open("wayla_raw.json", encoding="utf-8"))["meta"]

def clean(s):
    if s is None: return ""
    s = str(s)
    s = re.sub(r'[\u2068\u2069\u2066\u2067\u200b\u200c\u200d\ufeff\u200e\u200f\u202a\u202b\u202c\u202d\u202e]', '', s)
    s = s.replace('\U0001f480', '[skull]')
    out = ""
    for ch in s:
        o = ord(ch)
        if o > 0xFFFF:
            out += "?"
        else:
            out += ch
    out = re.sub(r'\s+', ' ', out).strip()
    return out

def mc(pdf, w, h, txt, **kw):
    kw.setdefault("new_x", XPos.LMARGIN)
    kw.setdefault("new_y", YPos.NEXT)
    # shard long unbreakable tokens by inserting zero-width-ish spaces
    txt = re.sub(r'([^\s]{40})', r'\1 ', txt)
    pdf.multi_cell(w, h, txt, **kw)

def cell_nl(pdf, w, h, txt, **kw):
    kw.setdefault("new_x", XPos.LMARGIN)
    kw.setdefault("new_y", YPos.NEXT)
    pdf.cell(w, h, txt, **kw)

class PDF(FPDF):
    def header(self):
        if self.page_no() == 1: return
        self.set_font("ArialU", "", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, "Wayla Science Lab - Channel Content Audit  |  @waylasciencelab357",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)
    def footer(self):
        self.set_y(-15)
        self.set_font("ArialU", "", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Page {self.page_no()}/{self.pages_count}  |  Generated {date.today().isoformat()}  |  Public data only",
                  align="C")

pdf = PDF(orientation="P", unit="mm", format="A4")
pdf.set_auto_page_break(True, margin=18)
pdf.add_font("ArialU", "", r"C:\Windows\Fonts\arial.ttf")
pdf.add_font("ArialU", "B", r"C:\Windows\Fonts\arialbd.ttf")

# COVER
pdf.add_page()
pdf.ln(22)
pdf.set_font("ArialU", "B", 26)
pdf.set_text_color(20, 20, 20)
mc(pdf, 0, 12, "Wayla Science Lab\nChannel Content Audit", align="C")
pdf.ln(4)
pdf.set_font("ArialU", "", 12)
pdf.set_text_color(60, 60, 60)
mc(pdf, 0, 7, f"https://www.youtube.com/{meta['handle']}\nChannel ID: {meta['channel_id']}", align="C")
pdf.ln(6)
pdf.set_fill_color(242, 242, 242)
pdf.set_font("ArialU", "B", 12)
cell_nl(pdf, 0, 10, f"  {clean(meta['subs'])}  |  {len(videos)} uploads found  |  Header: {clean(meta['video_count_label'])}", align="C", fill=True)
pdf.ln(4)
pdf.set_font("ArialU", "", 11)
pdf.set_text_color(20, 20, 20)
mc(pdf, 0, 6.5,
    "Scope: log all content types on the channel. NOTE: despite the name, this is NOT a science channel. "
    "Description is literally \"entertainment\". Content is gaming, original mini-series, reactions, skits, memes and vlogs, "
    "dominated by vertical Shorts.\n\n"
    "Client goals (provided): 100 subscribers this month (Oct 2026); long-term YouTube monetisation.\n"
    f"Baseline at audit ({date.today().isoformat()}): {clean(meta['subs'])} (39 to go to 100).")
pdf.ln(4)
pdf.set_font("ArialU", "", 9)
pdf.set_text_color(90, 90, 90)
mc(pdf, 0, 5.5,
    "Method: public uploads playlist UUAgk4f96GrNCEHC9mIPRJVg, Videos tab, Shorts tab, channel header. "
    "No login, no private analytics. Views/ages are YouTube-rounded public values. "
    "One entry (Today is my freaking birthday) has no duration / 0 views and looks unavailable/private - listed for completeness.")

# 1. SNAPSHOT
pdf.add_page()
pdf.set_text_color(20, 20, 20)
pdf.set_font("ArialU", "B", 16)
cell_nl(pdf, 0, 10, "1. Channel snapshot")
pdf.set_font("ArialU", "", 10)
rows = [
    ("Channel name", "Wayla Science Lab"),
    ("Handle / URL", f"{meta['handle']}  |  {meta['url']}"),
    ("Channel ID", meta["channel_id"]),
    ("Subscribers (public)", clean(meta["subs"])),
    ("Videos (header label)", clean(meta["video_count_label"])),
    ("Uploads found in playlist", str(len(videos))),
    ("Description", clean(meta["desc_short"])),
    ("Niche (actual)", "Entertainment / gaming / original comedy series - NOT science"),
]
for k, v in rows:
    pdf.set_font("ArialU", "B", 10)
    pdf.cell(52, 7, clean(k)+":", new_x=XPos.END, new_y=YPos.TOP)
    pdf.set_font("ArialU", "", 10)
    pdf.multi_cell(138, 7, clean(v), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.ln(3)
pdf.set_font("ArialU", "B", 13)
cell_nl(pdf, 0, 9, "Format split")
pdf.set_font("ArialU", "", 10)
fc = Counter(v["format"] for v in videos)
mc(pdf, 0, 6.5,
    f"Shorts: {fc.get('Shorts',0)}  |  Long-form: {fc.get('Long-form',0)}  |  Unknown/Private: {fc.get('Unknown/Private',0)}\n"
    "Shorts = in Shorts tab OR duration <= 3:00 (YouTube Shorts allow up to 3 min). Longs are 3:01-34:32. "
    "Channel is Shorts-led by volume (~84%), but recent 2 weeks show a push into 15-35 min longs.")

pdf.ln(2)
pdf.set_font("ArialU", "B", 13)
cell_nl(pdf, 0, 9, "Top 5 by public views (all-time, Shorts)")
pdf.set_font("ArialU", "", 9.5)
top5 = sorted(videos, key=lambda x: x.get("views_num", 0), reverse=True)[:5]
for i, t in enumerate(top5, 1):
    mc(pdf, 0, 6, f"{i}. {clean(t['title'])}  [{clean(t['duration'])} | {clean(t['views'])} views | {clean(t['age'])}]  https://youtu.be/{t['id']}")

# 2. TAXONOMY
pdf.add_page()
pdf.set_font("ArialU", "B", 16)
pdf.set_text_color(20, 20, 20)
cell_nl(pdf, 0, 10, "2. Content taxonomy (10 types logged)")
pdf.set_font("ArialU", "", 9.5)
mc(pdf, 0, 6, "Rule-based grouping from titles + format. Counts sum to 55 uploads found (incl. 1 unavailable). Examples are literal titles.")
pdf.ln(2)

taxonomy = [
    ("Random / experimental shorts", 24, "Early era 1-3y ago: human, i love you all, castrol (3.6K, channel best), help me (856), Im 10 (1.4K), lockjaw, how did i, single-word titles, test posts."),
    ("Attack on All Wayla - series", 10, "Numbered eps: atack on all wayla, attack 2 (67), 4 (14), 8+add moonwalk christmas (30), 9 part1-3 (32/22/21), 10, 11, 12 part1 (18 each). Core IP, 0:15-0:48 vertical."),
    ("Vlog / channel updates", 5, "Today is my birthday 30:00 (12), Today is my freaking birthday (unavailable), Hi guys 3:01 (8), Im back 0:16 (15), My channel is 4 yrs old now 34:32 (15)."),
    ("Gaming (Roblox/chess)", 3, "99 nights again 32:16 (185, best recent long), golden capybara Statue part1 23:04 (80), chess with @MuhahaBoston 9:22 (23, collab)."),
    ("Short skits / effects", 3, "Magic trick 0:16 (15), Llamapie2928 0:13 (1.8K), Fall from the sky 0:16 (2.1K). Effects-driven, 2 of top-5 all-time."),
    ("Memes / trends", 3, "#memes #funny #helpmemakethismakesense #frontman, bro front man, #bluey #funny #bingo. Hashtag-stuffed, 22-38 views."),
    ("Reaction x Attack crossover", 2, "Reacting to my friend part 2 + more ep of attack on all wayla 18:22 (5), Reacting to my series attack on all wayla 16:01 (6)."),
    ("MJ / moonwalk tributes", 2, "michael deerson #michaeljackson #michaelmovie #moonwalk 0:35 (318), Billie jean #moonwalk 0:21 (1.4K)."),
    ("Backrooms / Rooms skits", 2, "Looping the rooms 0:44 (20), backroom dance full vid 0:17 (24). 5 mo ago pair."),
    ("Reaction / commentary", 1, "Reacting to my friends part 3 15:49 (3, 2d ago). Newest long, friends-reaction format."),
]
pdf.set_fill_color(30, 30, 30)
pdf.set_text_color(255, 255, 255)
pdf.set_font("ArialU", "B", 9.5)
pdf.cell(62, 8, "  Content type", fill=True, new_x=XPos.END, new_y=YPos.TOP)
pdf.cell(14, 8, "Count", align="C", fill=True, new_x=XPos.END, new_y=YPos.TOP)
pdf.cell(0, 8, "  What it looks like / examples", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_text_color(20, 20, 20)
pdf.set_font("ArialU", "", 9)
fill = False
for name, cnt, desc in taxonomy:
    pdf.set_fill_color(245, 245, 245) if fill else pdf.set_fill_color(255, 255, 255)
    pdf.cell(62, 7, "  "+clean(name), fill=True, new_x=XPos.END, new_y=YPos.TOP)
    pdf.cell(14, 7, str(cnt), align="C", fill=True, new_x=XPos.END, new_y=YPos.TOP)
    x = pdf.get_x()
    w = pdf.w - pdf.r_margin - x
    pdf.multi_cell(w, 7, clean(desc), fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    fill = not fill

pdf.ln(3)
pdf.set_font("ArialU", "B", 12)
cell_nl(pdf, 0, 8, "What this means (factual, no plan yet)")
pdf.set_font("ArialU", "", 10)
mc(pdf, 0, 6.2,
    "- Two eras: 2023-2024 random/meme shorts seeding (views 20-60 typical, outliers to 3.6K) -> 2025-2026 focused IP: Attack series + gaming longs + reactions.\n"
    "- Last 30 days: 7 uploads (3 longs 15-34 min + 4 shorts). Longs 3-185 views; shorts 14-80 views except Idk what is gonna happen (1.1K, 1 mo ago).\n"
    "- Best watch-time assets now are longs (99 nights 32:16, capybara 23:04); best reach assets are old shorts (castrol, Fall from the sky, Llamapie2928).")

# 3. FULL CATALOG (landscape)
pdf.add_page(orientation="L")
pdf.set_font("ArialU", "B", 14)
pdf.set_text_color(20, 20, 20)
cell_nl(pdf, 0, 9, f"3. Full catalog - {len(videos)} uploads (newest first, as in uploads playlist)")
pdf.set_font("ArialU", "", 8.5)
pdf.set_text_color(80, 80, 80)
mc(pdf, 0, 5, "Views/ages are public rounded values at audit time. Duration blank = unavailable/private. Links are youtu.be short links.")
pdf.set_text_color(20, 20, 20)
pdf.ln(1)
cols = [("No", 10), ("Title", 95), ("Type", 52), ("Fmt", 18), ("Dur", 14), ("Views", 14), ("Age", 16), ("Link", 58)]
def catalog_header():
    pdf.set_fill_color(30, 30, 30)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("ArialU", "B", 8)
    for h, w in cols:
        pdf.cell(w, 7, h, align="C", fill=True, new_x=XPos.END, new_y=YPos.TOP)
    pdf.ln()
    pdf.set_text_color(20, 20, 20)
    pdf.set_font("ArialU", "", 7.5)
catalog_header()
fill = False
for i, v in enumerate(videos, 1):
    if pdf.get_y() > 185:
        pdf.add_page(orientation="L")
        catalog_header()
    pdf.set_fill_color(245, 245, 245) if fill else pdf.set_fill_color(255, 255, 255)
    title = clean(v["title"]) or "(untitled / blank)"
    if len(title) > 110: title = title[:107] + "..."
    ctype = clean(v["content_type"])
    if len(ctype) > 34: ctype = ctype[:31] + "..."
    pdf.cell(cols[0][1], 6, str(i), align="C", fill=True, new_x=XPos.END, new_y=YPos.TOP)
    pdf.cell(cols[1][1], 6, " "+title, fill=True, new_x=XPos.END, new_y=YPos.TOP)
    pdf.cell(cols[2][1], 6, " "+ctype, fill=True, new_x=XPos.END, new_y=YPos.TOP)
    pdf.cell(cols[3][1], 6, clean(v["format"])[:6], align="C", fill=True, new_x=XPos.END, new_y=YPos.TOP)
    pdf.cell(cols[4][1], 6, clean(v["duration"]), align="C", fill=True, new_x=XPos.END, new_y=YPos.TOP)
    pdf.cell(cols[5][1], 6, clean(v["views"]), align="C", fill=True, new_x=XPos.END, new_y=YPos.TOP)
    pdf.cell(cols[6][1], 6, clean(v["age"]), align="C", fill=True, new_x=XPos.END, new_y=YPos.TOP)
    pdf.cell(cols[7][1], 6, f"youtu.be/{v['id']}", align="C", fill=True, new_x=XPos.END, new_y=YPos.TOP)
    pdf.ln()
    fill = not fill

pdf.add_page(orientation="P")
pdf.set_font("ArialU", "B", 14)
cell_nl(pdf, 0, 9, "4. Notes & limits")
pdf.set_font("ArialU", "", 10)
mc(pdf, 0, 6.2,
    "Sources: uploads playlist UUAgk4f96GrNCEHC9mIPRJVg (55 lockups incl. 1 unavailable), header (61 subs / 54 videos label), "
    "Shorts tab (44 shortsLockup IDs), Videos tab. Fetched Oct 2026 via public web endpoints.\n\n"
    "Counts: header says 54 videos but playlist yields 55 entries (54 playable + 1 unavailable Today is my freaking birthday, 2y ago). "
    "Use 54 playable as working total; discrepancy is likely caching/private status.\n\n"
    "Views like 1.1K/3.6K are YouTube abbreviations, not exact. Ages like 1mo ago are relative.\n\n"
    "Not a science channel: name is legacy/misleading. Do not pitch as educational science; audience signals are gaming, original animation/skits, reactions, memes.\n\n"
    "Next step (awaiting your brief): goal-gap to 100 subs (+39), and monetisation prerequisites (1,000 subs + 4,000 watch hours or 10M Shorts views) - needs a content + posting plan. Tell me what to do next.")
out = "Wayla-Science-Lab_Content-Audit.pdf"
pdf.output(out)
print(f"saved {out}")
