"""
Phase 4 prototype — Real-time blink detector.

Uses eyelid aperture to detect blinks and track blink rate per minute.
Thresholds calibrated against observed Neon data (open ~5-12, closed ~0).
"""
from pupil_labs.realtime_api.simple import discover_one_device
import time

# When average aperture drops below this, eyes are considered closed.
# Calibrated from inspect_log.py: median aperture when open ~5, min ~0.
APERTURE_CLOSED_THRESHOLD = 2

# Minimum time between blinks (ignore rapid retriggers).
MIN_BLINK_INTERVAL = 0.1

# Minimum duration eyes must stay closed to count as a blink.
# Below this, it's probably just a micro-flutter or signal noise.
MIN_CLOSED_DURATION = 0.05


def main():
    print("Looking for Neon device...")
    device = discover_one_device()
    if device is None:
        print("No device found.")
        return

    print(f"Connected: {device}")
    print(f"Threshold: aperture < {APERTURE_CLOSED_THRESHOLD}  "
          f"min interval {MIN_BLINK_INTERVAL}s  "
          f"min closed {MIN_CLOSED_DURATION}s")
    print("Blink normally. Press Ctrl+C to stop.\n")

    blinks = 0
    start = time.time()
    last_blink_time = 0
    eyes_closed_since = None  # timestamp when eyes started being closed
    eyes_were_open = True

    try:
        while True:
            gaze = device.receive_gaze_datum()
            if not gaze.worn:
                # Reset state when device not worn
                eyes_closed_since = None
                eyes_were_open = True
                continue

            avg_aperture = (gaze.eyelid_aperture_left + gaze.eyelid_aperture_right) / 2
            eyes_closed_now = avg_aperture < APERTURE_CLOSED_THRESHOLD
            now = time.time()

            if eyes_closed_now and eyes_were_open:
                # Just started closing
                eyes_closed_since = now
                eyes_were_open = False

            elif not eyes_closed_now and not eyes_were_open:
                # Just reopened — this is the end of a blink
                if eyes_closed_since is not None:
                    closed_duration = now - eyes_closed_since
                    time_since_last = now - last_blink_time

                    if (closed_duration >= MIN_CLOSED_DURATION and
                            time_since_last > MIN_BLINK_INTERVAL):
                        blinks += 1
                        elapsed_min = (now - start) / 60
                        rate = blinks / elapsed_min if elapsed_min > 0 else 0
                        print(f"Blink #{blinks}  "
                              f"(closed for {closed_duration*1000:.0f}ms, "
                              f"rate: {rate:.1f}/min)")
                        last_blink_time = now

                eyes_closed_since = None
                eyes_were_open = True

    except KeyboardInterrupt:
        elapsed = time.time() - start
        rate = blinks / (elapsed / 60) if elapsed > 0 else 0
        print(f"\nStopped. {blinks} blinks in {elapsed:.1f}s "
              f"(avg rate: {rate:.1f}/min)")
    finally:
        device.close()
        print("Disconnected.")


if __name__ == "__main__":
    main()