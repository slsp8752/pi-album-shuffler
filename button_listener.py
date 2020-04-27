#!/usr/bin/env python
import RPi.GPIO as GPIO
from os import system
import subprocess

GPIO.setmode(GPIO.BCM)

GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

bangerState = 0

with open("/home/pi/radio_star/banger_state.txt", "w+") as banger_file:
  banger_file.write("0")
  

def button_callback(channel):
  print "GOT button press"
  with open("/home/pi/radio_star/banger_state.txt", "r") as banger_file:
    bangerState = int(banger_file.readline().strip())
  if(bangerState == 0):
    # play a banger
    system("/home/pi/radio_star/play_a_banger.py &") 
    with open("/home/pi/radio_star/banger_state.txt", "w+") as banger_file:
      banger_file.write("1")
  elif(bangerState == 1):
    system("killall omxplayer.bin")

GPIO.add_event_detect(13, GPIO.FALLING, callback=button_callback, bouncetime=1000)

while True:
  pass
GPIO.cleanup()
