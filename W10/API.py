from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

# =====================================================
# 🧾 API VERSION 1 (Cũ) — Sẽ bị Deprecation
# =====================================================
@app.route("/api/v1/payments", methods=["POST"])
def payment_v1():
    data = request.json

    # Giả lập xử lý thanh toán V1
    response_body = {
        "status": "ok",
        "message": "Payment processed (V1)",
        "received_field": list(data.keys())
    }

    # Tạo response kèm các header cảnh báo deprecation
    resp = make_response(jsonify(response_body))
    resp.headers["Deprecation"] = "true"
    resp.headers["Sunset"] = "Wed, 01 May 2026 00:00:00 GMT"
    resp.headers["Link"] = "<https://docs.payhub.com/migrate-v1-to-v2>; rel='deprecation'"
    resp.headers["Warning"] = '299 - "API v1 will be deprecated after 2026-05-01. Please migrate to /api/v2."'
    return resp


# =====================================================
# 💳 API VERSION 2 (Mới) — Sử dụng OAuth2 và chuẩn hoá dữ liệu
# =====================================================
@app.route("/api/v2/payments", methods=["POST"])
def payment_v2():
    data = request.json

    # Giả lập xử lý thanh toán V2
    response = {
        "success": True,
        "transaction_id": "TXN-123456",
        "amount": data.get("amount"),
        "currency": data.get("currency", "VND")
    }
    return jsonify(response)


# =====================================================
# 💸 API REFUND (Mới trong v2)
# =====================================================
@app.route("/api/v2/refunds", methods=["POST"])
def refund_v2():
    data = request.json

    # Giả lập xử lý refund
    return jsonify({
        "success": True,
        "refund_id": "RFD-9876",
        "original_txn": data.get("transaction_id"),
    })


# =====================================================
# 🧠 Ví dụ minh họa Breaking Changes
# =====================================================
# ❌ V1 dùng trường amount_vnd
# ✅ V2 dùng amount + currency

# Cách gọi thử API:
# V1 (cũ, sẽ có cảnh báo Deprecation): 
# curl -i -X POST http://127.0.0.1:5000/api/v1/payments -H "Content-Type: application/json" -d "{\"amount_vnd\": 50000}"

# V2 (mới, chuẩn hóa dữ liệu):
# curl -i -X POST http://127.0.0.1:5000/api/v2/payments -H "Content-Type: application/json" -d "{\"amount\": 50000, \"currency\": \"VND\"}"

# =====================================================
if __name__ == "__main__":
    app.run(debug=True)
# ==============================================
# W10/API.py
