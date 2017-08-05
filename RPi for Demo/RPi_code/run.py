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
            deadzone = 5,
            scale = 255,
            invertYAxis = True)

        #setup call backs ### NEED CALLBACKS FOR DRIVING, WALL, AND HOPPER: send state value over serial port and do motor control math
        self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.A, self.WallCallBack) # wall servo
        self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.RTRIGGER, self.DriveCallBack) # hopper window motor
        self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.LTRIGGER, self.DriveCallBack)
        self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.LTHUMBY, self.DriveCallBack)
        self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.LTHUMBX, self.DriveCallBack)
        self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.RTHUMBX, self.HopperCallBack)

        #start the controller
        self.xboxCont.start()

        self.running = True

        self.ser.open()
        print(self.ser.readline())

    def WallCallBack(self,value):
        if (self.xboxCont.A == 1):
            msg = 'W'
            print(msg)
            self.ser.write(str.encode(msg))
            # print(self.ser.readline())
            # print(self.ser.readline())

    def HopperCallBack(self,value):
        # figure out hopper speed (positive down?)
        # ltrig = self.xboxCont.LTRIGGER
        # rtrig = self.xboxCont.RTRIGGER
        spd = self.xboxCont.RTHUMBX
        if (abs(spd)<20): spd = 0
        msg = 'H,{}'.format(spd)  #rtrig-ltrig)
        print(msg)
        self.ser.write(str.encode(msg))
        # print(self.ser.readline())
        # print(self.ser.readline())
        # print(self.ser.readline())

    def DriveCallBack(self,value):
        rot = self.xboxCont.RTRIGGER - self.xboxCont.LTRIGGER #self.xboxCont.RTHUMBX
        strafe = self.xboxCont.LTHUMBX
        drive = self.xboxCont.LTHUMBY

        motor1 = -drive + strafe - rot
        if (motor1>255): motor1 = 255
        if (motor1<-255): motor1 = -255
        if (abs(motor1)<30): motor1 = 0
        motor2 = -drive - strafe + rot
        if (motor2>255): motor2 = 255
        if (motor2<-255): motor2 = -255
        if (abs(motor2)<30): motor1 = 0
        motor3 = -drive - strafe - rot
        if (motor3>255): motor3 = 255
        if (motor3<-255): motor3 = -255
        if (abs(motor3)<30): motor1 = 0
        motor4 = -drive + strafe + rot
        if (motor4>255): motor4 = 255
        if (motor4<-255): motor4 = -255
        if (abs(motor4)<30): motor1 = 0

        msg = 'D,{},{},{},{}'.format(motor1, motor2, motor3, motor4)
        print(msg)
        self.ser.write(str.encode(msg))
        # print(self.ser.readline())
        # print(self.ser.readline())
        # print(self.ser.readline())
        # print(self.ser.readline())
        # print(self.ser.readline())
        # print(self.ser.readline())

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
            pass

        # GPIO.cleanup()

    #Ctrl C
    except KeyboardInterrupt:
        bot.xboxCont.stop()
        # GPIO.cleanup()
        print("User cancelled")

    #Error
    except:
        bot.xboxCont.stop()
        print("Unexpected error:", sys.exc_info()[0])
        raise
