from flask import Flask
from api.v1.books import bp as books_v1
from api.v2.books import bp as books_v2
from api.v3.books import bp as books_v3
from api.v4.books import bp as books_v4

app = Flask(__name__)
app.register_blueprint(books_v1, url_prefix="/api/v1")
app.register_blueprint(books_v2, url_prefix="/api/v2")
app.register_blueprint(books_v3, url_prefix="/api/v3")
app.register_blueprint(books_v4, url_prefix="/api/v4")

if __name__ == '__main__':
    app.run(debug=True)
