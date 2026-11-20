"""Figure 19: Varignon's theorem of moments (parallelogram ACDB with pole S)."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def _lerp(p: tuple[float, float], q: tuple[float, float], t: float) -> tuple[float, float]:
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def _intersect(
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    p4: tuple[float, float],
) -> tuple[float, float]:
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    # Primary vertices of parallelogram ACDB
    A = (318.4, 255.0)
    C = (62.0, 654.0)
    D = (315.1, 1455.2)
    B = (571.5, 1056.2)  # A + D - C
    S = (1355.0, 1246.0)

    # Auxiliary points
    # G lies on AC (~52% from A to C)
    G = _lerp(A, C, 0.52)
    # H is intersection of GS with line DB extended past B
    H = _intersect(G, S, D, B)
    # N is on AD around y = 1272
    N = (316.0, 1272.0)
    # M is extension of AB past B to y = 1484
    t_M = (1484.0 - A[1]) / (B[1] - A[1])
    M = _lerp(A, B, t_M)

    # Extensions above A:
    # E along SA extended past A
    E = _lerp(S, A, 1.18)
    # K along BA extended past A
    K = _lerp(B, A, 1.20)
    # F along CA extended past A
    F = _lerp(C, A, 1.40)

    # Solid lines: AC, CD, AD, AB
    sw_solid = 8.5
    s.line(*A, *C, stroke_width=sw_solid)
    s.line(*C, *D, stroke_width=sw_solid)
    s.line(*A, *D, stroke_width=sw_solid)
    s.line(*A, *B, stroke_width=sw_solid)

    # Dashed construction lines
    sw_dash = 5.0
    dash_long = "32,16"
    # Rays from S
    s.line(*S, *E, stroke_width=sw_dash, dash=dash_long)
    s.line(*S, *G, stroke_width=sw_dash, dash=dash_long)
    s.line(*S, *C, stroke_width=sw_dash, dash=dash_long)
    s.line(*S, *B, stroke_width=sw_dash, dash=dash_long)
    s.line(*S, *N, stroke_width=sw_dash, dash=dash_long)
    s.line(*S, *D, stroke_width=sw_dash, dash=dash_long)
    s.line(*S, *M, stroke_width=sw_dash, dash=dash_long)

    # Extensions of parallelogram sides
    s.line(*D, *H, stroke_width=sw_dash, dash=dash_long)
    s.line(*A, *K, stroke_width=sw_dash, dash=dash_long)
    s.line(*A, *F, stroke_width=sw_dash, dash=dash_long)
    s.line(*B, *M, stroke_width=sw_dash, dash=dash_long)

    # Labels
    labels = [
        ("E", 113, 62),
        ("K", 242, 60),
        ("F", 433, 54),
        ("A", 367, 267),
        ("G", 151, 440),
        ("C", 22, 654),
        ("H", 752, 796),
        ("B", 520, 1068),
        ("N", 349, 1233),
        ("S", 1389, 1241),
        ("D", 314, 1490),
        ("M", 716, 1516),
    ]
    for txt, x, y in labels:
        lib.label(s, x, y, txt, size=50, italic=False, bold=True)

    s.save(out_svg)
