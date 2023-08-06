import click
from vhcs.service import lcm
from vhcs.util import duration


@click.command()
@click.argument("id", type=str, required=True)
@click.option(
    "--status",
    "-s",
    type=click.Choice(["READY", "ERROR", "DELETING", "EXPANDING", "SHRINKING", "CUSTOMIZING", "MAINTENANCE"]),
    required=False,
    default="READY",
    help="The target status to wait for.",
)
@click.option("--timeout", "-t", type=str, required=False, default="1m", help="Timeout. Examples: '2m', '30s', '1h30m'")
@click.option(
    "--fail-fast/--fail-timeout-only",
    "-f",
    type=bool,
    default=True,
    required=False,
    help="Stop waiting if the template reached to non-expected terminal states, e.g. waiting for ERROR but template is READY, or waiting for READY and template is ERROR.",
)
@click.option(
    "--silent/--return-template",
    type=bool,
    required=False,
    default=True,
    help="Slient mode will has no output on success. Otherwise the full template is returned",
)
def wait(id: str, status: str, timeout: str, fail_fast: bool, silent: bool):
    """Wait for a template to transit to specific status. If the template"""

    timeout_seconds = duration.to_seconds(timeout)
    expected_status = status.upper().split(",")
    exclude_status = []
    if fail_fast:
        if "READY" not in expected_status:
            exclude_status.append("READY")
        if "ERROR" not in expected_status:
            exclude_status.append("ERROR")
    try:
        template = lcm.template.wait(id, expected_status, timeout_seconds, exclude_status)
        return template if not silent else None
    except Exception as e:
        return str(e), 1
