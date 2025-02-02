#!/bin/sh
picom --daemon &
sxhkd &
nitrogen --restore &

conky -c ~/GitHub/my-conky-config/.conky-center.lua & CONKY_CENTER_CONFIG=2 conky -c ~/GitHub/my-conky-config/.conky-center.lua & CONKY_CENTER_CONFIG=3 conky -c ~/GitHub/my-conky-config/.conky-center.lua &
conky -c ~/GitHub/my-conky-config/.conky-right.lua & conky -c ~/GitHub/my-conky-config/.conky-left.lua & CONKY_LEFT_CONFIG=2 conky -c ~/GitHub/my-conky-config/.conky-left.lua &

sleep 1 &

clipmenud &
tmux new -d -s default &

kdeconnectd &
