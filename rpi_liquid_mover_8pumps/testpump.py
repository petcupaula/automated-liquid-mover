#!/usr/bin/python

import sys
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
pinList = [2, 3, 4, 17, 27, 22, 10, 9]
cmds = ['test', 'identify']

def setup():
    # Set mode and state to 'low'
    for i in pinList:
        GPIO.setup(i, GPIO.OUT, initial=GPIO.HIGH)
    return

def pour(pin, pourTime):
    GPIO.output(pin, GPIO.LOW)
    time.sleep(pourTime)
    GPIO.output(pin, GPIO.HIGH) 

def pour2(pin1, pin2, pourTime):
    GPIO.output(pin1, GPIO.LOW)
    GPIO.output(pin2, GPIO.LOW)
    time.sleep(pourTime)
    GPIO.output(pin1, GPIO.HIGH) 
    GPIO.output(pin2, GPIO.HIGH)

def test(pin):
    # Test params
    ml = 100
    flowRate = 60.0/100.0
    pourTime = ml*flowRate
    # Pour liquid
    print("Pouring liquid")
    pour(pin, pourTime)
    print("Finished pouring liquid")

def identify(pin):
    pour(pin, 5)

def printUsageInfo(reason):
    print(reason)
    print("Usage: python testpump.py cmd pin")
    print("Example: python testmpump.py identify 2")
    print("Available cmds:", ", ".join(cmds))
    print("Available pins:", str(pinList))

if __name__ == "__main__":
    if len(sys.argv) == 3:
        cmd = sys.argv[1]
        pin = int(sys.argv[2])
        if cmd in cmds and pin in pinList:
            setup()
            if cmd == "identify":
                identify(pin)
            elif cmd == "test":
                test(pin)
            GPIO.cleanup()
        else:
            printUsageInfo("Unknown cmd or pin")
    else:
        printUsageInfo("Number of args mismatch")

    #setup()   
    #pour2(27,17,5)
    #GPIO.cleanup()