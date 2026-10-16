"""
Capture a resting pupil baseline.
Averages pupil diameter over a quiet staring period.
Saves to data/pupil_baseline.json for other scripts to use.
"""
from pupil_labs.realtime_api.simple import discover_one_device
from pathlib import Path
from statistics import mean
import json
import time

BASELINE_SECONDS = 5
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
BASELINE_FILE = DATA_DIR / "pupil_baseline.json"

print("Pupil baseline capture.")
print(f"Put the Neon on, stare at a neutral spot in steady lighting for {BASELINE_SECONDS}s.")
input("Press Enter to start...")

device = discover_one_device()
if device is None:
    print("No device found.")
    exit(1)

try:
    print(f"Capturing for {BASELINE_SECONDS}s... stay still.")
    left_vals = []
    right_vals = []
    start = time.time()
    while time.time() - start < BASELINE_SECONDS:
        gaze = device.receive_gaze_datum()
        if gaze.worn:
            left_vals.append(gaze.pupil_diameter_left)
            right_vals.append(gaze.pupil_diameter_right)

    if not left_vals:
        print("No worn samples captured. Fit the Neon properly and try again.")
        exit(1)

    baseline = {
        "timestamp_unix": time.time(),
        "duration_seconds": BASELINE_SECONDS,
        "samples": len(left_vals),
        "pupil_L_mm_mean": mean(left_vals),
        "pupil_R_mm_mean": mean(right_vals),
        "pupil_L_mm_min": min(left_vals),
        "pupil_L_mm_max": max(left_vals),
        "pupil_R_mm_min": min(right_vals),
        "pupil_R_mm_max": max(right_vals),
    }

    with open(BASELINE_FILE, "w") as f:
        json.dump(baseline, f, indent=2)

    print(f"\nBaseline captured:")
    print(f"  Left:  {baseline['pupil_L_mm_mean']:.2f}mm "
          f"(range {baseline['pupil_L_mm_min']:.2f}-{baseline['pupil_L_mm_max']:.2f})")
    print(f"  Right: {baseline['pupil_R_mm_mean']:.2f}mm "
          f"(range {baseline['pupil_R_mm_min']:.2f}-{baseline['pupil_R_mm_max']:.2f})")
    print(f"Saved to {BASELINE_FILE.name}")

finally:
    device.close()