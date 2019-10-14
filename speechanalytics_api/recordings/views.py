from uuid import UUID

from aiohttp import web

from ..utils import get_call_data


class RecordingsView(web.View):
    """
    Recordings view.
    """
    async def get(self):
        data = {
            'calls': []
        }
        call_id = self.request.query.get('call_id')
        try:
            if not call_id:     # Query param `call_id` is required
                raise ValueError
            # Checks valid UUID
            UUID(call_id)
        except ValueError:
            return web.Response(status=web.HTTPBadRequest.status_code)

        # TODO: Запрос данных записей
        df = await get_call_data()

        return web.Response(data)

    async def post(self):
        pass
