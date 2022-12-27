import hashlib
from pathlib import Path
from typing import AsyncIterator
import aiosqlite
import sqlite3

from aiohttp import web


def get_db_path() -> Path:
    here = Path.cwd()
    while not (here / ".git").exists():
        if here == here.parent:
            raise RuntimeError("Cannot find root github dir")
        here = here.parent

    return here / "db.sqlite3"


async def init_db(app: web.Application) -> AsyncIterator[None]:
    sqlite_db = get_db_path()
    db = await aiosqlite.connect(sqlite_db)
    db.row_factory = aiosqlite.Row
    app["DB"] = db
    yield
    await db.close()


async def fetch_user(
        db: aiosqlite.Connection,
        username: str,
        hashed_password: str
):
    async with db.execute(
            "SELECT username, secret_data FROM users WHERE username = ? and password = ?",
            [username, hashed_password]
    ) as cursor:
        row = await cursor.fetchone()
        if row is None:
            return False
        else:
            return {
                'username': row['username'],
                'secret_data': row['secret_data']
            }


def try_make_db() -> None:
    sqlite_db = get_db_path()
    if sqlite_db.exists():
        print('db exist!')
        return

    with sqlite3.connect(sqlite_db) as conn:
        cur = conn.cursor()
        cur.execute(
            """CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password CHAR(64),
            secret_data TEXT
            )
        """
        )
        login = 'ssudarikov'
        password_not_hashed = 'qmiLT4O5S0bTYZc'
        password_hashed = hashlib.sha256(password_not_hashed.encode()).hexdigest()
        cur.execute(
            """INSERT INTO users (username, password, secret_data) VALUES (?, ?, ?)""",
            (login, password_hashed, 'I very love Cookies!')
        )
        login = 'ftromp'
        password_not_hashed = 'phasXR'
        password_hashed = hashlib.sha256(password_not_hashed.encode()).hexdigest()
        cur.execute(
            """INSERT INTO users (username, password, secret_data) VALUES (?, ?, ?)""",
            (login, password_hashed, 'I very love Milk!')
        )

        conn.commit()
