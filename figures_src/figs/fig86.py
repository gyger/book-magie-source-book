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

    # Helper for flared conical interior pedestals (M, I, N, J)
    def _pedestal(cx: float, base_y: float, collar_y: float, rx_base: float = 34.0, rx_collar: float = 17.0) -> None:
        # Base disk (bottom thickness + top oval)
        s.ellipse(cx, base_y + 4.0, rx_base, 14.0, fill="#ffffff", stroke_width=sw * 0.85)
        s.ellipse(cx, base_y, rx_base, 13.0, fill="#ffffff", stroke_width=sw * 0.8)
        # Flared conical body rising from base to top collar
        s.path(
            f"M {cx - rx_base + 4} {base_y - 2} "
            f"Q {cx - rx_collar - 4} {(base_y + collar_y) * 0.5 + 4}, {cx - rx_collar + 2} {collar_y} "
            f"L {cx + rx_collar - 2} {collar_y} "
            f"Q {cx + rx_collar + 4} {(base_y + collar_y) * 0.5 + 4}, {cx + rx_base - 4} {base_y - 2} "
            f"A {rx_base - 4} 11 0 0 1 {cx - rx_base + 4} {base_y - 2} Z",
            fill="#ffffff",
            stroke_width=sw * 0.85,
        )
        # Top collar ring
        s.ellipse(cx, collar_y, rx_collar, 7.5, fill="#ffffff", stroke_width=sw * 0.8)

    # === Outer conductor support rods P (left) and Q (right) with pedestals I and J ===
    _pedestal(482.0, 1106.0, 1072.0, rx_base=36.0, rx_collar=17.0)
    _pedestal(1418.0, 1106.0, 1072.0, rx_base=36.0, rx_collar=17.0)
    # Left rod P curving to pivot X
    s.path("M 476 1072 L 476 382 Q 476 350, 514 350 L 620 350", stroke_width=sw * 0.85)
    s.path("M 488 1072 L 488 388 Q 488 362, 518 362 L 620 362", stroke_width=sw * 0.85)
    # Right rod Q curving to pivot Y
    s.path("M 1412 1072 L 1412 388 Q 1412 362, 1380 362 L 1280 362", stroke_width=sw * 0.85)
    s.path("M 1424 1072 L 1424 382 Q 1424 350, 1386 350 L 1280 350", stroke_width=sw * 0.85)

    # Diagonal connecting straps M-I and N-J on interior base
    s.line(446.0, 1140.0, 474.0, 1114.0, stroke_width=sw * 0.9)
    s.line(1380.0, 1140.0, 1408.0, 1114.0, stroke_width=sw * 0.9)

    # Vertical posts A (left) and B (right) with pedestals M and N
    _pedestal(428.0, 1156.0, 1122.0, rx_base=34.0, rx_collar=17.0)
    s.rect(422.0, 960.0, 12.0, 162.0, fill="#ffffff", stroke_width=sw * 0.8)
    _pedestal(1362.0, 1156.0, 1122.0, rx_base=34.0, rx_collar=17.0)
    s.rect(1356.0, 960.0, 12.0, 162.0, fill="#ffffff", stroke_width=sw * 0.8)

    # === Four connecting wires from mercury cups R, S, T, U over/under frame rim to terminals M, I, N, J ===
    wsw = sw * 0.78
    # Wire from cup R (front-left) -> over rim -> to post A / terminal M
    s.path("M 206 1106 L 206 1060 Q 206 1054, 214 1054 L 242 1054 Q 248 1054, 248 1062 L 248 1148", stroke_width=wsw)
    s.line(248.0, 1148.0, 308.0, 1148.0, stroke_width=wsw * 0.9, dash="14,10")
    s.path("M 308 1148 L 308 1062 Q 308 1054, 316 1054 L 340 1054 Q 348 1054, 348 1046 L 422 1046", stroke_width=wsw)

    # Wire from cup S (back-left) -> over rim -> to rod P / terminal I
    s.path("M 272 1040 L 272 1002 Q 272 996, 280 996 L 318 996 Q 324 996, 324 1004 L 324 1084", stroke_width=wsw)
    s.line(324.0, 1084.0, 374.0, 1084.0, stroke_width=wsw * 0.9, dash="14,10")
    s.path("M 374 1084 L 374 998 Q 374 990, 382 990 L 404 990 L 476 990", stroke_width=wsw)

    # Wire from cup T (front-right) -> over rim -> to post B / terminal N
    s.path("M 1578 1102 L 1578 1066 Q 1578 1058, 1570 1058 L 1528 1058 Q 1522 1058, 1522 1066 L 1522 1138", stroke_width=wsw)
    s.line(1522.0, 1138.0, 1474.0, 1138.0, stroke_width=wsw * 0.9, dash="14,10")
    s.path("M 1474 1138 L 1474 1054 Q 1474 1046, 1466 1046 L 1368 1046", stroke_width=wsw)

    # Wire from cup U (back-right) -> over rim -> to rod Q / terminal J
    s.path("M 1648 1040 L 1648 994 Q 1648 986, 1640 986 L 1598 986 Q 1592 986, 1592 994 L 1592 1066", stroke_width=wsw)
    s.line(1592.0, 1066.0, 1538.0, 1066.0, stroke_width=wsw * 0.9, dash="14,10")
    s.path("M 1538 1066 L 1538 992 Q 1538 984, 1530 984 L 1424 984", stroke_width=wsw)

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
    s.line(1734.0, 38.0, 1734.0, 356.0, stroke_width=sw)
    s.rect(1718.0, 198.0, 32.0, 34.0, fill="#ffffff", stroke_width=sw * 0.8)
    s.line(1722.0, 166.0, 1722.0, 260.0, stroke_width=sw * 0.8)
    # Lower detail (compass needle with waisted central sleeve and horizontal pin e-f)
    s.polygon([(1738.0, 488.0), (1760.0, 642.0), (1742.0, 796.0), (1718.0, 642.0)], fill="#ffffff", stroke_width=sw * 0.9)
    # Waisted central sleeve inside the needle
    s.path(
        "M 1728 600 L 1752 600 Q 1746 622, 1752 642 Q 1746 660, 1752 678 "
        "L 1728 678 Q 1734 660, 1728 642 Q 1734 622, 1728 600 Z",
        fill="#ffffff",
        stroke_width=sw * 0.8,
    )
    # Horizontal pin/rod from circle e through the central sleeve to pointed tip near f
    s.line(1702.0, 642.0, 1788.0, 642.0, stroke_width=sw * 0.9)
    s.polygon([(1778.0, 636.0), (1796.0, 642.0), (1778.0, 648.0)], fill="#000000", stroke="none")
    s.circle(1740.0, 642.0, 6.0, fill="#ffffff", stroke_width=sw * 0.7)
    s.circle(1690.0, 642.0, 11.0, fill="#ffffff", stroke_width=sw * 0.85)
    # Small dashed leader line from c to lower sleeve
    s.line(1704.0, 668.0, 1732.0, 665.0, stroke_width=sw * 0.65, dash="8,6")

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
        (1740, 464, "b", True), (1786, 582, "d", True), (1686, 610, "e", True),
        (1694, 694, "c", True), (1814, 642, "f", True), (1748, 822, "a", True),
    ]:
        lib.label(s, float(x), float(y), txt, size=54.0, italic=it, bold=True)

    s.save(out_svg)
