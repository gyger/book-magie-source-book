"""Figure 68: Fresnel's diagram of effective diffracted rays FC, FA, FB, FD."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.0
    sw_thin = 4.8

    # Observation point F at bottom-left
    fx, fy = 90.5, 1300.0

    # Horizontal line C-A-B-D at y = 324: dashed outside A-B, solid between A and B
    y_line = 324.0
    cx, ax, bx, dx = 301.5, 359.0, 512.0, 579.0
    s.line(206.0, y_line, ax, y_line, stroke_width=sw_thin, dash="24,14")
    s.line(ax, y_line, bx, y_line, stroke_width=sw + 1.5)
    s.line(bx, y_line, 649.0, y_line, stroke_width=sw_thin, dash="24,14")

    # 4 rays from F up to C, A, B, D
    for px in (cx, ax, bx, dx):
        s.line(fx, fy, px, y_line, stroke_width=sw_thin)

    # Dashed near-vertical line E-A (top (377, 38) -> A(359, 324) -> bottom E(297, 1300))
    s.line(377.0, 38.0, 297.0, 1300.0, stroke_width=sw_thin, dash="24,14")

    # Dashed vertical line G-B (top (515, 38) -> B(512.5, 324) -> bottom G(504.5, 1300))
    s.line(515.0, 38.0, 504.5, 1300.0, stroke_width=sw_thin, dash="24,14")

    # Labels
    lib.label(s, 302.0, 290.0, "C", size=48.0, italic=False, bold=True)
    lib.label(s, 387.0, 290.0, "A", size=48.0, italic=False, bold=True)
    lib.label(s, 536.0, 290.0, "B", size=48.0, italic=False, bold=True)
    lib.label(s, 586.0, 290.0, "D", size=48.0, italic=False, bold=True)
    lib.label(s, 44.0, 1268.0, "F", size=50.0, italic=False, bold=True)
    lib.label(s, 258.0, 1264.0, "E", size=50.0, italic=False, bold=True)
    lib.label(s, 468.0, 1264.0, "G", size=50.0, italic=False, bold=True)

    s.save(out_svg)
