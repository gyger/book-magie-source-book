"""Figure 111: Wien's canal-ray magnetic and electrostatic deflection apparatus."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 9.0
    # Upper glass tube C (semicircular top centered at (184, 136), r=62)
    d_upper = (
        "M 122 420 L 122 136 "
        "A 62 62 0 0 1 246 136 "
        "L 246 420"
    )
    s.path(d_upper, stroke_width=sw)

    # Magnet poles S (left) and N (right)
    s.polyline([(0.0, 250.0), (114.0, 250.0), (114.0, 420.0)], stroke_width=sw)
    s.polyline([(420.0, 250.0), (258.0, 250.0), (258.0, 420.0)], stroke_width=sw)

    # Perforated iron diaphragm blocks (a, a) with central canal slit
    s.rect(2.0, 420.0, 180.0, 100.0, fill="#ffffff", stroke_width=sw)
    s.rect(204.0, 420.0, 174.0, 100.0, fill="#ffffff", stroke_width=sw)

    # Lower glass tube b (semicircular bottom centered at (188, 1126), r=61)
    d_lower = (
        "M 127 520 L 127 1126 "
        "A 61 61 0 0 0 249 1126 "
        "L 249 520"
    )
    s.path(d_lower, stroke_width=sw)

    # Side deflection plates flanking lower tube b
    s.rect(4.0, 520.0, 80.0, 576.0, fill="#ffffff", stroke_width=sw)
    s.line(4.0, 800.0, 84.0, 800.0, stroke_width=sw * 0.9)
    s.rect(290.0, 520.0, 88.0, 576.0, fill="#ffffff", stroke_width=sw)
    s.line(290.0, 800.0, 378.0, 800.0, stroke_width=sw * 0.9)

    # Anode A (T-shaped electrode at bottom of tube b)
    s.line(156.0, 1150.0, 220.0, 1150.0, stroke_width=sw * 1.1)
    s.line(188.0, 1150.0, 188.0, 1230.0, stroke_width=sw * 1.1)

    # Labels
    lib.label(s, 184.0, 146.0, "C", size=64.0, italic=True, bold=True)
    lib.label(s, 58.0, 350.0, "S", size=64.0, italic=True, bold=True)
    lib.label(s, 340.0, 350.0, "N", size=64.0, italic=True, bold=True)
    lib.label(s, 108.0, 472.0, "a", size=60.0, italic=True, bold=True)
    lib.label(s, 298.0, 472.0, "a", size=60.0, italic=True, bold=True)
    lib.label(s, 190.0, 804.0, "b", size=64.0, italic=True, bold=True)
    lib.label(s, 180.0, 1258.0, "A", size=68.0, italic=True, bold=True)

    s.save(out_svg)
