
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=True)
    total_copies = db.Column(db.Integer, default=1, nullable=False)
    available_copies = db.Column(db.Integer, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Book {self.id} {self.title}>"

class BorrowRecord(db.Model):
    __tablename__ = "borrow_records"
    id = db.Column(db.Integer, primary_key=True)
    borrower_name = db.Column(db.String(255), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=True)
    returned = db.Column(db.Boolean, default=False)

    # relationship convenience
    book = db.relationship("Book", backref=db.backref("borrow_records", lazy=True))

    def __repr__(self):
        return f"<BorrowRecord {self.id} {self.borrower_name} Book:{self.book_id}>"
