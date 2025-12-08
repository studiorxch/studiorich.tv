#!/usr/bin/env python3
# update_mood_csv.py — fully header-agnostic version (handles Mood, mood, etc.)

import csv, datetime, shutil, os

BASE_DIR = "/Users/studio/Projects/studiorich.shop/_data"
CSV_PATH = os.path.join(BASE_DIR, "mood_colors_master.csv")
BACKUP_DIR = os.path.join(BASE_DIR, "archives")
OUT_DIR = "/assets/media/wallpapers/moods"

os.makedirs(BACKUP_DIR, exist_ok=True)

# 1. Backup first
timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
backup_path = os.path.join(BACKUP_DIR, f"{timestamp}_mood_colors_master.csv")
shutil.copy(CSV_PATH, backup_path)
print(f"📦 Backup saved → {backup_path}")

# 2. Read CSV and normalize headers
with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    normalized_rows = []
    field_map = {k.lower().strip(): k for k in reader.fieldnames}

    # find flexible column references
    mood_col = field_map.get("mood") or field_map.get("name") or field_map.get("title") or field_map.get("moods")
    hex_col = field_map.get("hex") or field_map.get("color") or field_map.get("hexcode") or field_map.get("hex value")

    if not mood_col or not hex_col:
        raise KeyError(f"⚠️ Could not find 'mood' or 'hex' column. Headers found: {reader.fieldnames}")

    for row in reader:
        # normalize values
        mood = row[mood_col].strip()
        hex_code = row[hex_col].strip()
        if not hex_code.startswith("#"):
            hex_code = "#" + hex_code

        # generate file URL
        safe_mood = mood.lower().replace(" ", "-")
        safe_hex = hex_code.lstrip("#").lower()
        row["url"] = f"{OUT_DIR}/{safe_mood}-{safe_hex}.png"

        normalized_rows.append(row)

# 3. Write updated CSV back
fieldnames = list(reader.fieldnames)
if "url" not in fieldnames:
    fieldnames.append("url")

with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(normalized_rows)








print(f"✅ Updated CSV written → {CSV_PATH}")
print(f"🖼  URLs now mapped to {OUT_DIR}/<mood>-<hex>.png")




# 6. Generate Markdown preview index
md_path = os.path.join(BASE_DIR, "mood_colors_index.md")
with open(md_path, "w", encoding="utf-8") as md:
    md.write("# 🎨 StudioRich Mood Atlas\n\n")
    md.write("Auto-generated visual reference for all mood colors.\n\n")
    md.write("| Mood | Hex | Preview | URL |\n")
    md.write("|------|-----|----------|-----|\n")

    for row in normalized_rows:
        mood = row[mood_col]
        hex_code = row[hex_col]
        url = row["url"]
        md.write(f"| {mood} | `{hex_code}` | ![]({url}) | {url} |\n")

print(f"📘 Markdown index created → {md_path}")
