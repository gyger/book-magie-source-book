"""Figure 28: Cavendish torsion balance — vertical cross-section / elevation of apparatus inside wooden room."""

from __future__ import annotations

from pathlib import Path
from PIL import Image

import draw
import library as lib


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    s = draw.Scene(w, h)

    # --- 1) Outer wooden building frame (walls & roof beam) ---
    # Thin top roof line
    s.line(206.0, 25.0, 2266.0, 34.0, stroke_width=6.0)
    # Main horizontal roof beam
    s.rect(206.0, 52.0, 2060.0, 92.0, fill="#000000", stroke="none")

    # Left vertical wall (with slanted window opening at y=1147..1226 and shelf slot at y=1254..1272)
    s.rect(206.0, 20.0, 132.0, 1234.0, fill="#000000", stroke="none")
    # Slanted window gap in left wall (both upper and lower edges sloped)
    s.polygon(
        [(204.0, 1147.0), (340.0, 1182.0), (340.0, 1226.0), (204.0, 1191.0)],
        fill="#ffffff",
        stroke="none",
    )
    s.rect(206.0, 1272.0, 132.0, 268.0, fill="#000000", stroke="none")

    # Right vertical wall (with slanted window opening and shelf slot)
    s.rect(2134.0, 32.0, 138.0, 1222.0, fill="#000000", stroke="none")
    s.polygon(
        [(2132.0, 1173.0), (2274.0, 1132.0), (2274.0, 1180.0), (2132.0, 1218.0)],
        fill="#ffffff",
        stroke="none",
    )
    s.rect(2134.0, 1272.0, 138.0, 268.0, fill="#000000", stroke="none")
    # White letters T and G on lower right post
    s.text(2202.0, 1322.0, "T", size=72.0, style="normal", weight="bold", fill="#ffffff")
    s.text(2202.0, 1456.0, "G", size=72.0, style="normal", weight="bold", fill="#ffffff")

    # --- 2) Left pulley m & hanging counterweight ---
    s.circle(162.0, 204.0, 42.0, fill="#000000", stroke="none")
    s.line(162.0, 166.0, 1020.0, 168.0, stroke_width=6.0)
    s.line(124.0, 204.0, 124.0, 410.0, stroke_width=5.5)
    s.circle(124.0, 410.0, 24.0, fill="#000000", stroke="none")

    # --- 3) Upper pulley M-M, truss P-r-r, and lead-sphere suspension rods ---
    # Central shaft through roof beam
    s.rect(1210.0, 48.0, 32.0, 164.0, fill="#000000", stroke="none")
    # Horizontal pulley disk M-M
    s.rect(1022.0, 150.0, 428.0, 38.0, fill="#000000", stroke="none")
    s.line(1022.0, 169.0, 1450.0, 169.0, stroke="#ffffff", stroke_width=4.0)

    # Triangular truss P -> r-r
    s.line(1226.0, 206.0, 864.0, 420.0, stroke_width=18.0)
    s.line(1226.0, 206.0, 1582.0, 420.0, stroke_width=18.0)
    # Horizontal beam r-r
    s.rect(860.0, 408.0, 728.0, 38.0, fill="#000000", stroke="none")

    # Vertical suspension rods from r-r down to large lead spheres W-W
    s.rect(860.0, 446.0, 22.0, 786.0, fill="#000000", stroke="none")
    s.circle(871.0, 484.0, 20.0, fill="#000000", stroke="none")
    s.rect(1580.0, 446.0, 22.0, 826.0, fill="#000000", stroke="none")
    s.circle(1591.0, 484.0, 20.0, fill="#000000", stroke="none")

    # --- 4) Torsion-wire adjustment shaft K ---
    # Horizontal shaft extends left to connect seamlessly with central top pin above F-F
    s.rect(1224.0, 524.0, 42.0, 14.0, fill="#000000", stroke="none")
    s.rect(1262.0, 524.0, 1020.0, 26.0, fill="#000000", stroke="none")
    # Small crank/handle K on outside of right wall
    s.path(
        "M 2266 458 C 2292 470, 2292 590, 2266 602",
        stroke="#000000",
        stroke_width=10.0,
    )
    s.line(2280.0, 531.0, 2318.0, 531.0, stroke_width=12.0)
    s.circle(2318.0, 531.0, 14.0, fill="#000000", stroke="none")

    # --- 5) Central torsion wire housing F-F-E-E and horizontal mahogany case A-A ---
    # Hatching pattern for double-walled wooden housing A-E-F
    s.add_def(
        '<pattern id="wood_hatch" width="11" height="11" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
        '<rect width="11" height="11" fill="#ffffff"/>'
        '<line x1="0" y1="0" x2="0" y2="11" stroke="#000000" stroke-width="2.6"/>'
        "</pattern>"
    )

    # Top finial pin, collar & cap at F-F (connected to horizontal shaft K)
    s.rect(1217.0, 500.0, 14.0, 44.0, fill="#000000", stroke="none")
    s.circle(1224.0, 504.0, 8.0, fill="#000000", stroke="none")
    s.rect(1208.0, 520.0, 34.0, 18.0, fill="#000000", stroke="none")
    s.rect(1196.0, 540.0, 58.0, 14.0, fill="#000000", stroke="none")

    # Double-walled hatched wooden housing: left wall A-E-F and right wall F-E-A
    s.polygon(
        [
            (638.0, 1245.0),
            (1152.0, 1165.0),
            (1197.0, 550.0),
            (1210.0, 550.0),
            (1166.0, 1177.0),
            (642.0, 1258.0),
        ],
        fill="url(#wood_hatch)",
        stroke="#000000",
        stroke_width=4.5,
    )
    s.polygon(
        [
            (1252.0, 550.0),
            (1292.0, 1165.0),
            (1796.0, 1245.0),
            (1792.0, 1258.0),
            (1278.0, 1177.0),
            (1239.0, 550.0),
        ],
        fill="url(#wood_hatch)",
        stroke="#000000",
        stroke_width=4.5,
    )

    # Central torsion wire l -> g -> m
    s.line(1224.0, 552.0, 1222.0, 1188.0, stroke_width=4.0)
    s.circle(1222.0, 1188.0, 12.0, fill="#ffffff", stroke="#000000", stroke_width=5.0)
    s.line(1222.0, 1200.0, 1222.0, 1272.0, stroke_width=4.0)

    # Interior torsion-arm suspension brace wires from g to ends of arm
    s.line(654.0, 1264.0, 1210.0, 1188.0, stroke_width=5.0)
    s.line(1780.0, 1264.0, 1234.0, 1188.0, stroke_width=5.0)

    # Horizontal torsion arm & bottom of mahogany box
    s.line(664.0, 1270.0, 1768.0, 1270.0, stroke_width=5.0)
    s.line(696.0, 1286.0, 1736.0, 1286.0, stroke_width=10.0)

    # Left & right end chambers (B, C, D, h)
    # Left chamber
    s.polyline([(638.0, 1254.0), (638.0, 1396.0), (696.0, 1396.0), (696.0, 1286.0)], stroke_width=8.0)
    s.line(666.0, 1270.0, 666.0, 1352.0, stroke_width=3.5)
    s.circle(666.0, 1352.0, 16.0, fill="#000000", stroke="none")
    # Right chamber
    s.polyline([(1736.0, 1286.0), (1736.0, 1396.0), (1794.0, 1396.0), (1794.0, 1254.0)], stroke_width=8.0)
    s.line(1766.0, 1270.0, 1766.0, 1352.0, stroke_width=3.5)
    s.circle(1766.0, 1352.0, 16.0, fill="#000000", stroke="none")

    # --- 6) Large lead spheres W-W ---
    # Left sphere W
    s.circle(852.0, 1344.0, 82.0, fill="#000000", stroke="none")
    s.circle(834.0, 1318.0, 14.0, fill="#ffffff", stroke="none")
    s.rect(844.0, 1424.0, 16.0, 22.0, fill="#000000", stroke="none")

    # Right sphere W
    s.circle(1590.0, 1348.0, 82.0, fill="#000000", stroke="none")
    s.circle(1572.0, 1322.0, 14.0, fill="#ffffff", stroke="none")
    s.rect(1582.0, 1428.0, 16.0, 22.0, fill="#000000", stroke="none")

    # --- 7) Support legs under ends of box (S) ---
    # Left leg
    s.rect(584.0, 1288.0, 60.0, 14.0, fill="#000000", stroke="none")
    s.rect(602.0, 1302.0, 30.0, 238.0, fill="#000000", stroke="none")
    # Right leg
    s.rect(1796.0, 1288.0, 60.0, 14.0, fill="#000000", stroke="none")
    s.rect(1816.0, 1302.0, 30.0, 238.0, fill="#000000", stroke="none")

    # --- 8) Left & right lamps/telescopes L and shelves ---
    # Left shelf
    s.line(34.0, 1254.0, 452.0, 1254.0, stroke_width=7.0)
    s.line(34.0, 1272.0, 452.0, 1272.0, stroke_width=5.0)
    # Left lamp L
    s.polygon(
        [(52.0, 1054.0), (190.0, 1084.0), (164.0, 1212.0), (26.0, 1182.0)],
        fill="#ffffff",
        stroke="#000000",
        stroke_width=7.0,
    )
    # Lamp lens tube
    s.polygon(
        [(182.0, 1138.0), (256.0, 1158.0), (248.0, 1190.0), (174.0, 1170.0)],
        fill="#ffffff",
        stroke="#000000",
        stroke_width=6.0,
    )
    # Lamp flame/wick inside
    s.path("M 66 1164 L 78 1094 C 86 1118, 92 1140, 82 1168 Z", fill="#000000", stroke="none")
    # Support wedge under lamp
    s.line(22.0, 1196.0, 206.0, 1236.0, stroke_width=10.0)

    # Right shelf
    s.line(2008.0, 1250.0, 2334.0, 1250.0, stroke_width=7.0)
    s.line(2008.0, 1270.0, 2334.0, 1270.0, stroke_width=5.0)
    # Right telescope/lamp tube passing through right wall
    s.polygon(
        [(2200.0, 1152.0), (2270.0, 1134.0), (2280.0, 1168.0), (2210.0, 1186.0)],
        fill="#ffffff",
        stroke="#000000",
        stroke_width=6.0,
    )
    s.line(2264.0, 1232.0, 2394.0, 1192.0, stroke_width=10.0)

    # --- 9) Labels ---
    lib.label(s, 68.0, 212.0, "m", size=64.0, italic=True, bold=True)
    lib.label(s, 974.0, 214.0, "M", size=66.0, italic=False, bold=True)
    lib.label(s, 1484.0, 212.0, "M", size=66.0, italic=False, bold=True)
    lib.label(s, 1226.0, 272.0, "P", size=66.0, italic=False, bold=True)

    lib.label(s, 818.0, 434.0, "r", size=64.0, italic=True, bold=True)
    lib.label(s, 1632.0, 434.0, "r", size=64.0, italic=True, bold=True)
    lib.label(s, 2365.0, 534.0, "K", size=68.0, italic=False, bold=True)

    lib.label(s, 1148.0, 578.0, "F", size=60.0, italic=False, bold=True)
    lib.label(s, 1284.0, 578.0, "F", size=60.0, italic=False, bold=True)
    lib.label(s, 1218.0, 642.0, "l", size=60.0, italic=True, bold=True)

    lib.label(s, 1114.0, 1142.0, "E", size=60.0, italic=False, bold=True)
    lib.label(s, 1312.0, 1142.0, "E", size=60.0, italic=False, bold=True)
    lib.label(s, 1172.0, 1226.0, "g", size=56.0, italic=True, bold=True)
    lib.label(s, 1264.0, 1244.0, "m", size=54.0, italic=True, bold=True)

    lib.label(s, 78.0, 1020.0, "L", size=66.0, italic=False, bold=True)
    lib.label(s, 2330.0, 1034.0, "L", size=66.0, italic=False, bold=True)

    lib.label(s, 636.0, 1206.0, "A", size=64.0, italic=False, bold=True)
    lib.label(s, 1804.0, 1206.0, "A", size=64.0, italic=False, bold=True)

    lib.label(s, 566.0, 1296.0, "S", size=56.0, italic=False, bold=True)
    lib.label(s, 564.0, 1364.0, "n", size=56.0, italic=True, bold=True)
    lib.label(s, 642.0, 1438.0, "B", size=58.0, italic=False, bold=True)
    lib.label(s, 704.0, 1438.0, "C", size=58.0, italic=False, bold=True)
    lib.label(s, 734.0, 1326.0, "D", size=56.0, italic=False, bold=True)
    lib.label(s, 746.0, 1384.0, "h", size=56.0, italic=True, bold=True)

    lib.label(s, 1876.0, 1296.0, "S", size=56.0, italic=False, bold=True)
    lib.label(s, 1876.0, 1364.0, "n", size=56.0, italic=True, bold=True)
    lib.label(s, 1734.0, 1438.0, "C", size=58.0, italic=False, bold=True)
    lib.label(s, 1794.0, 1438.0, "B", size=58.0, italic=False, bold=True)
    lib.label(s, 1702.0, 1326.0, "D", size=56.0, italic=False, bold=True)
    lib.label(s, 1696.0, 1384.0, "h", size=56.0, italic=True, bold=True)

    lib.label(s, 970.0, 1352.0, "W", size=66.0, italic=False, bold=True)
    lib.label(s, 1456.0, 1352.0, "W", size=66.0, italic=False, bold=True)
    lib.label(s, 852.0, 1496.0, "R", size=66.0, italic=False, bold=True)
    lib.label(s, 1582.0, 1496.0, "R", size=66.0, italic=False, bold=True)

    s.save(out_svg)
