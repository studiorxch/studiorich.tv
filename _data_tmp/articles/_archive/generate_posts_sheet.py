import pandas as pd
import os
from slugify import slugify
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from urllib.parse import urlparse

# Setup paths and sheet info
POSTS_DIR = "/Users/studio/Sites/studiorich/home/_posts"
SERVICE_ACCOUNT_FILE = "blog-automator-468810-e9ac2ca5c307.json"
SPREADSHEET_NAME = "lofi_articles_sync"

# Google Sheets authentication
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scope)
client = gspread.authorize(creds)
sheet = client.open(SPREADSHEET_NAME).sheet1

# Load data
rows = sheet.get_all_records()
df = pd.DataFrame(rows)

# Filter for eligible posts
eligible = df[(df['score'] >= 85) & (df['status'].str.lower() != 'published')]

count = 0  # Track how many posts are generated

for idx, row in eligible.iterrows():
    title = row['title']
    date = row['date']
    url = row['url']
    description = row.get('snippet', '')
    tags = row.get('tags', '')
    tag_list = [tag.strip() for tag in tags.split(',')] if tags else []

    # Generate unique slug using domain
    domain = urlparse(url).netloc.replace('.', '-')
    slug = slugify(f"{title.lower()}-{domain}")
    filename = f"{date}-{slug}.md"
    filepath = os.path.join(POSTS_DIR, filename)

    # Image path logic
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
    frontmatter += "unpublished: true\n---\n"

    # Save markdown post
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(frontmatter)

    print(f"✅ Generated: {filename}")
    count += 1

    # Update Google Sheet: mark as published
    sheet.update_cell(idx + 2, df.columns.get_loc("status") + 1, "published")

print(f"✅ {count} post(s) generated.")
