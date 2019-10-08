from aiohttp import web


class OperatorsView(web.View):
    """
    Operators view.
    """
    @staticmethod
    async def get():
        data = {
            'operators': []
        }
        return web.json_response(data)
