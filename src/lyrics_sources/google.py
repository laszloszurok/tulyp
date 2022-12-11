import sys
import re
from urllib.request import Request, urlopen
from urllib.error import URLError
from urllib.parse import quote

HEADER = {"User-Agent": "Mozilla/5.0"}
CLASS_NAME = r"\w{5,7} \w{4,5} \w{5,7}"  # dependent on User-Agent

def get_html(search_url: str, header: str = HEADER) -> str:
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

def get_lyrics(search_url: str) -> str:
    """Fetch lyrics from google and return list of strings."""
    html = get_html(search_url)
    if isinstance(html, tuple):
        return html[0]

    html_regex = re.compile(
        r"<div class='{}'>([^>]*?)</div>".format(CLASS_NAME), re.S)

    text_list = html_regex.findall(html)

    lyrics_lines = []
    for lyric in text_list[1:]:
        # lyrics must be multiline,
        # ignore the artist info below lyrics
        if lyric.count("\n") > 2:
            lyrics_lines += lyric.split("\n")

    return lyrics_lines
