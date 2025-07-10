from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import BaseModel, EmailStr
from passlib.hash import bcrypt
from app.db.connection import pool

router = APIRouter()


class UserIn(BaseModel):
    email: EmailStr
    password: str
    full_name: str


@router.post("/signup")
async def signup(user: UserIn, request: Request):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT id FROM users WHERE email=%s", (user.email,))
            if await cur.fetchone():
                raise HTTPException(status_code=400, detail="Email already exists")

            hashed = bcrypt.hash(user.password)
            await cur.execute(
                "INSERT INTO users (email, password_hash, full_name) VALUES (%s, %s, %s)",
                (user.email, hashed, user.full_name)
            )
            return {"message": "User created"}
