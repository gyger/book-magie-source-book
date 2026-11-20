"""Figure 109: J.J. Thomson's bell-jar magnetic deflection apparatus."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 8.0
    # Main bell-jar dome on right
    d_jar = (
        "M 508 854 L 508 496 "
        "M 508 260 C 508 100, 624 20, 788 20 "
        "C 962 20, 1066 112, 1066 260 "
        "L 1066 854"
    )
    s.path(d_jar, stroke_width=sw)

    # Base plate at bottom
    s.polyline([(452.0, h - 1.0), (452.0, 854.0), (1100.0, 854.0), (1100.0, h - 1.0)], stroke_width=sw)

    # Side cathode tube attached on left
    d_side = (
        "M 508 260 L 246 260 "
        "A 96 118 0 0 0 246 496 "
        "L 508 496"
    )
    s.path(d_side, stroke_width=sw)

    # Cathode wire and vertical disk inside side tube
    s.line(0.0, 378.0, 236.0, 378.0, stroke_width=sw)
    s.line(238.0, 332.0, 238.0, 428.0, stroke_width=14.0)

    # Metallic slit plug at junction between side tube and bell-jar
    s.rect(468.0, 260.0, 68.0, 104.0, fill="#ffffff", stroke_width=sw)
    s.rect(468.0, 396.0, 68.0, 100.0, fill="#ffffff", stroke_width=sw)

    s.save(out_svg)
