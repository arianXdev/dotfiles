#!/bin/sh
lxsession --de="ARH" &
dbus-update-activation-environment --all &
gnome-keyring-daemon --start --components=secrets &
picom --daemon &
clipmenud &
sleep 1 &
nitrogen --restore & 
conky -c .conky-right & conky -c .conky-left & conky -c .conky-center &
sleep 1 &

if xrandr --listmonitors | grep "Monitors: 2"; then
	conky -c .conky-second-monitor &
fi

alacritty -T cmus -e cmus &
#alacritty -T "terminal-floating" -o "window.dimensions.columns=40" -o "window.dimensions.lines=14" -o "window.position.y=400" -e COMMAND &
