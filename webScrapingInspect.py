import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL for fiction category
base_url = "https://openlibrary.org/search?subject=Fantasy&page={}"

all_books = []

for page in range(1, 500):  # num of pages
    url = base_url.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    item_count = 0

    # Extract book details
    books = soup.find_all("li", class_="searchResultItem sri--w-main")
    for book in books:
        title = book.find("a", class_="results").text.strip()
        author = book.find("span", class_="bookauthor").find("a").text.strip() if book.find("span", class_="bookauthor").find("a") else "Unknown"
        year = book.find("span", class_="resultDetails").find("span").text.strip() if book.find("span", class_="resultDetails").find("span") else "Unknown"
        all_books.append({"Title": title, "Author": author, "Year": year})
        item_count = item_count + 1

    print(f"Scraped page {page}")
    print(f"{item_count} Items scraped")

# Save to CSV
df = pd.DataFrame(all_books)
df.to_csv("openlibrary_books_classic.csv", item_count=False)
print("Data saved to openlibrary_books_classic.csv!")