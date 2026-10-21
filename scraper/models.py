from pathlib import Path
from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select

# 取得專案根目錄的絕對路徑，確保爬蟲與後端讀寫同一顆資料庫
BASE_DIR = Path(__file__).resolve().parent.parent
sqlite_file_name = BASE_DIR / "books.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=False)


class Book(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  title: str = Field(index=True, unique=True)
  price: str
  rating: str


def init_db():
  SQLModel.metadata.create_all(engine)


def save_books_to_db(books_data: list[dict]):
  init_db()
  new_count = 0
  updated_count = 0

  with Session(engine) as session:
    for item in books_data:
      statement = select(Book).where(Book.title == item["title"])
      existing_book = session.exec(statement).first()

      if existing_book:
        if (
            existing_book.price != item["price"]
            or existing_book.rating != item["rating"]
        ):
          existing_book.price = item["price"]
          existing_book.rating = item["rating"]
          session.add(existing_book)
          updated_count += 1
      else:
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