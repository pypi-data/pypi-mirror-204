import click
from zipy.web3 import Account


@click.group()
def command_group():
    ...


@command_group.command()
def gen_account():
    """
    Generate account
    """
    acct = Account.create()
    print(f"address: {acct.address}")
    print(f"private_key: {acct.private_key}")


@command_group.command()
@click.argument("private_key")
def address_of(private_key):
    """
    Get address from private key
    """
    address = Account(private_key).address
    print(f"address: {address}")


if __name__ == "__main__":
    command_group()
