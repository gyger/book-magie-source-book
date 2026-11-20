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
    y_top: float,
    y_bot: float,
    sw: float = 5.5,
) -> None:
    """Draw the lower portion of a tilted ellipse centered at (cx, cy), clipped to [y_top, y_bot]."""
    rad = math.radians(tilt_deg)
    ct, st = math.cos(rad), math.sin(rad)
    pts: list[tuple[float, float]] = []
    # Sample angle theta from 0 to pi (lower half in SVG coords where +y is down)
    for i in range(121):
        th = -0.15 + (math.pi + 0.30) * (i / 120.0)
        ex = a * math.cos(th)
        ey = b * math.sin(th)
        x = cx + ex * ct - ey * st
        y = cy + ex * st + ey * ct
        if y >= y_top - 2.0 and y <= y_bot + 3.0:
            pts.append((x, y))
    if len(pts) >= 2:
        s.polyline(pts, stroke_width=sw)


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.0
    sw_thin = 5.0

    y_top = 86.0
    y_surf = 395.0
    y_bot = 770.0

    # Three horizontal lines: RC (top), SAB (surface), NQ (bottom envelope)
    s.line(115.0, y_top, 858.0, y_top, stroke_width=sw)
    s.line(24.0, y_surf, 898.0, y_surf, stroke_width=sw)
    s.line(36.0, y_bot, 878.0, y_bot, stroke_width=sw)

    # 5 incident vertical rays from RC down to SAB
    xs_top = [299.0, 405.0, 513.0, 614.0, 718.0]
    xs_surf = [290.0, 404.0, 511.0, 611.0, 719.0]
    for xt, xs in zip(xs_top, xs_surf):
        s.line(xt, y_top, xs, y_surf, stroke_width=sw_thin)

    # Refracted extraordinary rays inside crystal (parallel, shifted left by ~48px at y_bot)
    for xs in xs_surf:
        s.line(xs, y_surf, xs - 48.0, y_bot, stroke_width=sw_thin)

    # Principal axis line through A (290, 395): up-right to (368, 200), down-left to (160, 770)
    ax, ay = 290.0, y_surf
    s.line(368.0, 200.0, 160.0, y_bot, stroke_width=sw_thin)

    # Line A-Z and parallel axis T-Z down to envelope
    tx, ty = 574.0, y_surf
    zx, zy = 516.0, 514.0
    s.line(ax, ay, zx, zy, stroke_width=sw_thin)
    s.line(tx, ty, 444.0, y_bot, stroke_width=sw_thin)

    # 5 elliptical secondary wavelets centered at xs_surf on y_surf, tangent to y_bot
    for idx, xs in enumerate(xs_surf):
        _elliptical_wavelet(s, xs, y_surf, 198.0, 375.0, -13.0, y_surf if idx == 0 else 545.0, y_bot, sw=sw_thin)

    # Labels
    lib.label(s, 296.0, 52.0, "R", size=50.0, italic=False, bold=True)
    lib.label(s, 402.0, 52.0, "H", size=50.0, italic=False, bold=True)
    lib.label(s, 512.0, 52.0, "h", size=50.0, italic=True, bold=True)
    lib.label(s, 616.0, 52.0, "h", size=50.0, italic=True, bold=True)
    lib.label(s, 718.0, 52.0, "C", size=50.0, italic=False, bold=True)
    lib.label(s, 332.0, 126.0, "X", size=46.0, italic=False, bold=True)

    lib.label(s, 50.0, 362.0, "S", size=50.0, italic=False, bold=True)
    lib.label(s, 256.0, 362.0, "A", size=50.0, italic=False, bold=True)
    lib.label(s, 376.0, 362.0, "K", size=48.0, italic=False, bold=True)
    lib.label(s, 490.0, 362.0, "k", size=48.0, italic=True, bold=True)
    lib.label(s, 576.0, 362.0, "T", size=48.0, italic=False, bold=True)
    lib.label(s, 640.0, 362.0, "k", size=48.0, italic=True, bold=True)
    lib.label(s, 756.0, 362.0, "B", size=50.0, italic=False, bold=True)

    lib.label(s, 548.0, 518.0, "Z", size=48.0, italic=False, bold=True)
    lib.label(s, 122.0, 678.0, "V", size=48.0, italic=False, bold=True)
    lib.label(s, 232.0, 804.0, "N", size=50.0, italic=False, bold=True)
    lib.label(s, 672.0, 804.0, "Q", size=50.0, italic=False, bold=True)

    s.save(out_svg)
