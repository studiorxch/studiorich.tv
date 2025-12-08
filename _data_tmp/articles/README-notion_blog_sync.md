# StudioRich Editorial Sync & Blog Automation System

This README documents the full pipeline for syncing scored articles from a CSV file to Notion, reviewing/editing them inside a Notion database, and generating markdown-based blog posts based on scored and approved entries.

---

## 🔁 Overview

The pipeline connects these key elements:

1. **CSV Article Input** (`articles.csv`)
2. **Notion Editorial Scoring System** (sync via API)
3. **Blog Post Generator** (`generate_md_posts.py`)
4. **Markdown Output for Publishing**

---

## 🧩 Folder Structure

```
articles/
├── articles.csv                    # Main source of article entries
├── notion-editorial-sync.js       # JS script to sync CSV to Notion
├── generate_md_posts.py           # Python script to convert Notion-approved entries to blog posts
├── sync_to_sheets.py              # Optional: sync to Google Sheets
├── .env                           # Contains Notion credentials and DB ID
└── _archive/                      # Deprecated CSVs and older scoring data
```

---

## 🔐 .env File (Required)

Place this in `articles/.env`:

```dotenv
NOTION_TOKEN=ntn_XXXXXXXXXXXXXXX     # Integration token from Notion
NOTION_DATABASE_ID=XXXXXXXXXXXXXXXX  # Your editorial scoring DB ID
```

> 📝 Make sure the token is from an internal integration with full access to the relevant Notion database. Share the database with the integration bot.

---

## 🔄 Sync Script: `notion-editorial-sync.js`

### Description:
Pushes all entries from `articles.csv` into your Notion database.

### Run Command:
```bash
node notion-editorial-sync.js
```

### Prerequisites:
```bash
npm install @notionhq/client dotenv csv-parser
```

### Handles:
- Title, Score, Date, URL, Pros, Cons, Notes
- Skips rows missing required fields
- Logs errors for failed entries

### Requirements:
- Column names in the CSV must exactly match the Notion database property names (`title`, `score`, `date`, etc.)
- CSV must be in `articles/`

---

## ✍️ Notion Database Setup

- Use lowercase property names: `title`, `score`, `date`, `url`, `pros`, `cons`, `notes`
- Make sure the integration token is invited to the database
- Optional: Add a `status` or `ready` checkbox property for filtering approved posts

---

## 📝 Blog Generation: `generate_md_posts.py`

### Description:
Converts approved Notion entries into fully formatted markdown blog posts.

### Features:
- Adds internal backlinks (e.g. [visual beat loop aesthetics](/tags/visual-beat-loop/))
- Auto-generates frontmatter for blog publishing
- Optional tagging based on scoring system or editorial notes

### Run Command:
```bash
python generate_md_posts.py
```

> Optionally pair this with music sync (`article_to_music_scoring.md`) or auto-thumbnail generation for visuals.

---

## 🛠 Future Add-ons

- Scheduled Notion sync (via cron or GitHub Action)
- Duplicate detection during sync
- Pull updated scoring notes from Notion
- Match blog post with audio from lo-fi track archive

---

## 🧠 Tips

- Always validate the `articles.csv` before syncing (title + score required)
- Keep the `.env` file private and out of version control
- Use the Notion database as your source of truth for editorial approval

---

## 🎉 You're Done!

Once synced, reviewed, and approved in Notion, blog generation becomes a 1-command process.

This system helps ensure that only the highest-quality, contextually relevant articles move forward into StudioRich's editorial flow — keeping the blog aligned with our scoring philosophy, aesthetics, and publishin