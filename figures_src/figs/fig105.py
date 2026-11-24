"""Figure 105: Perrin's Faraday-cylinder cathode-ray charge tube."""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image

import draw
import library as lib


def _helix(s: draw.Scene, x1: float, y1: float, x2: float, y2: float, turns: int, amp: float, sw: float) -> None:
    """Draw a coiled helical wire from (x1, y1) to (x2, y2)."""
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    if L < 1e-6:
        return
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    pts = []
    steps = turns * 16
    for i in range(steps + 1):
        t = i / steps
        ang = t * turns * 2.0 * math.pi
        px = x1 + dx * t + ux * (amp * 0.45 * math.sin(ang)) + nx * (amp * math.cos(ang))
        py = y1 + dy * t + uy * (amp * 0.45 * math.sin(ang)) + ny * (amp * math.cos(ang))
        pts.append((px, py))
    s.polyline(pts, stroke_width=sw)


def _curved_helix(
    s: draw.Scene,
    x1: float, y1: float,
    cx: float, cy: float,
    x2: float, y2: float,
    turns: int, amp: float, sw: float,
) -> None:
    """Draw a coiled helical wire along a quadratic Bezier curve."""
    pts = []
    steps = turns * 16
    for i in range(steps + 1):
        t = i / steps
        mt = 1.0 - t
        bx = mt * mt * x1 + 2.0 * mt * t * cx + t * t * x2
        by = mt * mt * y1 + 2.0 * mt * t * cy + t * t * y2
        tx = 2.0 * mt * (cx - x1) + 2.0 * t * (x2 - cx)
        ty = 2.0 * mt * (cy - y1) + 2.0 * t * (y2 - cy)
        L = math.hypot(tx, ty)
        if L < 1e-6:
            continue
        ux, uy = tx / L, ty / L
        nx, ny = -uy, ux
        ang = t * turns * 2.0 * math.pi
        px = bx + ux * (amp * 0.45 * math.sin(ang)) + nx * (amp * math.cos(ang))
        py = by + uy * (amp * 0.45 * math.sin(ang)) + ny * (amp * math.cos(ang))
        pts.append((px, py))
    s.polyline(pts, stroke_width=sw)


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.5
    # Outer glass tube envelope
    d_glass = (
        "M 2374 278 L 2280 278 C 2180 278, 2080 162, 1900 162 "
        "L 360 162 C 300 162, 290 220, 260 258 "
        "Q 226 286, 232 308 Q 250 326, 270 350 "
        "C 295 390, 310 450, 380 450 "
        "L 1930 450 C 2090 450, 2180 340, 2310 340 L 2374 340"
    )
    s.path(d_glass, stroke_width=sw)

    # Inner glass insulating sleeve around lead S on left
    s.path("M 264 256 C 320 274, 420 276, 484 298", stroke_width=sw * 0.75)
    s.path("M 272 346 C 324 326, 420 324, 484 304", stroke_width=sw * 0.75)

    # Grounded shielding cylinder EFGH
    s.polyline([(350.0, 256.0), (350.0, 190.0), (1244.0, 190.0), (1244.0, 268.0)], stroke_width=sw)
    s.polyline([(350.0, 340.0), (350.0, 418.0), (1244.0, 418.0), (1244.0, 336.0)], stroke_width=sw)

    # Inner Faraday cylinder ABCD
    s.polyline([
        (1002.0, 276.0), (1002.0, 238.0), (584.0, 238.0),
        (584.0, 358.0), (1002.0, 358.0), (1002.0, 318.0),
    ], stroke_width=sw)

    # Lead wire from AD through glass sleeve to electroscope coil
    s.line(170.0, 300.0, 584.0, 300.0, stroke_width=sw)
    _helix(s, 170.0, 304.0, 114.0, 392.0, turns=6, amp=16.0, sw=4.5)

    # Ground wire + coil Sol. from top of EFGH
    s.polyline([(828.0, 190.0), (832.0, 94.0), (860.0, 94.0)], stroke_width=sw)
    _helix(s, 860.0, 96.0, 1036.0, 96.0, turns=9, amp=16.0, sw=4.5)

    # Cathode N on right and curved lead wire + helical coil
    s.line(2066.0, 228.0, 2066.0, 382.0, stroke_width=12.0)
    s.path("M 2066 294 L 2145 294 Q 2210 294, 2246 238", stroke_width=sw)
    _curved_helix(s, 2238.0, 232.0, 2150.0, 110.0, 2000.0, 82.0, turns=13, amp=16.0, sw=4.5)

    # Labels
    lib.label(s, 1100.0, 100.0, "Sol.", size=52.0, italic=True, bold=True)
    lib.label(s, 326.0, 208.0, "E", size=54.0, italic=False, bold=True)
    lib.label(s, 1268.0, 224.0, "F", size=54.0, italic=False, bold=True)
    lib.label(s, 1272.0, 392.0, "G", size=54.0, italic=False, bold=True)
    lib.label(s, 328.0, 404.0, "H", size=54.0, italic=False, bold=True)
    lib.label(s, 422.0, 240.0, "γ", size=54.0, italic=True, bold=True)
    lib.label(s, 478.0, 272.0, "S", size=54.0, italic=False, bold=True)
    lib.label(s, 608.0, 274.0, "A", size=54.0, italic=False, bold=True)
    lib.label(s, 608.0, 330.0, "D", size=54.0, italic=False, bold=True)
    lib.label(s, 972.0, 274.0, "B", size=54.0, italic=False, bold=True)
    lib.label(s, 970.0, 330.0, "C", size=54.0, italic=False, bold=True)
    lib.label(s, 1024.0, 300.0, "α", size=54.0, italic=True, bold=True)
    lib.label(s, 1208.0, 306.0, "β", size=54.0, italic=True, bold=True)
    lib.label(s, 2092.0, 332.0, "N", size=54.0, italic=False, bold=True)
    lib.label(s, 158.0, 468.0, "Electroscope", size=54.0, italic=True, bold=True)

    s.save(out_svg)
