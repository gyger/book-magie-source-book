"""Figure 91, 6: Faraday's cylindrical magnet A-B with knife blade N-P cutting magnetic curves."""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw_field = 4.2
    sw_mag = 6.5

    # Closed magnetic field curves arching above the magnet (7 curves)
    for peak_y, x1, x2 in [
        (202, 260, 824),
        (170, 255, 832),
        (140, 250, 838),
        (110, 246, 844),
        (80,  242, 850),
        (52,  238, 855),
        (24,  235, 860),
    ]:
        cx = 0.5 * (x1 + x2)
        cy_ctrl = 2.0 * peak_y - 340.0
        s.path(f"M {x1} 340 Q {cx:.1f} {cy_ctrl:.1f}, {x2} 336", stroke_width=sw_field)

    # Closed magnetic field curves arching below the magnet (6 curves)
    for peak_y, x1, x2 in [
        (530, 265, 824),
        (558, 260, 832),
        (586, 255, 840),
        (612, 250, 848),
        (638, 245, 856),
        (662, 240, 862),
    ]:
        cx = 0.5 * (x1 + x2)
        cy_ctrl = 2.0 * peak_y - 406.0
        s.path(f"M {x1} 406 Q {cx:.1f} {cy_ctrl:.1f}, {x2} 406", stroke_width=sw_field)

    # Open radiating field lines from left pole A (centered near (240, 368))
    ax, ay = 240.0, 368.0
    for deg in range(76, 296, 10):
        a = math.radians(deg)
        length = 260.0 if 140 <= deg <= 225 else 300.0
        if deg > 250 or deg < 110:
            length = 340.0
        x2 = max(4.0, min(w - 4.0, ax + length * math.cos(a)))
        y2 = max(14.0, min(h - 14.0, ay + length * math.sin(a)))
        s.line(ax, ay, x2, y2, stroke_width=sw_field)

    # Open radiating field lines from right pole B (centered near (866, 368))
    bx, by = 866.0, 368.0
    for deg in range(-106, 108, 10):
        a = math.radians(deg)
        length = 260.0 if -40 <= deg <= 40 else 280.0
        x2 = max(4.0, min(w - 4.0, bx + length * math.cos(a)))
        y2 = max(14.0, min(h - 14.0, by + length * math.sin(a)))
        s.line(bx, by, x2, y2, stroke_width=sw_field)

    # Cylindrical bar magnet A-B (white-filled to cleanly mask field lines)
    d_mag = (
        "M 232 332 L 892 332 "
        "A 18 37 0 0 1 892 406 "
        "L 232 406 "
        "A 18 37 0 0 1 232 332 Z"
    )
    s.path(d_mag, fill="#ffffff", stroke_width=sw_mag)
    s.ellipse(232.0, 369.0, 18.0, 37.0, fill="#ffffff", stroke_width=sw_mag)

    # Oblique silver knife-blade N-P resting across magnet
    d_blade = (
        "M 438 238 "
        "Q 480 250, 514 300 "
        "L 574 388 "
        "Q 574 400, 560 396 "
        "L 438 238 Z"
    )
    s.path(d_blade, fill="#ffffff", stroke_width=sw_mag * 0.85)

    # Labels
    lib.label(s, 294.0, 374.0, "A", size=68.0, italic=False, bold=True)
    lib.label(s, 864.0, 368.0, "B", size=68.0, italic=False, bold=True)
    lib.label(s, 422.0, 276.0, "N", size=66.0, italic=False, bold=True)
    lib.label(s, 598.0, 382.0, "P", size=66.0, italic=False, bold=True)

    s.save(out_svg)
