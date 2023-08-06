import click
from vhcs.service import org_service


@click.command()
@click.argument("id", type=str, required=True)
def get(id: str):
    """Get datacenter"""
    ret = org_service.datacenter.get(id)
    if ret:
        return ret
    return ret, 1
