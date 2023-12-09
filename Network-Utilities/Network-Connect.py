import subprocess
import pyautogui



commands = { "SCAN":       "sudo iwctl station wlan0 scan",
             "SELECT":     "sudo iwctl station wlan0 get-networks",
             "CONNECT":    "sudo iwctl station wlan0 connect {}",
             "REQUEST IP": "sudo dhcpcd"                            }



while True:
    network_host_scan = subprocess.run( commands["SCAN"].split(),
                                        stdout = subprocess.PIPE,
                                        stderr = subprocess.STDOUT )\
                                  .returncode

    host_discovery_results = subprocess.Popen( commands["SELECT"].split("\n"),
                                               stdout - subprocess.PIPE,
                                               stderr = subprocess.STDOUT     )\

    print( host_discovery_results.stdout\
                                 .read()\
                                 .decode() )

    """
    if network_host_scan != 0:
        # Turn the wifi off and on, then try again.
        pyautogui.hotkey("fn", "f5"); sleep(.1)
        pyautogui.hotkey("fn", "f5")

    else: break

   """
