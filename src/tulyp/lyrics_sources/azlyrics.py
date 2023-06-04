import sys
import re
from urllib.request import Request, urlopen
from urllib.error import URLError
from urllib.parse import quote_plus

from tulyp.exceptions.lyrics_not_found import LyricsNotFoundError

HEADER = {"User-Agent": "Mozilla/5.0"}
base_url = "https://www.google.com/search?q="

def get_html(search_url: str, header: dict[str, str] = HEADER) -> str:
    """Return html text from given search_url."""
    try:
        req = Request(search_url, data=None, headers=header)
        req_search_url = urlopen(req)
    except URLError:
        sys.exit()

    if req_search_url.code != 200:
        sys.exit()

    return req_search_url.read().decode("utf-8")


def get_az_html(search_url: str) -> str:
    """Find azlyrics website link and return html text from azlyrics.

    If azlyrics link not found return error string.
    """
    html = get_html(search_url.replace("lyrics", "azlyrics"))
    if isinstance(html, tuple):
        return html

    regex = re.compile(r"(http[s]?://www.azlyrics.com/lyrics(?:.*?))&amp")
    az_search_url = regex.search(html)

    if az_search_url is None:
        return "No Lyrics Found!"
    else:
        header = {"User-Agent": "Mozilla/5.0 Firefox/70.0"}
        az_search_url = az_search_url.group(1)
        az_html = get_html(az_search_url, header)
        return az_html


def get_lyrics(title: str, artist: str) -> str:
    """Fetch lyrics from azlyrics and return a list of strings of the lyrics."""
    search_url = f"{base_url}{quote_plus(string=f'{artist} {title} lyrics')}"

    az_html = get_az_html(search_url)

    if isinstance(az_html, tuple):
        return az_html[0]

    az_regex = re.compile(
        r"<!--Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->(.*)<!-- MxM banner -->", re.S)

    ly = az_regex.search(az_html)
    if ly is None:
        raise LyricsNotFoundError

    rep = {"&quot;": "\"", "&amp;": "&", "\r": ""}

    ly = re.sub(r"<[/]?\w*?>", "", ly.group(1)).strip()
    ly = re.sub("|".join(rep.keys()), lambda match: rep[match.group(0)], ly)

    return ly
