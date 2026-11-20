"""Figure 59: Huygens's construction of the reflection of a plane wave AC at surface AB."""

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

    # Mirror surface A-B
    ax, ay = 197.0, 748.0
    bx, by = 1094.0, 748.0
    s.line(ax, ay, bx, by, stroke_width=sw)

    # Wavefront C (top of incident wavefront AC)
    cx, cy = 394.0, 396.0
    # Reflected wavefront N (symmetric to G across AB)
    gx, gy = 890.0, 1114.0
    nx, ny = 905.0, 396.0

    # AC, BG, BN, AN
    s.line(ax, ay, cx, cy, stroke_width=sw_thin)
    s.line(bx, by, gx, gy, stroke_width=sw_thin)
    s.line(bx, by, nx, ny, stroke_width=sw)
    s.line(ax, ay, nx, ny, stroke_width=sw_thin)

    # Direction of incident rays: C -> B
    dx_cb = bx - cx
    dy_cb = by - cy
    L_cb = math.hypot(dx_cb, dy_cb)
    ux, uy = dx_cb / L_cb, dy_cb / L_cb

    # 5 incident rays at t = 0, 0.25, 0.5, 0.75, 1.0 along AC
    # Extend behind AC by 230px
    for i in range(5):
        t = i / 4.0
        hx = ax + (cx - ax) * t
        hy = ay + (cy - ay) * t
        # Start behind wavefront
        sx = hx - ux * 220.0
        sy = hy - uy * 220.0
        # End on BG
        ex = gx + (bx - gx) * t
        ey = gy + (by - gy) * t
        s.line(sx, sy, ex, ey, stroke_width=sw_thin)

    # Points K1, K2, K3 on AB (where rays 1, 2, 3 hit AB)
    # Wait: ray i hits AB at x_k = ax + (bx - ax) * (1 - t) ? No:
    # Ray 4 (t=1, through C) hits B (t_ab=1). Ray 0 (t=0, through A) hits A (t_ab=0).
    # Ray i hits AB at t_ab = t!
    for i in (1, 2, 3):
        t = i / 4.0
        kx = ax + (bx - ax) * t
        ky = ay
        # Intermediate wavefront parallel to AC from K up to CB? Wait:
        # In Huygens's diagram:
        # Line from K_i going up-left to CB (parallel to AC? Actually perpendicular to CB!)
        # And line from K_i going up-right to AN (perpendicular to BN, i.e., parallel to AN? No, reflected rays go up-right parallel to A-N? Let's check!)
        # Wait: A-N is perpendicular to B-N!
        # Let's draw lines from K_i parallel to AC up to CB (points L) and from K_i parallel to AN up to BN?
        # Look at fig59: from K1(421,746), K2(645,746), K3(870,746):
        # Going UP-RIGHT parallel to AC (slope of AC): hits CB at L1, L2, L3!
        # Going UP-LEFT parallel to BN (slope of BN): hits AN at O1, O2, O3!
        lx = kx + (cx - ax) * (1.0 - t)
        ly = ky + (cy - ay) * (1.0 - t)
        s.line(kx, ky, lx, ly, stroke_width=3.6)

        ox = kx + (nx - bx) * (1.0 - t)
        oy = ky + (ny - by) * (1.0 - t)
        # Wait: O_i is on AN, and K_i -> O_i is parallel to BN!
        s.line(kx, ky, ox, oy, stroke_width=3.6)

    # Wavelet arcs centered at A, K1, K2, K3 tangent to BN!
    # Distance from point (kx, ky) to line BN:
    # Since A-N is perpendicular to B-N, dist(A, BN) = |AN| = hypot(nx - ax, ny - ay)
    r_a = math.hypot(nx - ax, ny - ay)
    ang_an = math.degrees(math.atan2(ny - ay, nx - ax))  # ~ -26.5 deg
    # Arc centered at A through N up to S
    s.arc(ax, ay, r_a, ang_an - 35.0, ang_an + 27.0, stroke_width=sw_thin, sweep=1)

    # Also extra upper-left arcs through N (S arcs in scan)
    for i in (1, 2, 3):
        t = i / 4.0
        kx = ax + (bx - ax) * t
        ky = ay
        rk = r_a * (1.0 - t)
        s.arc(kx, ky, rk, ang_an - 42.0, ang_an + 27.0, stroke_width=sw_thin, sweep=1)

    # Also tangent extension of BN upward-left to S
    ux_bn = (nx - bx) / math.hypot(nx - bx, ny - by)
    uy_bn = (ny - by) / math.hypot(nx - bx, ny - by)
    s.line(nx, ny, nx + ux_bn * 440.0, ny + uy_bn * 440.0, stroke_width=sw_thin)

    # Labels
    lib.label(s, 616.0, 48.0, "S", size=48.0, italic=False, bold=True)
    lib.label(s, 405.0, 362.0, "C", size=48.0, italic=False, bold=True)
    lib.label(s, 940.0, 388.0, "N", size=48.0, italic=False, bold=True)
    lib.label(s, 558.0, 434.0, "L", size=44.0, italic=False, bold=True)
    lib.label(s, 728.0, 444.0, "O", size=44.0, italic=False, bold=True)
    lib.label(s, 906.0, 514.0, "R", size=46.0, italic=False, bold=True)
    lib.label(s, 386.0, 476.0, "H", size=42.0, italic=False, bold=True)
    lib.label(s, 336.0, 558.0, "H", size=42.0, italic=False, bold=True)
    lib.label(s, 294.0, 646.0, "H", size=42.0, italic=False, bold=True)
    lib.label(s, 180.0, 782.0, "A", size=48.0, italic=False, bold=True)
    lib.label(s, 412.0, 782.0, "K", size=46.0, italic=False, bold=True)
    lib.label(s, 626.0, 782.0, "K", size=46.0, italic=False, bold=True)
    lib.label(s, 845.0, 782.0, "K", size=46.0, italic=False, bold=True)
    lib.label(s, 1122.0, 748.0, "B", size=48.0, italic=False, bold=True)
    lib.label(s, 1068.0, 848.0, "M", size=44.0, italic=False, bold=True)
    lib.label(s, 1030.0, 926.0, "M", size=44.0, italic=False, bold=True)
    lib.label(s, 984.0, 1012.0, "M", size=44.0, italic=False, bold=True)
    lib.label(s, 940.0, 1104.0, "G", size=48.0, italic=False, bold=True)

    s.save(out_svg)
