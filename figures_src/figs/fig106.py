"""Figure 106: Perrin's Faraday cylinder with extra metallic diaphragm beta'."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 7.5
    # Outer protecting cylinder EFGH (top line + left/right walls with openings gamma, beta)
    s.polyline([(136.0, 198.0), (136.0, 128.0), (1194.0, 128.0), (1194.0, 218.0)], stroke_width=sw)
    s.line(136.0, 286.0, 136.0, h - 1.0, stroke_width=sw)
    s.line(1194.0, 286.0, 1194.0, h - 1.0, stroke_width=sw)

    # Extra metallic diaphragm with opening beta'
    s.line(1048.0, 128.0, 1048.0, 218.0, stroke_width=sw)
    s.line(1048.0, 286.0, 1048.0, h - 1.0, stroke_width=sw)

    # Inner Faraday cylinder ABCD with opening alpha
    s.polyline([
        (890.0, 224.0), (890.0, 190.0), (488.0, 190.0),
        (488.0, 304.0), (890.0, 304.0), (890.0, 264.0),
    ], stroke_width=sw)

    # Lead wire from AD out through gamma
    s.line(36.0, 248.0, 488.0, 248.0, stroke_width=sw)

    # Labels
    lib.label(s, 100.0, 130.0, "E", size=64.0, italic=False, bold=True)
    lib.label(s, 1218.0, 132.0, "F", size=64.0, italic=False, bold=True)
    lib.label(s, 166.0, 198.0, "γ", size=64.0, italic=True, bold=True)
    lib.label(s, 456.0, 194.0, "A", size=62.0, italic=False, bold=True)
    lib.label(s, 458.0, 300.0, "D", size=62.0, italic=False, bold=True)
    lib.label(s, 916.0, 194.0, "B", size=62.0, italic=False, bold=True)
    lib.label(s, 920.0, 300.0, "C", size=62.0, italic=False, bold=True)
    lib.label(s, 852.0, 248.0, "α", size=64.0, italic=True, bold=True)
    lib.label(s, 1022.0, 216.0, "β′", size=64.0, italic=True, bold=True)
    lib.label(s, 1164.0, 216.0, "β", size=64.0, italic=True, bold=True)

    s.save(out_svg)
