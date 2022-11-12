set -vex
source config.sh

time rsync -r ../../remote_car/src "${RASPBERRY_USER}@${RASPBERRY_IP}:${REMOTE_LOCATION}/remote_car"
