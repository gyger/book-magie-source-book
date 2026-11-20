"""Figure 103: Crookes spherical bulb with concave cathode a focusing on platinum strip c."""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.5
    # Spherical glass bulb centered at (484, 616), rx=466, ry=466, with top neck, lower stem & exhaust hook
    d_bulb = (
        "M 412 152 C 412 90, 412 50, 466 50 C 520 50, 536 90, 540 152 "
        "C 776 184, 948 380, 948 616 "
        "C 948 800, 840 946, 728 1020 "
        "C 660 1076, 636 1190, 622 1380 "
        "C 614 1480, 558 1536, 488 1536 "
        "C 424 1536, 376 1500, 356 1446 "
        "C 336 1410, 310 1424, 310 1470 "
        "L 310 1600 Q 290 1660, 266 1600 L 260 1450 "
        "C 260 1396, 316 1384, 344 1364 "
        "C 366 1344, 352 1240, 336 1160 "
        "C 316 1068, 252 1018, 198 972 "
        "C 84 876, 18 756, 18 616 "
        "C 18 378, 184 188, 412 152 Z"
    )
    s.path(d_bulb, stroke_width=sw)

    # Top anode b
    s.circle(466.0, 36.0, 12.0, fill="#ffffff", stroke_width=sw * 0.85)
    s.polygon([(450.0, 48.0), (482.0, 48.0), (474.0, 118.0), (458.0, 118.0)], fill="#ffffff", stroke_width=5.5)
    s.line(466.0, 118.0, 466.0, 134.0, stroke_width=sw)
    s.line(440.0, 134.0, 496.0, 134.0, stroke_width=sw * 1.1)

    # Concave hemispherical cathode cup a along bottom of sphere
    s.path("M 200 956 A 352 352 0 0 0 764 950", stroke_width=sw * 1.4)

    # Supporting glass stem down to bottom pinch seal
    s.path("M 442 1088 Q 478 1220, 470 1420", stroke_width=sw * 0.85)
    s.path("M 518 1088 Q 486 1220, 508 1420", stroke_width=sw * 0.85)
    s.line(486.0, 1088.0, 492.0, 1544.0, stroke_width=sw * 0.9)
    s.polygon([(466.0, 1424.0), (514.0, 1424.0), (534.0, 1528.0), (444.0, 1528.0)], fill="#ffffff", stroke_width=5.5)
    s.circle(492.0, 1556.0, 12.0, fill="#ffffff", stroke_width=sw * 0.85)

    # 7 dashed cathode rays radiating from concave cup a through focus (478, 706)
    fx, fy = 478.0, 706.0
    rays = [
        ((260, 1012), (804, 290)),
        ((328, 1052), (702, 212)),
        ((402, 1078), (596, 174)),
        ((484, 1086), (468, 136)),
        ((584, 1072), (332, 182)),
        ((658, 1034), (226, 236)),
        ((724, 984),  (138, 316)),
    ]
    for (x1, y1), (x2, y2) in rays:
        s.line(float(x1), float(y1), float(x2), float(y2), stroke_width=sw * 0.8, dash="24,16")

    # Platinum strip c passing obliquely through focus (478, 706) to side electrode d
    s.polygon([(404.0, 718.0), (748.0, 622.0), (756.0, 642.0), (428.0, 732.0)], fill="#ffffff", stroke_width=sw * 0.9)
    s.path("M 744 630 Q 770 618, 788 646 Q 820 682, 870 682", stroke_width=sw)
    # Side pinch seal d
    s.polygon([(866.0, 672.0), (944.0, 666.0), (944.0, 706.0), (866.0, 696.0)], fill="#ffffff", stroke_width=5.5)
    s.circle(968.0, 686.0, 12.0, fill="#ffffff", stroke_width=sw * 0.85)

    # Labels
    lib.label(s, 500.0, 104.0, "b", size=64.0, italic=True, bold=True)
    lib.label(s, 670.0, 686.0, "c", size=64.0, italic=True, bold=True)
    lib.label(s, 966.0, 742.0, "d", size=64.0, italic=True, bold=True)
    lib.label(s, 606.0, 1100.0, "a", size=64.0, italic=True, bold=True)

    s.save(out_svg)
