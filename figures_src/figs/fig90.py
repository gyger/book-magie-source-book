"""Figure 90: Ohm's thermoelectric tin vessels A (boiling water) and B (ice)."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 7.5
    # === Vessel A (left, boiling water) ===
    # Main vessel walls and bottom
    s.polyline([(306.0, 210.0), (306.0, 626.0), (702.0, 626.0), (702.0, 210.0)], stroke_width=sw)
    # Top deck segments
    s.line(306.0, 210.0, 364.0, 210.0, stroke_width=sw)
    s.line(408.0, 210.0, 452.0, 210.0, stroke_width=sw)
    s.line(558.0, 210.0, 604.0, 210.0, stroke_width=sw)
    s.line(652.0, 210.0, 702.0, 210.0, stroke_width=sw)

    # Central recess x-x in vessel A
    s.polyline([(452.0, 210.0), (452.0, 552.0), (558.0, 552.0), (558.0, 210.0)], stroke_width=sw)

    # Funnel y on top right of A
    s.line(604.0, 210.0, 588.0, 168.0, stroke_width=sw)
    s.line(652.0, 210.0, 678.0, 168.0, stroke_width=sw)

    # Curved steam exhaust pipe z-z on top left of A
    s.path("M 364 210 C 330 110, 200 104, 96 228", stroke_width=sw)
    s.path("M 408 210 C 370 50, 180 42, 60 198", stroke_width=sw)
    s.polyline([(60.0, 198.0), (76.0, 208.0), (80.0, 218.0), (96.0, 228.0)], stroke_width=sw * 0.85)

    # Stand legs and crossbar under vessel A
    s.line(306.0, 626.0, 192.0, 1110.0, stroke_width=sw)
    s.line(702.0, 626.0, 822.0, 1138.0, stroke_width=sw)
    s.line(246.0, 878.0, 762.0, 878.0, stroke_width=sw)

    # Spirit lamp and flame
    s.rect(420.0, 778.0, 174.0, 100.0, fill="#ffffff", stroke_width=sw * 0.9)
    d_flame = (
        "M 494 778 C 468 746, 470 704, 488 674 "
        "C 496 658, 504 646, 508 634 "
        "C 514 648, 524 662, 534 680 "
        "C 554 714, 554 750, 518 778"
    )
    s.path(d_flame, stroke_width=sw * 0.75)
    s.path("M 502 778 C 492 752, 496 720, 508 696 C 520 722, 522 752, 512 778", stroke_width=sw * 0.55)

    # === Vessel B (right, melting ice) ===
    s.polyline([(1066.0, 210.0), (1164.0, 626.0), (w - 1.0, 626.0)], stroke_width=sw)
    s.line(1164.0, 626.0, 1066.0, 1116.0, stroke_width=sw)

    # Central recess x-x in vessel B
    s.polyline([(1390.0, 214.0), (1390.0, 552.0), (1498.0, 552.0), (1498.0, 214.0)], stroke_width=sw)
    # Dashed extensions to bottom of vessel B
    s.line(1392.0, 552.0, 1392.0, 626.0, stroke_width=sw * 0.85, dash="14,10")
    s.line(1500.0, 552.0, 1500.0, 626.0, stroke_width=sw * 0.85, dash="14,10")

    # Labels
    lib.label(s, 30.0, 190.0, "z", size=64.0, italic=True, bold=True)
    lib.label(s, 426.0, 186.0, "z", size=60.0, italic=True, bold=True)
    lib.label(s, 506.0, 224.0, "x", size=64.0, italic=True, bold=True)
    lib.label(s, 508.0, 526.0, "x", size=64.0, italic=True, bold=True)
    lib.label(s, 734.0, 200.0, "y", size=64.0, italic=True, bold=True)
    lib.label(s, 734.0, 490.0, "A", size=66.0, italic=True, bold=True)
    lib.label(s, 1092.0, 490.0, "B", size=66.0, italic=True, bold=True)
    lib.label(s, 1446.0, 244.0, "x", size=64.0, italic=True, bold=True)
    lib.label(s, 1446.0, 522.0, "x", size=64.0, italic=True, bold=True)

    s.save(out_svg)
