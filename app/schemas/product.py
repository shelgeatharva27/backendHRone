from pydantic import BaseModel
from typing import List, Optional

class Size(BaseModel):
    size: str
    quantity: int

class ProductCreate(BaseModel):
    name: str
    price: float
    sizes: List[Size]

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    sizes: Optional[List[Size]] = None


