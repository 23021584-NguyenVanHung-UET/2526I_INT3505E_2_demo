from repositories.book_repository import BookRepository
from datetime import datetime

class BookService:
    @staticmethod
    def list_books(page=1, per_page=20):
        offset = (page - 1) * per_page
        books = BookRepository.get_all(offset=offset, limit=per_page)
        return books

    @staticmethod
    def get_book(book_id):
        return BookRepository.get_by_id(book_id)

    @staticmethod
    def create_book(payload):
        # validation/business rules
        if "title" not in payload or "author" not in payload:
            raise ValueError("title and author required")
        # optional: convert published_date string to date
        if "published_date" in payload and payload["published_date"]:
            try:
                payload["published_date"] = datetime.fromisoformat(payload["published_date"]).date()
            except Exception:
                raise ValueError("published_date must be ISO date YYYY-MM-DD")
        return BookRepository.create(payload)

    @staticmethod
    def update_book(book_id, payload):
        book = BookRepository.get_by_id(book_id)
        if not book:
            return None
        if "published_date" in payload and payload["published_date"]:
            try:
                payload["published_date"] = datetime.fromisoformat(payload["published_date"]).date()
            except Exception:
                raise ValueError("published_date must be ISO date YYYY-MM-DD")
        return BookRepository.update(book, payload)

    @staticmethod
    def delete_book(book_id):
        book = BookRepository.get_by_id(book_id)
        if not book:
            return False
        BookRepository.delete(book)
        return True
