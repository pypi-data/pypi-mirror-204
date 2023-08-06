import click
from vhcs.service import admin
from vhcs.common.sglib.util import option_org_id, get_org_id


@click.command()
@click.argument("id", type=str, required=True)
@option_org_id
def get(id: str, org: str):
    """Get edge by ID"""
    ret = admin.edge.get(id, org_id=get_org_id(org))
    if ret:
        return ret
    return ret, 1
