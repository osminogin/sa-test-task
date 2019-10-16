import os
import hashlib
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

import aiofiles
import pandas as pd
from aiohttp import ClientSession, web
from aiohttp_jwt import JWTMiddleware

from .middlewares.version import version_middleware
from .middlewares.firewall import firewall_middleware
from .middlewares.remove_slash import remove_slash_middleware
from .settings import SECRET_KEY, YADISK_CALLDATA, WHITELIST_URLS


def get_middlewares() -> tuple:
    """ List of active middlewares. """
    middlewares = (
        version_middleware,
        firewall_middleware,
        remove_slash_middleware,
        JWTMiddleware(SECRET_KEY, whitelist=WHITELIST_URLS),
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


async def get_call_data(app, columns: list = None) -> pd.DataFrame:
    """ Get latest call metadata. """
    meta = await app.yadisk.get_meta(YADISK_CALLDATA)
    filename = meta['name']
    public_url = meta['file']
    data_frame = None

    def get_data_frame(cols: list = None) -> pd.DataFrame:
        """ Parse CSV with Pandas. """
        return pd.read_csv(
            filename, delimiter=';', parse_dates=['date'],
            # index_col=['call_id', 'date'],
            dtype={'duration_answer': 'int32'},
            # XXX: Неработает - почему-то все равно тип объект в полях
            converters={
                'call_id': str,
                'filename': str,
                'status': str,
                'type': str,
                'phone_number_operator': str,
                'name_operator': str,
                'phone_number_client': str,
            }
        )

    def get_sha256_sum(file_name: str) -> str:
        """ Ckecksum of file object with sha256 hash function. """
        # TODO: Хорошо бы сделать буферизованное чтение и обновление
        #   блоков хеш-функции.
        with open(file_name, 'rb') as file:
            return hashlib.sha256(file.read()).hexdigest()

    try:
        # Blocking CPU-bound code runs async (another thread)
        with ThreadPoolExecutor() as pool:
            # If data file already exists - checks sha256 sums
            result = await app.loop.run_in_executor(pool,
                                                    get_sha256_sum, filename)
            assert result == meta['sha256']

        # I/O bound function also non blocks main event loop
        with ThreadPoolExecutor() as pool:
            df = await app.loop.run_in_executor(pool,
                                                get_data_frame, columns)
            return df

    # Download/redownload CSV file only if needed
    except (FileNotFoundError, AssertionError):
        async with ClientSession() as session:
            await fetch(session, public_url, filename)

    return get_data_frame(columns) if not data_frame else data_frame


async def get_json_url(session, url, headers=None) -> (dict, list):
    """ Fetch URL and return native object from JSON. """
    async with session.get(url, headers=headers) as response:
        # Check valid `Content-Type` for JSON response
        assert response.content_type == 'application/json'
        return await response.json()


async def redirect_handler(request):
    """ Redirect to some page. """
    raise web.HTTPFound(location='/health')
