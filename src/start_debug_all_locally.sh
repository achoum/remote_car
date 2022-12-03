set -vex
set -o pipefail

#../tools/EventViewer.sh $(pwd)/event_viewer.sce &
#python3 controller.py | python3 runner.py | nc -v -l -k localhost 2003

#python3 controller.py

python3 controller.py | python3 runner.py