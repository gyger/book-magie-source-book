"""Figure 52: Descartes's explanation of the primary and secondary rainbows."""

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

    sw = 5.5
    sw_thin = 4.5

    # Raindrop circle fitted to original scan
    cx, cy, r = 1008.5, 356.5, 124.5

    # Primary rainbow ray A -> B -> C -> D -> E
    ax, ay = 196.0, 165.0
    bx, by = 974.0, 237.0
    cx_pt, cy_pt = 1130.0, 332.0
    dx_pt, dy_pt = 1035.0, 478.0
    ex, ey = 135.0, 1122.0

    # Secondary rainbow dotted ray F -> G -> H -> I -> K -> E
    fx, fy = 146.0, 383.0
    gx, gy = 938.0, 460.0
    hx, hy = 1125.0, 400.0
    ix, iy = 1015.0, 232.0
    kx, ky = 886.0, 336.0

    # Horizon reference ray E -> M
    em_x0, em_y0 = 0.0, 1119.5
    em_x1, em_y1 = 934.0, 1215.0

    # --- 1. Vector-traced stippled rain cloud, rainbow arcs, observer & ground ---
    yy, xx = np.ogrid[:h, :w]
    woodcut = arr.copy()
    # Exclude the left region above observer/ground where only A, F, E rays & labels live
    left_open = (xx < 520) & (yy < 1125)
    # Exclude neighborhood of circle rim
    dist_c = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    near_c = np.abs(dist_c - r) < 9.0
    # Exclude all raster ray segments so vector rays don't double them
    near_rays = (
        _near_seg(xx, yy, ax, ay, bx, by, 8.0)
        | _near_seg(xx, yy, bx, by, cx_pt, cy_pt, 7.0)
        | _near_seg(xx, yy, cx_pt, cy_pt, dx_pt, dy_pt, 7.0)
        | _near_seg(xx, yy, dx_pt, dy_pt, ex, ey, 8.0)
        | _near_seg(xx, yy, fx, fy, gx, gy, 7.5)
        | _near_seg(xx, yy, gx, gy, hx, hy, 6.5)
        | _near_seg(xx, yy, hx, hy, ix, iy, 6.5)
        | _near_seg(xx, yy, ix, iy, kx, ky, 6.5)
        | _near_seg(xx, yy, kx, ky, ex, ey, 7.5)
        | (_near_seg(xx, yy, em_x0, em_y0, em_x1, em_y1, 8.5) & ((xx < 80) | (xx > 160)))
    )
    # Exclude raster label 'M' so vector 'M' doesn't duplicate it
    label_m = (xx >= 936) & (xx <= 1002) & (yy >= 1166) & (yy <= 1222)

    woodcut[left_open | near_c | near_rays | label_m] = False
    d_wood = _trace_mask_svg_path(woodcut, step=2, eps=1.1)
    if d_wood:
        s.path(d_wood, fill="#000000", stroke="none", fill_rule="evenodd")

    # --- 2. Crisp geometric optical rays & raindrop circle ---
    s.circle(cx, cy, r, stroke_width=sw)

    # Primary rainbow ray A -> B -> C -> D -> E
    s.line(ax, ay, bx, by, stroke_width=sw_thin)
    s.line(bx, by, cx_pt, cy_pt, stroke_width=sw_thin)
    s.line(cx_pt, cy_pt, dx_pt, dy_pt, stroke_width=sw_thin)
    s.line(dx_pt, dy_pt, ex, ey, stroke_width=sw_thin)

    # Secondary rainbow dotted ray F -> G -> H -> I -> K -> E
    s.line(fx, fy, gx, gy, stroke_width=3.8, dash="6,6")
    s.line(gx, gy, hx, hy, stroke_width=3.8, dash="6,6")
    s.line(hx, hy, ix, iy, stroke_width=3.8, dash="6,6")
    s.line(ix, iy, kx, ky, stroke_width=3.8, dash="6,6")
    s.line(kx, ky, ex, ey, stroke_width=3.8, dash="6,6")

    # Horizon reference ray E -> M
    s.line(em_x0, em_y0, em_x1, em_y1, stroke_width=sw_thin)

    # Labels
    lib.label(s, 185.0, 203.0, "A", size=52.0, italic=False, bold=True)
    lib.label(s, 161.0, 410.0, "F", size=52.0, italic=False, bold=True)
    lib.label(s, 101.0, 1102.0, "E", size=52.0, italic=False, bold=True)
    lib.label(s, 968.0, 1192.0, "M", size=48.0, italic=False, bold=True)

    s.save(out_svg)
