import re
import os
import sys
import dbus
from pathlib import Path

from tulyp.lyrics_sources import genius, google, azlyrics
from tulyp.exceptions.lyrics_not_found import LyricsNotFoundError

cache_path = Path.home().joinpath(".cache", "lyrics")

def create_cache_path(seed: str) -> str:
    """Return a file path generated from the input to save the lyrics to.

    Args:
        seed_str (str): The string from which the filename will be generated.
    """
    filename = re.sub(r"(\[.*\].*)|(\(.*\).*)", "", seed).strip()
    filename = re.sub(r"\s|\/|\\|\.", "", filename)
    return os.path.join(cache_path, filename)

def get_dbus_interface(player: str) -> dbus.Interface:
    try:
        session_bus = dbus.SessionBus()

        bus_name = f"org.mpris.MediaPlayer2.{player}"
        obj_path = "/org/mpris/MediaPlayer2"

        bus = session_bus.get_object(bus_name=bus_name, object_path=obj_path)

        return dbus.Interface(bus, "org.freedesktop.DBus.Properties")

    except dbus.DBusException:
        print(f"{player} is not running")
        sys.exit()

def get_lyrics(title: str, artist: str, source: str = "", cache: bool = True) -> str:
    """Get lyrics for a song from the given source.

    Lyrics will be written to a cache file after obtaining them from a source.
    Further calls will provide the lyrics from the cache, unless a source is
    passed in.

    Args:
        title (str): The title of the song.
        artist (str): The artist of the song.
        source (str): The source to fetch lyrics from (genius, azlyrics, google).
        cache (bool): If True, try serving the lyrics from cache.

    Returns:
        str: The lyrics of the song as a single string.
    """
    # some empty lines concatenated to the lyrics for better readablility
    bottom_padding = "\n" * 30
    track_name = f"{artist} - {title}"
    filepath = create_cache_path(track_name)
    serving_from_cache = False

    if not os.path.isdir(cache_path):
        os.makedirs(cache_path)

    if os.path.isfile(filepath) and cache:
        with open(filepath) as file:
            lyrics = file.read()
            serving_from_cache = True
    elif source == "":
        try:
            genius.init_genius_api()
            lyrics = genius.get_lyrics(title=title, artist=artist)
        except LyricsNotFoundError:
            try:
                lyrics = google.get_lyrics(title=title, artist=artist)
            except LyricsNotFoundError:
                lyrics = azlyrics.get_lyrics(title=title, artist=artist)
    else:
        match source:
            case "genius":
                genius.init_genius_api()
                lyrics = genius.get_lyrics(title=title, artist=artist)
            case "google":
                lyrics = google.get_lyrics(title=title, artist=artist)
            case "azlyrics":
                lyrics = azlyrics.get_lyrics(title=title, artist=artist)
            case _:
                print(f"Unknown source {source}")
                sys.exit()

    if not serving_from_cache and lyrics is not None:
        with open(filepath, "w") as file:
            file.writelines(lyrics)

    return f"{track_name}\n\n{lyrics}{bottom_padding}"
