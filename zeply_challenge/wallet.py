import abc
import typing
from functools import lru_cache

import eth_keys.datatypes  # type: ignore
import cryptos  # type: ignore

from . import settings
from .models import Address, Coin


class BaseWallet(abc.ABC):
    def __init__(self):
        self.keystore = cryptos.from_bip39_seed(
            settings.seed_phrase,
            passphrase=None,
            derivation=self.derivation,
            coin=cryptos.Bitcoin(),
        )

    @property
    @abc.abstractmethod
    def derivation(self) -> str:
        ...

    @abc.abstractmethod
    def get_address(self, id: int) -> Address:
        ...


class BTCWallet(BaseWallet):
    derivation: str = "m/84'/0'/0'"  # Bitcoin p2wpkh

    def get_address(self, id: int) -> Address:
        return typing.cast(Address, cryptos.HDWallet(self.keystore).receiving_address(id))


class ETHWallet(BaseWallet):
    derivation: str = "m/44'/60'/0'"  # Ethereum Metamask

    def get_address(self, id: int) -> Address:
        pubkey: str = self.keystore.derive_pubkey(for_change=False, n=id)
        return Address(eth_keys.datatypes.PublicKey.from_compressed_bytes(bytes.fromhex(pubkey)).to_address())


# Other possible derivation paths
# derivation = "m/84'/0'/0'"  # Bitcoin p2wpkh
# derivation = "m/49'/0'/0'"  # Bitcoin p2wpkh_p2sh
# derivation = "m/44'/0'/0'"  # Bitcoin standard
# derivation = "m/84'/1'/0'"  # Bitcoin Testnet p2wpkh
# derivation = "m/49'/1'/0'"  # Bitcoin Testnet p2wpkh_p2sh
# derivation = "m/44'/1'/0'"  # Bitcoin Testnet standard


@lru_cache
def load_wallet(coin: Coin) -> BaseWallet:
    return {
        Coin.btc: BTCWallet,
        Coin.eth: ETHWallet,
    }[coin]()
