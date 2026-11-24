"""Figure 18: Circle with two vertical chords EG and HK."""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    cx, cy, r = 546.5, 485.5, 457.5
    sw = 8.5

    s.circle(cx, cy, r, stroke_width=sw)

    # Vertical chords clipped precisely to circle
    for x_c in (234.0, 849.5):
        dy = math.sqrt(max(0.0, r * r - (x_c - cx) ** 2))
        s.line(x_c, cy - dy, x_c, cy + dy, stroke_width=sw)

    lib.label(s, 224, 108, "E", size=56, italic=False, bold=True)
    lib.label(s, 866, 108, "H", size=56, italic=False, bold=True)
    lib.label(s, 42, 488, "F", size=56, italic=False, bold=True)
    lib.label(s, 1032, 488, "I", size=56, italic=False, bold=True)
    lib.label(s, 212, 850, "G", size=56, italic=False, bold=True)
    lib.label(s, 842, 862, "K", size=56, italic=False, bold=True)

    s.save(out_svg)
