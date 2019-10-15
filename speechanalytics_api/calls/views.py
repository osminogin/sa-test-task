from datetime import datetime

from aiohttp import web

from ..utils import get_call_data


class CallsView(web.View):
    """
    Calls view.
    """
    async def get(self) -> web.Response:
        data = {
            'calls': []
        }
        # Get timestamps range to search (with by default settings)
        try:
            date_from = int(self.request.query.get('date_from') or 1)
            date_till = int(self.request.query.get('date_till') or
                            datetime.now().timestamp())
        except (TypeError, ValueError):
            return web.Response(status=web.HTTPBadRequest.status_code)
        # Unix timestamp to datetime convert
        if date_from:
            date_from = datetime.fromtimestamp(date_from)
        if date_till:
            date_till = datetime.fromtimestamp(date_till)

        # Get DataFrame
        df = await get_call_data(self.request.app)

        # Apply range datetime filter on the `date` field
        if date_from or date_till:
            df = df[
                (df['date'] > date_from) & (df['date'] < date_till)
            ]

        # Do DataFrame modifications and convert to dict
        select_columns = [
            'date', 'type', 'duration_answer', 'status',
            'phone_number_client', 'phone_number_operator',
        ]
        df['date'] = df['date'].map(lambda d: int(d.timestamp()))
        data['calls'] = df[select_columns] \
            .to_dict(orient='records')

        return web.json_response(data)
