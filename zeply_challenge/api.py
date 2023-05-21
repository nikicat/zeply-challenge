

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoResultFound

from . import db
from .models import Coin, AddressModel, Message
from .wallet import load_wallet, BaseWallet


app = FastAPI()


@app.get("/address/list", response_model=list[AddressModel])
async def list_addresses():
    async with db.get_session() as session:
        return await session.list_addresses()


@app.post("/address/generate/{coin}", response_model=AddressModel)
async def generate_address(coin: Coin):
    wallet: BaseWallet = load_wallet(coin)
    async with db.get_session() as db_session:
        count: int = await db_session.count_addresses()
        address_str: str = wallet.get_address(count)
        address = AddressModel(coin=coin, id=count, address=address_str)
        await db_session.save_address(address=address)
    return address


@app.get("/address/by-id/{id}", response_model=AddressModel, responses={404: dict(model=Message)})
async def get_address(id: int):
    try:
        async with db.get_session() as db_session:
            return await db_session.get_address(id=id)
    except NoResultFound:
        return JSONResponse(status_code=404, content=dict(message="No such address"))
