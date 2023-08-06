import click


@click.group()
def command_group():
    ...


@command_group.command()
@click.argument("string")
def lower(string):
    """
    Lower case
    """
    print(string.lower())


@command_group.command()
@click.argument("string")
def upper(string):
    """
    Upper case
    """
    print(string.upper())


@command_group.command()
@click.argument("string")
def cap(string):
    """
    Capitalize
    """
    print(string.capitalize())


if __name__ == "__main__":
    command_group()
