from flask import Blueprint, jsonify, request, make_response, url_for
import hashlib
import json

bp = Blueprint('books_v4', __name__)

books = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin"},
    {"id": 2, "title": "Designing Data-Intensive Applications", "author": "Martin Kleppmann"}
]

def generate_etag(data):
    return hashlib.sha1(json.dumps(data, sort_keys=True).encode()).hexdigest()

@bp.route('/books', methods=['GET'])
def get_books_v4():
    etag = generate_etag(books)
    if request.headers.get('If-None-Match') == etag:
        return make_response('', 304)
    response = make_response(jsonify({
        "data": books,
        "meta": {"count": len(books)},
        "links": {"self": url_for('books_v4.get_books_v4')}
    }))
    response.headers['ETag'] = etag
    response.headers['Cache-Control'] = 'public, max-age=60'
    return response
