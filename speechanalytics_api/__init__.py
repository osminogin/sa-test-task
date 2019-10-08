import asyncio

from .app import build_app

loop = asyncio.get_event_loop()
app = build_app()
