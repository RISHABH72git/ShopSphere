import uuid

from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import BaseModel, EmailStr
from passlib.hash import bcrypt
from app.db import connection

router = APIRouter()


class UserIn(BaseModel):
    email: EmailStr
    password: str
    full_name: str


@router.post("/signup")
async def signup(user: UserIn):
    async with connection.pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT id FROM users WHERE email=%s", (user.email,))
            if await cur.fetchone():
                raise HTTPException(status_code=400, detail="Email already exists")

            hashed = bcrypt.hash(user.password)
            id = str(uuid.uuid4())
            await cur.execute(
                "INSERT INTO users (id, email, password_hash, full_name) VALUES (%s, %s, %s, %s)",
                (id, user.email, hashed, user.full_name)
            )
            return {"message": "User created", "data": {"id": id}}
