"""Figure 29: Cavendish torsion balance — plan (top) view showing wooden case AA, torsion arm h-h, and lead spheres W-W / w-w."""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image

import draw
import library as lib


def _tapered_bar_pts(
    x1: float, y1: float, x2: float, y2: float, r_end: float = 12.0, r_mid: float = 28.0
) -> list[tuple[float, float]]:
    """Return polygon points for a symmetric tapered bar from (x1,y1) to (x2,y2)."""
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    mx, my = (x1 + x2) * 0.5, (y1 + y2) * 0.5
    return [
        (x1 + nx * r_end, y1 + ny * r_end),
        (mx + nx * r_mid, my + ny * r_mid),
        (x2 + nx * r_end, y2 + ny * r_end),
        (x2 - nx * r_end, y2 - ny * r_end),
        (mx - nx * r_mid, my - ny * r_mid),
        (x1 - nx * r_end, y1 - ny * r_end),
    ]


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    cx, cy = 1066.0, 336.0

    # --- 1) Large dashed reference circle M-M ---
    s.circle(cx, cy, 248.0, stroke_width=6.0, dash="22,14")

    # --- 2) Dashed alternate position of lead spheres w-w and connecting bar ---
    w1 = (306.0, 144.0)
    w2 = (1836.0, 530.0)
    s.circle(w1[0], w1[1], 125.0, stroke_width=6.0, dash="22,14")
    s.circle(w2[0], w2[1], 132.0, stroke_width=6.0, dash="22,14")
    bar_dash = _tapered_bar_pts(w1[0], w1[1], w2[0], w2[1], r_end=11.0, r_mid=24.0)
    s.polygon(bar_dash, fill="none", stroke="#000000", stroke_width=5.0, dash="22,14")

    # --- 3) Solid position of lead spheres W-W and connecting bar ---
    W1 = (304.0, 550.0)
    W2 = (1820.0, 142.0)
    s.circle(W1[0], W1[1], 134.0, fill="none", stroke="#000000", stroke_width=6.0)
    s.circle(W2[0], W2[1], 126.0, fill="none", stroke="#000000", stroke_width=6.0)
    bar_solid = _tapered_bar_pts(W1[0], W1[1], W2[0], W2[1], r_end=11.0, r_mid=25.0)
    s.polygon(bar_solid, fill="none", stroke="#000000", stroke_width=5.5)

    # --- 4) Central vertical strut with two small circles S-S ---
    s.rect(1045.0, 192.0, 42.0, 280.0, fill="#ffffff", stroke="#000000", stroke_width=5.0)
    s.circle(1066.0, 192.0, 21.0, fill="#ffffff", stroke="#000000", stroke_width=5.0)
    s.circle(1066.0, 472.0, 21.0, fill="#ffffff", stroke="#000000", stroke_width=5.0)

    # --- 5) Horizontal wooden housing box A-A (thick walls) ---
    # Left & right end caps S
    s.rect(162.0, 322.0, 50.0, 44.0, fill="#ffffff", stroke="#000000", stroke_width=5.0)
    s.circle(182.0, 344.0, 21.0, fill="#ffffff", stroke="#000000", stroke_width=5.0)
    s.rect(1938.0, 316.0, 52.0, 44.0, fill="#ffffff", stroke="#000000", stroke_width=5.0)
    s.circle(1970.0, 338.0, 21.0, fill="#ffffff", stroke="#000000", stroke_width=5.0)

    # Outer housing polygon (transparent interior so diagonal bar lines remain visible inside)
    s.polygon(
        [(214.0, 286.0), (1938.0, 280.0), (1938.0, 390.0), (214.0, 396.0)],
        fill="none",
        stroke="#000000",
        stroke_width=17.0,
        linejoin="miter",
    )

    # --- 6) Inner torsion rod with small lead balls h-h ---
    s.circle(273.0, 342.0, 21.0, fill="none", stroke="#000000", stroke_width=4.5)
    s.circle(1876.0, 330.0, 21.0, fill="none", stroke="#000000", stroke_width=4.5)

    arm_pts = _tapered_bar_pts(260.0, 342.0, 1884.0, 330.0, r_end=5.5, r_mid=18.0)
    s.polygon(arm_pts, fill="none", stroke="#000000", stroke_width=4.5)
    for i in range(1, 70):
        t = i / 70.0
        tx = 260.0 + (1884.0 - 260.0) * t
        ty = 342.0 + (330.0 - 342.0) * t
        half_h = 5.5 + (18.0 - 5.5) * (1.0 - abs(2.0 * t - 1.0))
        s.line(tx, ty - half_h, tx, ty + half_h, stroke_width=2.2)

    # --- 7) Labels ---
    lib.label(s, 280.0, 112.0, "w", size=54.0, italic=True, bold=True)
    lib.label(s, 1844.0, 100.0, "W", size=54.0, italic=True, bold=True)
    lib.label(s, 282.0, 514.0, "W", size=54.0, italic=True, bold=True)
    lib.label(s, 1868.0, 520.0, "w", size=54.0, italic=True, bold=True)

    lib.label(s, 1260.0, 128.0, "M", size=56.0, italic=False, bold=True)
    lib.label(s, 868.0, 544.0, "M", size=56.0, italic=False, bold=True)

    lib.label(s, 1114.0, 184.0, "S", size=54.0, italic=True, bold=True)
    lib.label(s, 1114.0, 476.0, "S", size=54.0, italic=False, bold=True)

    lib.label(s, 174.0, 276.0, "A", size=52.0, italic=False, bold=True)
    lib.label(s, 128.0, 344.0, "S", size=54.0, italic=True, bold=True)
    lib.label(s, 174.0, 412.0, "A", size=52.0, italic=False, bold=True)

    lib.label(s, 1975.0, 266.0, "A", size=52.0, italic=False, bold=True)
    lib.label(s, 2026.0, 336.0, "S", size=54.0, italic=True, bold=True)
    lib.label(s, 1972.0, 404.0, "A", size=52.0, italic=False, bold=True)

    lib.label(s, 314.0, 314.0, "h", size=50.0, italic=True, bold=True)
    lib.label(s, 1836.0, 356.0, "h", size=50.0, italic=True, bold=True)

    s.save(out_svg)
