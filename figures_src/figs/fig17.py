"""Figure 17: Newton's pendulum collision diagram."""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image

import draw
import library as lib


def _draw_tick(s: draw.Scene, cx: float, cy: float, r: float, deg: float, length: float = 24.0, sw: float = 3.5) -> None:
    rad = math.radians(deg)
    x1 = cx + (r - length * 0.5) * math.cos(rad)
    y1 = cy + (r - length * 0.5) * math.sin(rad)
    x2 = cx + (r + length * 0.5) * math.cos(rad)
    y2 = cy + (r + length * 0.5) * math.sin(rad)
    s.line(x1, y1, x2, y2, stroke_width=sw)


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    # Top horizontal bar E-G-C-D-F-H
    y_bar_l, y_bar_r = 80.0, 74.5
    s.line(48.0, y_bar_l, 1502.0, y_bar_r, stroke_width=5.5)

    # Suspension points C and D
    C = (709.5, 77.5)
    D = (845.4, 77.0)

    # Ball A and Ball B centers & radii
    A_c = (706.5, 728.0)
    rA = 83.0
    B_c = (845.4, 736.0)
    rB = 46.0

    # Vertical strings C -> top of Ball A, D -> top of Ball B
    s.line(C[0], C[1], C[0], A_c[1] - rA, stroke_width=5.5)
    s.line(D[0], D[1], D[0], B_c[1] - rB, stroke_width=5.5)

    # Elliptical/circular arcs matching the scan's slight aspect ratio
    def _earc(cx: float, cy: float, rx: float, ry: float, deg1: float, deg2: float, sweep: int) -> None:
        a1, a2 = math.radians(deg1), math.radians(deg2)
        x1, y1 = cx + rx * math.cos(a1), cy + ry * math.sin(a1)
        x2, y2 = cx + rx * math.cos(a2), cy + ry * math.sin(a2)
        s.path(f"M {x1:.2f} {y1:.2f} A {rx:.2f} {ry:.2f} 0 0 {sweep} {x2:.2f} {y2:.2f}", stroke_width=5.0)

    # Left outer arc (E to left side of Ball A), centered at C
    rx_EA, ry_EA = 653.0, 662.0
    _earc(C[0], C[1], rx_EA, ry_EA, 179.8, 97.5, sweep=0)

    # Left inner arc (G to left side of Ball A), centered at D
    rx_GB, ry_GB = 659.5, 670.0
    _earc(D[0], D[1], rx_GB, ry_GB, 179.8, 109.5, sweep=0)

    # Right inner arc (F to right side of Ball B), centered at C
    rx_AF, ry_AF = 646.0, 656.0
    _earc(C[0], C[1], rx_AF, ry_AF, 0.0, 73.5, sweep=1)

    # Right outer arc (H to right side of Ball B), centered at D
    rx_BH, ry_BH = 650.0, 666.0
    _earc(D[0], D[1], rx_BH, ry_BH, 0.0, 85.8, sweep=1)

    # Ticks on left outer arc (R, S, T, V)
    for deg in (158.2, 153.2, 148.2, 143.0):
        _draw_tick(s, C[0], C[1], 0.5 * (rx_EA + ry_EA), deg, length=24.0, sw=3.5)

    # Ticks on right inner arc (v, t, s, r)
    for deg in (36.0, 41.2, 46.2, 51.2):
        _draw_tick(s, C[0], C[1], 0.5 * (rx_AF + ry_AF), deg, length=22.0, sw=3.5)

    # Ticks on right outer arc (l, k)
    for deg in (17.2, 23.8):
        _draw_tick(s, D[0], D[1], 0.5 * (rx_BH + ry_BH), deg, length=22.0, sw=3.5)

    # Balls A and B (drawn cleanly, subtle inner shading arc on right side)
    s.circle(A_c[0], A_c[1], rA, fill="#ffffff", stroke="#000000", stroke_width=5.5)
    s.arc(A_c[0], A_c[1], rA - 12.0, -35.0, 40.0, stroke_width=3.0, sweep=1)
    s.arc(A_c[0], A_c[1], rA - 22.0, -25.0, 32.0, stroke_width=2.2, sweep=1)

    s.circle(B_c[0], B_c[1], rB, fill="#ffffff", stroke="#000000", stroke_width=5.0)
    s.arc(B_c[0], B_c[1], rB - 8.0, -35.0, 40.0, stroke_width=2.5, sweep=1)

    # Top labels
    for txt, x, y in [
        ("E", 48, 44),
        ("G", 178, 44),
        ("C", 701, 42),
        ("D", 840, 44),
        ("F", 1345, 41),
        ("H", 1484, 42),
    ]:
        lib.label(s, x, y, txt, size=48, italic=False, bold=True)

    # Left arc tick labels R, S, T, V
    for txt, x, y in [
        ("R", 58, 320),
        ("S", 80, 372),
        ("T", 106, 424),
        ("V", 134, 477),
    ]:
        lib.label(s, x, y, txt, size=44, italic=False, bold=True)

    # Right inner arc tick labels v, t, s, r (italic)
    for txt, x, y in [
        ("v", 1207, 445),
        ("t", 1184, 488),
        ("s", 1143, 526),
        ("r", 1107, 564),
    ]:
        lib.label(s, x, y, txt, size=44, italic=True, bold=True)

    # Right outer arc tick labels l, k (italic)
    lib.label(s, 1499, 265, "l", size=46, italic=True, bold=True)
    lib.label(s, 1483, 336, "k", size=46, italic=True, bold=True)

    # Ball labels A, B
    lib.label(s, 703, 738, "A", size=46, italic=False, bold=True)
    lib.label(s, 846, 738, "B", size=42, italic=False, bold=True)

    s.save(out_svg)
