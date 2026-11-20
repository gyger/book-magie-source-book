"""Figure 49: Descartes's law of refraction — two circles illustrating constant sine ratio for multiple incident angles."""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.0
    sw_thin = 4.0

    y_surf = 419.0
    s.line(3.0, y_surf, w - 3.0, y_surf, stroke_width=sw)

    # Diagonal 45-degree hatching below surface
    x_h0, x_h1 = 42.0, 1554.0
    y_h1 = 860.0
    step = 30.5
    c = x_h0 + y_surf + 16.0
    while c <= x_h1 + y_h1 - 10.0:
        xt = min(x_h1, c - y_surf)
        yt = c - xt
        xb = max(x_h0, c - y_h1)
        yb = c - xb
        if yt < yb:
            s.line(xt, yt, xb, yb, stroke_width=3.2)
        c += step

    # --- Left circle centered at B ---
    bx, by = 511.5, y_surf
    r1 = 385.5
    s.circle(bx, by, r1, stroke_width=sw)
    # Vertical diameter through B
    s.line(bx, by - r1, bx, by + r1, stroke_width=sw_thin)

    # Point K on upper-left circle
    kx, ky = 238.0, 147.0
    # Point A on upper-left circle
    ax, ay = 148.0, 288.0
    # Horizontal KM and AH
    s.line(kx, ky, bx, ky, stroke_width=sw_thin)
    s.line(ax, ay, bx, ay, stroke_width=sw_thin)

    # Refracted points I (from A) and L (from K) on lower-right circle
    ix, iy = 772.0, 697.0
    lx, ly = 696.0, 756.0
    # Rays KB -> L and AB -> I
    s.line(kx, ky, bx, by, stroke_width=sw_thin)
    s.line(ax, ay, bx, by, stroke_width=sw_thin)
    s.line(bx, by, ix, iy, stroke_width=sw_thin)
    s.line(bx, by, lx, ly, stroke_width=sw_thin)
    # Horizontal GI and NL
    s.line(bx, iy, ix, iy, stroke_width=sw_thin)
    s.line(bx, ly, lx, ly, stroke_width=sw_thin)

    # --- Right circle (open arc) centered at R ---
    rx, ry = 1143.0, y_surf
    r2 = 303.0
    # Arc from ~ -132 deg (point P) clockwise around top, right, bottom to ~ 116 deg
    s.arc(rx, ry, r2, -133.0, 116.0, stroke_width=sw, sweep=1)
    # Vertical diameter through R
    s.line(rx, ry - r2, rx, ry + r2, stroke_width=sw_thin)

    # Point P on upper-left of right circle
    px, py = 936.0, 196.0
    # Point S on lower-right of right circle
    sx_pt, sy_pt = 1301.0, 677.0
    # Horizontal PQ and TS
    s.line(px, py, rx, py, stroke_width=sw_thin)
    s.line(rx, sy_pt, sx_pt, sy_pt, stroke_width=sw_thin)
    # Ray P-R-S
    s.line(px, py, rx, ry, stroke_width=sw_thin)
    s.line(rx, ry, sx_pt, sy_pt, stroke_width=sw_thin)

    # Labels
    lib.label(s, 194.0, 130.0, "K", size=54.0, italic=False, bold=True)
    lib.label(s, 548.0, 144.0, "M", size=54.0, italic=False, bold=True)
    lib.label(s, 112.0, 282.0, "A", size=54.0, italic=False, bold=True)
    lib.label(s, 544.0, 286.0, "H", size=54.0, italic=False, bold=True)
    lib.label(s, 93.0, 386.0, "C", size=54.0, italic=False, bold=True)
    lib.label(s, 536.0, 392.0, "B", size=54.0, italic=False, bold=True)
    lib.label(s, 478.0, 686.0, "G", size=54.0, italic=False, bold=True)
    lib.label(s, 478.0, 756.0, "N", size=54.0, italic=False, bold=True)
    lib.label(s, 720.0, 780.0, "L", size=54.0, italic=False, bold=True)
    lib.label(s, 784.0, 730.0, "I", size=54.0, italic=False, bold=True)

    lib.label(s, 898.0, 198.0, "P", size=54.0, italic=False, bold=True)
    lib.label(s, 1190.0, 196.0, "Q", size=54.0, italic=False, bold=True)
    lib.label(s, 1106.0, 444.0, "R", size=54.0, italic=False, bold=True)
    lib.label(s, 1108.0, 672.0, "T", size=54.0, italic=False, bold=True)
    lib.label(s, 1335.0, 682.0, "S", size=54.0, italic=False, bold=True)

    s.save(out_svg)
