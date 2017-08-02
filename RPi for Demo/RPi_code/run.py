import RPi.GPIO as GPIO
import time
import XboxController
import sys
import math
import motor
import sonic
import os
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
import numpy as np
import pickle
import analog
import heading


class VeggieBot:
    
    def __init__(self):        

        #setup gpio
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(12,GPIO.OUT)   
        
        self.mcp = analog.Analog()

        self.motor2 = motor.Motor(19,20)
        self.motor1 = motor.Motor(26,21)


        self.sonic1 = sonic.Sonic(18,23)
        self.sonic4 = sonic.Sonic(25,24)
        self.sonic2 = sonic.Sonic(16,12)
        self.sonic3 = sonic.Sonic(6,13)
        self.sonic5 = sonic.Sonic(22,5)

        self.sense = heading.Heading()


        self.data_status = False

        self.wpath = os.getcwd() + "/data/" + time.strftime("%H%M%S") + ".csv"
        self.file = open(self.wpath,"w")
        self.file.write("time, motor, pwm\n")

        with open('data/saved_net.pickle', 'rb') as handle:
            self.net = pickle.load(handle)


#   self.sensor_collect = open("data/sensors.txt","w")
#   self.sensor_collect.write("time, sonic1, sonic2, sonic3, sonic4, sonic5\n")

        self.data = list()
        self.collecting = False
        
        #setup controller values
        self.state = 0

        #create xbox controller class
        self.xboxCont = XboxController.XboxController(
            joystickNo = 0,
            deadzone = 0.1,
            scale = 1,
            invertYAxis = False)

        #setup call backs
        self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.A, self.aButtonCallBack)
        self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.BACK, self.backButton)
        self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.LTHUMBY, self.LthumbY)
        self.xboxCont.setupControlCallback(self.xboxCont.XboxControls.RTHUMBY, self.RthumbY)


        #start the controller
        self.xboxCont.start()

        self.running = True

    #call back funtions for left thumb stick    
    def aButtonCallBack(self,value):
   #     self.data_status = not self.data_status
        self.motor_collect()

    def backButton(self, value):
        self.stop()
        
    def LthumbY(self,value):
        self.motor1.setVelocity(value)
    #   if self.data_status:
        self.file.write(str(time.time()) + ", " + "left, " + str(value)  + "\n")
    
    def RthumbY(self,value):
        self.motor2.setVelocity(value)
    #   if self.data_status:
        self.file.write(str(time.time()) + ", " + "right, " + str(value) + "\n")


    def run_neural_net(self,data):
        motor_command = self.net.activate(data)
        left_speed = motor_command[0]
        right_speed = motor_command[1]

        self.motor1.setVelocity(left_speed)
        self.motor2.setVelocity(right_speed)

    def turn_left(self, val):
            bot.motor1.setVelocity(-val)
            bot.motor2.setVelocity(val)

    def turn_right(self, val):
            bot.motor1.setVelocity(val)
            bot.motor2.setVelocity(-val)

    def follow_right(self,dist):
        #if error is positive,too far, turn right
        #if error is negative,too close, turn left
        desired = 20
        ykp = 0.05
        xkp = 0.05
        error = dist - desired
        max = 0.3 
        if error > 0:
            right = max - ykp*error
            left = max
        else:
            right = max
            left = max - xkp*error

        self.motor1.setVelocity(left)
        self.motor2.setVelocity(right)
       # starttime = time.time()
       # while time.time() - starttime < 1:
       #    pass

       #self.motor1.setVelocity(0)
       #self.motor2.setVelocity(0)
        print str(dist) + ", " + str(right) + " " + str(left)

    def check_left_dist(self):
        d1 = self.mcp.readDistance(4) + 7.45
        d2 = self.mcp.readDistance(5) + 7.45
        theta = math.pi/4
        h = d1*d2*math.sin(theta) / math.sqrt(math.pow(d1,2) + math.pow(d2,2) - 2*d1*d2*math.cos(theta))
        return h

    def angle_target(self,current,target):
        current = float(current)
        target = float(target)
        if abs(current-target) == 180.:
            return "right"
        elif 0 < current < 180:
            if target > current + 180 or 0 <= target < current:
                return "left"
            else:
                return "right"

        elif 180 < current <= 359:
            if current < target <= 359 or 0 <= target < current - 180:
                return "right"
            else:
                return "left"
    def stop_motors(self):
        self.motor1.setVelocity(0)
        self.motor2.setVelocity(0)



    def stop(self):
        #GPIO.cleanup()
        self.file.close()
        self.xboxCont.stop()
        self.running = False




if __name__ == '__main__':
    print ("started")
    try:
        #create class
        bot = VeggieBot()
        while bot.running:
           # bot.data.append([bot.motor1.returnVelocity()])
            time.sleep(0.02)
            target = float(raw_input("target: "))
            current = bot.sense.readAngle()
            error = abs(current - target)
            while error > 2:
                direc = bot.angle_target(current,target)
                print direc
                if direc is "right":
                    bot.turn_right(0.3)
                else:
                    bot.turn_left(0.3)
                time.sleep(0.02)
                current = bot.sense.readAngle()
                error = abs(current - target)
                print current
            bot.stop_motors()
                
            
        #    print bot.check_left_dist()
        #    a = bot.mcp.readDistance(0)     
        #    command = raw_input("num: ")
        #    a = bot.sonic1.readDistance()
        #    b = bot.sonic2.readDistance()
        #    c = bot.sonic3.readDistance()
        #    d = bot.sonic4.readDistance()
        #    e = bot.sonic5.readDistance()
        #    data = str(a) 
        #    data = str(time.time()) + ", " + str(a) + ", " +  str(b) + ", " +  str(c) + ", " +  str(d) + ", " + str(e) + "\n"
        #    print data
        #    bot.run_neural_net([(x*0.008 - 1) if x <= 250 else 1 for x in [a,b,c,d,e]])
        #    print bot.mcp.readVolts(0)
        #    bot.follow_right_wall(e)
        #    bot.follow_right(a)
        #    bot.motor1.setVelocity(float(command))
        #    bot.file.write(data)
        GPIO.cleanup()
       # print bot.data

    #Ctrl C
    except KeyboardInterrupt:
        bot.xboxCont.stop()
        bot.file.close()
        GPIO.cleanup()
        print "User cancelled"
        i = input("Keep File? (1 no) ")
        if i == 1:
            os.remove(bot.wpath)
            print("File Removed")

    #Error
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    
