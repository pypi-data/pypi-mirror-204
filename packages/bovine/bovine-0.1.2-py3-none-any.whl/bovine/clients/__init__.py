import logging
import traceback

import aiohttp

from bovine.utils import parse_fediverse_handle

from .lookup_account import lookup_with_webfinger
from .nodeinfo import fetch_nodeinfo20, fetch_nodeinfo_document

logger = logging.getLogger(__name__)


async def lookup_account_with_webfinger(
    session: aiohttp.ClientSession, fediverse_handle: str
) -> str | None:
    """Looks up the actor url associated with a FediVerse handle,
    i.e. an identifier of the form username@domain, using
    the webfinger endpoint

    :param session: the aiohttp.ClientSession to use
    :param fediverse_handle: the FediVerse handle as a string
    """
    username, domain = parse_fediverse_handle(fediverse_handle)

    webfinger_url = f"https://{domain}/.well-known/webfinger"
    params = {"resource": f"acct:{username}@{domain}"}

    return await lookup_with_webfinger(session, webfinger_url, params)


async def lookup_did_with_webfinger(
    session: aiohttp.ClientSession, domain: str, did: str
) -> str | None:
    """Looks up the actor url associated with a did and domain
    using the webfinger endpoint

    :param session: the aiohttp.ClientSession to use
    :param domain: the domain to perform the lookup from
    :param did: the did key to perform lookup with
    """
    webfinger_url = f"https://{domain}/.well-known/webfinger"
    params = {"resource": did}

    return await lookup_with_webfinger(session, webfinger_url, params)


async def fetch_nodeinfo(session: aiohttp.ClientSession, domain: str) -> dict | None:
    """Fetches the nodeinfo 2.0 object from domain using the /.well-known/nodeinfo
    endpoint"""

    try:
        data = await fetch_nodeinfo_document(session, domain)

        for link in data["links"]:
            if link["rel"] == "http://nodeinfo.diaspora.software/ns/schema/2.0":
                return await fetch_nodeinfo20(session, link["href"])

        return None

    except Exception as e:
        logger.error(str(e))
        for log_line in traceback.format_exc().splitlines():
            logger.error(log_line)
        return None
