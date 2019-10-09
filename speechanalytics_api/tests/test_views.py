import asyncio
from datetime import datetime

from aiohttp import web

from speechanalytics_api import build_app


async def test_ping_success(aiohttp_client):
    """ Проверка тестового метода ping-pong. """
    client = await aiohttp_client(build_app)
    response = await client.get('/ping/')
    assert response.status == web.HTTPOk.status_code
    content = await response.text()
    assert response.content_type == 'text/plain'
    assert content == 'pong'


async def test_healthcheck_success(aiohttp_client):
    """ Проверка аптайма (специально делаем задержку в 1s). """
    client = await aiohttp_client(build_app)
    response = await client.get('/health/')
    assert response.status == web.HTTPOk.status_code
    assert response.content_type == 'application/json'
    data = await response.json()
    sleep = await asyncio.sleep(1)
    assert 'uptime' in data
    assert not sleep, data['uptime'] > 0


async def test_get_calls(aiohttp_client, auth):
    """ Example call list. """
    client = await aiohttp_client(build_app)
    response = await client.get('/calls/', headers=auth)
    assert response.status == web.HTTPOk.status_code
    assert response.content_type == 'application/json'


async def test_get_calls_filters(aiohttp_client, auth):
    """ Example call list witj date range. """
    client = await aiohttp_client(build_app)
    query_params = {
        'date_from': 1,
        'date_till': datetime.utcnow().timestamp()
    }
    response = await client.get('/calls/', params=query_params, headers=auth)
    data = await response.json()
    assert not data['calls']
    assert False    # TODO


async def test_get_operators(aiohttp_client, auth):
    """ Test operators list. """
    client = await aiohttp_client(build_app)
    response = await client.get('/operators/', headers=auth)
    data = await response.json()
    assert response.status == web.HTTPOk.status_code
    assert response.content_type == 'application/json'


async def test_get_operators_filters(aiohttp_client, auth):
    """ Test operators list with filters. """
    client = await aiohttp_client(build_app)
    query_params = {'date_till': datetime.utcnow()}
    response = await client.get(
        '/operators/',
        params=query_params,
        headers=auth
    )
    data = await response.json()
    assert response.status == web.HTTPOk.status_code
    assert response.content_type == 'application/json'
    assert False    # TODO
