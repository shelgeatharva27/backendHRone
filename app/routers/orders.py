from fastapi import APIRouter, status, HTTPException
from app.schemas.order import OrderCreate
from app.db import orders_collection, products_collection
from bson import ObjectId
from datetime import datetime

router = APIRouter()

# ✅ CREATE ORDER with inventory validation
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):
    updated_products = []

    # Step 1: Check and update inventory
    for item in order.items:
        product = await products_collection.find_one({"_id": ObjectId(item.product_id)})

        if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} not found")

        sizes = product.get("sizes", [])
        size_found = False

        for size in sizes:
            if size["size"] == item.size:
                size_found = True
                if size["quantity"] < item.quantity:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Not enough stock for product {product['name']} - size {item.size}"
                    )
                size["quantity"] -= item.quantity
                break

        if not size_found:
            raise HTTPException(
                status_code=400,
                detail=f"Size {item.size} not available for product {product['name']}"
            )

        updated_products.append({
            "id": product["_id"],
            "sizes": sizes
        })

    # Step 2: Update products in DB
    for updated in updated_products:
        await products_collection.update_one(
            {"_id": updated["id"]},
            {"$set": {"sizes": updated["sizes"]}}
        )

    # Step 3: Save the order
    order_doc = {
        "customer_name": order.customer_name,
        "items": [item.dict() for item in order.items],
        "created_at": datetime.utcnow()
    }

    result = await orders_collection.insert_one(order_doc)

    return {"id": str(result.inserted_id), "message": "Order placed successfully"}


# ✅ LIST ORDERS
@router.get("/")
async def list_orders():
    cursor = orders_collection.find()
    orders = []
    async for order in cursor:
        orders.append({
            "id": str(order["_id"]),
            "customer_name": order.get("customer_name", "N/A"),
            "items": order.get("items", []),
            "created_at": order.get("created_at")
        })
    return {"data": orders}
