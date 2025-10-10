from flask import Blueprint, jsonify, request, url_for

bp = Blueprint('books_v3', __name__)

books = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin"},
    {"id": 2, "title": "Designing Data-Intensive Applications", "author": "Martin Kleppmann"}
]

# Middleware: log request
@bp.before_request
def log_request():
    print(f"[LayeredSystem] {request.method} {request.path}")

@bp.route('/books', methods=['GET'])
def get_books_v3():
    return jsonify({
        "data": books,
        "meta": {"count": len(books)},
        "links": {"self": url_for('books_v3.get_books_v3')}
    })
