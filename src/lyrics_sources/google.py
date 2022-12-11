import sys
import re
from urllib.request import Request, urlopen
from urllib.error import URLError
from urllib.parse import quote

from exceptions.lyrics_not_found import LyricsNotFoundError
from utils import create_query_str

HEADER = {"User-Agent": "Mozilla/5.0"}
CLASS_NAME = r"\w{5,7} \w{4,5} \w{5,7}"  # dependent on User-Agent
base_url = "https://www.google.com/search?q="

def get_html(search_url: str, header: dict[str, str] = HEADER) -> str:
    """Return html text from given search_url."""
    try:
        req = Request(search_url, data=None, headers=header)
        req_search_url = urlopen(req)
    except URLError:
        print("No connection!")
        sys.exit()

    if req_search_url.code != 200:
        print("invalid request")
        sys.exit()

    return req_search_url.read().decode("utf-8")

def get_lyrics(title: str, artist: str) -> str:
    """Fetch lyrics from google and return list of strings."""
    
    search_url = f"{base_url}{create_query_str(title=title, artist=artist)}"

    html = get_html(search_url)
    if isinstance(html, tuple):
        return html[0]

    html_regex = re.compile(
        r"<div class='{}'>([^>]*?)</div>".format(CLASS_NAME), re.S)

    text_list = html_regex.findall(html)

    lyrics_lines = []
    for line in text_list[1:]:
        # lyrics must be multiline,
        # ignore the artist info below lyrics
        if line.count("\n") > 2:
            lyrics_lines += line.split("\n")

    if len(lyrics_lines) > 0:
        return "\n".join(lyrics_lines)

    raise LyricsNotFoundError
