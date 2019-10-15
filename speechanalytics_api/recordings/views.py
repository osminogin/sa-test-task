from uuid import UUID

from aiohttp import web

from ..utils import get_call_data


class RecordingsView(web.View):
    """
    Recordings view.
    """
    async def get(self) -> web.Response:
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

        df = await get_call_data(self.request.app, columns=[])

        # TODO
        df

        return web.Response(data)

    async def post(self) -> web.Response:
        # TODO
        pass
