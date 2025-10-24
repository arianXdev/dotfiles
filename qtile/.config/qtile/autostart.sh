#!/bin/sh
dbus-update-activation-environment --all &
picom --daemon &
sxhkd &
nitrogen --restore &

conky -c ~/GitHub/my-conky-config/conky-center.lua & CONKY_CENTER_CONFIG=2 conky -c ~/GitHub/my-conky-config/conky-center.lua & CONKY_CENTER_CONFIG=3 conky -c ~/GitHub/my-conky-config/conky-center.lua &
conky -c ~/GitHub/my-conky-config/conky-right.lua & conky -c ~/GitHub/my-conky-config/conky-left.lua & CONKY_LEFT_CONFIG=2 conky -c ~/GitHub/my-conky-config/conky-left.lua &

sleep 1 &
clipmenud &

sleep 3 && xwinwrap -g 202x203+1630+730 -ov -ni -s -nf -b -un -argb -- gifview -w WID .conky-hud-1.gif -a &
# sleep 3 && xwinwrap -g 235x229+595+270 -ov -ni -s -nf -b -un -argb -- gifview -w WID .conky-hud-2.gif -a &
