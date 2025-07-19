from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class OrderItem(BaseModel):
    product_id: str
    size: str  # Include size since products have multiple sizes
    quantity: int = Field(..., gt=0)

class OrderCreate(BaseModel):
    customer_name: str
    items: List[OrderItem]

class OrderResponse(BaseModel):
    id: str
    customer_name: str
    items: List[OrderItem]
    created_at: datetime
