from aiohttp import web

from db import try_make_db, init_db
from handlers import login_handler


async def init_app() -> web.Application:
    app = web.Application()
    app.add_routes([web.post("/api/login/", login_handler)])
    app.cleanup_ctx.append(init_db)
    return app


try_make_db()
web.run_app(init_app(), host='127.0.0.1', port=8888)