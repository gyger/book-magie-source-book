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
    fx, fy = 82.0, 1286.0

    # Horizontal line C-A-B-D at y = 325
    y_line = 325.0
    s.line(205.0, y_line, 636.0, y_line, stroke_width=sw)

    # Points on horizontal line
    cx, ax, bx, dx = 310.0, 362.0, 518.0, 582.0

    # 4 rays from F up to C, A, B, D
    for px in (cx, ax, bx, dx):
        s.line(fx, fy, px, y_line, stroke_width=sw_thin)

    # Dashed near-vertical line E-A (slight lean: top (370, 38) -> A(352, 325) -> bottom E(292, 1288))
    s.line(370.0, 38.0, 292.0, 1288.0, stroke_width=sw_thin, dash="24,14")

    # Dashed vertical line G-B (top (506, 34) -> B(504, 325) -> bottom G(496, 1288))
    s.line(506.0, 34.0, 496.0, 1288.0, stroke_width=sw_thin, dash="24,14")

    # Labels
    lib.label(s, 296.0, 290.0, "C", size=48.0, italic=False, bold=True)
    lib.label(s, 382.0, 290.0, "A", size=48.0, italic=False, bold=True)
    lib.label(s, 526.0, 290.0, "B", size=48.0, italic=False, bold=True)
    lib.label(s, 574.0, 290.0, "D", size=48.0, italic=False, bold=True)
    lib.label(s, 44.0, 1264.0, "F", size=50.0, italic=False, bold=True)
    lib.label(s, 250.0, 1264.0, "E", size=50.0, italic=False, bold=True)
    lib.label(s, 456.0, 1264.0, "G", size=50.0, italic=False, bold=True)

    s.save(out_svg)
