set -vex

nc -ulkv localhost 2002 | python3 runner.py | nc -v -l -k localhost 2003
