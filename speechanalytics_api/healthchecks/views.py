from datetime import datetime
from aiohttp import web


class PingCheckView(web.View):
    """
    Ping-pong view.
    """
    @staticmethod
    async def get() -> web.Response:
        return web.Response(text='pong')


class HealthCheckView(web.View):
    """
    Health checks view.
    """
    async def get(self) -> web.Response:
        """ System health data. """
        data = {
            'uptime': await self._get_uptime(),
            # 'client_ip': self.request.remote,
            'remote_client': self.request.transport.get_extra_info('peername'),
        }
        if getattr(self.request.app, 'yadisk'):
            yadisk_info = await self._get_yadisk_info()
            data['yadisk'] = {
                'user': yadisk_info.user.display_name,
                'valid_token': await self.request.app.yadisk.check_token(),
                'total_space': yadisk_info.total_space,
                'used_space': yadisk_info.used_space,
            }
        return web.json_response(data)

    async def _get_uptime(self) -> int:
        """ Server uptime in seconds. """
        uptime = datetime.utcnow() - self.request.app.started
        return int(uptime.total_seconds())

    async def _get_yadisk_info(self) -> dict:
        return await self.request.app.yadisk.get_disk_info()
