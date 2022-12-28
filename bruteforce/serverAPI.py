import aiohttp

async def login(client: aiohttp.ClientSession, username: str, password: str):
    json = {
        "username": username,
        "password": password
    }
    async with client.post('http://127.0.0.1:8888/api/login/', json=json) as resp:
        json_data = await resp.json()
        if json_data.get("status") == 'ok':
            return True
        else:
            return False
