from flask import Blueprint, jsonify, request, url_for

bp = Blueprint('books_v2', __name__)

books = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin"},
    {"id": 2, "title": "Designing Data-Intensive Applications", "author": "Martin Kleppmann"}
]

@bp.route('/books', methods=['GET'])
def get_books_v2():
    response = {
        "data": books,
        "links": {"self": url_for('books_v2.get_books_v2')}
    }
    return jsonify(response)

@bp.route('/books', methods=['POST'])
def add_book_v2():
    data = request.get_json()
    new_book = {"id": len(books)+1, "title": data["title"], "author": data["author"]}
    books.append(new_book)
    return jsonify({
        "data": new_book,
        "links": {"self": url_for('books_v2.get_books_v2')}
    }), 201
