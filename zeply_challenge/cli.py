import asyncio
import logging.config
import typing

import typer
from hypercorn.asyncio import serve as hypercorn_serve
from hypercorn.config import Config
from hypercorn.typing import ASGIFramework

from . import db, settings
from .api import app

cli = typer.Typer()


@cli.command()
def create_tables():
    asyncio.run(db.create_tables())


@cli.command()
def serve():
    logging.config.dictConfig(settings.log_config)
    hyper_config = Config.from_mapping(dict(bind=settings.bind))
    asyncio.run(hypercorn_serve(typing.cast(ASGIFramework, app), hyper_config))


if __name__ == "__main__":
    cli()
