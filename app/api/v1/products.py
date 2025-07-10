from fastapi import APIRouter, Request
from sqlalchemy.dialects.mysql import aiomysql

from app.db.connection import pool

router = APIRouter()

@router.get("/")
async def list_products():
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT * FROM products WHERE is_active = TRUE")
            return await cur.fetchall()

@router.get("/{product_id}")
async def product_detail(product_id: int):
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            product = await cur.fetchone()
            if not product:
                return {"error": "Product not found"}
            return product
