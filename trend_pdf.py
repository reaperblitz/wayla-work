import json, re
from fpdf import FPDF, XPos, YPos
from datetime import date

def clean(s):
    if s is None: return ""
    s = str(s)
    s = re.sub(r'[\u2068\u2069\u2066\u2067\u200b\u200c\u200d\ufeff\u200e\u200f\u202a\u202b\u202c\u202d\u202e\u2060]', '', s)
    s = s.replace('\U0001f480', '[skull]')
    out = ""
    for ch in s:
        if ord(ch) > 0xFFFF: out += "?"
        else: out += ch
    return re.sub(r'\s+', ' ', out).strip()

def mc(pdf, w, h, txt, **kw):
    kw.setdefault("new_x", XPos.LMARGIN); kw.setdefault("new_y", YPos.NEXT)
    txt = re.sub(r'([^\s]{45})', r'\1 ', txt)
    pdf.multi_cell(w, h, txt, **kw)

def cell_nl(pdf, w, h, txt, **kw):
    kw.setdefault("new_x", XPos.LMARGIN); kw.setdefault("new_y", YPos.NEXT)
    pdf.cell(w, h, txt, **kw)

class PDF(FPDF):
    def header(self):
        if self.page_no() == 1: return
        self.set_font("ArialU", "", 8); self.set_text_color(100,100,100)
        self.cell(0, 6, "Wayla Science Lab - Trend Analysis Oct 2026 | 1 human + 2 machine ideas",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)
    def footer(self):
        self.set_y(-15); self.set_font("ArialU", "", 8); self.set_text_color(120,120,120)
        self.cell(0, 10, f"Page {self.page_no()}/{self.pages_count} | {date.today().isoformat()} | public trend data, no private analytics", align="C")

pdf = PDF("P", "mm", "A4")
pdf.set_auto_page_break(True, margin=18)
pdf.add_font("ArialU", "", r"C:\Windows\Fonts\arial.ttf")
pdf.add_font("ArialU", "B", r"C:\Windows\Fonts\arialbd.ttf")

# COVER
pdf.add_page(); pdf.ln(18)
pdf.set_font("ArialU","B",26); pdf.set_text_color(20,20,20)
mc(pdf,0,12,"Wayla Science Lab\nTrend Analysis\nOct 2026",align="C")
pdf.ln(3)
pdf.set_font("ArialU","",11); pdf.set_text_color(60,60,60)
mc(pdf,0,6.5,"Shitpost-first / informal only | Hates: Brainrot + Verity (excluded)\nGoal: 100 subs this month (61 now, +39) -> monetisation later",align="C")
pdf.ln(4)
pdf.set_fill_color(242,242,242); pdf.set_font("ArialU","B",11); pdf.set_text_color(20,20,20)
cell_nl(pdf,0,9,"  RESULT: 1 HUMAN video + 2 MACHINE / ANIMATOR videos - only 3, to ship before trends die",align="C",fill=True)
pdf.ln(3)
pdf.set_font("ArialU","",10)
mc(pdf,0,6.2,"This file = complete trend summary (videos + trends observed Oct 1-12, 2026) + 3 picked ideas with scripts. "
"Why only 3: Shorts trends live 7-21 days. Halloween dies Nov 1. Mandem / Buggin peaked Oct 1-7. "
"Shipping 3 fast beats planning 10 slow.")

# PART 1 TRENDS
pdf.add_page()
pdf.set_font("ArialU","B",16); pdf.set_text_color(20,20,20)
cell_nl(pdf,0,10,"1. Complete trend analysis (Oct 1-12, 2026)")
pdf.set_font("ArialU","",9.5); pdf.set_text_color(60,60,60)
mc(pdf,0,5.5,"Sources: TikTok Creative Center trackers, YT Shorts reports Oct 2026, Roblox charts Oct 12, Fortnite Fortnitemares schedule, meme DB. All public. Lifespan notes included.")
pdf.ln(2)

clusters = [
 ("A. Halloween reveals (PEAK NOW, dies Nov 1)",
  "Ramalama Costume Walk: low shoes walk -> lift reveal on R. Murphy Ramalama (Bang Bang). 430.7K videos on sound (Oct 5), ~50.5M views on 6 vids Sep 29-Oct 4. 7-15s, no talking.\n"
  "Pumpkin Head Illusion: real pumpkin near lens = friend head, friend dances. Zero edit, hocus-pocus remix.\n"
  "Also: Things You Should Definitely Ghost (sheet holds signs), Be OK (happy dance + chaos caption), costume transitions (hand-swipe), pet pumpkin / hot-dog. NRF 2026: witch/vampire/Batman/Spider-Man/ghost lead; pets: pumpkin.\n"
  "Window: post Oct 29-31 Fri-Sat peak. Halloween Sat this year = 2-day runway."),
 ("B. AI photo-to-video templates (PEAK NOW, 7-14 day cycle)",
  "Formula: 1-2 photos -> finished video, CapCut / Higgsfield Genjutsu. No filming.\n"
  "Rumpelstiltskin tiptoe (Tip Toe Wing In My Jawwdinz): 900K in 1 week, 65K-follower repost account in days. Swap imp for anyone.\n"
  "Burning Bridges (Drake dinner): #burningbridgesai 748 vids / 2M views Oct 7-10. 1 photo = you host party. 15-25s.\n"
  "Alors on danse (keyboard + hype man), Gas Station Dance (3-photo group), APT pink studio, Toc Toc line, Smalltown Boy scream duo, Hotel Lobby Migos, AI Arrest Filter (not bro getting arrested again). 59 posts/52 creators in 72h Oct 1.\n"
  "Cost: $2-7 per 15s (Higgsfield) or free CapCut. Must label AI. Original ranks higher since Oct 1 YT change."),
 ("C. Dance / sound memes (PEAK / EARLY FADE)",
  "Mandem Style (Luke Day drill Gangnam remix ching dat mandem style): Sasuke shrug sync. Template 2.3M views 1st week (Sep 26), 650K 2nd edit, 800K cooking gag Oct 2. Accuracy reenactments 230K.\n"
  "Baby You Buggin (Khantrast Genius Sep 30): 1.2M / 1M / 335K Oct 3-5. POV caption meme.\n"
  "Six Seven funk (Seis Sete): 75M single (J-Hope). Slayyyter posing dances = equal to choreo now.\n"
  "Rule: 5-11s steady views, ~60s breakout watch-time. Use trending sound in first 2s (+21% reach)."),
 ("D. Gaming events (EVERGREEN + SEASONAL BOOST)",
  "Fortnitemares Oct 1-Nov 1: FNAF Day 1, Freddy Krueger boss Day 2, Black Clover, Hollow Knight, Reload Nightmare Island Oct 8, 99 Nights Deer skin Oct 10, Beetlejuice/Hazbin/Purge/Slenderman rolling. 26 Nitemare quests -> free skin.\n"
  "Roblox Oct 12: Steal An Egg 1.9M, Brookhaven, 99 Nights in the Forest 347K players / 30B visits / 90% likes, updated Oct 7. Adopt Me Halloween 252K, Dandy World 94K.\n"
  "Wayla tie: his 99 nights again 32:16 (185 views) is his top recent long. 99 Nights x Fortnite cross = perfect bridge."),
 ("E. Anime edits + comedy containers (STEADY)",
  "Sasuke / Naruto vs Sasuke rapid-cut edits, Minato edits (128K likes). POV yellow-text relationships, I asked ChatGPT to lie (horse neigh), ceiling-fan wipe outfits, geometric horror (one strong joke), StudyTok 5-sec homework gag.\n"
  "Avoid per Wayla: Folk Valley / Only-in-Ohio absurd + Steal a Brainrot + Italian brainrot = BRAINROT. Bunker vs Verity / Crack Verity / verity-explainers = VERITY. All excluded from ideas below."),
]
pdf.set_text_color(20,20,20)
for title, body in clusters:
    pdf.set_font("ArialU","B",11)
    cell_nl(pdf,0,7.5,title)
    pdf.set_font("ArialU","",9.5)
    mc(pdf,0,5.5,body)
    pdf.ln(2)

# PART 2 IDEAS
pdf.add_page()
pdf.set_font("ArialU","B",16)
cell_nl(pdf,0,10,"2. The 3 picks - 1 human, 2 machine")
pdf.set_font("ArialU","",10)
mc(pdf,0,6,"Picked for: <1hr work, fits shitpost + Attack IP + Halloween + 99 Nights, no Brainrot/Verity, loopable, postable by Oct 31.")
pdf.ln(2)

pdf.set_fill_color(27,133,27); pdf.set_text_color(255,255,255); pdf.set_font("ArialU","B",12)
cell_nl(pdf,0,9,"  IDEA 1 - HUMAN: Pumpkin Head Attack (phone, friend, pumpkin)",fill=True)
pdf.set_text_color(20,20,20); pdf.set_font("ArialU","",10)
mc(pdf,0,6,
 "Concept: Attack on All Wayla Halloween special as Pumpkin Head Illusion. You hold real pumpkin near lens, friend (or MuhahaBoston) 3m behind dances as Attack character. 0:12, no edit.\n"
 "Hook 0-1s: pumpkin fills frame + on-screen: attack on all wayla 13.\n"
 "Shots: (1) 0-3s pumpkin close, friend hidden (2) 3-10s friend flails / moonwalk (Wayla MJ tie) (3) 10-12s drop pumpkin -> reveal face + Attack roar.\n"
 "Sound: hocus-pocus spooky remix (same as trend) OR Ramalama whisper. Film golden hour.\n"
 "Title: attack on all wayla 13 pumpkin head #halloween #attackonallwayla #shorts\n"
 "Why Wayla: uses 10-ep core IP (18-32 views base) + #1 Halloween format (zero edit) + MJ dance callback. Human-only charm = original boost Oct 1 algo.\n"
 "Ship: film 20 min, post Oct 29-31 7pm. Success = 3x median shorts views (~60+) + 2 subs. If pops, part 2 with Backrooms skin.")
pdf.ln(2)

pdf.set_fill_color(30,80,180); pdf.set_text_color(255,255,255); pdf.set_font("ArialU","B",12)
cell_nl(pdf,0,9,"  IDEA 2 - MACHINE/ANIMATOR: Mandem Attack shrug loop (no camera)",fill=True)
pdf.set_text_color(20,20,20); pdf.set_font("ArialU","",10)
mc(pdf,0,6,
 "Concept: Animator redraws 1 Attack on All Wayla character doing Sasuke Mandem shrug, 3 frames, beat-synced to ching dat mandem style. 0:08 loop. No human filming.\n"
 "Spec for animator/CapCut: 9:16, 3-frame shoulder bounce on each syllable, white flash on drop (like Zany Emote burst), captions: ching dat mandem style. Export perfect loop (last frame = first).\n"
 "Hook: first shrug on beat 0.5s. Sound: Mandem Style original (Luke Day). Use Sound -> Use this sound.\n"
 "Title: attack on all wayla does mandem style #mandemstyle #sasuke #animeedit #shorts\n"
 "Why Wayla: anime-edit trend (2.3M template) + his IP, no filming, repostable as accuracy reenactment later with human. Animator 1-2h. Post Oct 15-25 before sound fades.\n"
 "Ship: send animator 1 front PNG of Attack character + this spec. Success = loop rate >120% avg view duration, 5 subs from anime crowd.")
pdf.ln(2)

pdf.set_fill_color(120,40,140); pdf.set_text_color(255,255,255); pdf.set_font("ArialU","B",12)
cell_nl(pdf,0,9,"  IDEA 3 - MACHINE/AI: Burning Bridges Attack dinner (1 photo)",fill=True)
pdf.set_text_color(20,20,20); pdf.set_font("ArialU","",10)
mc(pdf,0,6,
 "Concept: AI template puts Wayla (+MuhahaBoston) as hosts of Drake Burning Bridges dinner, guests = Attack on All Wayla cast. 0:15. 1 photo only.\n"
 "Steps (agency does it): 1 front photo Wayla, Higgsfield/CapCut Burning Bridges template, prompt: replace host, keep room/chandeliers/wave, Halloween horror guests. Enable TikTok/YT AI label. 10-min render, $0-7.\n"
 "Hook: Where she at? hand-over-eyes 0-2s. Caption: me at my birthday dinner after burning every bridge.\n"
 "Title: attack crew at drake dinner where she at #burningbridgesai #halloween #shorts\n"
 "Why Wayla: #burningbridgesai 2M/3 days Oct 7-10 = still rising Oct 12, two-person = tags Muhaha = subs, horror guests = Fortnitemares tie, zero shoot. Fits shitpost + collab history (chess 9:22).\n"
 "Ship: render 2 variants (Wayla solo, Wayla+Muhaha), post better one Oct 18-28. Success = comments naming guests + cross-post to community. If tool blocks copyright, fallback: AI Arrest Filter with Attack villain (same 1-photo flow).")

pdf.add_page()
pdf.set_font("ArialU","B",14)
cell_nl(pdf,0,9,"3. Posting rules (so trends don't fall off)")
pdf.set_font("ArialU","",10)
mc(pdf,0,6,
 "1) Order: HUMAN pumpkin (Oct 29-31) -> MACHINE mandem (ASAP, sound fading) -> MACHINE bridges (Oct 18-28). Actually render machines NOW, stagger posts.\n"
 "2) Length: 7-15s Halloween/AI, 8-20s dance. Captions on (80% viral use them), on-screen hook text (1.79x views), 10-25 cuts/min.\n"
 "3) Sound: Use This Sound from trend, first 2s. 11am / 7pm local, 1/day max, don't post over a surging video.\n"
 "4) No-no: no Brainrot audio/game, no Verity game/explainer, no re-upload w/o commentary (Oct 1 demotion), no delete-repost (spam), label AI.\n"
 "5) Goal math: 61 -> 100 = +39. Collab tags (Muhaha) + 99 Nights/Fortnite search + Halloween browse = 3 discovery pools. Track chose-to-view in Studio, double down on winner with 3-10 hook variants.\n\n"
 "Excluded deliberately: Rumpelstiltskin (needs 2-photo + creep fatigue), Folk Valley (brainrot-adjacent), Steal a Brainrot game (hate), Verity games, long vlogs (too slow for trend window). Save for Nov.")

out = "Wayla_Trend-Analysis_Oct2026.pdf"
pdf.output(out)
print(f"saved {out}")
