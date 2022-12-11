import re
import os
from pathlib import Path
from urllib.parse import quote

cache_path = Path.home().joinpath(".cache", "lyrics")

def create_query_str(title: str, artist: str) -> str:
    """Take a song title and artist and return a url endcoded string."""
    #track_name = re.sub(r"(\[.*\].*)|(\(.*\).*)", "", track_name).strip()
    return quote(f"{artist} {title} lyrics")

def create_cache_path(track_name: str) -> str:
    """Return a file path generated from track_name to save the lyrics to."""
    filename = re.sub(r"(\[.*\].*)|(\(.*\).*)", "", track_name).strip()  # removing text in brackets [] ()
    filename = re.sub(r"\s|\/|\\|\.", "", filename)
    return os.path.join(cache_path, filename)
