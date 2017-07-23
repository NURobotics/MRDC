import RPi.GPIO as GPIO
import time
import sys
import math


#map from xbox controller to duty cycle
def valmap(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

#class for setting velocity of motors
class Motor:

    def __init__(self, enable, direction):
        self.enable = enable
        self.direction = direction
        self.vel = 0;

        #setup pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(enable, GPIO.OUT)
        GPIO.setup(direction, GPIO.OUT)

        self.pwm = GPIO.PWM(enable, 100)
        self.pwm.start(0)

    def setVelocity(self, value):
        if value < -1:
            value = -1
        if value > 1:
            value = 1
        self.vel = valmap(value, -1, 1, -100, 100)
	#print self.vel
        if (self.vel > 0):
            self.pwm.ChangeDutyCycle(self.vel)
            GPIO.output(self.direction, GPIO.HIGH)
        else:
            self.pwm.ChangeDutyCycle(-self.vel)
            GPIO.output(self.direction, GPIO.LOW)


    def returnVelocity(self):
        return self.vel

       

if __name__=='__main__':
    left_motor = Motor(19,20)
    right_motor = Motor(26,21)
    start_time = time.time()
    while time.time() - start_time < 1:
        left_motor.setVelocity(1)
        right_motor.setVelocity(1)

   # left_motor.setVelocity(0)
   # right_motor.setVelocity(0)

