"""Figure 77: Michelson-Morley fringe displacement observations (noon upper, evening lower) vs. 1/8 theoretical sinusoid."""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw_obs = 6.5
    sw_th = 5.5

    x0, x1 = 44.0, 2046.0
    span = x1 - x0

    # --- Upper (noon) curves ---
    y0_up = 300.0
    amp_up = 256.0
    # Theoretical dashed sinusoid (1/8 theoretical displacement)
    pts_th_up: list[tuple[float, float]] = []
    for i in range(121):
        u = i / 120.0
        x = x0 + span * u
        y = y0_up - amp_up * math.sin(2.0 * math.pi * u)
        pts_th_up.append((x, y))
    s.polyline(pts_th_up, stroke_width=sw_th, dash="28,12")

    # Observed noon piecewise-linear curve (measured from scan at 16 azimuth steps)
    obs_up_y = [
        304.0, 294.0, 278.0, 294.0, 314.0, 322.0, 314.0, 304.0,
        296.0, 318.0, 352.0, 386.0, 418.0, 396.0, 366.0, 328.0, 286.0,
    ]
    pts_obs_up = [(x0 + span * (i / 16.0), y) for i, y in enumerate(obs_up_y)]
    s.polyline(pts_obs_up, stroke_width=sw_obs)

    # --- Lower (evening) curves ---
    y0_dn = 734.0
    amp_dn = 248.0
    pts_th_dn: list[tuple[float, float]] = []
    for i in range(121):
        u = i / 120.0
        x = x0 + span * u
        y = y0_dn - amp_dn * math.sin(2.0 * math.pi * u)
        pts_th_dn.append((x, y))
    s.polyline(pts_th_dn, stroke_width=sw_th, dash="28,12")

    # Observed evening piecewise-linear curve (16 azimuth steps)
    obs_dn_y = [
        734.0, 754.0, 772.0, 752.0, 728.0, 746.0, 764.0, 754.0,
        740.0, 772.0, 798.0, 786.0, 770.0, 748.0, 728.0, 712.0, 702.0,
    ]
    pts_obs_dn = [(x0 + span * (i / 16.0), y) for i, y in enumerate(obs_dn_y)]
    s.polyline(pts_obs_dn, stroke_width=sw_obs)

    # --- Central vertical tick scales at x = 1045 ---
    tx = 1045.0
    # Upper ticks (from 0.05 lambda down to 0.00)
    for idx in range(6):
        ty = 48.0 + idx * 50.0
        tw = 42.0 if idx in (0, 5) else 26.0
        s.line(tx - tw, ty, tx + tw, ty, stroke_width=5.0)
    # Lower ticks (from -0.05 down to 0.00 lambda)
    for idx in range(6):
        ty = 472.0 + idx * 50.0
        tw = 42.0 if idx in (0, 5) else 26.0
        s.line(tx - tw, ty, tx + tw, ty, stroke_width=5.0)

    # Scale labels
    lib.label(s, 1176.0, 92.0, "0.05 \u03bb", size=44.0, italic=True, bold=True)
    lib.label(s, 1152.0, 294.0, "0.00", size=42.0, italic=False, bold=True)
    lib.label(s, 1144.0, 472.0, "0.05", size=42.0, italic=False, bold=True)
    lib.label(s, 1178.0, 712.0, "0.00 \u03bb", size=44.0, italic=True, bold=True)

    # Compass direction labels (N/S left, E/W middle, S/N right)
    lib.label(s, 58.0, 778.0, "N", size=42.0, italic=False, bold=True)
    lib.label(s, 58.0, 828.0, "S", size=42.0, italic=False, bold=True)
    lib.label(s, 1046.0, 796.0, "E", size=42.0, italic=False, bold=True)
    lib.label(s, 1046.0, 848.0, "W", size=42.0, italic=False, bold=True)
    lib.label(s, 2068.0, 744.0, "S", size=42.0, italic=False, bold=True)
    lib.label(s, 2068.0, 794.0, "N", size=42.0, italic=False, bold=True)

    s.save(out_svg)
