"""Figure 70: Roemer's determination of the velocity of light from eclipses of Jupiter's first satellite."""

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


def _trace_mask_svg_path(mask: np.ndarray, step: int = 2, eps: float = 0.9) -> str:
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
    sw_thin = 4.5

    # Sun A center and Earth orbit circle
    ax, ay = 381.0, 1062.0
    r_earth = 355.0

    # Vector-trace only the classical Sun woodcut around A (radius < 110)
    yy, xx = np.ogrid[:h, :w]
    sun_mask = arr & (((xx - ax) ** 2 + (yy - ay) ** 2) < 110**2)
    d_sun = _trace_mask_svg_path(sun_mask, step=2, eps=0.8)
    if d_sun:
        s.path(d_sun, fill="#000000", stroke="none", fill_rule="evenodd")

    # Earth's orbit circle (E-F-G-H-L-K)
    s.circle(ax, ay, r_earth, stroke_width=sw)

    # Jupiter B and satellite orbit
    bx, by = 376.0, 238.0
    r_jup = 31.0
    r_sat = 117.0
    s.circle(bx, by, r_sat, stroke_width=sw)

    # Shadow cylinder/cone behind Jupiter B up to y = 34
    for dx_s in (-29.0, -18.0, -9.0, 0.0, 9.0, 18.0, 29.0):
        s.line(bx + dx_s, 34.0, bx + dx_s, by, stroke_width=3.5)

    # Jupiter disk (white fill to cover shadow lines inside disk)
    s.circle(bx, by, r_jup, fill="#ffffff", stroke="#000000", stroke_width=sw_thin)

    # Central vertical axis from B down through H, A to E
    s.line(bx, by + r_jup, ax, ay - 95.0, stroke_width=sw_thin)
    s.line(ax, ay + 95.0, ax, ay + r_earth, stroke_width=sw_thin)

    # Tangent rays from D (347, 124) -> L -> K (40, 1158) and C (405, 124) -> G -> F (726, 1158)
    s.line(347.0, 124.0, 40.0, 1158.0, stroke_width=sw_thin)
    s.line(405.0, 124.0, 726.0, 1158.0, stroke_width=sw_thin)

    # Labels
    lib.label(s, 304.0, 92.0, "D", size=44.0, italic=False, bold=True)
    lib.label(s, 434.0, 92.0, "C", size=44.0, italic=False, bold=True)
    lib.label(s, 405.0, 294.0, "B", size=44.0, italic=False, bold=True)
    lib.label(s, 412.0, 672.0, "H", size=44.0, italic=False, bold=True)
    lib.label(s, 114.0, 774.0, "L", size=44.0, italic=False, bold=True)
    lib.label(s, 636.0, 750.0, "G", size=44.0, italic=False, bold=True)
    lib.label(s, 508.0, 1058.0, "A", size=44.0, italic=False, bold=True)
    lib.label(s, 78.0, 1150.0, "K", size=44.0, italic=False, bold=True)
    lib.label(s, 754.0, 1166.0, "F", size=44.0, italic=False, bold=True)
    lib.label(s, 382.0, 1452.0, "E", size=44.0, italic=False, bold=True)

    s.save(out_svg)
