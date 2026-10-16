"""
Analyze a session log CSV.
Prints summary stats to help calibrate thresholds for the state layer.
"""
import csv
from pathlib import Path
from statistics import mean, stdev, median
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Load the most recent CSV if no arg given
if len(sys.argv) > 1:
    log_file = Path(sys.argv[1])
else:
    csvs = sorted(DATA_DIR.glob("gaze_log_*.csv"))
    if not csvs:
        print("No CSVs found in data/.")
        exit(1)
    log_file = csvs[-1]

print(f"Analyzing: {log_file.name}\n")

rows = []
with open(log_file, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

print(f"Total samples: {len(rows)}")
print(f"Duration: {float(rows[-1]['t_seconds']):.1f} seconds")
print(f"Effective rate: {len(rows) / float(rows[-1]['t_seconds']):.1f} Hz\n")

# Worn fraction
worn_count = sum(1 for r in rows if r["worn"] == "True")
print(f"Worn: {worn_count}/{len(rows)} ({100*worn_count/len(rows):.1f}%)\n")

# Only analyze worn samples
worn_rows = [r for r in rows if r["worn"] == "True"]
if not worn_rows:
    print("No samples where worn=True. Put the Neon on and re-log.")
    exit(0)

for field in ["pupil_L_mm", "pupil_R_mm", "eyelid_aperture_left", "eyelid_aperture_right"]:
    vals = [float(r[field]) for r in worn_rows]
    print(f"{field}:")
    print(f"  mean={mean(vals):.2f}  median={median(vals):.2f}  "
          f"stdev={stdev(vals):.2f}  min={min(vals):.2f}  max={max(vals):.2f}")

# Gaze range
xs = [float(r["gaze_x"]) for r in worn_rows]
ys = [float(r["gaze_y"]) for r in worn_rows]
print(f"\ngaze_x:  min={min(xs):.0f}  max={max(xs):.0f}  range={max(xs)-min(xs):.0f}")
print(f"gaze_y:  min={min(ys):.0f}  max={max(ys):.0f}  range={max(ys)-min(ys):.0f}")