from flask import Flask, jsonify, make_response
from datetime import datetime

app = Flask(__name__)

# ==============================================
# VERSION 1: API cũ (chuẩn bị ngưng hoạt động)
# ==============================================
@app.route("/api/v1/books")
def get_books_v1():
    # Dữ liệu phiên bản cũ
    data = [
        {"id": 1, "title": "Clean Code", "author": "Robert C. Martin"}
    ]

    # Gắn thông tin cảnh báo Deprecation (chuẩn RFC 8594)
    response = make_response(jsonify(data))
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = "Wed, 01 Jan 2026 00:00:00 GMT"
    response.headers["Link"] = "<https://libraryapi.com/docs/migrate-v1-to-v2>; rel='deprecation'"
    return response


# ==============================================
# VERSION 2: API mới (đã thay đổi cấu trúc)
# ==============================================
@app.route("/api/v2/books")
def get_books_v2():
    # Thay đổi:
    # - "author" đổi thành "author_name"
    # - thêm "published_year"
    # - id từ int -> string
    data = [
        {"id": "1", "title": "Clean Code", "author_name": "Robert C. Martin", "published_year": 2008}
    ]
    return jsonify(data)


# ==============================================
# VERSION 1 đã bị gỡ bỏ hoàn toàn (giả lập)
# ==============================================
@app.route("/api/v1/removed")
def removed_v1():
    response = make_response(jsonify({
        "error": "API v1 has been retired. Please upgrade to /api/v2/books"
    }), 410)  # 410 Gone
    return response


# ==============================================
# TRANG CHÍNH (giải thích)
# ==============================================
@app.route("/")
def index():
    return jsonify({
        "message": "Welcome to Library API",
        "available_versions": ["/api/v1/books", "/api/v2/books"],
        "status": "v1 deprecated, v2 stable"
    })


if __name__ == "__main__":
    app.run(debug=True)
