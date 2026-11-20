"""Figure 35: Vibrating strings showing fundamental, 2/5 node (C, E), 2/5 & 4/5 nodes (C, E, G), and 5th harmonic (D, E, F, G)."""

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
    x1, y1 = 42.0, 134.0
    x2, y2 = 1644.0, 131.0
    _draw_baseline(s, x1, y1, x2, y2, tick_fracs=fracs)
    _draw_wave_envelope(s, x1, y1, x2, y2, [(0.0, 1.0, 102.0, 100.0)])
    lib.label(s, x1 + 2.0, y1 - 48.0, "A", size=58.0, italic=False, bold=True)
    lib.label(s, x2 + 6.0, y2 - 52.0, "B", size=58.0, italic=False, bold=True)

    # --- Row 1: Node at 2/5 (E) with dot C ---
    x1, y1 = 48.0, 438.5
    x2, y2 = 1652.0, 438.5
    _draw_baseline(s, x1, y1, x2, y2, tick_fracs=fracs)
    _draw_wave_envelope(
        s, x1, y1, x2, y2,
        [
            (0.0, 0.4, 56.0, 50.0),
            (0.4, 1.0, 62.0, 56.0),
        ],
    )
    ex = x1 + (x2 - x1) * 0.4
    lib.filled_dot(s, ex, y1 - 16.0, r=15.0)
    lib.label(s, x1 + 2.0, y1 - 48.0, "A", size=58.0, italic=False, bold=True)
    lib.label(s, x2 + 6.0, y2 - 48.0, "B", size=58.0, italic=False, bold=True)
    lib.label(s, ex + 2.0, y1 - 56.0, "C", size=58.0, italic=False, bold=True)
    lib.label(s, ex + 2.0, y1 + 42.0, "E", size=58.0, italic=False, bold=True)

    # --- Row 2: Nodes at 2/5 (E) and 4/5 (G) ---
    x1, y1 = 44.0, 756.5
    x2, y2 = 1650.0, 758.5
    _draw_baseline(s, x1, y1, x2, y2, tick_fracs=fracs)
    _draw_wave_envelope(
        s, x1, y1, x2, y2,
        [
            (0.0, 0.4, 56.0, 54.0),
            (0.4, 0.8, 56.0, 54.0),
            (0.8, 1.0, 32.0, 34.0),
        ],
    )
    ex = x1 + (x2 - x1) * 0.4
    gx = x1 + (x2 - x1) * 0.8
    lib.filled_dot(s, ex, y1 - 16.0, r=15.0)
    lib.label(s, x1 + 2.0, y1 - 48.0, "A", size=58.0, italic=False, bold=True)
    lib.label(s, x2 + 6.0, y2 - 48.0, "B", size=58.0, italic=False, bold=True)
    lib.label(s, ex + 2.0, y1 - 56.0, "C", size=58.0, italic=False, bold=True)
    lib.label(s, ex + 2.0, y1 + 42.0, "E", size=58.0, italic=False, bold=True)
    lib.label(s, gx + 2.0, y1 + 44.0, "G", size=58.0, italic=False, bold=True)

    # --- Row 3: 5th harmonic (nodes D, E, F, G) ---
    x1, y1 = 45.0, 1077.0
    x2, y2 = 1652.0, 1076.5
    _draw_baseline(s, x1, y1, x2, y2, tick_fracs=fracs)
    _draw_wave_envelope(
        s, x1, y1, x2, y2,
        [(i * 0.2, (i + 1) * 0.2, 34.0, 36.0) for i in range(5)],
    )
    dx = x1 + (x2 - x1) * 0.2
    ex = x1 + (x2 - x1) * 0.4
    fx = x1 + (x2 - x1) * 0.6
    gx = x1 + (x2 - x1) * 0.8
    lib.filled_dot(s, ex, y1 - 16.0, r=15.0)
    lib.label(s, x1 + 2.0, y1 - 48.0, "A", size=58.0, italic=False, bold=True)
    lib.label(s, x2 + 6.0, y2 - 48.0, "B", size=58.0, italic=False, bold=True)
    lib.label(s, ex + 2.0, y1 - 56.0, "C", size=58.0, italic=False, bold=True)
    lib.label(s, dx + 2.0, y1 + 44.0, "D", size=58.0, italic=False, bold=True)
    lib.label(s, ex + 2.0, y1 + 44.0, "E", size=58.0, italic=False, bold=True)
    lib.label(s, fx + 2.0, y1 + 44.0, "F", size=58.0, italic=False, bold=True)
    lib.label(s, gx + 2.0, y1 + 44.0, "G", size=58.0, italic=False, bold=True)

    s.save(out_svg)
