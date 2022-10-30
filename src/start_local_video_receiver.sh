set -vex
source config.sh

gst-launch-1.0 -v tcpclientsrc host=${RASPBERRY_IP} port=2032 ! gdpdepay ! rtph264depay ! avdec_h264 ! videoconvert ! autovideosink sync=false


#vlc -vvv --network-caching 200 rtsp://127.0.0.1:8554/

#vlc --network-caching 0 http://localhost:8099

# rtsp://127.0.0.1:8554/
#http://localhost:8099

#vlc --network-caching 0 udp://@:1234
