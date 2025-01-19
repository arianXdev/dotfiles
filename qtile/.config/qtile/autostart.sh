#!/bin/sh
dbus-update-activation-environment --all &
picom --daemon &
sxhkd &
clipmenud &
sleep 1 &
nitrogen --restore & 
conky -c ~/GitHub/my-conky-config/.conky-center & CONKY_CENTER_CONFIG=2 conky -c ~/GitHub/my-conky-config/.conky-center &
conky -c ~/GitHub/my-conky-config/.conky-right & conky -c ~/GitHub/my-conky-config/.conky-left & CONKY_LEFT_CONFIG=2 conky -c ~/GitHub/my-conky-config/.conky-left &

tmux new -d -s default &

kdeconnectd &
