from aiohttp import web

from db import fetch_user
from utils import hash_password


async def login_handler(request: web.Request) -> web.Response:
    post = await request.json()
    username = post['username']
    password = post['password']
    hashed_password = hash_password(password)
    db = request.config_dict["DB"]
    user = await fetch_user(db, username=username, hashed_password=hashed_password)
    if user:
        return web.json_response({
            'status': 'ok',
            'username': user.get('username'),
            'secret_data': user.get('secret_data')
        })
    else:
        return web.json_response({
            'status': 'error',
            'error': {
                'auth': "User not found!"
            }
        })