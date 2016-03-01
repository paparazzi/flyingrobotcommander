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
import os
import argparse
from flask import Flask

# if PAPARAZZI_SRC not set, then assume the tree containing this
# file is a reasonable substitute
PPRZ_SRC = getenv("PAPARAZZI_SRC", path.normpath(path.join(path.dirname(path.abspath(__file__)), '../../../')))
sys.path.append(PPRZ_SRC + "/sw/lib/python")
sys.path.append(PPRZ_SRC + "/sw/ext/pprzlink/lib/v1.0/python")

from ivy_msg_interface import IvyMessagesInterface
from pprzlink.message import PprzMessage
from settings_xml_parse import PaparazziACSettings

from math import radians


app = Flask(__name__)

ivy_interface = IvyMessagesInterface("FlyingRobotCommander", start_ivy=False)
frc_version = "0.0.2"


@app.route('/')
def index():
    return 'Index Page'

@app.route('/guidance/')
def guidance_all():
    return 'Guidance: All'

#Set auto2 mode to GUIDED(value=19) or NAV(value=13).
@app.route('/guidance/setmode/<int:ac_id>/<int:value>')
def guidance_setmode(ac_id, value):
    try:
        settings = PaparazziACSettings(ac_id)
    except Exception as e:
        print(e)
        return
    try:
        index = settings.name_lookup['auto2'].index
    except Exception as e:
        print(e)
        print("auto2 setting not found, mode change not possible.")
        return

    if index is not None:
        msg = PprzMessage("ground", "DL_SETTING")
        msg['ac_id'] = ac_id
        msg['index'] = index
        msg['value'] = value
        print("Setting mode to: %s" % msg)
        ivy_interface.send(msg)
        return 'Guidance mode: ac_id=%d, index=%d, value=%d' % (ac_id, index, value)


@app.route('/guidance/<int:ac_id>/<int:flag>/<x>/<y>/<z>/<yaw>')
def guidance(ac_id, flag, x, y, z, yaw):
    msg = PprzMessage("datalink", "GUIDED_SETPOINT_NED")
    msg['ac_id'] = ac_id
    msg['flags'] = flag
    msg['x'] = x
    msg['y'] = y
    msg['z'] = z
    msg['yaw'] = yaw
    print("Sending message: %s" % msg)
    ivy_interface.send_raw_datalink(msg)
    return 'Guidance: ac_id=%d, flag=%d, x=%s, y=%s, z=%s, yaw=%s' % (ac_id, flag, x, y, z, yaw)

@app.route('/waypoint/')
def waypoint_all():
    return 'Waypoint: All'

@app.route('/waypoint/<int:ac_id>/<int:wp_id>/<lat>/<lon>/<alt>')
def waypoint(ac_id, wp_id, lat, lon, alt):
    msg = PprzMessage("ground", "MOVE_WAYPOINT")
    msg['ac_id'] = ac_id
    msg['wp_id'] = wp_id
    msg['lat'] = lat
    msg['long'] = lon
    msg['alt'] = alt
    print("Sending message: %s" % msg)
    ivy_interface.send(msg)
    return 'Waypoint: ac_id=%d, wp_id=%d, lat=%s, lon=%s, alt=%s' % (ac_id, wp_id, lat, lon, alt)

@app.route('/flightblock/<int:fb_id>')
def flightblock_all():
    # TBD : Need to query the server for all aircraft id prior to calling this route
    return 'Flightblock: All Aircraft'

@app.route('/flightblock/<int:ac_id>/<int:fb_id>')
def flightblock(ac_id, fb_id):
    msg = PprzMessage("ground", "JUMP_TO_BLOCK")
    msg['ac_id'] = ac_id
    msg['block_id'] = fb_id
    print("Sending message: %s" % msg)
    ivy_interface.send(msg)
    return 'Flightblock: ac_id=%d, fb_id=%d' % (ac_id, fb_id)

@app.route('/about')
def about():
    return 'About: Flying Robot Commander Server v%s' % (frc_version)

if __name__ == '__main__':

    # Get the required IP address and port number command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", type=str, default="127.0.0.1",
                        help="ip address")
    parser.add_argument("-p","--port", type=int, default=5000,
                        help="port number")
    try:
        args = parser.parse_args()

        ivy_interface.start()

        # Supply flask the appropriate ip address and port for the server
        app.run(host=args.ip,port=args.port)

        ivy_interface.shutdown()
    except Exception as e:
        print(e)
        sys.exit(0)
