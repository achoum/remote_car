start "video" gst-launch-1.0 -v tcpclientsrc host=192.168.0.234 port=2032 ! gdpdepay ! rtph264depay ! avdec_h264 ! videoconvert ! autovideosink sync=false

python controller.py | "C:\Program Files (x86)\Nmap\ncat" -vu 192.168.0.234 2020
