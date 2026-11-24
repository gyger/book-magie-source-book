"""Fig. 91, 4: Faraday's cylindrical bar magnet thrust into a hollow copper helix."""

from pathlib import Path
from PIL import Image
import draw


def build(src_png: Path, out_svg: Path) -> None:
    w, h = Image.open(src_png).size
    scene = draw.Scene(w, h)

    # Vertical connecting wires going up to galvanometer
    scene.line(52.0, 22.0, 48.0, 145.0, stroke_width=8.0)
    scene.line(418.0, 22.0, 420.0, 145.0, stroke_width=8.0)

    # Left short cylindrical collar protruding from the hollow helix
    scene.rect(24.0, 160.0, 28.0, 34.0, rx=5.0, fill="#ffffff", stroke="#000000", stroke_width=7.0)

    # Right short cylindrical collar protruding from the hollow helix
    scene.rect(414.0, 164.0, 30.0, 34.0, rx=5.0, fill="#ffffff", stroke="#000000", stroke_width=7.0)

    # Hollow helix cylinder body (rounded rectangle / tube)
    scene.rect(44.0, 136.0, 378.0, 76.0, rx=30.0, fill="#ffffff", stroke="#000000", stroke_width=8.0)

    # Subtle collar rim ellipse on the right collar where the magnet enters
    scene.ellipse(438.0, 181.0, 6.0, 17.0, fill="#ffffff", stroke="#000000", stroke_width=6.0)

    # Cylindrical bar magnet thrust into the right end of the helix
    scene.rect(438.0, 173.0, 330.0, 20.0, rx=7.0, fill="#ffffff", stroke="#000000", stroke_width=6.5)
    # Small circular/elliptical end-face detail at the right tip of the rod
    scene.ellipse(761.0, 183.0, 5.5, 9.5, fill="#ffffff", stroke="#000000", stroke_width=5.0)

    scene.save(out_svg)
