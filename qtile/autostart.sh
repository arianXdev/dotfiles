#!/bin/sh
lxsession --de="ARH" -a &
dbus-update-activation-environment --all &
gnome-keyring-daemon --start --components=secrets &
picom --daemon &
clipmenud &
sleep 1 &
nitrogen --restore & 
conky -c ~/GitHub/my-conky-config/.conky-center & CONKY_CENTER_CONFIG=2 conky -c ~/GitHub/my-conky-config/.conky-center &
conky -c ~/GitHub/my-conky-config/.conky-right & conky -c ~/GitHub/my-conky-config/.conky-left &

if xrandr --listmonitors | grep "Monitors: 2"; then
	xrandr --output VGA-0 --primary --right-of LVDS &
	conky -c ~/GitHub/my-conky-config/.conky-right & conky -c ~/GitHub/my-conky-config/.conky-left &
fi


#alacritty -T cmus -e cmus &
#alacritty -T "terminal-floating" -o "window.dimensions.columns=40" -o "window.dimensions.lines=14" -o "window.position.y=400" -e COMMAND &
