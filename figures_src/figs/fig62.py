"""Figure 62: Huygens's experiment with two stacked Iceland spar crystals showing polarization of ordinary and extraordinary rays."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 5.5
    sw_thin = 4.5

    # --- Left pair of stacked crystals ---
    # Upper crystal
    s.polygon([(216.0, 178.0), (696.0, 178.0), (585.0, 556.0), (96.0, 556.0)], stroke_width=sw)
    # Lower crystal
    s.polygon([(156.0, 672.0), (610.0, 672.0), (500.0, 1020.0), (42.0, 1020.0)], stroke_width=sw)

    # Normal incident ray A-B-D-G-H
    s.line(478.0, 24.0, 464.0, 1068.0, stroke_width=sw_thin)
    # Extraordinary ray B -> C -> E -> F
    s.line(476.0, 178.0, 425.0, 556.0, stroke_width=sw_thin)
    s.line(425.0, 556.0, 412.0, 672.0, stroke_width=sw_thin)
    s.line(412.0, 672.0, 358.0, 1068.0, stroke_width=sw_thin)

    # Left labels
    lib.label(s, 444.0, 62.0, "A", size=46.0, italic=False, bold=True)
    lib.label(s, 444.0, 146.0, "B", size=46.0, italic=False, bold=True)
    lib.label(s, 392.0, 588.0, "C", size=44.0, italic=False, bold=True)
    lib.label(s, 504.0, 588.0, "D", size=44.0, italic=False, bold=True)
    lib.label(s, 382.0, 704.0, "E", size=44.0, italic=False, bold=True)
    lib.label(s, 498.0, 704.0, "G", size=44.0, italic=False, bold=True)
    lib.label(s, 336.0, 990.0, "F", size=44.0, italic=False, bold=True)
    lib.label(s, 488.0, 990.0, "H", size=44.0, italic=False, bold=True)

    # --- Right pair of stacked crystals ---
    # Upper crystal
    s.polygon([(890.0, 176.0), (1434.0, 176.0), (1320.0, 552.0), (779.0, 552.0)], stroke_width=sw)
    # Lower crystal
    s.polygon([(758.0, 672.0), (1310.0, 672.0), (1200.0, 1018.0), (650.0, 1018.0)], stroke_width=sw)

    # Oblique incident ray A -> B
    bx, by = 1196.0, 176.0
    s.line(1248.0, 26.0, bx, by, stroke_width=sw_thin)
    # Ordinary ray B -> D -> G -> H
    s.line(bx, by, 1118.0, 552.0, stroke_width=sw_thin)
    s.line(1118.0, 552.0, 1094.0, 672.0, stroke_width=sw_thin)
    s.line(1094.0, 672.0, 1028.0, 1068.0, stroke_width=sw_thin)
    # Extraordinary ray B -> C -> E -> F
    s.line(bx, by, 1066.0, 552.0, stroke_width=sw_thin)
    s.line(1066.0, 552.0, 1040.0, 672.0, stroke_width=sw_thin)
    s.line(1040.0, 672.0, 926.0, 1068.0, stroke_width=sw_thin)

    # Right labels
    lib.label(s, 1190.0, 62.0, "A", size=46.0, italic=False, bold=True)
    lib.label(s, 1164.0, 146.0, "B", size=46.0, italic=False, bold=True)
    lib.label(s, 1028.0, 588.0, "C", size=44.0, italic=False, bold=True)
    lib.label(s, 1138.0, 588.0, "D", size=44.0, italic=False, bold=True)
    lib.label(s, 984.0, 704.0, "E", size=44.0, italic=False, bold=True)
    lib.label(s, 1112.0, 704.0, "G", size=44.0, italic=False, bold=True)
    lib.label(s, 898.0, 988.0, "F", size=44.0, italic=False, bold=True)
    lib.label(s, 1060.0, 988.0, "H", size=44.0, italic=False, bold=True)

    s.save(out_svg)
