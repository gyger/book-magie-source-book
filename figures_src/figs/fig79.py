"""Figure 79: Gilbert's versorium (pivoted electroscope needle)."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 7.0
    # Needle shaft (two parallel horizontal edges on either side of central pivot cap)
    s.line(82.0, 62.0, 417.0, 62.0, stroke_width=sw)
    s.line(80.0, 81.0, 424.0, 81.0, stroke_width=sw)
    s.line(474.0, 66.0, w - 1.0, 65.0, stroke_width=sw)
    s.line(468.0, 84.0, w - 1.0, 84.0, stroke_width=sw)

    # Left arrowhead (hollow curved barb)
    d_head = (
        "M 82 62 "
        "Q 96 42, 102 22 "
        "Q 64 56, 4 69 "
        "Q 64 88, 104 123 "
        "Q 95 100, 80 81"
    )
    s.path(d_head, stroke_width=sw)

    # Central pivot cap (rounded diamond/circle)
    d_cap = (
        "M 417 65 "
        "Q 432 36, 445 36 "
        "Q 460 36, 474 65 "
        "Q 460 83, 445 83 "
        "Q 430 83, 417 65 Z"
    )
    s.path(d_cap, fill="#ffffff", stroke_width=sw)

    # Vertical pivot needle tapering down and flaring into domed base
    d_stem_l = "M 442 83 L 438 242 Q 434 268, 405 272"
    d_stem_r = "M 450 83 L 456 242 Q 460 268, 479 272"
    s.path(d_stem_l, stroke_width=sw)
    s.path(d_stem_r, stroke_width=sw)

    # Domed circular base (left and right arcs meeting stem)
    d_base_l = "M 326 297 C 326 260, 380 238, 438 238"
    d_base_r = "M 456 238 C 512 238, 562 260, 562 297"
    s.path(d_base_l, stroke_width=sw)
    s.path(d_base_r, stroke_width=sw)
    # Inner rim hint at bottom of base
    s.path("M 332 276 Q 345 292, 366 297", stroke_width=sw * 0.8)
    s.path("M 556 276 Q 544 292, 524 297", stroke_width=sw * 0.8)

    s.save(out_svg)
