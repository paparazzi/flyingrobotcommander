#!/usr/bin/env python

"""
/*
 * Copyright (C) 2003-2016 The Paparazzi Team
 *
 * This file is part of paparazzi.
 *
 * paparazzi is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 *
 * paparazzi is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with paparazzi; see the file COPYING.  If not, see
 * <http://www.gnu.org/licenses/>.
 */
"""

from __future__ import print_function

import sys
from os import path, getenv

# if PAPARAZZI_SRC not set, then assume the tree containing this
# file is a reasonable substitute
PPRZ_SRC = getenv("PAPARAZZI_SRC", path.normpath(path.join(path.dirname(path.abspath(__file__)), '../../../')))
sys.path.append(PPRZ_SRC + "/sw/ext/pprzlink/lib/v1.0/python")

from ivy_msg_interface import IvyMessagesInterface
from pprzlink.message import PprzMessage
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
