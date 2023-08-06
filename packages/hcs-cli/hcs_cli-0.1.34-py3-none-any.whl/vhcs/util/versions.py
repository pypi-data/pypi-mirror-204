import logging
import httpx
import time
import vhcs.common.ctxp as ctxp

import pkg_resources
from packaging.version import Version

log = logging.getLogger(__name__)


def check_upgrade():
    last_upgrade_check_at = "last_upgrade_check_at"
    checked_at = ctxp.state.get(last_upgrade_check_at, 0)

    now = time.time()
    if now - checked_at > 24 * 60 * 60:
        try:
            latest = get_latest_version()
            current = Version(get_version())
            if current < latest:
                log.warning(f"New version available: {latest}. Execute 'hcs upgrade' to upgrade.")
        except Exception as e:
            logging.debug(e)

    ctxp.state.set(last_upgrade_check_at, now)


def get_version():
    return pkg_resources.require("hcs-cli")[0].version


def get_latest_version() -> Version:
    res = httpx.get("https://pypi.org/pypi/hcs-cli/json")
    names = res.json().get("releases").keys()
    versions = [Version(n) for n in names]
    versions.sort(reverse=True)
    return versions[0]


def is_version(s: str):
    try:
        return Version(s)
    except ValueError:
        return False
