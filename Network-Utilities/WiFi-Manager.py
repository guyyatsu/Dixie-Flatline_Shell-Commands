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

commands = { "SCAN":       "sudo iwctl station wlan0 scan",
             "SELECT":     "sudo iwctl station wlan0 get-networks",
             "CONNECT":    "sudo iwctl station wlan0 connect {}",
             "REQUEST IP": "sudo dhcpcd"                            }




# Scan for wifi access points around the local area.
network_host_scan = subprocess.run( commands["SCAN"].split(),
                                    stdout = subprocess.PIPE,
                                    stderr = subprocess.STDOUT )\
                              .returncode

# Gather a list of networks discovered during the scan.
host_discovery_results = subprocess.Popen( commands["SELECT"].split(),
                                           stdout = subprocess.PIPE,
                                           stderr = subprocess.STDOUT     )\
                                   .stdout\
                                   .read()\
                                   .decode()
#results = ( host_discovery_results


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
