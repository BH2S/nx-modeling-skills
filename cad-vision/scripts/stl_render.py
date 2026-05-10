
# stl_render.py — Render STL to PNG from multiple angles (no NX needed)
# Usage: python stl_render.py <input.stl> [output_dir]

import sys, os, math, struct
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def load_stl_vertices(stl_path):
    """Parse binary STL and extract vertices."""
    with open(stl_path, 'rb') as f:
        f.read(80)  # header
        n_triangles = int.from_bytes(f.read(4), 'little')
        verts = []
        for _ in range(n_triangles):
            f.read(12)  # normal
            for _ in range(3):
                x = struct.unpack('f', f.read(4))[0]
                y = struct.unpack('f', f.read(4))[0]
                z = struct.unpack('f', f.read(4))[0]
                verts.append([x, y, z])
            f.read(2)  # attribute
    return np.array(verts)


def render_views(stl_path, output_dir=None, prefix="view"):
    """Render STL from 4 angles: isometric, front, top, side."""
    verts = load_stl_vertices(stl_path)

    if output_dir is None:
        output_dir = os.path.dirname(stl_path) or "."
    os.makedirs(output_dir, exist_ok=True)

    # Normalize to center
    center = (verts.max(axis=0) + verts.min(axis=0)) / 2
    verts = verts - center

    views = [
        ("iso", 30, -60),     # isometric
        ("front", 0, -90),     # front (looking along Y)
        ("top", 90, 0),       # top (looking down Z)
        ("side", 0, 0),       # side (looking along X)
    ]

    paths = []
    fig = plt.figure(figsize=(16, 12))

    for i, (name, elev, azim) in enumerate(views):
        ax = fig.add_subplot(2, 2, i+1, projection='3d')
        ax.scatter(verts[::5, 0], verts[::5, 1], verts[::5, 2],
                   s=0.5, c='steelblue', alpha=0.6)
        ax.set_title(name.upper(), fontsize=14)
        ax.view_init(elev=elev, azim=azim)
        ax.set_box_aspect([1, 1, 1])
        ax.axis('off')

    plt.tight_layout()
    out_path = os.path.join(output_dir, f"{prefix}_4views.png")
    plt.savefig(out_path, dpi=100)
    plt.close()
    paths.append(out_path)
    print(f"4-view render: {out_path}")

    return paths


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python stl_render.py <input.stl> [output_dir]")
        sys.exit(1)

    stl_path = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(stl_path):
        print(f"STL not found: {stl_path}")
        sys.exit(1)

    paths = render_views(stl_path, out_dir)
    for p in paths:
        print(p)
