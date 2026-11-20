"""Figure 89: Ohm's torsion balance for measuring thermoelectric current."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.0
    # === Tripod wooden base with 3 leveling screws ===
    d_base = (
        "M 18 1444 C 120 1444, 240 1540, 320 1630 "
        "C 400 1710, 470 1756, 524 1806 "
        "C 580 1834, 650 1824, 710 1796 "
        "L 764 1764 C 810 1788, 880 1786, 940 1754 "
        "L 1064 1676 C 1130 1704, 1240 1686, 1252 1626 "
        "C 1256 1584, 1200 1560, 1130 1574 "
        "C 1000 1554, 860 1510, 720 1466 "
        "C 620 1434, 480 1420, 350 1446 "
        "C 240 1446, 130 1420, 60 1378"
    )
    s.path(d_base, stroke_width=sw)
    # Lower thickness edge of tripod base
    s.path(
        "M 20 1486 C 130 1492, 230 1590, 310 1674 "
        "C 390 1754, 460 1796, 514 1834 "
        "M 640 1834 L 764 1808 C 820 1828, 888 1824, 946 1790 "
        "L 1070 1714 C 1140 1740, 1244 1720, 1252 1662",
        stroke_width=sw * 0.9,
    )
    # 3 leveling thumb-screws (left, bottom-center, right)
    for sx, sy in [(44.0, 1356.0), (582.0, 1732.0), (1196.0, 1546.0)]:
        s.ellipse(sx, sy, 36.0, 18.0, fill="#ffffff", stroke_width=sw * 0.85)
        s.rect(sx - 10.0, sy + 18.0, 20.0, 56.0, fill="#ffffff", stroke_width=sw * 0.8)

    # === Central brass pillar g-h ===
    s.ellipse(518.0, 1632.0, 86.0, 40.0, fill="#ffffff", stroke_width=sw)
    s.ellipse(518.0, 1612.0, 66.0, 28.0, fill="#ffffff", stroke_width=sw * 0.85)
    s.line(468.0, 1166.0, 468.0, 1596.0, stroke_width=sw)
    s.line(566.0, 1166.0, 566.0, 1596.0, stroke_width=sw)
    # Collar clamp + mercury cup bracket m, m'
    s.path(
        "M 468 1344 C 420 1320, 300 1280, 250 1324 "
        "C 218 1354, 260 1408, 344 1408 "
        "C 400 1408, 434 1390, 468 1384",
        fill="#ffffff",
        stroke_width=sw,
    )
    s.ellipse(518.0, 1364.0, 74.0, 34.0, fill="#ffffff", stroke_width=sw)
    # Mercury cups m, m' and vertical leads d, d'
    for mx in (306.0, 362.0):
        s.rect(mx - 8.0, 1086.0, 16.0, 202.0, fill="#ffffff", stroke_width=sw * 0.8)
        s.ellipse(mx, 1296.0, 28.0, 14.0, fill="#ffffff", stroke_width=sw * 0.8)
        s.path(f"M {mx - 26} 1298 Q {mx - 14} 1336, {mx} 1340 Q {mx + 14} 1336, {mx + 26} 1298", fill="#ffffff", stroke_width=sw * 0.8)

    # === Lower brass base cylinder f-f ===
    s.path("M 254 960 L 254 1076 A 256 116 0 0 0 766 1076 L 766 960", fill="#ffffff", stroke_width=sw)
    s.ellipse(510.0, 954.0, 256.0, 118.0, fill="#ffffff", stroke_width=sw)
    s.ellipse(510.0, 954.0, 222.0, 98.0, fill="none", stroke_width=sw * 0.85)

    # Left reading microscope l on bracket k-f
    s.rect(96.0, 960.0, 158.0, 114.0, fill="#ffffff", stroke_width=sw * 0.85)
    s.path("M 106 960 L 160 916 L 172 876", stroke_width=sw * 0.85)
    s.ellipse(158.0, 824.0, 52.0, 28.0, fill="#ffffff", stroke_width=sw, rotate=-48.0)
    s.ellipse(158.0, 824.0, 32.0, 16.0, fill="#ffffff", stroke_width=sw * 0.75, rotate=-48.0)
    s.path("M 190 806 L 244 868 Q 222 908, 184 892 L 154 862", stroke_width=sw * 0.85)

    # === Glass cylinder v-v ===
    s.line(286.0, 318.0, 286.0, 954.0, stroke_width=sw)
    s.line(734.0, 318.0, 734.0, 954.0, stroke_width=sw)
    # Top disk flange
    s.path("M 284 300 L 284 338 A 226 102 0 0 0 736 338 L 736 300", fill="#ffffff", stroke_width=sw)
    s.ellipse(510.0, 300.0, 226.0, 102.0, fill="#ffffff", stroke_width=sw)
    # Inner brass collar p-o
    s.ellipse(510.0, 312.0, 116.0, 52.0, fill="#ffffff", stroke_width=sw * 0.9)
    s.ellipse(510.0, 294.0, 116.0, 52.0, fill="#ffffff", stroke_width=sw * 0.9)
    # Torsion neck s + graduated head n-r + knob q
    s.rect(474.0, 206.0, 74.0, 90.0, fill="#ffffff", stroke_width=sw * 0.9)
    s.ellipse(510.0, 178.0, 96.0, 48.0, fill="#ffffff", stroke_width=sw)
    s.ellipse(510.0, 150.0, 96.0, 48.0, fill="#ffffff", stroke_width=sw)
    s.rect(494.0, 110.0, 34.0, 44.0, fill="#ffffff", stroke_width=sw * 0.85)
    s.ellipse(510.0, 106.0, 38.0, 20.0, fill="#ffffff", stroke_width=sw)

    # Torsion thread & magnetic needle t-t + circular scale arc u-u
    s.line(508.0, 308.0, 508.0, 932.0, stroke_width=sw * 0.8)
    s.line(376.0, 934.0, 694.0, 934.0, stroke_width=sw)
    s.ellipse(416.0, 934.0, 16.0, 24.0, fill="#ffffff", stroke_width=sw * 0.8)
    s.ellipse(618.0, 934.0, 16.0, 24.0, fill="#ffffff", stroke_width=sw * 0.8)
    s.path("M 412 868 C 300 906, 300 996, 412 1034", stroke_width=sw * 0.85)

    # === External copper conductor strips a-b and a'-b' ===
    # Rear arm b -> a
    s.polyline([(740.0, 962.0), (826.0, 962.0), (840.0, 1198.0), (800.0, 1198.0), (796.0, 978.0), (740.0, 978.0)], fill="#ffffff", stroke_width=sw * 0.9)
    # Front arched arm c -> b' -> a'
    s.path("M 316 1044 C 480 1168, 700 1252, 948 1280 L 948 1488 L 976 1492 L 976 1262 L 832 962 L 806 962 L 932 1260 C 696 1236, 480 1152, 338 1044", fill="#ffffff", stroke_width=sw * 0.9)

    # Labels
    for x, y, txt in [
        (512, 38, "q"), (388, 126, "r"), (638, 134, "r"),
        (378, 182, "n"), (640, 190, "n"), (508, 250, "s"),
        (434, 290, "o"), (586, 290, "o"), (358, 314, "p"), (654, 320, "p"),
        (246, 540, "v"), (760, 546, "v"), (126, 766, "l"),
        (56, 996, "k"), (166, 1002, "f"), (710, 1054, "f"),
        (420, 846, "u"), (448, 1024, "u"), (442, 898, "t"), (626, 898, "t"),
        (362, 986, "c"), (306, 1056, "c"), (806, 932, "b"), (832, 1232, "a"),
        (994, 1258, "b′"), (966, 1524, "a′"),
        (264, 1222, "d"), (402, 1222, "d′"), (234, 1296, "m"), (428, 1296, "m′"),
        (524, 1236, "g"), (520, 1542, "h"), (1280, 1656, "i"),
    ]:
        lib.label(s, float(x), float(y), txt, size=62.0, italic=True, bold=True)

    s.save(out_svg)
