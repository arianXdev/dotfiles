#!/bin/bash

DEVICE_MAC="13:FB:BC:6E:8F:12"

STATUS=$(bluetoothctl info "$DEVICE_MAC" | grep "Connected" | awk '{print $2}')
if [ "$STATUS" == "yes" ]; then
  NAME=$(bluetoothctl info "$DEVICE_MAC" | grep "Name" | awk '{$1=""; print $0}')
  echo "$NAME (Connected)"
else
  echo "Disconnected"
fi

