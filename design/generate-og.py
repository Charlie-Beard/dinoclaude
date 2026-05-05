#!/usr/bin/env python3
"""Generates assets/images/og-image.png for DinoClaude."""
from PIL import Image, ImageDraw, ImageFont
import os, sys

W, H = 1200, 630
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images', 'og-image.png')

BG      = (255, 251, 245)
TEXT1   = ( 18,  32,  51)
TEXT2   = ( 81,  96, 114)
TEXT3   = (138, 154, 176)
OR      = (212, 103,  61)
OR2     = (184,  85,  48)
DK      = ( 30,  10,   2)
BRICK1  = (143,  56,  32)
BRICK2  = (122,  46,  24)
BRICK3  = ( 94,  32,  16)
GROUND  = (219, 227, 238)

img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img, 'RGBA')

# Ground line
d.rectangle([0, 500, W, 503], fill=GROUND)

# ── Pixel-art mascot ──────────────────────────────────────────────────────────
P = 16    # 1 pixel = 16px  (game uses P=6, scaled up ~2.67x)
bx = 710  # left edge of sprite
by = 490  # bottom edge of sprite (ground level)

def sq(col, row, w, h, color):
    x = bx + col * P
    y = by - (row + h) * P
    d.rectangle([x, y, x + w*P - 1, y + h*P - 1], fill=color)

# Body (torso)
sq(0, 3, 8, 6, OR)
sq(0, 3, 8, 1, OR2)       # darker bottom strip on torso
# Face / head
sq(0, 9, 8, 2, OR)
sq(0, 9, 8, 1, OR2)       # brow line
sq(0, 11, 8, 1, OR)       # top of head
# Antennae
sq(1, 12, 2, 1, OR)
sq(5, 12, 2, 1, OR)
# Eyes
sq(1, 6, 2, 2, DK)
sq(5, 6, 2, 2, DK)
# Arms (raised — jump pose)
sq(-3, 6, 3, 2, OR)
sq( 8, 6, 3, 2, OR)
# Legs (jumping — spread apart)
sq(1, 0, 2, 3, OR)
sq(5, 1, 2, 2, OR2)

# Shadow ellipse on ground
shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ds = ImageDraw.Draw(shadow)
cx, cy, rx, ry = 770, 508, 72, 8
ds.ellipse([cx-rx, cy-ry, cx+rx, cy+ry], fill=(18, 32, 51, 18))
img.paste(Image.alpha_composite(Image.new('RGBA', (W, H), (0,0,0,0)), shadow).convert('RGB'), mask=shadow.split()[3])

# Motion lines
for x1, x2, y, alpha in [(622, 666, 318, 55), (612, 664, 352, 38), (628, 666, 386, 25)]:
    d.rectangle([x1, y, x2, y+2], fill=OR + (alpha,))

# ── Brick wall ───────────────────────────────────────────────────────────────
bw, bh, gap = 88, 34, 5

def brick(x, y):
    d.rectangle([x, y, x+bw-1, y+bh-1], fill=BRICK1)
    d.rectangle([x, y, x+bw-1, y+3],   fill=BRICK2)

wx = 978
for row in range(4):
    wy = 500 - (row + 1) * (bh + gap)
    off = 44 if row % 2 == 1 else 0
    for col in range(3):
        bx2 = wx + off + col * (bw + gap)
        if bx2 + bw <= W + 20:
            brick(bx2, wy)

# ── Typography ───────────────────────────────────────────────────────────────
def load_font(size, bold=False):
    # Try system fonts on macOS, fall back to default
    candidates = [
        '/System/Library/Fonts/SFNS.ttf',
        '/System/Library/Fonts/SFNSDisplay.ttf',
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

font_title   = load_font(94, bold=True)
font_tagline = load_font(38)
font_sub     = load_font(28)
font_label   = load_font(15)

d.text((80, 148), "DinoClaude", font=font_title,   fill=TEXT1)
d.text((84, 272), "Jump the Context Limit.", font=font_tagline, fill=TEXT2)
d.text((84, 326), "A browser-based runner game.", font=font_sub, fill=TEXT3)

# CONTEXT LIMIT label above wall
d.text((978, 218), "CONTEXT LIMIT", font=font_label, fill=BRICK2)

img.save(OUT, 'PNG', optimize=True)
print(f"Saved {OUT} ({os.path.getsize(OUT):,} bytes)")
