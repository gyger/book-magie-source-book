"""Figure 51: Descartes's refraction of rays from candle flame A through curved glass sphere BCD."""

from __future__ import annotations

import math
from pathlib import Path
import numpy as np
from PIL import Image

import draw
import library as lib


def _dp(pts: list[tuple[float, float]], eps: float) -> list[tuple[float, float]]:
    if len(pts) <= 3:
        return pts
    stack = [(0, len(pts) - 1)]
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    while stack:
        i0, i1 = stack.pop()
        if i1 <= i0 + 1:
            continue
        x0, y0 = pts[i0]
        x1, y1 = pts[i1]
        dx, dy = x1 - x0, y1 - y0
        den = math.hypot(dx, dy)
        best_d, best_i = -1.0, -1
        for i in range(i0 + 1, i1):
            px, py = pts[i]
            d = math.hypot(px - x0, py - y0) if den < 1e-9 else abs(dy * px - dx * py + x1 * y0 - y1 * x0) / den
            if d > best_d:
                best_d, best_i = d, i
        if best_d > eps:
            keep[best_i] = True
            stack.append((i0, best_i))
            stack.append((best_i, i1))
    return [p for p, k in zip(pts, keep) if k]


def _trace_mask_svg_path(mask: np.ndarray, step: int = 2, eps: float = 1.0) -> str:
    m = mask[::step, ::step]
    h, w = m.shape
    p = np.zeros((h + 2, w + 2), dtype=np.uint8)
    p[1:-1, 1:-1] = m.astype(np.uint8)
    edges: dict[tuple[int, int], list[tuple[int, int]]] = {}
    ys, xs = np.where(p[:-1, :] != p[1:, :])
    for y, x in zip(ys.tolist(), xs.tolist()):
        u, v = ((x, y + 1), (x + 1, y + 1)) if p[y + 1, x] else ((x + 1, y + 1), (x, y + 1))
        edges.setdefault(u, []).append(v)
    ys, xs = np.where(p[:, :-1] != p[:, 1:])
    for y, x in zip(ys.tolist(), xs.tolist()):
        u, v = ((x + 1, y + 1), (x + 1, y)) if p[y, x + 1] else ((x + 1, y), (x + 1, y + 1))
        edges.setdefault(u, []).append(v)
    parts: list[str] = []
    while edges:
        start = next(iter(edges))
        nxt = edges[start].pop()
        if not edges[start]:
            del edges[start]
        loop = [start, nxt]
        cur = nxt
        while cur != start and cur in edges:
            nv = edges[cur].pop()
            if not edges[cur]:
                del edges[cur]
            loop.append(nv)
            cur = nv
        if len(loop) < 5:
            continue
        pts = [((vx - 1) * step, (vy - 1) * step) for vx, vy in loop[:-1]]
        simp = _dp(pts + [pts[0]], eps * step)[:-1]
        if len(simp) < 3:
            continue
        parts.append("M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in simp) + " Z")
    return " ".join(parts)


def _near_seg(
    xx: np.ndarray,
    yy: np.ndarray,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    tol: float,
) -> np.ndarray:
    dx, dy = x2 - x1, y2 - y1
    l2 = dx * dx + dy * dy
    if l2 < 1e-9:
        return (xx - x1) ** 2 + (yy - y1) ** 2 <= tol * tol
    t = np.clip(((xx - x1) * dx + (yy - y1) * dy) / l2, 0.0, 1.0)
    px = x1 + t * dx
    py = y1 + t * dy
    return (xx - px) ** 2 + (yy - py) ** 2 <= tol * tol


def build(src_png: Path, out_svg: Path) -> None:
    im = Image.open(src_png).convert("L")
    w, h = im.size
    arr = np.asarray(im) < 180
    s = draw.Scene(w, h)

    sw = 7.0
    sw_thin = 4.6

    # Glass sphere matching original scan rim
    cx, cy, r = 1091.0, 435.5, 338.0

    # Key optical coordinates fitted to original scan
    ax, ay = 138.0, 436.0
    dx_pt, dy_pt = 901.0, 163.0
    ux_out, uy_out = 1393.0, 286.0
    bx_pt, by_pt = 859.0, 679.5
    lx_out, ly_out = 1397.0, 591.0

    # --- 1. Vector-traced candlestick (left) + table base (bottom) + sphere woodcut shading ---
    yy, xx = np.ogrid[:h, :w]
    in_candle = (
        ((xx >= 55) & (xx <= 198) & (yy >= 468) & (yy <= 770))
        | ((xx >= 90) & (xx <= 143) & (yy >= 375) & (yy < 468))
    )
    in_table = (yy >= 762) & (yy <= h - 1)
    # Inner shading strokes of glass sphere (strictly inside sphere, excluding internal rays & raster 'B')
    dist_c = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    in_sphere_shade = dist_c < (r - 12)
    in_sphere_shade &= ~_near_seg(xx, yy, dx_pt, dy_pt, ux_out, uy_out, 11.0)
    in_sphere_shade &= ~_near_seg(xx, yy, cx - r, ay, cx + r, ay, 11.0)
    in_sphere_shade &= ~_near_seg(xx, yy, bx_pt, by_pt, lx_out, ly_out, 11.0)
    in_sphere_shade &= ~((xx >= 842) & (xx <= 895) & (yy >= 594) & (yy <= 654))

    woodcut = arr & (in_candle | in_table | in_sphere_shade)
    d_wood = _trace_mask_svg_path(woodcut, step=2, eps=0.9)
    if d_wood:
        s.path(d_wood, fill="#000000", stroke="none", fill_rule="evenodd")

    # --- 2. Crisp geometric optical diagram ---
    s.circle(cx, cy, r, stroke_width=sw)

    # Upper ray A -> D on sphere -> refracted through sphere -> exit
    s.line(ax, ay, dx_pt, dy_pt, stroke_width=sw_thin)
    s.line(dx_pt, dy_pt, ux_out, uy_out, stroke_width=sw_thin)
    s.line(ux_out, uy_out, w - 2.0, 386.0, stroke_width=sw_thin)

    # Central horizontal ray A -> C -> straight through sphere
    s.line(ax, ay, w - 2.0, ay, stroke_width=sw_thin)

    # Lower ray A -> B on sphere -> refracted through sphere -> exit
    s.line(ax, ay, bx_pt, by_pt, stroke_width=sw_thin)
    s.line(bx_pt, by_pt, lx_out, ly_out, stroke_width=sw_thin)
    s.line(lx_out, ly_out, w - 2.0, 526.0, stroke_width=sw_thin)

    # Tangent lines at D (K-D-I), C (G-C-H), and B (E-B-F)
    s.line(744.0, 274.0, 1012.0, 66.0, stroke_width=sw_thin)   # K-D-I
    s.line(751.0, 332.0, 748.0, 546.0, stroke_width=sw_thin)   # G-C-H
    s.line(744.0, 580.0, 936.0, 760.0, stroke_width=sw_thin)   # E-B-F

    # Labels
    lib.label(s, 70.0, 459.0, "A", size=54.0, italic=False, bold=True)
    lib.label(s, 958.0, 52.0, "I", size=50.0, italic=False, bold=True)
    lib.label(s, 851.0, 129.0, "D", size=50.0, italic=False, bold=True)
    lib.label(s, 712.0, 280.0, "K", size=50.0, italic=False, bold=True)
    lib.label(s, 714.0, 365.0, "G", size=50.0, italic=False, bold=True)
    lib.label(s, 711.0, 466.0, "C", size=50.0, italic=False, bold=True)
    lib.label(s, 714.0, 519.0, "H", size=50.0, italic=False, bold=True)
    lib.label(s, 721.0, 583.0, "E", size=50.0, italic=False, bold=True)
    lib.label(s, 868.0, 624.0, "B", size=50.0, italic=False, bold=True)
    lib.label(s, 842.0, 734.0, "F", size=50.0, italic=False, bold=True)

    s.save(out_svg)
