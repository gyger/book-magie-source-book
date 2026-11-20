"""Figure 15: Parallelogram ABCD with diagonal AD."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    A = (52.6, 82.8)
    B = (854.8, 85.4)
    C = (168.5, 532.9)
    D = (977.3, 536.2)

    sw = 9.0
    s.polygon([A, B, D, C], stroke_width=sw)
    s.line(*A, *D, stroke_width=sw)

    lib.label(s, 58, 46, "A", size=58, italic=False, bold=True)
    lib.label(s, 836, 46, "B", size=58, italic=False, bold=True)
    lib.label(s, 172, 570, "C", size=58, italic=False, bold=True)
    lib.label(s, 968, 570, "D", size=58, italic=False, bold=True)

    s.save(out_svg)
