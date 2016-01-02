#!/usr/bin/env python

from __future__ import print_function

import sys
from os import path, getenv

# if PAPARAZZI_SRC not set, then assume the tree containing this
# file is a reasonable substitute
PPRZ_SRC = getenv("PAPARAZZI_SRC", path.normpath(path.join(path.dirname(path.abspath(__file__)), '../../../')))
sys.path.append(PPRZ_SRC + "/sw/lib/python")

from ivy_msg_interface import IvyMessagesInterface
from pprz_msg.message import PprzMessage
from time import sleep


class FlightBlockMsg(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
        self._interface = IvyMessagesInterface(self.message_recv)

    def message_recv(self, ac_id, msg):
        if self.verbose:
            print("Got msg %s" % msg.name)

    def shutdown(self):
        print("Shutting down ivy interface...")
        self._interface.shutdown()

    def __del__(self):
        self.shutdown()

    def set_flightblock(self, ac_id, block_id):
        msg = PprzMessage("datalink", "BLOCK")
        msg['ac_id'] = ac_id
        msg['block_id'] = block_id
        print("Sending message: %s" % msg)
        self._interface.send(msg)


if __name__ == '__main__':
    try:
        fbm = FlightBlockMsg()
        sleep(0.2)
        fbm.set_flightblock(ac_id=sys.argv[1], block_id=sys.argv[2])
        sleep(0.2)
    except KeyboardInterrupt:
        print("Stopping on request")
    fbm.shutdown()
