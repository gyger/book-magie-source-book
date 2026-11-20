"""Figure 31: Two vertical rectangular prisms / pipes connected at base B with level line AC."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 7.5

    # --- Left prism ---
    l_bl = (68.0, 130.0)
    l_br = (127.0, 130.0)
    l_fr = (87.0, 166.0)
    l_fl = (28.0, 166.0)

    l_fl_bot = (31.0, 645.0)
    l_fr_bot = (89.0, 645.0)
    l_br_bot = (132.0, 608.0)

    # Inner vertical visible inside open top
    s.line(l_bl[0], l_bl[1], l_bl[0], 166.0, stroke_width=sw)
    # Top rim
    s.polygon([l_bl, l_br, l_fr, l_fl], stroke_width=sw)
    # Vertical edges
    s.line(*l_fl, *l_fl_bot, stroke_width=sw)
    s.line(*l_fr, *l_fr_bot, stroke_width=sw)
    # Back-right vertical (goes behind bridge at y=557..591)
    s.line(l_br[0], l_br[1], 131.0, 557.0, stroke_width=sw)
    s.line(132.0, 591.0, *l_br_bot, stroke_width=sw)
    # Bottom right diagonal
    s.line(*l_br_bot, *l_fr_bot, stroke_width=sw)

    # --- Right prism ---
    r_bl = (253.0, 30.0)
    r_br = (304.0, 30.0)
    r_fr = (267.0, 72.0)
    r_fl = (207.0, 69.0)

    r_fl_bot = (212.0, 645.0)
    r_fr_bot = (272.0, 645.0)
    r_br_bot = (308.0, 610.0)

    # Inner vertical visible inside open top
    s.line(r_bl[0], r_bl[1], r_bl[0], 71.0, stroke_width=sw)
    # Top rim
    s.polygon([r_bl, r_br, r_fr, r_fl], stroke_width=sw)
    # Vertical edges
    s.line(*r_fl, *r_fl_bot, stroke_width=sw)
    s.line(*r_fr, *r_fr_bot, stroke_width=sw)
    s.line(*r_br, *r_br_bot, stroke_width=sw)
    # Bottom right diagonal
    s.line(*r_br_bot, *r_fr_bot, stroke_width=sw)

    # --- Horizontal level line AC ---
    s.line(87.0, 166.0, 268.0, 166.0, stroke_width=6.0)

    # --- Connecting bridge at B ---
    # Top face
    s.polygon(
        [(107.0, 574.0), (128.0, 557.0), (211.0, 557.0), (211.0, 574.0)],
        fill="#ffffff",
        stroke="#000000",
        stroke_width=sw,
    )
    # Front face
    s.rect(107.0, 574.0, 104.0, 17.0, fill="#ffffff", stroke="#000000", stroke_width=sw)

    # Labels
    lib.label(s, 162.0, 134.0, "A", size=58.0, italic=False, bold=True)
    lib.label(s, 238.0, 134.0, "C", size=58.0, italic=False, bold=True)
    lib.label(s, 166.0, 620.0, "B", size=58.0, italic=False, bold=True)

    s.save(out_svg)
