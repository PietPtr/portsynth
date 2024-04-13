#!/bin/bash
set -e
set -o xtrace

if [ -z "$1" ]; then
  echo "Error: must provide deploy target, e.g. pi@raspberry" >&2
  exit 1
fi

REMOTE_HOST="$1"
scp fluidsynth.service midi-connector.service midi-connector.py "${REMOTE_HOST}:/tmp/"

# Execute commands on remote host
ssh "${REMOTE_HOST}" << 'EOF'
set -x
sudo cp /tmp/fluidsynth.service /etc/systemd/system/fluidsynth.service
sudo cp /tmp/midi-connector.service /etc/systemd/system/midi-connector.service
chmod +x /tmp/midi-connector.py
sudo cp /tmp/midi-connector.py /usr/local/bin/
sudo systemctl daemon-reload
sudo systemctl enable fluidsynth
sudo systemctl enable midi-connector
sudo systemctl restart fluidsynth
sudo systemctl restart midi-connector
echo "Restarted services, sleeping..."
sleep 5
sudo systemctl status fluidsynth
sudo systemctl status midi-connector
EOF
