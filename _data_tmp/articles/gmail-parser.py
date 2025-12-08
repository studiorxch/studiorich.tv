# gmail-parser.py (updated to unwrap Google redirect URLs)

import imaplib, email
from email.header import decode_header
import os
from dotenv import load_dotenv
from datetime import datetime
import csv
import re
from urllib.parse import unquote, urlparse, parse_qs

load_dotenv()

IMAP_SERVER = "imap.gmail.com"
EMAIL = os.getenv("GMAIL_USER")
PASSWORD = os.getenv("GMAIL_PASS")

# Compute absolute path to data CSV
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV_FILE = os.path.join(BASE_DIR, "_data/articles/lofi_articles.csv")

HEADERS = [
    "date",
    "title",
    "url",
    "snippet",
    "source",
    "keyword_source",
    "status",
    "flags",
]

# Hard-block list
BLOCK_TERMS = ["cryptocurrency", "token", "nft", "web3"]
BLOCK_DOMAINS = ["lofichain", "lofitoon"]

# Clean filename


def clean(text):
    return "".join(c for c in text if c.isalnum() or c in (" ", "-", "_")).rstrip()


# Unwrap Google redirect URLs


def unwrap_google_url(url):
    if "google.com/url" in url:
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        if "url" in qs:
            return unquote(qs["url"][0])
    return url


# Write row to CSV


def save_article(row):
    is_new = not os.path.exists(CSV_FILE)
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(HEADERS)
        writer.writerow(row)


# Parse latest emails


def fetch_alerts():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    result, data = mail.search(None, '(FROM "googlealerts-noreply@google.com")')
    email_ids = data[0].split()[-20:]  # Only last 20
    new_articles = 0

    for eid in email_ids:
        _, msg_data = mail.fetch(eid, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        subject = decode_header(msg["Subject"])[0][0]
        subject = subject.decode() if isinstance(subject, bytes) else subject

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    break
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        matches = re.findall(r"https://www.google.com/url\?[^\s\)]+", body)

        for match in matches:
            final_url = unwrap_google_url(match)
            snippet = body.strip().split("\n")[0]
            status = (
                "trash"
                if any(term in snippet.lower() for term in BLOCK_TERMS)
                or any(domain in final_url.lower() for domain in BLOCK_DOMAINS)
                else "pending"
            )
            flags = "crypto_block" if "trash" in status else ""

            row = [
                datetime.now().strftime("%Y-%m-%d"),
                subject,
                final_url,
                snippet,
                "Google Alert",
                "lofi",
                status,
                flags,
            ]
            save_article(row)
            new_articles += 1

    mail.logout()
    print(f"Saved {new_articles} new articles to {CSV_FILE}")


if __name__ == "__main__":
    fetch_alerts()
