from aiohttp.web import middleware, HTTPForbidden, Response

from ..settings import WHITELIST_IPS


@middleware
async def firewall_middleware(request, handler):
    """ Restrict access to whitelist middleware. """
    if request.remote not in WHITELIST_IPS:
        return Response(status=HTTPForbidden.status_code)
    response = await handler(request)
    return response
