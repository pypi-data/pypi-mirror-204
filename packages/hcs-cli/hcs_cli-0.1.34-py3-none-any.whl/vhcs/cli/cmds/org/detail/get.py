import click
from vhcs.service import org_service
from vhcs.common.sglib.util import option_org_id, get_org_id


@click.command()
@option_org_id
def get(org: str):
    """Get org details"""
    org_id = get_org_id(org)
    ret = org_service.details.get(org_id)
    if ret:
        return ret
    return ret, 1
