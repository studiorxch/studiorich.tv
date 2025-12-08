import os
import csv

AUDIO_DIR = "/Users/studio/Projects/studiorich.shop/assets/media/audio"
OUTPUT_CSV = "/Users/studio/Projects/studiorich.shop/_data/mood_track_catalog.csv"

# Create output folder if missing
os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

# CSV column headers
headers = [
    "id",
    "index",
    "name",
    "variant",
    "filename",
    "audio_path",
    "mood_group",
    "color",
    "bpm",
    "key",
    "energy",
    "duration",
    "family",
    "tags"
]

rows = []

def parse_filename(filename):
    """
    Converts: 041_Comforting.m4a
    Into:
    index=41
    name="Comforting"
    variant="A"
    """
    base = filename.replace(".m4a", "")

    # Split at first "_" → ["041", "Comforting"]
    idx, name = base.split("_", 1)

    # Detect variant
    # Because each mood has 2 versions, we assign:
    # odd → A, even → B
    variant = "A" if int(idx) % 2 == 1 else "B"

    return idx, name, variant


print("Scanning audio folder...")

for f in sorted(os.listdir(AUDIO_DIR)):
    if not f.endswith(".m4a"):
        continue

    idx, name, variant = parse_filename(f)

    rows.append({
        "id": f"{idx}_{name}_{variant}",
        "index": idx,
        "name": name,
        "variant": variant,
        "filename": f,
        "audio_path": f"/assets/media/audio/{f}",

        # Placeholder fields — to be filled later
        "mood_group": "",
        "color": "",
        "bpm": "",
        "key": "",
        "energy": "",
        "duration": "",
        "family": "",
        "tags": ""
    })

# Write CSV
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)

print(f"CSV generated → {OUTPUT_CSV}")
print(f"Total tracks: {len(rows)}")
