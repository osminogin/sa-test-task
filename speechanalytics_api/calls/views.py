from aiohttp import web


class CallsView(web.View):
    """
    Calls view.
    """
    async def get(self):
        data = {
            'calls': []
        }
        return web.Response(data)
