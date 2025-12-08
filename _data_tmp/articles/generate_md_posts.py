import pandas as pd
import openai
import os
from slugify import slugify
from datetime import datetime
from urllib.parse import urlparse

# === CONFIG ===
POSTS_DIR = "/Users/studio/Sites/studiorich/home/_posts"
TARGET = os.getenv("BLOG_TARGET", "lofi")  # default
CSV_FILE = f"/Users/studio/Sites/studiorich/home/_data/articles/{TARGET}_articles.csv"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # set your API key as env variable

openai.api_key = OPENAI_API_KEY

# === LOAD DATA ===
df = pd.read_csv(CSV_FILE)
df = df[
    (df["score"] >= 85)
    & (df["status"].str.lower() != "published")
    & (df["approved"].str.lower() != "no")
]


# === GENERATE ===
def generate_post_body(title, snippet, url):
    prompt = f"""
Write a blog blurb for a lo-fi / sound culture website based on the following Google Alert result.

Title: {title}
Snippet: {snippet}
URL: {url}

The tone should be lo-fi editorial: relaxed, confident, curious.
Keep it under 120 words. Link the original URL at the end using markdown.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"].strip()


count = 0
for _, row in df.iterrows():
    title = row["title"]
    date = row["date"]
    snippet = row.get("snippet", "")
    url = row.get("url", "")
    tags = row.get("tags", "").split(",") if "tags" in row else []
    domain = urlparse(url).netloc.replace(".", "-")
    slug = slugify(f"{title.lower()}-{domain}")
    filename = f"{date}-{slug}.md"
    filepath = os.path.join(POSTS_DIR, filename)

    # Generate blog body
    try:
        body = generate_post_body(title, snippet, url)
    except Exception as e:
        print(f"❌ Failed to generate post for: {title}\n{e}")
        continue

    image_path = f"/assets/img/blog/{slug}.webp"

    frontmatter = f"""---
layout: post
title: \"{title}\"
date: {date}
description: \"{snippet.strip()}\"
image: {image_path}
tags:
"""
    for tag in tags:
        frontmatter += f"  - {tag.strip()}\n"
    frontmatter += "unpublished: true\n---\n\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(frontmatter + body + "\n")

    count += 1
    print(f"✅ Generated: {filename}")

print(f"\n✅ {count} post(s) generated with OpenAI.")
