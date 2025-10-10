# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY
from models import db, Book, BorrowRecord
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SECRET_KEY'] = SECRET_KEY

    db.init_app(app)

    @app.route("/")
    def index():
        books = Book.query.order_by(Book.title).all()
        return render_template("index.html", books=books)

    # Create book (form)
    @app.route("/books/new", methods=["GET", "POST"])
    def create_book():
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            author = request.form.get("author", "").strip()
            try:
                total_copies = int(request.form.get("total_copies", "1"))
            except ValueError:
                total_copies = 1

            if not title:
                flash("Tiêu đề sách không được để trống.", "danger")
                return redirect(url_for("create_book"))

            new_book = Book(
                title=title,
                author=author,
                total_copies=max(1, total_copies),
                available_copies=max(1, total_copies)
            )
            db.session.add(new_book)
            db.session.commit()
            flash("Đã thêm sách mới.", "success")
            return redirect(url_for("index"))

        return render_template("book_form.html", action="Create", book=None)

    # Edit book
    @app.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
    def edit_book(book_id):
        book = Book.query.get_or_404(book_id)
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            author = request.form.get("author", "").strip()
            try:
                total_copies = int(request.form.get("total_copies", book.total_copies))
            except ValueError:
                total_copies = book.total_copies

            if not title:
                flash("Tiêu đề sách không được để trống.", "danger")
                return redirect(url_for("edit_book", book_id=book.id))

            # Adjust available_copies if total_copies changed
            diff = total_copies - book.total_copies
            book.title = title
            book.author = author
            book.total_copies = max(1, total_copies)
            book.available_copies = max(0, book.available_copies + diff)
            db.session.commit()
            flash("Cập nhật thông tin sách thành công.", "success")
            return redirect(url_for("index"))

        return render_template("book_form.html", action="Edit", book=book)

    # Delete book
    @app.route("/books/<int:book_id>/delete", methods=["POST"])
    def delete_book(book_id):
        book = Book.query.get_or_404(book_id)
        # optional: prevent deletion if there are active borrows
        active_borrows = BorrowRecord.query.filter_by(book_id=book.id, returned=False).count()
        if active_borrows > 0:
            flash("Không thể xóa sách. Vẫn còn bản ghi mượn chưa trả.", "warning")
            return redirect(url_for("index"))

        db.session.delete(book)
        db.session.commit()
        flash("Đã xóa sách.", "success")
        return redirect(url_for("index"))

    # Borrow a book
    @app.route("/books/<int:book_id>/borrow", methods=["POST"])
    def borrow_book(book_id):
        book = Book.query.get_or_404(book_id)
        borrower_name = request.form.get("borrower_name", "").strip()
        if not borrower_name:
            flash("Vui lòng nhập tên người mượn.", "danger")
            return redirect(url_for("index"))

        if book.available_copies < 1:
            flash("Hiện không còn bản sách nào để mượn.", "warning")
            return redirect(url_for("index"))

        book.available_copies -= 1
        borrow_record = BorrowRecord(
            borrower_name=borrower_name,
            book_id=book.id,
            borrow_date=datetime.utcnow(),
            returned=False
        )
        db.session.add(borrow_record)
        db.session.commit()
        flash(f"'{book.title}' đã được mượn bởi {borrower_name}.", "success")
        return redirect(url_for("index"))

    # List borrows
    @app.route("/borrows")
    def view_borrows():
        # show recent borrows first
        borrow_records = BorrowRecord.query.order_by(BorrowRecord.borrow_date.desc()).all()
        return render_template("borrows.html", borrow_records=borrow_records)

    # Return a book
    @app.route("/borrows/<int:borrow_id>/return", methods=["POST"])
    def return_book(borrow_id):
        record = BorrowRecord.query.get_or_404(borrow_id)
        if record.returned:
            flash("Bản ghi này đã trả rồi.", "info")
            return redirect(url_for("view_borrows"))

        record.returned = True
        record.return_date = datetime.utcnow()
        # increase available count
        book = Book.query.get(record.book_id)
        if book:
            book.available_copies += 1
        db.session.commit()
        flash(f"'{record.book.title}' đã được trả bởi {record.borrower_name}.", "success")
        return redirect(url_for("view_borrows"))

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
