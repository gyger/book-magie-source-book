"""Figure 89: Ohm's torsion balance for measuring thermoelectric current."""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image

import draw
import library as lib


def _label_primed(scene: draw.Scene, x: float, y: float, base: str, *, size: float = 62.0) -> None:
    """Render an italic bold letter with a crisp slanted prime mark (avoiding non-italic font fallback on U+2032)."""
    lib.label(scene, x - 6.0, y, base, size=size, italic=True, bold=True)
    # Draw a crisp classical italic prime stroke to the upper right of the letter
    x_off = 0.44 if base == "m" else 0.30
    px = x + size * x_off
    py = y - size * 0.34
    scene.path(
        f"M {px + 5:.1f} {py - 8:.1f} L {px - 3:.1f} {py + 12:.1f}",
        stroke_width=4.6,
        linecap="round",
    )


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.0
    # === Tripod wooden base with 3 leveling screws ===
    # Top surface outline (traced to match original scan scallops & central belly)
    d_base_top = (
        "M 0 1428 C 26 1454, 62 1456, 88 1444 "
        "L 230 1564 C 282 1638, 344 1690, 430 1720 "
        "L 536 1790 C 520 1816, 540 1836, 582 1836 "
        "C 624 1836, 644 1816, 628 1792 "
        "L 764 1738 C 836 1788, 922 1768, 996 1688 "
        "L 1132 1644 C 1178 1678, 1248 1662, 1252 1618 "
        "C 1254 1584, 1200 1566, 1132 1610 "
        "L 858 1574 C 786 1502, 686 1458, 566 1452 "
        "L 466 1452 C 414 1454, 370 1466, 344 1484 "
        "L 106 1438 C 90 1416, 60 1398, 20 1404"
    )
    s.path(d_base_top, stroke_width=sw)
    # Lower thickness edge of tripod base + vertical corner creases
    s.path(
        "M 0 1476 C 28 1500, 62 1502, 88 1492 "
        "L 230 1612 C 282 1684, 344 1736, 430 1766 "
        "L 530 1834 "
        "M 634 1834 L 764 1786 C 836 1834, 922 1814, 996 1736 "
        "L 1132 1692 C 1180 1724, 1250 1708, 1252 1664 L 1252 1618",
        stroke_width=sw * 0.9,
    )
    for vx, vy in [(88.0, 1444.0), (230.0, 1564.0), (430.0, 1720.0), (628.0, 1792.0), (764.0, 1738.0), (996.0, 1688.0), (1132.0, 1644.0)]:
        s.line(vx, vy, vx, vy + 46.0, stroke_width=sw * 0.75)

    # 3 leveling thumb-screws (left, bottom-center, right)
    for sx, sy in [(42.0, 1346.0), (582.0, 1736.0), (1192.0, 1554.0)]:
        s.rect(sx - 10.0, sy + 16.0, 20.0, 56.0, fill="#ffffff", stroke_width=sw * 0.8)
        s.ellipse(sx, sy + 6.0, 34.0, 16.0, fill="#ffffff", stroke_width=sw * 0.85)
        s.ellipse(sx, sy - 4.0, 36.0, 17.0, fill="#ffffff", stroke_width=sw * 0.85)

    # === Central brass pillar g-h ===
    # Flared conical pillar foot at base
    s.ellipse(514.0, 1636.0, 86.0, 38.0, fill="#ffffff", stroke_width=sw)
    s.path(
        "M 442 1628 Q 460 1606, 462 1574 L 566 1574 Q 568 1606, 586 1628 "
        "A 72 28 0 0 1 442 1628 Z",
        fill="#ffffff",
        stroke_width=sw * 0.9,
    )
    s.ellipse(514.0, 1574.0, 56.0, 22.0, fill="#ffffff", stroke_width=sw * 0.85)
    # Main vertical pillar shaft
    s.rect(466.0, 1164.0, 96.0, 412.0, fill="#ffffff", stroke="none")
    s.line(466.0, 1164.0, 466.0, 1574.0, stroke_width=sw)
    s.line(562.0, 1164.0, 562.0, 1574.0, stroke_width=sw)

    # Collar clamp + mercury cup bracket m, m'
    # Bracket plate (lower thickness + top surface)
    s.path(
        "M 450 1378 C 414 1396, 376 1412, 326 1412 "
        "C 254 1412, 232 1374, 240 1344 "
        "L 240 1328 C 244 1362, 266 1396, 326 1396 "
        "C 376 1396, 412 1380, 444 1356 Z",
        fill="#ffffff",
        stroke_width=sw * 0.85,
    )
    s.path(
        "M 464 1330 C 424 1308, 300 1280, 250 1316 "
        "C 226 1340, 254 1396, 326 1396 "
        "C 380 1396, 416 1378, 446 1358",
        fill="#ffffff",
        stroke_width=sw,
    )
    # Cylindrical brass clamp sleeve wrapping pillar between g and h
    s.path(
        "M 442 1348 L 442 1408 A 70 24 0 0 0 582 1408 L 582 1348 Z",
        fill="#ffffff",
        stroke_width=sw,
    )
    s.ellipse(512.0, 1348.0, 70.0, 24.0, fill="#ffffff", stroke_width=sw)
    s.ellipse(512.0, 1344.0, 50.0, 16.0, fill="#ffffff", stroke_width=sw * 0.8)
    # Re-draw upper pillar walls cleanly entering the clamp sleeve
    s.rect(468.0, 1164.0, 92.0, 180.0, fill="#ffffff", stroke="none")
    s.line(466.0, 1164.0, 466.0, 1344.0, stroke_width=sw)
    s.line(562.0, 1164.0, 562.0, 1344.0, stroke_width=sw)

    # Wing-nut / thumbscrew on right side of clamp sleeve (between g and h)
    s.rect(580.0, 1372.0, 18.0, 14.0, fill="#ffffff", stroke_width=sw * 0.8)
    s.path(
        "M 598 1374 C 598 1354, 608 1340, 620 1344 "
        "C 628 1348, 626 1368, 616 1378 "
        "C 624 1388, 624 1408, 614 1412 "
        "C 602 1416, 596 1400, 598 1384 Z",
        fill="#ffffff",
        stroke_width=sw * 0.85,
    )
    s.circle(598.0, 1379.0, 5.0, fill="#ffffff", stroke_width=sw * 0.7)
    s.line(610.0, 1354.0, 614.0, 1368.0, stroke_width=sw * 0.6)
    s.line(608.0, 1392.0, 612.0, 1404.0, stroke_width=sw * 0.6)

    # Mercury cups m, m' (stemmed goblets with circular bases) and vertical leads d, d'
    for mx, my_rim, lead_top in [(302.0, 1274.0, 1086.0), (358.0, 1288.0, 1072.0)]:
        # Circular foot + flared stem
        s.ellipse(mx, my_rim + 50.0, 28.0, 10.0, fill="#ffffff", stroke_width=sw * 0.8)
        s.path(
            f"M {mx - 20} {my_rim + 48} Q {mx - 10} {my_rim + 40}, {mx - 10} {my_rim + 30} "
            f"L {mx + 10} {my_rim + 30} Q {mx + 10} {my_rim + 40}, {mx + 20} {my_rim + 48}",
            fill="#ffffff",
            stroke_width=sw * 0.8,
        )
        # Cup bowl
        s.path(
            f"M {mx - 30} {my_rim + 2} Q {mx - 24} {my_rim + 28}, {mx - 10} {my_rim + 32} "
            f"L {mx + 10} {my_rim + 32} Q {mx + 24} {my_rim + 28}, {mx + 30} {my_rim + 2} Z",
            fill="#ffffff",
            stroke_width=sw * 0.85,
        )
        # Rim ellipse
        s.ellipse(mx, my_rim, 30.0, 11.0, fill="#ffffff", stroke_width=sw * 0.8)
        # Vertical lead descending into cup center
        s.rect(mx - 8.0, lead_top, 16.0, my_rim - lead_top + 2.0, fill="#ffffff", stroke_width=sw * 0.8)

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

    # === Circular graduated scale arc u-c-u inside the dish ===
    scx, scy = 506.0, 946.0
    rx_out, ry_out = 196.0, 91.0
    rx_in, ry_in = 166.0, 76.0
    a_start, a_end = 122.0, 238.0
    n_seg = 24
    pts_out = [
        (scx + rx_out * math.cos(math.radians(a_start + (a_end - a_start) * i / n_seg)),
         scy + ry_out * math.sin(math.radians(a_start + (a_end - a_start) * i / n_seg)))
        for i in range(n_seg + 1)
    ]
    pts_in = [
        (scx + rx_in * math.cos(math.radians(a_start + (a_end - a_start) * i / n_seg)),
         scy + ry_in * math.sin(math.radians(a_start + (a_end - a_start) * i / n_seg)))
        for i in range(n_seg + 1)
    ]
    # Scale band polygon (white fill with crisp border)
    s.polygon(pts_out + list(reversed(pts_in)), fill="#ffffff", stroke_width=sw * 0.78)
    # Graduation tick marks along the circular scale arc u-c-u
    n_ticks = 20
    for i in range(1, n_ticks):
        ang = math.radians(a_start + (a_end - a_start) * i / n_ticks)
        ca, sa = math.cos(ang), math.sin(ang)
        major = (i % 5 == 0)
        frac = 0.62 if major else 0.40
        x1 = scx + rx_in * ca
        y1 = scy + ry_in * sa
        x2 = scx + (rx_in + (rx_out - rx_in) * frac) * ca
        y2 = scy + (ry_in + (ry_out - ry_in) * frac) * sa
        s.line(x1, y1, x2, y2, stroke_width=sw * (0.55 if major else 0.42))

    # Horizontal conductor wire crossing inside the dish underneath needle t-t
    s.line(302.0, 954.0, 728.0, 962.0, stroke_width=sw * 0.75)

    # Torsion thread & detailed magnetic needle assembly t-t
    s.line(508.0, 308.0, 508.0, 922.0, stroke_width=sw * 0.8)
    # Central needle shaft (double-line bar)
    s.rect(424.0, 922.0, 174.0, 10.0, fill="#ffffff", stroke_width=sw * 0.75)
    # Left flanged sleeve (left t) + curved reading pointer over scale u-c-u
    s.path(
        "M 374 920 C 344 914, 322 926, 314 946 L 324 948 C 330 934, 348 926, 374 932 Z",
        fill="#ffffff",
        stroke_width=sw * 0.75,
    )
    s.ellipse(424.0, 927.0, 9.0, 16.0, fill="#ffffff", stroke_width=sw * 0.75)
    s.rect(378.0, 916.0, 46.0, 22.0, fill="#ffffff", stroke_width=sw * 0.75)
    s.ellipse(378.0, 927.0, 10.0, 19.0, fill="#ffffff", stroke_width=sw * 0.8)
    # Right flanged sleeve (right t) + end finial knob
    s.ellipse(674.0, 927.0, 13.0, 10.0, fill="#ffffff", stroke_width=sw * 0.8)
    s.ellipse(652.0, 927.0, 10.0, 19.0, fill="#ffffff", stroke_width=sw * 0.8)
    s.rect(598.0, 916.0, 54.0, 22.0, fill="#ffffff", stroke_width=sw * 0.75)
    s.ellipse(598.0, 927.0, 10.0, 19.0, fill="#ffffff", stroke_width=sw * 0.8)

    # === External copper conductor strips a-b and a'-b' ===
    # Rear vertical leg b -> a (with 3D edge)
    s.polygon(
        [(726.0, 956.0), (824.0, 956.0), (824.0, 1196.0), (796.0, 1196.0), (786.0, 1190.0), (786.0, 974.0), (726.0, 974.0)],
        fill="#ffffff",
        stroke_width=sw * 0.85,
    )
    s.line(796.0, 974.0, 796.0, 1196.0, stroke_width=sw * 0.75)

    # Diagonal strut b -> b' and front vertical leg b' -> a'
    s.polygon(
        [
            (806.0, 956.0), (836.0, 956.0),
            (950.0, 1276.0), (946.0, 1492.0), (920.0, 1492.0), (904.0, 1484.0),
            (906.0, 1282.0), (906.0, 1258.0),
        ],
        fill="#ffffff",
        stroke_width=sw * 0.85,
    )
    # Inner 3D ridge along diagonal strut and front vertical leg
    s.polyline([(816.0, 956.0), (926.0, 1276.0), (922.0, 1492.0)], stroke_width=sw * 0.75)

    # Front arched conductor strip c -> b' (with 3D thickness edge)
    s.path(
        "M 310 1038 C 468 1152, 684 1236, 914 1260 "
        "L 914 1284 C 680 1262, 462 1174, 304 1054 Z",
        fill="#ffffff",
        stroke_width=sw * 0.85,
    )
    s.path(
        "M 308 1046 C 466 1162, 682 1248, 914 1272",
        stroke_width=sw * 0.65,
    )

    # Labels (unprimed)
    for x, y, txt in [
        (512, 38, "q"), (388, 126, "r"), (638, 134, "r"),
        (378, 182, "n"), (640, 190, "n"), (508, 250, "s"),
        (434, 290, "o"), (586, 290, "o"), (358, 314, "p"), (654, 320, "p"),
        (246, 540, "v"), (760, 546, "v"), (126, 766, "l"),
        (56, 996, "k"), (166, 1002, "f"), (708, 1056, "f"),
        (414, 846, "u"), (448, 1024, "u"), (442, 892, "t"), (626, 892, "t"),
        (352, 976, "c"), (292, 1066, "c"), (804, 926, "b"), (812, 1218, "a"),
        (264, 1222, "d"), (232, 1288, "m"),
        (524, 1228, "g"), (520, 1542, "h"), (1280, 1656, "i"),
    ]:
        lib.label(s, float(x), float(y), txt, size=62.0, italic=True, bold=True)

    # Primed labels (rendered with italic bold letter + crisp slanted prime)
    for x, y, base in [
        (980, 1266, "b"),
        (942, 1524, "a"),
        (400, 1222, "d"),
        (426, 1286, "m"),
    ]:
        _label_primed(s, float(x), float(y), base, size=62.0)

    s.save(out_svg)
