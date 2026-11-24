"""Figure 61: Huygens's elliptical secondary wavelets for extraordinary refraction in Iceland spar."""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image

import draw
import library as lib


def _elliptical_wavelet(
    s: draw.Scene,
    cx: float,
    cy: float,
    a: float,
    b: float,
    tilt_deg: float,
    y_left_top: float,
    y_right_top: float,
    y_bot: float,
    sw: float = 5.5,
) -> None:
    """Draw the lower portion of a tilted ellipse centered at (cx, cy), clipped per side."""
    rad = math.radians(tilt_deg)
    ct, st = math.cos(rad), math.sin(rad)
    pts: list[tuple[float, float]] = []
    # Sample angle theta from -0.6 to pi + 0.6 so both sides cover up to y_surf
    for i in range(181):
        th = -0.6 + (math.pi + 1.2) * (i / 180.0)
        ex = a * math.cos(th)
        ey = b * math.sin(th)
        x = cx + ex * ct - ey * st
        y = cy + ex * st + ey * ct
        y_lim = y_left_top if x < cx else y_right_top
        if y >= y_lim - 2.0 and y <= y_bot + 3.0:
            pts.append((x, y))
    if len(pts) >= 2:
        s.polyline(pts, stroke_width=sw)


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.0
    sw_thin = 5.0

    y_top = 90.5
    y_surf = 391.0
    y_bot = 760.5

    # Three horizontal lines: RC (top), SAB (surface), NQ (bottom envelope)
    s.line(115.0, y_top, 858.0, y_top, stroke_width=sw)
    s.line(24.0, y_surf, 898.0, y_surf, stroke_width=sw)
    s.line(36.0, y_bot, 878.0, y_bot, stroke_width=sw)

    # 5 incident vertical rays from RC down to SAB
    xs_top = [305.0, 416.0, 524.0, 626.0, 733.0]
    xs_surf = [291.0, 410.0, 518.0, 620.0, 729.0]
    for xt, xs in zip(xs_top, xs_surf):
        s.line(xt, y_top, xs, y_surf, stroke_width=sw_thin)

    # Refracted extraordinary rays inside crystal (parallel, shifted left by ~57px at y_bot)
    for xs in xs_surf:
        s.line(xs, y_surf, xs - 57.0, y_bot, stroke_width=sw_thin)

    # Principal axis line through A (291, 391): up-right to (368, 200), down-left to (156, 760.5)
    ax, ay = 291.0, y_surf
    s.line(368.0, 200.0, 156.0, y_bot, stroke_width=sw_thin)

    # Line A-Z and parallel axis T-Z down to envelope
    tx, ty = 576.0, y_surf
    zx, zy = 524.0, 506.0
    s.line(ax, ay, zx, zy, stroke_width=sw_thin)
    s.line(tx, ty, 436.0, y_bot, stroke_width=sw_thin)

    # 5 elliptical secondary wavelets shifted down-left so each is tangent to y_bot at its refracted ray
    clip_tops = [
        (y_surf, 550.0),
        (535.0, 565.0),
        (595.0, 580.0),
        (580.0, 565.0),
        (550.0, 550.0),
    ]
    for idx, (xs, (yl, yr)) in enumerate(zip(xs_surf, clip_tops)):
        if idx == 0:
            dx0, a_rx = -38.0, 217.0
        else:
            dx0, a_rx = -20.0, 195.0
        _elliptical_wavelet(
            s,
            xs + dx0,
            y_surf + 89.0,
            a_rx,
            282.0,
            13.4,
            yl,
            yr,
            y_bot,
            sw=sw_thin,
        )

    # Labels
    lib.label(s, 302.0, 52.0, "R", size=50.0, italic=False, bold=True)
    lib.label(s, 412.0, 52.0, "H", size=50.0, italic=False, bold=True)
    lib.label(s, 520.0, 52.0, "h", size=50.0, italic=True, bold=True)
    lib.label(s, 624.0, 52.0, "h", size=50.0, italic=True, bold=True)
    lib.label(s, 728.0, 52.0, "C", size=50.0, italic=False, bold=True)
    lib.label(s, 338.0, 128.0, "X", size=46.0, italic=False, bold=True)

    lib.label(s, 48.0, 358.0, "S", size=50.0, italic=False, bold=True)
    lib.label(s, 256.0, 358.0, "A", size=50.0, italic=False, bold=True)
    lib.label(s, 378.0, 358.0, "K", size=48.0, italic=False, bold=True)
    lib.label(s, 492.0, 358.0, "k", size=48.0, italic=True, bold=True)
    lib.label(s, 578.0, 358.0, "T", size=48.0, italic=False, bold=True)
    lib.label(s, 646.0, 358.0, "k", size=48.0, italic=True, bold=True)
    lib.label(s, 760.0, 358.0, "B", size=50.0, italic=False, bold=True)

    lib.label(s, 552.0, 508.0, "Z", size=48.0, italic=False, bold=True)
    lib.label(s, 122.0, 678.0, "V", size=48.0, italic=False, bold=True)
    lib.label(s, 232.0, 798.0, "N", size=50.0, italic=False, bold=True)
    lib.label(s, 672.0, 798.0, "Q", size=50.0, italic=False, bold=True)

    s.save(out_svg)
