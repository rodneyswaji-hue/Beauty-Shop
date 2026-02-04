from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.user import User
from app.schemas.order import OrderCreate, OrderOut, OrderUpdate
from app.core.security import get_current_user
from app.services.pdf_service import pdf_service
from app.services.email_service import email_service
import io

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])

@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Create order
    db_order = Order(
        user_id=current_user.id,
        total_price=order.total_price,
        status="pending",
        phone_number=order.phone_number
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Create order items
    for item in order.items:
        db_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_order)
    
    # Send order confirmation email
    try:
        email_service.send_order_confirmation(
            current_user.email,
            f"ORD-{db_order.id:03d}",
            float(db_order.total_price)
        )
    except Exception as e:
        print(f"Failed to send confirmation email: {e}")
    
    return db_order

@router.get("/", response_model=List[OrderOut])
def get_user_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return orders

@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check if user owns the order or is admin
    if order.user_id != current_user.id and not current_user.is_Admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return order

@router.get("/{order_id}/invoice")
def download_invoice(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check if user owns the order or is admin
    if order.user_id != current_user.id and not current_user.is_Admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Prepare order data for PDF
    order_data = {
        'id': f"ORD-{order.id:03d}",
        'status': order.status,
        'customer_name': f"{order.user.first_name} {order.user.last_name}",
        'customer_email': order.user.email,
        'total_amount': float(order.total_price),
        'items': [
            {
                'name': item.product.name,
                'quantity': item.quantity,
                'price': float(item.price),
                'total_price': float(item.price * item.quantity)
            }
            for item in order.items
        ]
    }
    
    # Generate PDF
    pdf_buffer = pdf_service.generate_invoice(order_data)
    
    return StreamingResponse(
        io.BytesIO(pdf_buffer.read()),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=invoice-{order.id}.pdf"}
    )

@router.put("/{order_id}/status", response_model=OrderOut)
def update_order_status(
    order_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_Admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    old_status = order.status
    order.status = order_update.status
    if order_update.mpesa_receipt:
        order.mpesa_receipt = order_update.mpesa_receipt
    
    db.commit()
    db.refresh(order)
    
    # Send status update email if status changed
    if old_status != order.status:
        try:
            email_service.send_order_status_update(
                order.user.email,
                f"ORD-{order.id:03d}",
                order.status
            )
        except Exception as e:
            print(f"Failed to send status update email: {e}")
    
    return order

@router.delete("/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_Admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Delete order items first
    db.query(OrderItem).filter(OrderItem.order_id == order_id).delete()
    
    # Delete order
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}

@router.get("/admin/all", response_model=List[OrderOut])
def get_all_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_Admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    orders = db.query(Order).offset(skip).limit(limit).all()
    return orders