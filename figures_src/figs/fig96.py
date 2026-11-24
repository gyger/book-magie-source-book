"""Figure 96: Hertz's parabolic mirror for electric waves (elevation and plan, 100 cm scale)."""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image

import draw
import library as lib


def _helix(s: draw.Scene, x1: float, y1: float, x2: float, y2: float, turns: int, amp: float, sw: float) -> None:
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    if L < 1e-6:
        return
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    pts = []
    steps = turns * 14
    for i in range(steps + 1):
        t = i / steps
        ang = t * turns * 2.0 * math.pi
        px = x1 + dx * t + ux * (amp * 0.4 * math.sin(ang)) + nx * (amp * math.cos(ang))
        py = y1 + dy * t + uy * (amp * 0.4 * math.sin(ang)) + ny * (amp * math.cos(ang))
        pts.append((px, py))
    s.polyline(pts, stroke_width=sw)


def _curved_helix(
    s: draw.Scene,
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    turns: int,
    amp: float,
    sw: float,
) -> None:
    pts = []
    steps = turns * 14
    for i in range(steps + 1):
        t = i / steps
        mt = 1.0 - t
        bx = mt * mt * p0[0] + 2.0 * mt * t * p1[0] + t * t * p2[0]
        by = mt * mt * p0[1] + 2.0 * mt * t * p1[1] + t * t * p2[1]
        dx = 2.0 * mt * (p1[0] - p0[0]) + 2.0 * t * (p2[0] - p1[0])
        dy = 2.0 * mt * (p1[1] - p0[1]) + 2.0 * t * (p2[1] - p1[1])
        L = math.hypot(dx, dy)
        if L < 1e-6:
            continue
        ux, uy = dx / L, dy / L
        nx, ny = -uy, ux
        ang = t * turns * 2.0 * math.pi
        px = bx + ux * (amp * 0.35 * math.sin(ang)) + nx * (amp * math.cos(ang))
        py = by + uy * (amp * 0.35 * math.sin(ang)) + ny * (amp * math.cos(ang))
        pts.append((px, py))
    s.polyline(pts, stroke_width=sw)


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 5.5
    # === TOP: ELEVATION ===
    # Floor line
    s.line(0.0, 1254.0, 892.0, 1254.0, stroke_width=sw * 1.3)

    # Wooden table on left
    s.rect(8.0, 794.0, 390.0, 20.0, fill="#ffffff", stroke_width=sw)
    s.rect(34.0, 814.0, 336.0, 92.0, fill="#ffffff", stroke_width=sw)
    s.rect(62.0, 824.0, 268.0, 68.0, fill="#ffffff", stroke_width=sw * 0.85)
    s.circle(198.0, 856.0, 9.0, fill="#ffffff", stroke_width=4.0)
    # Table legs
    s.polygon([(36.0, 906.0), (62.0, 906.0), (54.0, 1254.0), (32.0, 1254.0)], fill="#ffffff", stroke_width=sw)
    s.polygon([(336.0, 906.0), (362.0, 906.0), (370.0, 1254.0), (346.0, 1254.0)], fill="#ffffff", stroke_width=sw)

    # Induction coil on table
    s.path("M 144 720 C 86 720, 86 764, 144 764", stroke_width=4.0)
    s.rect(108.0, 774.0, 232.0, 20.0, fill="#ffffff", stroke_width=sw * 0.85)
    s.rect(144.0, 704.0, 158.0, 70.0, fill="#ffffff", stroke_width=sw * 0.9)
    s.rect(160.0, 718.0, 126.0, 42.0, fill="#ffffff", stroke_width=sw * 0.8)
    # Binding posts on top of induction coil
    s.rect(168.0, 692.0, 12.0, 12.0, fill="#ffffff", stroke_width=3.8)
    s.rect(280.0, 692.0, 12.0, 12.0, fill="#ffffff", stroke_width=3.8)

    # Tall parabolic mirror housing (elevation)
    s.rect(456.0, 48.0, 408.0, 1142.0, fill="#ffffff", stroke_width=sw)
    # Top and bottom protruding wooden frame posts
    s.rect(474.0, 0.0, 38.0, 48.0, fill="#ffffff", stroke_width=sw * 0.85)
    s.rect(752.0, 0.0, 44.0, 48.0, fill="#ffffff", stroke_width=sw * 0.85)
    s.rect(474.0, 1190.0, 38.0, 64.0, fill="#ffffff", stroke_width=sw * 0.85)
    s.rect(752.0, 1190.0, 44.0, 64.0, fill="#ffffff", stroke_width=sw * 0.85)
    # Vertical sheet-metal shading lines (drawn beneath clamping frames)
    for x in (474, 496, 534, 574, 636, 686, 744):
        s.line(float(x), 54.0, float(x), 1184.0, stroke_width=3.5)
    # Horizontal clamping frames a, a
    s.rect(456.0, 314.0, 408.0, 22.0, fill="#ffffff", stroke_width=sw * 0.9)
    s.rect(456.0, 886.0, 408.0, 22.0, fill="#ffffff", stroke_width=sw * 0.9)

    # Primary oscillator vertical mounting bar, dipole rods, and horizontal T-bracket
    s.rect(554.0, 336.0, 12.0, 550.0, fill="#ffffff", stroke_width=4.0)
    # Horizontal T-support bracket between back edge of mirror and spark gap
    s.rect(460.0, 594.0, 10.0, 38.0, fill="#ffffff", stroke_width=3.8)
    s.rect(470.0, 606.0, 42.0, 14.0, fill="#ffffff", stroke_width=3.8)
    s.rect(512.0, 592.0, 10.0, 42.0, fill="#ffffff", stroke_width=3.8)
    # Upper and lower brass dipole cylinders + clamps to vertical bar
    s.rect(532.0, 524.0, 16.0, 54.0, fill="#ffffff", stroke_width=4.2)
    s.rect(532.0, 646.0, 16.0, 54.0, fill="#ffffff", stroke_width=4.2)
    s.rect(548.0, 540.0, 12.0, 12.0, fill="#ffffff", stroke_width=3.5)
    s.rect(548.0, 672.0, 12.0, 12.0, fill="#ffffff", stroke_width=3.5)
    # Primary oscillator knobs inside mirror at x=540, y=594 & 630
    s.circle(540.0, 594.0, 18.0, fill="#ffffff", stroke_width=4.5)
    s.circle(540.0, 630.0, 18.0, fill="#ffffff", stroke_width=4.5)
    # Helical leads from induction coil to oscillator
    _helix(s, 174.0, 692.0, 360.0, 566.0, turns=11, amp=12.0, sw=4.0)
    s.path("M 360 566 Q 450 532, 526 588", stroke_width=4.5)
    s.path("M 286 692 Q 294 676, 304 676", stroke_width=4.0)
    _helix(s, 304.0, 676.0, 416.0, 666.0, turns=7, amp=11.0, sw=4.0)
    s.path("M 416 666 Q 480 666, 526 634", stroke_width=4.5)

    # Vertical 100 cm scale bar on right
    s.line(946.0, 354.0, 946.0, 932.0, stroke_width=sw)
    for i in range(11):
        y = 354.0 + i * 57.8
        tlen = 22.0 if i % 5 == 0 else 12.0
        s.line(946.0, y, 946.0 + tlen, y, stroke_width=4.5)

    # === BOTTOM: PLAN ===
    # Table top rectangle on left
    s.rect(6.0, 1364.0, 410.0, 452.0, fill="#ffffff", stroke_width=sw)
    # 3 battery cells in top row + inter-cell jumpers
    for bx in (138.0, 214.0, 290.0):
        s.rect(bx, 1412.0, 64.0, 68.0, fill="#ffffff", stroke_width=4.5)
        s.rect(bx + 12.0, 1424.0, 40.0, 44.0, fill="none", stroke_width=3.2)
    s.line(202.0, 1446.0, 214.0, 1446.0, stroke_width=4.5)
    s.line(278.0, 1446.0, 290.0, 1446.0, stroke_width=4.5)
    # Induction coil in plan
    s.rect(144.0, 1554.0, 208.0, 122.0, fill="#ffffff", stroke_width=sw * 0.9)
    s.rect(164.0, 1574.0, 168.0, 82.0, fill="#ffffff", stroke_width=sw * 0.8)
    # Coiled wire from left battery cell around left to induction coil
    s.path("M 138 1446 L 114 1446", stroke_width=4.0)
    _curved_helix(s, (114.0, 1446.0), (48.0, 1470.0), (46.0, 1542.0), turns=7, amp=9.0, sw=3.8)
    s.path("M 46 1542 Q 52 1620, 154 1620", stroke_width=4.0)
    # Coiled wire from right battery cell across to induction coil
    s.path("M 354 1446 Q 386 1446, 386 1474 Q 386 1502, 358 1502", stroke_width=4.0)
    _helix(s, 358.0, 1502.0, 150.0, 1514.0, turns=11, amp=9.5, sw=3.8)
    s.path("M 150 1514 Q 108 1526, 114 1564 Q 120 1594, 164 1598", stroke_width=4.0)
    # Two coiled connecting leads from induction coil to parabolic mirror
    _helix(s, 352.0, 1624.0, 470.0, 1624.0, turns=6, amp=9.5, sw=3.8)
    _curved_helix(s, (186.0, 1596.0), (304.0, 1502.0), (416.0, 1566.0), turns=11, amp=9.5, sw=3.8)
    s.path("M 416 1566 Q 444 1584, 470 1608", stroke_width=4.0)

    # Parabolic mirror plan on right
    # Three mounting blocks 'b' along the back of the mirror
    s.polygon([(738.0, 1292.0), (774.0, 1268.0), (786.0, 1284.0), (750.0, 1308.0)], fill="#ffffff", stroke_width=4.5)
    s.polygon([(496.0, 1484.0), (512.0, 1496.0), (486.0, 1542.0), (470.0, 1530.0)], fill="#ffffff", stroke_width=4.5)
    s.polygon([(486.0, 1682.0), (512.0, 1728.0), (496.0, 1740.0), (470.0, 1694.0)], fill="#ffffff", stroke_width=4.5)
    # Vertical back frame bar
    s.rect(796.0, 1266.0, 68.0, 648.0, fill="#ffffff", stroke_width=sw)
    # Parabolic curved sheet metal reflector
    s.path("M 796 1280 Q 470 1440, 470 1612 Q 470 1780, 796 1912", stroke_width=sw * 1.1)
    # Inner triangular wooden frame braces
    s.polygon([(580.0, 1576.0), (796.0, 1372.0), (796.0, 1284.0), (580.0, 1456.0)], fill="#ffffff", stroke_width=sw * 0.9)
    s.polygon([(580.0, 1648.0), (796.0, 1838.0), (796.0, 1912.0), (580.0, 1756.0)], fill="#ffffff", stroke_width=sw * 0.9)
    # Curved nose block
    s.path("M 580 1456 Q 474 1528, 474 1612 Q 474 1696, 580 1756 L 580 1456 Z", fill="#ffffff", stroke_width=sw * 0.9)
    # Small central oscillator block at the apex of the frame
    s.rect(574.0, 1596.0, 22.0, 32.0, fill="#ffffff", stroke_width=4.5, rx=5.0)

    # Labels (mask vertical rib lines behind 'a' labels)
    s.rect(650.0, 266.0, 48.0, 46.0, fill="#ffffff", stroke="none")
    lib.label(s, 674.0, 292.0, "a", size=58.0, italic=True, bold=True)
    s.rect(650.0, 838.0, 48.0, 46.0, fill="#ffffff", stroke="none")
    lib.label(s, 674.0, 864.0, "a", size=58.0, italic=True, bold=True)
    lib.label(s, 988.0, 354.0, "0", size=52.0, italic=True, bold=True)
    lib.label(s, 1002.0, 646.0, "50", size=52.0, italic=True, bold=True)
    lib.label(s, 1064.0, 928.0, "100 cm.", size=52.0, italic=True, bold=True)
    lib.label(s, 706.0, 1278.0, "b", size=56.0, italic=True, bold=True)
    lib.label(s, 470.0, 1466.0, "b", size=56.0, italic=True, bold=True)
    lib.label(s, 470.0, 1762.0, "b", size=56.0, italic=True, bold=True)

    s.save(out_svg)
