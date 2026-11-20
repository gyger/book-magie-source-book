"""Figure 54: Fermat's principle of least time applied to the refraction of light."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 7.0
    sw_thin = 5.5

    cx, cy, r = 420.5, 396.0, 362.5

    # Main circle ACBI
    s.circle(cx, cy, r, stroke_width=sw)

    # Horizontal diameter AB
    s.line(cx - r, cy, cx + r, cy, stroke_width=sw_thin)

    # Points C (upper-left on circle) and I (lower-right on circle)
    c_pt = (114.0, 211.0)
    i_pt = (611.0, 702.0)
    d_pt = (cx, cy)

    # Rays C-D, D-I, and chord C-O-I
    s.line(c_pt[0], c_pt[1], d_pt[0], d_pt[1], stroke_width=sw)
    s.line(d_pt[0], d_pt[1], i_pt[0], i_pt[1], stroke_width=sw)
    s.line(c_pt[0], c_pt[1], i_pt[0], i_pt[1], stroke_width=sw_thin)

    # Vertical dashed perpendiculars CF and HI
    s.line(c_pt[0], c_pt[1], c_pt[0], cy, stroke_width=sw_thin, dash="22,16")
    s.line(i_pt[0], cy, i_pt[0], i_pt[1], stroke_width=sw_thin, dash="22,16")

    # Labels
    lib.label(s, 52.0, 224.0, "C", size=64.0, italic=False, bold=True)
    lib.label(s, 24.0, 405.0, "A", size=64.0, italic=False, bold=True)
    lib.label(s, 118.0, 444.0, "F", size=64.0, italic=False, bold=True)
    lib.label(s, 300.0, 434.0, "O", size=64.0, italic=False, bold=True)
    lib.label(s, 442.0, 355.0, "D", size=64.0, italic=False, bold=True)
    lib.label(s, 605.0, 356.0, "H", size=64.0, italic=False, bold=True)
    lib.label(s, 822.0, 404.0, "B", size=64.0, italic=False, bold=True)
    lib.label(s, 612.0, 742.0, "I", size=64.0, italic=False, bold=True)

    s.save(out_svg)
