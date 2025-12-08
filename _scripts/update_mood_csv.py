#!/usr/bin/env python3
# update_mood_csv.py — backup + append wallpaper URLs to mood_colors_master.csv

import csv, datetime, shutil, os

BASE_DIR = "/Users/studio/Projects/studiorich.shop/_data"
CSV_PATH = os.path.join(BASE_DIR, "mood_colors_master.csv")
BACKUP_DIR = os.path.join(BASE_DIR, "archives")
OUT_DIR = "/assets/media/wallpapers/moods"

os.makedirs(BACKUP_DIR, exist_ok=True)

# 1. Backup the current CSV
timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
backup_path shu=til.copy(CSV_PATH, backup_path)
 os.path.join(BACKUP_DIR, f"{timestamp}_mood_colors_master.csv")
print(f"📦 Backup saved → {backup_path}")

# 2. Load and update
rows = []
with open(CSV_PATH, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        hex_clean = row["hex"].lstrip("#").lower()
        mood_clean = row["mood"].strip().replace(" ", "-").lower()
        row["url"] = f"{OUT_DIR}/{mood_clean}-{hex_clean}.png"
        rows.append(row)

# 3. Write back to main CSV (preserving header)
fieldnames = reader.fieldnames + ["url"] if "url" not in reader.fieldnames else reader.fieldnames
with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ Updated CSV written → {CSV_PATH}")
print(f"🖼  URLs now point to {OUT_DIR}/<mood>-<hex>.png")
