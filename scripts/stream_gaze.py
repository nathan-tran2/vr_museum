"""
Phase 1.2 — Live gaze stream.
Prints gaze coordinates and pupil diameter to the console at ~10 Hz.
Press Ctrl+C to stop.
"""
from pupil_labs.realtime_api.simple import discover_one_device
import time

print("Looking for Neon device...")
device = discover_one_device()

if device is None:
    print("No device found.")
    exit(1)

print(f"Connected: {device}")
print("Streaming. Press Ctrl+C to stop.\n")

try:
    while True:
        gaze = device.receive_gaze_datum()
        eye_state = device.receive_eye_state()
        print(
            f"x={gaze.x:7.1f}  y={gaze.y:7.1f}  "
            f"pupil_L={eye_state.pupil_diameter_left:.2f}mm  "
            f"pupil_R={eye_state.pupil_diameter_right:.2f}mm  "
            f"worn={gaze.worn}"
        )
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nStopped.")