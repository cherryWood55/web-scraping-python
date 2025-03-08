import sqlite3
import requests
from bs4 import BeautifulSoup
import time

# Database setup
conn = sqlite3.connect('quotes.db')
c = conn.cursor()

# Create Quotes Table
c.execute('''
CREATE TABLE IF NOT EXISTS quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    author TEXT NOT NULL,
    bio_link TEXT NOT NULL
)
''')

# Create Authors Table
c.execute('''
CREATE TABLE IF NOT EXISTS authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    birth_date TEXT,
    birth_place TEXT,
    bio_link TEXT NOT NULL UNIQUE
)
''')

conn.commit()
conn.close()

# Web Scraping Setup
base_url = "http://quotes.toscrape.com/"
url = "/page/1"

quotes_data = []
authors_data = set()  # Avoid duplicate authors

while url:
    res = requests.get(f"{base_url}{url}")
    print(f"Scraping {base_url}{url}...")
    soup = BeautifulSoup(res.text, "html.parser")

    quotes = soup.find_all(class_="quote")


    for quote in quotes:
        text = quote.find(class_="text").get_text()
        author = quote.find(class_="author").get_text()
        bio_link = quote.find("a")["href"]

        # Store quote data
        quotes_data.append((text, author, bio_link))

        # Fetch birth details only if the author is new
        if bio_link not in {a[3] for a in authors_data}:  # ✅ Ensures bio_link is checked correctly
            author_res = requests.get(f"{base_url}{bio_link}")
            author_soup = BeautifulSoup(author_res.text, "html.parser")

            birth_date = author_soup.find(class_="author-born-date").get_text()
            birth_place = author_soup.find(class_="author-born-location").get_text()

            authors_data.add((author, birth_date, birth_place, bio_link))  # ✅ Correct structure

    # Go to next page if available
    next_btn = soup.find(class_="next")
    url = next_btn.find("a")["href"] if next_btn else None
    time.sleep(2)

# Store scraped data in the database
conn = sqlite3.connect('quotes.db')
c = conn.cursor()

# Insert Quotes
c.executemany("INSERT INTO quotes (text, author, bio_link) VALUES (?, ?, ?)", quotes_data)

# Insert Authors
c.executemany("INSERT OR IGNORE INTO authors (name, birth_date, birth_place, bio_link) VALUES (?, ?, ?, ?)", authors_data)

conn.commit()
conn.close()
print("Scraping complete! Data saved in quotes.db")
