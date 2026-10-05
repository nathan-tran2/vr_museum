"""
Phase 1.3 — Session logger.
Records gaze and pupil data to a timestamped CSV for N seconds.
Use the output to analyze signal quality offline.
"""
from pupil_labs.realtime_api.simple import discover_one_device
import csv
import time
from datetime import datetime

DURATION_SECONDS = 60

print("Looking for Neon device...")
device = discover_one_device()

if device is None:
    print("No device found.")
    exit(1)

filename = f"../data/gaze_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
start = time.time()

with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "t_seconds", "gaze_x", "gaze_y", "worn",
        "pupil_L_mm", "pupil_R_mm"
    ])

    print(f"Logging {DURATION_SECONDS} seconds to {filename}...")
    while time.time() - start < DURATION_SECONDS:
        gaze = device.receive_gaze_datum()
        eye_state = device.receive_eye_state()
        writer.writerow([
            time.time() - start,
            gaze.x, gaze.y, gaze.worn,
            eye_state.pupil_diameter_left,
            eye_state.pupil_diameter_right,
        ])

print(f"Done. Logged to {filename}")