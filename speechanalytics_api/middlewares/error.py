from aiohttp import web
from aiohttp.web import middleware, HTTPException


@middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        if response.status != 404:
            return response
        message = response.message
    except HTTPException as e:
        if e.status != 404:
            raise
        message = e.reason
    data = {'error': message}
    return web.json_response(data)
