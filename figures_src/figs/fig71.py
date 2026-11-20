"""Figure 71: Bradley's triangle of stellar aberration (CA vertical ray, CB inclined telescope)."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.5

    cx, cy = 249.0, 72.0
    dx, dy = 48.0, 1368.0
    ax, ay = 262.0, 1368.0
    bx, by = 474.0, 1368.0

    # Triangle C-D-B
    s.polygon([(cx, cy), (dx, dy), (bx, by)], stroke_width=sw)

    # Vertical dashed ray C-A
    s.line(cx, cy, ax, ay, stroke_width=sw, dash="22,14")

    # Labels
    lib.label(s, 249.0, 42.0, "C", size=54.0, italic=False, bold=True)
    lib.label(s, 52.0, 1412.0, "D", size=54.0, italic=False, bold=True)
    lib.label(s, 262.0, 1412.0, "A", size=54.0, italic=False, bold=True)
    lib.label(s, 466.0, 1412.0, "B", size=54.0, italic=False, bold=True)

    s.save(out_svg)
