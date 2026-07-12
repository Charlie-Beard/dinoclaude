#!/usr/bin/env python3
"""Generates assets/images/apple-touch-icon.png (180x180) for DinoClaude.

iOS ignores SVG apple-touch-icons, so the favicon mascot is re-rendered as a
PNG on a solid background (iOS fills transparency with black).
"""
from PIL import Image, ImageDraw
import os

SIZE = 180
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images', 'apple-touch-icon.png')

BG  = (255, 251, 245)
OR  = (212, 103,  61)
OR2 = (184,  85,  48)
DK  = ( 30,  10,   2)

img = Image.new('RGB', (SIZE, SIZE), BG)
d   = ImageDraw.Draw(img)

# Mascot grid matches favicon.svg: 8 cols x 11 rows.
P  = 13
ox = (SIZE - 8 * P) // 2
oy = (SIZE - 11 * P) // 2

def px(x, y, w, h, color):
    d.rectangle([ox + x * P, oy + y * P, ox + (x + w) * P - 1, oy + (y + h) * P - 1], fill=color)

px(1, 0, 2, 2, OR)    # left antenna
px(5, 0, 2, 2, OR)    # right antenna
px(0, 2, 8, 5, OR)    # body
px(0, 7, 8, 1, OR2)   # belly shading
px(1, 3, 2, 2, DK)    # left eye
px(5, 3, 2, 2, DK)    # right eye
px(1, 8, 2, 3, OR)    # left leg (extended)
px(5, 8, 2, 2, OR2)   # right leg (raised)

img.save(OUT, 'PNG', optimize=True)
print(f"Saved {OUT}  ({os.path.getsize(OUT):,} bytes)")
