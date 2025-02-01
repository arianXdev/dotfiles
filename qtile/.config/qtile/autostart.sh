#!/bin/sh
picom --daemon &
sxhkd &
nitrogen --restore &

conky -c ~/GitHub/my-conky-config/.conky-center & CONKY_CENTER_CONFIG=2 conky -c ~/GitHub/my-conky-config/.conky-center & CONKY_CENTER_CONFIG=3 conky -c ~/GitHub/my-conky-config/.conky-center &
conky -c ~/GitHub/my-conky-config/.conky-right & conky -c ~/GitHub/my-conky-config/.conky-left & CONKY_LEFT_CONFIG=2 conky -c ~/GitHub/my-conky-config/.conky-left &

sleep 1 &

clipmenud &
tmux new -d -s default &

kdeconnectd
