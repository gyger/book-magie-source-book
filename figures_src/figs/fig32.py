"""Figure 32: Vertical rectangular prism with dashed adjacent air column C."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.5

    # --- Left prism ---
    bl = (96.0, 79.0)
    br = (179.0, 78.0)
    fr = (124.0, 131.0)
    fl = (46.0, 131.0)

    fl_bot = (47.0, 675.0)
    fr_bot = (125.0, 675.0)
    br_mid = (183.0, 591.0)

    # Inner vertical visible inside open top
    s.line(bl[0], bl[1], bl[0], 131.0, stroke_width=sw)
    # Top rim
    s.polygon([bl, br, fr, fl], stroke_width=sw)
    # Vertical edges
    s.line(*fl, *fl_bot, stroke_width=sw)
    s.line(*fr, *fr_bot, stroke_width=sw)
    s.line(*br, *br_mid, stroke_width=sw)
    # Bottom right diagonal (below foot block)
    s.line(180.0, 637.0, 132.0, 675.0, stroke_width=sw)

    # --- Horizontal reference line under D ---
    s.line(146.0, 131.0, 267.0, 131.0, stroke_width=5.5)

    # --- Foot block at B ---
    # Top face
    s.polygon(
        [(147.0, 616.0), (170.0, 592.0), (247.0, 592.0), (225.0, 616.0)],
        fill="#ffffff",
        stroke="#000000",
        stroke_width=sw,
    )
    # Front face
    s.rect(147.0, 616.0, 78.0, 21.0, fill="#ffffff", stroke="#000000", stroke_width=sw)
    # Right side face
    s.polygon(
        [(225.0, 616.0), (247.0, 592.0), (247.0, 612.0), (225.0, 637.0)],
        fill="#ffffff",
        stroke="#000000",
        stroke_width=sw,
    )

    # --- Dashed air column C ---
    # Smooth closed loop starting at bottom-left inside top of foot block
    d_col = (
        "M 200 603 "
        "L 199 182 "
        "C 199 124, 256 122, 267 182 "
        "L 293 603 "
        "Z"
    )
    s.path(d_col, stroke_width=5.5, dash="18,12")

    # Labels
    lib.label(s, 96.0, 45.0, "A", size=56.0, italic=False, bold=True)
    lib.label(s, 224.0, 99.0, "D", size=54.0, italic=False, bold=True)
    lib.label(s, 228.0, 197.0, "C", size=56.0, italic=False, bold=True)
    lib.label(s, 225.0, 551.0, "B", size=56.0, italic=False, bold=True)
    lib.label(s, 266.0, 636.0, "E", size=54.0, italic=False, bold=True)

    s.save(out_svg)
