import lyricsgenius
import sys

from exceptions.lyrics_not_found import LyricsNotFoundError

genius_token: str = "udS-ThnfpSvQIl5H-wCoKeXhydgLTdpsp1L-0_sW2VANeiWZbK5xvfTOTTnnUCz1"

# initialize genius 
genius_api = lyricsgenius.Genius(genius_token)

# Turn off status messages
genius_api.verbose = False

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
            return song.lyrics
    except ConnectionError:
        print("No internet connection!")
        sys.exit()

    raise LyricsNotFoundError
