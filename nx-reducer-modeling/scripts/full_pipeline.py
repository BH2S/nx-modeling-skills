
# full_pipeline.py — End-to-end: build → STL export → render → vision analysis
# Fully automated. NX must be running but does NOT need to be visible.
#
# Usage: python full_pipeline.py <build_script.py> [--vision]
#   --vision : after rendering, call vision.sh for automated analysis

import subprocess, os, sys, time, struct
import numpy as np

NX_PYTHON = "F:/anaconda/envs/opencv_test/python"
NX_BIN = "C:/Program Files/Siemens/NX2312/NXBIN"
VISION_SCRIPT = "G:/Test/vision.sh"

# STL export function (runs INSIDE NX Open context)
STL_EXPORTER = """
import NXOpen, NXOpen.UF as UF, os
s = NXOpen.Session.GetSession()
uf = UF.UFSession.GetUFSession()
wp = s.Parts.Work
if not wp:
    print('ERROR: No work part')
else:
    bodies = [b for b in wp.Bodies]
    if not bodies:
        print('ERROR: No bodies in work part')
    else:
        body = bodies[0]
        out = r'{stl_path}'
        fh = uf.Std.OpenBinaryStlFile(out, False, 'Pipeline STL Export')
        uf.Std.PutSolidInStlFile(fh, 0, body.Tag, 0.0, 0.0, 0.01)
        uf.Std.CloseStlFile(fh)
        if os.path.exists(out):
            print(f'STL_OK: {{os.path.getsize(out)}} bytes')
        else:
            print('STL_FAIL: file not created')
"""


def run_build_and_export_stl(build_script, stl_path):
    """1. Run build script  2. Export STL from NX"""
    env = os.environ.copy()
    env["PATH"] = f"{NX_BIN};{env.get('PATH', '')}"
    env["PYTHONPATH"] = f"{NX_BIN}/python"

    # Step 1: Build
    print("[1/4] Building model...")
    result = subprocess.run(
        [NX_PYTHON, build_script],
        capture_output=True, text=True, env=env, timeout=300
    )
    print(result.stdout[-300:] if len(result.stdout) > 300 else result.stdout)
    if result.returncode != 0:
        print(f"BUILD FAILED:\n{result.stderr[-500:]}")
        return False

    # Step 2: Export STL (run as inline script)
    print(f"\n[2/4] Exporting STL to {stl_path}...")
    exporter = STL_EXPORTER.replace('{stl_path}', stl_path.replace('\\', '\\\\'))
    result = subprocess.run(
        [NX_PYTHON, "-c", exporter],
        capture_output=True, text=True, env=env, timeout=30
    )
    print(result.stdout.strip())
    if "STL_OK" not in result.stdout:
        print(f"STL EXPORT FAILED:\n{result.stderr[-300:]}")
        return False

    return os.path.exists(stl_path) and os.path.getsize(stl_path) > 100


def render_stl(stl_path, output_dir):
    """3. Render STL to 4-view PNG using matplotlib."""
    print(f"\n[3/4] Rendering {stl_path}...")

    # Parse binary STL
    verts = []
    with open(stl_path, 'rb') as f:
        f.read(80)
        n = int.from_bytes(f.read(4), 'little')
        for _ in range(n):
            f.read(12)
            for _ in range(3):
                verts.append([
                    struct.unpack('f', f.read(4))[0],
                    struct.unpack('f', f.read(4))[0],
                    struct.unpack('f', f.read(4))[0],
                ])
            f.read(2)
    verts = np.array(verts)
    center = (verts.max(axis=0) + verts.min(axis=0)) / 2
    verts = verts - center
    print(f"  {len(verts)} vertices, {n} triangles")

    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    views = [("iso", 30, -60), ("front", 0, -90), ("top", 90, 0), ("side", 0, 0)]
    fig = plt.figure(figsize=(16, 12))
    for i, (name, elev, azim) in enumerate(views):
        ax = fig.add_subplot(2, 2, i+1, projection='3d')
        ax.scatter(verts[::10, 0], verts[::10, 1], verts[::10, 2],
                   s=0.3, c='steelblue', alpha=0.5)
        ax.set_title(name.upper())
        ax.view_init(elev=elev, azim=azim)
        ax.axis('off')

    os.makedirs(output_dir, exist_ok=True)
    png_path = os.path.join(output_dir, "render_4views.png")
    plt.savefig(png_path, dpi=100)
    plt.close()
    print(f"  Saved: {png_path} ({os.path.getsize(png_path):,} bytes)")
    return png_path


def vision_analyze(png_path):
    """4. Run vision.sh on the rendered image."""
    print(f"\n[4/4] Vision analysis...")
    result = subprocess.run(
        ["bash", VISION_SCRIPT, png_path],
        capture_output=True, text=True, timeout=60
    )
    analysis = result.stdout

    # Save analysis
    analysis_path = png_path.replace(".png", "_analysis.txt")
    with open(analysis_path, "w", encoding="utf-8") as f:
        f.write(analysis)
    print(f"  Analysis saved: {analysis_path}")
    print(analysis[:1000])


def main():
    if len(sys.argv) < 2:
        print("Usage: python full_pipeline.py <build_script.py> [--vision]")
        sys.exit(1)

    build_script = sys.argv[1]
    use_vision = "--vision" in sys.argv

    if not os.path.exists(build_script):
        print(f"ERROR: Script not found: {build_script}")
        sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(build_script)) or "."
    out_dir = os.path.join(script_dir, "_pipeline_output")
    stl_path = os.path.join(out_dir, "model.stl")
    os.makedirs(out_dir, exist_ok=True)

    print("=" * 60)
    print(f"FULL PIPELINE: {os.path.basename(build_script)}")
    print("=" * 60)

    if not run_build_and_export_stl(build_script, stl_path):
        print("\nPIPELINE ABORTED — build or STL export failed")
        sys.exit(1)

    png_path = render_stl(stl_path, out_dir)

    if use_vision:
        vision_analyze(png_path)

    print(f"\nPipeline complete. Output: {out_dir}/")
    print(f"  STL: {stl_path}")
    print(f"  PNG: {png_path}")


if __name__ == "__main__":
    main()
