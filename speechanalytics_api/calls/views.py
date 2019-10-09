from aiohttp import web


class CallsView(web.View):
    """
    Calls view.
    """
    async def get(self):
        data = {
            'calls': []
        }
        # date_from=1527847200&date_till=1528641300
        date_from, date_till = self.request.query_string.get('date_from'), \
            self.request.query_string.get('date_till')

        # TODO: Поиск по метаданным

        return web.Response(data)
