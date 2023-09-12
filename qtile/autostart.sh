#!/bin/sh
lxsession --de="ARH" &
picom &
alacritty -T cmus -e cmus &
conky -c .conky-right & conky -c .conky-left & sleep 2s & nitrogen --restore & 
clipmenud &
