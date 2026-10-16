"""
Phase 1.1 — Discovery test.
Confirms the Companion phone is reachable on the network and streaming gaze.
"""
from pupil_labs.realtime_api.simple import discover_one_device

print("Looking for Neon device on the network...")
device = discover_one_device()

if device is None:
    print("No device found. Check that the Companion app is running and on the same Wi-Fi.")
else:
    try:
        print(f"Connected to: {device}")
        print(f"Gaze: {device.receive_gaze_datum()}")
    finally:
        device.close()
        print("Disconnected.")