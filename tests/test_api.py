from fastapi.testclient import TestClient
import pytest

from zeply_challenge.api import app
from zeply_challenge.models import Coin, Address

client = TestClient(app)


def test_empty_list():
    response = client.get("/address/list")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.parametrize("coin, address", [
    (Coin.btc, 'bc1qyuty90t4dgr4v8elhpsh2z8jg6zy57h35zr89z'),
    (Coin.eth, '0x959fd7ef9089b7142b6b908dc3a8af7aa8ff0fa1'),
])
def test_create_address(coin: Coin, address: Address):
    address_response = dict(id=0, coin=coin.value, address=address)
    response = client.post(f"/address/generate/{coin.value}")
    assert response.status_code == 200
    assert response.json() == address_response

    response = client.get("/address/by-id/0")
    assert response.status_code == 200
    assert response.json() == address_response

    response = client.get("/address/list")
    assert response.status_code == 200
    assert response.json() == [address_response]


@pytest.mark.parametrize("coin", [Coin.btc, Coin.eth])
def test_unexistent_address(coin: Coin):
    response = client.get("/address/by-id/0")
    assert response.status_code == 404
    assert response.json() == dict(message='No such address')


def test_invalid_coin():
    response = client.post("/address/generate/invalid")
    assert response.status_code == 422
    assert response.json() == dict(
        detail=[dict(
            ctx=dict(enum_values=['btc', 'eth']),
            loc=['path', 'coin'],
            msg="value is not a valid enumeration member; permitted: 'btc', 'eth'",
            type='type_error.enum',
        )]
    )


def test_invalid_url():
    response = client.get('/invalid')
    assert response.status_code == 404
    assert response.json() == dict(detail='Not Found')


def test_invalid_method():
    response = client.get('/address/generate/btc')
    assert response.status_code == 405
    assert response.json() == dict(detail='Method Not Allowed')
