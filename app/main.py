import os
from fastapi import FastAPI

from app.api.v1 import users, products, cart

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello From ShopSphere"}

app.include_router(users.router, prefix="/api/v1/users")
app.include_router(products.router, prefix="/api/v1/products")
app.include_router(cart.router, prefix="/api/v1/cart")
