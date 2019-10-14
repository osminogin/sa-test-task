from aiohttp import web

from ..utils import get_call_data


class OperatorsView(web.View):
    """
    Operators view.
    """
    async def get(self):
        data = {
            'operators': []
        }
        select_columns = ['phone_number_operator', 'name_operator']
        df = await get_call_data(self.request.app, columns=select_columns)
        df.astype({'phone_number_operator': str})

        # Prapare DataFrame for the return
        data['operators'] = df[select_columns] \
            .rename(columns={'phone_number_operator': 'phone_number',
                             'name_operator': 'name'}) \
            .to_dict(orient='records')

        return web.json_response(data)

    async def post(self):
        self.request.app.validators['operatora']({})
