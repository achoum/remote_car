set -vex
source config.sh

python3 controller.py | nc -vu ${RASPBERRY_IP} 2020
