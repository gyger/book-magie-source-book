"""Figure 72: Michelson-Morley interferometer schematic with stationary aether (s-a-b, s-a-c, a-d)."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 10.0

    # Center of beam splitter a
    ax, ay = 453.0, 922.0

    # Horizontal optical path s -> a -> c
    s.line(74.0, ay, 1335.0, ay, stroke_width=sw)
    # Vertical optical path b -> a -> d
    s.line(ax, 44.0, ax, 1236.0, stroke_width=sw)

    # Mirror b at top
    s.line(376.0, 44.0, 534.0, 44.0, stroke_width=11.0)
    # Mirror c at right
    s.line(1335.0, 824.0, 1335.0, 1028.0, stroke_width=11.0)
    # 45-degree half-silvered mirror at a
    s.line(312.0, 1064.0, 588.0, 788.0, stroke_width=12.0)

    # Labels
    lib.label(s, 488.0, 82.0, "b", size=58.0, italic=True, bold=True)
    lib.label(s, 44.0, 928.0, "s", size=54.0, italic=True, bold=True)
    lib.label(s, 404.0, 882.0, "a", size=58.0, italic=True, bold=True)
    lib.label(s, 1300.0, 882.0, "c", size=56.0, italic=True, bold=True)
    lib.label(s, 496.0, 1200.0, "d", size=58.0, italic=True, bold=True)

    s.save(out_svg)
