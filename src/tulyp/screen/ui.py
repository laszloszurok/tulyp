import curses
import sys

from tulyp.utils.misc import get_lyrics
from tulyp.exceptions.lyrics_not_found import LyricsNotFoundError

class Screen(object):
    UP = -1
    DOWN = 1

    def __init__(self, dbus_interface, items: list[str] = []):
        self.window = curses.initscr()
        self.window.keypad(True)
        self.window.timeout(2000)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

        self.width = 0
        self.height = 0

        self.items = items
        self.dbus_interface = dbus_interface
        self.artist = None
        self.title = None

        self.max_lines = curses.LINES
        self.top = 0
        self.bottom = len(self.items)

        self.height, self.width = self.window.getmaxyx()

    def run(self):
        """Continue running the TUI until getting interrupted."""
        try:
            self.input_stream()
        except KeyboardInterrupt:
            pass
        finally:
            curses.endwin()

    def update_lyrics(self, source: str = "", force=False):
        try:
            metadata = self.dbus_interface.Get(
                "org.mpris.MediaPlayer2.Player",
                "Metadata"
            )
            artist = metadata.get("xesam:albumArtist")[0]
            title = metadata.get("xesam:title")
        except:
            sys.exit()

        if force or self.artist != artist or self.title != title:
            self.artist = artist
            self.title = title
            try:
                if source != "":
                    self.items = get_lyrics(
                        title=title,
                        artist=artist,
                        source=source,
                        cache=False
                    ).splitlines()
                else:
                    self.items = get_lyrics(
                        title=title,
                        artist=artist
                    ).splitlines()
            except LyricsNotFoundError:
                self.items = ["no lyrics found"]
            self.top = 0
            self.bottom = len(self.items)

    def input_stream(self):
        """Wait for an input and run a proper method according to type of input."""
        while True:
            self.height, self.width = self.window.getmaxyx()
            curses.resize_term(self.height, self.width)
            self.max_lines = curses.LINES
            
            self.update_lyrics()
            
            self.display()

            ch = self.window.getch()

            if ch == curses.KEY_UP or ch == ord('k'):
                self.scroll(self.UP)
            elif ch == curses.KEY_DOWN or ch == ord('j'):
                self.scroll(self.DOWN)
            elif ch == ord('1'):
                self.update_lyrics(source="genius", force=True)
            elif ch == ord('2'):
                self.update_lyrics(source="google", force=True)
            elif ch == ord('3'):
                self.update_lyrics(source="azlyrics", force=True)
            elif ch == ord('q'):
                sys.exit()

    def scroll(self, direction):
        """Scrolling the window when pressing up/down arrow keys"""

        # Up direction scroll overflow
        # current cursor position is 0, but top position is greater than 0
        if (direction == self.UP) and (self.top > 0):
            self.top += direction
            return
        # Down direction scroll overflow
        # next cursor position touch the max lines, but absolute position of max lines could not touch the bottom
        if (direction == self.DOWN) and (self.top + self.max_lines < self.bottom):
            self.top += direction
            return

    def display(self):
        """Display the items on window"""
        self.window.erase()
        for idx, item in enumerate(self.items[self.top:self.top + self.max_lines]):
            self.window.addnstr(idx, 0, item, self.width - 1)
        self.window.refresh()
