#  Quote Guessing Game - Flask App

This is a simple **Flask-based web app** where users guess the author of a randomly selected quote. The app provides **progressive hints** after incorrect guesses and keeps track of the user's score.

---

## Features

✅ **Random Quotes:** Fetches a random quote from an SQLite database  
✅ **User Guesses:** User tries to guess the author  
✅ **Progressive Hints:**  
   - After 1 wrong attempt → First letter of the first and last name  
   - After 2 wrong attempts → Author’s birth date & place  
   - After 3 wrong attempts → First letter of the last name  
   - After 4 wrong attempts → Reveals the correct answer  
✅ **Score Tracking:**  
   - **Correct guesses** are incremented when the user gets the author right  
   - **Incorrect guesses** are incremented when the user guesses incorrectly  
   - **Incorrect attempts reset** when a new quote is loaded  
✅ **New Quote Option:** Users can start over anytime  

---

##  Setup & Installation

### 1️. Clone the Repository
```bash
git clone https://github.com/your-username/quote-guess-game.git
cd quote-guess-game
```
### 2. Set Up the Database

Create a SQLite database and add two tables (quotes and authors).
Run the following SQL queries in an SQLite environment:

```bash
CREATE TABLE quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    author TEXT NOT NULL,
    bio_link TEXT NOT NULL
);

CREATE TABLE authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    birth_date TEXT,
    birth_place TEXT,
    bio_link TEXT UNIQUE NOT NULL
);
```
Then, insert some sample data into quotes and authors.

### Running the app
```bash
python3 quotes_scraper.py
python3 app.py
```
Go to http://127.0.0.1:5000/ in your browser.

### Project Structure
```csharp
- quote-guess-game
 ┣  app.py               # Main Flask application
 ┣  quotes_scraper.py
 ┣  templates/
 ┃ ┣  index.html         # Frontend UI (HTML & CSS)
 ┣  quotes.db            # SQLite database
 ┣  README.md            # Project documentation
```

Built with ❤️ using Flask & SQLite.



