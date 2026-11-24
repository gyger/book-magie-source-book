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
    # Elliptical sun mask so no thick raster ray stubs protrude outside the sun corona
    in_sun = ((xx - 200.5) / 168.0) ** 2 + ((yy - 225.5) / 163.0) ** 2 <= 1.0
    # Prism triangle bounded strictly below/right of its hypotenuse (excludes ray crossing above prism)
    in_prism = (
        (yy >= 530)
        & (yy <= 836)
        & (xx >= 425)
        & (xx <= 835)
        & (xx >= 824.0 - 1.44 * (yy - 533.0) - 6.0)
    )
    in_screen = (xx >= 798) & (yy >= 800)
    woodcut = arr & (in_sun | in_prism | in_screen)
    d_wood = _trace_mask_svg_path(woodcut, step=2, eps=0.9)
    if d_wood:
        s.path(d_wood, fill="#000000", stroke="none", fill_rule="evenodd")

    # --- 2. Crisp optical rays from Sun through prism aperture DE to screen H, G, F ---
    # Incident rays from Sun rim crossing above prism to prism entry face
    s.line(329.0, 310.0, 504.0, 765.0, stroke_width=sw)                 # right -> left
    s.line(222.0, 370.0, 534.0, 755.0, stroke_width=sw)                 # left -> right
    s.line(288.0, 350.0, 514.0, 765.0, stroke_width=5.2, dash="12,10")  # middle dashed

    # Refracted rays from aperture DE (y~820) to screen (x~804)
    s.line(596.0, 820.0, 804.0, 965.0, stroke_width=sw)                 # -> H
    s.line(566.0, 820.0, 804.0, 1048.0, stroke_width=5.5, dash="10,10") # -> G (dotted)
    s.line(544.0, 820.0, 804.0, 1125.0, stroke_width=sw)                # -> F

    # Small white halos behind labels adjacent to refracted rays so rays don't cut through text
    s.rect(638.0, 838.0, 52.0, 52.0, fill="#ffffff", stroke="none")  # behind E
    s.rect(750.0, 922.0, 50.0, 54.0, fill="#ffffff", stroke="none")  # behind H
    s.rect(746.0, 1022.0, 50.0, 48.0, fill="#ffffff", stroke="none") # behind G
    s.rect(752.0, 1078.0, 46.0, 48.0, fill="#ffffff", stroke="none") # behind F

    # Labels
    lib.label(s, 806.0, 506.0, "M", size=54.0, italic=False, bold=True)
    lib.label(s, 390.0, 812.0, "N", size=54.0, italic=False, bold=True)
    lib.label(s, 513.0, 861.0, "D", size=48.0, italic=False, bold=True)
    lib.label(s, 664.0, 864.0, "E", size=48.0, italic=False, bold=True)
    lib.label(s, 767.0, 861.0, "P", size=48.0, italic=False, bold=True)
    lib.label(s, 775.0, 949.0, "H", size=48.0, italic=False, bold=True)
    lib.label(s, 770.0, 1046.0, "G", size=48.0, italic=False, bold=True)
    lib.label(s, 775.0, 1102.0, "F", size=48.0, italic=False, bold=True)

    s.save(out_svg)
