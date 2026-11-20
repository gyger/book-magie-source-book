"""Figure 36: Amontons's air thermometer (long vertical tube A, globe D, U-bend C, mercury level B-E)."""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 8.0

    # Slight natural lean of the long glass tube from top (y=96) to U-bend start (y=2910)
    # Measured: y=150 -> L=303.5, R=345.5; y=2900 -> L=320.5, R=362.5
    top_y = 95.0
    ubend_y = 2915.0

    lx_top, rx_top = 304.0, 346.5
    lx_bot, rx_bot = 320.5, 362.5

    # Open top rim ellipse at A
    cx_top = 0.5 * (lx_top + rx_top)
    rx_ell = 0.5 * (rx_top - lx_top)
    s.ellipse(cx_top, top_y, rx_ell, 9.5, stroke_width=sw)

    # Long left vertical tube walls (from top rim down to start of U-bend)
    s.line(lx_top, top_y, lx_bot, ubend_y, stroke_width=sw)
    s.line(rx_top, top_y, rx_bot, ubend_y, stroke_width=sw)

    # Right short arm of U-bend connecting to bottom of globe D
    # Measured at y=2850..2900: inner wall x=470.5, outer wall x=515.5
    r_in_x = 470.5
    r_out_x = 515.5
    neck_y = 2796.0

    s.line(r_in_x, neck_y, r_in_x, ubend_y, stroke_width=sw)
    s.line(r_out_x, neck_y, r_out_x, ubend_y, stroke_width=sw)

    # Bottom U-bend (semicircular inner and outer arcs)
    # Inner arc connects (rx_bot, ubend_y) to (r_in_x, ubend_y)
    # Outer arc connects (lx_bot, ubend_y) to (r_out_x, ubend_y)
    in_cx = 0.5 * (rx_bot + r_in_x)
    in_r = 0.5 * (r_in_x - rx_bot)
    out_cx = 0.5 * (lx_bot + r_out_x)
    out_r = 0.5 * (r_out_x - lx_bot)

    # Use elliptical arcs for exact bottom y matching (inner bottom ~2972, outer bottom ~3016)
    in_ry = 2972.0 - ubend_y
    out_ry = 3016.0 - ubend_y
    s.path(
        f"M {draw._fmt(rx_bot)} {draw._fmt(ubend_y)} "
        f"A {draw._fmt(in_r)} {draw._fmt(in_ry)} 0 0 0 {draw._fmt(r_in_x)} {draw._fmt(ubend_y)}",
        stroke_width=sw,
    )
    s.path(
        f"M {draw._fmt(lx_bot)} {draw._fmt(ubend_y)} "
        f"A {draw._fmt(out_r)} {draw._fmt(out_ry)} 0 0 0 {draw._fmt(r_out_x)} {draw._fmt(ubend_y)}",
        stroke_width=sw,
    )

    # Spherical globe D sitting on top of the right neck (opening between r_in_x and r_out_x)
    gcx, gcy, gr = 496.5, 2673.0, 124.5
    # Compute angles where the globe meets the neck walls at r_in_x and r_out_x
    a_left = math.degrees(math.acos((r_in_x - gcx) / gr))   # lower-left
    a_right = math.degrees(math.acos((r_out_x - gcx) / gr)) # lower-right
    # Sweep clockwise from a_left around the top to a_right
    s.arc(gcx, gcy, gr, a_left, a_right, stroke_width=sw, sweep=1)

    # Horizontal dashed mercury-level line B-E
    s.line(22.0, 2798.0, 715.0, 2798.0, stroke_width=6.0, dash="28,22")

    # Labels (roman bold/upright matching 1935 scan)
    lib.label(s, 326.0, 48.0, "A", size=64.0, italic=False, bold=True)
    lib.label(s, 484.0, 2508.0, "D", size=58.0, italic=False, bold=True)
    lib.label(s, 280.0, 2766.0, "B", size=58.0, italic=False, bold=True)
    lib.label(s, 544.0, 2828.0, "E", size=58.0, italic=False, bold=True)
    lib.label(s, 414.0, 3048.0, "C", size=58.0, italic=False, bold=True)

    s.save(out_svg)
