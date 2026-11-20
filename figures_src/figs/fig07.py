"""Figure 7: Inclined plane AB with height AC, point D on AB, and dashed line AE (Galileo)."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    scene = draw.Scene(w, h)

    sw = 8.5

    # Vertices measured from scan
    bx, by = 45.0, 536.5
    cx, cy = 853.5, 536.5
    ax, ay = 852.0, 52.0
    ex, ey = 455.0, 536.5

    # Triangle ABC
    scene.line(bx, by, cx, cy, stroke_width=sw)
    scene.line(cx, cy, ax, ay, stroke_width=sw)
    scene.line(bx, by, ax, ay, stroke_width=sw)

    # Dashed line AE
    scene.line(ax, ay, ex, ey, stroke_width=7.5, dash="30,16")

    # Small tick mark at D on AB
    scene.line(688.0, 138.0, 678.0, 184.0, stroke_width=7.0)

    # Labels
    lib.label(scene, 848, 28, "A", size=60, italic=False, bold=True)
    lib.label(scene, 643, 148, "D", size=60, italic=False, bold=True)
    lib.label(scene, 51, 570, "B", size=60, italic=False, bold=True)
    lib.label(scene, 442, 570, "E", size=60, italic=False, bold=True)
    lib.label(scene, 858, 570, "C", size=60, italic=False, bold=True)

    scene.save(out_svg)
