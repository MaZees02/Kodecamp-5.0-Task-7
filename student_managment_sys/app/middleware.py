import logging
import time
from pathlib import Path
from fastapi import Request

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

# Configure logging
logging.basicConfig(filename="app.log", level=logging.INFO)

class RequestLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logging.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        return response

