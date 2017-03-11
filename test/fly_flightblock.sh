#!/bin/bash

IP=127.0.0.1
PORT=5000
WAIT=15 

# Start all aircraft motors
curl http://$IP:$PORT/flightblock/217/3
curl http://$IP:$PORT/flightblock/218/3
curl http://$IP:$PORT/flightblock/219/3
curl http://$IP:$PORT/flightblock/216/3
curl http://$IP:$PORT/flightblock/215/3

sleep $WAIT

# Fly all aircraft to their standby positions
curl http://$IP:$PORT/flightblock/217/4
curl http://$IP:$PORT/flightblock/218/4
curl http://$IP:$PORT/flightblock/219/4
curl http://$IP:$PORT/flightblock/216/4
curl http://$IP:$PORT/flightblock/215/4

sleep $WAIT

# Fly all aircraft to their waypoint 4
curl http://$IP:$PORT/flightblock/217/9
curl http://$IP:$PORT/flightblock/218/9
curl http://$IP:$PORT/flightblock/219/9
curl http://$IP:$PORT/flightblock/216/9
curl http://$IP:$PORT/flightblock/215/9

sleep $WAIT

curl http://$IP:$PORT/flightblock/217/6

sleep $WAIT

curl http://$IP:$PORT/flightblock/217/8
curl http://$IP:$PORT/flightblock/218/6

sleep $WAIT

curl http://$IP:$PORT/flightblock/217/7
curl http://$IP:$PORT/flightblock/218/8
curl http://$IP:$PORT/flightblock/219/6

sleep $WAIT

curl http://$IP:$PORT/flightblock/217/12
curl http://$IP:$PORT/flightblock/218/7
curl http://$IP:$PORT/flightblock/219/8
curl http://$IP:$PORT/flightblock/216/6

sleep $WAIT

curl http://$IP:$PORT/flightblock/217/33
curl http://$IP:$PORT/flightblock/218/12
curl http://$IP:$PORT/flightblock/219/7
curl http://$IP:$PORT/flightblock/216/8
curl http://$IP:$PORT/flightblock/215/6

sleep $WAIT

curl http://$IP:$PORT/flightblock/218/33
curl http://$IP:$PORT/flightblock/219/12
curl http://$IP:$PORT/flightblock/216/7
curl http://$IP:$PORT/flightblock/215/8

sleep $WAIT

curl http://$IP:$PORT/flightblock/219/33
curl http://$IP:$PORT/flightblock/216/12
curl http://$IP:$PORT/flightblock/215/7

sleep $WAIT

curl http://$IP:$PORT/flightblock/216/33
curl http://$IP:$PORT/flightblock/215/12

sleep $WAIT

curl http://$IP:$PORT/flightblock/215/33

sleep $WAIT

# Stop all aircraft motors 
curl http://$IP:$PORT/flightblock/217/2
curl http://$IP:$PORT/flightblock/219/2
curl http://$IP:$PORT/flightblock/216/2
curl http://$IP:$PORT/flightblock/215/2
curl http://$IP:$PORT/flightblock/218/2

