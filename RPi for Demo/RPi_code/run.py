import RPi.GPIO as GPIO
import time
import XboxController
import sys
import math
import os
import numpy as np
import serial


class NURCbot:

    def __init__(self):

        #setup gpio ### DO WE NEED THIS? -> WALL MOTOR AND SERVO?? BETTER TO BE BOTH SERVOS?
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(12,GPIO.OUT)

        self.data_status = False

        self.data = list()
        self.collecting = False

        self.ser = serial.Serial()
        self.ser.baudrate = 115200
        self.ser.port = 'COM9'

        #setup controller values
        self.state = 0

        #create xbox controller class ### ENSURE THAT THESE INITIAL VALUES ARE CORRECT
        self.xboxCont = XboxController.XboxController(
            joystickNo = 0,
            deadzone = 0.1,
            scale = 1,
            invertYAxis = False)

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

    #call back funtions for left thumb stick

    ### DEFINE THREE CALLBACKS: DRIVING, WALL, HOPPER
    def WallCallBack(self,value):
   #     self.data_status = not self.data_status
        self.ser.write('W')

    def HopperCallBack(self,value):
        self.ser.write('H')

    def DriveCallBack(self,value):
        self.ser.write('D')
   #
   #  def LthumbY(self,value):
   #      self.motor1.setVelocity(value)
   #  #   if self.data_status:
   #      self.file.write(str(time.time()) + ", " + "left, " + str(value)  + "\n")
   #
   #  def RthumbY(self,value):
   #      self.motor2.setVelocity(value)
   #  #   if self.data_status:
   #      self.file.write(str(time.time()) + ", " + "right, " + str(value) + "\n")

    def stop(self):
        #GPIO.cleanup()
        self.xboxCont.stop()
        self.ser.close()
        self.running = False




if __name__ == '__main__':
    print ("started")
    try:
        #create class
        bot = NURCBot()
        while bot.running:
            time.sleep(1)

        GPIO.cleanup()

    #Ctrl C
    except KeyboardInterrupt:
        bot.xboxCont.stop()
        bot.ser.close()
        GPIO.cleanup()
        print "User cancelled"

    #Error
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
