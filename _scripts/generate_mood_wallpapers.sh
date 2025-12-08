#!/usr/bin/env zsh
# generate_mood_wallpapers.sh — 5120×2880 solid-color PNG wallpapers from CSV

CSV="/Users/studio/Projects/studiorich.shop/_data/mood_colors_master.csv"
OUT_DIR="/Users/studio/Projects/studiorich.shop/assets/media/wallpapers/moods"
WIDTH=5120
HEIGHT=2880

mkdir -p "$OUT_DIR"

# Skip header, read CSV line by line
tail -n +2 "$CSV" | while IFS=, read -r mood name hex url; do
  safe_name=$(echo "$mood" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9-' '-')
  safe_hex=$(echo "$hex" | tr -cd 'A-Fa-f0-9')
  file="${OUT_DIR}/${safe_name}-${safe_hex}.png"
  
  echo "🎨 Generating $file ..."
  magick -size "${WIDTH}x${HEIGHT}" "xc:${hex}" "$file"
done

echo "✅ All PNG wallpapers saved in: $OUT_DIR"
