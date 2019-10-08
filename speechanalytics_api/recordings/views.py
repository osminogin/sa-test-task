from aiohttp import web


class RecordingsView(web.View):
    """
    Recordings view.
    """
    async def get(self):
        data = {
            'calls': []
        }
        return web.Response(data)
