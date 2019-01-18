#!/usr/bin/env python3

"""
ble2mqttd -- systemctl service script to read pH data coming into BLE device 
            from an eddystone beacon put it in a json string
            and send it up to an mqtt broker


This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  

See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


from json import JSONEncoder as json
from binascii import unhexlify
from datetime import datetime

# convert TX & RSSI to distance
# TX is measured from beacon

from math import pow

_TX_ = -59

def getDistance (RSSI, TX):
    return pow(10, (TX - RSSI) / (10 * 2));


# scan for & pick up BLE beacon signal using bluepy 
# to get bluepy: pip install bluepy

from bluepy.btle import Scanner, DefaultDelegate

_pHprobe1_addr = 'e5:b5:5a:fa:76:de'

import logging
import random
import socket
import time
import sys
import os

# All singletons are prefixed the
theLog = logging.getLogger(__name__)

def systemd_ready(address, sock):
    """Helper function to send a ready signal."""
    message = b"READY=1"
    theLog.debug("Signaling system ready")
    return sd_message(address, sock, message)


def systemd_stop(address, sock):
    """Helper function to signal service stopping."""
    message = b"STOPPING=1"
    return sd_message(address, sock, message)


def systemd_status(address, sock, status):
    """Helper function to update the service status."""
    message = ("STATUS=%s" % status).encode('utf8')
    return sd_message(address, sock, message)


def print_err(msg):
    """Print an error message to STDERR and quit."""
    print(msg, file=sys.stderr)
    sys.exit(1)


def mainloop(notify, period, probability):
    """A simple mainloop, spinning 100 times.
    Uses the probability flag to test how likely it is to cause a
    watchdog error.
    """
    systemd_status(*notify,
                   status="Mainloop started, probability: %s" % probability)

    for x in range(100):
        watchdog_ping(*notify)
        theLog.debug("Sending Watchdog ping: %s" % x)
        time.sleep(period)
        if random.random() < probability:
            systemd_status(*notify, status=b"Probability hit, sleeping extra")
            theLog.info("Sleeping extra, watch for triggered watchdog")
            time.sleep(1)

    theLog.info("Orderly shutdown")
    systemd_status(*notify, status=b"Shutting down")
    systemd_stop(*notify)


def get_probability():
    """Grab the probability from the environment.
    Return it if set, otherwise falls back to 0.01
    """
    prob = os.environ.get("PROBABILITY", "0.01")
    return float(prob)


if __name__ == "__main__":
    # Get our settings from the environment

    notify = notify_socket()
    period = watchdog_period()
    probability = get_probability()
    # Validate some in-data
    if not notify[0]:
        print_err("No notification socket, not launched via systemd?")
    if not period:
        print_err("No watchdog period set in the unit file.")

    # Start processing
    systemd_status(*notify, status=b"Initializing")

    logging.basicConfig()
    theLog.setLevel(logging.DEBUG)

    # Cut off a bit from the period to make the ping/Execution time work
    period -= 0.01

    theLog.info("We have to ping every: {} seconds".format(period))
    theLog.info("Signalling ready")
    systemd_ready(*notify)

    mainloop(notify, period, probability)
