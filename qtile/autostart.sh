#!/bin/sh
lxsession --de="ARH" &
picom --daemon &
alacritty -T cmus -e cmus &
conky -c .conky-right & conky -c .conky-left & conky -c .conky-second-monitor & sleep 1s &
nitrogen --restore & 
clipmenud &
dunst &



#alacritty -T "terminal-floating" -o "window.dimensions.columns=40" -o "window.dimensions.lines=14" -o "window.position.y=400" -e COMMAND &
