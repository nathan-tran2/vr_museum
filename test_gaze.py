from pupil_labs.realtime_api.simple import discover_one_device

print("Looking for Neon device on the network...")
device = discover_one_device()

if device is None:
    print("No device found. Check that the Companion app is running and on the same Wi-Fi.")
else:
    print(f"Connected to: {device}")
    print(f"Gaze: {device.receive_gaze_datum()}")