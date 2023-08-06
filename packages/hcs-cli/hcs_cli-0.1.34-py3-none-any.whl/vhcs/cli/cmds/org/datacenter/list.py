import click
from vhcs.service import org_service
from vhcs.common.sglib.util import option_org_id, get_org_id


@click.command("list")
@option_org_id
def list_datacenters(org: str):
    """List all datacenters"""

    if org == "" or org == "all":
        ret = org_service.datacenter.list()
    else:
        org_id = get_org_id(org)
        return org_service.datacenter.find_by_org(org_id)

    return ret
