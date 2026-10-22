from playwright.sync_api import sync_playwright
from models import save_books_to_db


def run_dynamic_crawler():
  print("正在啟動 Playwright 無頭瀏覽器...")
  with sync_playwright() as p:
    # 啟動 Chromium 瀏覽器
    browser = p.chromium.launch(headless=True)
    page = browser.new_context().new_page()

    print("正在前往目標網站...")
    page.goto("http://books.toscrape.com/")

    # 等待頁面上的書籍元素順利載入（展示動態等待機制）
    page.wait_for_selector(".product_pod")

    books_data = []
    products = page.locator(".product_pod")
    count = products.count()
    print(f"頁面載入完成，發現 {count} 本書的渲染元素。")

    for i in range(count):
      product = products.nth(i)
      title = product.locator("h3 a").get_attribute("title")
      price = product.locator(".price_color").inner_text()

      # 解析評分星等（class 名稱中包含評分，如 star-rating Three）
      rating_class = (
          product.locator(".star-rating").get_attribute("class") or ""
      )
      rating = rating_class.replace("star-rating", "").strip()

      books_data.append({"title": title, "price": price, "rating": rating})

    browser.close()
    print("瀏覽器已關閉。")

    # 將抓取到的動態資料寫入 SQLModel 資料庫（自動去重與更新）
    save_books_to_db(books_data)


if __name__ == "__main__":
  run_dynamic_crawler()