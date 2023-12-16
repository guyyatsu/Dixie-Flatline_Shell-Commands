#!/bin/python3
"""
"""

from subprocess import run
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT

from pyautogui import hotkey

#import tkinter as tk


""" Linux System Commands
The 'commands' dictionary establishes a local short-hand for making system
calls to the underlying Linux kernel.  The commands being used invoke
functionality from a bare-bones IWD network stack; complete with control over
the network hardware itself, as well as RFKILL and IP package protocols.

The list of commands enacted are as follows:
    - PING: Impatiently send a packet to a host of your choosing.
    - SCAN: Use IWD to search for local WIFI access points.
    - SELECT: Curate a list of discovered access points.
    - CONNECT: Connect to a network of your choosing; may require a password.
    - REQUEST IP: Solicit the network's router for an address space.
    - HARDWARE RESET: Ensure successful connection by removing any potential
                      blocking rules placed upon the network hardware.
"""

# NOTE: These commands will probably only work on a Linux system.
#       And not even every linux system, at that.
commands = { "PING":           "ping -c1 -W2 {}",
             "SCAN":           "sudo iwctl station wlan0 scan",
             "SELECT":         "sudo iwctl station wlan0 get-networks",
             "CONNECT":        "sudo iwctl station wlan0 connect {}",
             "REQUEST IP":     "sudo dhcpcd",
             "HARDWARE RESET": ( f"sudo rfkill unblock all; ",
                                 f"sudo ip link set wlan0 down; ",
                                 f"sudo ip link set wlan0 up"     )    }


# Attempt to connect to any previously connected networks if any are present.
try:
    run( commands["REQUEST IP"].split(),
         stdout = PIPE, stderr = STDOUT  )

    if run( commands["PING"],
            stdout = PIPE, stderr = STDOUT ).returncode is not 0:

        # Turn the wifi card off then back on again.
        hotkey("fn", "f5"); sleep(.5)
        hotkey("fn", "f5")


# Scan for wifi access points around the local area.
# NOTE: This must be retried every time we recieve a non-zero exit status.
network_host_scan = run( commands["SCAN"].split(),
                         stdout = PIPE, stderr = STDOUT ).returncode

# Gather a list of networks discovered during the scan.
host_discovery_results = Popen( commands["SELECT"].split(),
                                stdout = PIPE, stderr = STDOUT ).stdout\
                                                                .read()\
                                                                .decode()
# Trim the whitespace lines from the formatted text results.
results = host_discovery_results.split("\n")[4:]
del results[-1]; del results[-1]


"""
So this next part was some bullshit; to the point I almost asked ChatGPT for
help.

The problem here is we have a list of lines consisting of unicode and
plaintext; where the first item in the list usually has three blocks of
unicode; then two blocks of plaintext that we need, and they all have a
trailing block of unicode we can disregard.  As well, every item beyond the
first simply starts with the two textblocks we're looking for.

Since this all exists within the context of a network connection we can
conduct a ping scan before we look at the list to determine if the first
item in the list is going to be unicode or not.

As for actually trimming the unicode off; we can just delete those items
while iterating.
"""

# NOTE: This only needs to run if we fail a pingscan.
# Split each line along it's whitespace into tokens.
items = []
for item in results:
    items.append(item.split())

# Delete the first three tokens from item[0].
del items[0][0:3]

# Delete the token from every item.
for item in range(0, len(items)):
    del items[item][-1]

"""
I figured a solution; after a successful pingscan we're always going to delete
three tokens from item[0].  So, we DON'T need to get crazy here with what we're
doing; just store the tokens as a nested list and delete the first token from
the first item three times.  EZPZ.
"""
for item in items:
    print(item)


