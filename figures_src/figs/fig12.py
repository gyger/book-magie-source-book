"""Figure 12: Stevinus's inclined plane with hand-held balance, weight M, block HG, pulley F, and weight E."""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    scene = draw.Scene(w, h)

    sw = 7.5
    sw_hand = 7.0

    # --- 1. Inclined plane triangle ABC ---
    ax, ay = 248.0, 926.5
    cx, cy = 1047.5, 926.5
    bx, by = 1047.5, 458.0
    scene.polygon([(ax, ay), (bx, by), (cx, cy)], stroke_width=sw)

    # --- 2. Tilted rectangular prism HG resting on AB ---
    # Four corners measured from zoomed grid
    bl = (428.0, 818.0)
    br = (540.0, 754.0)
    tl = (248.0, 492.0)
    tr = (358.0, 428.0)
    scene.polygon([bl, br, tr, tl], stroke_width=sw)
    # Centerline H-G
    hx, hy = 0.5 * (tl[0] + tr[0]), 0.5 * (tl[1] + tr[1])
    gx, gy = 0.5 * (bl[0] + br[0]), 0.5 * (bl[1] + br[1])
    scene.line(hx, hy, gx, gy, stroke_width=sw)

    # --- 3. Balance beam, stem, cords, and weight M ---
    y_beam = 393.5
    x_left = 77.5
    x_mid = 243.5
    x_right = 393.5
    y_d = 616.0

    # Horizontal beam
    scene.line(x_left, y_beam, x_right, y_beam, stroke_width=sw)
    # Central vertical stem up into hand
    scene.line(x_mid, y_beam, x_mid, 122.0, stroke_width=9.5)
    # Left cord down to weight M
    scene.line(x_left, y_beam, x_left, 578.0, stroke_width=sw)
    # Right cord K-L-D down to point D on block centerline
    scene.line(x_right, y_beam, x_right, y_d, stroke_width=sw)

    # Pear-shaped hanging weight M
    m_path = (
        "M 77.5 578 "
        "C 102 586, 130 634, 130 682 "
        "C 130 726, 108 750, 77.5 750 "
        "C 47 750, 26 726, 26 682 "
        "C 26 634, 53 586, 77.5 578 Z"
    )
    scene.path(m_path, fill="#ffffff", stroke="#000000", stroke_width=sw)

    # --- 4. Hand holding balance stem (clean Bezier curves matching scan silhouette) ---
    # Cuff / wrist line
    lib.smooth_curve(
        scene,
        [(194, 34), (190, 56), (202, 72), (218, 62), (246, 72), (282, 75), (312, 66), (328, 46), (336, 26)],
        stroke_width=sw_hand,
    )
    # Outer left contour (back of hand + pinky)
    lib.smooth_curve(
        scene,
        [(202, 72), (192, 94), (174, 118), (168, 148), (170, 170), (180, 176)],
        stroke_width=sw_hand,
    )
    # Finger 1 / 2 crease (pinky/ring)
    lib.smooth_curve(
        scene,
        [(186, 118), (180, 148), (182, 182), (194, 196), (202, 198)],
        stroke_width=sw_hand,
    )
    # Finger 2 / 3 crease (ring/middle)
    lib.smooth_curve(
        scene,
        [(200, 132), (198, 166), (200, 196), (212, 206), (222, 208)],
        stroke_width=sw_hand,
    )
    # Finger 3 / 4 crease (middle/index) curving down to stem
    lib.smooth_curve(
        scene,
        [(218, 140), (214, 174), (218, 208), (228, 220), (240, 226)],
        stroke_width=sw_hand,
    )
    # Index inner edge along stem
    lib.smooth_curve(
        scene,
        [(238, 152), (233, 182), (236, 206)],
        stroke_width=sw_hand,
    )
    # Thumb outer right contour from wrist down to stem
    lib.smooth_curve(
        scene,
        [(282, 75), (282, 114), (282, 154), (274, 184), (260, 204), (248, 206)],
        stroke_width=sw_hand,
    )
    # Thumb inner crease
    lib.smooth_curve(
        scene,
        [(268, 134), (258, 158), (252, 188), (248, 204)],
        stroke_width=sw_hand,
    )
    # Small palm crease between stem and thumb
    lib.smooth_curve(
        scene,
        [(246, 130), (256, 144), (262, 150)],
        stroke_width=sw_hand,
    )

    # --- 5. Pulley F, post, base block, cord D-I-F, and weight E ---
    px, py, pr = 1228.0, 240.0, 90.0

    # Cord from D=(393.5, 616) tangent to top-left of pulley F
    dx_pf, dy_pf = px - x_right, py - y_d
    dist_pf = math.hypot(dx_pf, dy_pf)
    # Angle of tangent point on upper side of pulley
    base_ang = math.atan2(dy_pf, dx_pf)
    # Tangent offset angle: sin(alpha) = pr / dist_pf
    alpha = math.asin(pr / dist_pf)
    tang_ang = base_ang - math.pi / 2.0 - alpha
    tx = px + pr * math.cos(tang_ang)
    ty = py + pr * math.sin(tang_ang)
    scene.line(x_right, y_d, tx, ty, stroke_width=sw)

    # Vertical cord from right edge of pulley F down to weight E
    ex_line = 1312.5
    scene.line(ex_line, py, ex_line, 476.0, stroke_width=sw)

    # Small pear-shaped weight E
    e_path = (
        f"M {ex_line:.1f} 476 "
        "C 1326 488, 1340 524, 1338 552 "
        "C 1336 570, 1326 578, 1314 578 "
        "C 1302 578, 1294 568, 1294 550 "
        "C 1294 522, 1304 488, 1312.5 476 Z"
    )
    scene.path(e_path, fill="#ffffff", stroke="#000000", stroke_width=sw)

    # Pulley wheel (circle) drawn before post so post overlays axle cleanly
    scene.circle(px, py, pr, fill="#ffffff", stroke="#000000", stroke_width=sw)

    # Base block (isometric rectangular plinth at bottom right)
    scene.polygon(
        [(1111.0, 914.0), (1192.0, 846.0), (1420.0, 846.0), (1336.0, 914.0)],
        fill="#ffffff",
        stroke="#000000",
        stroke_width=sw,
    )
    scene.polygon(
        [(1111.0, 914.0), (1336.0, 914.0), (1336.0, 976.0), (1111.0, 976.0)],
        fill="#ffffff",
        stroke="#000000",
        stroke_width=sw,
    )
    scene.polygon(
        [(1336.0, 914.0), (1420.0, 846.0), (1420.0, 916.0), (1336.0, 976.0)],
        fill="#ffffff",
        stroke="#000000",
        stroke_width=sw,
    )

    # Vertical post supporting pulley axle (drawn on top of pulley and base top)
    scene.polygon(
        [(1206.5, 228.0), (1248.0, 228.0), (1260.0, 882.0), (1206.5, 882.0)],
        fill="#ffffff",
        stroke="#000000",
        stroke_width=sw,
    )
    # Vertical rib line on post
    scene.line(1238.5, 236.0, 1238.5, 882.0, stroke_width=5.5)
    # Axle pin
    scene.circle(px, py, 10.0, fill="#ffffff", stroke="#000000", stroke_width=6.0)

    # --- 6. Labels ---
    lib.label(scene, 76, 668, "M", size=54, italic=False, bold=True)
    lib.label(scene, 268, 444, "H", size=54, italic=False, bold=True)
    lib.label(scene, 422, 378, "K", size=54, italic=False, bold=True)
    lib.label(scene, 424, 466, "L", size=54, italic=False, bold=True)
    lib.label(scene, 474, 594, "I", size=54, italic=False, bold=True)
    lib.label(scene, 368, 636, "D", size=54, italic=False, bold=True)
    lib.label(scene, 488, 822, "G", size=54, italic=False, bold=True)
    lib.label(scene, 248, 956, "A", size=54, italic=False, bold=True)
    lib.label(scene, 1044, 422, "B", size=54, italic=False, bold=True)
    lib.label(scene, 1044, 956, "C", size=54, italic=False, bold=True)
    lib.label(scene, 1152, 116, "F", size=54, italic=False, bold=True)
    lib.label(scene, 1368, 536, "E", size=54, italic=False, bold=True)

    scene.save(out_svg)
