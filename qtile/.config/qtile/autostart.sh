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

xset r rate 300 50 & setxkbmap -option caps:swapescape &
