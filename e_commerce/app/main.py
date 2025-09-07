from fastapi import FastAPI
from app.database import init_db
from .middleware import ResponseTimeMiddleware
from app.routers import products, cart, users

app = FastAPI()

@app.get("/")
def root():
    return {"message": "E-commerce API running"}

#app = FastAPI(title="E-Commerce API")

# Middleware
app.add_middleware(ResponseTimeMiddleware)

@app.on_event("startup")
def on_startup():
    init_db()

# Routers
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(users.router)