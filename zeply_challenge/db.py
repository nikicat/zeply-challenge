from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy import select, insert, func, Integer, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession, AsyncEngine

from . import settings
from .models import AddressModel

engine: AsyncEngine = create_async_engine(settings.db_url)
async_session = async_sessionmaker(engine)
Base = declarative_base()


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    coin = Column(String, nullable=False)


class DbSession:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def count_addresses(self) -> int:
        result = await self.session.scalars(select(func.count()).select_from(Address))
        return result.one()

    async def save_address(self, address: AddressModel):
        await self.session.execute(insert(Address).values(
            address=address.address,
            coin=address.coin,
            id=address.id,
        ))

    async def list_addresses(self) -> list[AddressModel]:
        result = await self.session.scalars(select(Address))
        return [AddressModel.from_orm(address) for address in result]

    async def get_address(self, id: int) -> AddressModel:
        result = await self.session.scalars(select(Address).where(Address.id == id))
        return AddressModel.from_orm(result.one())


@asynccontextmanager
async def get_session() -> AsyncIterator[DbSession]:
    async with async_session() as session:
        yield DbSession(session)
        await session.commit()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
