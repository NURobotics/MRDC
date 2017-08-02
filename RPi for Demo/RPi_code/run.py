import RPi.GPIO as GPIO
import time
import XboxController
import sys
import math
import os
import numpy as np
import analog
import heading


class NURCbot:

    def __init__(self):

        #setup gpio ### DO WE NEED THIS? -> WALL MOTOR AND SERVO?? BETTER TO BE BOTH SERVOS?
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(12,GPIO.OUT)

        self.mcp = analog.Analog()

        self.sense = heading.Heading()

        self.data_status = False

        self.data = list()
        self.collecting = False

        #setup controller values
        self.state = 0

        #create xbox controller class ### ENSURE THAT THESE INITIAL VALUES ARE CORRECT
        self.xboxCont = XboxController.XboxController(
            joystickNo = 0,
            deadzone = 0.1,
            scale = 1,
            invertYAxis = False)

        #setup call backs ### NEED CALLBACKS FOR DRIVING, WALL, AND HOPPER: send state value over serial port and do motor control math
        self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.A, self.aButtonCallBack)
        self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.BACK, self.backButton)
        self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.LTHUMBY, self.LthumbY)
        self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.RTHUMBY, self.RthumbY)

        #start the controller
        self.xboxCont.start()

        self.running = True

        ### SETUP SERIAL PORT HERE

    #call back funtions for left thumb stick

    ### DEFINE THREE CALLBACKS: DRIVING, WALL, HOPPER
   #  def aButtonCallBack(self,value):
   # #     self.data_status = not self.data_status
   #      self.motor_collect()
   #
   #  def backButton(self, value):
   #      self.stop()
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
        self.running = False




if __name__ == '__main__':
    print ("started")
    try:
        #create class
        bot = NURCBot()
        while bot.running:
           ### MONITOR XBOX CONTROLLER IN INFINITE LOOP

        GPIO.cleanup()

    #Ctrl C
    except KeyboardInterrupt:
        bot.xboxCont.stop()
        GPIO.cleanup()
        print "User cancelled"

    #Error
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
