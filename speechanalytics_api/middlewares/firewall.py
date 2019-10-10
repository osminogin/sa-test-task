from aiohttp.web import middleware, HTTPForbidden, Response

from ..settings import WHITELIST_IP


@middleware
async def firewall_middleware(request, handler):
    if request.remote not in WHITELIST_IP:
        return Response(status=HTTPForbidden.status_code)
    response = await handler(request)
    return response
