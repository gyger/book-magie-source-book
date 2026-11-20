"""Figure 86: Ampère's electrodynamic apparatus for mutual action of parallel currents."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 5.5
    # === Wooden base plinth and feet ===
    # Top perspective surface of wooden base
    s.polyline([(44.0, 1272.0), (382.0, 1020.0), (1798.0, 1020.0), (1528.0, 1272.0), (44.0, 1272.0)], stroke_width=sw)
    # Front face of base plinth
    s.polyline([
        (44.0, 1272.0), (44.0, 1364.0), (118.0, 1364.0),
        (148.0, 1332.0), (192.0, 1318.0), (1388.0, 1318.0),
        (1430.0, 1332.0), (1454.0, 1366.0), (1530.0, 1366.0), (1530.0, 1272.0),
    ], stroke_width=sw)
    s.line(44.0, 1318.0, 1530.0, 1318.0, stroke_width=sw * 0.85)
    # Right side face of base plinth
    s.polyline([
        (1530.0, 1366.0), (1570.0, 1330.0), (1570.0, 1286.0),
        (1736.0, 1142.0), (1776.0, 1142.0), (1804.0, 1114.0),
        (1804.0, 1020.0),
    ], stroke_width=sw)

    # Inner recessed frame / tray
    s.polyline([(172.0, 1200.0), (390.0, 1006.0), (1648.0, 1006.0), (1446.0, 1200.0), (172.0, 1200.0)], stroke_width=sw)
    s.polyline([(172.0, 1200.0), (172.0, 1244.0), (1446.0, 1244.0), (1446.0, 1200.0)], stroke_width=sw)
    s.polyline([(206.0, 1184.0), (400.0, 1020.0), (1614.0, 1020.0), (1430.0, 1184.0), (206.0, 1184.0)], stroke_width=sw * 0.85)
    s.line(316.0, 1072.0, 1554.0, 1072.0, stroke_width=sw * 0.7)

    # === Glass enclosure frame ===
    # Front glass rectangle
    s.rect(196.0, 96.0, 1248.0, 1086.0, fill="none", stroke_width=sw)
    # Back glass edges and top perspective connectors
    s.line(392.0, 0.0, 392.0, 1006.0, stroke_width=sw * 0.85)
    s.line(1634.0, 0.0, 1634.0, 1006.0, stroke_width=sw * 0.85)
    s.line(196.0, 96.0, 304.0, 0.0, stroke_width=sw)
    s.line(1444.0, 96.0, 1552.0, 0.0, stroke_width=sw)

    # === Fixed horizontal conductor A-B and base connecting bar K-L ===
    s.rect(406.0, 976.0, 980.0, 10.0, fill="#ffffff", stroke_width=sw * 0.75)
    s.rect(438.0, 1106.0, 926.0, 12.0, fill="#ffffff", stroke_width=sw * 0.75)

    # Vertical posts A (left) and B (right)
    s.rect(422.0, 960.0, 12.0, 174.0, fill="#ffffff", stroke_width=sw * 0.8)
    s.ellipse(428.0, 1152.0, 32.0, 16.0, fill="#ffffff", stroke_width=sw * 0.85)
    s.rect(1356.0, 960.0, 12.0, 174.0, fill="#ffffff", stroke_width=sw * 0.8)
    s.ellipse(1362.0, 1152.0, 32.0, 16.0, fill="#ffffff", stroke_width=sw * 0.85)

    # === Outer conductor support rods P (left) and Q (right) ===
    # Left rod P curving to pivot X
    s.path("M 476 1080 L 476 382 Q 476 350, 514 350 L 620 350", stroke_width=sw * 0.85)
    s.path("M 488 1080 L 488 388 Q 488 362, 518 362 L 620 362", stroke_width=sw * 0.85)
    s.ellipse(482.0, 1104.0, 28.0, 14.0, fill="#ffffff", stroke_width=sw * 0.85)
    # Right rod Q curving to pivot Y
    s.path("M 1412 1080 L 1412 388 Q 1412 362, 1380 362 L 1280 362", stroke_width=sw * 0.85)
    s.path("M 1424 1080 L 1424 382 Q 1424 350, 1386 350 L 1280 350", stroke_width=sw * 0.85)
    s.ellipse(1418.0, 1104.0, 28.0, 14.0, fill="#ffffff", stroke_width=sw * 0.85)

    # === Movable rectangular conductor C-D suspended from axle E-O-G-Z-F ===
    # Horizontal axle bar E-F
    s.rect(612.0, 322.0, 684.0, 10.0, fill="#ffffff", stroke_width=sw * 0.8)
    # Pivot sleeves E, F and counterweight hooks X, Y
    s.rect(628.0, 314.0, 42.0, 26.0, fill="#ffffff", stroke_width=sw * 0.8)
    s.rect(1234.0, 314.0, 42.0, 26.0, fill="#ffffff", stroke_width=sw * 0.8)
    s.circle(620.0, 356.0, 12.0, fill="#ffffff", stroke_width=sw * 0.8)
    s.circle(1284.0, 356.0, 12.0, fill="#ffffff", stroke_width=sw * 0.8)

    # Central suspension stirrup G-V-H
    s.rect(932.0, 316.0, 48.0, 36.0, fill="#ffffff", stroke_width=sw * 0.85)
    s.rect(948.0, 232.0, 14.0, 84.0, fill="#ffffff", stroke_width=sw * 0.8)
    s.path("M 954 232 Q 950 186, 944 152", stroke_width=sw)
    s.circle(944.0, 144.0, 9.0, fill="#ffffff", stroke_width=sw * 0.85)

    # Hanging rectangular conductor loop C-D
    s.path(
        "M 638 340 L 638 912 Q 638 926, 654 926 L 1246 926 Q 1262 926, 1262 912 L 1262 340",
        stroke_width=sw * 0.9,
    )
    s.path(
        "M 648 340 L 648 906 Q 648 916, 658 916 L 1242 916 Q 1252 916, 1252 906 L 1252 340",
        stroke_width=sw * 0.75,
    )

    # === Four mercury cups R, S (left) and T, U (right) ===
    for cx, cy in [(194.0, 1110.0), (272.0, 1044.0), (1598.0, 1110.0), (1666.0, 1044.0)]:
        s.ellipse(cx, cy, 32.0, 12.0, fill="#ffffff", stroke_width=sw * 0.8)
        s.path(f"M {cx - 32} {cy} Q {cx - 24} {cy + 40}, {cx} {cy + 46} Q {cx + 24} {cy + 40}, {cx + 32} {cy}", fill="#ffffff", stroke_width=sw * 0.8)
        s.ellipse(cx, cy + 56.0, 24.0, 10.0, fill="#ffffff", stroke_width=sw * 0.8)

    # === Right-margin detail drawings (suspension & needle a-b-c-d-e-f) ===
    # Upper detail
    s.line(1736.0, 38.0, 1736.0, 356.0, stroke_width=sw)
    s.rect(1720.0, 198.0, 32.0, 34.0, fill="#ffffff", stroke_width=sw * 0.8)
    s.line(1724.0, 166.0, 1724.0, 260.0, stroke_width=sw * 0.8)
    # Lower detail (compass needle)
    s.polygon([(1740.0, 496.0), (1764.0, 646.0), (1740.0, 804.0), (1716.0, 646.0)], fill="#ffffff", stroke_width=sw * 0.9)
    s.rect(1728.0, 610.0, 24.0, 72.0, fill="#ffffff", stroke_width=sw * 0.8)
    s.circle(1692.0, 648.0, 9.0, fill="#ffffff", stroke_width=sw * 0.8)

    # Labels
    for x, y, txt, it in [
        (904, 134, "H", False), (990, 264, "V", False), (956, 386, "G", False),
        (672, 286, "E", False), (1222, 286, "F", False),
        (772, 366, "O", False), (1116, 366, "Z", False),
        (606, 396, "X", False), (1296, 396, "Y", False),
        (518, 618, "P", False), (1374, 618, "Q", False),
        (680, 888, "C", False), (1216, 888, "D", False),
        (430, 932, "A", False), (1358, 932, "B", False),
        (134, 1132, "R", False), (222, 1004, "S", False),
        (1544, 1196, "T", False), (1724, 1044, "U", False),
        (366, 1148, "M", False), (506, 1148, "I", False),
        (652, 1148, "K", False), (1220, 1148, "L", False),
        (1312, 1148, "N", False), (1428, 1148, "J", False),
        (42, 1212, "m", True), (1682, 1200, "n", True),
        (1736, 18, "b", True), (1696, 152, "d", True), (1768, 178, "e", True),
        (1706, 262, "c", True), (1772, 240, "f", True), (1742, 382, "a", True),
        (1740, 464, "b", True), (1788, 588, "d", True), (1692, 618, "e", True),
        (1696, 698, "c", True), (1812, 646, "f", True), (1748, 826, "a", True),
    ]:
        lib.label(s, float(x), float(y), txt, size=54.0, italic=it, bold=True)

    s.save(out_svg)
