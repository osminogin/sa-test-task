from aiohttp import web


class OperatorsView(web.View):
    """
    Operators view.
    """
    async def get(self):
        data = {
            'operators': []
        }
        return web.json_response(data)
