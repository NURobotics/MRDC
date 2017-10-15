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
        print("initializing...")
        time.sleep(1)
        self.data_status = False

        self.data = list()
        self.collecting = False

        self.ser = serial.Serial()
        self.ser.baudrate = 9600
        self.ser.port = '/dev/ttyUSB0'

	# wrapper index for drive callback
	self.ind = 0

        #setup controller values
        self.state = 0

        #create xbox controller class ### ENSURE THAT THESE INITIAL VALUES ARE CORRECT
        self.xboxCont = XboxController.XboxController(
            deadzone = 50,
            scale = 255,
            invertYAxis = True)

        #setup call backs ### NEED CALLBACKS FOR DRIVING, WALL, AND HOPPER: send state value over serial port and do motor control math
        self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.A, self.WallCallBack) # wall servo
        self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.RTRIGGER, self.HopperCallBack) # hopper window motor
        self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.LTRIGGER, self.HopperCallBack)
        self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.LTHUMBY, self.DriveCallBack)
        self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.LTHUMBX, self.DriveCallBack)
        self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.RTHUMBX, self.DriveCallBack)

        #start the controller
        self.xboxCont.start()

        self.running = True

        self.ser.open()
        print('Serial port is open')
       # print(self.ser.readline())

    def WallCallBack(self,value):
        if (self.xboxCont.A == 1):
            msg = '<W,0,0,0,0>'
            print(msg)
            self.ser.write(msg)
            self.ser.flush()
            #print(self.ser.readline())
            #print(self.ser.readline())

    def HopperCallBack(self,value):
        # figure out hopper speed (positive down?)
        ltrig = self.xboxCont.LTRIGGER
        rtrig = self.xboxCont.RTRIGGER
        spd =  rtrig-ltrig 
        if (abs(spd)<20): spd = 0
        msg = '<H,{},0,0,0>'.format(int(spd))  #rtrig-ltrig)
        print(msg)
	self.ser.write(msg)
	self.ser.flush()
        
        # print(self.ser.readline())
        # print(self.ser.readline())
        # print(self.ser.readline())

    def DriveCallBack(self,value):
	self.ind += 1

        rot = self.xboxCont.RTHUMBX
        strafe = self.xboxCont.LTHUMBX
        drive = self.xboxCont.LTHUMBY

        motor1 = -drive + strafe - rot
        if (motor1>100): motor1 = 100
        if (motor1<-100): motor1 = -100
        if (abs(motor1)<70): motor1 = 0
        motor2 = -drive - strafe + rot
        if (motor2>100): motor2 = 100
        if (motor2<-100): motor2 = -100
        if (abs(motor2)<70): motor2 = 0
        motor3 = -drive - strafe - rot
        if (motor3>100): motor3 = 100
        if (motor3<-100): motor3 = -100
        if (abs(motor3)<70): motor3 = 0
        motor4 = -drive + strafe + rot
        if (motor4>100): motor4 = 100
        if (motor4<-100): motor4 = -100
        if (abs(motor4)<70): motor4 = 0

        msg = '<D,{},{},{},{}>'.format(int(motor1), int(motor2), int(motor3), int(motor4))
   
        if ((self.ind == 2)): # or (msg == '<D,0,0,0,0>')):
	    self.ind = 0
            print(msg)
	    self.ser.write(msg)
	    self.ser.flush()
        
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
    time.sleep(2)
    while True:
        try:
            print("Trying to connect...")
            time.sleep(1)
	    #create class
            bot = NURCbot()
            while bot.running:
                True

            # GPIO.cleanup()

        #Ctrl C
        except KeyboardInterrupt:
            bot.xboxCont.stop()
            # GPIO.cleanup()
            print("User cancelled")
            raise

        # Joystick not connected
        except:
            print("Joystick not connected")
            raise
            

        #Error
        #except:
            #bot.xboxCont.stop()
            #print("Unexpected error:", sys.exc_info()[0])
            #raise
