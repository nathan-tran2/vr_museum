"""
Phase 1.2 — Live gaze stream.
Prints gaze coordinates and pupil diameter to the console at ~10 Hz.
Press Ctrl+C to stop.
"""
from pupil_labs.realtime_api.simple import discover_one_device
import time
import traceback

print("Looking for Neon device...")
device = discover_one_device()

if device is None:
    print("No device found.")
    exit(1)

print(f"Connected: {device}")
print("Streaming. Press Ctrl+C to stop.\n")

count = 0
try:
    while True:
        try:
            gaze = device.receive_gaze_datum()
            print(
                f"[{count:4d}]  x={gaze.x:7.1f}  y={gaze.y:7.1f}  "
                f"pupil_L={gaze.pupil_diameter_left:.2f}mm  "
                f"pupil_R={gaze.pupil_diameter_right:.2f}mm  "
                f"worn={gaze.worn}"
            )
            count += 1
        except Exception as e:
            print(f"Error in loop iteration {count}: {e}")
            traceback.print_exc()
            break
        time.sleep(0.1)
except KeyboardInterrupt:
    print(f"\nStopped after {count} samples.")
finally:
    device.close()
    print("Disconnected.")