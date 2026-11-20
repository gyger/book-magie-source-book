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

    # Bounding rays AC and AE (angles from +x axis: ~110.5 deg and ~67.5 deg)
    ang_l = math.radians(110.5)
    ang_r = math.radians(67.5)
    r_env = 782.0  # Envelope DCF radius

    cx, cy = ax + r_env * math.cos(ang_l), ay + r_env * math.sin(ang_l)
    ex, ey = ax + r_env * math.cos(ang_r), ay + r_env * math.sin(ang_r)
    s.line(ax, ay, cx, cy, stroke_width=sw)
    s.line(ax, ay, ex, ey, stroke_width=sw)

    # Arc H-B-G-I (radius ~478)
    r1 = 478.0
    s.arc(ax, ay, r1, 47.0, 134.0, stroke_width=sw_thin, sweep=1)

    # Tick marks b, b, b, b along arc B-G
    for deg in (75.5, 84.5, 93.5, 102.5):
        rad = math.radians(deg)
        p1 = (ax + (r1 - 12) * math.cos(rad), ay + (r1 - 12) * math.sin(rad))
        p2 = (ax + (r1 + 12) * math.cos(rad), ay + (r1 + 12) * math.sin(rad))
        s.line(*p1, *p2, stroke_width=3.5)

    # Arc d-d-d-d (radius ~618)
    r2 = 618.0
    s.arc(ax, ay, r2, 67.5, 110.5, stroke_width=sw_thin, sweep=1)

    # Tick marks along d-d-d-d and secondary wavelets centered on them (radius = r_env - r2 = 164)
    r_w2 = r_env - r2
    for deg in (73.5, 81.5, 89.5, 97.5, 105.5):
        rad = math.radians(deg)
        wx, wy = ax + r2 * math.cos(rad), ay + r2 * math.sin(rad)
        p1 = (ax + (r2 - 10) * math.cos(rad), ay + (r2 - 10) * math.sin(rad))
        p2 = (ax + (r2 + 10) * math.cos(rad), ay + (r2 + 10) * math.sin(rad))
        s.line(*p1, *p2, stroke_width=3.5)
        # Wavelet arc tangent to outer envelope
        s.arc(wx, wy, r_w2, deg - 58.0, deg + 58.0, stroke_width=3.8, sweep=1)

    # Larger secondary wavelets centered at B and G (radius = r_env - r1 = 304)
    r_w1 = r_env - r1
    bx, by = ax + r1 * math.cos(ang_l), ay + r1 * math.sin(ang_l)
    gx, gy = ax + r1 * math.cos(ang_r), ay + r1 * math.sin(ang_r)
    s.arc(bx, by, r_w1, 60.0, 155.0, stroke_width=sw_thin, sweep=1)
    s.arc(gx, gy, r_w1, 25.0, 120.0, stroke_width=sw_thin, sweep=1)

    # Outer envelope arc D-C-E-F
    s.arc(ax, ay, r_env, 51.0, 129.0, stroke_width=sw, sweep=1)

    # Labels
    lib.label(s, 491.0, 42.0, "A", size=54.0, italic=False, bold=True)
    lib.label(s, 178.0, 392.0, "H", size=52.0, italic=False, bold=True)
    lib.label(s, 830.0, 386.0, "I", size=52.0, italic=False, bold=True)
    lib.label(s, 274.0, 536.0, "B", size=52.0, italic=False, bold=True)
    lib.label(s, 725.0, 530.0, "G", size=52.0, italic=False, bold=True)

    # b labels
    for x_b, y_b in [(375.0, 588.0), (454.0, 602.0), (534.0, 600.0), (620.0, 582.0)]:
        lib.label(s, x_b, y_b, "b", size=48.0, italic=True, bold=True)

    # d labels
    for x_d, y_d in [
        (246.0, 646.0),
        (368.0, 656.0),
        (456.0, 666.0),
        (552.0, 666.0),
        (652.0, 650.0),
        (764.0, 628.0),
    ]:
        lib.label(s, x_d, y_d, "d", size=48.0, italic=True, bold=True)

    lib.label(s, 44.0, 646.0, "K", size=50.0, italic=False, bold=True)
    lib.label(s, 48.0, 742.0, "D", size=50.0, italic=False, bold=True)
    lib.label(s, 200.0, 838.0, "C", size=52.0, italic=False, bold=True)
    lib.label(s, 514.0, 738.0, "L", size=48.0, italic=False, bold=True)
    lib.label(s, 800.0, 832.0, "E", size=52.0, italic=False, bold=True)
    lib.label(s, 980.0, 728.0, "F", size=50.0, italic=False, bold=True)

    s.save(out_svg)
