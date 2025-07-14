import aiomysql
from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.db.connection import pool

router = APIRouter()


class AddToCart(BaseModel):
    user_id: int
    product_variant_id: int
    quantity: int


@router.post("/add")
async def add_to_cart(data: AddToCart):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            # Get or create active cart
            await cur.execute("SELECT id FROM carts WHERE user_id = %s AND is_active = TRUE", (data.user_id,))
            cart = await cur.fetchone()
            if not cart:
                await cur.execute("INSERT INTO carts (user_id) VALUES (%s)", (data.user_id,))
                await cur.execute("SELECT LAST_INSERT_ID()")
                cart_id = (await cur.fetchone())[0]
            else:
                cart_id = cart[0]

            # Insert or update cart item
            await cur.execute("""
                              INSERT INTO cart_items (cart_id, product_variant_id, quantity)
                              VALUES (%s, %s, %s) ON DUPLICATE KEY
                              UPDATE quantity = quantity +
                              VALUES (quantity)
                              """, (cart_id, data.product_variant_id, data.quantity))

            return {"message": "Item added to cart"}


@router.get("/{user_id}")
async def get_cart(user_id: int):
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("""
                              SELECT p.title, pv.variant_name, ci.quantity, pv.price
                              FROM cart_items ci
                                       JOIN carts c ON ci.cart_id = c.id
                                       JOIN product_variants pv ON ci.product_variant_id = pv.id
                                       JOIN products p ON pv.product_id = p.id
                              WHERE c.user_id = %s
                                AND c.is_active = TRUE
                              """, (user_id,))
            return await cur.fetchall()
