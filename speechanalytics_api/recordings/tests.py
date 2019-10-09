from datetime import datetime

from aiohttp import web

from .. import build_app


async def test_operators_date_from_till_filter(aiohttp_client, auth):
    client = await aiohttp_client(build_app)
    query_params = {
        'date_from': datetime(2017, 11, 10, 17, 53, 59),
        'date_till': datetime.utcnow()
    }
    response = await client.get(
        '/operators/',
        params=query_params,
        headers=auth
    )
    assert response.status == web.HTTPOk.status_code

