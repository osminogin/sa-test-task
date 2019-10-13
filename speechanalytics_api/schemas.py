import os
import json
import pathlib

import aiofiles


class SpeechAnalyticsSchemas:

    def __init__(self, app, schemas_dir=None):
        self.app = app
        if schemas_dir is None:
            self.schemas_dir = pathlib.Path.cwd() / 'schemas'

    @property
    async def schemas(self):
        """
        Генерируем json схемы из файлов в директории.
        В дирректории должны содержаться только файлы со схемами!
        TODO: Забирать файлы из файлового хранилища.
        """
        for path in pathlib.Path.iterdir(self.schemas_dir):
            name = self.get_schema_name(path)
            schema = await self.read_schema_file(path)
            yield name, schema

    @staticmethod
    def get_schema_name(path):
        filename = os.path.basename(path.as_posix())
        name = filename.split('.')[0]
        name = name.title()
        schema_name = ''.join(name.split('_'))
        return schema_name

    @staticmethod
    async def read_schema_file(path):
        async with aiofiles.open(path, 'r') as f:
            data = await f.read()
        return json.loads(data)
