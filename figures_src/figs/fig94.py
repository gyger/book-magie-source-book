"""Figure 94: Joule's tangent galvanometer coil and needle."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 7.0
    # Horizontal baseboard top and vertical table sides
    s.line(90.0, 332.0, 1448.0, 332.0, stroke_width=sw)
    s.line(18.0, 322.0, 20.0, h - 1.0, stroke_width=sw)
    s.line(1446.0, 332.0, 1448.0, h - 1.0, stroke_width=sw)

    # Left terminal twist loop
    d_twist = (
        "M 18 322 Q 46 322, 54 352 Q 62 380, 78 380 "
        "Q 90 380, 90 332 L 210 332"
    )
    s.path(d_twist, stroke_width=sw * 0.9)
    s.path("M 18 328 Q 42 332, 46 356 Q 50 382, 66 376 Q 74 370, 70 350 Q 66 332, 90 326", stroke_width=sw * 0.85)

    # Upper solid wire loop A -> top -> B
    d_upper = (
        "M 204 332 Q 228 326, 228 294 "
        "L 228 60 Q 228 20, 268 20 "
        "L 1354 18 Q 1396 18, 1396 60 "
        "L 1396 332"
    )
    s.path(d_upper, stroke_width=sw)

    # Lower dashed wire loop (hidden behind board)
    d_lower = (
        "M 206 334 Q 228 344, 228 370 "
        "L 228 566 Q 228 606, 268 606 "
        "L 1358 608 Q 1400 608, 1400 568 "
        "L 1400 334"
    )
    s.path(d_lower, stroke_width=sw * 0.9, dash="22,16")

    # Magnetic needle N resting on pivot on top of baseboard
    d_needle = (
        "M 714 332 L 714 316 Q 714 312, 720 312 "
        "L 892 312 L 892 300 L 916 300 L 916 312 "
        "L 1076 312 Q 1082 312, 1082 316 L 1082 332"
    )
    s.path(d_needle, stroke_width=sw * 0.8)
    s.line(904.0, 300.0, 904.0, 332.0, stroke_width=sw * 0.7)

    # Labels
    lib.label(s, 190.0, 250.0, "A", size=66.0, italic=False, bold=True)
    lib.label(s, 782.0, 248.0, "N", size=66.0, italic=False, bold=True)
    lib.label(s, 1428.0, 252.0, "B", size=66.0, italic=False, bold=True)
    lib.label(s, 782.0, 502.0, "C", size=66.0, italic=False, bold=True)

    s.save(out_svg)
