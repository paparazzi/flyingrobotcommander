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

IP_CMD_PREFIX=http://192.168.1.7:5000

curl $IP_CMD_PREFIX/waypoint/217/6/45.5643/-122.6219406/61.0
curl $IP_CMD_PREFIX/waypoint/218/6/45.5644/-122.6219406/61.0
curl $IP_CMD_PREFIX/guidance/217/0/10.0/5.0/-5.0/90.0/10.0
curl $IP_CMD_PREFIX/guidance/217/1/-5.0/-5.0/-2.0/45.0/10.0
curl $IP_CMD_PREFIX/guidance/217/3/0.0/5.0/2.0/0.0/10.0
curl $IP_CMD_PREFIX/flightblock/217/3
curl $IP_CMD_PREFIX/flightblock/218/3
curl $IP_CMD_PREFIX/flightblock/217/12
curl $IP_CMD_PREFIX/flightblock/218/12
curl $IP_CMD_PREFIX/flightblock/217/33
curl $IP_CMD_PREFIX/flightblock/218/33
