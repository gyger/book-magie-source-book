"""Figure 87: Seebeck thermoelectric circuit with multi-turn copper coil and compass needle."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 7.0
    # Main top and bottom copper strips (K)
    s.line(78.0, 76.0, 1860.0, 74.0, stroke_width=sw)
    s.line(64.0, 358.0, 1916.0, 361.0, stroke_width=sw)

    # Thick bismuth bar B on bottom-left
    s.line(138.0, 330.0, 436.0, 330.0, stroke_width=15.0)

    # Multi-turn coil loops on right side
    d_outer = (
        "M 1146 28 L 1882 28 "
        "C 2026 114, 2026 272, 1916 361"
    )
    s.path(d_outer, stroke_width=sw)
    d_outer_l = (
        "M 1146 28 "
        "C 1054 118, 1054 258, 1144 342 "
        "L 1898 342 "
        "C 1994 258, 1994 128, 1874 52 "
        "L 1164 52"
    )
    s.path(d_outer_l, stroke_width=sw)

    d_inner = (
        "M 1164 52 "
        "C 1084 128, 1084 246, 1158 317 "
        "L 1878 317 "
        "C 1962 246, 1962 138, 1860 74"
    )
    s.path(d_inner, stroke_width=sw)

    # Magnetic compass needle s-n inside the coil
    s.line(1240.0, 197.0, 1775.0, 195.0, stroke_width=5.5)
    # Central pivot double vertical bars
    s.line(1532.0, 180.0, 1532.0, 212.0, stroke_width=5.0)
    s.line(1545.0, 180.0, 1545.0, 212.0, stroke_width=5.0)

    # Labels
    lib.label(s, 42.0, 206.0, "S", size=84.0, italic=True, bold=True)
    lib.label(s, 2044.0, 196.0, "N", size=84.0, italic=True, bold=True)
    lib.label(s, 268.0, 42.0, "a", size=64.0, italic=True, bold=True)
    lib.label(s, 712.0, 68.0, "K", size=72.0, italic=True, bold=True)
    lib.label(s, 318.0, 326.0, "B", size=78.0, italic=True, bold=True)
    lib.label(s, 242.0, 394.0, "b", size=60.0, italic=True, bold=True)
    lib.label(s, 744.0, 344.0, "K", size=72.0, italic=True, bold=True)
    lib.label(s, 1262.0, 162.0, "s", size=62.0, italic=True, bold=True)
    lib.label(s, 1756.0, 160.0, "n", size=62.0, italic=True, bold=True)

    s.save(out_svg)
