import RPi.GPIO as GPIO
import time
import os
import random

"""Global Variable definition section"""
PIRPin = 11
musicDir = /path/to/directory


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PIRPin, GPIO.IN)


def getPinState(pin):
    """Get status from PIR sensor"""
    detection = GPIO.input(pin)
    if detection==1:
        return true
    return false


def main():
    """Main setup"""
    setup()

    """Main loop"""
    while True:
        if getPinState(PIRPin):
            """Play entire song from USB"""
            print "Poopers detected"
        else:
            print "No poopers"
            # No music
            time.sleep(0.5)

if __name__ == "__main__":
    main()
