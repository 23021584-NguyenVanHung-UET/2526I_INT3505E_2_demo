import logging
import time
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
# Thư viện Rate Limit
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
# Thư viện Monitoring
from prometheus_fastapi_instrumentator import Instrumentator

# --- 1. CẤU HÌNH LOGGING ---
# Tạo logger
logger = logging.getLogger("my_app_logger")
logger.setLevel(logging.INFO)

# Format log: Thời gian - Mức độ - Message
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Handler 1: Ghi ra File (tương tự winston.transports.File)
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(formatter)

# Handler 2: Ghi ra Console (tương tự winston.transports.Console)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Add handlers vào logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# --- 2. CẤU HÌNH RATE LIMIT ---
# Lấy địa chỉ IP của người dùng để làm key giới hạn
limiter = Limiter(key_func=get_remote_address)


# --- 3. KHỞI TẠO APP ---
app = FastAPI()

# Đăng ký handler lỗi cho Rate Limit (để trả về JSON đẹp thay vì lỗi mặc định)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# --- 4. CẤU HÌNH MONITORING (PROMETHEUS) ---
# Tự động đo lường tất cả request và expose endpoint /metrics
Instrumentator().instrument(app).expose(app)


# --- 5. MIDDLEWARE LOGGING THỦ CÔNG ---
# Ghi log mỗi khi có request mới (tương tự middleware trong Express)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Xử lý request
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    logger.info(f"Path: {request.url.path} - Method: {request.method} - Status: {response.status_code} - Time: {process_time:.2f}ms")
    
    return response


# --- 6. ROUTES (API ENDPOINTS) ---

@app.get("/")
def read_root():
    logger.info("Truy cập trang chủ")
    return {"message": "Hello World from Python!"}

@app.get("/heavy-task")
@limiter.limit("5/minute") # Giới hạn 5 request mỗi phút cho API này
def heavy_task(request: Request):
    logger.info("Đang xử lý tác vụ nặng...")
    # Giả lập xử lý
    return {"message": "Xử lý xong tác vụ nặng", "data": [1, 2, 3]}

@app.get("/error")
def trigger_error():
    try:
        # Giả lập lỗi
        result = 1 / 0
    except Exception as e:
        logger.error(f"Đã xảy ra lỗi nghiêm trọng: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})

if __name__ == "__main__":
    # Chạy server tại localhost:8000
    uvicorn.run(app, host="0.0.0.0", port=8000)