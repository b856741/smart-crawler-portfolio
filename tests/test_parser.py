from pathlib import Path
from bs4 import BeautifulSoup


def test_book_parser():
  current_dir = Path(__file__).parent
  html_path = current_dir / "fixtures" / "sample_page.html"

  with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

  soup = BeautifulSoup(html_content, "html.parser")
  product = soup.find("article", class_="product_pod")

  title = product.find("h3").find("a")["title"]
  # 將 price_colorN 修正為 price_color
  price = product.find("p", class_="price_color").text
  rating = product.find("p", class_="star-rating")["class"][1]

  assert title == "Test Book Title"
  assert price == "£51.99"
  assert rating == "Three"