"""
Real-time fixation detector.
Prints when gaze stays within a radius for a sustained duration.
Prototypes the dwell logic the Unity agent will use for AOI resolution.
"""
from pupil_labs.realtime_api.simple import discover_one_device
import time
import math

FIXATION_RADIUS_PX = 100       # how tight the gaze has to stay
FIXATION_MIN_DURATION = 0.5    # how long before we call it a fixation (seconds)

print("Looking for Neon device...")
device = discover_one_device()
if device is None:
    print("No device found.")
    exit(1)

print(f"Connected: {device}")
print(f"Fixation threshold: {FIXATION_RADIUS_PX}px radius, {FIXATION_MIN_DURATION}s minimum")
print("Press Ctrl+C to stop.\n")

fixation_start = None
fixation_center = None
fixation_reported = False

try:
    while True:
        gaze = device.receive_gaze_datum()
        if not gaze.worn:
            fixation_start = None
            fixation_center = None
            fixation_reported = False
            continue

        pos = (gaze.x, gaze.y)
        if fixation_center is None:
            fixation_center = pos
            fixation_start = time.time()
            fixation_reported = False
        else:
            dx = pos[0] - fixation_center[0]
            dy = pos[1] - fixation_center[1]
            dist = math.sqrt(dx*dx + dy*dy)
            if dist > FIXATION_RADIUS_PX:
                # moved out of fixation
                if fixation_reported:
                    duration = time.time() - fixation_start
                    print(f"  Fixation ended after {duration:.2f}s")
                fixation_center = pos
                fixation_start = time.time()
                fixation_reported = False
            else:
                duration = time.time() - fixation_start
                if duration >= FIXATION_MIN_DURATION and not fixation_reported:
                    print(f"Fixation at ({fixation_center[0]:.0f}, {fixation_center[1]:.0f}) "
                          f"— held for {duration:.2f}s")
                    fixation_reported = True
except KeyboardInterrupt:
    print("\nStopped.")
finally:
    device.close()
    print("Disconnected.")