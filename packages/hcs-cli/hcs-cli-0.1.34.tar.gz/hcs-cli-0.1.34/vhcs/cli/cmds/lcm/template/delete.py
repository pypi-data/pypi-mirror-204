import click
from vhcs.service import lcm
from vhcs.common.sglib.util import option_org_id, get_org_id


@click.command()
@click.argument("id", type=str, required=True)
@option_org_id
@click.option(
    "--force/--safe", default=True, help="In 'force' mode, the template deletion will continue and ignore any error."
)
def delete(id: str, org: str, force: bool):
    """Delete template by ID"""
    org_id = get_org_id(org)
    return lcm.template.delete(id, org_id, force)
