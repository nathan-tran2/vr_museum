"""
Shared Neon XR connection helper.
Tries mDNS discovery first, falls back to direct IP if that fails.
Returns a connected Device, or raises if nothing works.
"""
from pupil_labs.realtime_api.simple import discover_one_device, Device

# Set this to your phone's IP as a fallback. Update when the IP changes.
FALLBACK_IP = "100.70.91.42"
PORT = 8080


def connect():
    """Returns a connected Pupil Labs Neon Device, or exits the script if neither method works."""
    print("Looking for Neon device via mDNS...")
    device = discover_one_device(max_search_duration_seconds=5)

    if device is not None:
        print(f"Found via mDNS: {device}")
        return device

    print(f"mDNS discovery failed. Trying direct IP {FALLBACK_IP}...")
    try:
        device = Device(address=FALLBACK_IP, port=PORT)
        print(f"Connected via direct IP: {device}")
        return device
    except Exception as e:
        print(f"Direct IP also failed: {e}")
        print("Check that the Companion app is running and the phone is reachable.")
        exit(1)