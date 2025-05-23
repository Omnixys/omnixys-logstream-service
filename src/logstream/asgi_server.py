
"""Funktion `run`, um die FastAPI-Applikation mit einem ASGI-Server zu starten.

Dazu stehen _uvicorn_ (default) und _hypercorn_ zur Verfügung.
"""

import asyncio
from ssl import PROTOCOL_TLS_SERVER
from typing import Final

import uvicorn
from hypercorn.asyncio import serve
from hypercorn.config import Config

from .main import app

__all__ = ["run"]

def _run_hypercorn() -> None:
    """Start der Anwendung mit hypercorn."""
    config: Final = Config()
    config.bind = [f"{"127.0.0.1"}:{"7401"}"]
    # config.keyfile = tls_keyfile
    # config.certfile = tls_certfile
    asyncio.run(serve(app=app, config=config, mode="asgi"))  # pyright: ignore[reportArgumentType]


def run() -> None:
    """CLI für den asynchronen Appserver."""
    _run_hypercorn()

