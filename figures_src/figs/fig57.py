"""Figure 57: Bartholinus's double refraction experiment with rotating Iceland spar crystal and eye O."""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    sw = 4.5
    sw_thin = 3.5

    # Crystal top face I-E-K-D
    pt_i = (740.0, 581.0)
    pt_e = (1434.0, 583.0)
    pt_k = (1232.0, 804.0)
    pt_d = (530.0, 801.0)

    # Crystal bottom face (back-left P, M, H, L)
    pt_p = (514.0, 1250.0)
    pt_m = (1212.0, 1255.0)
    pt_h = (1008.0, 1456.0)
    pt_l = (304.0, 1453.0)

    # Base/table slab F-G
    # Top outline (drawn behind crystal)
    tbl_bl = (56.0, 1598.0)
    tbl_br = (1470.0, 1598.0)
    tbl_tr = (1600.0, 932.0)
    tbl_tl = (198.0, 928.0)
    # 3D bottom thickness
    tbl_bl2 = (86.0, 1646.0)
    tbl_br2 = (1488.0, 1646.0)
    tbl_tr2 = (1622.0, 976.0)

    # Table top edges (clipped outside crystal left/right)
    s.line(*tbl_tl, 480.0, 929.0, stroke_width=sw)
    s.line(1312.0, 931.0, *tbl_tr, stroke_width=sw)
    s.line(*tbl_tl, *tbl_bl, stroke_width=sw)
    s.line(*tbl_bl, *tbl_br, stroke_width=sw)
    s.line(*tbl_br, *tbl_tr, stroke_width=sw)
    # Table thickness edges
    s.line(*tbl_bl, *tbl_bl2, stroke_width=sw)
    s.line(*tbl_bl2, *tbl_br2, stroke_width=sw)
    s.line(*tbl_br2, *tbl_tr2, stroke_width=sw)
    s.line(*tbl_tr, *tbl_tr2, stroke_width=sw)
    s.line(*tbl_br, *tbl_br2, stroke_width=sw)

    # Crystal faces and edges
    s.polygon([pt_i, pt_e, pt_k, pt_d], stroke_width=sw)
    s.polygon([pt_p, pt_m, pt_h, pt_l], stroke_width=sw)
    s.line(*pt_i, *pt_p, stroke_width=sw)
    s.line(*pt_e, *pt_m, stroke_width=sw)
    s.line(*pt_k, *pt_h, stroke_width=sw)
    s.line(*pt_d, *pt_l, stroke_width=sw)

    # Diagonals D-E (top) and L-M (bottom)
    s.line(*pt_d, *pt_e, stroke_width=sw_thin)
    s.line(*pt_l, *pt_m, stroke_width=sw_thin)

    # Object point A on L-M and two image points C, B on D-E
    pt_a = (758.0, 1354.0)
    pt_c = (886.0, 715.0)
    pt_b = (982.0, 692.0)
    pt_o = (1422.0, 62.0)

    # Small tilted ellipse around C and B on top face
    s.ellipse(886.0, 715.0, 98.0, 62.0, rotate=-14.0, stroke_width=sw_thin)

    # Rays A -> C -> O and A -> B -> O
    s.line(*pt_a, *pt_c, stroke_width=sw_thin)
    s.line(*pt_c, *pt_o, stroke_width=sw_thin)
    s.line(*pt_a, *pt_b, stroke_width=sw_thin)
    s.line(*pt_b, *pt_o, stroke_width=sw_thin)

    # Open dots at A, C, B
    lib.open_dot(s, *pt_a, r=10.0, stroke_width=3.5)
    lib.open_dot(s, *pt_c, r=9.0, stroke_width=3.5)
    lib.open_dot(s, *pt_b, r=9.0, stroke_width=3.5)

    # Eye icon at O
    s.path(
        "M 1384 62 Q 1422 36 1460 62 Q 1422 88 1384 62 Z",
        fill="#ffffff",
        stroke="#000000",
        stroke_width=4.0,
    )
    lib.filled_dot(s, 1422.0, 62.0, r=11.0)

    # Labels
    lib.label(s, 1344.0, 62.0, "O", size=50.0, italic=False, bold=True)
    lib.label(s, 732.0, 536.0, "I", size=50.0, italic=False, bold=True)
    lib.label(s, 1466.0, 586.0, "E", size=50.0, italic=False, bold=True)
    lib.label(s, 848.0, 694.0, "C", size=44.0, italic=False, bold=True)
    lib.label(s, 1020.0, 732.0, "B", size=44.0, italic=False, bold=True)
    lib.label(s, 474.0, 798.0, "D", size=50.0, italic=False, bold=True)
    lib.label(s, 1172.0, 845.0, "K", size=50.0, italic=False, bold=True)
    lib.label(s, 132.0, 932.0, "F", size=50.0, italic=False, bold=True)
    lib.label(s, 706.0, 1325.0, "A", size=46.0, italic=False, bold=True)
    lib.label(s, 1252.0, 1272.0, "M", size=48.0, italic=False, bold=True)
    lib.label(s, 260.0, 1455.0, "L", size=50.0, italic=False, bold=True)
    lib.label(s, 1012.0, 1498.0, "H", size=50.0, italic=False, bold=True)
    lib.label(s, 1524.0, 1656.0, "G", size=50.0, italic=False, bold=True)

    s.save(out_svg)
