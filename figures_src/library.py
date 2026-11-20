"""Shared geometric and typographic helpers for Source Book in Physics SVGs."""

from __future__ import annotations

import math
from draw import Scene, _fmt


DEFAULT_STROKE = 4.5
THIN_STROKE = 3.2
DASH_MAIN = "16,12"
DASH_FINE = "10,9"


def label(
    scene: Scene,
    x: float,
    y: float,
    text: str,
    *,
    size: float = 54.0,
    italic: bool = True,
    bold: bool = False,
    anchor: str = "middle",
    baseline: str = "central",
    rotate: float | None = None,
) -> None:
    """Place a classical physics-diagram letter/label."""
    scene.text(
        x,
        y,
        text,
        size=size,
        family="New Computer Modern, Latin Modern Roman, Georgia, serif",
        style="italic" if italic else "normal",
        weight="bold" if bold else "normal",
        anchor=anchor,
        baseline=baseline,
        rotate=rotate,
    )


def arrow(
    scene: Scene,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    *,
    stroke_width: float = DEFAULT_STROKE,
    head_len: float = 22.0,
    head_w: float = 12.0,
    dash: str | None = None,
    double: bool = False,
) -> None:
    """Draw a line with an arrow head at (x2, y2) (and optionally at (x1, y1))."""
    scene.line(x1, y1, x2, y2, stroke_width=stroke_width, dash=dash)
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    if L < 1e-6:
        return
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux

    def _head(tx: float, ty: float, dir_x: float, dir_y: float) -> None:
        bx, by = tx - dir_x * head_len, ty - dir_y * head_len
        p1 = (bx + nx * head_w * 0.5, by + ny * head_w * 0.5)
        p2 = (bx - nx * head_w * 0.5, by - ny * head_w * 0.5)
        scene.polygon([(tx, ty), p1, p2], fill="#000000", stroke="#000000", stroke_width=1.5)

    _head(x2, y2, ux, uy)
    if double:
        _head(x1, y1, -ux, -uy)


def open_dot(
    scene: Scene,
    cx: float,
    cy: float,
    r: float = 7.0,
    stroke_width: float = 3.5,
) -> None:
    scene.circle(cx, cy, r, fill="#ffffff", stroke="#000000", stroke_width=stroke_width)


def filled_dot(scene: Scene, cx: float, cy: float, r: float = 6.0) -> None:
    scene.circle(cx, cy, r, fill="#000000", stroke="none")


def right_angle_mark(
    scene: Scene,
    vx: float,
    vy: float,
    u1: tuple[float, float],
    u2: tuple[float, float],
    size: float = 18.0,
    stroke_width: float = 2.8,
) -> None:
    """Small right-angle square at vertex (vx, vy) along unit vectors u1, u2."""
    p1 = (vx + u1[0] * size, vy + u1[1] * size)
    p2 = (vx + (u1[0] + u2[0]) * size, vy + (u1[1] + u2[1]) * size)
    p3 = (vx + u2[0] * size, vy + u2[1] * size)
    scene.polyline([p1, p2, p3], stroke_width=stroke_width)


def smooth_curve(
    scene: Scene,
    pts: list[tuple[float, float]],
    *,
    stroke_width: float = DEFAULT_STROKE,
    dash: str | None = None,
) -> None:
    """Catmull-Rom to cubic Bezier smooth curve through points."""
    if len(pts) < 2:
        return
    if len(pts) == 2:
        scene.line(pts[0][0], pts[0][1], pts[1][0], pts[1][1], stroke_width=stroke_width, dash=dash)
        return
    d_parts = [f"M {_fmt(pts[0][0])} {_fmt(pts[0][1])}"]
    n = len(pts)
    for i in range(n - 1):
        p0 = pts[max(0, i - 1)]
        p1 = pts[i]
        p2 = pts[i + 1]
        p3 = pts[min(n - 1, i + 2)]
        c1x = p1[0] + (p2[0] - p0[0]) / 6.0
        c1y = p1[1] + (p2[1] - p0[1]) / 6.0
        c2x = p2[0] - (p3[0] - p1[0]) / 6.0
        c2y = p2[1] - (p3[1] - p1[1]) / 6.0
        d_parts.append(
            f"C {_fmt(c1x)} {_fmt(c1y)}, {_fmt(c2x)} {_fmt(c2y)}, {_fmt(p2[0])} {_fmt(p2[1])}"
        )
    scene.path(" ".join(d_parts), stroke_width=stroke_width, dash=dash)
