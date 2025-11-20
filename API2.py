from flask import Flask, jsonify, request, make_response
from flasgger import Swagger, swag_from

app = Flask(__name__)

# =====================================================
# 🔧 Cấu hình Swagger UI
# =====================================================
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "swagger_ui": True,
    "specs_route": "/docs/"   # 👉 Truy cập Swagger tại: http://127.0.0.1:5000/docs/
}

swagger = Swagger(app, config=swagger_config)


# =====================================================
# 🧾 API VERSION 1 (Cũ) — Sẽ bị Deprecation
# =====================================================
@app.route("/api/v1/payments", methods=["POST"])
@swag_from({
    "tags": ["Payments v1"],
    "description": "Xử lý thanh toán theo chuẩn API v1 (sắp bị deprecate).",
    "parameters": [
        {
            "in": "body",
            "name": "body",
            "schema": {
                "type": "object",
                "properties": {
                    "amount_vnd": {"type": "number"}
                },
                "required": ["amount_vnd"]
            }
        }
    ],
    "responses": {
        200: {
            "description": "Thanh toán thành công (V1)"
        }
    }
})
def payment_v1():
    data = request.json

    response_body = {
        "status": "ok",
        "message": "Payment processed (V1)",
        "received_field": list(data.keys())
    }

    # Header cảnh báo Deprecation
    resp = make_response(jsonify(response_body))
    resp.headers["Deprecation"] = "true"
    resp.headers["Sunset"] = "Wed, 01 May 2026 00:00:00 GMT"
    resp.headers["Link"] = "<https://docs.payhub.com/migrate-v1-to-v2>; rel='deprecation'"
    resp.headers["Warning"] = '299 - "API v1 sẽ bị gỡ bỏ sau 2026-05-01. Vui lòng chuyển sang /api/v2."'
    return resp


# =====================================================
# 💳 API VERSION 2 (Mới)
# =====================================================
@app.route("/api/v2/payments", methods=["POST"])
@swag_from({
    "tags": ["Payments v2"],
    "description": "Xử lý thanh toán theo chuẩn API v2 (amount + currency).",
    "parameters": [
        {
            "in": "body",
            "name": "body",
            "schema": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number"},
                    "currency": {"type": "string"}
                },
                "required": ["amount"]
            }
        }
    ],
    "responses": {
        200: {"description": "Payment processed (V2)"}
    }
})
def payment_v2():
    data = request.json
    response = {
        "success": True,
        "transaction_id": "TXN-123456",
        "amount": data.get("amount"),
        "currency": data.get("currency", "VND")
    }
    return jsonify(response)


# =====================================================
# 💸 REFUND API (mới trong v2)
# =====================================================
@app.route("/api/v2/refunds", methods=["POST"])
@swag_from({
    "tags": ["Refund v2"],
    "description": "API hoàn tiền mới của phiên bản v2.",
    "parameters": [
        {
            "in": "body",
            "name": "body",
            "schema": {
                "type": "object",
                "properties": {
                    "transaction_id": {"type": "string"}
                },
                "required": ["transaction_id"]
            }
        }
    ],
    "responses": {
        200: {"description": "Refund processed"}
    }
})
def refund_v2():
    data = request.json
    return jsonify({
        "success": True,
        "refund_id": "RFD-9876",
        "original_txn": data.get("transaction_id"),
    })


# =====================================================
# 🏁 Run App
# =====================================================
if __name__ == "__main__":
    app.run(debug=True)
