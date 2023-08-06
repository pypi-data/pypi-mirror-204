import env
from httpx import AsyncClient

UPLOAD_URL = "https://vgy.me/upload"
PARAMS = {"userkey": env.get("VGY_KEY")}


async def download(url: str) -> bytes:
    async with AsyncClient() as client:
        resp = await client.get(url)
    return resp.content


async def upload(file: bytes) -> str:
    async with AsyncClient() as client:
        resp = await client.post(
            UPLOAD_URL,
            files={"file": ("img.png", file)},
            params=PARAMS,
        )
    result = resp.json()
    if result["error"]:
        raise RuntimeError(result)
    return result["image"]
