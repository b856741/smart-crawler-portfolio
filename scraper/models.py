from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select

# 定義 SQLite 資料庫檔案名稱
sqlite_file_name = "books.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=False)


# 1. 設計 Book 資料表模型
class Book(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  title: str = Field(index=True, unique=True)  # 以書名建立唯一索引，用於去重
  price: str
  rating: str


# 2. 初始化資料庫（自動建立資料表）
def init_db():
  SQLModel.metadata.create_all(engine)


# 3. 帶有「去重與增量更新」的寫入邏輯
def save_books_to_db(books_data: list[dict]):
  init_db()
  new_count = 0
  updated_count = 0

  with Session(engine) as session:
    for item in books_data:
      # 檢查資料庫是否已存在相同標題的書籍
      statement = select(Book).where(Book.title == item["title"])
      existing_book = session.exec(statement).first()

      if existing_book:
        # 若已存在，檢查內容是否有變更（增量更新）
        if (
            existing_book.price != item["price"]
            or existing_book.rating != item["rating"]
        ):
          existing_book.price = item["price"]
          existing_book.rating = item["rating"]
          session.add(existing_book)
          updated_count += 1
      else:
        # 若為新資料，則新增紀錄
        new_book = Book(
            title=item["title"], price=item["price"], rating=item["rating"]
        )
        session.add(new_book)
        new_count += 1

    session.commit()

  print(
      f"資料庫寫入完成！新增: {new_count} 筆，更新: {updated_count} 筆，忽略重複:"
      f" {len(books_data) - new_count - updated_count} 筆。"
  )