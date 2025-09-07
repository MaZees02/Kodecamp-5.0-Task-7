from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from ..models import Product
from ..schemas import ProductCreate, ProductRead
from ..auth import get_current_user
from fastapi import APIRouter

# Create router
router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/")
def get_products():
    return {"message": "List of products"}

#router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=list[ProductRead])
def list_products(session: Session = Depends(get_session)):
    return session.exec(select(Product)).all()

@router.post("/admin/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, session: Session = Depends(get_session), current_user: str = Depends(get_current_user)):
    # simple admin check (username == "admin")
    if current_user != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    product = Product(**payload.dict())
    session.add(product)
    session.commit()
    session.refresh(product)
    return product
