"""Figure 47: Descartes's total internal reflection / oblique impact on water surface."""

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

    sw = 8.5
    sw_thin = 6.0

    cx, cy, r = 958.0, 463.0, 386.0

    # --- 1. Vector-traced woodcut player + foliage + water bank ---
    yy, xx = np.ogrid[:h, :w]
    in_player = (xx < 580) & (((xx - cx) ** 2 + (yy - cy) ** 2) > (r + 12) ** 2)
    in_bank = (yy >= 445) & (yy <= 585) & (xx >= 420) & (xx <= w - 20)
    # Also bushes just inside left circle between y=340 and 460
    in_bush = (xx >= 565) & (xx <= 880) & (yy >= 340) & (yy <= 470) & (((xx - cx) ** 2 + (yy - cy) ** 2) < (r - 12) ** 2)
    ray_y = 140.0 + (474.0 - 140.0) * (xx - 165.0) / (958.0 - 165.0)
    on_ray = (xx > 340) & (np.abs(yy - ray_y) < 18)
    woodcut = arr & (in_player | in_bank | in_bush) & (~on_ray)
    d_wood = _trace_mask_svg_path(woodcut, step=2, eps=0.9)
    if d_wood:
        s.path(d_wood, fill="#000000", stroke="none", fill_rule="evenodd")

    # --- 2. Crisp geometric optical diagram ---
    s.circle(cx, cy, r, stroke_width=sw)
    # Vertical HBG
    s.line(cx, cy - r, cx, cy + r, stroke_width=sw)
    # Vertical F line outside circle on right
    s.line(1404.0, 276.0, 1404.0, 868.0, stroke_width=sw)

    # Incident ray from racket (165, 140) through A to B
    s.line(165.0, 140.0, cx, cy, stroke_width=sw_thin)
    # Dashed continuation B -> D
    s.line(cx, cy, 1312.0, 628.0, stroke_width=sw_thin, dash="14,12")
    # Reflected ray B -> L -> beyond
    s.line(cx, cy, 1388.0, 290.0, stroke_width=sw_thin)

    # Labels
    lib.label(s, 916.0, 140.0, "H", size=58.0, italic=False, bold=True)
    lib.label(s, 594.0, 250.0, "A", size=58.0, italic=False, bold=True)
    lib.label(s, 1338.0, 260.0, "L", size=58.0, italic=False, bold=True)
    lib.label(s, 1446.0, 315.0, "F", size=58.0, italic=False, bold=True)
    lib.label(s, 1344.0, 650.0, "D", size=58.0, italic=False, bold=True)
    lib.label(s, 922.0, 815.0, "G", size=58.0, italic=False, bold=True)

    s.save(out_svg)
