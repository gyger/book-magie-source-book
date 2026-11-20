"""Figure 50: Descartes's comparison of ball vs. light ray refraction at water surface CBE."""

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

    sw = 6.5
    sw_thin = 4.5

    cx, cy, r = 652.0, 407.0, 375.0

    # --- 1. Vector-traced water ripple texture below surface (excluding circle, rays, labels) ---
    yy, xx = np.ogrid[:h, :w]
    in_water = (yy >= 412) & (yy <= 605) & (xx >= 32) & (xx <= w - 30)
    # Exclude neighborhood of circle rim, vertical line, and rays
    dist_c = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    near_circle = np.abs(dist_c - r) < 10
    near_vert = np.abs(xx - cx) < 10
    # Exclude label V region
    near_v = (xx >= 995) & (xx <= 1065) & (yy >= 515) & (yy <= 590)
    water_mask = arr & in_water & (~near_circle) & (~near_vert) & (~near_v)
    d_water = _trace_mask_svg_path(water_mask, step=2, eps=1.0)
    if d_water:
        s.path(d_water, fill="#000000", stroke="none", fill_rule="evenodd")

    # --- 2. Crisp geometric optical diagram ---
    s.circle(cx, cy, r, stroke_width=sw)
    # Horizontal surface CBE
    s.line(32.0, cy, w - 30.0, cy, stroke_width=sw)
    # Vertical normal through B
    s.line(cx, cy - r, cx, cy + r, stroke_width=sw_thin)

    # Incident ray AB (A on upper-left circle)
    ax, ay = 387.0, 142.0
    s.line(ax, ay, cx, cy, stroke_width=sw_thin)

    # Dashed straight continuation B -> D (lower-right circle)
    dx, dy = 918.0, 672.0
    s.line(cx, cy, dx, dy, stroke_width=sw_thin, dash="20,16")

    # Refracted light ray B -> I (toward normal)
    ix, iy = 839.0, 732.0
    s.line(cx, cy, ix, iy, stroke_width=sw_thin)

    # Deflected ball path B -> V (away from normal)
    vx, vy = 995.0, 560.0
    s.line(cx, cy, vx, vy, stroke_width=sw_thin)

    # Labels
    lib.label(s, 355.0, 118.0, "A", size=58.0, italic=False, bold=True)
    lib.label(s, 240.0, 372.0, "C", size=58.0, italic=False, bold=True)
    lib.label(s, 682.0, 374.0, "B", size=58.0, italic=False, bold=True)
    lib.label(s, 1052.0, 372.0, "E", size=58.0, italic=False, bold=True)
    lib.label(s, 1028.0, 562.0, "V", size=58.0, italic=False, bold=True)
    lib.label(s, 954.0, 694.0, "D", size=58.0, italic=False, bold=True)
    lib.label(s, 855.0, 758.0, "I", size=58.0, italic=False, bold=True)

    s.save(out_svg)
