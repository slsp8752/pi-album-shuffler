#!/usr/bin/env python

from os import system

system("/home/pi/radio_star/killer.py")

with open("/home/pi/radio_star/now_playing.txt", "r") as np_r:
  for i, line in enumerate(np_r):
    if i == 0:
      album_index = line.rstrip('\n')
    elif i == 1:
      song_index = int(line.rstrip('\n'))

with open("/home/pi/radio_star/now_playing.txt", "w+") as np_w:
  np_w.write(album_index + '\n')
  if song_index > 0:
    song_index = song_index - 1
  np_w.write(str(song_index) + '\n')
  np_w.write("0" + '\n')

system("/home/pi/radio_star/radio_star.py")
