#!/bin/bash

cargo build --release
cp target/release/portsynth /usr/local/bin/
cp infra/portsynth.service /etc/systemd/system/portsynth.service
systemctl enable portsynth