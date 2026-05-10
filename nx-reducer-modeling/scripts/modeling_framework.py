
# modeling_framework.py — Step-by-step model building with auto-screenshot + geometry validation
# Every feature addition is followed by: screenshot + measurement check
# This gives the AI spatial awareness it cannot get from coordinates alone.

import os, sys, json, time, math
from datetime import datetime
from PIL import ImageGrab

# === Configuration ===
SCREENSHOT_DIR = None  # set per session
CHECKPOINTS = []       # stores (step_name, screenshot_path, measurements)


def init_session(output_dir):
    """Start a new modeling session with screenshot tracking."""
    global SCREENSHOT_DIR, CHECKPOINTS
    SCREENSHOT_DIR = os.path.join(output_dir, "_checkpoints")
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    CHECKPOINTS = []
    return SCREENSHOT_DIR


def checkpoint(name, measurements=None):
    """
    Called after each modeling step.
    Takes a screenshot and records measurements.
    Returns the screenshot path for vision analysis.
    """
    global CHECKPOINTS
    timestamp = datetime.now().strftime("%H%M%S")
    step_num = len(CHECKPOINTS) + 1
    filename = f"{step_num:02d}_{name}_{timestamp}.png"
    path = os.path.join(SCREENSHOT_DIR, filename)

    # Take screenshot
    img = ImageGrab.grab()
    img.save(path)

    record = {
        "step": step_num,
        "name": name,
        "screenshot": path,
        "measurements": measurements or {},
        "timestamp": timestamp,
    }
    CHECKPOINTS.append(record)

    # Print summary for AI to read
    size_kb = os.path.getsize(path) // 1024
    print(f"\n[CHECKPOINT {step_num}] {name}")
    print(f"  Screenshot: {filename} ({size_kb}KB)")
    if measurements:
        for k, v in measurements.items():
            print(f"  {k}: {v}")
    print()

    return path


def measure_body(body):
    """
    Extract key measurements from an NX body.
    Returns a dict the AI can use for validation.
    """
    edges = list(body.GetEdges())
    faces = list(body.GetFaces())

    # Bounding box from edge vertices
    xs, ys, zs = [], [], []
    sample_edges = min(300, len(edges))
    for e in edges[:sample_edges]:
        try:
            for p in e.GetVertices():
                xs.append(p.X); ys.append(p.Y); zs.append(p.Z)
        except:
            pass

    if not xs:
        return {"error": "no vertices"}

    return {
        "faces": len(faces),
        "edges": len(edges),
        "bbox_x": (round(min(xs), 1), round(max(xs), 1)),
        "bbox_y": (round(min(ys), 1), round(max(ys), 1)),
        "bbox_z": (round(min(zs), 1), round(max(zs), 1)),
        "span_x": round(max(xs) - min(xs), 1),
        "span_y": round(max(ys) - min(ys), 1),
        "span_z": round(max(zs) - min(zs), 1),
    }


def validate_against_spec(measurements, spec):
    """
    Compare current measurements against design spec.
    Returns list of (check_name, passed, actual, expected) tuples.
    """
    results = []
    for check_name, expected in spec.items():
        actual = measurements.get(check_name)
        if actual is not None:
            if isinstance(expected, (int, float)):
                passed = abs(actual - expected) < max(1.0, expected * 0.05)
            elif isinstance(expected, tuple) and len(expected) == 2:
                passed = expected[0] <= actual <= expected[1]
            else:
                passed = True
            results.append((check_name, passed, actual, expected))
    return results


def save_session_log():
    """Save all checkpoints to a JSON log for later analysis."""
    if not CHECKPOINTS:
        return None
    log_path = os.path.join(SCREENSHOT_DIR, "_session_log.json")
    log_data = {
        "total_steps": len(CHECKPOINTS),
        "checkpoints": [{k: v for k, v in c.items() if k != "screenshot"}
                        for c in CHECKPOINTS],
    }
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)
    return log_path


def get_last_screenshot():
    """Return path to the most recent screenshot."""
    if CHECKPOINTS:
        return CHECKPOINTS[-1]["screenshot"]
    return None


def get_all_screenshots():
    """Return all screenshot paths for batch vision analysis."""
    return [c["screenshot"] for c in CHECKPOINTS]


# === Quick test ===
if __name__ == "__main__":
    init_session(r"G:\作业\建模\箱体_重做")
    print(f"Session initialized: {SCREENSHOT_DIR}")

    # Test screenshot
    path = checkpoint("test_step", {"faces": 10, "bbox_x": (-100, 100)})
    print(f"Test screenshot: {path}")

    log = save_session_log()
    print(f"Session log: {log}")
