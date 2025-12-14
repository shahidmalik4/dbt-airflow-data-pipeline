from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class FactOrders(BaseModel):
    order_id: int
    customer_id: int
    order_date: datetime
    total_price: Optional[Decimal] = None
    total_items: Optional[int] = None
    total_amount_after_discount: Optional[Decimal] = None
    total_tax: Optional[Decimal] = None

class FactLineItem(BaseModel):
    order_id: int
    line_number: int
    part_id: int
    supplier_id: int
    quantity: int
    extended_price: Optional[Decimal] = None
    discount: Optional[Decimal] = None
    tax: Optional[Decimal] = None
    line_status: Optional[str] = None
    price_after_discount: Optional[Decimal] = None