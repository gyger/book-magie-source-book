"""Figure 48: Descartes's law of refraction — circle with incident ray AB, refracted ray BI, and hatched denser medium."""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.5
    sw_thin = 4.2

    cx, cy = 594.5, 446.5
    r = 384.0

    # Horizontal surface line CBE (slight natural slope 443 -> 451)
    def surf_y(x: float) -> float:
        return 442.5 + (x / w) * 8.5

    s.line(28.0, surf_y(28.0), w - 2.0, surf_y(w - 2.0), stroke_width=sw)

    # Diagonal 45-degree hatching below surface
    x_h0, x_h1 = 118.0, 1072.0
    y_h1 = 860.0
    step = 32.5
    # Lines of form x + y = c
    c_start = x_h0 + surf_y(x_h0) + 18.0
    c_end = x_h1 + y_h1 - 10.0
    c = c_start
    while c <= c_end:
        # Intersect x + y = c with y = surf_y(x), y = y_h1, x = x_h0, x = x_h1
        # Solve x + 442.5 + 8.5*x/w = c => x * (1 + 8.5/w) = c - 442.5
        xt = (c - 442.5) / (1.0 + 8.5 / w)
        yt = surf_y(xt)
        if xt > x_h1:
            xt = x_h1
            yt = c - xt
        xb = c - y_h1
        yb = y_h1
        if xb < x_h0:
            xb = x_h0
            yb = c - xb
        if yt < yb and x_h0 - 1 <= xb <= x_h1 + 1 and x_h0 - 1 <= xt <= x_h1 + 1:
            s.line(xt, yt, xb, yb, stroke_width=3.6)
        c += step

    # White knockout masks over hatching behind labels D, G, I (before drawing circle/lines)
    s.rect(898.0, 667.0, 50.0, 56.0, fill="#ffffff", stroke="none")  # behind D
    s.rect(531.0, 728.0, 54.0, 56.0, fill="#ffffff", stroke="none")  # behind G
    s.rect(790.0, 770.0, 36.0, 52.0, fill="#ffffff", stroke="none")  # behind I

    # Main circle: solid upper semicircle above interface, dashed lower semicircle below interface
    surf_deg = math.degrees(math.atan2(8.5, w))
    s.arc(cx, cy, r, 180.0 + surf_deg, 360.0 + surf_deg, stroke_width=sw, sweep=1)
    s.arc(cx, cy, r, surf_deg, 180.0 + surf_deg, stroke_width=sw, dash="28,18", sweep=1)

    # Vertical diameter through B (H-B-G)
    s.line(cx, cy - r, cx, cy + r, stroke_width=sw)

    # Point A on upper-left circle
    ax, ay = 299.0, 200.5
    # Point D on lower-right circle (straight continuation of AB)
    dx_ab = cx - ax
    dy_ab = cy - ay
    # Extend before A to (102, 37) and past D to (920, 718)
    s.line(102.0, 37.0, 895.0, 696.5, stroke_width=sw)

    # Vertical AC and horizontal AH
    s.line(ax, ay, ax, surf_y(ax), stroke_width=sw_thin)
    s.line(ax, ay, cx, ay, stroke_width=sw_thin)

    # Vertical FEI at x = 803.5
    x_fe = 803.5
    y_f_top = cy - math.sqrt(max(0.0, r * r - (x_fe - cx) ** 2))
    y_i = cy + math.sqrt(max(0.0, r * r - (x_fe - cx) ** 2))  # ~768
    s.line(x_fe, y_f_top - 4.0, x_fe, y_i, stroke_width=sw)

    # Refracted ray BI and horizontal GI
    s.line(cx, cy, x_fe, y_i, stroke_width=sw_thin)
    s.line(cx, y_i, x_fe, y_i, stroke_width=sw_thin)

    # Labels
    lib.label(s, 290.0, 160.0, "A", size=58.0, italic=False, bold=True)
    lib.label(s, 624.0, 188.0, "H", size=58.0, italic=False, bold=True)
    lib.label(s, 825.0, 102.0, "F", size=58.0, italic=False, bold=True)
    lib.label(s, 330.0, 410.0, "C", size=58.0, italic=False, bold=True)
    lib.label(s, 626.0, 410.0, "B", size=58.0, italic=False, bold=True)
    lib.label(s, 836.0, 410.0, "E", size=58.0, italic=False, bold=True)
    lib.label(s, 922.0, 695.0, "D", size=58.0, italic=False, bold=True)
    lib.label(s, 558.0, 756.0, "G", size=58.0, italic=False, bold=True)
    lib.label(s, 808.0, 796.0, "I", size=58.0, italic=False, bold=True)

    s.save(out_svg)
