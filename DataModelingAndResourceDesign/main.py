from fastapi import FastAPI, Query
from typing import List, Optional
from pydantic import BaseModel
from datetime import date
import math

app = FastAPI(title="Library API Demo")

# -------------------------
# Models
# -------------------------
class Author(BaseModel):
    id: int
    name: str

class Book(BaseModel):
    id: int
    title: str
    isbn: str
    category: str
    author: Author
    published_date: date
    copies_available: int

class PaginatedBooks(BaseModel):
    page: int
    limit: int
    total_items: int
    total_pages: int
    data: List[Book]

# -------------------------
# Sample data
# -------------------------
authors = [
    Author(id=1, name="J.K. Rowling"),
    Author(id=2, name="George R.R. Martin")
]

books = [
    Book(id=1, title="Harry Potter and the Philosopher's Stone", isbn="978-3-16-148410-0",
         category="Fantasy", author=authors[0], published_date=date(1997,6,26), copies_available=5),
    Book(id=2, title="A Game of Thrones", isbn="978-0-553-10354-0",
         category="Fantasy", author=authors[1], published_date=date(1996,8,6), copies_available=3),
    Book(id=3, title="Harry Potter and the Chamber of Secrets", isbn="978-3-16-148411-7",
         category="Fantasy", author=authors[0], published_date=date(1998,7,2), copies_available=4)
]

# -------------------------
# Search & Pagination API
# -------------------------
@app.get("/api/books", response_model=PaginatedBooks)
def search_books(
    q: Optional[str] = Query(None, description="Từ khóa tìm kiếm (title/author)"),
    category: Optional[str] = Query(None, description="Lọc theo thể loại"),
    author: Optional[str] = Query(None, description="Lọc theo tên tác giả"),
    page: int = Query(1, ge=1, description="Số trang"),
    limit: int = Query(10, ge=1, le=50, description="Số sách/trang")
):
    # Lọc dữ liệu
    results = books
    if q:
        results = [b for b in results if q.lower() in b.title.lower()]
    if category:
        results = [b for b in results if b.category.lower() == category.lower()]
    if author:
        results = [b for b in results if author.lower() in b.author.name.lower()]

    # Metadata phân trang
    total_items = len(results)
    total_pages = math.ceil(total_items / limit)

    # Phân trang
    start = (page - 1) * limit
    end = start + limit
    paged_results = results[start:end]

    return PaginatedBooks(
        page=page,
        limit=limit,
        total_items=total_items,
        total_pages=total_pages,
        data=paged_results
    )

# Optional root route
@app.get("/")
def root():
    return {"message": "Welcome to Library API Demo"}
