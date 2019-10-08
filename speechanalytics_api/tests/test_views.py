import asyncio
from speechanalytics_api import build_app


async def test_ping_success(aiohttp_client):
    """ Проверка тестового метода ping-pong. """
    client = await aiohttp_client(build_app)
    response = await client.get('/ping/')
    assert response.status == 200
    content = await response.text()
    assert content == 'pong'


async def test_healthcheck_success(aiohttp_client):
    """ Проверка аптайма (специально делаем задержку в 1s). """
    client = await aiohttp_client(build_app)
    response = await client.get('/health/')
    assert response.status == 200   # Ok
    data = await response.json()
    sleep = await asyncio.sleep(1)
    assert 'uptime' in data
    assert not sleep, data['uptime'] > 0


async def test_get_calls(aiohttp_client):
    """ Example call list. """
    client = await aiohttp_client(build_app)
    response = await client.get('/calls/')
    assert response.status == 200   # Ok