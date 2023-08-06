import click
from vhcs.service import lcm


@click.command()
@click.argument("id", type=str, required=True)
def get(id: str):
    """Get template by ID"""
    ret = lcm.template.get(id)
    if ret:
        return ret
    return ret, 1
