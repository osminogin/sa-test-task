from aiohttp.web import middleware


@middleware
async def version_middleware(request, handler):
    """ Adds additional header with API version. """
    response = await handler(request)
    response.headers['X-API-Version'] = request.app.version
    return response
