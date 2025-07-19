from fastapi import FastAPI
from app.routers import products, orders

app = FastAPI()

# Root route (optional)
@app.get("/")
async def root():
    return {"message": "Ecommerce Backend is running!"}

# Include routers
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
