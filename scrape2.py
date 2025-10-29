import requests
from bs4 import BeautifulSoup
import json

url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")

books = soup.find_all("article", class_="product_pod")

data = []

for book in books:

    title_tag = book.h3.a
    title = title_tag.get("title", "").strip()

    price_tag = book.find("p", class_="price_color")
    price = price_tag.get_text(strip=True) if price_tag else ""

    rating_tag = book.find("p", class_="star-rating")
    rating_class = rating_tag.get("class", [])
    rating = rating_class[1] if len(rating_class) > 1 else ""

    book_info = {
        "title": title,
        "price": price,
        "rating": rating
    }
    data.append(book_info)

print(json.dumps(data, indent=4, ensure_ascii=False))
