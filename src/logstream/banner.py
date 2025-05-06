"""Banner beim Start des Servers."""

import sys
from collections import namedtuple
from getpass import getuser
from importlib.metadata import version, PackageNotFoundError
from locale import getlocale
from socket import gethostbyname, gethostname
from sysconfig import get_platform
from typing import Final

from loguru import logger
from pyfiglet import Figlet
from starlette.routing import BaseRoute, Route
from tabulate import tabulate


TableEntry = namedtuple("TableEntry", "pfad http_methoden funktion")


def _route_to_table_entry(route: Route) -> TableEntry:
    endpoint: Final = route.endpoint
    methods_str = str(route.methods)[2:-2] if route.methods is not None else "-"
    methods_str = methods_str.replace("', '", ", ")
    return TableEntry(
        pfad=route.path,
        http_methoden=methods_str,
        funktion=f"{endpoint.__module__}.{endpoint.__qualname__}",
    )


def _routes_to_str(routes: list[BaseRoute]) -> str:
    routes_str: Final = [
        _route_to_table_entry(route) for route in routes if isinstance(route, Route)
    ]
    return tabulate(
        sorted(routes_str),
        headers=["Pfad", "HTTP-Methoden", "Implementierung"],
    )


def _version(pkg: str) -> str:
    try:
        return version(pkg)
    except PackageNotFoundError:
        return "nicht installiert"


def banner(routes: list[BaseRoute]) -> None:
    """Banner für den Start des Servers."""
    figlet: Final = Figlet(font="slant")
    print()
    print(figlet.renderText("logstream-Service"))

    rechnername: Final = gethostname()

    logger.info("Python        {}", sys.version_info)
    logger.info("Plattform     {}", get_platform())
    logger.info("uvicorn       {}", _version("uvicorn"))
    logger.info("FastAPI       {}", _version("fastapi"))
    logger.info("Starlette     {}", _version("starlette"))
    logger.info("AnyIO         {}", _version("anyio"))
    logger.info("Pydantic      {}", _version("pydantic"))
    logger.info("Environment   {}", sys.prefix)
    logger.info("User          {}", getuser())
    logger.info("Locale        {}", getlocale())
    logger.info("Rechnername   {}", rechnername)
    logger.info("IP-Adresse    {}", gethostbyname(rechnername))
    logger.info("{} Routen wurden registriert:", len(routes))

    print()
    print(_routes_to_str(routes))
    print()
