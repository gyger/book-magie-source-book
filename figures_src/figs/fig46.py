"""Figure 46: Descartes's refraction model — tennis player striking ball through cloth CBE into denser medium."""

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

    sw = 8.0
    sw_thin = 5.5

    cx, cy, r = 879.0, 646.0, 381.0

    # --- 1. Vector-traced woodcut player + foliage + cloth band ---
    yy, xx = np.ogrid[:h, :w]
    woodcut = arr.copy()
    # Keep player/foliage on left (x < 595, excluding circle & ray) + cloth band (638 <= y <= 738)
    in_player = (xx < 595) & (((xx - cx) ** 2 + (yy - cy) ** 2) > (r + 12) ** 2)
    in_bush = (xx >= 500) & (xx <= 670) & (yy >= 530) & (yy <= 642) & (((xx - cx) ** 2 + (yy - cy) ** 2) < (r - 12) ** 2)
    in_cloth = (yy >= 638) & (yy <= 738) & (xx >= 75) & (xx <= w - 15)
    # Exclude the original woodcut incident ray between player's shoulder and A
    wood_ray_y = 114.0 + (366.0 - 114.0) * (xx - 395.0) / (618.0 - 395.0)
    on_ray = (xx > 406) & (xx < 618) & (np.abs(yy - wood_ray_y) < 16)
    woodcut = arr & (in_player | in_bush | in_cloth) & (~on_ray)
    d_wood = _trace_mask_svg_path(woodcut, step=2, eps=0.9)
    if d_wood:
        s.path(d_wood, fill="#000000", stroke="none", fill_rule="evenodd")

    # --- 2. Crisp geometric optical diagram ---
    s.circle(cx, cy, r, stroke_width=sw)
    # Horizontal top of cloth CBE
    s.line(498.0, 646.0, w - 20.0, 646.0, stroke_width=sw_thin)
    # Vertical normal HBG
    s.line(cx, cy - r, cx, cy + r, stroke_width=sw)

    # Point A on upper-left circle
    ax, ay = 618.0, 372.0
    # Vertical FEI at x = 1228
    x_fe = 1228.5
    s.line(x_fe, 232.0, x_fe, h - 10.0, stroke_width=sw)

    # Horizontal AHF
    s.line(ax, ay, x_fe, ay, stroke_width=sw_thin)
    # Vertical AC
    s.line(ax, ay, ax, 646.0, stroke_width=sw_thin)

    # Incident ray from player's shoulder through A (618, 372) to B (879, 646)
    x_ray0 = 398.0
    y_ray0 = ay + (cy - ay) * (x_ray0 - ax) / (cx - ax)
    s.line(x_ray0, y_ray0, cx, cy, stroke_width=sw_thin)
    # Dashed straight continuation B -> D -> beyond
    s.line(cx, cy, 1345.0, 1152.0, stroke_width=sw_thin, dash="14,12")
    # Refracted ray B -> I -> beyond
    s.line(cx, cy, 1474.0, 902.0, stroke_width=sw_thin)

    # Labels
    lib.label(s, 616.0, 318.0, "A", size=58.0, italic=False, bold=True)
    lib.label(s, 845.0, 336.0, "H", size=58.0, italic=False, bold=True)
    lib.label(s, 1272.0, 355.0, "F", size=58.0, italic=False, bold=True)
    lib.label(s, 932.0, 608.0, "B", size=58.0, italic=False, bold=True)
    lib.label(s, 1188.0, 608.0, "E", size=58.0, italic=False, bold=True)
    lib.label(s, 1260.0, 855.0, "I", size=58.0, italic=False, bold=True)
    lib.label(s, 845.0, 980.0, "G", size=58.0, italic=False, bold=True)
    lib.label(s, 1126.0, 976.0, "D", size=58.0, italic=False, bold=True)

    s.save(out_svg)
