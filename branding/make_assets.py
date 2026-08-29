"""Generate on-brand PNG assets (banner, og card, logo, favicon) matching
the site's terminal aesthetic: #0b0f14 bg, #2dd4a7 green, #38bdf8 cyan.
Run:  .venv\\Scripts\\python.exe branding\\make_assets.py
"""
from PIL import Image, ImageDraw, ImageFont
import math
import os

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..", "docs")
F = "C:/Windows/Fonts/consola.ttf"
FB = "C:/Windows/Fonts/consolab.ttf"

BG = (11, 15, 20)
GRID = (45, 212, 167, 14)
GREEN = (45, 212, 167)
CYAN = (56, 189, 248)
DIM = (91, 113, 134)
PANEL = (13, 20, 28)
BORDER = (30, 42, 56)
TEXT = (215, 226, 238)


def font(path, size):
    return ImageFont.truetype(path, size)


def draw_grid(img):
    d = ImageDraw.Draw(img, "RGBA")
    w, h = img.size
    step = 44
    for x in range(0, w, step):
        d.line([(x, 0), (x, h)], fill=GRID, width=1)
    for y in range(0, h, step):
        d.line([(0, y), (w, y)], fill=GRID, width=1)


def glow_orb(img, cx, cy, radius, color, alpha):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for r in range(radius, 0, -4):
        a = int(alpha * (1 - r / radius) ** 2)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color + (a,))
    img.alpha_composite(overlay)


def terminal_window(img, box, title):
    d = ImageDraw.Draw(img, "RGBA")
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, radius=14, fill=PANEL + (235,), outline=GREEN + (110,), width=2)
    # title bar
    d.rounded_rectangle([x0, y0, x1, y0 + 44], radius=14, fill=(15, 21, 29) + (255,))
    d.rectangle([x0, y0 + 26, x1, y0 + 44], fill=(15, 21, 29) + (255,))
    d.line([(x0, y0 + 44), (x1, y0 + 44)], fill=BORDER + (255,), width=1)
    # traffic lights
    for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
        cx = x0 + 26 + i * 24
        d.ellipse([cx - 7, y0 + 22 - 7, cx + 7, y0 + 22 + 7], fill=c + (255,))
    # title
    f = font(F, 20)
    d.text((x0 + 110, y0 + 12), title, font=f, fill=DIM + (255,))
    return y0 + 44


def center_text(d, cx, y, text, f, fill):
    w = d.textlength(text, font=f)
    d.text((cx - w / 2, y), text, font=f, fill=fill + (255,))


def banner():
    W, H = 1500, 500
    img = Image.new("RGBA", (W, H), BG + (255,))
    draw_grid(img)
    glow_orb(img, 120, 60, 420, GREEN, 26)
    glow_orb(img, W - 80, H - 40, 380, CYAN, 20)

    ybar = terminal_window(img, (250, 120, 1250, 420), "daniel@kali: ~")
    d = ImageDraw.Draw(img, "RGBA")
    cx = W / 2
    dim = DIM + (255,)
    center_text(d, cx, ybar + 48, ">_ CTF WRITE-UPS", font(FB, 64), GREEN)
    center_text(d, cx, ybar + 135, "HTB | THM | METHODOLOGY FIRST", font(F, 26), CYAN)
    d.text((300, ybar + 195), "$ nmap -sV --top-ports 1000 target.htb", font=font(F, 20), fill=dim)
    d.text((300, ybar + 225), "→ 22/tcp  ssh   OpenSSH 8.4", font=font(F, 20), fill=dim)
    d.text((300, ybar + 255), "→ 80/tcp  http  nginx 1.24", font=font(F, 20), fill=TEXT + (220,))
    d.text((300, ybar + 285), "→ [FLAG CAPTURED]", font=font(F, 20), fill=GREEN)
    out = os.path.join(HERE, "banner.png")
    img.convert("RGB").save(out)
    print("banner", img.size)


def og():
    W, H = 1200, 630
    img = Image.new("RGBA", (W, H), BG + (255,))
    draw_grid(img)
    glow_orb(img, 80, 40, 380, GREEN, 24)
    glow_orb(img, W - 60, H - 30, 340, CYAN, 18)
    ybar = terminal_window(img, (60, 70, 1140, 560), "daniel@kali: ~")
    d = ImageDraw.Draw(img, "RGBA")
    dim = DIM + (255,)
    d.text((110, ybar + 40), "$ whoami", font=font(F, 24), fill=dim)
    d.text((110, ybar + 85), "DANIEL DAYAN", font=font(FB, 72), fill=TEXT)
    d.text((110, ybar + 190), "ENTRY-LEVEL PENETRATION TESTER", font=font(FB, 32), fill=CYAN)
    d.text((110, ybar + 250), ">_ CTF WRITE-UPS — HACK THE BOX — TRYHACKME", font=font(F, 24), fill=GREEN)
    d.text((110, ybar + 300), "nmap  burp  metasploit  |  Security+ → PNPT → OSCP", font=font(F, 22), fill=dim)
    out = os.path.join(HERE, "og.png")
    img.convert("RGB").save(out)
    print("og", img.size)


def logo():
    S = 512
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img, "RGBA")
    glow_orb(img, S // 2, S // 2, S // 2, GREEN, 30)
    d.rounded_rectangle([16, 16, S - 16, S - 16], radius=90, fill=BG + (255,), outline=GREEN + (200,), width=4)
    f = font(FB, 210)
    w = d.textlength(">_", font=f)
    d.text(((S - w) / 2 - 24, S / 2 - 150), ">_", font=f, fill=GREEN + (255,))
    # cursor
    d.rectangle([S / 2 + 80, S / 2 + 20, S / 2 + 130, S / 2 + 80], fill=GREEN + (255,))
    out = os.path.join(HERE, "logo.png")
    img.save(out)
    print("logo", img.size)
    # favicon 32px
    fav = img.resize((32, 32), Image.LANCZOS)
    favout = os.path.join(ROOT, "favicon.png")
    fav.save(favout)
    print("favicon", fav.size, favout)


banner()
og()
logo()
print("done")
