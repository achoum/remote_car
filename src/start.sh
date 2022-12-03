#!/bin/bash

set -vex
source config.sh

trap 'killall' INT

killall() {
    trap '' INT TERM     # ignore INT and TERM while shutting down
    echo "**** Shutting down... ****"     # added double quotes
    kill -TERM 0         # fixed order, send TERM not INT
    wait
    echo DONE
}

# Copy runner source code on pi
time rsync -r ../../remote_car/src "${RASPBERRY_USER}@${RASPBERRY_IP}:${REMOTE_LOCATION}/remote_car"

# Start video emiter
# -b 200000 => poor quality, good refresh
CMD="raspivid -b 200000 -vf -hf -t 0 -fps 30 -w 1024 -h 768 --flush -o - | gst-launch-1.0 fdsrc ! h264parse ! rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host=192.168.0.234 port=2032"
${REMOTE_EXEC} "${CMD}" &

# Run runner remotely
CMD=". ~/.bashrc && cd ${REMOTE_LOCATION}/remote_car/src && nc -lkuv 2020 | ${PYTHON} runner.py"
${REMOTE_EXEC} "${CMD}" &

# Wait for the runner & video emiter to start
sleep 10

# Start controler
python3 controller.py | nc -vu ${RASPBERRY_IP} 2020 &

# Start video receiver
gst-launch-1.0 -v tcpclientsrc host=${RASPBERRY_IP} port=2032 ! gdpdepay ! rtph264depay ! avdec_h264 ! videoconvert ! autovideosink sync=false &

# Wait for the controller to start
sleep 2

echo "========================"
echo "You can control the car!"
echo "========================"

cat # wait forever
