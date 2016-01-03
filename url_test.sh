#!/bin/bash

IP_CMD_PREFIX=http://192.168.1.7:5000

curl $IP_CMD_PREFIX/waypoint/217/6/45.5643/-122.6219406/61.0
curl $IP_CMD_PREFIX/waypoint/218/6/45.5644/-122.6219406/61.0
curl $IP_CMD_PREFIX/guidance/217/0/10.0/5.0/-5.0/90.0
curl $IP_CMD_PREFIX/guidance/217/1/-5.0/-5.0/-2.0/45.0
curl $IP_CMD_PREFIX/guidance/217/3/0.0/5.0/2.0/0.0
curl $IP_CMD_PREFIX/flightblock/217/3
curl $IP_CMD_PREFIX/flightblock/218/3
curl $IP_CMD_PREFIX/flightblock/217/12
curl $IP_CMD_PREFIX/flightblock/218/12
curl $IP_CMD_PREFIX/flightblock/217/33
curl $IP_CMD_PREFIX/flightblock/218/33
