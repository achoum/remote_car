set -vex

# Configuration
RASPBERRY_IP="192.168.0.234"
REMOTE_LOCATION="~/"
RASPBERRY_USER="pi"
REMOTE_EXEC="ssh -t ${RASPBERRY_USER}@${RASPBERRY_IP}"
PYTHON=python3.9

# Copy runner.
time scp -r ../../remote_car/src "${RASPBERRY_USER}@${RASPBERRY_IP}:${REMOTE_LOCATION}"

# Run runner remotely
CMD="true"
CMD="${CMD} && . ~/.bashrc"
#CMD="${CMD} && ${PYTHON} -m pip install -r requirements.txt"
CMD="${CMD} && cd ${REMOTE_LOCATION}/remote_car/src"
#CMD="${CMD} && ${PYTHON} remote_car.py"
CMD="${CMD} && nc -ulkv localhost 2002 | ${PYTHON} runner.py"
#CMD="${CMD} && systemctl restart plants.service"
${REMOTE_EXEC} "${CMD}"

# Run controller locally
