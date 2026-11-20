"""Figure 10: Stevinus's inclined plane with two weights D and E connected over vertex F."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    scene = draw.Scene(w, h)

    sw = 7.5

    # Triangle ABC
    ax, ay = 40.0, 513.5
    cx, cy = 1046.0, 513.5
    bx, by = 846.0, 114.0
    scene.polygon([(ax, ay), (bx, by), (cx, cy)], stroke_width=sw)

    # Corner F above B where cord turns
    fx, fy = 856.0, 38.0

    # Ball D on plane AB and ball E on plane BC
    dx, dy, dr = 366.0, 282.0, 62.0
    ex, ey, er = 992.0, 314.0, 40.0

    # Cord from D over F to E
    scene.polyline([(dx, dy), (fx, fy), (ex, ey)], stroke_width=sw)

    # Balls drawn on top with white fill so cord terminates cleanly at rims
    scene.circle(dx, dy, dr, fill="#ffffff", stroke="#000000", stroke_width=sw)
    scene.circle(ex, ey, er, fill="#ffffff", stroke="#000000", stroke_width=sw)

    # Labels (excluding clipped caption fragments at very bottom)
    lib.label(scene, 56, 548, "A", size=54, italic=False, bold=True)
    lib.label(scene, 830, 160, "B", size=54, italic=False, bold=True)
    lib.label(scene, 1034, 548, "C", size=54, italic=False, bold=True)
    lib.label(scene, 266, 286, "D", size=54, italic=False, bold=True)
    lib.label(scene, 1066, 316, "E", size=54, italic=False, bold=True)
    lib.label(scene, 838, 22, "F", size=54, italic=False, bold=True)

    scene.save(out_svg)
