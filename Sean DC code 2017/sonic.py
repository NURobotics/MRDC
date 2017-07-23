import RPi.GPIO as GPIO
import time

class Sonic:

	def __init__(self, trig, echo):
		#setup
		self.TRIG = trig
		self.ECHO = echo

		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.TRIG, GPIO.OUT)
		GPIO.setup(self.ECHO, GPIO.IN)

	def readDistance(self):
        
	        dthreshold = 250.
	#	dtthreshold = 0.1749
        
	        dtthreshold = dthreshold / 17150
	#	dtthreshold = 0.008
		GPIO.output(self.TRIG, False)
		time.sleep(0.01)
		GPIO.output(self.TRIG, True)
		time.sleep(0.00001)
		GPIO.output(self.TRIG, False)
		
                find_pulse_start = time.time()
                pulse_start = -1
		while GPIO.input(self.ECHO) == 0:
		
			pulse_start = time.time()
			if pulse_start - find_pulse_start >= 0.5:
#0.00044
				print "broke 1"
                                return dthreshold # no pulse found
                if pulse_start == -1:
                        return dthreshold

		while GPIO.input(self.ECHO) == 1:
		
			pulse_duration = time.time() - pulse_start
			if pulse_duration >= dtthreshold:
		#		print "broke 2"
                                break

	
		distance = pulse_duration * 17150
		distance = round(distance,2)
#		print pulse_duration
#		print distance
		return distance


if __name__=='__main__':
	sensor = Sonic(13,6)
	while(True):
		print sensor.readDistance()
	
