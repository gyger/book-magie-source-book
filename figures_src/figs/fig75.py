"""Figure 75: Michelson-Morley apparatus in plan view showing the 16 corner mirrors and folded light paths."""

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


def _trace_mask_svg_path(mask: np.ndarray, step: int = 2, eps: float = 0.8) -> str:
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

    # Outer square stone slab border drawn programmatically; internal mechanical mounts,
    # corner mirror assemblies, telescope, and folded beam paths vectorized cleanly
    yy, xx = np.ogrid[:h, :w]
    inner_mask = arr.copy()
    # Mask out ONLY the slightly-skewed scanned outer border lines tightly so we preserve:
    # - top-left label 'd_1' (sits right beside the left border at x>=90, y=155..245)
    # - the four 45-degree corner diagonal segments near each corner
    # - telescope 'f' crossing the bottom border
    x_left_line = 86.0 + 2.5 * (yy / 1450.0)
    x_right_line = 1495.5 + 4.5 * (yy / 1450.0)
    y_top_line = 28.5 + 3.0 * (xx / 1500.0)
    y_bot_line = 1450.0 + 7.5 * (xx / 1500.0)

    in_d1_box = (xx >= 90) & (xx <= 150) & (yy >= 155) & (yy <= 245)
    in_d_box = (xx >= 1435) & (xx <= 1494) & (yy >= 145) & (yy <= 235)

    on_outer_box = (
        ((np.abs(xx - x_left_line) < 5.5) & (yy >= 20) & (yy <= 1465) & ~in_d1_box)
        | ((np.abs(xx - x_right_line) < 6.0) & (yy >= 20) & (yy <= 1465) & ~in_d_box)
        | ((np.abs(yy - y_top_line) < 6.5) & (xx >= 78) & (xx <= 1508))
        | ((np.abs(yy - y_bot_line) < 8.0) & (xx >= 78) & (xx <= 1508))
    )
    inner_mask[on_outer_box] = False
    d_inner = _trace_mask_svg_path(inner_mask, step=2, eps=0.75)
    if d_inner:
        s.path(d_inner, fill="#000000", stroke="none", fill_rule="evenodd")

    # Crisp outer square stone slab aligned with the scanned border
    s.rect(88.0, 29.0, 1410.0, 1425.0, stroke_width=7.5)

    s.save(out_svg)
