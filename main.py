import requests
# requests help us grab the page, when the response is received it is stored in the form of a string
from bs4 import BeautifulSoup
# bs4 library is used to create beasutifulSoup object
# Beautiful Soup is a Python library for pulling data out of HTML and XML files. 
# It works with your favorite parser to provide idiomatic ways of navigating, searching, and modifying the parse tree. 
# It commonly saves programmers hours or days of work. The latest Version of Beautifulsoup is v4.9.3 as of now. 
from csv import writer
# csv library helps reading and writing CSV files using python
from time import sleep
# sleep function from time module helps add delay in the execution of the program
from random import choice
# to return a random element

# list to store scraped data
all_quotes = []

# this part of the url is constant
base_url = "http://quotes.toscrape.com/"
# Scrape the details from this link

# this part of the url will keep changing
url = "/page/1"

while url:
	# concatenating both urls
	# making request
	res = requests.get(f"{base_url}{url}")
	print(f"Now Scraping {base_url}{url}")
	soup = BeautifulSoup(res.text, "html.parser")

	# extracting all elements
	quotes = soup.find_all(class_="quote")

	for quote in quotes:
		all_quotes.append({
			"text": quote.find(class_="text").get_text(),
			"author": quote.find(class_="author").get_text(),
			"bio-link": quote.find("a")["href"]
		})
	next_btn = soup.find(class_="next")
	url = next_btn.find("a")["href"] if next_btn else None
	sleep(2)

quote = choice(all_quotes)
remaining_guesses = 4
print("Here's a quote: ")
print(quote["text"])

guess = ''
while guess.lower() != quote["author"].lower() and remaining_guesses > 0:
	guess = input(
		f"Who said this quote? Guesses remaining {remaining_guesses}\n")
	
	if guess == quote["author"]:
		print("CONGRATULATIONS!!! YOU GOT IT RIGHT")
		break
	remaining_guesses -= 1
	
	if remaining_guesses == 3:
		res = requests.get(f"{base_url}{quote['bio-link']}")
		soup = BeautifulSoup(res.text, "html.parser")
		birth_date = soup.find(class_="author-born-date").get_text()
		birth_place = soup.find(class_="author-born-location").get_text()
		print(
			f"Here's a hint: The author was born on {birth_date}{birth_place}")
	
	elif remaining_guesses == 2:
		print(
			f"Here's a hint: The author's first name starts with: {quote['author'][0]}")
	
	elif remaining_guesses == 1:
		last_initial = quote["author"].split(" ")[1][0]
		print(
			f"Here's a hint: The author's last name starts with: {last_initial}")
	
	else:
		print(
			f"Sorry, you ran out of guesses. The answer was {quote['author']}")
