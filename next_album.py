#!/usr/bin/env python

from os import system, remove, path

system("pkill -f radio_star.py")
system("killall omxplayer.bin")
if(path.exists("/home/pi/radio_star/songs.txt")):
  remove("/home/pi/radio_star/songs.txt")
with open("/home/pi/radio_star/now_playing.txt", 'r') as np:
  for i, line in enumerate(np):
    if i == 0:
      album_index = int(line.rstrip())
print album_index
album_index += 1

with open("/home/pi/radio_star/now_playing.txt", 'w') as npw:
  npw.write(str(album_index)+"\n")
  npw.write("0\n")
  npw.write("0\n")
system("/home/pi/radio_star/radio_star.py")
