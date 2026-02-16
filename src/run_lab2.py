import os
import json
import pandas as pd
import matplotlib.pyplot as plt

from spatial import PointSet

#-------------------------------------------------------------------------
# Paths
#-------------------------------------------------------------------------
DATA_PATH = "data/points.csv"
OUTPUT_DIR = "output"
SUMMARY_PATH = os.path.join(OUTPUT_DIR, "Lab2_report.json")
PLOT_PATH = os.path.join(OUTPUT_DIR, "Lab2_preview.png")

#-------------------------------------------------------------------------
# Read the CSV file
#-------------------------------------------------------------------------
try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    print(f"Error: Cannot find file at '{DATA_PATH}'.")
    print("Make sure you have: data/points.csv")
    raise

print("=== DATA INSPECTION REPORT ===")

point_set = PointSet.from_csv(DATA_PATH)
bbox = point_set.bbox()
print("\nBounding Box:")
print(f"Min Longitude: {bbox[0]}")
print(f"Min Latitude : {bbox[1]}")
print(f"Max Longitude: {bbox[2]}")
print(f"Max Latitude : {bbox[3]}")

pois = point_set.filter_by_tag("poi")
print(f"Found {pois.count()} POIs.")

plt.figure()
if point_set.count() == 0:

    plt.title("Preview Plot (No valid coordinates to plot)")
else:
    plt.scatter([p.lon for p in point_set._points], [p.lat for p in point_set._points])
    plt.title("Lab Exer 2: Point Preview (lon vs lat)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

plt.savefig(PLOT_PATH, dpi=150, bbox_inches="tight")
plt.close()

print(f"Saved scatter plot to: {PLOT_PATH}")

summary = {
    "total_point_count": point_set.count(),
    "bounding_box": {
        "min_lon": bbox[0],
        "min_lat": bbox[1], 
        "max_lon": bbox[2],
        "max_lat": bbox[3],
    },
     "counts_per_tag": point_set.get_tag_counts(), #(optional)
}

with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)

print(f"\nSaved report to: {SUMMARY_PATH}")