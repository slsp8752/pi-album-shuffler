#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import time
from os import system

string = "This is a sentence that should scroll."
spaced = "  " + string + "  "

while(True):
    system("clear")
    print(spaced)
    spaced = spaced[1:] + spaced[0]
    time.sleep(0.1)
    
