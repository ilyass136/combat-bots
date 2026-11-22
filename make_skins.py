"""Generates the built-in 64x64 bot skins (original artwork).

Usage: python3 tools/make_skins.py src/main/resources/assets/botmod/textures/entity
Edit the palettes below (or drop your own 64x64 PNG skin in that folder,
named like the skin you want, e.g. myskin.png -> /bot spawn Bob myskin).
"""
import os
import sys

from PIL import Image

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)

# name: (u, v, width, height, depth) of each body box in the 64x64 skin layout
BOXES = {
    "head": (0, 0, 8, 8, 8),
    "body": (16, 16, 8, 12, 4),
    "rarm": (40, 16, 4, 12, 4),
    "rleg": (0, 16, 4, 12, 4),
    "larm": (32, 48, 4, 12, 4),
    "lleg": (16, 48, 4, 12, 4),
}


def fill(img, x0, y0, x1, y1, c):
    for x in range(x0, x1):
        for y in range(y0, y1):
            img.putpixel((x, y), c)


def box(img, name, c):
    u, v, w, h, d = BOXES[name]
    fill(img, u, v, u + 2 * d + 2 * w, v + d + h, c)


def bottom_rows(img, name, c, rows=3):
    u, v, w, h, d = BOXES[name]
    fill(img, u, v + d + h - rows, u + 2 * d + 2 * w, v + d + h, c)


def make(name, skin, hair, shirt, pants, boots, accent, eye, mask=False):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    box(img, "head", skin)
    box(img, "body", shirt)
    box(img, "rarm", shirt)
    box(img, "larm", shirt)
    box(img, "rleg", pants)
    box(img, "lleg", pants)
    for arm in ("rarm", "larm"):
        bottom_rows(img, arm, skin)
    for leg in ("rleg", "lleg"):
        bottom_rows(img, leg, boots)

    if mask:
        fill(img, 0, 0, 32, 16, hair)          # whole head covered
        fill(img, 8, 11, 16, 14, skin)         # eye strip
    else:
        fill(img, 0, 0, 32, 8, hair)           # top + bottom of head
        fill(img, 8, 8, 16, 11, hair)          # fringe
        fill(img, 24, 8, 32, 16, hair)         # back of head
        fill(img, 0, 8, 8, 13, hair)           # right side
        fill(img, 16, 8, 24, 13, hair)         # left side

    # eyes + mouth (front of head is x 8..16, y 8..16)
    img.putpixel((9, 12), (255, 255, 255, 255))
    img.putpixel((10, 12), eye)
    img.putpixel((13, 12), eye)
    img.putpixel((14, 12), (255, 255, 255, 255))
    if not mask:
        fill(img, 11, 14, 13, 15, (110, 60, 50, 255))

    # belt + chest emblem
    fill(img, 16, 28, 40, 30, accent)
    fill(img, 23, 22, 25, 25, accent)

    img.save(os.path.join(OUT, name + ".png"))


def c(r, g, b):
    return (r, g, b, 255)


make("knight", c(224, 172, 140), c(70, 50, 40), c(120, 130, 150), c(70, 76, 92),
     c(45, 48, 58), c(210, 170, 60), c(40, 90, 200))
make("warrior", c(210, 160, 125), c(30, 25, 25), c(170, 40, 40), c(60, 40, 40),
     c(35, 25, 25), c(235, 200, 70), c(40, 40, 40))
make("ninja", c(224, 172, 140), c(25, 25, 30), c(35, 35, 42), c(30, 30, 36),
     c(20, 20, 24), c(200, 30, 30), c(20, 20, 20), mask=True)
make("builder", c(224, 172, 140), c(240, 200, 40), c(230, 120, 30), c(60, 80, 140),
     c(80, 55, 35), c(250, 240, 120), c(60, 40, 20))
make("robot", c(170, 200, 210), c(90, 100, 112), c(130, 150, 165), c(95, 110, 125),
     c(60, 70, 82), c(60, 220, 230), c(60, 230, 240))
print("skins written to", OUT)
