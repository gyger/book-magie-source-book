"""Figure 58: Huygens's principle of secondary spherical wavelets from luminous point A."""

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
    sw_thin = 4.5

    # Luminous point A
    ax, ay = 491.0, 78.0

    # Bounding rays AC and AE (angles from +x axis: ~110.6 deg and ~66.5 deg)
    ang_l_deg = 110.6
    ang_r_deg = 66.5
    ang_l = math.radians(ang_l_deg)
    ang_r = math.radians(ang_r_deg)
    r_env = 784.0  # Envelope DCF radius

    cx, cy = ax + r_env * math.cos(ang_l), ay + r_env * math.sin(ang_l)
    ex, ey = ax + r_env * math.cos(ang_r), ay + r_env * math.sin(ang_r)
    s.line(ax, ay, cx, cy, stroke_width=sw)
    s.line(ax, ay, ex, ey, stroke_width=sw)

    # Arc H-B-G-I (radius ~478)
    r1 = 478.0
    s.arc(ax, ay, r1, 47.0, 134.0, stroke_width=sw_thin, sweep=1)

    # 4 interior tick angles along B-G and d-d-d-d
    tick_degs = (75.3, 84.1, 93.0, 101.8)

    # Tick marks b, b, b, b along arc B-G
    for deg in tick_degs:
        rad = math.radians(deg)
        p1 = (ax + (r1 - 12) * math.cos(rad), ay + (r1 - 12) * math.sin(rad))
        p2 = (ax + (r1 + 12) * math.cos(rad), ay + (r1 + 12) * math.sin(rad))
        s.line(*p1, *p2, stroke_width=3.5)

    # Arc d-d-d-d (radius ~618)
    r2 = 618.0
    s.arc(ax, ay, r2, ang_r_deg, ang_l_deg, stroke_width=sw_thin, sweep=1)

    # 4 tick marks along d-d-d-d aligned with the 4 interior 'd' labels
    for deg in tick_degs:
        rad = math.radians(deg)
        p1 = (ax + (r2 - 10) * math.cos(rad), ay + (r2 - 10) * math.sin(rad))
        p2 = (ax + (r2 + 10) * math.cos(rad), ay + (r2 + 10) * math.sin(rad))
        s.line(*p1, *p2, stroke_width=3.5)

    # Secondary wavelets centered at B, b, b, b, b, G (radius = r_env - r1)
    r_w1 = r_env - r1
    wavelet_specs = [
        (ang_l_deg, ang_l_deg - 55.0, ang_l_deg + 43.0),  # B (leftmost, K to L-peak)
        (101.8, 101.8 - 56.0, 101.8 + 56.0),              # b1
        (93.0, 93.0 - 54.0, 93.0 + 61.0),                 # b2
        (84.1, 84.1 - 64.0, 84.1 + 54.0),                 # b3
        (75.3, 75.3 - 61.0, 75.3 + 55.0),                 # b4
        (ang_r_deg, ang_r_deg - 37.0, ang_r_deg + 55.0),  # G (rightmost, L-peak to above F)
    ]
    for deg, a0, a1 in wavelet_specs:
        rad = math.radians(deg)
        wx, wy = ax + r1 * math.cos(rad), ay + r1 * math.sin(rad)
        s.arc(wx, wy, r_w1, a0, a1, stroke_width=sw_thin, sweep=1)

    # Outer envelope arc D-C-E-F
    s.arc(ax, ay, r_env, 51.0, 126.5, stroke_width=sw, sweep=1)

    # Labels
    lib.label(s, 491.0, 42.0, "A", size=54.0, italic=False, bold=True)
    lib.label(s, 178.0, 392.0, "H", size=52.0, italic=False, bold=True)
    lib.label(s, 830.0, 386.0, "I", size=52.0, italic=False, bold=True)
    lib.label(s, 274.0, 536.0, "B", size=52.0, italic=False, bold=True)
    lib.label(s, 734.0, 530.0, "G", size=52.0, italic=False, bold=True)

    # b labels
    for x_b, y_b in [(375.0, 580.0), (454.0, 594.0), (534.0, 592.0), (620.0, 574.0)]:
        lib.label(s, x_b, y_b, "b", size=48.0, italic=True, bold=True)

    # d labels
    for x_d, y_d in [
        (232.0, 638.0),
        (366.0, 646.0),
        (456.0, 656.0),
        (552.0, 656.0),
        (648.0, 642.0),
        (772.0, 622.0),
    ]:
        lib.label(s, x_d, y_d, "d", size=48.0, italic=True, bold=True)

    lib.label(s, 44.0, 646.0, "K", size=50.0, italic=False, bold=True)
    lib.label(s, 52.0, 746.0, "D", size=50.0, italic=False, bold=True)
    lib.label(s, 200.0, 838.0, "C", size=52.0, italic=False, bold=True)
    lib.label(s, 496.0, 730.0, "L", size=48.0, italic=False, bold=True)
    lib.label(s, 808.0, 832.0, "E", size=52.0, italic=False, bold=True)
    lib.label(s, 984.0, 728.0, "F", size=50.0, italic=False, bold=True)

    s.save(out_svg)
