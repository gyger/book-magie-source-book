"""Figure 53: Descartes's prism experiment producing the colors of the rainbow."""

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

    # --- 1. Vector-traced Sun woodcut (top-left) + shaded prism & screen (bottom-right) ---
    yy, xx = np.ogrid[:h, :w]
    in_sun = (xx < 395) & (yy < 395)
    in_prism_screen = (xx >= 425) & (yy >= 525) & (
        ((yy <= 835) & (xx <= 840))  # prism body
        | ((xx >= 795) & (yy >= 800))  # vertical black screen on right
    )
    woodcut = arr & (in_sun | in_prism_screen)
    d_wood = _trace_mask_svg_path(woodcut, step=2, eps=0.9)
    if d_wood:
        s.path(d_wood, fill="#000000", stroke="none", fill_rule="evenodd")

    # --- 2. Crisp optical rays from Sun through prism aperture DE to screen H, G, F ---
    # Incident rays from Sun rim to prism entry & aperture DE
    s.line(316.0, 304.0, 505.0, 775.0, stroke_width=sw)
    s.line(230.0, 372.0, 535.0, 775.0, stroke_width=sw)
    s.line(276.0, 342.0, 520.0, 775.0, stroke_width=5.0, dash="14,10")

    # Refracted rays from aperture DE (x~530..570, y~815) to screen (x~800)
    s.line(580.0, 815.0, 800.0, 965.0, stroke_width=sw)               # -> H
    s.line(550.0, 815.0, 800.0, 1022.0, stroke_width=5.5, dash="10,10")  # -> G (dotted)
    s.line(520.0, 815.0, 800.0, 1098.0, stroke_width=sw)              # -> F

    # Labels
    lib.label(s, 808.0, 504.0, "M", size=54.0, italic=False, bold=True)
    lib.label(s, 390.0, 815.0, "N", size=54.0, italic=False, bold=True)
    lib.label(s, 514.0, 864.0, "D", size=48.0, italic=False, bold=True)
    lib.label(s, 666.0, 864.0, "E", size=48.0, italic=False, bold=True)
    lib.label(s, 772.0, 864.0, "P", size=48.0, italic=False, bold=True)
    lib.label(s, 775.0, 950.0, "H", size=48.0, italic=False, bold=True)
    lib.label(s, 770.0, 1042.0, "G", size=48.0, italic=False, bold=True)
    lib.label(s, 772.0, 1104.0, "F", size=48.0, italic=False, bold=True)

    s.save(out_svg)
