import click
from vhcs.service import org_service


@click.command("list")
@click.option(
    "--limit", "-l", type=int, required=False, default=20, help="Optionally, specify the number of records to return."
)
@click.option(
    "--search",
    "-s",
    type=str,
    required=False,
    help="Specify the REST-search string. E.g. 'orgId $eq 21eb79bc-f737-479f-b790-7753da55f363 AND orgName $like VMW'. Note, in bash/sh/zsh, use single quote.",
)
def list_org_details(limit: int, search: str):
    """List all org details"""
    ret = org_service.details.list(limit=limit, search=search)
    return ret
