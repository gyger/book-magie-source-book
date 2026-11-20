"""Figure 73: Michelson-Morley interferometer light paths when apparatus moves through the aether along sc."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 8.0
    sw_thin = 6.5

    y_axis = 1468.0
    y_mir = 40.0

    # Horizontal optical axis s -> a -> a1 -> c
    s.line(92.0, y_axis, 1906.0, y_axis, stroke_width=sw)

    # Top mirror b1-b
    s.line(404.0, y_mir, 658.0, y_mir, stroke_width=9.5)
    # Right mirror c
    s.line(1906.0, 1358.0, 1906.0, 1588.0, stroke_width=9.5)

    # Key points
    ax, a1x = 464.0, 606.0
    b1x, bx = 446.0, 524.0

    # Vertical dashed line b1 -> a
    s.line(b1x, y_mir, ax, y_axis, stroke_width=sw_thin, dash="28,18")

    # Slanted rays: a -> b -> a1 -> e (inside telescope)
    s.line(ax, y_axis, bx, y_mir, stroke_width=sw_thin)
    s.line(bx, y_mir, a1x, y_axis, stroke_width=sw_thin)
    s.line(a1x, y_axis, 616.0, 1796.0, stroke_width=sw_thin)

    # Two parallel 45-degree beam splitters at a and a1
    s.line(350.0, 1582.0, 562.0, 1372.0, stroke_width=9.0)
    s.line(490.0, 1582.0, 706.0, 1372.0, stroke_width=9.0)

    # Observing telescope d-e-f below a1
    tx0, tx1 = 538.0, 650.0
    ty0, ty1 = 1606.0, 1962.0
    # Objective lens d (small flat ellipse at top of tube)
    s.ellipse(0.5 * (tx0 + tx1), ty0, 0.5 * (tx1 - tx0), 12.0, stroke_width=sw_thin)
    # Main tube walls
    s.line(tx0, ty0, tx0, ty1, stroke_width=sw_thin)
    s.line(tx1, ty0, tx1, ty1, stroke_width=sw_thin)
    # Shoulder to eyepiece
    s.line(tx0, ty1, 566.0, ty1, stroke_width=sw_thin)
    s.line(620.0, ty1, tx1, ty1, stroke_width=sw_thin)
    # Eyepiece f
    s.polyline([(566.0, ty1), (566.0, 2022.0), (620.0, 2022.0), (620.0, ty1)], stroke_width=sw_thin)
    # Focus dot e
    lib.filled_dot(s, 616.0, 1796.0, r=9.0)

    # Labels
    lib.label(s, 405.0, 76.0, "b\u2081", size=50.0, italic=True, bold=True)
    lib.label(s, 560.0, 76.0, "b", size=50.0, italic=True, bold=True)
    lib.label(s, 62.0, 1474.0, "s", size=52.0, italic=True, bold=True)
    lib.label(s, 412.0, 1432.0, "a", size=50.0, italic=True, bold=True)
    lib.label(s, 656.0, 1506.0, "a\u2081", size=50.0, italic=True, bold=True)
    lib.label(s, 1874.0, 1510.0, "c", size=50.0, italic=True, bold=True)
    lib.label(s, 694.0, 1606.0, "d", size=50.0, italic=True, bold=True)
    lib.label(s, 612.0, 1844.0, "e", size=48.0, italic=True, bold=True)
    lib.label(s, 536.0, 1986.0, "f", size=50.0, italic=True, bold=True)

    s.save(out_svg)
