from datetime import datetime
from aiohttp import web


class PingCheckView(web.View):
    """
    Ping-pong view.
    """
    @staticmethod
    async def get():
        return web.Response(body=b'pong')


class HealthCheckView(web.View):
    """
    Health checks view.
    """
    async def get(self) -> web.Response:
        data = {
            'uptime': await self._get_uptime()
        }
        return web.json_response(data)

    async def _get_uptime(self) -> int:
        """ Server uptime in seconds. """
        uptime = datetime.utcnow() - self.request.app.started
        return int(uptime.total_seconds())
