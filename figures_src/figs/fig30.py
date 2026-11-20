"""Figure 30: Vertical rectangular prism / organ pipe AB."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 8.5

    # Top rim quadrilateral (back-left, back-right, front-right, front-left)
    bl = (86.0, 31.0)
    br = (176.0, 29.0)
    fr = (237.0, 86.0)
    fl = (145.0, 84.0)

    # Bottom endpoints (matching slight scan tilt)
    bl_bot = (79.0, 650.0)
    fl_bot = (139.0, 705.0)
    fr_bot = (232.0, 705.0)

    # Back-right inner vertical visible inside open top
    s.line(br[0], br[1], br[0], 84.0, stroke_width=sw)

    # Top rim
    s.polygon([bl, br, fr, fl], stroke_width=sw)

    # Vertical edges
    s.line(*bl, *bl_bot, stroke_width=sw)
    s.line(*fl, *fl_bot, stroke_width=sw)
    s.line(*fr, *fr_bot, stroke_width=sw)

    # Bottom left diagonal edge
    s.line(*bl_bot, 132.0, 705.0, stroke_width=sw)

    # Horizontal reference line under A
    s.line(37.0, 83.0, 130.0, 83.0, stroke_width=7.5)

    # Labels
    lib.label(s, 50.0, 48.0, "A", size=62.0, italic=False, bold=True)
    lib.label(s, 42.0, 619.0, "B", size=62.0, italic=False, bold=True)

    s.save(out_svg)
