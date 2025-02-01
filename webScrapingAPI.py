import requests
import pandas as pd



base_url = "https://openlibrary.org/search.json"



query = "subject:fiction"  
limit = 100                # API limit 
total_records = 10000      # Total records you want to fetch
all_books = []




for offset in range(0, total_records, limit):
    params = {
        "q": query,
        "limit": limit,
        "offset": offset
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        for book in data.get("docs", []):
            all_books.append({
                "Title": book.get("title"),
                "Author": ", ".join(book.get("author_name", [])) if book.get("author_name") else "Unknown",
                "First Publish Year": book.get("first_publish_year", "Unknown"),
                "Subjects": ", ".join(book.get("subject", [])) if book.get("subject") else "Unknown"
            })
        print(f"Fetched {len(all_books)} books so far...")
    else:
        print(f"Error fetching data at offset {offset}: {response.status_code}")
        break




df = pd.DataFrame(all_books)
df.to_csv("openlibrary_books_large.csv", index=False)
print("Data saved to openlibrary_books_large.csv!")

