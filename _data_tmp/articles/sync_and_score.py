# sync_and_score.py
import pandas as pd
import os
from slugify import slugify
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from urllib.parse import urlparse
import hashlib

# Setup paths and sheet info
POSTS_DIR = "/Users/studio/Sites/studiorich/home/_posts"
SERVICE_ACCOUNT_FILE = "blog-automator-468810-e9ac2ca5c307.json"
SPREADSHEET_NAME = "lofi_articles_sync"

# Google Sheets auth
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scope)
client = gspread.authorize(creds)
sheet = client.open(SPREADSHEET_NAME).sheet1

# Load sheet
rows = sheet.get_all_records()
df = pd.DataFrame(rows)

# Normalize status + filter
df["status"] = df["status"].str.lower().str.strip()
eligible = df[(df['score'] >= 85) & (df['status'] != 'published')]

count = 0

for idx, row in eligible.iterrows():
    title = row['title']
    date = row['date']
    url = row['url']
    description = row.get('snippet', '').strip()
    tags = row.get('tags', '')
    tag_list = [t.strip() for t in tags.split(',') if t.strip()]

    # Slug generation with fallback hash for duplicates
    domain = urlparse(url).netloc.replace('.', '-')
    base_slug = slugify(f"{title.lower()}-{domain}")
    slug_hash = hashlib.md5(url.encode()).hexdigest()[:6]
    slug = f"{base_slug}-{slug_hash}"
    filename = f"{date}-{slug}.md"
    filepath = os.path.join(POSTS_DIR, filename)

    if os.path.exists(filepath):
        print(f"⚠️ Skipped (exists): {filename}")
        continue

    image_path = f"/assets/img/blog/{slug}.webp"

    # Build frontmatter
    frontmatter = f"""---
layout: post
title: "{title}"
date: {date}
description: "{description}"
image: {image_path}
tags:
"""
    for tag in tag_list:
        frontmatter += f"  - {tag}\n"
    frontmatter += "unpublished: true\n---\n\n"
    frontmatter += f"_Auto-generated from: [{url}]({url})_\n\n"
    frontmatter += "> TODO: Expand this post with full commentary, visuals, and embed links.\n"

    # Write post
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(frontmatter)

    print(f"✅ Generated: {filename}")
    count += 1

    # Mark row as published
    sheet.update_cell(idx + 2, df.columns.get_loc("status") + 1, "published")

print(f"✅ {count} post(s) generated.")
