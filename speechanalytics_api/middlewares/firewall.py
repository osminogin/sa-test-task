from aiohttp.web import middleware, HTTPForbidden

from ..settings import WHITELIST_IPS, WHITELIST_URLS


@middleware
async def firewall_middleware(request, handler):
    """ Restrict access to whitelist middleware. """
    remote_ip = request.headers.get('X-Forwarded-For')
    if remote_ip not in WHITELIST_IPS and \
            request.path not in WHITELIST_URLS:
        raise HTTPForbidden
    response = await handler(request)
    return response
