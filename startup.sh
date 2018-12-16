#!/usr/bin/env bash

TELEGRAM_BOT_TOKEN=?
PROJ_PATH=?

while [[ "$(cat /sys/class/net/wlan0/operstate)" != "up" ]]; do
  echo 'waiting for network'
  sleep 5
done

export TELEGRAM_BOT_TOKEN

npm start --prefix $PROJ_PATH
