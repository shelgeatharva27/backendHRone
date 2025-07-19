from fastapi import APIRouter, status, Query, HTTPException
from app.schemas.product import ProductCreate, ProductUpdate
from app.db import products_collection
from bson import ObjectId
from typing import Optional
from fastapi.encoders import jsonable_encoder

router = APIRouter()

# ✅ CREATE PRODUCT
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    product_dict = product.dict()
    result = await products_collection.insert_one(product_dict)
    return {"id": str(result.inserted_id)}

# ✅ LIST PRODUCTS with pagination and filtering
@router.get("/")
async def list_products(
    name: Optional[str] = Query(None, description="Filter by product name"),
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0)
):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}  # case-insensitive match

    cursor = products_collection.find(query).skip(skip).limit(limit)
    products = []
    async for product in cursor:
        products.append({
            "id": str(product["_id"]),
            "name": product.get("name", "N/A"),
            "price": product.get("price", 0.0)
        })

    return {
        "data": products,
        "page": {
            "next": skip + limit,
            "previous": max(skip - limit, 0),
            "limit": limit
        }
    }

# ✅ UPDATE PRODUCT
@router.put("/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(product_id: str, product: ProductUpdate):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")

    update_data = {k: v for k, v in product.dict(exclude_unset=True).items()}
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided for update")

    result = await products_collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": jsonable_encoder(update_data)}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Product not found or no change made")

    return {"message": "Product updated successfully"}
