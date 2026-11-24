"""Figure 34: Vibrating strings showing fundamental, asymmetric node at 1/5 (C, D), and 5th harmonic."""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image

import draw
import library as lib


def _draw_wave_envelope(
    s: draw.Scene,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    segments: list[tuple[float, float, float, float]],
    *,
    stroke_width: float = 8.0,
) -> None:
    """Draw upper and lower sine-loop envelopes along baseline (x1,y1)->(x2,y2).

    segments: list of (t_start, t_end, amp_up, amp_dn) in normalized t in [0, 1].
    """
    for t0, t1, amp_up, amp_dn in segments:
        n = 48
        pts_up: list[tuple[float, float]] = []
        pts_dn: list[tuple[float, float]] = []
        for i in range(n + 1):
            u = i / n
            t = t0 + (t1 - t0) * u
            bx = x1 + (x2 - x1) * t
            by = y1 + (y2 - y1) * t
            sin_val = math.sin(math.pi * u)
            pts_up.append((bx, by - amp_up * sin_val))
            pts_dn.append((bx, by + amp_dn * sin_val))
        s.polyline(pts_up, stroke_width=stroke_width)
        s.polyline(pts_dn, stroke_width=stroke_width)


def _draw_baseline(
    s: draw.Scene,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    *,
    tick_fracs: list[float],
    tick_half: float = 18.0,
) -> None:
    s.line(x1, y1, x2, y2, stroke_width=6.0)
    for t in [0.0, *tick_fracs, 1.0]:
        bx = x1 + (x2 - x1) * t
        by = y1 + (y2 - y1) * t
        th = tick_half if t in (0.0, 1.0) else tick_half * 0.85
        s.line(bx, by - th, bx, by + th, stroke_width=5.5)


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    fracs = [0.2, 0.4, 0.6, 0.8]

    # --- Row 0: Fundamental ---
    x1, y1 = 38.0, 110.0
    x2, y2 = 1604.0, 134.0
    _draw_baseline(s, x1, y1, x2, y2, tick_fracs=fracs)
    _draw_wave_envelope(s, x1, y1, x2, y2, [(0.0, 1.0, 91.0, 98.0)])
    lib.label(s, x1 + 4.0, y1 - 45.0, "A", size=58.0, italic=False, bold=True)
    lib.label(s, x2 + 6.0, y2 - 56.0, "B", size=58.0, italic=False, bold=True)

    # --- Row 1: Node at 1/5 (D) with dot C ---
    x1, y1 = 48.0, 449.0
    x2, y2 = 1612.0, 471.0
    _draw_baseline(s, x1, y1, x2, y2, tick_fracs=fracs)
    _draw_wave_envelope(
        s, x1, y1, x2, y2,
        [
            (0.0, 0.2, 31.0, 31.0),
            (0.2, 1.0, 58.0, 62.0),
        ],
    )
    node_x = x1 + (x2 - x1) * 0.2
    node_y = y1 + (y2 - y1) * 0.2
    lib.filled_dot(s, node_x, node_y - 16.0, r=15.0)
    lib.label(s, x1 + 2.0, y1 - 45.0, "A", size=58.0, italic=False, bold=True)
    lib.label(s, x2 + 4.0, y2 - 56.0, "B", size=58.0, italic=False, bold=True)
    lib.label(s, node_x + 4.0, node_y - 60.0, "C", size=58.0, italic=False, bold=True)
    lib.label(s, node_x + 2.0, node_y + 42.0, "D", size=58.0, italic=False, bold=True)

    # --- Row 2: 5th harmonic (5 equal loops) ---
    x1, y1 = 40.0, 779.0
    x2, y2 = 1610.0, 804.0
    _draw_baseline(s, x1, y1, x2, y2, tick_fracs=fracs)
    _draw_wave_envelope(
        s, x1, y1, x2, y2,
        [(i * 0.2, (i + 1) * 0.2, 29.0, 28.0) for i in range(5)],
    )
    node_x = x1 + (x2 - x1) * 0.2
    node_y = y1 + (y2 - y1) * 0.2
    lib.filled_dot(s, node_x - 1.0, node_y - 19.0, r=15.5)
    lib.label(s, x1 + 2.0, y1 - 45.0, "A", size=58.0, italic=False, bold=True)
    lib.label(s, x2 + 4.0, y2 - 56.0, "B", size=58.0, italic=False, bold=True)
    lib.label(s, node_x - 5.0, node_y - 63.0, "C", size=58.0, italic=False, bold=True)
    # Interior node labels D, E, F, G (partially clipped at bottom edge of scan)
    for t, lbl in zip(fracs, ("D", "E", "F", "G")):
        nx = x1 + (x2 - x1) * t
        ny = y1 + (y2 - y1) * t
        lib.label(s, nx, ny + 43.0, lbl, size=58.0, italic=False, bold=True)

    s.save(out_svg)
