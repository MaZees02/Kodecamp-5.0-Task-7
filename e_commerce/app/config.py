import os

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
DATABASE_URL = "sqlite:///./ecommerce.db"
ORDERS_FILE = "orders.json"
LOG_FILE = "logs/app.log"