import lyricsgenius
import sys
import re

from exceptions.lyrics_not_found import LyricsNotFoundError

genius_token: str = "udS-ThnfpSvQIl5H-wCoKeXhydgLTdpsp1L-0_sW2VANeiWZbK5xvfTOTTnnUCz1"

# initialize genius 
genius_api = lyricsgenius.Genius(genius_token)

# Turn off status messages
genius_api.verbose = False

def format_lyrics(lyrics: str) -> str:
    """Remove some unuseful string patterns from the input lyrics string.
    
    Used to clean up the lyrics returned from genius.com. Sometimes the
    returned lyrics contain some trailing strings, that are not part of
    the lyrics. They are just other strings that happen to be on genius.com
    under the lyrics section. This function removes those and returns only
    the lyrics.

    Keyword arguments:
        lyrics: str -- the lyrics gathered from genius.com
    """
    lyrics = re.sub(r"EmbedShare Url:CopyEmbed:Copy", "", lyrics)

    return lyrics

def get_lyrics(title: str, artist: str) -> str:
    """Search for a song on genius.com and return the lyrics.

    The lyricsgenius module is used to get the lyrics from
    genius.com. If there are no lyrics for a song, this
    function will raise a LyricsNotFoundError exception.
    
    Keyword arguments:
        title: str  -- the title of the song
        artist: str -- the name of the artist

    Raises:
        LyricsNotFoundError
    """
    try:
        song = genius_api.search_song(title=title, artist=artist)
        if song is not None:
            return format_lyrics(song.lyrics)
    except ConnectionError:
        print("No internet connection!")
        sys.exit()

    raise LyricsNotFoundError
