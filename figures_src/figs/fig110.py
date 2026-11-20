"""Figure 110: J.J. Thomson circular cathode-ray trajectory geometry in a magnetic field."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.5
    # Horizontal glass tube with hemispherical ends
    d_tube = (
        "M 180 120 L 966 120 "
        "A 115 115 0 0 1 966 350 "
        "L 180 350 "
        "A 115 115 0 0 1 180 120 Z"
    )
    s.path(d_tube, stroke_width=sw)

    # Cathode lead and disk on left
    s.line(0.0, 236.0, 168.0, 236.0, stroke_width=sw)
    s.line(170.0, 194.0, 170.0, 274.0, stroke_width=14.0)

    # Anode slit diaphragm C (upper and lower rectangular blocks)
    s.rect(354.0, 120.0, 33.0, 95.0, fill="#ffffff", stroke_width=sw * 0.85)
    s.rect(354.0, 252.0, 33.0, 98.0, fill="#ffffff", stroke_width=sw * 0.85)

    # Circular cathode-ray trajectory from slit A=(352, 238) to wall E=(726, 120)
    s.path("M 352 238 Q 550 230, 726 120", stroke_width=sw)

    # Labels
    lib.label(s, 368.0, 82.0, "C", size=68.0, italic=False, bold=True)
    lib.label(s, 422.0, 174.0, "A", size=68.0, italic=False, bold=True)
    lib.label(s, 732.0, 78.0, "E", size=68.0, italic=False, bold=True)

    s.save(out_svg)
