from datetime import datetime
from aiohttp import web


class PingCheckView(web.View):
    """
    Ping-pong view.
    """
    @staticmethod
    async def get():
        return web.Response(text='pong')


class HealthCheckView(web.View):
    """
    Health checks view.
    """
    async def get(self) -> web.Response:
        """ System health data. """
        data = {
            'uptime': await self._get_uptime(),
            'yadisk': await self._get_yadisk_info()
        }
        return web.json_response(data)

    async def _get_uptime(self) -> int:
        """ Server uptime in seconds. """
        uptime = datetime.utcnow() - self.request.app.started
        return int(uptime.total_seconds())

    async def _get_yadisk_info(self):
        return await self.request.app.yadisk.get_disk_info()
