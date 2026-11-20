"""Figure 3: Galileo's mean-speed theorem diagram (rectangle GABF, triangle AEB, line CD)."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    scene = draw.Scene(w, h)

    sw = 8.5
    sw_bar = 6.5

    # Vertical lines GF, AB, CD
    x_gf = 220.5
    x_ab = 392.5
    x_cd = 587.5

    y_top = 164.5
    y_bot = 1267.5
    x_e = 50.0  # Bottom-left vertex E of triangle AEB

    # Main vertical lines of rectangle GABF
    scene.line(x_gf, y_top, x_gf, y_bot, stroke_width=sw)
    scene.line(x_ab, y_top, x_ab, y_bot, stroke_width=sw)

    # Diagonal AE (passing through I on GF)
    scene.line(x_ab, y_top, x_e, y_bot, stroke_width=sw)

    # Horizontal bars: top GA, 7 interior rungs, bottom EB
    ys = [164.5, 325.5, 458.5, 591.5, 725.5, 859.5, 994.5, 1129.5, 1267.5]
    for idx, yy in enumerate(ys):
        t = (yy - y_top) / (y_bot - y_top)
        x_diag = x_ab + t * (x_e - x_ab)
        x_left = min(x_gf, x_diag)
        w_bar = sw if idx in (0, len(ys) - 1) else sw_bar
        scene.line(x_left, yy, x_ab, yy, stroke_width=w_bar)

    # Vertical line CD with end caps
    y_c = 76.0
    y_d = 1500.0
    scene.line(x_cd, y_c, x_cd, y_d, stroke_width=sw)
    scene.line(x_cd - 20.0, y_c, x_cd + 20.0, y_c, stroke_width=sw)
    scene.line(x_cd - 20.0, y_d, x_cd + 20.0, y_d, stroke_width=sw)

    # Labels (excluding the stray 'FIG. 3.' caption at bottom)
    lib.label(scene, 222, 120, "G", size=64, italic=False, bold=True)
    lib.label(scene, 396, 122, "A", size=64, italic=False, bold=True)
    lib.label(scene, 588, 36, "C", size=64, italic=False, bold=True)
    lib.label(scene, 180, 720, "I", size=64, italic=False, bold=True)
    lib.label(scene, 50, 1304, "E", size=64, italic=False, bold=True)
    lib.label(scene, 218, 1304, "F", size=64, italic=False, bold=True)
    lib.label(scene, 384, 1304, "B", size=64, italic=False, bold=True)
    lib.label(scene, 586, 1536, "D", size=64, italic=False, bold=True)

    scene.save(out_svg)
