"""
Phase 1 — Direct IP fallback.
Use if discover_one_device() hangs (university client isolation, etc.)
Replace PHONE_IP with the IP shown in the Neon Companion app.
"""
from pupil_labs.realtime_api.simple import Device

PHONE_IP = "192.168.1.XXX"  # <- replace with your phone's IP
PORT = 8080

print(f"Connecting directly to {PHONE_IP}:{PORT}...")
device = Device(address=PHONE_IP, port=PORT)
print(f"Connected: {device}")
print(f"Gaze: {device.receive_gaze_datum()}")