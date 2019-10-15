import pytest
from aiohttp import web

from speechanalytics_api import build_app


async def test_version_middleware(aiohttp_client) -> None:
    """ Add version in response headers. """
    client = await aiohttp_client(build_app)
    response = await client.get('/ping')
    assert response.status == web.HTTPOk.status_code
    assert response.headers.get('X-API-Version') == client.app.version


@pytest.mark.skip(reason='Нужно мокать remote_ip запроса, что бы получить Forbidden')
async def test_firewall_middleware(aiohttp_client) -> None:
    """ Checks firewall middleware restrictions. """
    client = await aiohttp_client(build_app)
    response = await client.get('/ping')
    assert response.status == web.HTTPForbidden.status_code


@pytest.mark.parametrize('test_url', ['/ping/', '/health/', '/ping///'])
async def test_remove_middleware(aiohttp_client, test_url) -> None:
    """ Must redirect to URL without trailing slashes. """
    client = await aiohttp_client(build_app)
    response = await client.get(test_url)
    assert response.url.path == test_url.rstrip('/')
