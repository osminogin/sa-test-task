import asyncio
from datetime import datetime, timedelta

from aiohttp import web

from speechanalytics_api import build_app


async def test_ping_success(aiohttp_client) -> None:
    """ Проверка тестового метода ping-pong. """
    client = await aiohttp_client(build_app)
    response = await client.get('/ping')
    assert response.status == web.HTTPOk.status_code
    content = await response.text()
    assert response.content_type == 'text/plain'
    assert content == 'pong'


async def test_healthcheck_success(aiohttp_client):
    """ Проверка аптайма (специально делаем задержку в 1s). """
    client = await aiohttp_client(build_app)
    response = await client.get('/health')
    assert response.status == web.HTTPOk.status_code
    assert response.content_type == 'application/json'
    data = await response.json()
    sleep = await asyncio.sleep(1)  # Timeout 1 second
    assert 'uptime' in data
    assert 'yadisk' in data
    assert not sleep, data['uptime'] > 0


async def test_get_calls(aiohttp_client, auth) -> None:
    """ Example call list. """
    client = await aiohttp_client(build_app)
    response = await client.get('/calls', headers=auth)
    assert response.status == web.HTTPOk.status_code
    assert response.content_type == 'application/json'
    data = client.app.validator['calls'](await response.json())
    assert data, 'calls' in data


async def test_get_calls_filters(aiohttp_client, auth) -> None:
    """ Example call list witj date range. """
    # Select all first
    client = await aiohttp_client(build_app)
    query_params = {
        'date_till': int(datetime.now().timestamp())
    }
    response = await client.get('/calls', params=query_params, headers=auth)
    assert response.status == web.HTTPOk.status_code
    assert response.content_type == 'application/json'
    data = client.app.validator['calls'](await response.json())
    assert data, 'calls' in data
    assert len(data['calls']) > 1
    entry = data['calls'].pop()
    assert isinstance(entry['date'], int)
    assert isinstance(entry['phone_number_client'], str)
    assert isinstance(entry['phone_number_operator'], str)
    assert isinstance(entry['duration_answer'], int)

    # Example of range filter (only one call choosed)
    query_params = {
        'date_till': int(
            (datetime.now() - timedelta(days=79)).timestamp()
        )
    }
    response = await client.get('/calls', params=query_params, headers=auth)
    assert response.status == web.HTTPOk.status_code
    assert response.content_type == 'application/json'
    data = client.app.validator['calls'](await response.json())
    assert data, 'calls' in data
    assert len(data['calls']) == 1


async def test_get_operators(aiohttp_client, auth) -> None:
    """ Test operators list. """
    client = await aiohttp_client(build_app)
    response = await client.get('/operators', headers=auth)
    assert response.status == web.HTTPOk.status_code
    assert response.content_type == 'application/json'
    data = client.app.validator['operators'](await response.json())
    assert data, 'operators' in data
    assert len(data['operators']) > 1


async def test_get_operators_filters(aiohttp_client, auth) -> None:
    """ Test operators list with filters. """
    client = await aiohttp_client(build_app)
    query_params = {'date_till': int(datetime.now().timestamp())}
    response = await client.get(
        '/operators',
        params=query_params,
        headers=auth
    )
    assert response.status == web.HTTPOk.status_code
    assert response.content_type == 'application/json'
    data = client.app.validator['operators'](await response.json())
    assert data, 'operators' in data
    assert len(data['operators']) > 1
