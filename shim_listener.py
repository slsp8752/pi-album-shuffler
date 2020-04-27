#!/usr/bin/env python

import buttonshim
import time
from os import system

@buttonshim.on_press(buttonshim.BUTTON_A)
def button_a(button, pressed):
  # shuffle albums
  system("/home/pi/radio_star/reshuffle.py")
    
@buttonshim.on_press(buttonshim.BUTTON_B)
def button_b(button, pressed):
  # previous song
  system("/home/pi/radio_star/prev_song.py")

@buttonshim.on_press(buttonshim.BUTTON_C)
def button_c(button, pressed):
  # play/pause
  # todo: implement... 
  pass

@buttonshim.on_press(buttonshim.BUTTON_D)
def button_d(button, pressed):
  # next song
  system("/home/pi/radio_star/next_song.py")

@buttonshim.on_press(buttonshim.BUTTON_E)
def button_e(button, pressed):    
  # next album
  system("/home/pi/radio_star/next_album.py")

while True:
  time.sleep(.1)
