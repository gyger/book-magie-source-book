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
    s.rect(108.0, 774.0, 232.0, 20.0, fill="#ffffff", stroke_width=sw * 0.85)
    s.rect(144.0, 704.0, 158.0, 70.0, fill="#ffffff", stroke_width=sw * 0.9)
    s.rect(160.0, 718.0, 126.0, 42.0, fill="#ffffff", stroke_width=sw * 0.8)

    # Tall parabolic mirror housing (elevation)
    s.rect(456.0, 48.0, 408.0, 1142.0, fill="#ffffff", stroke_width=sw)
    # Top and bottom protruding wooden frame posts
    s.rect(474.0, 0.0, 38.0, 48.0, fill="#ffffff", stroke_width=sw * 0.85)
    s.rect(752.0, 0.0, 44.0, 48.0, fill="#ffffff", stroke_width=sw * 0.85)
    s.rect(474.0, 1190.0, 38.0, 64.0, fill="#ffffff", stroke_width=sw * 0.85)
    s.rect(752.0, 1190.0, 44.0, 64.0, fill="#ffffff", stroke_width=sw * 0.85)
    # Horizontal clamping frames a, a
    s.rect(456.0, 314.0, 408.0, 22.0, fill="#ffffff", stroke_width=sw * 0.9)
    s.rect(456.0, 886.0, 408.0, 22.0, fill="#ffffff", stroke_width=sw * 0.9)
    # Vertical sheet-metal shading lines
    for x in (474, 496, 534, 574, 636, 686, 744):
        s.line(float(x), 54.0, float(x), 1184.0, stroke_width=3.5)
    # Primary oscillator knobs inside mirror at x=540, y=540..660
    s.circle(540.0, 594.0, 18.0, fill="#ffffff", stroke_width=4.5)
    s.circle(540.0, 630.0, 18.0, fill="#ffffff", stroke_width=4.5)
    # Helical leads from induction coil to oscillator
    _helix(s, 174.0, 696.0, 360.0, 566.0, turns=11, amp=12.0, sw=4.0)
    s.path("M 360 566 Q 450 532, 526 588", stroke_width=4.5)
    _helix(s, 300.0, 680.0, 416.0, 666.0, turns=7, amp=11.0, sw=4.0)
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
    # 3 battery cells in top row
    for bx in (138.0, 214.0, 290.0):
        s.rect(bx, 1412.0, 64.0, 68.0, fill="#ffffff", stroke_width=4.5)
        s.rect(bx + 12.0, 1424.0, 40.0, 44.0, fill="none", stroke_width=3.2)
    # Induction coil in plan
    s.rect(144.0, 1554.0, 208.0, 122.0, fill="#ffffff", stroke_width=sw * 0.9)
    s.rect(164.0, 1574.0, 168.0, 82.0, fill="#ffffff", stroke_width=sw * 0.8)
    # Coiled connecting wires to mirror
    _helix(s, 352.0, 1624.0, 466.0, 1624.0, turns=6, amp=10.0, sw=4.0)
    _helix(s, 144.0, 1522.0, 360.0, 1502.0, turns=12, amp=10.0, sw=4.0)

    # Parabolic mirror plan on right
    # Vertical back frame bar
    s.rect(796.0, 1266.0, 68.0, 648.0, fill="#ffffff", stroke_width=sw)
    # Parabolic curved sheet metal reflector
    s.path("M 796 1280 Q 470 1440, 470 1612 Q 470 1780, 796 1912", stroke_width=sw * 1.1)
    # Inner triangular wooden frame braces
    s.polygon([(580.0, 1576.0), (796.0, 1372.0), (796.0, 1284.0), (580.0, 1456.0)], fill="#ffffff", stroke_width=sw * 0.9)
    s.polygon([(580.0, 1648.0), (796.0, 1838.0), (796.0, 1912.0), (580.0, 1756.0)], fill="#ffffff", stroke_width=sw * 0.9)
    # Curved nose block
    s.path("M 580 1456 Q 474 1528, 474 1612 Q 474 1696, 580 1756 L 580 1456 Z", fill="#ffffff", stroke_width=sw * 0.9)

    # Labels
    lib.label(s, 672.0, 294.0, "a", size=58.0, italic=True, bold=True)
    lib.label(s, 686.0, 864.0, "a", size=58.0, italic=True, bold=True)
    lib.label(s, 988.0, 354.0, "0", size=52.0, italic=True, bold=True)
    lib.label(s, 1002.0, 646.0, "50", size=52.0, italic=True, bold=True)
    lib.label(s, 1064.0, 928.0, "100 cm.", size=52.0, italic=True, bold=True)
    lib.label(s, 738.0, 1296.0, "b", size=56.0, italic=True, bold=True)
    lib.label(s, 476.0, 1476.0, "b", size=56.0, italic=True, bold=True)
    lib.label(s, 476.0, 1746.0, "b", size=56.0, italic=True, bold=True)

    s.save(out_svg)
