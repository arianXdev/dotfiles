#!/bin/sh
lxsession --de="ARH" &
picom --daemon &
alacritty -T cmus -e cmus &
conky -c .conky-right & conky -c .conky-left &

if xrandr --listmonitors | grep "Monitors: 2"; then
	conky -c .conky-second-monitor &
fi

sleep 1s &
nitrogen --restore & 
dbus-update-activation-environment --all &
clipmenud &
dunst &
gnome-keyring-daemon --start --components=secrets &

#alacritty -T "terminal-floating" -o "window.dimensions.columns=40" -o "window.dimensions.lines=14" -o "window.position.y=400" -e COMMAND &
