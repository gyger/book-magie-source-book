"""CLI to build one or all figXX.svg figures and generate red/blue overlays."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from render import make_diagnostics

HERE = Path(__file__).resolve().parent
TYPST_DIR = HERE.parent
FIGS_DIR = TYPST_DIR / "figures"
SRC_FIGS_DIR = HERE / "figs"
OUT_COMPARE = HERE / "out" / "compare"


def build_one(name: str) -> None:
    py_path = SRC_FIGS_DIR / f"{name}.py"
    if not py_path.exists():
        raise FileNotFoundError(f"Missing generator script: {py_path}")
    src_png = FIGS_DIR / f"{name}.png"
    out_svg = FIGS_DIR / f"{name}.svg"

    spec = importlib.util.spec_from_file_location(name, py_path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.build(src_png, out_svg)

    if src_png.exists():
        stats = make_diagnostics(src_png, out_svg, OUT_COMPARE, name)
        print(f"[OK] {name}: SVG -> {out_svg.name} | IoU={stats['iou']:.3f} (scan={stats['scan_px']}, svg={stats['svg_px']})")
    else:
        print(f"[OK] {name}: SVG -> {out_svg.name} (no reference PNG)")


def main(argv: list[str]) -> int:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    targets = argv[1:] if len(argv) > 1 else sorted(p.stem for p in SRC_FIGS_DIR.glob("fig*.py"))
    if not targets:
        print("No figure scripts found in figs/.")
        return 0
    for name in targets:
        build_one(name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
