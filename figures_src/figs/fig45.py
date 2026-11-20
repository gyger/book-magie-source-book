"""Figure 45: Descartes's law of reflection — tennis player striking ball from A to B and reflected to F."""

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
    """Vectorize a boolean mask into simplified closed SVG subpaths (evenodd)."""
    m = mask[::step, ::step]
    h, w = m.shape
    p = np.zeros((h + 2, w + 2), dtype=np.uint8)
    p[1:-1, 1:-1] = m.astype(np.uint8)
    # Collect boundary directed edges on pixel grid (around True cells, CCW/CW consistent)
    # Edges are between grid vertices (x, y) in [0..w+1] x [0..h+1]
    edges: dict[tuple[int, int], list[tuple[int, int]]] = {}
    # Horizontal edges where p[y, x] != p[y+1, x]
    # Vertical edges where p[y, x] != p[y, x+1]
    ys, xs = np.where(p[:-1, :] != p[1:, :])
    for y, x in zip(ys.tolist(), xs.tolist()):
        if p[y + 1, x]:  # True below -> edge goes left-to-right along y+1
            u, v = (x, y + 1), (x + 1, y + 1)
        else:  # True above -> edge goes right-to-left along y+1
            u, v = (x + 1, y + 1), (x, y + 1)
        edges.setdefault(u, []).append(v)
    ys, xs = np.where(p[:, :-1] != p[:, 1:])
    for y, x in zip(ys.tolist(), xs.tolist()):
        if p[y, x + 1]:  # True on right -> edge goes bottom-to-top along x+1
            u, v = (x + 1, y + 1), (x + 1, y)
        else:  # True on left -> edge goes top-to-bottom along x+1
            u, v = (x + 1, y), (x + 1, y + 1)
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
        # Convert to original coords (offset by -1 for padding)
        pts = [((vx - 1) * step, (vy - 1) * step) for vx, vy in loop[:-1]]
        simp = _dp(pts + [pts[0]], eps * step)[:-1]
        if len(simp) < 3:
            continue
        d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in simp) + " Z"
        parts.append(d)
    return " ".join(parts)


def build(src_png: Path, out_svg: Path) -> None:
    im = Image.open(src_png).convert("L")
    w, h = im.size
    arr = np.asarray(im) < 180
    s = draw.Scene(w, h)

    sw = 6.5
    sw_thin = 4.2

    # --- 1. Vector-traced historical woodcut tennis player & ground (left region) ---
    yy, xx = np.ogrid[:h, :w]
    # Keep player + ground, excluding the incident ray above x=255 and circle on right
    cx, cy, r = 835.0, 624.5, 381.0
    woodcut_mask = arr.copy()
    # Mask out circle & everything right of x=465 (except ground below y=530 up to x=518)
    in_diagram = (xx > 455) & ~((xx <= 525) & (yy >= 530) & (yy <= 655))
    # Also mask out the straight ray from racket (240, 105) to A (548, 372) for x > 260
    ray_y = 105.0 + (372.0 - 105.0) * (xx - 240.0) / (548.0 - 240.0)
    on_ray = (xx > 265) & (np.abs(yy - ray_y) < 16)
    woodcut_mask[in_diagram | on_ray] = False
    d_wood = _trace_mask_svg_path(woodcut_mask, step=2, eps=0.9)
    if d_wood:
        s.path(d_wood, fill="#000000", stroke="none", fill_rule="evenodd")

    # --- 2. Crisp geometric optical diagram ---
    # Circle centered at B
    s.circle(cx, cy, r, stroke_width=sw)

    # Horizontal ground/surface CBE (slight natural slope: left 627 -> right 618)
    s.line(454.0, 626.0, w - 5.0, 619.0, stroke_width=sw_thin)

    # Vertical normal through B (from top y=52 down to B)
    s.line(cx, 52.0, cx, cy, stroke_width=sw)

    # Key points on circle: A (upper-left), F (upper-right), D (lower-right)
    ax, ay = 548.0, 373.0
    fx, fy = 1117.0, 373.0
    dx, dy = 1117.5, 878.0

    # Incident ray from racket (226, 93) through A to B
    s.line(226.0, 93.0, cx, cy, stroke_width=sw_thin)
    # Reflected ray from B through F to (1302, 211)
    s.line(cx, cy, 1302.0, 211.0, stroke_width=sw_thin)

    # Verticals AC and FED
    s.line(ax, ay, ax, 625.0, stroke_width=sw_thin)
    s.line(fx, fy, dx, dy, stroke_width=sw_thin)

    # Horizontal hatched/ticked line AHF (series of short vertical strokes like original woodcut)
    n_ticks = 64
    for i in range(1, n_ticks):
        t = i / n_ticks
        tx = ax + (fx - ax) * t
        s.line(tx, ay - 7.0, tx, ay + 7.0, stroke_width=3.2)

    # Dotted/ticked line BD
    n_bd = 44
    for i in range(1, n_bd):
        t = i / n_bd
        tx = cx + (dx - cx) * t
        ty = cy + (dy - cy) * t
        s.line(tx - 5.0, ty + 6.0, tx + 5.0, ty - 6.0, stroke_width=3.2)

    # Labels
    lib.label(s, 548.0, 326.0, "A", size=58.0, italic=False, bold=True)
    lib.label(s, 868.0, 342.0, "H", size=58.0, italic=False, bold=True)
    lib.label(s, 1122.0, 324.0, "F", size=58.0, italic=False, bold=True)
    lib.label(s, 544.0, 662.0, "C", size=58.0, italic=False, bold=True)
    lib.label(s, 813.0, 654.0, "B", size=58.0, italic=False, bold=True)
    lib.label(s, 1144.0, 655.0, "E", size=58.0, italic=False, bold=True)
    lib.label(s, 1142.0, 910.0, "D", size=58.0, italic=False, bold=True)

    s.save(out_svg)
