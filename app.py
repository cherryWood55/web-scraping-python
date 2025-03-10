from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for session handling

def get_random_quote():
    """Fetch a random quote from the database."""
    conn = sqlite3.connect('quotes.db')
    c = conn.cursor()
    c.execute("SELECT text, author, bio_link FROM quotes ORDER BY RANDOM() LIMIT 1")
    quote = c.fetchone()
    conn.close()
    return quote

def get_author_details(bio_link):
    """Fetch author birth details from the database."""
    conn = sqlite3.connect('quotes.db')
    c = conn.cursor()
    c.execute("SELECT birth_date, birth_place FROM authors WHERE bio_link=?", (bio_link,))
    details = c.fetchone()
    conn.close()
    return details if details else ("Unknown", "Unknown")

def get_author_hint(author):
    """Provide hints about the author's name."""
    name_parts = author.split()
    first_name_hint = name_parts[0][0]  # First letter of first name
    last_name_hint = name_parts[-1][0] if len(name_parts) > 1 else ""  # First letter of last name
    return f"First name starts with '{first_name_hint}', Last name starts with '{last_name_hint}'"

@app.route("/", methods=["GET", "POST"])
def home():
    # Initialize score tracking
    if "score" not in session:
        session["score"] = {"correct": 0, "incorrect": 0}

    # Fetch a new quote if needed
    if "quote" not in session or session["quote"] is None:
        session["quote"] = get_random_quote()
        session["hints"] = 0
        session["remaining_guesses"] = 4  # Reset attempts
        session["incorrect"] = 0  # Reset incorrect guesses

    quote = session["quote"]
    message = ""
    hint = ""
    show_input = True  # Controls whether the textbox is displayed

    if request.method == "POST":
        # Handle new game request
        if "new_game" in request.form:
            session.pop("quote", None)
            session["remaining_guesses"] = 4
            session["incorrect"] = 0  # Reset incorrect attempts
            return redirect(url_for("home"))  

        # Process user guess
        guess = request.form["guess"].strip().lower()
        if guess == quote[1].lower():
            message = "🎉 Congratulations! You guessed it right!"
            session["score"]["correct"] += 1  # ✅ Increment correct guesses
            session.pop("quote", None)  # ✅ Get new quote on next request
            show_input = False  # ✅ Hide input textbox
            return render_template("index.html", quote_text=quote[0], message=message, correct_answer=quote[1], score=session["score"], show_input=show_input)

        else:
            session["score"]["incorrect"] += 1  # ✅ Increment incorrect guesses
            session["remaining_guesses"] -= 1
            session["incorrect"] += 1  # ✅ Track incorrect guesses
            message = f"❌ Incorrect! {session['remaining_guesses']} attempts left."

            # Provide hints based on attempts
            if session["remaining_guesses"] == 3:
                hint = get_author_hint(quote[1])
            elif session["remaining_guesses"] == 2:
                birth_date, birth_place = get_author_details(quote[2])
                hint = f"The author was born on {birth_date} in {birth_place}."
            elif session["remaining_guesses"] == 1:
                hint = f"Final hint: Author's last name starts with '{quote[1].split()[-1][0]}'"
            elif session["remaining_guesses"] == 0:
                message = f"😢 Sorry, max attempts over! The correct answer was {quote[1]}."
                session.pop("quote", None)  # ✅ Get new quote on next request
                session["incorrect"] = 0  # ✅ Reset incorrect guesses for new game
                show_input = False  # ✅ Hide input textbox
                return render_template("index.html", quote_text=quote[0], message=message, correct_answer=quote[1], score=session["score"], show_input=show_input)

    return render_template(
        "index.html",
        quote_text=quote[0],
        message=message,
        hint=hint,
        score=session["score"],
        show_input=show_input
    )

if __name__ == "__main__":
    app.run(debug=True)
