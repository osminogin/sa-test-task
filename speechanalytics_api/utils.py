import aiofiles
from aiohttp_jwt import JWTMiddleware

from .middlewares.version import version_middleware
from .middlewares.firewall import firewall_middleware
from .settings import SECRET_KEY


def get_middlewares() -> tuple:
    """ List of active middlewares. """
    middlewares = (
        version_middleware,
        firewall_middleware,
        JWTMiddleware(SECRET_KEY, whitelist=[r'/ping/', r'/health/']),
    )
    return middlewares


async def get_version() -> str:
    """ Current version of app. """
    async with aiofiles.open('VERSION', mode='r') as f:
        version = await f.readline()
        version = version.rstrip('\n')
    return version


async def get_json_url(session, url, headers=None):
    """ Fetch URL and return native object from JSON. """
    async with session.get(url, headers=headers) as response:
        # XXX: Проверить Content-Type ответа и при необходимости выбросить исключение
        return await response.json()
