import aiomysql
from fastapi import FastAPI

MYSQL_CONFIG = {
    "host": "mysql",
    "port": 3306,
    "user": "root",
    "password": "password",
    "db": "shopsphere",
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