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
sys.path.append(PPRZ_SRC + "/sw/lib/python")

from ivy_msg_interface import IvyMessagesInterface
from pprz_msg.message import PprzMessage
from settings_xml_parse import PaparazziACSettings

from math import radians
from time import sleep


class GuidanceMsg(object):
    def __init__(self, ac_id, verbose=False):
        self.ac_id = ac_id
        self.verbose = verbose
        self._interface = None
        self.auto2_index = None
        try:
            settings = PaparazziACSettings(self.ac_id)
        except Exception as e:
            print(e)
            return
        try:
            self.auto2_index = settings.name_lookup['auto2'].index
        except Exception as e:
            print(e)
            print("auto2 setting not found, mode change not possible.")
        self._interface = IvyMessagesInterface(self.message_recv)

    def message_recv(self, ac_id, msg):
        if self.verbose:
            print("Got msg %s" % msg.name)

    def shutdown(self):
        if self._interface is not None:
            print("Shutting down ivy interface...")
            self._interface.shutdown()

    def __del__(self):
        self.shutdown()

    def set_guided_mode(self):
        """
        change auto2 mode to GUIDED.
        """
        if self.auto2_index is not None:
            msg = PprzMessage("ground", "DL_SETTING")
            msg['ac_id'] = self.ac_id
            msg['index'] = self.auto2_index
            msg['value'] = 19  # AP_MODE_GUIDED
            print("Setting mode to GUIDED: %s" % msg)
            self._interface.send(msg)

    def set_nav_mode(self):
        """
        change auto2 mode to NAV.
        """
        if self.auto2_index is not None:
            msg = PprzMessage("ground", "DL_SETTING")
            msg['ac_id'] = self.ac_id
            msg['index'] = self.auto2_index
            msg['value'] = 13  # AP_MODE_NAV
            print("Setting mode to NAV: %s" % msg)
            self._interface.send(msg)

    def set_guidance(self, flag, x, y, z, yaw):
        """
        set a local position in meters (if already in GUIDED mode)
        """
        msg = PprzMessage("datalink", "GUIDED_SETPOINT_NED")
        msg['ac_id'] = self.ac_id
        msg['flags'] = flag
        msg['x'] = x
        msg['y'] = y
        msg['z'] = z
        msg['yaw'] = yaw
        print("set guidance: %s" % msg)
        # embed the message in RAW_DATALINK so that the server can log it
        self._interface.send_raw_datalink(msg)

    def goto_ned(self, north, east, down, heading=0.0):
        """
        goto a local NorthEastDown position in meters (if already in GUIDED mode)
        """
        msg = PprzMessage("datalink", "GUIDED_SETPOINT_NED")
        msg['ac_id'] = self.ac_id
        msg['flags'] = 0x00
        msg['x'] = north
        msg['y'] = east
        msg['z'] = down
        msg['yaw'] = heading
        print("goto NED: %s" % msg)
        # embed the message in RAW_DATALINK so that the server can log it
        self._interface.send_raw_datalink(msg)

    def goto_ned_relative(self, north, east, down, yaw=0.0):
        """
        goto a local NorthEastDown position relative to current position in meters (if already in GUIDED mode)
        """
        msg = PprzMessage("datalink", "GUIDED_SETPOINT_NED")
        msg['ac_id'] = self.ac_id
        msg['flags'] = 0x01
        msg['x'] = north
        msg['y'] = east
        msg['z'] = down
        msg['yaw'] = yaw
        print("goto NED relative: %s" % msg)
        self._interface.send_raw_datalink(msg)

    def goto_body_relative(self, forward, right, down, yaw=0.0):
        """
        goto to a position relative to current position and heading in meters (if already in GUIDED mode)
        """
        msg = PprzMessage("datalink", "GUIDED_SETPOINT_NED")
        msg['ac_id'] = self.ac_id
        msg['flags'] = 0x03
        msg['x'] = forward
        msg['y'] = right
        msg['z'] = down
        msg['yaw'] = yaw
        print("goto body relative: %s" % msg)
        self._interface.send_raw_datalink(msg)


if __name__ == '__main__':
    ac_id     = int(sys.argv[1])
    flag_mask = int(sys.argv[2])
    yaw_value = float(sys.argv[6])
    cmd_time  = float(sys.argv[7])
    try:
        gm = GuidanceMsg(ac_id)
        sleep(0.2)

        # KLUDGE: Overload flag_mask to enable(5)/disble(6) the guided mode
        if flag_mask == 5:
            gm.set_guided_mode()
            sleep(0.2)
        elif flag_mask == 6:
            gm.set_nav_mode()
            sleep(0.2)        

        # KLUDGE: Execute guidance command if valid flag_mask (i.e. < 5)
        if flag_mask < 5: 
            gm.set_guidance(flag=sys.argv[2], x=sys.argv[3], y=sys.argv[4], z=sys.argv[5], yaw=radians(yaw_value))
            sleep(cmd_time)  # Time to spend in guided mode to allow the above instruction/message to express itself        

    
        # UNUSED CODE BLOCK    
        #gm.goto_ned(north=10.0, east=5.0, down=-5.0, heading=radians(90))
        #sleep(10)
        #gm.goto_ned_relative(north=-5.0, east=-5.0, down=-2.0, yaw=-radians(45))
        #sleep(10)
        #gm.goto_body_relative(forward=0.0, right=5.0, down=2.0)
        #sleep(10)

    except KeyboardInterrupt:
        print("Stopping on request")
    gm.shutdown()
