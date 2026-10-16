"""
Phase 1.3 — Session logger.
Records gaze and pupil data to a timestamped CSV for N seconds.
Writes to <project_root>/data/ regardless of where the script is run from.
"""
from pupil_labs.realtime_api.simple import discover_one_device
import csv
import time
from pathlib import Path
from datetime import datetime

DURATION_SECONDS = 60

# Resolve data/ relative to the project root (parent of scripts/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

filename = DATA_DIR / f"gaze_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

print("Looking for Neon device...")
device = discover_one_device()

if device is None:
    print("No device found.")
    exit(1)

try:
    print(f"Connected: {device}")
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "t_seconds", "gaze_x", "gaze_y", "worn",
            "pupil_L_mm", "pupil_R_mm",
            "eyelid_aperture_left", "eyelid_aperture_right",
        ])

        print(f"Logging {DURATION_SECONDS} seconds to {filename.name}...")
        start = time.time()
        count = 0
        while time.time() - start < DURATION_SECONDS:
            gaze = device.receive_gaze_datum()
            writer.writerow([
                time.time() - start,
                gaze.x, gaze.y, gaze.worn,
                gaze.pupil_diameter_left,
                gaze.pupil_diameter_right,
                gaze.eyelid_aperture_left,
                gaze.eyelid_aperture_right,
            ])
            count += 1

    print(f"Done. Logged {count} samples to {filename}")
finally:
    device.close()
    print("Disconnected.")