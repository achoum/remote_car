set -vex

python3 controller.py | nc -v -u localhost 2002