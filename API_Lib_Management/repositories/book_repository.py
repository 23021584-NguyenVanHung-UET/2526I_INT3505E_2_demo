from app import db
from models.models import Book
from sqlalchemy.exc import IntegrityError

class BookRepository:
    @staticmethod
    def get_all(offset=0, limit=50):
        return Book.query.offset(offset).limit(limit).all()

    @staticmethod
    def get_by_id(book_id):
        return Book.query.get(book_id)

    @staticmethod
    def get_by_isbn(isbn):
        return Book.query.filter_by(isbn=isbn).first()

    @staticmethod
    def create(data):
        book = Book(**data)
        db.session.add(book)
        try:
            db.session.commit()
            return book
        except IntegrityError:
            db.session.rollback()
            raise

    @staticmethod
    def update(book, data):
        for k, v in data.items():
            setattr(book, k, v)
        db.session.commit()
        return book

    @staticmethod
    def delete(book):
        db.session.delete(book)
        db.session.commit()
