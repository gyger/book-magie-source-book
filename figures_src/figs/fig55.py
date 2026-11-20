"""Figure 55: Bartholinus's Iceland spar rhomboid crystal geometry."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 6.0

    # Top parallelogram
    t_tl = (34.0, 43.0)
    t_tr = (726.0, 39.0)
    t_br = (1004.0, 193.0)
    t_bl = (306.0, 198.0)

    # Bottom parallelogram
    b_tl = (384.0, 671.0)
    b_tr = (1078.0, 667.0)
    b_br = (1355.0, 806.0)
    b_bl = (638.0, 806.0)

    # Top face
    s.polygon([t_tl, t_tr, t_br, t_bl], stroke_width=sw)
    # Bottom visible/back edges
    s.line(*b_tl, *b_tr, stroke_width=sw)
    s.line(*b_tl, *b_bl, stroke_width=sw)
    s.line(*b_tr, *b_br, stroke_width=sw)
    # Vertical/slanted connecting edges
    s.line(*t_tl, *b_tl, stroke_width=sw)
    s.line(*t_tr, *b_tr, stroke_width=sw)
    s.line(*t_br, *b_br, stroke_width=sw)
    s.line(*t_bl, *b_bl, stroke_width=sw)

    s.save(out_svg)
