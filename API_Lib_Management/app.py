import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache
from flasgger import Swagger
from config import Config


db = SQLAlchemy()
migrate = Migrate()
cache = Cache()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure DB folder exists
    db_dir = os.path.join(os.path.dirname(__file__), "db")
    os.makedirs(db_dir, exist_ok=True)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)


    swagger = Swagger(app, template={
        "swagger": "2.0",
        "info": {
            "title": "📚 Library Management API",
            "description": "API quản lý thư viện (Flask + SQLAlchemy + REST + Swagger UI)",
            "version": "1.0.0",
            "contact": {
                "name": "Flask Demo",
                "url": "http://127.0.0.1:5000/apidocs",
                "email": "support@example.com"
            }
        },
        "basePath": "/api/v1",
        "schemes": ["http"],
        "definitions": {
            "Book": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "title": {"type": "string", "example": "Clean Code"},
                    "author": {"type": "string", "example": "Robert C. Martin"},
                    "isbn": {"type": "string", "example": "9780132350884"},
                    "published_date": {"type": "string", "example": "2008-08-11"},
                    "copies": {"type": "integer", "example": 5}
                }
            }
        }
    })

    from api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api/v1")


    from api.errors import register_error_handlers
    register_error_handlers(app)


    @app.route("/")
    def index():
        """Trang chính API"""
        return jsonify({
            "message": "📘 Library API - go to /apidocs to view Swagger UI",
            "links": {
                "swagger": "/apidocs",
                "books": "/api/v1/books"
            }
        })

    return app



if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
