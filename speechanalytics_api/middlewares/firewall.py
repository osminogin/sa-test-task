from aiohttp.web import middleware, Response

from ..settings import WHITELIST_IP


@middleware
async def firewall_middleware(request, handler):
    if request.remote not in WHITELIST_IP:
        return Response(status=403)     # Forbidden
    response = await handler(request)
    return response
