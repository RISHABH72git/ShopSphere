import os

import aiomysql
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_CONFIG = {
    "host": MYSQL_HOST,
    "port": int(MYSQL_PORT),
    "user": MYSQL_USER,
    "password": MYSQL_PASSWORD,
    "db": MYSQL_DB,
    "autocommit": True
}

pool = None


async def init_db(app: FastAPI):
    global pool
    pool = await aiomysql.create_pool(**MYSQL_CONFIG)
    app.state.db = pool


async def close_db(app: FastAPI):
    app.state.db.close()
    await app.state.db.wait_closed()
