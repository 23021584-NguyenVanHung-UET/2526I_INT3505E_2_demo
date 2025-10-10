from flask import Blueprint, request, jsonify, current_app, make_response
from services.book_service import BookService
from api.resources import BookSchema
from app import cache

api_bp = Blueprint("api", __name__)
book_schema = BookSchema()
books_schema = BookSchema(many=True)

# ==========================================================
# 📘 GET - Danh sách sách (có cache)
# ==========================================================
@api_bp.route("/books", methods=["GET"])
def list_books():
    """
    Lấy danh sách tất cả sách (có cache)
    ---
    tags:
      - Books
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        default: 1
        description: Số trang
      - name: per_page
        in: query
        type: integer
        required: false
        default: 20
        description: Số sách trên mỗi trang
    responses:
      200:
        description: Danh sách sách trả về
        schema:
          type: array
          items:
            $ref: '#/definitions/Book'
    """
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 20))
    cache_key = f"books:page={page}:per_page={per_page}"

    cached = cache.get(cache_key)
    if cached:
        resp = make_response(jsonify(cached), 200)
        resp.headers["Cache-Control"] = "public, max-age=60"
        return resp

    books = BookService.list_books(page=page, per_page=per_page)
    result = books_schema.dump(books)

    cache.set(cache_key, result, timeout=60)
    resp = make_response(jsonify(result), 200)
    resp.headers["Cache-Control"] = "public, max-age=60"
    return resp


# ==========================================================
# 📗 GET - Lấy thông tin 1 sách
# ==========================================================
@api_bp.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    """
    Lấy thông tin sách theo ID
    ---
    tags:
      - Books
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
        description: ID của sách cần lấy
    responses:
      200:
        description: Chi tiết sách
        schema:
          $ref: '#/definitions/Book'
      404:
        description: Không tìm thấy sách
    """
    book = BookService.get_book(book_id)
    if not book:
        return jsonify({"error": "Not found"}), 404

    result = book_schema.dump(book)
    resp = make_response(jsonify(result), 200)
    resp.headers["Cache-Control"] = "public, max-age=30"
    return resp


# ==========================================================
# 📙 POST - Tạo sách mới
# ==========================================================
@api_bp.route("/books", methods=["POST"])
def create_book():
    """
    Tạo sách mới
    ---
    tags:
      - Books
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/Book'
        description: Dữ liệu sách mới
    responses:
      201:
        description: Sách được tạo thành công
        schema:
          $ref: '#/definitions/Book'
      400:
        description: Dữ liệu không hợp lệ
    """
    payload = request.get_json() or {}

    try:
        book = BookService.create_book(payload)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.exception("Create book failed")
        return jsonify({"error": "Could not create"}), 400

    cache.clear()  # clear cache khi thêm mới
    return jsonify(book_schema.dump(book)), 201


# ==========================================================
# 📒 PUT - Cập nhật thông tin sách
# ==========================================================
@api_bp.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    """
    Cập nhật thông tin sách
    ---
    tags:
      - Books
    consumes:
      - application/json
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
        description: ID của sách cần cập nhật
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/Book'
        description: Dữ liệu sách cập nhật
    responses:
      200:
        description: Cập nhật thành công
        schema:
          $ref: '#/definitions/Book'
      400:
        description: Dữ liệu không hợp lệ
      404:
        description: Không tìm thấy sách
    """
    payload = request.get_json() or {}

    try:
        book = BookService.update_book(book_id, payload)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if not book:
        return jsonify({"error": "Not found"}), 404

    cache.clear()
    return jsonify(book_schema.dump(book)), 200


# ==========================================================
# 📕 DELETE - Xóa sách
# ==========================================================
@api_bp.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    """
    Xóa sách theo ID
    ---
    tags:
      - Books
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
        description: ID của sách cần xóa
    responses:
      204:
        description: Xóa thành công, không có nội dung trả về
      404:
        description: Không tìm thấy sách
    """
    ok = BookService.delete_book(book_id)
    if not ok:
        return jsonify({"error": "Not found"}), 404

    cache.clear()
    return jsonify({}), 204
