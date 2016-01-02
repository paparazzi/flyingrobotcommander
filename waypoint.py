#!/usr/bin/env python

from __future__ import print_function

import sys
from os import path, getenv
from time import sleep

# if PAPARAZZI_SRC not set, then assume the tree containing this
# file is a reasonable substitute
PPRZ_SRC = getenv("PAPARAZZI_SRC", path.normpath(path.join(path.dirname(path.abspath(__file__)), '../../../')))
sys.path.append(PPRZ_SRC + "/sw/lib/python")

from ivy_msg_interface import IvyMessagesInterface
from pprz_msg.message import PprzMessage


class WaypointMsg(object):
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

    def set_waypoint(self, ac_id, wp_id, lat, lon, alt):
        msg = PprzMessage("ground", "MOVE_WAYPOINT")
        msg['ac_id'] = ac_id
        msg['wp_id'] = wp_id
        msg['lat'] = lat
        msg['long'] = lon
        msg['alt'] = alt
        print("Sending message: %s" % msg)
        self._interface.send(msg)


if __name__ == '__main__':
    try:
        wpm = WaypointMsg()
        # sleep shortly in oder to make sure Ivy is up, then message sent before shutting down again
        sleep(0.2)
        wpm.set_waypoint(ac_id=sys.argv[1], wp_id=sys.argv[2], lat=sys.argv[3], lon=sys.argv[4], alt=sys.argv[5])
        #wpm.move_waypoint(ac_id=217, wp_id=6, lat=45.5643, lon=-122.6219406, alt=61.0) # Move Waypoint p3
        #wpm.move_waypoint(ac_id=218, wp_id=6, lat=45.5644, lon=-122.6219406, alt=61.0) # Move Waypoint p3
        sleep(0.2)
    except KeyboardInterrupt:
        print("Stopping on request")
    wpm.shutdown()
