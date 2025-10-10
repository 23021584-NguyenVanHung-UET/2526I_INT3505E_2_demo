from marshmallow import Schema, fields

class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    isbn = fields.Str(allow_none=True)
    published_date = fields.Date(allow_none=True)
    copies = fields.Int()
    created_at = fields.DateTime(dump_only=True)
    _links = fields.Method("get_links", dump_only=True)

    def get_links(self, obj):
        return {
            "self": f"/api/v1/books/{obj.id}",
            "collection": "/api/v1/books"
        }

BookSchema.definition = {
    "Book": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "title": {"type": "string"},
            "author": {"type": "string"},
            "isbn": {"type": "string"},
            "published_date": {"type": "string", "format": "date"},
            "copies": {"type": "integer"}
        }
    }
}
