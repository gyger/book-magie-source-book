"""Figure 91, 2: Faraday's helix on soft-iron core between two bar magnets with galvanometer."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.5
    # Left galvanometer dial
    cx, cy = 98.0, 128.0
    s.circle(cx, cy, 78.0, fill="#ffffff", stroke_width=sw)
    s.circle(cx, cy, 67.0, fill="none", stroke_width=sw * 0.75)

    # Dial tick marks around circumference
    import math
    for deg in range(0, 360, 22):
        a = math.radians(deg)
        r1 = 50.0 if deg % 90 == 0 else 56.0
        r2 = 66.0
        s.line(
            cx + r1 * math.cos(a), cy + r1 * math.sin(a),
            cx + r2 * math.cos(a), cy + r2 * math.sin(a),
            stroke_width=4.0,
        )
    # Horizontal compass needle in dial
    s.rect(cx - 40.0, cy - 7.0, 80.0, 14.0, fill="#ffffff", stroke_width=5.0, rx=5.0)

    # Connecting wires from dial to helix bobbin
    s.path("M 176 122 C 260 98, 520 96, 700 66 C 860 32, 960 28, 1138 62", stroke_width=sw)
    s.path("M 176 134 C 280 156, 450 164, 650 212 C 800 246, 980 226, 1138 196", stroke_width=sw)

    # Soft-iron core ends + vertical helix bobbin
    s.rect(1140.0, 44.0, 20.0, 168.0, fill="#ffffff", stroke_width=sw * 0.8)
    s.rect(1126.0, 60.0, 48.0, 138.0, fill="#ffffff", stroke_width=sw, rx=16.0)

    # Two bar magnets converging in a V to the right
    # Upper bar magnet
    s.polyline([(1134.0, 18.0), (w - 2.0, 76.0)], stroke_width=sw)
    s.polyline([(1134.0, 38.0), (w - 2.0, 96.0)], stroke_width=sw * 0.85)
    s.polyline([(1134.0, 48.0), (w - 2.0, 106.0)], stroke_width=sw)
    s.line(1134.0, 18.0, 1134.0, 48.0, stroke_width=sw)

    # Lower bar magnet
    s.polyline([(1134.0, 208.0), (w - 2.0, 112.0)], stroke_width=sw)
    s.polyline([(1134.0, 224.0), (w - 2.0, 126.0)], stroke_width=sw * 0.85)
    s.polyline([(1134.0, 236.0), (w - 2.0, 138.0)], stroke_width=sw)
    s.line(1134.0, 208.0, 1134.0, 236.0, stroke_width=sw)

    s.save(out_svg)
