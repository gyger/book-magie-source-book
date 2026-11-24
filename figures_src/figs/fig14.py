"""Figure 14: Stevinus's sphere on an inclined plane with pulley and balance."""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image

import draw
import library as lib


def _pear_weight(s: draw.Scene, cx: float, top_y: float, rx: float, h: float, sw: float = 5.5) -> None:
    bot_y = top_y + h
    mid_y = top_y + h * 0.65
    d = (
        f"M {cx:.1f} {top_y:.1f} "
        f"C {cx + rx * 0.45:.1f} {top_y + h * 0.22:.1f}, "
        f"{cx + rx * 1.05:.1f} {mid_y - h * 0.12:.1f}, "
        f"{cx + rx:.1f} {mid_y:.1f} "
        f"C {cx + rx * 0.98:.1f} {bot_y - h * 0.06:.1f}, "
        f"{cx + rx * 0.45:.1f} {bot_y:.1f}, "
        f"{cx:.1f} {bot_y:.1f} "
        f"C {cx - rx * 0.45:.1f} {bot_y:.1f}, "
        f"{cx - rx * 0.98:.1f} {bot_y - h * 0.06:.1f}, "
        f"{cx - rx:.1f} {mid_y:.1f} "
        f"C {cx - rx * 1.05:.1f} {mid_y - h * 0.12:.1f}, "
        f"{cx - rx * 0.45:.1f} {top_y + h * 0.22:.1f}, "
        f"{cx:.1f} {top_y:.1f} Z"
    )
    s.path(d, fill="#ffffff", stroke="#000000", stroke_width=sw)


def _draw_hand_fig14(s: draw.Scene, sw: float = 5.0) -> None:
    """Clean vector reconstruction of the hand holding the balance stem in Fig. 14."""
    # Sleeve & cuff
    s.line(200, 0, 200, 38, stroke_width=sw)
    s.line(310, 0, 310, 38, stroke_width=sw)
    lib.smooth_curve(s, [(200, 38), (255, 45), (310, 38)], stroke_width=sw)
    # Left palm & thumb curving down around stem
    lib.smooth_curve(s, [(210, 42), (200, 95), (189, 130), (199, 165), (222, 185), (252, 195), (272, 180)], stroke_width=sw)
    # Index finger
    lib.smooth_curve(s, [(218, 112), (212, 142), (222, 164), (242, 178)], stroke_width=sw)
    lib.smooth_curve(s, [(218, 114), (246, 136), (266, 168), (278, 212), (288, 232), (296, 224), (292, 182), (278, 146), (246, 112)], stroke_width=sw)
    # Middle finger
    lib.smooth_curve(s, [(294, 192), (308, 198), (324, 198), (330, 178), (322, 148), (298, 118), (274, 102)], stroke_width=sw)
    # Ring & pinky / right back of hand
    lib.smooth_curve(s, [(292, 42), (312, 92), (336, 132), (334, 162), (326, 172)], stroke_width=sw)
    lib.smooth_curve(s, [(296, 104), (318, 136), (324, 166)], stroke_width=sw)


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)
    sw = 5.5

    # 1. Inclined plane line AB: y = -0.4046*x + 900.3
    m_inc, b_inc = -0.4046, 900.3
    xA, xB = 188.0, 825.0
    A = (xA, m_inc * xA + b_inc)
    B = (xB, m_inc * xB + b_inc)
    s.line(*A, *B, stroke_width=6.0)

    # 2. Sphere (circle) resting on AB
    # Center D, radius r, tangent to AB at G
    r = 104.5
    nx, ny = -0.3751, -0.9270
    G_x = 426.0
    G = (G_x, m_inc * G_x + b_inc)
    D = (G[0] + r * nx, G[1] + r * ny)
    H = (D[0] + r * nx, D[1] + r * ny)

    s.circle(D[0], D[1], r, fill="#ffffff", stroke="#000000", stroke_width=sw)
    s.line(*H, *G, stroke_width=sw)

    # 3. Upper pulley F, stand, 3D base
    F_cx, F_cy, F_r = 956.0, 170.0, 90.0

    # String from D tangent to upper-left of pulley F
    ang_DF = math.atan2(F_cy - D[1], F_cx - D[0])
    dist_DF = math.hypot(F_cx - D[0], F_cy - D[1])
    alpha = math.asin(F_r / dist_DF)
    tang_ang = ang_DF - alpha - math.pi / 2.0
    F_tang = (F_cx + F_r * math.cos(tang_ang), F_cy + F_r * math.sin(tang_ang))
    s.line(D[0], D[1], F_tang[0], F_tang[1], stroke_width=sw)

    # 4. Balance beam, stem, strings K-D, K-C, E-C, and weight M
    beam_y = 356.0
    x_M = 80.0
    x_stem = 232.7
    K = (385.0, beam_y)
    s.line(x_M, beam_y, K[0], K[1], stroke_width=sw)
    s.line(x_stem, 130.0, x_stem, beam_y, stroke_width=sw)
    s.line(x_M, beam_y, x_M, 548.0, stroke_width=sw)
    _pear_weight(s, x_M, 548.0, rx=55.0, h=148.0, sw=sw)

    # K -> D (vertical)
    s.line(K[0], K[1], D[0], D[1], stroke_width=sw)

    # Vertical E-C at x = 527.7
    x_EC = 527.7
    C = (x_EC, m_inc * x_EC + b_inc)
    # E lies on line D -> F_tang at x = x_EC
    t_E = (x_EC - D[0]) / (F_tang[0] - D[0])
    E = (x_EC, D[1] + t_E * (F_tang[1] - D[1]))
    s.line(*E, *C, stroke_width=sw)
    # K -> C (passes through L and O)
    s.line(*K, *C, stroke_width=sw)

    # 5. Pulley F stand & 3D rectangular pedestal base
    bx1, bx2, by1, by2 = 834.0, 1060.0, 855.0, 954.0
    bdx, bdy = 78.0, -68.0
    s.rect(bx1, by1, bx2 - bx1, by2 - by1, fill="#ffffff", stroke="#000000", stroke_width=sw)
    s.polygon([(bx1, by1), (bx1 + bdx, by1 + bdy), (bx2 + bdx, by1 + bdy), (bx2, by1)], fill="#ffffff", stroke="#000000", stroke_width=sw)
    s.polygon([(bx2, by1), (bx2 + bdx, by1 + bdy), (bx2 + bdx, by2 + bdy), (bx2, by2)], fill="#ffffff", stroke="#000000", stroke_width=sw)

    # 3D vertical post — right side face (behind pulley wheel, occluded at rim)
    px1, px2, px3 = 936.0, 962.0, 990.0
    ptop, pbot = 148.0, 834.0
    s.polygon(
        [(px2, F_cy), (px3, F_cy), (px3, pbot - 18), (px2, pbot)],
        fill="#ffffff",
        stroke="#000000",
        stroke_width=sw,
    )

    # Pulley wheel (occludes top of right side face; behind front post arm)
    s.circle(F_cx, F_cy, F_r, fill="#ffffff", stroke="#000000", stroke_width=sw)

    # Front face of post with rounded top cap (in front of pulley wheel)
    pw = px2 - px1
    d_post = (
        f"M {px1:.1f} {pbot:.1f} "
        f"L {px1:.1f} {ptop + pw * 0.5:.1f} "
        f"A {pw * 0.5:.1f} {pw * 0.5:.1f} 0 0 1 {px2:.1f} {ptop + pw * 0.5:.1f} "
        f"L {px2:.1f} {pbot:.1f} Z"
    )
    s.path(d_post, fill="#ffffff", stroke="#000000", stroke_width=sw)

    # Hanging string & weight P on pulley F
    s.line(F_cx + F_r - 2, F_cy, F_cx + F_r - 2, 446, stroke_width=sw)
    _pear_weight(s, F_cx + F_r - 2, 446, rx=31.0, h=92.0, sw=sw)

    # 6. Hand holding balance stem
    _draw_hand_fig14(s, sw=5.0)

    # 7. Labels
    labels = [
        ("F", 876, 76, 58),
        ("K", 378, 324, 56),
        ("L", 422, 382, 56),
        ("E", 506, 456, 56),
        ("H", 334, 502, 56),
        ("O", 498, 554, 54),
        ("D", 356, 628, 56),
        ("M", 78, 636, 54),
        ("P", 1106, 496, 56),
        ("B", 826, 602, 56),
        ("C", 534, 720, 56),
        ("G", 434, 764, 56),
        ("A", 214, 854, 58),
    ]
    for txt, x, y, sz in labels:
        lib.label(s, x, y, txt, size=sz, italic=False, bold=True)

    s.save(out_svg)
