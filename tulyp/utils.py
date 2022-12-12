import re
import os
from pathlib import Path
from urllib.parse import quote_plus

cache_path = Path.home().joinpath(".cache", "lyrics")

def create_cache_path(seed: str) -> str:
    """Return a file path generated from the input to save the lyrics to.

    Args:
        seed_str (str): The string from which the filename will be generated.
    """
    filename = re.sub(r"(\[.*\].*)|(\(.*\).*)", "", seed).strip()
    filename = re.sub(r"\s|\/|\\|\.", "", filename)
    return os.path.join(cache_path, filename)
