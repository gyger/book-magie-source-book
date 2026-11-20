"""Figure 20: Solid segment F'P with dotted triangle PCp and vertical fCp."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    F_pt = (92.4, 98.0)
    P = (218.5, 638.0)
    f_top = (425.0, 140.0)
    C = (426.5, 639.0)
    p_bot = (427.6, 768.0)

    # Solid line F'P
    s.line(*F_pt, *P, stroke_width=8.5)

    # Dotted vertical f-C-p (wide dot spacing matching scan)
    s.line(*f_top, *p_bot, stroke_width=8.5, dash="1,34", linecap="round")
    # Dotted horizontal P-C and diagonal P-p (finer dot spacing)
    s.line(*P, *C, stroke_width=7.5, dash="1,22", linecap="round")
    s.line(*P, *p_bot, stroke_width=7.5, dash="1,20", linecap="round")

    lib.label(s, 86, 72, "F'", size=58, italic=False, bold=True)
    lib.label(s, 426, 104, "f", size=62, italic=True, bold=True)
    lib.label(s, 170, 638, "P", size=58, italic=False, bold=True)
    lib.label(s, 464, 642, "C", size=56, italic=False, bold=True)
    lib.label(s, 456, 774, "p", size=60, italic=True, bold=True)

    s.save(out_svg)
