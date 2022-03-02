import RPi.GPIO as GPIO
import time
import os
import random
import subprocess
import vlc

"""Global Variable definition section"""
PIRPin = 11
flashName = "skitrock"


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

def getFlashPath(driverName):
    """Find flash with specific name in /proc/mounts"""
    path = subprocess.check_output("cat /proc/mounts | grep '"+driverName+"' | awk '{print $2}'", shell=True)
    path = path.decode('utf-8') # convert bytes in string
    return path


def main():
    playing = set([1,2,3,4])
    """Main setup"""
    setup()
    while True:
        path = getFlashPath(flashName)
        if os.path.isdir(path):
            break
        time.sleep(0.5)

    """Main loop"""
    while True:
        if getPinState(PIRPin):
            """Play entire song from USB"""
            print "Poopers detected"
            if not os.path.isdir(path):
                print "Path not found. Flash disconnected?"
                break
            file = random.choice(os.listdir(path))
            media = vlc.MediaPlayer(file)
            media.play()
            while True:
                time.sleep(0.5)
                state = media.get_state()
                if state not in playing:
                    break
        else:
            print "No poopers"
            # No music
            time.sleep(0.5)

if __name__ == "__main__":
    main()
