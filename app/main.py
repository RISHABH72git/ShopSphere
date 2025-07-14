import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1 import users, products, cart
from app.db.connection import init_db

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting application...")
    await init_db(app)
    yield  # control passes to FastAPI app
    print("Shutting down application...")


# Create app with lifespan
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello From ShopSphere"}

app.include_router(users.router, prefix="/api/v1/users")
app.include_router(products.router, prefix="/api/v1/products")
app.include_router(cart.router, prefix="/api/v1/cart")
