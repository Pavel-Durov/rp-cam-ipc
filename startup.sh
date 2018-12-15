#!/usr/bin/env bash

PROJ_PATH=/home/pi/projects/git-repos/rp-cam-ipc

while [[ "$(cat /sys/class/net/wlan0/operstate)" != "up" ]]; do
  echo 'waiting for network'
  sleep 5
done

npm start --prefix $PROJ_PATH

