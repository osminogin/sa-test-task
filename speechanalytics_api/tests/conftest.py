import pytest

from speechanalytics_api import build_app


@pytest.fixture(scope='function')
async def async_client(aiohttp_client):
    return await aiohttp_client(build_app)
