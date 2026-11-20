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


def build(src_png: Path, out_svg: Path) -> None:
    im = Image.open(src_png).convert("L")
    w, h = im.size
    arr = np.asarray(im) < 180
    s = draw.Scene(w, h)

    sw = 5.5
    sw_thin = 4.0

    # Raindrop circle
    cx, cy, r = 996.0, 358.0, 124.0

    # --- 1. Vector-traced stippled rain cloud, rainbow arcs, observer & ground ---
    yy, xx = np.ogrid[:h, :w]
    woodcut = arr.copy()
    # Exclude the left region above ground where only A, F, E rays & labels live
    left_open = (xx < 520) & (yy < 1140)
    # Exclude neighborhood of circle rim
    dist_c = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    near_c = np.abs(dist_c - r) < 8
    woodcut[left_open | near_c] = False
    d_wood = _trace_mask_svg_path(woodcut, step=2, eps=1.1)
    if d_wood:
        s.path(d_wood, fill="#000000", stroke="none", fill_rule="evenodd")

    # --- 2. Crisp geometric optical rays & raindrop circle ---
    s.circle(cx, cy, r, stroke_width=sw)

    # Primary rainbow ray A -> B -> C -> D -> E
    ax, ay = 196.0, 166.0
    bx, by = 955.0, 246.0
    cx_pt, cy_pt = 1117.0, 332.0
    dx_pt, dy_pt = 1020.0, 492.0
    ex, ey = 136.0, 1138.0
    s.line(ax, ay, bx, by, stroke_width=sw_thin)
    s.line(bx, by, cx_pt, cy_pt, stroke_width=sw_thin)
    s.line(cx_pt, cy_pt, dx_pt, dy_pt, stroke_width=sw_thin)
    s.line(dx_pt, dy_pt, ex, ey, stroke_width=sw_thin)

    # Secondary rainbow dotted ray F -> G -> H -> I -> K -> E
    fx, fy = 186.0, 390.0
    gx, gy = 936.0, 479.0
    hx, hy = 1114.0, 396.0
    ix, iy = 1004.0, 242.0
    kx, ky = 886.0, 318.0
    s.line(fx, fy, gx, gy, stroke_width=3.5, dash="8,8")
    s.line(gx, gy, hx, hy, stroke_width=3.5, dash="8,8")
    s.line(hx, hy, ix, iy, stroke_width=3.5, dash="8,8")
    s.line(ix, iy, kx, ky, stroke_width=3.5, dash="8,8")
    s.line(kx, ky, ex, ey, stroke_width=3.5, dash="8,8")

    # Horizon reference ray E -> M
    s.line(18.0, 1126.0, 916.0, 1236.0, stroke_width=sw_thin)

    # Labels
    lib.label(s, 176.0, 206.0, "A", size=52.0, italic=False, bold=True)
    lib.label(s, 152.0, 420.0, "F", size=52.0, italic=False, bold=True)
    lib.label(s, 102.0, 1112.0, "E", size=52.0, italic=False, bold=True)
    lib.label(s, 948.0, 1205.0, "M", size=48.0, italic=False, bold=True)

    s.save(out_svg)
