import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

from tulyp.exceptions.lyrics_not_found import LyricsNotFoundError

BASE_URL: str = "https://www.google.com/search?q="
HEADERS: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:79.0) Gecko/20100101 Firefox/79.0",
    "Host": "www.google.com",
    "Referer": "https://www.google.com/"
}

def get_lyrics(title: str, artist: str) -> str:
    """Search for the given song on Google and return the lyrics.

    Parse the response html of the Google search and extract the lyrics, then
    return it as a string, keeping the formatting of the original text. A
    LyricsNotFoundError exception is raised, if no lyrics were found.

    Args:
        title (str): The title of the song to search for.
        artist (str): The artist of the song to search for.

    Returns:
        str: The lyrics.

    Raises:
        LyricsNotFoundError: No lyrics were found on Google.
    """
    search_url: str = f"{BASE_URL}{quote_plus(string=f'{artist} {title} lyrics')}"

    try:
        web_page: str = requests.get(url=search_url, headers=HEADERS).text
    except:
        raise LyricsNotFoundError

    html = BeautifulSoup(web_page, "html.parser")
    target_div = html.find(name="div", attrs={"jsname": "WbKHeb"})

    if target_div is not None and target_div.contents:
        lyrics_html: list[str] = target_div.contents
    else:
        raise LyricsNotFoundError

    lyrics: str = ""

    for verse_html in lyrics_html:
        verse_html_pretty = BeautifulSoup(str(verse_html), "html.parser").prettify()
        verse = BeautifulSoup(verse_html_pretty, "html.parser").get_text()
        verse = os.linesep.join([line.strip() for line in verse.splitlines() if line.strip()])
        lyrics = f"{lyrics}{verse}\n\n"

    return lyrics

