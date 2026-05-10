
# build_and_inspect.py — Build model, screenshot, optionally call vision analysis
# Pipeline: 1. Run NX Open build script  2. Take screenshot  3. [Call vision.sh]
#
# Usage: python build_and_inspect.py <build_script.py> [--vision]
#   --vision : after screenshots, automatically call vision.sh for analysis
#
# Requires: NX running, PIL installed, vision.sh available (if --vision)

import subprocess, os, sys, time, glob
from PIL import ImageGrab

NX_PYTHON = "F:/anaconda/envs/opencv_test/python"
NX_BIN = "C:/Program Files/Siemens/NX2312/NXBIN"
VISION_SCRIPT = "G:/Test/vision.sh"
SCREENSHOT_DIR = None  # set from build script name


def run_build(build_script):
    """Execute NX Open build script."""
    env = os.environ.copy()
    env["PATH"] = f"{NX_BIN};{env.get('PATH', '')}"
    env["PYTHONPATH"] = f"{NX_BIN}/python"

    result = subprocess.run(
        [NX_PYTHON, build_script],
        capture_output=True, text=True, env=env, timeout=300
    )
    return result.returncode == 0, result.stdout, result.stderr


def take_screenshot(output_path):
    """Capture full screen."""
    img = ImageGrab.grab()
    img.save(output_path)
    return os.path.getsize(output_path)


def call_vision(image_path, model="claude-haiku-4-5"):
    """Call vision.sh to analyze screenshot."""
    result = subprocess.run(
        ["bash", VISION_SCRIPT, image_path, model],
        capture_output=True, text=True, timeout=60
    )
    return result.stdout


def main():
    global SCREENSHOT_DIR

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    build_script = sys.argv[1]
    use_vision = "--vision" in sys.argv

    if not os.path.exists(build_script):
        print(f"ERROR: Build script not found: {build_script}")
        sys.exit(1)

    # Setup screenshot directory (next to build script)
    script_dir = os.path.dirname(os.path.abspath(build_script)) or "."
    SCREENSHOT_DIR = os.path.join(script_dir, "_screenshots")
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(build_script))[0]
    timestamp = time.strftime("%H%M%S")

    print("=" * 60)
    print(f"Pipeline: {base_name}")
    print(f"Screenshots: {SCREENSHOT_DIR}")
    print("=" * 60)

    # Step 1: Build
    print("\n[1/3] Building model...")
    success, stdout, stderr = run_build(build_script)
    print(stdout[-500:] if len(stdout) > 500 else stdout)
    if stderr:
        print("STDERR:", stderr[-300:])
    if not success:
        print("BUILD FAILED — skipping screenshots")
        sys.exit(1)

    # Step 2: Screenshot
    print("\n[2/3] Taking screenshot...")
    shot_path = os.path.join(SCREENSHOT_DIR, f"{base_name}_{timestamp}.png")
    size = take_screenshot(shot_path)
    print(f"  Saved: {shot_path} ({size:,} bytes)")

    # Step 3: Vision analysis (optional)
    if use_vision:
        print("\n[3/3] Vision analysis...")
        analysis = call_vision(shot_path)
        print(analysis[:1500])

        # Save analysis alongside screenshot
        analysis_path = shot_path.replace(".png", "_analysis.txt")
        with open(analysis_path, "w", encoding="utf-8") as f:
            f.write(analysis)
        print(f"  Analysis saved: {analysis_path}")
    else:
        print("\n[3/3] Vision skipped (add --vision to enable)")

    print(f"\nPipeline complete. Screenshot: {shot_path}")


if __name__ == "__main__":
    main()
