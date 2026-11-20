"""Figure 4: Galileo's odd-number law of falling bodies (triangle ABC and graduated line HI)."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    scene = draw.Scene(w, h)

    sw = 8.0
    sw_thin = 6.0

    # Triangle ABC
    ax, ay = 236.0, 82.0
    bx, by = 225.0, 1742.0
    cx, cy = 32.0, 1742.0

    scene.line(ax, ay, bx, by, stroke_width=sw)
    scene.line(ax, ay, cx, cy, stroke_width=sw)

    # Horizontal rungs between AC and AB
    rung_ys = [242.0, 396.0, 553.5, 709.5, 865.5]
    for ry in rung_ys:
        t = (ry - ay) / (by - ay)
        x_left = ax + t * (cx - ax)
        x_right = ax + t * (bx - ax)
        scene.line(x_left, ry, x_right, ry, stroke_width=sw_thin)

    # Graduated vertical line HI
    hx, hy = 367.0, 82.0
    ix, iy = 353.0, 1788.0
    scene.line(hx, hy, ix, iy, stroke_width=sw)

    # Ticks along HI: (y, left_ext, right_ext, major)
    ticks = [
        (82.0, 16.0, 18.0, True),     # H (0)
        (190.0, 14.0, 48.0, True),    # L (1)
        (296.5, 14.0, 14.0, False),   # 2
        (396.5, 14.0, 14.0, False),   # 3
        (498.0, 28.0, 56.0, True),    # M (4)
        (608.5, 14.0, 14.0, False),   # 5
        (704.5, 14.0, 14.0, False),   # 6
        (811.5, 14.0, 14.0, False),   # 7
        (914.5, 14.0, 14.0, False),   # 8
        (1018.0, 28.0, 56.0, True),   # N (9)
        (1122.5, 14.0, 14.0, False),  # 10
        (1230.5, 14.0, 14.0, False),  # 11
        (1337.5, 14.0, 14.0, False),  # 12
        (1445.5, 14.0, 14.0, False),  # 13
        (1552.5, 14.0, 14.0, False),  # 14
        (1656.5, 14.0, 14.0, False),  # 15
        (1762.0, 28.0, 32.0, True),   # I (16)
    ]
    for ty, ext_l, ext_r, major in ticks:
        t = (ty - hy) / (iy - hy)
        tx = hx + t * (ix - hx)
        scene.line(tx - ext_l, ty, tx + ext_r, ty, stroke_width=sw if major else sw_thin)

    # Labels
    lib.label(scene, 240, 44, "A", size=58, italic=False, bold=True)
    lib.label(scene, 367, 44, "H", size=58, italic=False, bold=True)
    lib.label(scene, 404, 174, "L", size=58, italic=False, bold=True)
    lib.label(scene, 174, 246, "O", size=58, italic=False, bold=True)
    lib.label(scene, 267, 210, "D", size=58, italic=False, bold=True)
    lib.label(scene, 158, 392, "P", size=58, italic=False, bold=True)
    lib.label(scene, 264, 372, "E", size=58, italic=False, bold=True)
    lib.label(scene, 402, 466, "M", size=58, italic=False, bold=True)
    lib.label(scene, 269, 530, "F", size=58, italic=False, bold=True)
    lib.label(scene, 270, 682, "G", size=58, italic=False, bold=True)
    lib.label(scene, 398, 984, "N", size=58, italic=False, bold=True)
    lib.label(scene, 60, 1726, "C", size=58, italic=False, bold=True)
    lib.label(scene, 255, 1730, "B", size=58, italic=False, bold=True)
    lib.label(scene, 381, 1734, "I", size=58, italic=False, bold=True)

    scene.save(out_svg)
