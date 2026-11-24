"""Figure 97: Hertz's primary oscillator (a) and secondary spark-gap receiver (b) with 40 cm scale."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.5
    # === Left (a): Primary oscillator ===
    # Left and right vertical frame bars
    s.rect(94.0, 86.0, 16.0, h - 88.0, fill="#ffffff", stroke_width=sw * 0.9)
    s.rect(496.0, 58.0, 26.0, h - 60.0, fill="#ffffff", stroke_width=sw * 0.9)

    # Horizontal T-support S on left frame
    s.rect(110.0, 576.0, 14.0, 130.0, fill="#ffffff", stroke_width=sw * 0.85)
    s.rect(124.0, 628.0, 146.0, 22.0, fill="#ffffff", stroke_width=sw * 0.85)
    s.rect(270.0, 576.0, 16.0, 136.0, fill="#ffffff", stroke_width=sw * 0.85)

    # Upper & lower brass cylindrical oscillator arms + spark-gap spheres
    # Mounting bar along right post
    s.rect(476.0, 338.0, 20.0, 608.0, fill="#ffffff", stroke_width=sw * 0.85)
    for by in (396.0, 496.0, 766.0, 872.0):
        s.rect(418.0, by, 58.0, 26.0, fill="#ffffff", stroke_width=sw * 0.85)

    # Upper brass cylinder & sleeve
    s.rect(348.0, 344.0, 70.0, 198.0, fill="#ffffff", stroke_width=sw)
    s.rect(338.0, 448.0, 90.0, 24.0, fill="#ffffff", stroke_width=sw * 0.85)
    # Lower brass cylinder & sleeve
    s.rect(348.0, 734.0, 70.0, 198.0, fill="#ffffff", stroke_width=sw)
    s.rect(338.0, 814.0, 90.0, 24.0, fill="#ffffff", stroke_width=sw * 0.85)

    # Two spark-gap spheres meeting at (378, 638)
    s.circle(378.0, 586.0, 52.0, fill="#ffffff", stroke_width=sw)
    s.circle(378.0, 690.0, 52.0, fill="#ffffff", stroke_width=sw)

    # Curved gutta-percha lead wires emerging left from spheres
    s.path("M 342 554 Q 202 452, 18 454", stroke_width=sw)
    s.path("M 334 566 Q 196 468, 18 468", stroke_width=sw)
    s.path("M 346 724 Q 204 824, 18 824", stroke_width=sw)
    s.path("M 338 712 Q 198 810, 18 810", stroke_width=sw)

    # === Center: 40 cm vertical scale ===
    s.line(708.0, 192.0, 708.0, 1126.0, stroke_width=sw)
    for y in (192.0, 414.0, 646.0, 882.0, 1126.0):
        s.line(708.0, y, 744.0, y, stroke_width=sw)

    # === Right (b): Secondary spark-gap receiver ===
    # Two parallel vertical support rods on left
    s.rect(924.0, 146.0, 20.0, 996.0, fill="#ffffff", stroke_width=sw * 0.9)
    s.rect(978.0, 146.0, 16.0, 456.0, fill="#ffffff", stroke_width=sw * 0.9)
    s.rect(978.0, 710.0, 16.0, 432.0, fill="#ffffff", stroke_width=sw * 0.9)
    # Cross clamps
    s.rect(916.0, 458.0, 86.0, 16.0, fill="#ffffff", stroke_width=sw * 0.8)
    s.rect(916.0, 854.0, 86.0, 16.0, fill="#ffffff", stroke_width=sw * 0.8)
    # Two small horizontal connecting bridges between the left vertical resonator tubes
    s.rect(944.0, 504.0, 34.0, 20.0, fill="#ffffff", stroke_width=sw * 0.8)
    s.rect(944.0, 792.0, 34.0, 20.0, fill="#ffffff", stroke_width=sw * 0.8)

    # Right vertical frame bar
    s.rect(1248.0, 154.0, 14.0, 974.0, fill="#ffffff", stroke_width=sw * 0.9)

    # Micrometer spark-gap housing on far right
    s.path("M 1276 556 L 1420 556 Q 1436 556, 1436 576 L 1436 756 Q 1436 774, 1418 774 L 1276 774", stroke_width=sw * 0.85)

    # Two horizontal secondary lead wires passing through insulating sleeves into micrometer
    s.path("M 994 588 L 1344 588 Q 1354 588, 1354 598 L 1354 646", stroke_width=sw * 0.85)
    s.path("M 994 726 L 1284 726 Q 1296 726, 1300 712 L 1306 704", stroke_width=sw * 0.85)
    s.rect(1168.0, 574.0, 108.0, 26.0, fill="#ffffff", stroke_width=sw * 0.85)
    s.rect(1168.0, 712.0, 108.0, 26.0, fill="#ffffff", stroke_width=sw * 0.85)

    # Binding collars, upper spark ball, lower spark tip, and micrometer screw
    s.rect(1306.0, 576.0, 18.0, 24.0, fill="#ffffff", stroke_width=4.5, rx=3.0)
    s.rect(1342.0, 616.0, 24.0, 18.0, fill="#ffffff", stroke_width=4.5, rx=3.0)
    s.circle(1354.0, 656.0, 10.0, fill="#ffffff", stroke_width=4.5)
    s.polygon([(1348.0, 688.0), (1354.0, 670.0), (1360.0, 688.0)], fill="#ffffff", stroke_width=4.0)
    s.circle(1300.0, 704.0, 7.0, fill="#ffffff", stroke_width=4.0)
    s.rect(1306.0, 688.0, 96.0, 24.0, fill="#ffffff", stroke_width=sw * 0.85, rx=10.0)
    s.rect(1344.0, 712.0, 20.0, 68.0, fill="#ffffff", stroke_width=sw * 0.8)
    s.rect(1308.0, 780.0, 92.0, 26.0, fill="#ffffff", stroke_width=sw * 0.85, rx=8.0)

    # Labels
    lib.label(s, 290.0, 140.0, "a", size=68.0, italic=False, bold=True)
    lib.label(s, 1118.0, 134.0, "b", size=68.0, italic=False, bold=True)
    lib.label(s, 190.0, 598.0, "S", size=60.0, italic=True, bold=True)
    lib.label(s, 750.0, 192.0, "40cm.", size=54.0, italic=True, bold=True, anchor="start")
    lib.label(s, 786.0, 414.0, "30", size=58.0, italic=True, bold=True)
    lib.label(s, 786.0, 646.0, "20", size=58.0, italic=True, bold=True)
    lib.label(s, 780.0, 882.0, "10", size=58.0, italic=True, bold=True)
    lib.label(s, 770.0, 1126.0, "0", size=58.0, italic=True, bold=True)

    s.save(out_svg)
