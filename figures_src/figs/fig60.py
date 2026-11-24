"""Figure 60: Huygens's construction of the refraction of a plane wave AC at surface AB."""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 5.5
    sw_thin = 4.2

    # Medium boundary box (left edge, top surface AB, bottom edge)
    ax, ay = 319.0, 368.0
    bx, by = 1044.0, 368.0
    s.line(85.0, ay, bx, ay, stroke_width=sw)
    s.line(85.0, ay, 85.0, 859.0, stroke_width=sw)
    s.line(85.0, 859.0, w - 35.0, 859.0, stroke_width=sw)

    # Vertical normal E-A-F (slight lean)
    s.line(321.0, 38.0, 318.0, 704.0, stroke_width=sw)

    # Incident wavefront A-C
    cx, cy = 518.0, 58.0
    s.line(ax, ay, cx, cy, stroke_width=sw_thin)

    # Ray D-A (parallel to C-B)
    dx_cb = bx - cx
    dy_cb = by - cy
    L_cb = math.hypot(dx_cb, dy_cb)
    ux, uy = dx_cb / L_cb, dy_cb / L_cb
    s.line(ax - ux * 350.0, ay - uy * 350.0, ax, ay, stroke_width=sw_thin)

    # Continuation of A-G (parallel to C-B) and B-G (parallel to A-C)
    gx = ax + dx_cb
    gy = ay + dy_cb + 4.0
    s.line(bx, by, gx, gy, stroke_width=sw_thin)

    # 5 parallel rays from C, H, H, H, A down-right to B, M, M, M, G
    for i in range(5):
        t = i / 4.0
        hx = ax + (cx - ax) * t
        hy = ay + (cy - ay) * t
        mx = gx + (bx - gx) * t
        my = gy + (by - gy) * t
        s.line(hx, hy, mx, my, stroke_width=sw_thin)

    # Points K1, K2, K3 on AB and parallel wavefront lines K-L (up-right parallel to AC)
    for i in (1, 2, 3):
        t = i / 4.0
        kx = ax + (bx - ax) * t
        ky = ay
        lx = kx + (cx - ax) * (1.0 - t)
        ly = ky + (cy - ay) * (1.0 - t)
        s.line(kx, ky, lx, ly, stroke_width=3.8)

    # Refracted wavefront B-N tangent to sphere around A of radius r_a ≈ 388
    nx, ny = 538.0, 688.0
    r_a = math.hypot(nx - ax, ny - ay)
    # Tangent line B-N extended slightly past N
    ux_bn = (nx - bx) / math.hypot(nx - bx, ny - by)
    uy_bn = (ny - by) / math.hypot(nx - bx, ny - by)
    s.line(bx, by, nx + ux_bn * 155.0, ny + uy_bn * 155.0, stroke_width=sw)

    # Refracted ray A-N and secondary wavelet arcs centered at K1, K2, K3 tangent to BN
    s.line(ax, ay, nx, ny, stroke_width=sw_thin)
    ang_an = math.degrees(math.atan2(ny - ay, nx - ax))
    # Angular spans (start_deg, end_deg) for K1, K2, K3 wavelets matching original scan
    wavelet_spans = {
        1: (22.0, 96.5),
        2: (16.0, 106.0),
        3: (0.0, 108.0),
    }
    for i in (1, 2, 3):
        t = i / 4.0
        kx = ax + (bx - ax) * t
        ky = ay
        rk = r_a * (1.0 - t)
        a0, a1 = wavelet_spans[i]
        s.arc(kx, ky, rk, a0, a1, stroke_width=4.0, sweep=1)

    # Main wavelet arc centered at A through N and S
    s.arc(ax, ay, r_a, 24.0, 91.5, stroke_width=sw_thin, sweep=1)

    # Lines from K1, K2, K3 going down-left parallel to BN to A-N (points O, O, O)
    for i in (1, 2, 3):
        t = i / 4.0
        kx = ax + (bx - ax) * t
        ky = ay
        ox = ax + (nx - ax) * t
        oy = ay + (ny - ay) * t
        s.line(kx, ky, ox, oy, stroke_width=3.8)

    # Labels
    lib.label(s, 344.0, 74.0, "E", size=48.0, italic=False, bold=True)
    lib.label(s, 470.0, 62.0, "C", size=48.0, italic=False, bold=True)
    lib.label(s, 32.0, 162.0, "D", size=48.0, italic=False, bold=True)
    lib.label(s, 424.0, 136.0, "H", size=42.0, italic=False, bold=True)
    lib.label(s, 378.0, 212.0, "H", size=42.0, italic=False, bold=True)
    lib.label(s, 336.0, 288.0, "H", size=42.0, italic=False, bold=True)
    lib.label(s, 684.0, 118.0, "L", size=44.0, italic=False, bold=True)
    lib.label(s, 796.0, 182.0, "L", size=44.0, italic=False, bold=True)
    lib.label(s, 936.0, 264.0, "L", size=44.0, italic=False, bold=True)
    lib.label(s, 286.0, 400.0, "A", size=48.0, italic=False, bold=True)
    lib.label(s, 494.0, 324.0, "K", size=44.0, italic=False, bold=True)
    lib.label(s, 678.0, 324.0, "K", size=44.0, italic=False, bold=True)
    lib.label(s, 858.0, 324.0, "K", size=44.0, italic=False, bold=True)
    lib.label(s, 1068.0, 368.0, "B", size=48.0, italic=False, bold=True)
    lib.label(s, 348.0, 456.0, "O", size=40.0, italic=False, bold=True)
    lib.label(s, 392.0, 530.0, "O", size=40.0, italic=False, bold=True)
    lib.label(s, 444.0, 602.0, "O", size=40.0, italic=False, bold=True)
    lib.label(s, 344.0, 674.0, "F", size=46.0, italic=False, bold=True)
    lib.label(s, 404.0, 714.0, "S", size=46.0, italic=False, bold=True)
    lib.label(s, 544.0, 722.0, "N", size=48.0, italic=False, bold=True)
    lib.label(s, 608.0, 576.0, "R", size=46.0, italic=False, bold=True)
    lib.label(s, 1028.0, 440.0, "M", size=42.0, italic=False, bold=True)
    lib.label(s, 982.0, 516.0, "M", size=42.0, italic=False, bold=True)
    lib.label(s, 932.0, 596.0, "M", size=42.0, italic=False, bold=True)
    lib.label(s, 878.0, 678.0, "G", size=48.0, italic=False, bold=True)

    s.save(out_svg)
