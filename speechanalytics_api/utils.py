import os
import hashlib
from urllib.parse import urlparse

import aiofiles
import pandas as pd
from aiohttp import ClientSession
from aiohttp_jwt import JWTMiddleware

from .middlewares.version import version_middleware
from .middlewares.firewall import firewall_middleware
from .settings import SECRET_KEY, YADISK_CALLDATA


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


async def fetch(session, url, destination=None) -> None:
    """ Fetch URL file to destination path. """
    async with session.get(url) as response:
        response.raise_for_status()     # Throw exception if not HTTP OK

        # If destination path not specified - take filename from URL
        if not destination:
            parsed_url = urlparse(url)
            destination = os.path.basename(parsed_url.path)

        # Async write response to local file
        async with aiofiles.open(destination, mode='wb') as f:
            assert await f.write(await response.content.read())


async def get_call_data(app) -> pd.DataFrame:
    """ Get latest call metadata. """
    meta = await app.yadisk.get_meta(YADISK_CALLDATA)
    filename = meta['name']
    public_url = meta['file']
    data_frame = None

    try:
        # If data file already exists - checks sha256 sums
        async with aiofiles.open(filename, 'rb') as f:
            # XXX: Blocking CPU-bound code - вынести в отдельную нитку
            local_sha256 = hashlib.sha256(await f.read()).hexdigest()
            assert local_sha256 == meta['sha256']
        data_frame = pd.read_csv(filename,
                                 delimiter=';',
                                 parse_dates=['date'])
        return data_frame

    # Download CSV file only if needed
    except (FileNotFoundError, AssertionError):
        async with ClientSession() as session:
            await fetch(session, public_url, filename)

    # TODO: Сделать чтение и парсинг дата-файла асинхронным и/или
    #   засунуть в отдельную нитку.
    if not data_frame:
        data_frame = pd.read_csv(filename, delimiter=';', parse_dates=['date'])
    # data_frame.sort('date')
    return data_frame


async def get_json_url(session, url, headers=None):
    """ Fetch URL and return native object from JSON. """
    async with session.get(url, headers=headers) as response:
        # XXX: Проверить Content-Type ответа и при необходимости выбросить исключение
        assert response.content_type == 'application/json'
        return await response.json()
