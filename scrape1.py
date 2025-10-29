import requests
import re

url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
response = requests.get(url)
html = response.text
pattern = r"£\d+\.\d{2}"
prices = re.findall(pattern, html)
print(prices)
