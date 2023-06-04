#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Credit to https://github.com/laszloszurok/tulyp

import sys
import dbus

from tulyp.utils.misc import get_dbus_interface
from tulyp.screen.ui import Screen

player = "ncspot"

if len(sys.argv) > 1:
    player = sys.argv[1]

def main() -> None:
    """Run tulyp."""
    try:
        interface = get_dbus_interface(player=player)
    except dbus.DBusException:
        print(f"{player} is not running")
        sys.exit()

    screen = Screen(dbus_interface=interface)
    screen.run()
