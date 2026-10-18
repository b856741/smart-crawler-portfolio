import csv
import requests
from bs4 import BeautifulSoup


def scrape_books():
  # 使用專門設計用於練習的網站 books.toscrape.com
  base_url = "http://books.toscrape.com/catalogue/page-{}.html"
  books_data = []

  # 帶有識別資訊的 User-Agent，避免被輕易阻擋
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
          " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
      )
  }

  # 示範抓取前 3 頁
  for page in range(1, 4):
    url = base_url.format(page)
    print(f"正在爬取頁面: {url}")

    try:
      # 發送請求，設定 10 秒逾時
      response = requests.get(url, headers=headers, timeout=10)

      # 檢查 HTTP 狀態碼
      if response.status_code == 404:
        print("已到達最後一頁，停止爬取。")
        break
      response.raise_for_status()

      # 使用 BeautifulSoup 解析 HTML
      soup = BeautifulSoup(response.text, "html.parser")
      products = soup.find_all("article", class_="product_pod")

      for product in products:
        # 抓取書名
        title = product.find("h3").find("a")["title"]
        # 抓取價格
        price = product.find("p", class_="price_color").text
        # 抓取評分 (星級會放在 class 的第二個屬性中，例如 'Three')
        rating = product.find("p", class_="star-rating")["class"][1]

        books_data.append({"title": title, "price": price, "rating": rating})

    except requests.exceptions.RequestException as e:
      print(f"網路請求發生錯誤: {e}")
      break

  # 將抓取到的資料寫入 CSV 檔案
  csv_filename = "books.csv"
  with open(csv_filename, mode="w", newline="", encoding="utf-8-sig") as f:
    fieldnames = ["title", "price", "rating"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()
    for row in books_data:
      writer.writerow(row)

  print(f"爬取成功！共收集 {len(books_data)} 筆資料，已儲存至 {csv_filename}")


if __name__ == "__main__":
  scrape_books()