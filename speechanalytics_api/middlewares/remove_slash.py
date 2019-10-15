from aiohttp.web import middleware
from aiohttp.web_exceptions import HTTPMovedPermanently


@middleware
async def remove_slash_middleware(request, handler):
    """ Redirect to URL without trailing slashes midlleware. """
    if request.path.endswith('/'):
        raise HTTPMovedPermanently(request.path.rstrip('/'))
    response = await handler(request)
    return response
