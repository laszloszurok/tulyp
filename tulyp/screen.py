import curses
import subprocess
import sys

class Screen(object):
    UP = -1
    DOWN = 1

    def __init__(self, items):
        self.window = None

        self.width = 0
        self.height = 0

        self.init_curses()

        self.items = items

        self.max_lines = curses.LINES
        self.top = 0
        self.bottom = len(self.items)

    def init_curses(self):
        """Setup the curses"""
        self.window = curses.initscr()
        self.window.keypad(True)
        self.window.timeout(2000)

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

        self.height, self.width = self.window.getmaxyx()

    def run(self):
        """Continue running the TUI until get interrupted"""
        try:
            self.input_stream()
        except KeyboardInterrupt:
            pass
        finally:
            curses.endwin()

    def input_stream(self):
        """Waiting an input and run a proper method according to type of input"""
        while True:
            self.height, self.width = self.window.getmaxyx()
            curses.resize_term(self.height, self.width)
            self.max_lines = curses.LINES
            self.display()

            subprocess.run(["notify-send", "tulyp: in event loop"])

            ch = self.window.getch()

            if ch == curses.KEY_UP or ch == ord('k'):
                self.scroll(self.UP)
            elif ch == curses.KEY_DOWN or ch == ord('j'):
                self.scroll(self.DOWN)
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
            self.window.addstr(idx, 0, item)
        self.window.refresh()
