from datetime import date, datetime

import pytest
from aiohttp import web

from speechanalytics_api import build_app
from speechanalytics_api.utils import get_version


async def test_app_version():
    """ Проверка версии приложения и API. """
    version = await get_version()
    assert version == '0.1'


async def test_build_app(aiohttp_client) -> None:
    client = await aiohttp_client(build_app)
    app = client.app
    assert isinstance(app, web.Application)
    assert getattr(app, 'started')
    assert isinstance(app.started, date)
    assert datetime.utcnow() > app.started
    assert getattr(app, 'version')
    assert float(client.app.version)


async def test_unauthorized_access(aiohttp_client) -> None:
    """ Unauthorized access to protected methods. """
    client = await aiohttp_client(build_app)
    response = await client.get('/calls')
    assert response.status == web.HTTPUnauthorized.status_code


async def test_not_found_method(aiohttp_client, auth) -> None:
    """ Not found method. """
    client = await aiohttp_client(build_app)
    response = await client.get('/abcde123', headers=auth)
    assert response.status == web.HTTPNotFound.status_code


@pytest.mark.skip(reason="Нужно мокать remote_ip запроса, что бы получить Forbidden")
async def test_forbidden(aiohttp_client, auth) -> None:
    client = await aiohttp_client(build_app)
    response = await client.get('/ping', headers=auth)
    assert response.status == web.HTTPForbidden.status_code
