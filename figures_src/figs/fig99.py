"""Figure 99: Crookes magnetic deflection tube (Elevation) with electromagnet S."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.5
    # Vertical glass neck + left side exhaust arm
    s.path("M 1408 0 L 1408 214 L 1236 214 Q 1208 232, 1236 250 L 1408 250 L 1408 820", stroke_width=sw)
    s.line(1522.0, 0.0, 1522.0, 820.0, stroke_width=sw)
    s.path("M 1414 140 Q 1465 156, 1516 140", stroke_width=sw * 0.8)

    # Main horizontal lens-shaped glass bulb
    d_bulb = (
        "M 1408 820 C 1180 848, 980 960, 860 1054 "
        "L 776 1064 C 724 1070, 724 1158, 776 1164 "
        "L 860 1172 C 990 1280, 1210 1414, 1480 1414 "
        "C 1740 1414, 1940 1280, 2060 1172 "
        "L 2140 1166 C 2194 1160, 2194 1068, 2140 1062 "
        "L 2060 1054 C 1930 950, 1740 842, 1522 820"
    )
    s.path(d_bulb, stroke_width=sw)

    # Suspension wire from top stem down to tiny wheel/vane d
    s.line(1465.0, 146.0, 1465.0, 1140.0, stroke_width=sw * 0.75)
    for by in (198.0, 380.0, 600.0, 808.0):
        s.circle(1465.0, by, 7.0, fill="#ffffff", stroke_width=4.0)
    # Suspended wheel/screen d
    s.path("M 1465 1138 Q 1428 1152, 1424 1214 L 1465 1214", stroke_width=sw * 0.8)
    s.circle(1462.0, 1192.0, 18.0, fill="none", stroke_width=5.0)
    s.line(1442.0, 1174.0, 1482.0, 1210.0, stroke_width=5.0)
    s.line(1482.0, 1174.0, 1442.0, 1210.0, stroke_width=5.0)

    # Vertical mica screen e mounted on bottom stem
    s.path(
        "M 1522 1316 L 1526 998 Q 1542 970, 1558 998 L 1556 1304 L 1522 1316 Z",
        fill="#ffffff",
        stroke_width=sw * 0.9,
    )
    s.line(1542.0, 1310.0, 1552.0, 1430.0, stroke_width=sw * 0.85)
    s.polygon([(1534.0, 1344.0), (1556.0, 1344.0), (1566.0, 1416.0), (1536.0, 1416.0)], fill="#ffffff", stroke_width=5.0)

    # Left electrode a (+)
    s.ellipse(878.0, 1114.0, 13.0, 34.0, fill="#ffffff", stroke_width=sw)
    s.line(744.0, 1114.0, 865.0, 1114.0, stroke_width=sw * 0.8)
    s.rect(746.0, 1098.0, 96.0, 32.0, fill="#ffffff", stroke_width=5.0, rx=10.0)

    # Right electrode b (-)
    s.ellipse(2044.0, 1114.0, 13.0, 34.0, fill="#ffffff", stroke_width=sw)
    s.line(2057.0, 1114.0, 2180.0, 1114.0, stroke_width=sw * 0.8)
    s.rect(2082.0, 1098.0, 96.0, 32.0, fill="#ffffff", stroke_width=5.0, rx=10.0)

    # Auxiliary electrode c on upper right wall
    s.line(1896.0, 1020.0, 1954.0, 960.0, stroke_width=sw)
    s.polygon([(1912.0, 996.0), (1944.0, 964.0), (1956.0, 976.0), (1924.0, 1008.0)], fill="#ffffff", stroke_width=4.5)

    # Electromagnet coil S at bottom-left
    # Outer wound solenoid cylinder
    s.rect(236.0, 1304.0, 716.0, 156.0, fill="#ffffff", stroke_width=sw, rx=16.0)
    # Iron core protruding on right
    s.path("M 920 1318 L 964 1318 A 18 64 0 0 1 964 1446 L 920 1446", fill="#ffffff", stroke_width=sw)
    # Winding lines across solenoid
    for x in range(254, 916, 16):
        s.line(x, 1308.0, x - 6.0, 1456.0, stroke_width=3.5, dash="18,12")
    # Two binding posts on far left
    s.rect(100.0, 1368.0, 86.0, 34.0, fill="#ffffff", stroke_width=5.5, rx=6.0)
    s.rect(108.0, 1494.0, 92.0, 34.0, fill="#ffffff", stroke_width=5.5, rx=6.0)
    s.path("M 186 1384 Q 214 1384, 224 1326 Q 232 1300, 250 1304", stroke_width=sw * 0.85)
    s.path("M 200 1510 Q 230 1510, 238 1456", stroke_width=sw * 0.85)
    # Curved arrow near S
    s.path("M 992 1350 Q 1002 1382, 990 1414", stroke_width=5.5)

    # Labels
    lib.label(s, 704.0, 1114.0, "+", size=64.0, italic=False, bold=True)
    lib.label(s, 922.0, 1114.0, "a", size=62.0, italic=True, bold=True)
    lib.label(s, 1396.0, 1192.0, "d", size=62.0, italic=True, bold=True)
    lib.label(s, 1586.0, 1196.0, "e", size=62.0, italic=True, bold=True)
    lib.label(s, 1940.0, 932.0, "c", size=62.0, italic=True, bold=True)
    lib.label(s, 2002.0, 1114.0, "b", size=62.0, italic=True, bold=True)
    lib.label(s, 2224.0, 1114.0, "−", size=64.0, italic=False, bold=True)
    lib.label(s, 1030.0, 1388.0, "S", size=64.0, italic=True, bold=True)
    lib.label(s, 1548.0, 1474.0, "Elevation", size=62.0, italic=True, bold=True)

    s.save(out_svg)
