from aiohttp import web

from speechanalytics_api import build_app


async def test_version_middleware(aiohttp_client):
    """ Add version in response headers. """
    client = await aiohttp_client(build_app)
    response = await client.get('/ping/')
    assert response.status == web.HTTPOk.status_code
    assert response.headers.get('X-API-Version') == client.app.version


async def test_firewall_middleware(aiohttp_client):
    # XXX: Нужно изменить remote у клиента.
    client = await aiohttp_client(build_app)
    response = await client.get('/ping/')
    assert response.status == web.HTTPForbidden.status_code
