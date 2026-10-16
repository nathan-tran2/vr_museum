"""
Phase 1 — Direct IP fallback.
Use if discover_one_device() hangs (university client isolation, etc.)
Update PHONE_IP with the IP shown in the Neon Companion app.
"""
from pupil_labs.realtime_api.simple import Device

PHONE_IP = "100.70.91.42"  # update if the phone's IP changes
PORT = 8080

print(f"Connecting directly to {PHONE_IP}:{PORT}...")
device = Device(address=PHONE_IP, port=PORT)

try:
    print(f"Connected: {device}")
    print(f"Gaze: {device.receive_gaze_datum()}")
finally:
    device.close()
    print("Disconnected.")