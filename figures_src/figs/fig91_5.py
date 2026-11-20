"""Figure 91, 5: Faraday's law of electromagnetic induction — wire cutting magnetic curves."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.0
    # Horizontal cylindrical magnet pole
    s.line(158.0, 152.0, 642.0, 150.0, stroke_width=sw)
    s.line(158.0, 256.0, w - 2.0, 256.0, stroke_width=sw)
    s.ellipse(158.0, 204.0, 24.0, 52.0, fill="#ffffff", stroke_width=sw)
    s.ellipse(154.0, 204.0, 18.0, 48.0, fill="none", stroke_width=sw * 0.7)

    # Vertical wire N'-P' (double outline passing in front of magnet)
    s.rect(322.0, 68.0, 12.0, 316.0, fill="#ffffff", stroke_width=sw * 0.85, rx=4.0)

    # Oblique wire P-N
    d_oblique = "M 214 294 L 224 290 L 356 515 L 342 515 Z"
    s.path(d_oblique, fill="#ffffff", stroke_width=sw * 0.85)

    # Outer dashed magnetic curve arching around pole
    d_arc_top = "M 312 24 C 190 -24, 30 34, 4 162"
    d_arc_bot = "M 4 272 C 42 400, 150 442, 272 412"
    s.path(d_arc_top, stroke_width=sw, dash="30,18")
    s.path(d_arc_bot, stroke_width=sw, dash="30,18")
    # Arrowheads on outer curve
    lib.arrow(s, 140.0, 8.0, 170.0, 4.0, stroke_width=1.0, head_len=24.0, head_w=16.0)
    lib.arrow(s, 12.0, 134.0, 4.0, 156.0, stroke_width=1.0, head_len=24.0, head_w=16.0)
    lib.arrow(s, 118.0, 404.0, 92.0, 392.0, stroke_width=1.0, head_len=24.0, head_w=16.0)

    # Inner dashed magnetic loop emerging from pole
    d_inner = "M 244 174 C 120 168, 2 184, 2 212 C 2 238, 120 250, 320 246"
    s.path(d_inner, stroke_width=sw, dash="28,16")
    lib.arrow(s, 80.0, 180.0, 108.0, 178.0, stroke_width=1.0, head_len=22.0, head_w=15.0)
    lib.arrow(s, 108.0, 240.0, 80.0, 238.0, stroke_width=1.0, head_len=22.0, head_w=15.0)

    # Labels
    lib.label(s, 372.0, 72.0, "N′", size=72.0, italic=False, bold=True)
    lib.label(s, 368.0, 354.0, "P′", size=72.0, italic=False, bold=True)
    lib.label(s, 178.0, 302.0, "P", size=72.0, italic=False, bold=True)

    s.save(out_svg)
