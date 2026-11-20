"""Figure 88: Seebeck bismuth-copper rectangular thermoelectric circuit."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 9.0
    # Left vertical bismuth bar B (rectangular strip)
    s.rect(146.0, 94.0, 48.0, 466.0, fill="none", stroke_width=sw)

    # Top and bottom copper arms K meeting curved right end
    d_loop = (
        "M 194 94 L 1922 94 "
        "Q 2022 325, 1894 560 "
        "L 194 560"
    )
    s.path(d_loop, stroke_width=sw)

    # Magnetic compass needle s-n in center
    s.line(566.0, 322.0, 1536.0, 322.0, stroke_width=7.0)
    # Pivot double vertical marks
    s.line(1051.0, 304.0, 1051.0, 338.0, stroke_width=6.0)
    s.line(1067.0, 304.0, 1067.0, 338.0, stroke_width=6.0)

    # Labels
    lib.label(s, 48.0, 325.0, "S", size=90.0, italic=True, bold=True)
    lib.label(s, 174.0, 325.0, "B", size=88.0, italic=True, bold=True)
    lib.label(s, 396.0, 56.0, "a", size=68.0, italic=True, bold=True)
    lib.label(s, 1042.0, 82.0, "K", size=78.0, italic=True, bold=True)
    lib.label(s, 580.0, 286.0, "s", size=64.0, italic=True, bold=True)
    lib.label(s, 1524.0, 286.0, "n", size=64.0, italic=True, bold=True)
    lib.label(s, 392.0, 546.0, "b", size=64.0, italic=True, bold=True)
    lib.label(s, 286.0, 596.0, "warm", size=60.0, italic=True, bold=True)
    lib.label(s, 1042.0, 548.0, "K", size=78.0, italic=True, bold=True)
    lib.label(s, 1742.0, 505.0, "östl.", size=58.0, italic=True, bold=True)
    lib.label(s, 2028.0, 305.0, "N", size=90.0, italic=True, bold=True)

    s.save(out_svg)
