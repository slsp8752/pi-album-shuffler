#!/usr/bin/env python

import buttonshim
import time

@buttonshim.on_press(buttonshim.BUTTON_A)
def button_a(button, pressed):
  print("A")
    
@buttonshim.on_press(buttonshim.BUTTON_B)
def button_b(button, pressed):
  print("B")

@buttonshim.on_press(buttonshim.BUTTON_C)
def button_c(button, pressed):
  print("C")

@buttonshim.on_press(buttonshim.BUTTON_D)
def button_d(button, pressed):
  print("D")

@buttonshim.on_press(buttonshim.BUTTON_E)
def button_e(button, pressed):    
  print("E")

while True:
  time.sleep(.1)
