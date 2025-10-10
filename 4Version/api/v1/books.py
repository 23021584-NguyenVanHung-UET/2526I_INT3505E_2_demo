from flask import Blueprint, jsonify, request

bp = Blueprint('books_v1', __name__)

books = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin"},
    {"id": 2, "title": "Designing Data-Intensive Applications", "author": "Martin Kleppmann"}
]

@bp.route('/books', methods=['GET'])
def get_books_v1():
    return jsonify(books)

@bp.route('/books/<int:book_id>', methods=['GET'])
def get_book_v1(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    return jsonify(book) if book else ("Not found", 404)

@bp.route('/books', methods=['POST'])
def add_book_v1():
    data = request.get_json()
    new_book = {"id": len(books)+1, "title": data["title"], "author": data["author"]}
    books.append(new_book)
    return jsonify(new_book), 201

@bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book_v1(book_id):
    global books
    books = [b for b in books if b["id"] != book_id]
    return ("", 204)
