"""Figure 13: Stevinus's inclined plane apparatus with rectangular block and two pulleys."""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image

import draw
import library as lib


def _pear_weight(s: draw.Scene, cx: float, top_y: float, rx: float, h: float, sw: float = 5.5) -> None:
    """Draw a smooth teardrop/pear-shaped hanging weight suspended at (cx, top_y)."""
    bot_y = top_y + h
    mid_y = top_y + h * 0.62
    d = (
        f"M {cx:.1f} {top_y:.1f} "
        f"C {cx + rx * 0.45:.1f} {top_y + h * 0.18:.1f}, "
        f"{cx + rx * 1.05:.1f} {mid_y - h * 0.12:.1f}, "
        f"{cx + rx:.1f} {mid_y:.1f} "
        f"C {cx + rx * 0.98:.1f} {bot_y - h * 0.06:.1f}, "
        f"{cx + rx * 0.45:.1f} {bot_y:.1f}, "
        f"{cx:.1f} {bot_y:.1f} "
        f"C {cx - rx * 0.45:.1f} {bot_y:.1f}, "
        f"{cx - rx * 0.98:.1f} {bot_y - h * 0.06:.1f}, "
        f"{cx - rx:.1f} {mid_y:.1f} "
        f"C {cx - rx * 1.05:.1f} {mid_y - h * 0.12:.1f}, "
        f"{cx - rx * 0.45:.1f} {top_y + h * 0.18:.1f}, "
        f"{cx:.1f} {top_y:.1f} Z"
    )
    s.path(d, fill="#ffffff", stroke="#000000", stroke_width=sw)


def _pulley_stand(
    s: draw.Scene,
    cx: float,
    cy: float,
    r: float,
    post_x1: float,
    post_x2: float,
    post_x3: float,
    post_top_y: float,
    post_bot_y: float,
    base_x1: float,
    base_x2: float,
    base_y1: float,
    base_y2: float,
    bdx: float,
    bdy: float,
    sw: float = 5.5,
) -> None:
    """Draw a Stevinus pulley wheel, 3D vertical post, and 3D rectangular pedestal base."""
    # 3D pedestal base
    # Front face
    s.rect(base_x1, base_y1, base_x2 - base_x1, base_y2 - base_y1, fill="#ffffff", stroke="#000000", stroke_width=sw)
    # Top face
    top_pts = [
        (base_x1, base_y1),
        (base_x1 + bdx, base_y1 + bdy),
        (base_x2 + bdx, base_y1 + bdy),
        (base_x2, base_y1),
    ]
    s.polygon(top_pts, fill="#ffffff", stroke="#000000", stroke_width=sw)
    # Right face
    right_pts = [
        (base_x2, base_y1),
        (base_x2 + bdx, base_y1 + bdy),
        (base_x2 + bdx, base_y2 + bdy),
        (base_x2, base_y2),
    ]
    s.polygon(right_pts, fill="#ffffff", stroke="#000000", stroke_width=sw)

    # 3D vertical post — right side face (behind pulley wheel, occluded at rim)
    side_pts = [
        (post_x2, cy),
        (post_x3, cy),
        (post_x3, post_bot_y - 18.0),
        (post_x2, post_bot_y),
    ]
    s.polygon(side_pts, fill="#ffffff", stroke="#000000", stroke_width=sw)

    # Pulley wheel (occludes top of right side face; behind front post arm)
    s.circle(cx, cy, r, fill="#ffffff", stroke="#000000", stroke_width=sw)

    # Front face of post with rounded top cap (in front of pulley wheel)
    post_w = post_x2 - post_x1
    d_post = (
        f"M {post_x1:.1f} {post_bot_y:.1f} "
        f"L {post_x1:.1f} {post_top_y + post_w * 0.5:.1f} "
        f"A {post_w * 0.5:.1f} {post_w * 0.5:.1f} 0 0 1 {post_x2:.1f} {post_top_y + post_w * 0.5:.1f} "
        f"L {post_x2:.1f} {post_bot_y:.1f} Z"
    )
    s.path(d_post, fill="#ffffff", stroke="#000000", stroke_width=sw)


def _draw_hand_fig13(s: draw.Scene, sw: float = 5.0) -> None:
    """Clean vector reconstruction of the hand holding the balance stem in Fig. 13."""
    # Sleeve & cuff
    s.line(305, 36, 326, 108, stroke_width=sw)
    s.line(412, 26, 434, 82, stroke_width=sw)
    lib.smooth_curve(s, [(326, 108), (362, 98), (402, 86), (434, 82)], stroke_width=sw)
    # Left palm & thumb holding stem
    lib.smooth_curve(s, [(338, 105), (350, 148), (350, 192), (362, 210), (376, 232), (384, 235)], stroke_width=sw)
    # Thumb inner edge & fingers curling around stem
    lib.smooth_curve(s, [(370, 152), (372, 185), (379, 206), (384, 224)], stroke_width=sw)
    lib.smooth_curve(s, [(372, 158), (392, 182), (402, 204), (394, 234), (384, 258), (394, 262), (414, 235), (426, 208), (424, 180), (412, 168)], stroke_width=sw)
    # Middle finger
    lib.smooth_curve(s, [(416, 232), (432, 226), (442, 202), (438, 175), (428, 152)], stroke_width=sw)
    # Ring finger
    lib.smooth_curve(s, [(438, 212), (452, 202), (454, 176), (446, 148), (438, 140)], stroke_width=sw)
    # Back of hand / pinky
    lib.smooth_curve(s, [(418, 86), (436, 120), (454, 146), (464, 178), (456, 198)], stroke_width=sw)


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)
    sw = 5.5

    # 1. Inclined plane triangle A-B-C-N
    A = (392.1, 927.2)
    B = (768.6, 706.1)
    C = (764.7, 925.7)
    N = (895.8, 925.2)
    s.line(*A, *N, stroke_width=sw)
    s.line(*A, *B, stroke_width=sw)
    s.line(*B, *C, stroke_width=sw)
    s.line(*B, *N, stroke_width=sw)

    # 2. Rectangular block resting perpendicularly on AB
    dx_ab, dy_ab = B[0] - A[0], B[1] - A[1]
    L_ab = math.hypot(dx_ab, dy_ab)
    ux, uy = dx_ab / L_ab, dy_ab / L_ab       # along AB
    nx, ny = uy, -ux                          # outward normal (up-left)

    # Base center G on AB
    t_G = 0.625
    G = (A[0] + t_G * dx_ab, A[1] + t_G * dy_ab)
    half_w = 56.0
    blk_h = 352.0
    p_bl = (G[0] - half_w * ux, G[1] - half_w * uy)
    p_br = (G[0] + half_w * ux, G[1] + half_w * uy)
    p_tl = (p_bl[0] + blk_h * nx, p_bl[1] + blk_h * ny)
    p_tr = (p_br[0] + blk_h * nx, p_br[1] + blk_h * ny)
    H = (G[0] + blk_h * nx, G[1] + blk_h * ny)

    s.polygon([p_bl, p_br, p_tr, p_tl], fill="#ffffff", stroke="#000000", stroke_width=sw)
    s.line(*G, *H, stroke_width=sw)

    # Point D on centerline H-G at y = 618.4
    t_D = (618.4 - G[1]) / (H[1] - G[1])
    D = (G[0] + t_D * (H[0] - G[0]), 618.4)

    # 3. Balance beam, stem, strings, and weight M
    beam_y = 403.4
    x_M = 219.2
    x_stem = 381.6
    x_K = 530.5
    s.line(x_M, beam_y, x_K, beam_y, stroke_width=sw)
    s.line(x_stem, 240.0, x_stem, beam_y, stroke_width=sw)
    s.line(x_M, beam_y, x_M, 590.0, stroke_width=sw)
    s.line(x_K, beam_y, D[0], D[1], stroke_width=sw)
    _pear_weight(s, x_M, 590.0, rx=63.0, h=154.0, sw=sw)

    # 4. Strings from D to upper pulley F and lower pulley
    F_cx, F_cy, F_r = 1351.0, 225.0, 90.5
    LP_cx, LP_cy, LP_r = 1013.8, 686.0, 72.0

    # Tangent from D to top-left of upper pulley F
    ang_DF = math.atan2(F_cy - D[1], F_cx - D[0])
    dist_DF = math.hypot(F_cx - D[0], F_cy - D[1])
    alpha = math.asin(F_r / dist_DF)
    tang_ang = ang_DF - alpha - math.pi / 2.0
    F_tang = (F_cx + F_r * math.cos(tang_ang), F_cy + F_r * math.sin(tang_ang))
    s.line(D[0], D[1], F_tang[0], F_tang[1], stroke_width=sw)

    # Horizontal string from D to top of lower pulley
    s.line(D[0], D[1], LP_cx, LP_cy - LP_r, stroke_width=sw)

    # 5. Pulleys, stands, and hanging weights E & P
    # Lower pulley stand
    _pulley_stand(
        s, LP_cx, LP_cy, LP_r,
        post_x1=1014, post_x2=1036, post_x3=1058,
        post_top_y=672, post_bot_y=892,
        base_x1=916, base_x2=1128, base_y1=914, base_y2=1000,
        bdx=74, bdy=-68, sw=sw,
    )
    # Hanging string & weight P on lower pulley
    s.line(LP_cx + LP_r - 2, LP_cy, LP_cx + LP_r - 2, 764, stroke_width=sw)
    _pear_weight(s, LP_cx + LP_r - 2, 764, rx=20.0, h=62.0, sw=sw)

    # Upper pulley F stand
    _pulley_stand(
        s, F_cx, F_cy, F_r,
        post_x1=1340, post_x2=1374, post_x3=1398,
        post_top_y=214, post_bot_y=878,
        base_x1=1242, base_x2=1450, base_y1=904, base_y2=1000,
        bdx=82, bdy=-64, sw=sw,
    )
    # Hanging string & weight E on upper pulley
    s.line(F_cx + F_r - 2, F_cy, F_cx + F_r - 2, 480, stroke_width=sw)
    _pear_weight(s, F_cx + F_r - 2, 480, rx=31.0, h=90.0, sw=sw)

    # 6. Hand holding balance stem
    _draw_hand_fig13(s, sw=5.0)

    # 7. Labels
    labels = [
        ("F", 1280, 114, 62),
        ("K", 568, 400, 58),
        ("H", 412, 452, 58),
        ("L", 554, 495, 58),
        ("I", 574, 554, 56),
        ("D", 494, 624, 56),
        ("O", 568, 646, 52),
        ("M", 218, 678, 56),
        ("B", 765, 682, 56),
        ("E", 1514, 536, 58),
        ("P", 1138, 796, 54),
        ("G", 624, 818, 54),
        ("A", 402, 956, 58),
        ("C", 764, 956, 58),
        ("N", 878, 956, 58),
    ]
    for txt, x, y, sz in labels:
        lib.label(s, x, y, txt, size=sz, italic=False, bold=True)

    s.save(out_svg)
