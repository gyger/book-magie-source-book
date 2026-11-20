"""Figure 98: Crookes tube for projection of molecular shadows with plans of a, b and c, d."""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image

import draw
import library as lib


def _pinch_seal(s: draw.Scene, x: float, y: float, dx: float, dy: float, length: float = 95.0, sw: float = 5.5) -> None:
    """Draw a Crookes glass-pinch electrode seal pointing along unit vector (dx, dy) from outer eyelet (x, y)."""
    nx, ny = -dy, dx
    # Outer tiny eyelet ring
    s.circle(x, y, 10.0, fill="#ffffff", stroke_width=sw * 0.85)
    # Tapered glass pinch cone
    p1 = (x + dx * 12 + nx * 16, y + dy * 12 + ny * 16)
    p2 = (x + dx * length + nx * 8, y + dy * length + ny * 8)
    p3 = (x + dx * length - nx * 8, y + dy * length - ny * 8)
    p4 = (x + dx * 12 - nx * 16, y + dy * 12 - ny * 16)
    s.polygon([p1, p2, p3, p4], fill="#ffffff", stroke_width=sw * 0.8)
    # Cross-ticks inside glass pinch
    for t in (0.25, 0.42, 0.58, 0.74, 0.88):
        cx = x + dx * (12 + t * (length - 12))
        cy = y + dy * (12 + t * (length - 12))
        hw = 14.0 - t * 6.0
        s.line(cx - nx * hw, cy - ny * hw, cx + nx * hw, cy + ny * hw, stroke_width=3.5)


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.5
    # === Left vertical Crookes tube ===
    # Upper section + central diaphragm flange + lower section + exhaust tail
    d_tube = (
        "M 122 746 L 122 158 "
        "A 188 114 0 0 1 498 158 "
        "L 498 746 "
        "Q 528 746, 528 762 Q 528 778, 498 778 "
        "L 500 1356 "
        "A 190 220 0 0 1 122 1356 "
        "C 122 1320, 74 1344, 74 1420 "
        "L 74 1742 Q 46 1762, 20 1742 L 20 1420 "
        "C 20 1330, 122 1320, 122 1280 "
        "L 122 778 "
        "Q 86 778, 86 762 Q 86 746, 122 746 Z"
    )
    s.path(d_tube, stroke_width=sw)

    # Central horizontal glass partition a with aperture/screen b
    s.line(96.0, 762.0, 518.0, 762.0, stroke_width=sw)
    s.rect(188.0, 750.0, 118.0, 12.0, fill="#000000", stroke="none")
    s.rect(318.0, 750.0, 118.0, 12.0, fill="#000000", stroke="none")

    # Electrodes e, f (top), c (upper-right), d (lower-right), g, h (bottom)
    _pinch_seal(s, 242.0, 26.0, 0.0, 1.0, 100.0, sw)
    s.line(242.0, 126.0, 242.0, 180.0, stroke_width=sw)
    s.line(212.0, 180.0, 276.0, 180.0, stroke_width=sw * 1.1)

    _pinch_seal(s, 362.0, 26.0, 0.0, 1.0, 100.0, sw)
    s.polygon([(362.0, 126.0), (374.0, 160.0), (362.0, 198.0), (350.0, 160.0)], fill="#000000", stroke="none")

    _pinch_seal(s, 518.0, 444.0, -1.0, 0.0, 105.0, sw)
    s.line(413.0, 444.0, 262.0, 444.0, stroke_width=sw)
    s.line(262.0, 444.0, 374.0, 444.0, stroke_width=sw * 1.5)

    _pinch_seal(s, 520.0, 1124.0, -1.0, 0.0, 105.0, sw)
    s.line(415.0, 1124.0, 264.0, 1124.0, stroke_width=sw)
    s.line(264.0, 1124.0, 376.0, 1124.0, stroke_width=sw * 1.5)

    _pinch_seal(s, 246.0, 1596.0, 0.0, -1.0, 100.0, sw)
    s.polygon([(246.0, 1496.0), (258.0, 1468.0), (246.0, 1434.0), (234.0, 1468.0)], fill="#000000", stroke="none")

    _pinch_seal(s, 368.0, 1598.0, 0.0, -1.0, 96.0, sw)
    s.line(336.0, 1502.0, 402.0, 1502.0, stroke_width=sw * 1.1)

    # === Top-right: Plan of a, b ===
    cx1, cy1 = 1078.0, 434.0
    s.circle(cx1, cy1, 222.0, fill="none", stroke_width=sw)
    s.circle(cx1, cy1, 196.0, fill="none", stroke_width=sw * 0.85)
    # Inner horizontal crescents
    s.path("M 920 326 Q 1078 240, 1236 326", stroke_width=sw * 0.85)
    s.path("M 920 542 Q 1078 628, 1236 542", stroke_width=sw * 0.85)
    # Central square aperture b rotated 45 deg
    s.polygon([
        (cx1, cy1 - 140.0), (cx1 + 146.0, cy1),
        (cx1, cy1 + 140.0), (cx1 - 146.0, cy1),
    ], fill="#ffffff", stroke_width=sw)

    # === Bottom-right: Plan of c and d ===
    cx2, cy2 = 1074.0, 1200.0
    s.circle(cx2, cy2, 198.0, fill="none", stroke_width=sw)
    # 8-pointed star at center
    star_pts = []
    for i in range(16):
        ang = math.radians(i * 22.5)
        r = 72.0 if i % 2 == 0 else 36.0
        star_pts.append((cx2 + r * math.cos(ang), cy2 + r * math.sin(ang)))
    s.polygon(star_pts, fill="#ffffff", stroke_width=sw * 0.85)
    # Small holes in star
    for dx, dy in [(0, 0), (-18, -18), (18, -18), (-18, 18), (18, 18)]:
        lib.filled_dot(s, cx2 + dx, cy2 + dy, r=6.5)
    # Side stem and pinch seal on right
    s.line(cx2 + 72.0, cy2, 1185.0, cy2, stroke_width=sw * 0.9)
    _pinch_seal(s, 1308.0, cy2, -1.0, 0.0, 118.0, sw)

    # Labels
    lib.label(s, 242.0, 214.0, "e", size=58.0, italic=True, bold=True)
    lib.label(s, 360.0, 224.0, "f", size=58.0, italic=True, bold=True)
    lib.label(s, 304.0, 480.0, "c", size=58.0, italic=True, bold=True)
    lib.label(s, 148.0, 738.0, "a", size=58.0, italic=True, bold=True)
    lib.label(s, 404.0, 796.0, "b", size=58.0, italic=True, bold=True)
    lib.label(s, 310.0, 1164.0, "d", size=58.0, italic=True, bold=True)
    lib.label(s, 244.0, 1412.0, "g", size=58.0, italic=True, bold=True)
    lib.label(s, 368.0, 1474.0, "h", size=58.0, italic=True, bold=True)

    lib.label(s, 916.0, 382.0, "a", size=60.0, italic=True, bold=True)
    lib.label(s, 1226.0, 382.0, "a", size=60.0, italic=True, bold=True)
    lib.label(s, 1076.0, 444.0, "b", size=64.0, italic=True, bold=True)
    lib.label(s, 1096.0, 694.0, "Plan of a, b", size=56.0, italic=True, bold=True)
    lib.label(s, 1088.0, 1456.0, "Plan of c and d", size=56.0, italic=True, bold=True)

    s.save(out_svg)
