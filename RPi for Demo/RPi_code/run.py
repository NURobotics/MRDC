# import RPi.GPIO as GPIO
import time
import XboxController
import sys
import math
import os
import numpy as np
import serial
import string


class NURCbot:

    def __init__(self):

        #setup gpio ### DO WE NEED THIS? -> WALL MOTOR AND SERVO?? BETTER TO BE BOTH SERVOS?
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setwarnings(False)
        # GPIO.setup(12,GPIO.OUT)

        self.data_status = False

        self.data = list()
        self.collecting = False

        self.ser = serial.Serial()
        self.ser.baudrate = 115200
        self.ser.port = 'COM4'

        #setup controller values
        self.state = 0

        #create xbox controller class ### ENSURE THAT THESE INITIAL VALUES ARE CORRECT
        self.xboxCont = XboxController.XboxController(
            deadzone = 30,
            scale = 100,
            invertYAxis = True)

        #setup call backs ### NEED CALLBACKS FOR DRIVING, WALL, AND HOPPER: send state value over serial port and do motor control math
        self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.A, self.WallCallBack) # wall servo
        self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.RTRIGGER, self.HopperCallBack) # hopper window motor
        self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.LTRIGGER, self.HopperCallBack)
        self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.LTHUMBY, self.DriveCallBack)
        self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.LTHUMBX, self.DriveCallBack)
        self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.RTHUMBY, self.DriveCallBack)
        self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.RTHUMBX, self.DriveCallBack)

        #start the controller
        self.xboxCont.start()

        self.running = True

        self.ser.open()

    def WallCallBack(self,value):
        msg = 'W'
        self.ser.write(str.encode(msg))

    def HopperCallBack(self,value):
        # figure out hopper speed (positive down?)
        msg = 'H,{}'.format(value)
        self.ser.write(str.encode(msg))

    def DriveCallBack(self,value):
        # figure out motor speeds
        msg = 'D,{},{},{},{}'.format(100,100,100,100)
        self.ser.write(str.encode(msg))

    def stop(self):
        #GPIO.cleanup()
        self.xboxCont.stop()
        self.ser.close()
        self.running = False




if __name__ == '__main__':
    print ("started")
    try:
        #create class
        bot = NURCbot()
        while bot.running:
            time.sleep(1)

        # GPIO.cleanup()

    #Ctrl C
    except KeyboardInterrupt:
        bot.xboxCont.stop()
        bot.ser.close()
        # GPIO.cleanup()
        print("User cancelled")

    #Error
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
