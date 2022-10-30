set -vex
set -o pipefail

# Configuration

RASPBERRY_IP="192.168.0.234"
REMOTE_LOCATION="~"
RASPBERRY_USER="pi"
REMOTE_EXEC="ssh -t ${RASPBERRY_USER}@${RASPBERRY_IP}"
PYTHON=python3.9
