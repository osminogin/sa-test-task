from aiohttp import web

from speechanalytics_api import build_app


async def test_version_middleware(aiohttp_client):
    client = await aiohttp_client(build_app)
    response = await client.get('/ping/')
    assert response.status == web.HTTPOk.status_code
    assert response.headers.get('X-API-Version') == client.app.version

# XXX: Сделать проверку firewall_middleware (нужно изменить remote у клиента)
