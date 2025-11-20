from flask import Flask, request, jsonify

app = Flask(__name__)

# 🧠 Cách 1: Version bằng Accept Header
@app.route('/api/books/accept')
def get_books_accept():
    accept = request.headers.get("Accept", "")
    
    if "vnd.library.v2" in accept:
        # Version 2
        return jsonify([
            {"id": 1, "title": "Clean Code", "author_name": "Robert C. Martin", "published_year": 2008}
        ])
    else:
        # Version 1 (mặc định)
        return jsonify([
            {"id": 1, "title": "Clean Code", "author": "Robert C. Martin"}
        ])
# Version 1 (default)
# curl http://localhost:5000/api/books/accept

# Version 2
# curl -H "Accept: application/vnd.library.v2+json" http://localhost:5000/api/books/accept

# 🧠 Cách 2: Version bằng Custom Header (X-API-Version)
@app.route('/api/books/custom')
def get_books_custom():
    version = request.headers.get("X-API-Version", "1")
    
    if version == "2":
        # Version 2
        return jsonify([
            {"id": 1, "title": "Clean Code", "author_name": "Robert C. Martin", "published_year": 2008}
        ])
    else:
        # Version 1
        return jsonify([
            {"id": 1, "title": "Clean Code", "author": "Robert C. Martin"}
        ])
# Version 1 (default)
#curl http://localhost:5000/api/books/custom

# Version 2
#curl -H "X-API-Version: 2" http://localhost:5000/api/books/custom
if __name__ == "__main__":
    app.run(debug=True)
