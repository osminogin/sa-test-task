from datetime import datetime

from aiohttp import web

from .utils import get_middlewares, get_version
from .calls.views import CallsView
from .healthchecks.views import PingCheckView, HealthCheckView


def build_app(argv=None) -> web.Application:
    app = web.Application(middlewares=get_middlewares())
    app.on_startup.append(startup_handler)
    app.on_cleanup.append(cleanup_handler)
    register_routes(app)
    return app


def register_routes(app) -> None:
    app.router.add_route('*', '/calls/', CallsView)
    app.router.add_route('*', '/ping/', PingCheckView)
    app.router.add_route('*', '/health/', HealthCheckView)


async def startup_handler(app) -> None:
    app.started = datetime.utcnow()
    app.version = await get_version()


async def cleanup_handler(app) -> None:
    pass
