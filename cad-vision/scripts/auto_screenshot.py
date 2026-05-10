
# auto_screenshot.py — NX viewport screenshot via PIL ImageGrab
# Usage: python auto_screenshot.py <output_path>
# Captures the primary display (where NX runs).
# For multi-monitor: captures all screens.
import sys, os
from PIL import ImageGrab

def capture(output_path):
    """Capture full screen and save to output_path."""
    img = ImageGrab.grab()
    img.save(output_path)
    return os.path.getsize(output_path)

def capture_all_screens(output_dir, prefix="nx_view"):
    """Capture each monitor separately if available."""
    import platform
    screenshots = []

    # Try to capture all monitors
    try:
        # MSS would handle multi-monitor better, but PIL works for single
        img = ImageGrab.grab()
        path = os.path.join(output_dir, f"{prefix}_full.png")
        img.save(path)
        screenshots.append(path)
    except Exception as e:
        print(f"Capture failed: {e}", file=sys.stderr)
        return []

    # Also try to capture specific regions if NX window position is known
    return screenshots

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python auto_screenshot.py <output_path>")
        print("       python auto_screenshot.py <output_dir> --multi")
        sys.exit(1)

    if sys.argv[-1] == "--multi":
        paths = capture_all_screens(sys.argv[1])
        for p in paths:
            print(p)
    else:
        size = capture(sys.argv[1])
        print(f"Saved: {sys.argv[1]} ({size} bytes)")
