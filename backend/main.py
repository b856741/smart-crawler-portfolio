from pathlib import Path
import sys
from typing import List, Optional
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

# 將 scraper 目錄加入系統路徑，以便正確匯出 Book 模型與資料庫 engine
sys.path.append(str(Path(__file__).parent.parent / "scraper"))
from models import Book, engine

app = FastAPI(title="Smart Crawler Portfolio API", version="1.0")

# 設定 CORS 跨域，讓前端 React（即使在不同連接埠或 Vercel 上）也能順利呼叫 API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 專案展示可開放所有來源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
  return {"message": "Welcome to Smart Crawler API!"}


# 1. 取得書籍列表 API（支援分頁與依評分篩選）
@app.get("/api/books", response_model=List[Book])
def get_books(
    skip: int = Query(0, description="略過幾筆"),
    limit: int = Query(20, description="回傳幾筆"),
    rating: Optional[str] = Query(None, description="依評分篩選 (例如 Three, Five)"),
):
  with Session(engine) as session:
    statement = select(Book)
    if rating:
      statement = statement.where(Book.rating == rating)
    statement = statement.offset(skip).limit(limit)
    books = session.exec(statement).all()
    return books


# 2. 取得統計數據 API（專門用來給前端 React 畫圖表用）
@app.get("/api/stats")
def get_stats():
  with Session(engine) as session:
    books = session.exec(select(Book)).all()
    total_books = len(books)

    # 計算各評分（Star Rating）的書籍數量分佈
    rating_counts = {}
    for book in books:
      rating_counts[book.rating] = rating_counts.get(book.rating, 0) + 1

    return {"total_books": total_books, "rating_distribution": rating_counts}