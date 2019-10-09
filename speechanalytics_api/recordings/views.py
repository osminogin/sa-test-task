from aiohttp import web


class RecordingsView(web.View):
    """
    Recordings view.
    """
    async def get(self):
        call_id = self.request.query_string.get('call_id')
        data = {
            'calls': []
        }
        return web.Response(data)

    async def post(self):
        pass
