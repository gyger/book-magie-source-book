"""Figure 92: Faraday's ice-pail electrostatic induction experiment (single vessel A)."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 7.5
    # Ice-pail vessel A (U-shaped with rounded bottom corners)
    d_pail = (
        "M 10 158 L 10 784 "
        "Q 10 882, 106 882 "
        "L 466 882 "
        "Q 562 882, 562 784 "
        "L 562 156"
    )
    s.path(d_pail, stroke_width=sw)

    # Silk thread suspending carrier sphere C
    s.line(283.0, 0.0, 283.0, 411.0, stroke_width=sw)
    s.circle(283.0, 498.0, 87.0, fill="#ffffff", stroke_width=sw * 0.85)

    # Connecting wire from vessel A to gold-leaf electrometer E
    d_wire = "M 562 732 C 646 786, 720 828, 766 862 Q 792 872, 818 870"
    s.path(d_wire, stroke_width=sw)

    # Gold-leaf electrometer E
    s.circle(838.0, 892.0, 34.0, fill="#ffffff", stroke_width=sw * 0.9)
    s.line(831.0, 926.0, 831.0, 1046.0, stroke_width=6.0)
    s.line(844.0, 926.0, 844.0, 1046.0, stroke_width=6.0)
    # Diverging gold leaves
    s.line(831.0, 1046.0, 812.0, h - 1.0, stroke_width=6.5)
    s.line(844.0, 1046.0, 859.0, h - 1.0, stroke_width=6.5)

    # Labels
    lib.label(s, 283.0, 496.0, "C", size=68.0, italic=False, bold=True)
    lib.label(s, 594.0, 438.0, "A", size=72.0, italic=False, bold=True)
    lib.label(s, 840.0, 822.0, "E", size=68.0, italic=False, bold=True)

    s.save(out_svg)
