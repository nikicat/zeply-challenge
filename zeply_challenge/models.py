import typing
from enum import Enum

from pydantic import BaseModel

Address = typing.NewType('Address', str)


class Coin(str, Enum):
    btc = 'btc'
    eth = 'eth'


class AddressModel(BaseModel):
    coin: Coin
    address: Address
    id: int

    class Config:
        orm_mode = True


class Message(BaseModel):
    message: str
