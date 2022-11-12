set -vex
source config.sh

time rsync -r ../../remote_car/src "${RASPBERRY_USER}@${RASPBERRY_IP}:${REMOTE_LOCATION}/remote_car"

CMD="true"
CMD="${CMD} && . ~/.bashrc"
CMD="${CMD} && cd ${REMOTE_LOCATION}/remote_car/src"
CMD="${CMD} && ${PYTHON} test_io.py"
${REMOTE_EXEC} "${CMD}"
