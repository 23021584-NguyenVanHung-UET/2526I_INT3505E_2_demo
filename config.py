
import os

MYSQL_USER = "libuser"
MYSQL_PASSWORD = "libpassword"
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DB = "library_demo"

SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ.get("LIB_SECRET_KEY", "dev-secret-key")
