import asyncio
import tempfile

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from zeply_challenge import db


@pytest.fixture()
def db_connection():
    with tempfile.NamedTemporaryFile() as db_file:
        db.engine = create_async_engine(f"sqlite+aiosqlite:///{db_file.name}")
        db.async_session = async_sessionmaker(db.engine)
        yield


@pytest.fixture(autouse=True)
def setup_db(db_connection):
    asyncio.run(db.create_tables())
