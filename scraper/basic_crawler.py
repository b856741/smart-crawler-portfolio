import csv
import requests
from bs4 import BeautifulSoup
from models import save_books_to_db  # 匯入剛剛寫好的資料庫邏輯


def scrape_books():
  base_url = "http://books.toscrape.com/catalogue/page-{}.html"
  books_data = []

  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
          " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
      )
  }

  for page in range(1, 4):
    url = base_url.format(page)
    print(f"正在爬取頁面: {url}")

    try:
      response = requests.get(url, headers=headers, timeout=10)
      if response.status_code == 404:
        break
      response.raise_for_status()

      soup = BeautifulSoup(response.text, "html.parser")
      products = soup.find_all("article", class_="product_pod")

      for product in products:
        title = product.find("h3").find("a")["title"]
        price = product.find("p", class_="price_color").text
        rating = product.find("p", class_="star-rating")["class"][1]

        books_data.append({"title": title, "price": price, "rating": rating})

    except requests.exceptions.RequestException as e:
      print(f"網路請求錯誤: {e}")
      break

  # 1. 寫入 CSV 備份
  csv_filename = "books.csv"
  with open(csv_filename, mode="w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "price", "rating"])
    writer.writeheader()
    writer.writerows(books_data)

  # 2. 寫入 SQLModel 資料庫（去重與增量更新）
  save_books_to_db(books_data)


if __name__ == "__main__":
  scrape_books()