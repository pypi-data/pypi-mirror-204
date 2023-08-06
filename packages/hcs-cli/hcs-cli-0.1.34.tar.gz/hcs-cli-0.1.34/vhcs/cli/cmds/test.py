import click

from vhcs.common.ctxp.util import option_field


@click.command(hidden=True)
@click.argument("id", type=str, required=True)
def test(id: str):
    print(id)
