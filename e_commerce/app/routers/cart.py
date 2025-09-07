import json
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.models import Product
from ..schemas import CartItem, CheckoutRequest, Order
from ..auth import get_current_user
from ..config import ORDERS_FILE

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/add/")
def add_to_cart(item: CartItem, session: Session = Depends(get_session)):
    product = session.get(Product, item.product_id)
    if not product or product.stock < item.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    return {"detail": f"Added {item.quantity} x {product.name} to cart."}

@router.post("/checkout/")
def checkout(payload: CheckoutRequest, current_user: str = Depends(get_current_user), session: Session = Depends(get_session)):
    total = 0
    items = []
    for item in payload.items:
        product = session.get(Product, item.product_id)
        if not product or product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for {item.product_id}")
        product.stock -= item.quantity
        session.add(product)
        total += product.price * item.quantity
        items.append(item.dict())
    session.commit()

    order = Order(user=current_user, items=items, total=total)
    # Save to orders.json
    orders = []
    p = Path(ORDERS_FILE)
    if p.exists():
        orders = json.loads(p.read_text())
    orders.append(order.dict())
    p.write_text(json.dumps(orders, indent=2))

    return {"detail": "Order placed", "total": total}
