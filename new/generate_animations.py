#!/usr/bin/env python3
"""
Generátor rotujících GIF animací pro každý krok tutoriálu Platónských těles.
Generating rotating GIF animations for each step of the Platonic solids tutorial.

Uložení / Output:
    Soubory se uloží do složky new/animations/
    Files are saved to the new/animations/ folder.

Instalace závislostí / Install dependencies:
    pip install kaleido imageio Pillow

Spuštění / Usage:
    cd new/
    python generate_animations.py

    Volitelné argumenty / Optional arguments:
    python generate_animations.py --frames 36 --fps 12 --size 600
    python generate_animations.py --steps 5              # pouze krok 5 / only step 5
    python generate_animations.py --steps 1-5            # kroky 1-5 / steps 1-5
    python generate_animations.py --steps 1,3,5          # kroky 1,3,5 / steps 1,3,5
    python generate_animations.py --steps 1-3,7,10-12    # kombinace / combination
"""

import sys
import os
import math
import io
import argparse
from pathlib import Path
from unittest.mock import MagicMock

# ── 1. Mock streamlit BEFORE any step imports ─────────────────────────────────
# Step modules call st.session_state inside render_plotly_diagram(), so we
# substitute a plain dict-like object that satisfies all .get() and attribute
# accesses without starting a real Streamlit server.

class _MockSessionState(dict):
    """Minimal stand-in for st.session_state."""

    def get(self, key, default=None):
        return super().get(key, default)

    def __getattr__(self, key):
        return self.get(key)

    def __setattr__(self, key, value):
        self[key] = value

    def __contains__(self, key):
        return dict.__contains__(self, key)


_mock_st = MagicMock()
_mock_st.session_state = _MockSessionState({
    'show_faces':    True,
    'face_opacity':  0.3,
    'face_color':    '#00CED1',
    'edge_width':    3,
    'vertex_size':   12,
})
sys.modules['streamlit'] = _mock_st

# ── 2. Set up Python path so step modules resolve correctly ───────────────────
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

# ── 3. Import all step classes ────────────────────────────────────────────────
from steps.definitions.tetrahedron import (
    TetraStep1_Cube, TetraStep2_Selection, TetraStep3_Complete,
)
from steps.definitions.octahedron import (
    OctaStep1_Axes, OctaStep2_Complete,
)
from steps.definitions.icosahedron import (
    IcosaStep1_Rectangle, IcosaStep2_ThreeRectangles, IcosaStep3_Complete,
)
from steps.definitions.dodecahedron import (
    DodecaStep1_Cube, DodecaStep2_GoldenRectangles, DodecaStep3_Complete,
)
from steps.definitions.duality_cube_octahedron    import DualityCubeOctahedron
from steps.definitions.duality_nested_octahedra   import DualityNestedOctahedra
from steps.definitions.duality_icosahedron_dodecahedron import DualityIcosahedronDodecahedron
from steps.definitions.duality_tetrahedron_self    import DualityTetrahedronSelf
from steps.definitions.bonus          import BonusStep_TriangleCenter
from steps.definitions.bonus_why_five import BonusStep_WhyOnlyFive

# ── 4. Helpers ────────────────────────────────────────────────────────────────

def _camera_eye(azimuth_deg: float, elevation_deg: float = 25.0, radius: float = 2.5) -> dict:
    """
    Convert spherical camera coordinates to Plotly eye dict.

    Plotly's 3D camera uses Cartesian eye coordinates. We orbit the solid
    by varying the azimuth while keeping elevation fixed.

    Args:
        azimuth_deg:   Horizontal angle in degrees (0 → 360).
        elevation_deg: Vertical angle above the XY plane (degrees).
        radius:        Camera distance from origin.
    """
    theta = math.radians(azimuth_deg)
    phi   = math.radians(elevation_deg)
    return dict(
        x=radius * math.cos(phi) * math.cos(theta),
        y=radius * math.cos(phi) * math.sin(theta),
        z=radius * math.sin(phi),
    )


def _is_3d_figure(fig) -> bool:
    """Return True if the figure contains any 3D traces."""
    _3d_types = {'scatter3d', 'mesh3d', 'cone', 'streamtube', 'isosurface', 'volume'}
    return any(getattr(t, 'type', '') in _3d_types for t in fig.data)


def _ascii_filename(text: str) -> str:
    """Replace Czech diacritics and spaces with ASCII equivalents."""
    replacements = {
        'á': 'a', 'č': 'c', 'ď': 'd', 'é': 'e', 'ě': 'e', 'í': 'i',
        'ň': 'n', 'ó': 'o', 'ř': 'r', 'š': 's', 'ť': 't', 'ú': 'u',
        'ů': 'u', 'ý': 'y', 'ž': 'z',
        'Á': 'A', 'Č': 'C', 'Ď': 'D', 'É': 'E', 'Ě': 'E', 'Í': 'I',
        'Ň': 'N', 'Ó': 'O', 'Ř': 'R', 'Š': 'S', 'Ť': 'T', 'Ú': 'U',
        'Ů': 'U', 'Ý': 'Y', 'Ž': 'Z',
        ' ': '_',
    }
    return ''.join(replacements.get(c, c) for c in text)


def save_rotating_gif(fig, output_path: Path, n_frames: int, fps: int,
                      size: int, elevation: float) -> None:
    """
    Rotate Plotly 3D figure 360° around the vertical axis and save as GIF.

    Each frame is rendered to PNG via Kaleido, then all frames are stitched
    into an animated GIF using Pillow (smaller, more compatible than imageio
    for palette-based animation).

    Args:
        fig:         Plotly Figure with a 3D scene.
        output_path: Destination .gif file.
        n_frames:    Number of rotation frames.
        fps:         Frames per second in the output GIF.
        size:        Pixel width and height of each frame.
        elevation:   Camera elevation angle in degrees.
    """
    from PIL import Image

    output_path.parent.mkdir(parents=True, exist_ok=True)
    frames = []

    for i in range(n_frames):
        azimuth = i * 360.0 / n_frames
        fig.update_layout(
            scene_camera=dict(
                eye=_camera_eye(azimuth, elevation),
                up=dict(x=0, y=0, z=1),
            )
        )
        png_bytes = fig.to_image(format='png', width=size, height=size, scale=1)
        img = Image.open(io.BytesIO(png_bytes)).convert('RGBA')

        # Convert to palette mode for compact GIF
        img_p = img.convert('P', palette=Image.ADAPTIVE, colors=128)
        frames.append(img_p)

        print(f"    frame {i + 1:>3}/{n_frames}", end='\r', flush=True)

    print()  # newline

    duration_ms = max(1, round(1000 / fps))
    frames[0].save(
        str(output_path),
        save_all=True,
        append_images=frames[1:],
        optimize=True,
        duration=duration_ms,
        loop=0,          # loop forever
    )


def save_static_gif(fig, output_path: Path, size_w: int, size_h: int) -> None:
    """
    Export a 2D Plotly figure as a two-frame GIF (static, always compatible).

    Args:
        fig:        Plotly Figure (2D).
        output_path: Destination .gif file.
        size_w:     Width in pixels.
        size_h:     Height in pixels.
    """
    from PIL import Image

    output_path.parent.mkdir(parents=True, exist_ok=True)

    png_bytes = fig.to_image(format='png', width=size_w, height=size_h, scale=1)
    img = Image.open(io.BytesIO(png_bytes)).convert('RGBA').convert('P', palette=Image.ADAPTIVE, colors=128)

    img.save(
        str(output_path),
        save_all=True,
        append_images=[img],   # 2 identical frames → valid animated GIF
        optimize=True,
        duration=2000,
        loop=0,
    )


# ── 5. Main ───────────────────────────────────────────────────────────────────

ALL_STEPS = [
    TetraStep1_Cube(),
    TetraStep2_Selection(),
    TetraStep3_Complete(),
    OctaStep1_Axes(),
    OctaStep2_Complete(),
    IcosaStep1_Rectangle(),
    IcosaStep2_ThreeRectangles(),
    IcosaStep3_Complete(),
    DodecaStep1_Cube(),
    DodecaStep2_GoldenRectangles(),
    DodecaStep3_Complete(),
    DualityCubeOctahedron(),
    DualityNestedOctahedra(),
    DualityIcosahedronDodecahedron(),
    DualityTetrahedronSelf(),
    BonusStep_TriangleCenter(),
    BonusStep_WhyOnlyFive(),
]


def parse_steps_arg(steps_str: str) -> set:
    """
    Parse step specification into a set of step numbers.

    Accepts:
      - Single number:     "5"           → {5}
      - Range:             "1-5"         → {1, 2, 3, 4, 5}
      - Comma-separated:   "1,3,5"       → {1, 3, 5}
      - Combination:       "1-3,7,10-12" → {1, 2, 3, 7, 10, 11, 12}

    Returns:
        Set of step numbers (integers).
    """
    result = set()
    parts = steps_str.split(',')

    for part in parts:
        part = part.strip()
        if '-' in part:
            # Range: "5-10"
            start_str, end_str = part.split('-', 1)
            start, end = int(start_str.strip()), int(end_str.strip())
            result.update(range(start, end + 1))
        else:
            # Single number: "5"
            result.add(int(part))

    return result


def main():
    parser = argparse.ArgumentParser(
        description='Generate rotating GIF animations for the Platonic solids tutorial.'
    )
    parser.add_argument('--frames',    type=int,   default=60,
                        help='Number of rotation frames per GIF (default: 60)')
    parser.add_argument('--fps',       type=int,   default=15,
                        help='Frames per second in output GIF (default: 15)')
    parser.add_argument('--size',      type=int,   default=700,
                        help='Pixel size (width=height) for 3D renders (default: 700)')
    parser.add_argument('--elevation', type=float, default=25.0,
                        help='Camera elevation angle in degrees (default: 25)')
    parser.add_argument('--outdir',    type=str,   default='animations',
                        help='Output folder (default: animations/)')
    parser.add_argument('--steps',     type=str,   default=None,
                        help='Specific step(s) to generate (e.g., "5", "1-5", "1,3,5", "1-3,7-9")')
    args = parser.parse_args()

    output_dir = _HERE / args.outdir
    output_dir.mkdir(exist_ok=True)

    # Filter steps if --steps is specified
    if args.steps:
        try:
            step_numbers = parse_steps_arg(args.steps)
        except ValueError as e:
            print(f"Error parsing --steps argument: {e}")
            sys.exit(1)

        steps_to_generate = [s for s in ALL_STEPS if s.get_metadata().number in step_numbers]

        if not steps_to_generate:
            available = sorted(s.get_metadata().number for s in ALL_STEPS)
            print(f"No steps found matching: {args.steps}")
            print(f"Available steps: {available}")
            sys.exit(1)

        step_nums_str = ', '.join(str(n) for n in sorted(step_numbers))
        filter_info = f"  filtering: steps {step_nums_str}"
    else:
        steps_to_generate = ALL_STEPS
        filter_info = f"  generating: all {len(ALL_STEPS)} steps"

    print(f"\n{'='*60}")
    print(f"  Platonic Solids – GIF Animation Generator")
    print(f"  frames={args.frames}  fps={args.fps}  size={args.size}px")
    print(filter_info)
    print(f"  output → {output_dir}")
    print(f"{'='*60}\n")

    succeeded, failed = [], []

    for step in steps_to_generate:
        meta  = step.get_metadata()
        label = f"[{meta.number:>2}] {meta.title}"
        safe  = f"step_{meta.number:02d}_{_ascii_filename(meta.category)}"
        out   = output_dir / f"{safe}.gif"

        print(f"{label}")
        print(f"  → {out.name}")

        try:
            fig = step.render_plotly_diagram()

            if _is_3d_figure(fig):
                save_rotating_gif(
                    fig, out,
                    n_frames=args.frames,
                    fps=args.fps,
                    size=args.size,
                    elevation=args.elevation,
                )
            else:
                save_static_gif(fig, out, size_w=1000, size_h=700)

            size_kb = out.stat().st_size // 1024
            print(f"  ✓ saved ({size_kb} KB)\n")
            succeeded.append((meta.number, meta.title, str(out.relative_to(_HERE))))

        except Exception as exc:
            import traceback
            print(f"  ✗ ERROR: {exc}")
            traceback.print_exc()
            failed.append((meta.number, meta.title, str(exc)))
            print()

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"{'='*60}")
    print(f"  Done: {len(succeeded)} OK  |  {len(failed)} failed")
    if failed:
        print("\nFailed steps:")
        for num, title, err in failed:
            print(f"  [{num}] {title}: {err}")

    # Write metadata JSON for create_google_slides.py
    import json
    meta_path = output_dir / '_metadata.json'
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(succeeded, f, ensure_ascii=False, indent=2)
    print(f"\nMetadata saved → {meta_path.relative_to(_HERE)}")
    print(f"{'='*60}\n")
    print("Next step: run  python create_google_slides.py\n")


if __name__ == '__main__':
    main()
