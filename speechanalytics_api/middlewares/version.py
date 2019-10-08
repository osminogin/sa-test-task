from aiohttp.web import middleware


@middleware
async def version_middleware(request, handler):
    response = await handler(request)
    response.headers['X-API-Version'] = request.app.version
    return response
