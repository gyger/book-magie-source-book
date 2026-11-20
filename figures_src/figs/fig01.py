"""Figure 1: Inclined planes AC and DC sharing vertical height CB (Galileo)."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    scene = draw.Scene(w, h)

    sw = 8.5

    # Key vertices measured from 600 DPI scan
    ax, ay = 82.0, 641.5
    bx, by = 1014.5, 641.5
    cx, cy = 1014.5, 76.0
    dx, dy = 470.0, 641.5

    # Triangle ABC and interior inclined plane DC
    scene.line(ax, ay, bx, by, stroke_width=sw)
    scene.line(bx, by, cx, cy, stroke_width=sw)
    scene.line(ax, ay, cx, cy, stroke_width=sw)
    scene.line(dx, dy, cx, cy, stroke_width=sw)

    # Upright bold serif labels matching the original woodcut
    lib.label(scene, 84, 668, "A", size=62, italic=False, bold=True)
    lib.label(scene, 470, 668, "D", size=62, italic=False, bold=True)
    lib.label(scene, 1014, 668, "B", size=62, italic=False, bold=True)
    lib.label(scene, 1009, 48, "C", size=62, italic=False, bold=True)

    scene.save(out_svg)
