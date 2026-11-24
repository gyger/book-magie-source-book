"""Figure 95: Joule's glass calorimeter jar B with thermometer T and coiled wire A."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.0
    # Glass jar base foot (elliptical base)
    s.ellipse(189.0, 1380.0, 178.0, 74.0, fill="#ffffff", stroke_width=sw * 1.1)
    s.ellipse(189.0, 1387.0, 106.0, 23.0, fill="#ffffff", stroke_width=sw * 0.85)

    # Glass jar vertical walls
    s.line(83.0, 566.0, 83.0, 1387.0, stroke_width=sw)
    s.line(295.0, 566.0, 295.0, 1387.0, stroke_width=sw)

    # Top rim ellipse
    s.ellipse(189.0, 566.0, 106.0, 34.0, fill="none", stroke_width=sw)

    # Water meniscus (dashed ellipse at y=674)
    s.ellipse(189.0, 674.0, 106.0, 34.0, fill="none", stroke_width=sw * 0.85, dash="22,16")

    # Thermometer T (vertical stem + filled mercury column + bulb)
    s.line(115.0, 0.0, 115.0, 1020.0, stroke_width=sw * 0.85)
    s.line(129.0, 0.0, 129.0, 1020.0, stroke_width=sw * 0.85)
    # Mercury column & bulb
    s.rect(116.0, 682.0, 12.0, 340.0, fill="#000000", stroke="none")
    s.circle(123.0, 1030.0, 15.0, fill="#000000", stroke="none")

    # Inclined glass tube A with coiled heating wire
    # Top center (281, 440), bottom center (112, 1382)
    x_top, y_top = 281.0, 440.0
    x_bot, y_bot = 112.0, 1382.0
    dx, dy = x_bot - x_top, y_bot - y_top
    L = (dx * dx + dy * dy) ** 0.5
    nx, ny = -dy / L, dx / L  # unit normal
    hw = 16.0  # half-width of glass tube

    # Tube outline
    pts_tube = [
        (x_top + nx * hw, y_top + ny * hw),
        (x_bot + nx * hw, y_bot + ny * hw),
        (x_bot - nx * hw, y_bot - ny * hw),
        (x_top - nx * hw, y_top - ny * hw),
    ]
    s.polygon(pts_tube, fill="#ffffff", stroke_width=sw * 0.85)

    # Central wire inside upper uncoiled part of glass tube
    s.line(x_top, y_top, x_top + dx * 0.28, y_top + dy * 0.28, stroke_width=4.5)

    # Coiled wire turns wrapped around lower submerged portion (t = 0.26 .. 0.99)
    n_turns = 48
    for i in range(n_turns):
        t = 0.26 + (0.99 - 0.26) * i / (n_turns - 1)
        cx = x_top + dx * t
        cy = y_top + dy * t
        s.line(
            cx - nx * (hw + 2.0), cy - ny * (hw + 2.0),
            cx + nx * (hw + 2.0), cy + ny * (hw + 2.0),
            stroke_width=4.8,
        )

    # Two lead wires emerging from top of tube A to the right
    s.path("M 294 440 Q 332 426, 368 552", stroke_width=sw)
    s.path("M 284 544 Q 316 534, 338 624", stroke_width=sw)

    # Labels
    lib.label(s, 84.0, 214.0, "T", size=72.0, italic=False, bold=True)
    lib.label(s, 282.0, 386.0, "A", size=72.0, italic=False, bold=True)
    lib.label(s, 318.0, 962.0, "B", size=72.0, italic=False, bold=True)

    s.save(out_svg)
