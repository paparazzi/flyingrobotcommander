#!/bin/bash

: '
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
'

IP_CMD_PREFIX=http://127.0.0.1:5000

curl $IP_CMD_PREFIX/
curl $IP_CMD_PREFIX/about
curl $IP_CMD_PREFIX/aircraft/
curl $IP_CMD_PREFIX/aircraft/client/
curl $IP_CMD_PREFIX/flightblock/client/
curl $IP_CMD_PREFIX/aircraft/client/add/215
curl $IP_CMD_PREFIX/aircraft/client/add/216
curl $IP_CMD_PREFIX/aircraft/client/add/217
curl $IP_CMD_PREFIX/aircraft/client/add/218
curl $IP_CMD_PREFIX/aircraft/client/add/219
curl $IP_CMD_PREFIX/flightblock/client/add/3
curl $IP_CMD_PREFIX/flightblock/client/add/4
curl $IP_CMD_PREFIX/flightblock/client/add/6
curl $IP_CMD_PREFIX/flightblock/client/add/7
curl $IP_CMD_PREFIX/flightblock/client/add/8
curl $IP_CMD_PREFIX/flightblock/client/add/9
curl $IP_CMD_PREFIX/flightblock/client/add/12
curl $IP_CMD_PREFIX/flightblock/client/add/32
curl $IP_CMD_PREFIX/flightblock/client/add/33
curl $IP_CMD_PREFIX/flightblock/client/add/2
curl $IP_CMD_PREFIX/aircraft/client/
curl $IP_CMD_PREFIX/flightblock/client/
curl $IP_CMD_PREFIX/waypoint/217/6/45.5643/-122.6219406/61.0
curl $IP_CMD_PREFIX/waypoint/218/6/45.5644/-122.6219406/61.0
curl $IP_CMD_PREFIX/guidance/setmode/217/19
curl $IP_CMD_PREFIX/guidance/217/0/10.0/5.0/-5.0/90.0
curl $IP_CMD_PREFIX/guidance/217/1/-5.0/-5.0/-2.0/45.0
curl $IP_CMD_PREFIX/guidance/217/3/0.0/5.0/2.0/0.0
curl $IP_CMD_PREFIX/guidance/3/0.0/5.0/2.0/0.0
curl $IP_CMD_PREFIX/guidance/setmode/217/13
curl $IP_CMD_PREFIX/flightblock/217/3
curl $IP_CMD_PREFIX/flightblock/218/3
curl $IP_CMD_PREFIX/flightblock/217/12
curl $IP_CMD_PREFIX/flightblock/218/12
curl $IP_CMD_PREFIX/flightblock/217/33
curl $IP_CMD_PREFIX/flightblock/218/33
curl $IP_CMD_PREFIX/flightblock/33

