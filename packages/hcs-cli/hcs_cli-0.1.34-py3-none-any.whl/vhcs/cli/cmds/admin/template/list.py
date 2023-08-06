import click
from vhcs.service import admin
from vhcs.common.sglib.util import option_org_id, get_org_id


@click.command()
@click.option("--limit", "-l", type=int, required=False, default=20, help="Optionally, specify cloud provider type.")
@option_org_id
@click.option("--brokerable-only", type=bool, required=False, default=False)
@click.option("--expanded", type=bool, required=False, default=False)
@click.option(
    "--reported-search",
    type=str,
    required=False,
    help="Search expression for selection of template reported properties",
)
@click.option("--template-search", type=str, required=False, help="Search expression for selection of templates")
@click.option(
    "--sort",
    type=str,
    required=False,
    help="Ascending/Descending. Format is property,{asc|desc} and default is ascending",
)
def list(
    limit: int, org: str, brokerable_only: bool, expanded: bool, reported_search: str, template_search: str, sort: str
):
    """List templates"""
    return admin.template.list(
        limit,
        org_id=get_org_id(org),
        borkerable_only=brokerable_only,
        expanded=expanded,
        reported_search=reported_search,
        template_search=template_search,
        sort=sort,
    )
