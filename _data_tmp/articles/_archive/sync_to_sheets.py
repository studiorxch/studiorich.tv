import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# CONFIG
SHEET_NAME = "lofi_articles_sync"
CSV_FILE = "/Users/studio/Sites/studiorich/home/_data/articles/articles.csv"
SERVICE_ACCOUNT_FILE = "blog-automator-468810-e9ac2ca5c307.json"

# Authenticate
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scope)
client = gspread.authorize(creds)


# Load CSV
df = pd.read_csv(CSV_FILE)
if "approved" not in df.columns:
    df["approved"] = ""

# Define basic keyword-weight pairs
KEYWORDS = {
    "lo-fi": 20,
    "chillhop": 15,
    "instrumental": 10,
    "nostalgia": 10,
    "beat tape": 10,
    "visual": 5,
    "ambient": 10,
    "retro": 5,
    "japanese": 10,
    "game boy": 15,
    "loop": 5,
    "vaporwave": 10,
    "diary": 5
}

# Apply rule-based score if missing or 0
def calculate_score(row):
    if row.get('score', 0) > 0:
        return row['score']
    
    text = f"{row.get('title', '')} {row.get('snippet', '')}".lower()
    score = 50  # base score

    for kw, weight in KEYWORDS.items():
        if kw in text:
            score += weight
    return min(score, 100)  # cap score

# Apply scoring to DataFrame
df['score'] = df.apply(calculate_score, axis=1)



# Sanitize
df = df.replace({float('inf'): '', float('-inf'): '', pd.NA: '', None: ''}).fillna('')

# Sync
sheet = client.open(SHEET_NAME).sheet1
sheet.clear()
sheet.update([df.columns.values.tolist()] + df.values.tolist())


print(f"✅ Synced {len(df)} articles to Google Sheet: {SHEET_NAME}")
