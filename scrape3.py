import json
import re
import requests
from bs4 import BeautifulSoup

URL = "https://www.books.com.tw/web/sys_saletopb/books/19?attribute=30"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def get_top20():
    resp = requests.get(URL, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, "lxml")

    # 主要 selector（已驗證可用）
    items = soup.select("div.type02_bd-a")[:20]
    books = []

    for idx, item in enumerate(items, 1):
        # 排名 - 修正：使用 .stitle .no 精準提取
        rank_tag = item.select_one(".stitle .no")
        rank = rank_tag.get_text(strip=True).replace("NO.", "").strip() if rank_tag else str(idx)

        # 書名
        title_tag = item.select_one("h4 a")
        title = title_tag.get_text(strip=True) if title_tag else "N/A"

        # 價格
        price_tag = item.select_one(".price_a")
        price_text = price_tag.get_text(strip=True) if price_tag else ""
        price_match = re.search(r"(\d+)元", price_text.replace(",", ""))
        price = f"NT${price_match.group(1)}" if price_match else "N/A"

        books.append({"title": title, "price": price, "rank": rank})

    return books

if __name__ == "__main__":
    data = get_top20()
    # 1. 輸出純 JSON 陣列（跟圖片一模一樣）
    print(json.dumps(data, ensure_ascii=False, separators=(',', ':')))
    
    # 2. 存檔
    with open("books_top20.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)