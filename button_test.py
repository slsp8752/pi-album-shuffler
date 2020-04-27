#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import signal
import RPi.GPIO as GPIO
from os import system
import subprocess

# The buttons on Pirate Audio are connected to pins 5, 6, 16 and 24
# Boards prior to 23 January 2020 used 5, 6, 16 and 20 
# try changing 24 to 20 if your Y button doesn't work.
BUTTONS = [5, 6, 16, 20]
# 5: A, 6: B, 16: X, 20: Y

# Set up RPi.GPIO with the "BCM" numbering scheme
GPIO.setmode(GPIO.BCM)

# Buttons connect to ground when pressed, so we should set them up
# with a "PULL UP", which weakly pulls the input signal to 3.3V.
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# "handle_button" will be called every time a button is pressed
# It receives one argument: the associated input pin.
def handle_button(pin):
    label = LABELS[BUTTONS.index(pin)]
    print("Button press detected on pin: {} label: {}".format(pin, label))

# Loop through out buttons and attach the "handle_button" function to each
# We're watching the "FALLING" edge (transition from 3.3V to Ground) and
# picking a generous bouncetime of 100ms to smooth out button presses.

def next_song(pin):
    #system("/home/pi/radio_star/next_song.py")
    subprocess.Popen(["/home/pi/radio_star/next_song.py"])

def next_album(pin):
    #system("/home/pi/radio_star/next_album.py")
    subprocess.Popen(["/home/pi/radio_star/next_album.py"])

def prev_song(pin):
    #system("/home/pi/radio_star/prev_song.py")
    subprocess.Popen(["/home/pi/radio_star/prev_song.py"])

def reshuffle(pin):
    #system("/home/pi/radio_star/reshuffle.py")
    subprocess.Popen(["/home/pi/radio_star/reshuffle.py"])


GPIO.add_event_detect(5, GPIO.FALLING, prev_song, bouncetime=200)
GPIO.add_event_detect(6, GPIO.FALLING, reshuffle, bouncetime=200)
GPIO.add_event_detect(16, GPIO.FALLING, next_song, bouncetime=200)
GPIO.add_event_detect(20, GPIO.FALLING, next_album, bouncetime=200)

# Finally, since button handlers don't require a "while True" loop,
# we pause the script to prevent it exiting immediately.
signal.pause()
