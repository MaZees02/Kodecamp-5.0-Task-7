import os

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production-please")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# Data & Files
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./students.db")
USERS_FILE = os.getenv("USERS_FILE", "users.json")
LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")

# CORS
ALLOWED_ORIGINS = ["http://localhost:3000"]
