#!/usr/bin/env python

from __future__ import print_function

import sys
from os import path, getenv

import os

from flask import Flask

# if PAPARAZZI_SRC not set, then assume the tree containing this
# file is a reasonable substitute
PPRZ_SRC = getenv("PAPARAZZI_SRC", path.normpath(path.join(path.dirname(path.abspath(__file__)), '../../../')))
sys.path.append(PPRZ_SRC + "/sw/lib/python")

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/guidance/')
def guidance_all():
    return 'Guidance: All'

@app.route('/guidance/<int:ac_id>/<int:flag>/<x>/<y>/<z>/<yaw>/<time>')
def guidance(ac_id, flag, x, y, z, yaw, time):
    os.system( "./guidance.py %d %d %s %s %s %s %s" % (ac_id, flag, x, y, z, yaw, time) )
    return 'Guidance: ac_id=%d, flag=%d, x=%s, y=%s, z=%s, yaw=%s, time=%s' % (ac_id, flag, x, y, z, yaw, time)

@app.route('/waypoint/')
def waypoint_all():
    return 'Waypoint: All'

@app.route('/waypoint/<int:ac_id>/<int:wp_id>/<lat>/<lon>/<alt>')
def waypoint(ac_id, wp_id, lat, lon, alt):
    os.system( "./waypoint.py %d %d %s %s %s" % (ac_id, wp_id, lat, lon, alt) )
    return 'Waypoint: ac_id=%d, wp_id=%d, lat=%s, lon=%s, alt=%s' % (ac_id, wp_id, lat, lon, alt)

@app.route('/flightblock/')
def flightblock_all():
    return 'Flightblock: All'

@app.route('/flightblock/<int:ac_id>/<int:fb_id>')
def flightblock(ac_id, fb_id):
    os.system( "./flightblock.py %d %d" % (ac_id, fb_id) )
    return 'Flightblock: ac_id=%d, fb_id=%d' % (ac_id, fb_id)


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/about')
def about():
    return 'The about page'

if __name__ == '__main__':
    app.run(host=sys.argv[1]) # supply the appropriate ip address for the server as the first command line argument