"""Figure 11: Stevinus's right-angled inclined plane ABC with weights D and E over F."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    scene = draw.Scene(w, h)

    sw = 7.5

    # Right triangle ABC
    ax, ay = 30.0, 657.5
    cx, cy = 840.5, 657.5
    bx, by = 840.5, 186.0
    scene.polygon([(ax, ay), (bx, by), (cx, cy)], stroke_width=sw)

    # Corner F above-right of B
    fx, fy = 890.0, 88.0

    # Ball D on plane AB and hanging ball E tangent to vertical BC
    dx, dy, dr = 328.0, 414.0, 62.0
    ex, ey, er = 888.0, 404.0, 48.0

    # Cord from D over F down to E
    scene.polyline([(dx, dy), (fx, fy), (ex, ey)], stroke_width=sw)

    # Balls (unfilled so cord visibly terminates at centers as in woodcut)
    scene.circle(dx, dy, dr, fill="none", stroke="#000000", stroke_width=sw)
    scene.circle(ex, ey, er, fill="none", stroke="#000000", stroke_width=sw)

    # Labels
    lib.label(scene, 56, 702, "A", size=58, italic=False, bold=True)
    lib.label(scene, 842, 162, "B", size=58, italic=False, bold=True)
    lib.label(scene, 836, 694, "C", size=58, italic=False, bold=True)
    lib.label(scene, 218, 412, "D", size=58, italic=False, bold=True)
    lib.label(scene, 968, 412, "E", size=58, italic=False, bold=True)
    lib.label(scene, 886, 52, "F", size=58, italic=False, bold=True)

    scene.save(out_svg)
