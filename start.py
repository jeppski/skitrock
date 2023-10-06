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
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIRPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def getPinState(pin):
    """Get status from PIR sensor"""
    detection = GPIO.input(pin)
    print ("GPIO:",pin,"status",detection)
    if detection==1:
        return True
    return False

def getFlashPath(driverName):
    """Find flash with specific name in /proc/mounts"""
    path = subprocess.check_output("cat /proc/mounts | grep '"+driverName+"' | awk '{print $2}'", shell=True)
    path = path.decode('utf-8') # convert bytes in string
    return path


def main():
    playing = set([1,2,3,4])
    """Main setup"""
    setup()

    """Setup bluetooth"""
    while not subprocess.run(['bluetoothctl', 'connect', '6C:47:60:64:7D:2B']):
        print ("Connecting bluetooth")
        time.sleep(1)
    
    while True:
        print ("Looking for USB-drive")
        path = "/media/pi/skitrock" #getFlashPath(flashName)
        if os.path.isdir(path):
            break
        time.sleep(0.5)

    clock = vlc.MediaPlayer("clock.wav")

    """Main loop"""
    while True:
        if getPinState(PIRPin):
            """Play entire song from USB"""
            print ("Poopers detected")
            if not os.path.isdir(path):
                print ("Path not found. Flash disconnected?")
                break
            file = path+'/'+random.choice(os.listdir(path))
            if file is path+"/System Volume Information":
                break
            print ("Playing media: "+file)
            media = vlc.MediaPlayer(file)
            media.play()
            while True:
                time.sleep(1)
                state = media.get_state()
                if state not in playing:
                    media.release()
                    break
        else:
            print ("No poopers")
            clock.play()
            time.sleep(2)
            clock.stop()


if __name__ == "__main__":
    main()
