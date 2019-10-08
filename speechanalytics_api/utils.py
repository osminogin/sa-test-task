import aiofiles
from aiohttp_jwt import JWTMiddleware

from .middlewares.version import version_middleware
from .middlewares.firewall import firewall_middleware
from .settings import SECRET_KEY


def get_middlewares() -> tuple:
    middlewares = (
        version_middleware,
        firewall_middleware,
        JWTMiddleware(SECRET_KEY, whitelist=[r'/ping/', r'/health/']),
    )
    return middlewares


async def get_version() -> str:
    async with aiofiles.open('VERSION', mode='r') as f:
        version = await f.readline()
        version = version.rstrip('\n')
    return version
