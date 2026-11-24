"""Figure 78: Gilbert's oblong lodestone (whole stone a-d and cut into two halves a-b, c-d)."""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image

import draw
import library as lib


def _cubic(p0: tuple[float, float], p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float], t: float) -> tuple[float, float]:
    u = 1.0 - t
    x = u**3 * p0[0] + 3 * u**2 * t * p1[0] + 3 * u * t**2 * p2[0] + t**3 * p3[0]
    y = u**3 * p0[1] + 3 * u**2 * t * p1[1] + 3 * u * t**2 * p2[1] + t**3 * p3[1]
    return x, y


def _cubic_tan(p0: tuple[float, float], p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float], t: float) -> tuple[float, float]:
    u = 1.0 - t
    dx = 3 * u**2 * (p1[0] - p0[0]) + 6 * u * t * (p2[0] - p1[0]) + 3 * t**2 * (p3[0] - p2[0])
    dy = 3 * u**2 * (p1[1] - p0[1]) + 6 * u * t * (p2[1] - p1[1]) + 3 * t**2 * (p3[1] - p2[1])
    return dx, dy


def _hatch_ellipse_rim(
    s: draw.Scene,
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    deg_start: float,
    deg_end: float,
    arc_step: float,
    depth_in: float,
    sw: float = 2.6,
) -> None:
    """Draw dense woodcut-style contour hatching with uniform arc-length spacing."""
    rad = math.radians(deg_start)
    rad_end = math.radians(deg_end)
    while rad <= rad_end + 1e-6:
        ca, sa = math.cos(rad), math.sin(rad)
        x_out = cx + rx * ca
        y_out = cy + ry * sa
        # Deeper shading on underside (sa > 0) and poles (|ca| large), lighter on top
        frac = depth_in * (0.48 + 0.62 * max(0.0, sa) + 0.16 * (ca * ca))
        # Subtle woodcut length modulation
        frac *= 0.92 + 0.08 * math.sin(rad * 19.0)
        x_in = cx + rx * (1.0 - frac) * ca
        y_in = cy + ry * (1.0 - frac) * sa
        s.line(x_out, y_out, x_in, y_in, stroke_width=sw)

        # Short denser secondary shading strokes along the darker lower rim & poles
        if sa > 0.15 or abs(ca) > 0.72:
            ds_cur = math.hypot(-rx * sa, ry * ca)
            rad_mid = rad + 0.5 * arc_step / max(ds_cur, 1.0)
            if rad_mid <= rad_end:
                cm, sm = math.cos(rad_mid), math.sin(rad_mid)
                f2 = depth_in * (0.28 + 0.34 * max(0.0, sm) + 0.14 * (cm * cm))
                s.line(
                    cx + rx * cm,
                    cy + ry * sm,
                    cx + rx * (1.0 - f2) * cm,
                    cy + ry * (1.0 - f2) * sm,
                    stroke_width=sw * 0.85,
                )

        ds = math.hypot(-rx * sa, ry * ca)
        rad += arc_step / max(ds, 1.0)


def _hatch_bezier_contour(
    s: draw.Scene,
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    inward_sign: float,
    arc_step: float,
    depth_fn,
    sw: float = 2.6,
    dense_rim: bool = False,
) -> None:
    """Hatch inward along a cubic Bezier contour at uniform arc-length spacing."""
    # Sample curve finely to step by uniform arc length
    n_samples = 400
    pts = [_cubic(p0, p1, p2, p3, i / n_samples) for i in range(n_samples + 1)]
    cum = [0.0]
    for i in range(1, len(pts)):
        cum.append(cum[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
    total = cum[-1]
    dist = arc_step * 0.5
    idx = 0
    while dist < total - arc_step * 0.3:
        while idx < n_samples - 1 and cum[idx + 1] < dist:
            idx += 1
        seg = cum[idx + 1] - cum[idx]
        frac = (dist - cum[idx]) / seg if seg > 1e-9 else 0.0
        t = (idx + frac) / n_samples
        x, y = _cubic(p0, p1, p2, p3, t)
        tx, ty = _cubic_tan(p0, p1, p2, p3, t)
        tn = math.hypot(tx, ty)
        if tn > 1e-6:
            # Normal pointing inward
            nx = -ty / tn * inward_sign
            ny = tx / tn * inward_sign
            # Slight woodcut slant toward the cut/vertical
            d_len = depth_fn(t)
            s.line(x, y, x + nx * d_len, y + ny * d_len, stroke_width=sw)
            if dense_rim:
                # Extra shorter stroke halfway to next tick for richer dark rim
                t2 = min(1.0, t + 0.5 * (arc_step / max(total, 1.0)))
                x2, y2 = _cubic(p0, p1, p2, p3, t2)
                tx2, ty2 = _cubic_tan(p0, p1, p2, p3, t2)
                tn2 = math.hypot(tx2, ty2)
                if tn2 > 1e-6:
                    nx2 = -ty2 / tn2 * inward_sign
                    ny2 = tx2 / tn2 * inward_sign
                    d2 = depth_fn(t2) * 0.55
                    s.line(x2, y2, x2 + nx2 * d2, y2 + ny2 * d2, stroke_width=sw * 0.85)
        dist += arc_step


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.5
    # === Top: whole oblong lodestone a-d ===
    cx1, cy1, rx1, ry1 = 739.0, 255.0, 629.0, 239.0
    s.ellipse(cx1, cy1, rx1, ry1, fill="#ffffff", stroke_width=sw)
    _hatch_ellipse_rim(s, cx1, cy1, rx1, ry1, 0.0, 359.5, arc_step=12.0, depth_in=0.25, sw=2.6)

    # === Bottom-left half: a-b ===
    # Top contour from tip (62, 912) to top-cut (672, 691)
    bl_top = ((62.0, 912.0), (62.0, 765.0), (310.0, 691.0), (672.0, 691.0))
    # Bottom contour from tip (62, 912) to bottom-cut (672, 1122) — full rounded lower curve matching scan
    bl_bot = ((62.0, 912.0), (62.0, 1082.0), (225.0, 1124.0), (672.0, 1122.0))
    d_left = (
        f"M {bl_top[0][0]:.1f} {bl_top[0][1]:.1f} "
        f"C {bl_top[1][0]:.1f} {bl_top[1][1]:.1f}, {bl_top[2][0]:.1f} {bl_top[2][1]:.1f}, {bl_top[3][0]:.1f} {bl_top[3][1]:.1f} "
        f"Q 782.0 908.0, {bl_bot[3][0]:.1f} {bl_bot[3][1]:.1f} "
        f"C {bl_bot[2][0]:.1f} {bl_bot[2][1]:.1f}, {bl_bot[1][0]:.1f} {bl_bot[1][1]:.1f}, {bl_bot[0][0]:.1f} {bl_bot[0][1]:.1f} Z"
    )
    s.path(d_left, fill="#ffffff", stroke_width=sw)
    # Dense hatching along top and bottom contours of bottom-left half
    _hatch_bezier_contour(
        s, *bl_top, inward_sign=1.0, arc_step=12.0,
        depth_fn=lambda t: 54.0 + 46.0 * t + 14.0 * (1.0 - t), sw=2.5, dense_rim=False,
    )
    _hatch_bezier_contour(
        s, *bl_bot, inward_sign=-1.0, arc_step=12.0,
        depth_fn=lambda t: 62.0 + 52.0 * t, sw=2.5, dense_rim=True,
    )

    # === Bottom-right half: c-d ===
    # Cut face center at x=852, rx=28, y=691..1122
    br_top = ((852.0, 691.0), (1185.0, 691.0), (1482.0, 765.0), (1482.0, 912.0))
    br_bot = ((852.0, 1122.0), (1255.0, 1124.0), (1482.0, 1082.0), (1482.0, 912.0))
    d_right = (
        f"M {br_top[0][0]:.1f} {br_top[0][1]:.1f} "
        f"C {br_top[1][0]:.1f} {br_top[1][1]:.1f}, {br_top[2][0]:.1f} {br_top[2][1]:.1f}, {br_top[3][0]:.1f} {br_top[3][1]:.1f} "
        f"C {br_bot[2][0]:.1f} {br_bot[2][1]:.1f}, {br_bot[1][0]:.1f} {br_bot[1][1]:.1f}, {br_bot[0][0]:.1f} {br_bot[0][1]:.1f} Z"
    )
    s.path(d_right, fill="#ffffff", stroke_width=sw)
    _hatch_bezier_contour(
        s, *br_top, inward_sign=1.0, arc_step=12.0,
        depth_fn=lambda t: 95.0 - 38.0 * t, sw=2.5, dense_rim=False,
    )
    _hatch_bezier_contour(
        s, *br_bot, inward_sign=-1.0, arc_step=12.0,
        depth_fn=lambda t: 108.0 - 44.0 * t, sw=2.5, dense_rim=True,
    )

    # Elliptical cut cross-section face on left of right half
    cx_cut, cy_cut, rx_cut, ry_cut = 852.0, 906.5, 28.0, 215.5
    s.ellipse(cx_cut, cy_cut, rx_cut, ry_cut, fill="#ffffff", stroke_width=sw * 0.9)
    # Diagonal shading inside the cut face
    for y in range(int(cy_cut - ry_cut + 20), int(cy_cut + ry_cut - 16), 16):
        dy = (y - cy_cut) / ry_cut
        hw = (rx_cut - 2.0) * max(0.0, 1.0 - dy * dy) ** 0.5
        s.line(cx_cut - hw, y + 9.0, cx_cut + hw, y - 9.0, stroke_width=2.8)

    # Labels
    lib.label(s, 78.0, 254.0, "a", size=74.0, italic=True, bold=True)
    lib.label(s, 1404.0, 248.0, "d", size=74.0, italic=True, bold=True)
    lib.label(s, 22.0, 912.0, "a", size=68.0, italic=True, bold=True)
    lib.label(s, 682.0, 912.0, "b", size=66.0, italic=True, bold=True)
    lib.label(s, 910.0, 912.0, "c", size=68.0, italic=True, bold=True)

    s.save(out_svg)
