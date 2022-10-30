set -vex
source config.sh

# Copy runner.
#time scp -r ../../remote_car/src "${RASPBERRY_USER}@${RASPBERRY_IP}:${REMOTE_LOCATION}/remote_car/src"
time rsync -r ../../remote_car/src "${RASPBERRY_USER}@${RASPBERRY_IP}:${REMOTE_LOCATION}/remote_car"

# Run runner remotely
CMD="true"
CMD="${CMD} && . ~/.bashrc"
#CMD="${CMD} && ${PYTHON} -m pip install -r requirements.txt"
CMD="${CMD} && cd ${REMOTE_LOCATION}/remote_car/src"
#CMD="${CMD} && ${PYTHON} remote_car.py"
CMD="${CMD} && nc -lkuv 2020 | ${PYTHON} runner.py"
#CMD="${CMD} && systemctl restart plants.service"
${REMOTE_EXEC} "${CMD}"

# Run controller locally
