#!/bin/bash
set -e
set -o xtrace

if [ -z "$1" ]; then
  echo "Error: must provide deploy target, e.g. pi@raspberry" >&2
  exit 1
fi

REMOTE_HOST="$1"
cargo build --release --target=armv7-unknown-linux-gnueabihf

# Copy portsynth binary to remote host
scp target/armv7-unknown-linux-gnueabihf/release/portsynth "${REMOTE_HOST}:/tmp/portsynth"
# Copy portsynth service file to remote host
scp infra/portsynth.service "${REMOTE_HOST}:/tmp/portsynth.service"

# Execute commands on remote host
ssh "${REMOTE_HOST}" << 'EOF'
sudo cp /tmp/portsynth /usr/local/bin/portsynth
sudo cp /tmp/portsynth.service /etc/systemd/system/portsynth.service
sudo systemctl enable portsynth
EOF
