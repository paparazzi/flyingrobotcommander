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
import time
import argparse
from flask import Flask, request, Response
import json

# if PAPARAZZI_SRC not set, then assume the tree containing this file is a reasonable substitute
PPRZ_SRC = getenv("PAPARAZZI_SRC", path.normpath(path.join(path.dirname(path.abspath(__file__)), '~/paparazzi/')))

sys.path.append(PPRZ_SRC + "/sw/lib/python")
sys.path.append(PPRZ_SRC + "/sw/ext/pprzlink/lib/v1.0/python")

from ivy_msg_interface  import IvyMessagesInterface
from pprzlink.message   import PprzMessage
from settings_xml_parse import PaparazziACSettings

from math import radians


app = Flask(__name__)

# --- Configure server logging levels

# Only spit out error level server messages
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


# --- Class/Global state variables

ivy_interface = IvyMessagesInterface("FlyingRobotCommander", start_ivy=False)
frc_version   = "0.0.3"
verbose       = 0       # Default is disabled(i.e. = 0)
curl          = 0       # Default is disabled(i.e. = 0)
subscribe     = 0       # Default is disabled(i.e. = 0)


# --- Aircraft, Flighblock & Message related state/methods

class Message(PprzMessage):
    def __init__(self, class_name, name, msg):
        super(Message, self).__init__(class_name, name)
        self.field_controls = {}
        self.index          = None
        self.last_seen      = time.clock()
        self.latest_msg     = msg

class Flightblock(object):
    def __init__(self, fb_id, fb_name):
        self.fb_id   = fb_id
        self.fb_name = fb_name

class Aircraft(object):
    def __init__(self, ac_id, name):
        self.ac_id        = ac_id
        self.name         = name
        self.flightblocks = {}
        self.messages     = {}

aircrafts = {}

def add_new_message( aircraft, msg_class, name, msg):
    aircraft.messages[name] = Message(msg_class, name, msg)

def add_new_flightblock( aircraft, fb_id, fb_name):
    aircraft.flightblocks[fb_id] = Flightblock(fb_id, fb_name)      

def add_new_aircraft(ac_id, name):
    aircrafts[ac_id] = Aircraft(ac_id, name)

def print_aircraft_data():
    for ac_id in aircrafts:
        print( ac_id, aircrafts[ac_id].name )
        for fb_id in aircrafts[ac_id].flightblocks:
            print( fb_id, aircrafts[ac_id].flightblocks[fb_id].fb_name )   


# --- Helper methods ---

def print_curl_header(host, port):
    print('#!/bin/bash')
    print('host=%s' % host)
    print('port=%s' % port)

def print_curl_format():
    #print('curl %s' % request.url)
    print('curl http://$host:$port%s' % request.path)

def print_ivy_trace(msg):
    print("Sending ivy message interface: %s" % msg)

import xml.etree.cElementTree as ET    
PPRZ_SRC_CONF = os.path.join(PPRZ_SRC, "conf")

def static_init_aircraft_data():
    tree = ET.parse(os.path.join( PPRZ_SRC_CONF, 'conf.xml' ))
    root = tree.getroot()

    # Populate aircraft objects
    for aircraft in root.findall('aircraft'):
        acid           = int(aircraft.get('ac_id'))
        name           = aircraft.get('name')
        flightplanpath = aircraft.get('flight_plan')
        #airframepath   = aircraft.get('airframe')
        #color          = aircraft.get('gui_color')
        add_new_aircraft(acid, name)
        aircraft = aircrafts[acid]
    
        # Populate flightblock objects
        fptree = ET.parse(os.path.join( PPRZ_SRC_CONF, flightplanpath )) 
        fproot = fptree.getroot()
        for idx, block in enumerate(fproot.iter('block')):
            name = block.get('name')
            add_new_flightblock(aircraft, idx, name)


def callback_aircraft_messages(ac_id, msg):
    # Possibly add the aircraft to the list
    if ac_id not in aircrafts:
        add_new_aircraft(ac_id, 'unknown')
    aircraft = aircrafts[ac_id]
    # Add the messages and say when last seen
    add_new_message(aircraft, msg.msg_class, msg.name,msg)
    aircrafts[ac_id].messages[msg.name].last_seen = time.time()
    for index in range(0, len(msg.fieldvalues)):
        aircraft.messages[msg.name].field_controls[index]=msg.get_field(index)


# --- Routes/Paths ----

@app.route('/')
def index():
    retval = ''

    if verbose: 
        retval = 'Index Page\n'
    if curl: print_curl_format()
    return retval


@app.route('/aircraft/')
def aircraft_all():
    aclist = []
    for ac_id in aircrafts:
        aclist.append(ac_id)
    if curl: print_curl_format()
    return str(aclist)


@app.route('/aircraft/<int:ac_id>')
def aircraft(ac_id):
    ac_id = int(ac_id)
    if ac_id in aircrafts:
        alist = []
        alist.append(ac_id)
        alist.append(aircrafts[ac_id].name)
        for fb_id in aircrafts[ac_id].flightblocks:
            alist.append(fb_id)   
            alist.append(aircrafts[ac_id].flightblocks[fb_id].fb_name)   
        if curl: print_curl_format()
        return str(alist)    
    return "unknown id"    


@app.route('/message/<int:ac_id>')
def message(ac_id):
    ac_id = int(ac_id)
    if ac_id in aircrafts:
        messagelist = []
        for key in aircrafts[ac_id].messages:
            messagelist.append(key)
        if curl: print_curl_format()
        return str(json.dumps(messagelist))
    return "unknown id"    


@app.route('/message/<int:ac_id>/<messagename>')
def message_byname(ac_id, messagename):
    # If the message is valid, return the latest message
    ac_id = int(ac_id)
    if ac_id in aircrafts:
        if messagename in aircrafts[ac_id].messages:
            if curl: print_curl_format()
            return Response(str(aircrafts[ac_id].messages[messagename].latest_msg.to_json()))
        else:
            return "unknown message"
    else:
        return "unknown id"


@app.route('/guidance/')
def guidance_all():
    retval = ''

    if verbose: 
        retval = 'Guidance: All\n'
    if curl: print_curl_format()
    return retval


#Set auto2 mode to GUIDED(value=19) or NAV(value=13).
@app.route('/guidance/setmode/<int:ac_id>/<int:value>')
def guidance_setmode(ac_id, value):
    retval = ''

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
        if verbose: 
            print_ivy_trace(msg)
            retval = 'Guidance mode: ac_id=%d, index=%d, value=%d\n' % (ac_id, index, value)
        ivy_interface.send(msg)
        if curl: print_curl_format()
        return retval


@app.route('/guidance/<int:ac_id>/<int:flag>/<x>/<y>/<z>/<yaw>')
def guidance(ac_id, flag, x, y, z, yaw):
    retval = ''

    msg = PprzMessage("datalink", "GUIDED_SETPOINT_NED")
    msg['ac_id'] = ac_id
    msg['flags'] = flag
    msg['x']     = x
    msg['y']     = y
    msg['z']     = z
    msg['yaw']   = yaw
    if verbose: 
        print_ivy_trace(msg)
        retval = 'Guidance: ac_id=%d, flag=%d, x=%s, y=%s, z=%s, yaw=%s\n' % (ac_id, flag, x, y, z, yaw)
    ivy_interface.send_raw_datalink(msg)
    if curl: print_curl_format()
    return retval


@app.route('/waypoint/')
def waypoint_all():
    retval = ''

    if verbose: 
        retval = 'Waypoint: All\n'
    if curl: print_curl_format()
    return retval


@app.route('/waypoint/<int:ac_id>/<int:wp_id>/<lat>/<lon>/<alt>')
def waypoint(ac_id, wp_id, lat, lon, alt):
    retval = ''

    msg = PprzMessage("ground", "MOVE_WAYPOINT")
    msg['ac_id'] = ac_id
    msg['wp_id'] = wp_id
    msg['lat']   = lat
    msg['long']  = lon
    msg['alt']   = alt
    if verbose: 
        print_ivy_trace(msg)
        retval = 'Waypoint: ac_id=%d, wp_id=%d, lat=%s, lon=%s, alt=%s\n' % (ac_id, wp_id, lat, lon, alt)
    ivy_interface.send(msg)
    if curl: print_curl_format()
    return retval


@app.route('/flightblock/<int:fb_id>')
def flightblock_all():
    retval = ''

    # TBD : Need to query the server for all aircraft id prior to calling this route
    if verbose: 
        retval = 'Flightblock: All Aircraft\n'
    if curl: print_curl_format()
    return retval


@app.route('/flightblock/<int:ac_id>/<int:fb_id>')
def flightblock(ac_id, fb_id):
    retval = ''

    msg = PprzMessage("ground", "JUMP_TO_BLOCK")
    msg['ac_id']    = ac_id
    msg['block_id'] = fb_id
    if verbose: 
        print_ivy_trace(msg)
        retval = 'Flightblock: ac_id=%d, fb_id=%d\n' % (ac_id, fb_id)
    ivy_interface.send(msg)
    if curl: print_curl_format()
    return retval


@app.route('/about')
def about():
    return 'About: Flying Robot Commander Server v%s\n' % (frc_version)


# --- Main body ----
if __name__ == '__main__':

    # Get/set the required IP address and port number along with other command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", type=str, default="127.0.0.1",
                        help="ip address")
    parser.add_argument("-p","--port", type=int, default=5000,
                        help="port number")
    parser.add_argument("-c","--curl",      action="store_true", help="dump actions as curl commands")
    parser.add_argument("-s","--subscribe", action="store_true", help="subscribe to the ivy bus")
    parser.add_argument("-v","--verbose",   action="store_true", help="verbose mode")

    try:
        # --- Startup state initialization block
        args = parser.parse_args()
        static_init_aircraft_data()
        if args.verbose: 
            print_aircraft_data()
        if args.subscribe: 
            ivy_interface.subscribe(callback_aircraft_messages)
        ivy_interface.start()

        # Handle misc. command line arguments
        if args.verbose: 
            verbose=args.verbose
        if args.curl: 
            curl=args.curl
            print_curl_header(args.ip, args.port)

        # --- Main loop
        # Supply flask the appropriate ip address and port for the server
        app.run(host=args.ip,port=args.port)

        # --- Shutdown state block
        ivy_interface.shutdown()

    except Exception as e:
        print(e)
        sys.exit(0)
