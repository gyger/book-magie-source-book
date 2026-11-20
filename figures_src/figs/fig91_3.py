"""Figure 91, 3: Faraday's induced current direction in helix on iron bar between magnetic poles."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 5.5
    # Upper bar magnet (3D prism)
    s.polyline([(516.0, 20.0), (232.0, 20.0), (250.0, 50.0), (534.0, 50.0)], stroke_width=sw)
    s.line(232.0, 20.0, 232.0, 118.0, stroke_width=sw)
    s.line(250.0, 50.0, 250.0, 140.0, stroke_width=sw * 0.85)
    s.polyline([(268.0, 50.0), (268.0, 190.0), (562.0, 190.0)], stroke_width=sw)

    # Lower bar magnet (3D prism)
    s.polyline([(w - 2.0, 250.0), (332.0, 250.0), (350.0, 286.0), (w - 2.0, 286.0)], stroke_width=sw)
    s.line(332.0, 250.0, 332.0, 326.0, stroke_width=sw)
    s.line(350.0, 286.0, 350.0, h - 1.0, stroke_width=sw)

    # Diagonal soft-iron cylinder bridging the two poles
    d_rod = (
        "M 204 98 Q 214 84, 230 88 "
        "L 346 376 L 322 376 L 204 98 Z"
    )
    s.path(d_rod, fill="#ffffff", stroke_width=sw)

    # Wire loop P-N wrapping around the iron rod
    # Upper wire P
    s.path("M 36 178 Q 160 170, 260 182 Q 298 188, 298 220 Q 298 242, 288 250", stroke_width=sw)
    s.path("M 36 188 Q 160 180, 258 192 Q 288 198, 288 220 Q 288 234, 282 242", stroke_width=sw)
    # Lower wire N
    s.path("M 58 254 Q 168 256, 268 252", stroke_width=sw)
    s.path("M 58 263 Q 168 264, 272 260", stroke_width=sw)

    # Current direction arrows
    lib.arrow(s, 96.0, 160.0, 174.0, 160.0, stroke_width=6.0, head_len=28.0, head_w=20.0)
    lib.arrow(s, 208.0, 285.0, 126.0, 285.0, stroke_width=6.0, head_len=28.0, head_w=20.0)

    # Labels
    lib.label(s, 26.0, 144.0, "P", size=72.0, italic=False, bold=True)
    lib.label(s, 36.0, 292.0, "N", size=72.0, italic=False, bold=True)

    s.save(out_svg)
