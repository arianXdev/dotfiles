#!/bin/sh
# /usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
dbus-update-activation-environment --all &
# gnome-keyring-daemon --start --components=secrets &
picom --daemon &
sxhkd &
clipmenud &
sleep 1 &
nitrogen --restore & 
conky -c ~/GitHub/my-conky-config/.conky-center & CONKY_CENTER_CONFIG=2 conky -c ~/GitHub/my-conky-config/.conky-center &
conky -c ~/GitHub/my-conky-config/.conky-right & conky -c ~/GitHub/my-conky-config/.conky-left & CONKY_LEFT_CONFIG=2 conky -c ~/GitHub/my-conky-config/.conky-left &
sleep 2 &

#windscribe &

#alacritty -T cmus -e cmus &
#alacritty -T "terminal-floating" -o "window.dimensions.columns=40" -o "window.dimensions.lines=14" -o "window.position.y=400" -e COMMAND &
