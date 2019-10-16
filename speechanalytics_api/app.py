from datetime import datetime

import yadisk_async
import fastjsonschema
from aiohttp import web

from .settings import YADISK_TOKEN, YADISK_CALLDATA
from .utils import get_middlewares, get_version, redirect_handler
from .calls.views import CallsView
from .schemas import SpeechAnalyticsSchemas
from .recordings.views import RecordingsView
from .operators.views import OperatorsView
from .healthchecks.views import PingCheckView, HealthCheckView


def build_app(argv=None) -> web.Application:
    """ Application factory. """
    app = web.Application(middlewares=get_middlewares())
    app.on_startup.append(startup_handler)
    app.on_cleanup.append(cleanup_handler)
    register_routes(app)
    return app


def register_routes(app) -> None:
    """ Routes table. """
    app.router.add_get('/', redirect_handler)
    app.router.add_get('/calls', CallsView, allow_head=False)
    app.router.add_route('*', '/recording', RecordingsView)
    app.router.add_get('/operators', OperatorsView, allow_head=False)
    app.router.add_get('/ping', PingCheckView)
    app.router.add_get('/health', HealthCheckView)


async def startup_handler(app) -> None:
    """ Initialize application state. """
    app.started = datetime.utcnow()
    app.version = await get_version()

    # Yandex.Disk connection init and checks
    app.yadisk = yadisk_async.YaDisk(token=YADISK_TOKEN)
    try:
        assert await app.yadisk.check_token()
        assert await app.yadisk.exists(YADISK_CALLDATA)
    except AssertionError:
        raise RuntimeError

    # JSON Schema validators pre-compiles
    app.schemas = SpeechAnalyticsSchemas(app).schemas
    app.validator = dict()
    async for schema in app.schemas:
        app.validator[schema[0].lower()] = fastjsonschema.compile(schema[1])


async def cleanup_handler(app) -> None:
    """ Always remember to close all the connections. """
    await app.yadisk.close()
