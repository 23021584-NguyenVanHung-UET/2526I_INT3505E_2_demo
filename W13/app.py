from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Fake database in memory
books = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin"},
    {"id": 2, "title": "The Pragmatic Programmer", "author": "Andrew Hunt"},
]

# ---------------------------
# Routes
# ---------------------------

@app.route("/")
def home():
    return jsonify({"message": "Book API is running"})

# GET all books
@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books)

# GET book by ID
@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        return jsonify(book)
    return jsonify({"error": "Book not found"}), 404

# Create new book
@app.route("/books", methods=["POST"])
def create_book():
    data = request.json
    new_id = max([b["id"] for b in books]) + 1 if books else 1
    new_book = {
        "id": new_id,
        "title": data.get("title"),
        "author": data.get("author")
    }
    books.append(new_book)
    return jsonify(new_book), 201

# Update book
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.json
    for book in books:
        if book["id"] == book_id:
            book["title"] = data.get("title", book["title"])
            book["author"] = data.get("author", book["author"])
            return jsonify(book)
    return jsonify({"error": "Book not found"}), 404

# Delete book
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books
    books = [b for b in books if b["id"] != book_id]
    return jsonify({"message": "Book deleted"})

if __name__ == "__main__":
    app.run(debug=True)
