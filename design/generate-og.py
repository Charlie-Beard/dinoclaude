#!/usr/bin/env python3
"""Generates assets/images/og-image.png for DinoClaude."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images', 'og-image.png')

BG     = (255, 251, 245)
TEXT1  = ( 18,  32,  51)
TEXT2  = ( 81,  96, 114)
TEXT3  = (138, 154, 176)
OR     = (212, 103,  61)
OR2    = (184,  85,  48)
DK     = ( 30,  10,   2)
BRICK1 = (143,  56,  32)
BRICK2 = (122,  46,  24)
MORTAR = ( 74,  26,   8)
GROUND = (219, 227, 238)

img = Image.new('RGB', (W, H), BG)
d   = ImageDraw.Draw(img, 'RGBA')

# ── Subtle dot-grid background texture ───────────────────────────────────────
for dot_x in range(10, W, 20):
    for dot_y in range(10, H, 20):
        d.ellipse([dot_x-1, dot_y-1, dot_x+1, dot_y+1], fill=(18, 32, 51, 9))

# Ground
d.rectangle([0, 510, W, 512], fill=GROUND)
d.rectangle([0, 512, W, H],   fill=(245, 239, 230, 110))

# ── Pixel-art mascot ─────────────────────────────────────────────────────────
# Exact game sprite from drawChar() in game.js, no additions.
# sq(bx, by, col, row, w, h) → fillRect(bx+col*P, by-(row+h)*P, w*P, h*P)
# P=16, bx=850, by=400  →  character bottom at y=400, ground at y=510 (110px airborne)

P  = 16
bx = 850
by = 400

def sq(col, row, w, h, color):
    x = bx + col * P
    y = by - (row + h) * P
    d.rectangle([x, y, x + w*P - 1, y + h*P - 1], fill=color)

sq(1, 9, 2, 2, OR)    # left ear
sq(5, 9, 2, 2, OR)    # right ear
sq(0, 3, 8, 6, OR)    # body
sq(0, 3, 8, 1, OR2)   # body: darker bottom strip
sq(1, 6, 2, 2, DK)    # left eye
sq(5, 6, 2, 2, DK)    # right eye
sq(1, 0, 2, 3, OR)    # left leg  (animF=0: forward, 3 rows)
sq(5, 1, 2, 2, OR2)   # right leg (animF=0: back,    2 rows)

# Jump shadow
shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ds = ImageDraw.Draw(shadow)
cx, cy, rx, ry = 914, 514, 58, 7
ds.ellipse([cx-rx, cy-ry, cx+rx, cy+ry], fill=(18, 32, 51, 18))
img.paste(Image.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, 0)), shadow).convert('RGB'), mask=shadow.split()[3])

# Motion lines (trailing left of character at bx=850)
for x1, x2, y, alpha in [
    (752, 826, 278, 90),
    (740, 825, 308, 62),
    (748, 826, 336, 42),
]:
    d.rectangle([x1, y, x2, y + 3], fill=OR + (alpha,))

# ── Brick wall ───────────────────────────────────────────────────────────────
# Matches game: BH=11, BG=2, BW=34 style, but scaled up for the OG image.
wall_x, wall_y, wall_w, wall_h = 1005, 315, 140, 195
BW, BH, BG = 44, 16, 3

# Mortar base
d.rectangle([wall_x, wall_y, wall_x + wall_w - 1, wall_y + wall_h - 1], fill=MORTAR)

row = 0
y   = wall_y
while y < wall_y + wall_h:
    offset = (BW // 2) if row % 2 == 1 else 0
    bh     = min(BH, wall_y + wall_h - y)
    x      = wall_x - offset
    while x < wall_x + wall_w:
        bxw   = max(x, wall_x)
        bwid  = min(x + BW, wall_x + wall_w) - bxw
        if bwid > 0 and bh > 0:
            fill = BRICK1 if row % 2 == 0 else BRICK2
            d.rectangle([bxw, y, bxw + bwid - 1, y + bh - 1], fill=fill)
            # Subtle top highlight on each brick
            d.rectangle([bxw, y, bxw + bwid - 1, y + min(2, bh - 1)], fill=OR2 + (30,))
        x += BW + BG
    y   += BH + BG
    row += 1

# ── Typography ───────────────────────────────────────────────────────────────
def load_font(size):
    candidates = [
        '/System/Library/Fonts/SFNS.ttf',
        '/System/Library/Fonts/SFNSDisplay.ttf',
        '/System/Library/Fonts/SFNSText.ttf',
        '/System/Library/Fonts/Helvetica.ttc',
        '/Library/Fonts/Arial.ttf',
        '/System/Library/Fonts/Arial.ttf',
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

font_title   = load_font(90)
font_tagline = load_font(36)
font_sub     = load_font(23)

d.text((70, 176), "DinoClaude",               font=font_title,   fill=TEXT1)
d.text((74, 288), "Jump the Context Limit.",   font=font_tagline, fill=OR)
d.text((74, 338), "A browser-based runner game.", font=font_sub,  fill=TEXT3)

img.save(OUT, 'PNG', optimize=True)
print(f"Saved {OUT}  ({os.path.getsize(OUT):,} bytes)")
