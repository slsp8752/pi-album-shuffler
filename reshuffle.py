#!/usr/bin/env python

from os import system, remove, path
from time import sleep


system("pkill -f radio_star.py")
system("killall omxplayer.bin")
if(path.exists("/home/pi/radio_star/albums.txt")):
  remove("/home/pi/radio_star/albums.txt")
if(path.exists("/home/pi/radio_star/songs.txt")):
  remove("/home/pi/radio_star/songs.txt")
if(path.exists("/home/pi/radio_star/now_playing.txt")):
  remove("/home/pi/radio_star/now_playing.txt")
system("/home/pi/radio_star/radio_star.py")
