"""Figure 107: J.J. Thomson's modified Perrin bulb with coaxial cylinders and electrometer."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 7.5
    # Main spherical bulb + upper-left cathode bulb A + upper-right side extension + lower long neck
    d_bulb = (
        "M 596 606 C 460 584, 392 464, 412 318 "
        "L 340 278 Q 320 264, 290 272 C 254 282, 224 278, 204 270 "
        "L 174 328 Q 152 346, 134 326 L 166 244 "
        "C 142 216, 128 184, 126 144 "
        "L 78 106 Q 48 80, 66 44 Q 88 22, 120 34 "
        "L 168 58 C 216 24, 314 34, 352 104 C 368 134, 370 160, 372 184 "
        "L 458 228 C 528 150, 666 122, 766 196 "
        "L 962 84 C 1000 66, 1036 86, 1062 110 L 1084 106 Q 1074 128, 1076 164 "
        "Q 1076 210, 1036 240 L 860 356 "
        "C 850 476, 774 584, 684 606 "
        "L 684 900 L 796 894 Q 824 912, 796 932 L 684 938 "
        "L 684 1206 A 46 46 0 0 1 596 1206 L 596 606 Z"
    )
    s.path(d_bulb, stroke_width=sw)

    # Cathode disk inside bulb A & anode wire B+ (with curved internal wire to lower neck electrode)
    s.line(226.0, 192.0, 260.0, 122.0, stroke_width=9.0)
    s.line(106.0, 416.0, 174.0, 286.0, stroke_width=sw * 0.85)
    s.path("M 174 286 C 196 226, 272 206, 346 250", stroke_width=sw * 0.85)

    # Slit plug in neck between bulb A and main bulb
    s.polygon([(360.0, 204.0), (384.0, 184.0), (452.0, 224.0), (432.0, 246.0)], fill="#ffffff", stroke_width=sw * 0.85)
    s.polygon([(336.0, 262.0), (356.0, 238.0), (424.0, 278.0), (404.0, 302.0)], fill="#ffffff", stroke_width=sw * 0.85)

    # Coaxial Faraday cylinders inside lower neck
    # Outer grounded cylinder (distinct thick black shield with slit at top left)
    s.path(
        "M 600 502 A 70 70 0 0 0 596 618 L 596 1178",
        stroke_width=sw * 2.3,
    )
    s.path(
        "M 620 498 A 70 70 0 0 1 684 618 L 684 1178",
        stroke_width=sw * 2.3,
    )
    # Inner Faraday cylinder + central rod to Electrometer
    s.path(
        "M 616 520 A 48 48 0 1 0 644 520",
        stroke_width=sw * 0.9,
    )
    s.line(634.0, 616.0, 640.0, 1326.0, stroke_width=sw * 0.9)

    # Hatched ebonite insulating plug at bottom of neck
    s.rect(608.0, 1100.0, 64.0, 80.0, fill="#ffffff", stroke_width=sw * 0.85)
    for y in range(1110, 1180, 14):
        s.line(608.0, y, 672.0, y - 10.0, stroke_width=4.0)

    # Earth lead wire
    s.line(684.0, 916.0, 902.0, 910.0, stroke_width=sw * 0.85)

    # Left inset detail C: end-view circle with slit
    s.circle(168.0, 704.0, 40.0, fill="#ffffff", stroke_width=sw * 0.9)
    s.line(134.0, 686.0, 202.0, 718.0, stroke_width=sw * 0.8)
    s.line(128.0, 702.0, 196.0, 734.0, stroke_width=sw * 0.8)

    # Perspective view of coaxial cylinder + ribbon
    s.ellipse(470.0, 882.0, 22.0, 36.0, fill="#ffffff", stroke_width=sw * 0.85, rotate=22.0)
    s.path("M 464 848 L 408 814 C 380 820, 366 854, 376 878 L 448 916", stroke_width=sw * 0.85)
    s.line(384.0, 838.0, 452.0, 876.0, stroke_width=sw * 0.75)
    s.polyline([(392.0, 886.0), (398.0, 996.0), (468.0, 1006.0), (462.0, 914.0)], stroke_width=sw * 0.85)

    # Labels
    lib.label(s, 22.0, 56.0, "A", size=64.0, italic=False, bold=True)
    lib.label(s, 70.0, 422.0, "B", size=64.0, italic=False, bold=True)
    lib.label(s, 134.0, 424.0, "+", size=58.0, italic=False, bold=True)
    lib.label(s, 254.0, 976.0, "C", size=64.0, italic=False, bold=True)
    lib.label(s, 974.0, 916.0, "Earth", size=58.0, italic=True, bold=True)
    lib.label(s, 634.0, 1364.0, "Electrometer", size=58.0, italic=True, bold=True)

    s.save(out_svg)
