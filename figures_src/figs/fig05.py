"""Figure 5: Vertical line with marks T, X, Y (Galileo)."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    scene = draw.Scene(w, h)

    sw = 10.5
    x0 = 134.5

    # Vertical line from top to Y
    scene.line(x0, 2.0, x0, 560.0, stroke_width=sw)

    # Tick marks at T, X, Y
    for ty in (119.0, 250.0, 558.0):
        scene.line(x0 - 14.0, ty, x0 + 14.0, ty, stroke_width=8.0)

    # Labels
    lib.label(scene, 178, 114, "T", size=58, italic=False, bold=True)
    lib.label(scene, 180, 246, "X", size=58, italic=False, bold=True)
    lib.label(scene, 180, 556, "Y", size=58, italic=False, bold=True)

    scene.save(out_svg)
