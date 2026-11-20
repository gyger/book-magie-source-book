"""Figure 64: Grimaldi's diffraction fringes — shadow X flanked by colored bands M, P, S bounded by N, O, Q, R, T, V."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 7.0
    y0, y1 = 86.0, 862.0

    # Left shadow bar X: rectangle x = 22..166
    x0, x1 = 22.0, 166.0
    s.rect(x0, y0, x1 - x0, y1 - y0, stroke_width=sw)

    # Horizontal hatching inside shadow bar X
    y = y0 + 13.0
    while y < y1 - 6.0:
        s.line(x0, y, x1, y, stroke_width=4.8)
        y += 13.5

    # White background cutout behind central X label
    s.rect(58.0, 434.0, 74.0, 72.0, fill="#ffffff", stroke="none")
    lib.label(s, 96.0, 472.0, "X", size=68.0, italic=False, bold=True)

    # Exact measured vertical fringe boundary lines (9 lines)
    for lx in (194.0, 271.0, 301.0, 323.0, 379.0, 401.0, 425.0, 481.0, 506.0):
        s.line(lx, y0, lx, y1, stroke_width=6.5)

    # Top and bottom labels N O Q R T V
    top_y = 44.0
    bot_y = 902.0
    for txt, lx in [
        ("N", 174.0),
        ("O", 258.0),
        ("Q", 312.0),
        ("R", 374.0),
        ("T", 434.0),
        ("V", 492.0),
    ]:
        lib.label(s, lx, top_y, txt, size=56.0, italic=False, bold=True)
        lib.label(s, lx, bot_y, txt, size=56.0, italic=False, bold=True)

    # Middle band labels M, P, S
    lib.label(s, 232.0, 466.0, "M", size=54.0, italic=False, bold=True)
    lib.label(s, 351.0, 466.0, "P", size=54.0, italic=False, bold=True)
    lib.label(s, 453.0, 466.0, "S", size=54.0, italic=False, bold=True)

    s.save(out_svg)
