import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load env variables from .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = AsyncIOMotorClient(MONGO_URI)
db = client["ecommerce"]  # Use 'ecommerce' DB

# Collections
products_collection = db["products"]
orders_collection = db["orders"]
