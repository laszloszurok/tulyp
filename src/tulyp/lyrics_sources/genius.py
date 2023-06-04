import lyricsgenius
import re
import os
from requests.exceptions import Timeout

from tulyp.exceptions.lyrics_not_found import LyricsNotFoundError

genius_api = None

def init_genius_api():
    """Initialize the genius API with an acces token.

    The token can be provided through an environment variable called
    TULYP_GENIUS_TOKEN. If this env var is not set, a default token
    will be used for initialization.
    """
    global genius_api

    try:
        genius_token = os.environ["TULYP_GENIUS_TOKEN"]
    except KeyError:
        genius_token = "udS-ThnfpSvQIl5H-wCoKeXhydgLTdpsp1L-0_sW2VANeiWZbK5xvfTOTTnnUCz1"

    genius_api = lyricsgenius.Genius(genius_token)

    # Turn off status messages
    genius_api.verbose = False

def format_lyrics(lyrics: str, title: str) -> str:
    """Remove some unuseful string patterns from the input lyrics string.
    
    Used to clean up the lyrics returned from genius.com. Sometimes the
    returned lyrics contain some trailing strings, that are not part of
    the lyrics. They are just other strings that happen to be on genius.com
    under the lyrics section. This function removes those and returns only
    the lyrics.

    Args:
        lyrics (str): The lyrics gathered from genius.com.
    """
    lyrics = lyrics.replace(chr(0x2019), "'") # replace unicode quote
    lyrics = re.sub(rf"{title}\s* Lyrics", "", lyrics, flags=re.IGNORECASE) # remove title from first line of lyrics
    lyrics = re.sub(r"EmbedShare Url:CopyEmbed:Copy", "", lyrics)
    lyrics = re.sub(r"[0-9]*Embed*", "", lyrics)
    lyrics = re.sub(r"You might also like", "", lyrics)
    lyrics = re.sub(r"Translations.*\[", "[", lyrics)
    lyrics = re.sub(r"[0-9].*Contributors*", "", lyrics)

    return lyrics

def get_lyrics(title: str, artist: str) -> str:
    """Search for a song on genius.com and return the lyrics.

    The lyricsgenius module is used to get the lyrics from
    genius.com. If there are no lyrics for a song, this
    function will raise a LyricsNotFoundError exception.
    
    Args:
        title (str): The title of the song.
        artist (str): The name of the artist.

    Raises:
        LyricsNotFoundError: No lyrics were found.
    """

    if genius_api is not None:
        try:
            song = genius_api.search_song(title=title, artist=artist)
            if song is not None:
                return format_lyrics(lyrics=song.lyrics, title=title)
        except Timeout:
            raise LyricsNotFoundError

    raise LyricsNotFoundError
