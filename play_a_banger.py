#!/usr/bin/env python

from os import system
from os import listdir
import random

system("pkill -f radio_star.py")
system("killall omxplayer.bin")

banger = random.choice(listdir("/home/pi/radio_star/bbbangers"))


system("omxplayer -o local /home/pi/radio_star/bbbangers/" + banger)
with open("/home/pi/radio_star/banger_state.txt", "w+") as banger_file:
  banger_file.write("0")
system("/home/pi/radio_star/radio_star.py")
