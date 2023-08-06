import click
from vhcs.service import lcm
from vhcs.common.sglib.util import option_org_id, get_org_id


@click.command()
@option_org_id
@click.option("--type", "-t", type=str, required=False, help="Optionally, specify cloud provider type.")
def list(org: str, type: str):
    """List providers"""
    org_id = get_org_id(org)
    return lcm.provider.list(org_id=org_id, type=type)
