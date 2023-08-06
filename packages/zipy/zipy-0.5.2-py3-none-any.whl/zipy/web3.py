from functools import cache
from eth_account import Account as _Web3Account
from eth_account.signers.local import LocalAccount
from eth_account.datastructures import SignedTransaction
from pydantic import BaseModel
from typing import Optional
from web3 import Web3 as OriginalWeb3
from web3 import HTTPProvider, WebsocketProvider


class Chain(BaseModel):
    rpc: str
    chain_id: int


CHAIN_ETHEREUM = Chain(
    rpc="https://mainnet.infura.io/v3/",
    chain_id=1,
)

CHAIN_GOERLI = Chain(
    rpc="https://goerli.blockpi.network/v1/rpc/public",
    chain_id=5,
)

CHAIN_BSC = Chain(
    rpc="https://bsc-dataseed1.binance.org",
    chain_id=56,
)


class Contract(BaseModel):
    address: str
    abi: str


class Account:
    @staticmethod
    def _require_set_chain(func):
        """
        Only used for bound method
        """

        def wrapper(*args, **kwargs):
            self = args[0]
            if getattr(self, "_chain", None) is None:
                raise ValueError("chain is not set. Please call set_chain() first")
            return func(*args, **kwargs)

        return wrapper

    @classmethod
    def create(cls) -> "Account":
        account = _Web3Account.create()
        private_key = account.key.hex()
        return cls(private_key)

    def __init__(self, private_key: str, chain: Optional[Chain] = None):
        self._web3_account: LocalAccount = _Web3Account.from_key(private_key)
        self._chain = chain
        self._web3 = None
        if self._chain:
            self.set_chain(self._chain)

    @property
    @cache
    def address(self) -> str:
        return self._web3_account.address

    @property
    @cache
    def private_key(self) -> str:
        return self._web3_account.key.hex()

    @property
    @_require_set_chain
    def transaction_count(self) -> int:
        return self._web3.eth.get_transaction_count(self.address)

    def set_chain(self, chain: Chain):
        if not isinstance(chain, Chain):
            raise ValueError("chain must be an instance of Chain")

        if chain.rpc.startswith("ws"):
            self._web3: OriginalWeb3 = OriginalWeb3(WebsocketProvider(chain.rpc))
        elif chain.rpc.startswith("http"):
            self._web3: OriginalWeb3 = OriginalWeb3(HTTPProvider(chain.rpc))
        else:
            raise ValueError(
                'Invalid RPC. chain.rpc must start with "ws" or "http, the passed chain is {}'.format(
                    self._chain
                )
            )

        self._chain = chain

    @_require_set_chain
    def balance_of_eth(self) -> int:
        """
        Get balance of ETH of an address

        :return: balance of ETH in wei
        """
        return self._web3.eth.get_balance(self.address)

    @_require_set_chain
    def balance_of_erc20(
        self, contract: Contract, method_name: str = "balanceOf"
    ) -> int:
        """
        Get balance of ERC20 of an address

        :param contract: contract of ERC20 Token
        :return: balance of ERC20
        """
        return self._balance_of_contract(contract, method_name)

    @_require_set_chain
    def balance_of_nft(self, contract: Contract, method_name: str = "balanceOf") -> int:
        """
        Get balance of NFT of an address

        :param contract: contract of NFT
        :return: balance of NFT
        """
        return self._balance_of_contract(contract, method_name)

    @_require_set_chain
    def transfer_eth(
        self,
        to_address: str,
        amount: int,
        gas_price: int | None = None,
        wait_for_receipt: bool = True,
        wait_timeout: int = 60,
        receipt_poll_interval: int = 5,
    ) -> str:
        """
        Transfer ETH

        :param to_address: account address of receiver
        :param amount: amount of ETH in wei
        :param gas_price: gas price in wei. None means use default gas price (web3.eth.gas_price)
        :return: transaction hash
        :raises: If wait_for_receipt is True, raise TimeoutError if transaction is not mined in wait_timeout seconds, or some other error if transaction is failed
        """
        sender_account = self._web3_account
        tx = {
            "to": self._web3.toChecksumAddress(to_address),
            "value": amount,
            "gas": 21000,
            "gasPrice": self._web3.eth.gas_price if gas_price is None else gas_price,
            "nonce": self.transaction_count,
            "chainId": self._chain.chain_id,
        }
        signed_tx = sender_account.sign_transaction(tx)
        tx_hash = self._web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        if wait_for_receipt:
            result = self._web3.eth.wait_for_transaction_receipt(
                tx_hash, timeout=wait_timeout, poll_latency=receipt_poll_interval
            )
            if result.status != 1:
                raise Exception(result)
        return tx_hash.hex()

    @_require_set_chain
    def transfer_erc20(
        self,
        *,
        to_address: str,
        amount: int,
        contract: Contract,
        gas_limit: int,
        gas_price: int | None = None,
        wait_for_receipt: bool = True,
        wait_timeout: int = 60,
        receipt_poll_interval: int = 5,
    ) -> str:
        """
        Transfer ERC20

        :param to_address: account address of receiver
        :param amount: amount of ERC20
        :param contract_address: contract address of ERC20
        :param abi: abi of ERC20
        :param gas_limit: gas limit
        :param gas_price: gas price in wei. None means use default gas price (web3.eth.gas_price)
        :return: transaction hash
        :raises: If wait_for_receipt is True, raise TimeoutError if transaction is not mined in wait_timeout seconds, or some other error if transaction is failed
        """
        if not isinstance(contract, Contract):
            raise ValueError("contract must be an instance of Contract")

        contract = self._web3.eth.contract(
            OriginalWeb3.toChecksumAddress(contract.address), abi=contract.abi
        )
        tx = contract.functions["transfer"](
            OriginalWeb3.toChecksumAddress(to_address), amount
        ).buildTransaction(
            {
                "gas": gas_limit,
                "gasPrice": self._web3.eth.gas_price
                if gas_price is None
                else gas_price,
                "nonce": self.transaction_count,
                "chainId": self._chain.chain_id,
            }
        )
        sender_account = self._web3_account
        signed_tx: SignedTransaction = sender_account.sign_transaction(tx)
        tx_hash = self._web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        if wait_for_receipt:
            result = self._web3.eth.wait_for_transaction_receipt(
                tx_hash, timeout=wait_timeout, poll_latency=receipt_poll_interval
            )
            if result.status != 1:
                raise Exception(result)
        return tx_hash.hex()

    @_require_set_chain
    def transfer_nft(
        self,
        *,
        to_address: str,
        contract: Contract,
        token_id: int,
        gas_limit: int,
        gas_price: int | None = None,
        wait_for_receipt: bool = True,
        wait_timeout: int = 60,
        receipt_poll_interval: int = 5,
    ) -> str:
        """
        Transfer NFT

        :param to_address: account address of receiver
        :param token_id: token id of NFT
        :param contract_address: contract address of NFT
        :param gas_limit: gas limit
        :param gas_price: gas price in wei. None means use default gas price (web3.eth.gas_price)
        :param chain_id: chain id of Ethereum network
        :return: transaction hash
        :raises: If wait_for_receipt is True, raise TimeoutError if transaction is not mined in wait_timeout seconds, or some other error if transaction is failed
        """
        if not isinstance(contract, Contract):
            raise ValueError("contract must be an instance of Contract")

        contract = self._web3.eth.contract(
            OriginalWeb3.toChecksumAddress(contract.address), abi=contract.abi
        )
        tx = contract.functions["transferFrom"](
            self.address,
            OriginalWeb3.toChecksumAddress(to_address),
            token_id,
        ).buildTransaction(
            {
                "gas": gas_limit,
                "gasPrice": self._web3.eth.gas_price
                if gas_price is None
                else gas_price,
                "nonce": self.transaction_count,
                "chainId": self._chain.chain_id,
            }
        )
        sender_account = self._web3_account
        signed_tx = sender_account.sign_transaction(tx)
        tx_hash = self._web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        if wait_for_receipt:
            result = self._web3.eth.wait_for_transaction_receipt(
                tx_hash, timeout=wait_timeout, poll_latency=receipt_poll_interval
            )
            if result.status != 1:
                raise Exception(result)
        return tx_hash.hex()

    @_require_set_chain
    def _balance_of_contract(self, contract: Contract, method_name: str) -> int:
        if not isinstance(contract, Contract):
            raise ValueError("contract must be an instance of Contract")

        contract = self._web3.eth.contract(
            OriginalWeb3.toChecksumAddress(contract.address), abi=contract.abi
        )
        return contract.functions[method_name](self.address).call()


def to_wei(amount: float, unit: str) -> int:
    """
    Convert amount to wei

    :param amount: amount
    :param unit: unit of amount. 'ether' or 'gwei'
    :return: amount in wei
    """
    return OriginalWeb3.toWei(amount, unit)
